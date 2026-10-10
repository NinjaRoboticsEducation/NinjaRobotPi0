"""Single-browser ownership for HTTP actions and persistent browser sockets."""

from __future__ import annotations

import asyncio
import logging
import re
import secrets
from contextvars import ContextVar

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

log = logging.getLogger(__name__)
SESSION_COOKIE = "ninja_web_session"
SESSION_CONTEXT = ContextVar("ninja_web_session", default=None)
SESSION_GENERATION = ContextVar("ninja_web_generation", default=None)
HEARTBEAT_TIMEOUT = 35


def valid_session_id(value):
    return isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9_-]{43}", value) is not None


class WebSessionManager:
    """One browser identity, allowing its tabs; cleanup precedes handoff."""

    def __init__(self, on_connect=None, on_disconnect=None):
        self._owner = None
        self.generation = None
        self._connections = set()
        self._auxiliary = set()
        self._requests = set()
        self._lock = asyncio.Lock()
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect

    @property
    def connected(self):
        return bool(self._connections)

    def owns(self, session_id):
        return bool(self._connections) and session_id == self._owner

    async def connect(self, websocket):
        session_id = websocket.cookies.get(SESSION_COOKIE)
        async with self._lock:
            if not valid_session_id(session_id):
                await websocket.close(code=4401)
                return False
            await websocket.accept()
            if self._owner is not None and self._owner != session_id:
                await websocket.send_json({"type": "session", "status": "busy"})
                await websocket.close(code=4409)
                return False
            first = not self._connections
            if first:
                self.generation = secrets.token_hex(16)
            self._owner = session_id
            self._connections.add(websocket)
            try:
                if first and self.on_connect:
                    await self.on_connect()
                await websocket.send_json({"type": "session", "status": "connected"})
            except BaseException:
                self._connections.discard(websocket)
                if not self._connections:
                    self._owner = None
                    if self.on_disconnect:
                        await self.on_disconnect()
                raise
            return True

    async def accept_auxiliary(self, websocket):
        async with self._lock:
            if not self.owns(websocket.cookies.get(SESSION_COOKIE)):
                await websocket.close(code=4409)
                return False
            await websocket.accept()
            self._auxiliary.add(websocket)
            return True

    def remove_auxiliary(self, websocket):
        self._auxiliary.discard(websocket)

    def begin_request(self, session_id, task):
        if not self.owns(session_id):
            return False
        self._requests.add(task)
        return True

    def end_request(self, task):
        self._requests.discard(task)

    async def run_when_idle(self, callback):
        async with self._lock:
            if not self.connected:
                return await callback()

    async def disconnect(self, websocket):
        async with self._lock:
            if websocket not in self._connections:
                return
            self._connections.remove(websocket)
            if self._connections:
                return
            # owns() becomes false now, so late callbacks cannot operate the robot.
            # Keep _owner reserved until all cleanup has finished.
            try:
                for task in tuple(self._requests):
                    if task is not asyncio.current_task():
                        task.cancel()
                for socket in tuple(self._auxiliary):
                    try:
                        await asyncio.wait_for(socket.close(code=1000), timeout=1)
                    except Exception:
                        log.debug("Auxiliary socket already closed", exc_info=True)
                self._auxiliary.clear()
                if self.on_disconnect:
                    await self.on_disconnect()
            finally:
                self._owner = None


def session_active(state):
    """Thread-offloaded HTTP actions inherit the request's ownership context."""
    session_id = SESSION_CONTEXT.get()
    manager = getattr(state, "web_sessions", None)
    if session_id is None:
        return True  # Internal, non-browser operations retain existing behavior.
    shutdown = getattr(state, "shutdown_event", None)
    if shutdown is not None and shutdown.is_set():
        return False
    generation = SESSION_GENERATION.get()
    return manager is not None and manager.owns(session_id) and (
        generation is None or generation == manager.generation
    )


class WebSessionMiddleware:
    """Issue an opaque cookie; require its live primary socket for every API."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        request = Request(scope)
        session_id = request.cookies.get(SESSION_COOKIE)
        state = getattr(scope["app"].state, "ninja", None)
        manager = getattr(state, "web_sessions", None)
        task = asyncio.current_task()
        if scope["path"].startswith("/api/"):
            shutdown = getattr(state, "shutdown_event", None)
            if shutdown is not None and shutdown.is_set():
                response = JSONResponse({"detail": "Robot is shutting down."}, status_code=503)
                await response(scope, receive, send)
                return
            if manager is None or not manager.begin_request(session_id, task):
                response = JSONResponse(
                    {"detail": "Robot is in use or no active browser session is connected."},
                    status_code=423,
                )
                await response(scope, receive, send)
                return
            context = SESSION_CONTEXT.set(session_id)
            generation = SESSION_GENERATION.set(manager.generation)
            try:
                await self.app(scope, receive, send)
            finally:
                SESSION_CONTEXT.reset(context)
                SESSION_GENERATION.reset(generation)
                manager.end_request(task)
            return
        # HTML navigation issues the cookie before the browser opens its socket.
        cookie = None
        if request.method == "GET" and not valid_session_id(session_id):
            response = Response()
            response.set_cookie(
                SESSION_COOKIE, secrets.token_urlsafe(32), httponly=True,
                samesite="strict", secure=request.url.scheme == "https", path="/",
            )
            cookie = response.raw_headers[-1]

        async def send_with_cookie(message):
            if cookie and message["type"] == "http.response.start":
                message = {**message, "headers": [*message.get("headers", []), cookie]}
            await send(message)

        await self.app(scope, receive, send_with_cookie)
