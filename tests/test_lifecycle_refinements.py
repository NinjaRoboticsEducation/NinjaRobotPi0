"""Exit, browser ownership and reconnect behavior with inert hardware only."""

import asyncio
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from starlette.websockets import WebSocketDisconnect

from ninja_core.config import NinjaConfig
from ninja_core.builtin_movements import MovementValidationError
from ninja_core.runtime_pipeline import RuntimePipeline
from ninja_core.web_sessions import (
    SESSION_CONTEXT, SESSION_COOKIE, SESSION_GENERATION,
    WebSessionManager, WebSessionMiddleware,
    session_active,
)


class Socket:
    def __init__(self, identity="a" * 43):
        self.cookies = {SESSION_COOKIE: identity}
        self.events = []

    async def accept(self):
        self.events.append("accept")

    async def send_json(self, value):
        self.events.append(value)

    async def close(self, code=1000):
        self.events.append(("close", code))


def run(coro):
    return asyncio.run(coro)


@pytest.mark.parametrize("pose", ["Poweroff", "home"])
def test_cli_exit_pose_precedes_shutdown_without_centering(monkeypatch, pose):
    from ninja_core import movement_cli

    calls = []
    config = NinjaConfig(movements={pose: []})
    hal = SimpleNamespace(
        servos=SimpleNamespace(center_all=lambda: calls.append("startup-center")),
        initialize=lambda **kwargs: calls.append("init"),
        shutdown=lambda: calls.append("shutdown"),
    )
    ctrl = SimpleNamespace(
        execute_movement=lambda name: calls.append(name),
        center_all_servos=lambda: pytest.fail("Exit must not center after final pose"),
    )
    monkeypatch.setattr(movement_cli, "load_config", lambda: config)
    monkeypatch.setattr(movement_cli, "HardwareAbstractionLayer", lambda _: hal)
    monkeypatch.setattr(movement_cli, "MovementController", lambda *_: ctrl)
    monkeypatch.setattr(movement_cli, "save_config", lambda _: calls.append("save"))
    monkeypatch.setattr(movement_cli.time, "sleep", lambda _: None)
    monkeypatch.setattr("builtins.input", lambda _: "6")
    movement_cli.run_cli()
    assert calls == ["init", "startup-center", pose, "shutdown", "save"]


@pytest.mark.parametrize("failure", ["initialization", "pose", "keyboard"])
def test_cli_failure_releases_hardware_and_saves_without_recovery_moves(monkeypatch, failure):
    from ninja_core import movement_cli

    calls = []
    config = NinjaConfig(movements={"Poweroff": []})

    def initialize(**kwargs):
        if failure == "initialization":
            raise RuntimeError("inert initialization failure")

    def execute(name):
        calls.append(name)
        raise MovementValidationError("inert invalid movement")

    def ask(_):
        if failure == "keyboard":
            raise KeyboardInterrupt
        return "6"

    hal = SimpleNamespace(servos=None, initialize=initialize, shutdown=lambda: calls.append("shutdown"))
    ctrl = SimpleNamespace(execute_movement=execute)
    monkeypatch.setattr(movement_cli, "load_config", lambda: config)
    monkeypatch.setattr(movement_cli, "HardwareAbstractionLayer", lambda _: hal)
    monkeypatch.setattr(movement_cli, "MovementController", lambda *_: ctrl)
    monkeypatch.setattr(movement_cli, "save_config", lambda _: calls.append("save"))
    monkeypatch.setattr("builtins.input", ask)
    if failure == "pose":
        movement_cli.run_cli()
        assert calls == ["Poweroff", "shutdown", "save"]
    else:
        with pytest.raises(RuntimeError if failure == "initialization" else KeyboardInterrupt):
            movement_cli.run_cli()
        assert calls == ["shutdown", "save"]


def test_simultaneous_browsers_have_one_owner_and_busy_reply():
    async def scenario():
        manager = WebSessionManager()
        first, other = Socket(), Socket("b" * 43)
        results = await asyncio.gather(manager.connect(first), manager.connect(other))
        assert results == [True, False]
        assert manager.owns("a" * 43)
        assert not manager.owns("b" * 43)
        assert {"type": "session", "status": "busy"} in other.events
        assert ("close", 4409) in other.events
    run(scenario())


