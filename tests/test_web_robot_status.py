"""Exercise the metadata route and real session gate without importing robot hardware.

The endpoint is compiled from its source AST into an inert FastAPI application;
the production lifespan (which initializes hardware) is never imported or run.
Run with a development Python containing FastAPI, Starlette and httpx.
"""

import ast
import asyncio
import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace

from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
SESSION_ID = "a" * 43


def load_session_module():
    spec = importlib.util.spec_from_file_location(
        "inert_web_sessions", ROOT / "ninja_core/src/ninja_core/web_sessions.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Socket:
    def __init__(self):
        self.cookies = {"ninja_web_session": SESSION_ID}

    async def accept(self):
        pass

    async def send_json(self, value):
        pass


class RobotStatusTests(unittest.TestCase):
    def setUp(self):
        sessions = load_session_module()
        self.manager = sessions.WebSessionManager()
        self.socket = Socket()
        self.state = SimpleNamespace(
            hal=SimpleNamespace(config=SimpleNamespace(robot_type="spider")),
            web_sessions=self.manager,
            shutdown_event=asyncio.Event(),
        )
        app = FastAPI()
        app.state.ninja = self.state
        app.add_middleware(sessions.WebSessionMiddleware)
        router = APIRouter(prefix="/api")
        tree = ast.parse((ROOT / "ninja_core/src/ninja_core/web_server.py").read_text())
        endpoint = next(node for node in tree.body if getattr(node, "name", "") == "robot_status")
        namespace = {"api_router": router, "Request": Request, "HTTPException": HTTPException}
        # Execute only the reviewed local endpoint AST, never the hardware lifespan.
        exec(compile(ast.Module(body=[endpoint], type_ignores=[]), "web_server.py", "exec"), namespace)  # noqa: S102
        app.include_router(router)
        self.client = TestClient(app)
        self.client.cookies.set(sessions.SESSION_COOKIE, SESSION_ID)

    def tearDown(self):
        self.client.close()

    def connect(self):
        asyncio.run(self.manager.connect(self.socket))

    def test_each_type_is_returned_without_configuration_or_hardware_access(self):
        self.connect()
        for robot_type in ("tire", "humanoid", "spider"):
            with self.subTest(robot_type=robot_type):
                self.state.hal.config.robot_type = robot_type
                response = self.client.get("/api/robot/status")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), {"robot_type": robot_type})

    def test_inactive_and_other_browser_cannot_read_metadata(self):
        self.assertEqual(self.client.get("/api/robot/status").status_code, 423)
        self.connect()
        self.client.cookies.set("ninja_web_session", "b" * 43)
        self.assertEqual(self.client.get("/api/robot/status").status_code, 423)

    def test_missing_hal_and_shutdown_report_unavailable(self):
        self.connect()
        self.state.hal = None
        self.assertEqual(self.client.get("/api/robot/status").status_code, 503)
        self.state.shutdown_event.set()
        self.assertEqual(self.client.get("/api/robot/status").status_code, 503)


if __name__ == "__main__":
    unittest.main()
