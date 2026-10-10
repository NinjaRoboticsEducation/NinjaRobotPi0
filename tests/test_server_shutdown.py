"""Shutdown regression tests with inert connections and no robot/server startup."""

import asyncio
import signal
import threading
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from ninja_core import web_server
from ninja_core.config import NinjaConfig


def make_state(monkeypatch, *, movement_failure=False):
    calls = []
    state = web_server.AppState()
    connection = SimpleNamespace(open=True)

    def move(name):
        assert connection.open, "Servo write attempted after connection release"
        calls.append(name)
        if movement_failure:
            raise RuntimeError("inert failed pose")

    def release():
        assert connection.open, "Repeated HAL shutdown"
        calls.append("release")
        connection.open = False

    state.movement = SimpleNamespace(execute_movement=move)
    state.hal = SimpleNamespace(servos=None, shutdown=release)
    monkeypatch.setattr(web_server.time, "sleep", lambda _: None)
    return state, calls


def test_shared_shutdown_is_once_and_pose_precedes_release(monkeypatch):
    async def scenario():
        state, calls = make_state(monkeypatch)
        state.agent = SimpleNamespace(cancel_pending=lambda: calls.append("invalidate"))
        await asyncio.gather(
            web_server._shutdown_robot(state), web_server._shutdown_robot(state)
        )
        await web_server._shutdown_robot(state)
        assert state.shutdown_event.is_set()
        assert calls == ["invalidate", "Poweroff", "release"]

    asyncio.run(scenario())


def test_pose_failure_still_releases_hardware_once(monkeypatch, capsys):
    async def scenario():
        state, calls = make_state(monkeypatch, movement_failure=True)
        await web_server._shutdown_robot(state)
        await web_server._shutdown_robot(state)
        assert calls == ["Poweroff", "release"]

    asyncio.run(scenario())
    assert "Poweroff movement failed" in capsys.readouterr().out


def test_shutdown_waits_for_action_lock_before_pose_and_release(monkeypatch):
    async def scenario():
        state, calls = make_state(monkeypatch)
        state.action_plan_lock = asyncio.Lock()
        await state.action_plan_lock.acquire()
        task = asyncio.create_task(web_server._shutdown_robot(state))
        await asyncio.sleep(0.1)
        assert calls == []
        state.action_plan_lock.release()
        await task
        assert calls == ["Poweroff", "release"]

    asyncio.run(scenario())


def test_canceled_caller_does_not_release_connection_during_pose(monkeypatch):
    async def scenario():
        state, calls = make_state(monkeypatch)
        entered, finish = threading.Event(), threading.Event()
        original = state.movement.execute_movement

        def movement(name):
            entered.set()
            assert finish.wait(2)
            original(name)

        state.movement.execute_movement = movement
        task = asyncio.create_task(web_server._shutdown_robot(state))
        assert await asyncio.to_thread(entered.wait, 2)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert calls == []
        finish.set()
        await web_server._shutdown_robot(state)
        assert calls == ["Poweroff", "release"]

    asyncio.run(scenario())


def test_uncooperative_executor_prevents_conflicting_pose(monkeypatch):
    async def scenario():
        state, calls = make_state(monkeypatch)
        monkeypatch.setattr(
            web_server,
            "interrupt_active_robot_action",
            AsyncMock(return_value={"still_running": True}),
        )
        await web_server._shutdown_robot(state)
        assert calls == ["release"]

    asyncio.run(scenario())


def test_web_poweroff_and_lifespan_share_shutdown_and_single_os_command(monkeypatch):
    async def scenario():
        state, calls = make_state(monkeypatch)
        request = SimpleNamespace(
            app=SimpleNamespace(state=SimpleNamespace(ninja=state))
        )
        monkeypatch.setattr(
            web_server.subprocess, "run", lambda args, **kw: calls.append(tuple(args))
        )
        await web_server.system_shutdown(request)
        await web_server.system_shutdown(request)
        await asyncio.gather(
            state.system_shutdown_task, web_server._shutdown_robot(state)
        )
        assert calls == ["Poweroff", "release", ("sudo", "shutdown", "-h", "now")]

    asyncio.run(scenario())


@pytest.mark.parametrize("exit_signal", [signal.SIGINT, signal.SIGTERM])
def test_uvicorn_signal_replay_does_not_move_after_lifespan_release(
    monkeypatch, exit_signal
):
    """Exercise actual Uvicorn capture/replay, with every startup dependency inert."""
    from ninja_core import dispatcher
    from ninja_ble import service
    import uvicorn

    state, calls = make_state(monkeypatch)
    monkeypatch.setattr(web_server, "AppState", lambda: state)
    state.hal.initialize = Mock()
    monkeypatch.setattr(web_server, "HardwareAbstractionLayer", lambda _: state.hal)
    monkeypatch.setattr(web_server, "load_config", lambda: NinjaConfig())
    monkeypatch.setattr(web_server, "RuntimePipeline", lambda _: Mock(mode="native"))
    inert_dispatcher = Mock()
    inert_dispatcher.safe_executor.is_running.return_value = False
    monkeypatch.setattr(
        dispatcher, "CommandDispatcher", lambda *a, **kw: inert_dispatcher
    )
    monkeypatch.setattr(web_server, "AnimatedFaces", lambda _: None)
    monkeypatch.setattr(web_server, "RobotSoundPlayer", lambda _: None)
    monkeypatch.setattr(web_server, "MovementController", lambda *_: state.movement)
    monkeypatch.setattr(web_server, "DistanceMonitor", lambda _: Mock())
    monkeypatch.setattr(
        service,
        "NinjaBLEService",
        lambda *a, **kw: SimpleNamespace(
            start=AsyncMock(), stop=AsyncMock(), is_running=False
        ),
    )
    monkeypatch.setattr(
        web_server, "NinjaAgent", Mock(side_effect=web_server.MissingAPIKeyError())
    )
    monkeypatch.setattr(web_server, "setup_network_and_display", AsyncMock())
    monkeypatch.setattr(web_server.ngrok, "kill", Mock())
    monkeypatch.setattr(web_server, "check_port_available", lambda *_: True)
    monkeypatch.setattr(web_server, "has_ngrok_auth_token", lambda: True)
    original = signal.getsignal(exit_signal)

    def replay(sig):
        handler = signal.getsignal(sig)
        if callable(handler):
            handler(sig, None)
        else:
            raise SystemExit(0)

    def inert_uvicorn_run(*args, **kwargs):
        server = uvicorn.Server(uvicorn.Config(web_server.app))
        with server.capture_signals():

            async def lifecycle():
                async with web_server.lifespan(web_server.app):
                    server.handle_exit(exit_signal, None)

            asyncio.run(lifecycle())

    monkeypatch.setattr(signal, "raise_signal", replay)
    monkeypatch.setattr(web_server.uvicorn, "run", inert_uvicorn_run)
    try:
        web_server.run_server(autostart=True)
        assert signal.getsignal(exit_signal) is original
        assert calls == ["Poweroff", "release"]
    finally:
        signal.signal(exit_signal, original)