def test_last_tab_disconnect_restores_screen_and_allows_new_browser():
    async def scenario():
        calls = []

        async def connected():
            calls.append("connected")

        async def disconnected():
            calls.append("QR")

        manager = WebSessionManager(connected, disconnected)
        first, tab, other = Socket(), Socket(), Socket("b" * 43)
        assert await manager.connect(first)
        assert await manager.connect(tab)
        await manager.disconnect(first)
        assert calls == ["connected"]
        await manager.disconnect(tab)
        assert calls == ["connected", "QR"]
        await manager.disconnect(tab)  # Idempotent cleanup.
        assert await manager.connect(other)
        assert calls == ["connected", "QR", "connected"]
    run(scenario())


def test_disconnect_cleanup_is_serialized_before_handoff():
    async def scenario():
        started, finish = asyncio.Event(), asyncio.Event()

        async def cleanup():
            started.set()
            await finish.wait()

        manager = WebSessionManager(on_disconnect=cleanup)
        first, other = Socket(), Socket("b" * 43)
        await manager.connect(first)
        closing = asyncio.create_task(manager.disconnect(first))
        await started.wait()
        opening = asyncio.create_task(manager.connect(other))
        await asyncio.sleep(0)
        assert not opening.done()
        assert not manager.owns("a" * 43)
        finish.set()
        await closing
        assert await opening
    run(scenario())


def test_cleanup_failure_does_not_leak_ownership():
    async def scenario():
        async def cleanup():
            raise RuntimeError("inert display failure")

        manager = WebSessionManager(on_disconnect=cleanup)
        first = Socket()
        await manager.connect(first)
        with pytest.raises(RuntimeError):
            await manager.disconnect(first)
        assert not manager.connected
        assert await manager.connect(Socket("b" * 43))
    run(scenario())


def test_auxiliary_socket_authorization_and_disconnect_close():
    async def scenario():
        manager = WebSessionManager()
        first, auxiliary, stranger = Socket(), Socket(), Socket("b" * 43)
        assert not await manager.accept_auxiliary(auxiliary)
        await manager.connect(first)
        assert await manager.accept_auxiliary(auxiliary)
        assert not await manager.accept_auxiliary(stranger)
        await manager.disconnect(first)
        assert ("close", 1000) in auxiliary.events
    run(scenario())


def test_missing_cookie_is_rejected_before_acceptance():
    async def scenario():
        manager = WebSessionManager()
        socket = Socket("invalid")
        assert not await manager.connect(socket)
        assert socket.events == [("close", 4401)]
    run(scenario())


def test_thread_action_context_loses_access_after_disconnect():
    async def scenario():
        manager = WebSessionManager()
        socket = Socket()
        state = SimpleNamespace(web_sessions=manager)
        await manager.connect(socket)
        token = SESSION_CONTEXT.set("a" * 43)
        try:
            assert await asyncio.to_thread(session_active, state)
            await manager.disconnect(socket)
            assert not await asyncio.to_thread(session_active, state)
            await manager.connect(Socket("b" * 43))
            assert not session_active(state)
        finally:
            SESSION_CONTEXT.reset(token)
    run(scenario())


async def middleware_request(manager, path="/api/test", identity=None, endpoint=None):
    messages = []
    state = SimpleNamespace(ninja=SimpleNamespace(web_sessions=manager))
    scope = {
        "type": "http", "method": "GET", "path": path, "raw_path": path.encode(),
        "query_string": b"", "scheme": "http", "http_version": "1.1",
        "server": ("test", 80), "client": ("127.0.0.1", 1),
        "headers": [(b"cookie", f"{SESSION_COOKIE}={identity}".encode())] if identity else [],
        "app": SimpleNamespace(state=state),
    }

    async def app(scope, receive, send):
        if endpoint:
            await endpoint()
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"OK"})

    async def send(message):
        messages.append(message)

    await WebSessionMiddleware(app)(scope, None, send)
    return messages


def test_same_browser_reconnect_cannot_reactivate_old_thread_context():
    async def scenario():
        manager = WebSessionManager()
        state = SimpleNamespace(web_sessions=manager, shutdown_event=asyncio.Event())
        socket = Socket()
        await manager.connect(socket)
        token = SESSION_CONTEXT.set("a" * 43)
        generation = SESSION_GENERATION.set(manager.generation)
        try:
            assert session_active(state)
            await manager.disconnect(socket)
            await manager.connect(Socket())
            assert not await asyncio.to_thread(session_active, state)
        finally:
            SESSION_CONTEXT.reset(token)
            SESSION_GENERATION.reset(generation)
    run(scenario())


def test_shutdown_invalidates_browser_actions_but_not_internal_poweroff():
    async def scenario():
        manager = WebSessionManager()
        state = SimpleNamespace(web_sessions=manager, shutdown_event=asyncio.Event())
        await manager.connect(Socket())
        token = SESSION_CONTEXT.set("a" * 43)
        try:
            assert session_active(state)
            state.shutdown_event.set()
            assert not session_active(state)
        finally:
            SESSION_CONTEXT.reset(token)
        assert session_active(state)
    run(scenario())


def test_middleware_issues_cookie_and_rejects_unowned_api():
    async def scenario():
        manager = WebSessionManager()
        response = await middleware_request(manager, path="/")
        cookie = dict(response[0]["headers"])[b"set-cookie"].decode()
        assert "HttpOnly" in cookie and "SameSite=strict" in cookie
        assert response[0]["status"] == 200
        called = Mock()
        response = await middleware_request(manager, endpoint=called)
        assert response[0]["status"] == 423
        called.assert_not_called()
        await manager.connect(Socket())
        assert (await middleware_request(manager, identity="a" * 43))[0]["status"] == 200
        assert (await middleware_request(manager, identity="b" * 43))[0]["status"] == 423
    run(scenario())


def test_disconnect_cancels_pending_http_request():
    async def scenario():
        manager = WebSessionManager()
        socket = Socket()
        await manager.connect(socket)
        started = asyncio.Event()

        async def endpoint():
            started.set()
            await asyncio.Event().wait()

        pending = asyncio.create_task(middleware_request(manager, identity="a" * 43, endpoint=endpoint))
        await started.wait()
        await manager.disconnect(socket)
        with pytest.raises(asyncio.CancelledError):
            await pending
        assert not manager._requests
    run(scenario())


def test_pipeline_does_not_restore_idle_over_waiting_qr():
    faces = Mock()
    pipeline = RuntimePipeline(faces=faces)
    pipeline.set_web_waiting(True)
    pipeline.begin_blockly()
    pipeline.complete_blockly("success")
    pipeline.abort_blockly()
    faces.play.assert_not_called()
    pipeline.set_web_waiting(False)
    faces.play.assert_called_once_with("idle", duration_s=float("inf"))


def web_state():
    from ninja_core.web_server import AppState
    state = AppState()
    state.hal = SimpleNamespace(display=Mock(width=240, height=320), servos=Mock())
    state.faces = Mock()
    state.sound = Mock()
    state.runtime_pipeline = RuntimePipeline(hal=state.hal, faces=state.faces)
    state.public_url = "https://inert.example.test"
    return state


def test_disconnect_restores_qr_with_suppressed_idle_and_abort():
    async def scenario():
        state = web_state()
        socket = Socket()
        await state.web_sessions.connect(socket)
        state.faces.reset_mock()
        await state.web_sessions.disconnect(socket)
        state.hal.servos.abort.assert_called_once()
        state.sound.stop.assert_called_once_with(restart_buzzer=True)
        state.faces.play.assert_not_called()
        image = state.hal.display.display.call_args.args[0]
        assert image.size == (240, 320)
        assert image.getpixel((0, 0)) == (255, 255, 255)
    run(scenario())


def test_shutdown_disconnect_does_not_redraw_qr_or_abort_poweroff():
    async def scenario():
        state = web_state()
        socket = Socket()
        await state.web_sessions.connect(socket)
        state.shutdown_event.set()
        await state.web_sessions.disconnect(socket)
        state.hal.servos.abort.assert_not_called()
        state.hal.display.display.assert_not_called()
    run(scenario())


@pytest.mark.parametrize("missing", [False, True])
def test_failed_or_missing_display_still_releases_owner(missing):
    async def scenario():
        state = web_state()
        if missing:
            state.hal.display = None
        else:
            state.hal.display.display.side_effect = RuntimeError("inert display failure")
        socket = Socket()
        await state.web_sessions.connect(socket)
        await state.web_sessions.disconnect(socket)
        assert not state.web_sessions.connected
        assert await state.web_sessions.connect(Socket("b" * 43))
    run(scenario())


def test_primary_socket_receives_close_and_cleans_up():
    from ninja_core.web_server import websocket_session

    async def scenario():
        state = web_state()
        socket = Socket()
        socket.app = SimpleNamespace(state=SimpleNamespace(ninja=state))

        async def closed():
            raise WebSocketDisconnect()

        socket.receive_text = closed
        await websocket_session(socket)
        assert not state.web_sessions.connected
        state.hal.display.display.assert_called_once()
    run(scenario())


def test_primary_socket_heartbeat_timeout_releases_owner(monkeypatch):
    from ninja_core import web_server

    async def scenario():
        state = web_state()
        socket = Socket()
        socket.app = SimpleNamespace(state=SimpleNamespace(ninja=state))
        socket.receive_text = asyncio.Event().wait
        monkeypatch.setattr(web_server, "HEARTBEAT_TIMEOUT", 0.001)
        await web_server.websocket_session(socket)
        assert ("close", 4408) in socket.events
        assert not state.web_sessions.connected
    run(scenario())


def test_stale_action_plan_cannot_write_or_reset_outputs():
    from ninja_core.web_server import execute_action_plan

    state = web_state()
    state.movement = Mock()
    token = SESSION_CONTEXT.set("a" * 43)
    try:
        run(execute_action_plan(state, {"movement": "Poweroff", "face": "happy", "sound": "happy"}))
    finally:
        SESSION_CONTEXT.reset(token)
    state.movement.execute_movement.assert_not_called()
    state.movement.center_all_servos.assert_not_called()
    state.faces.play.assert_not_called()
    state.sound.play.assert_not_called()


def test_disconnect_during_action_chain_does_not_center_afterward():
    from ninja_core.web_server import execute_action_plan

    async def scenario():
        state = web_state()
        state.movement = Mock()
        socket = Socket()
        await state.web_sessions.connect(socket)

        async def action_chain(_):
            await state.web_sessions.disconnect(socket)

        state.dispatcher = SimpleNamespace(execute_action_chain=action_chain, safe_executor=None)
        token = SESSION_CONTEXT.set("a" * 43)
        try:
            await execute_action_plan(state, {"action": "test"})
        finally:
            SESSION_CONTEXT.reset(token)
        state.movement.center_all_servos.assert_not_called()
    run(scenario())


def test_queued_centering_checks_abort_before_driver_write():
    import threading
    from ninja_core.movement_controller import MovementController, EmergencyStop

    driver = Mock(pins=[20])
    controller = MovementController(SimpleNamespace(servos=driver), NinjaConfig())
    controller.servo_definitions = {"20": {}}
    controller._motion_lock = threading.RLock()
    with pytest.raises(EmergencyStop):
        controller.center_all_servos(abort_check=lambda: True)
    driver.move_all_sync.assert_not_called()


def test_reconnect_qr_uses_lan_fallback_and_skips_occupied_display():
    from ninja_core.web_server import show_reconnect_qr

    async def scenario():
        state = web_state()
        state.public_url = None
        state.local_url = "http://192.0.2.1:8000"
        assert show_reconnect_qr(state)
        state.hal.display.display.reset_mock()
        await state.web_sessions.connect(Socket())
        assert not show_reconnect_qr(state)
        state.hal.display.display.assert_not_called()
    run(scenario())
