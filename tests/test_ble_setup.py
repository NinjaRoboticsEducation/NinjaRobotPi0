"""Bluetooth readiness with inert systemd/radio/D-Bus only."""

import asyncio
import importlib.util
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest
from dbus_next import Variant

from ninja_ble import system_setup as ble

ROOT = Path(__file__).resolve().parents[1]


def objects(*, powered=True, active=0, available=1, gatt=True):
    interfaces = {
        ble.ADAPTER: {"Powered": Variant("b", powered)},
        ble.ADVERTISING: {
            "ActiveInstances": Variant("y", active),
            "SupportedInstances": Variant("y", available),
        },
    }
    if gatt:
        interfaces[ble.GATT] = {}
    return {"/org/bluez/hci0": interfaces}


@pytest.fixture
def fixture(monkeypatch):
    monkeypatch.setattr(ble, "supported_host", lambda: True)
    monkeypatch.setattr(ble, "radio_blocks", lambda: (False, False))
    monkeypatch.setattr(ble, "legacy_uart_available", lambda: False)
    unit = AsyncMock(
        return_value={
            "LoadState": "loaded",
            "ActiveState": "active",
            "UnitFileState": "enabled",
        }
    )
    command = AsyncMock(return_value="")
    monkeypatch.setattr(ble, "unit_state", unit)
    monkeypatch.setattr(ble, "command", command)
    session = SimpleNamespace(
        connect=AsyncMock(),
        objects=AsyncMock(return_value=objects()),
        power_on=AsyncMock(),
        probe=AsyncMock(),
        close=Mock(),
    )
    return unit, command, session


def prepare(fixture, repair=False):
    return asyncio.run(
        ble.prepare_bluetooth(repair=repair, session_factory=lambda: fixture[2])
    )


@pytest.mark.parametrize("repair", [False, True])
def test_healthy_checks_do_not_mutate_os_and_repair_probes(fixture, repair):
    assert prepare(fixture, repair)
    fixture[1].assert_not_awaited()
    fixture[2].power_on.assert_not_awaited()
    assert fixture[2].probe.await_count == int(repair)
    fixture[2].close.assert_called_once()


@pytest.mark.parametrize(
    "enabled,active,expected",
    [
        ("disabled", "inactive", ["enable", "start"]),
        ("enabled", "inactive", ["start"]),
        ("disabled", "active", ["enable"]),
        ("enabled-runtime", "active", ["enable"]),
    ],
)
def test_repairs_only_missing_unit_states(fixture, enabled, active, expected):
    fixture[0].side_effect = [
        {"LoadState": "loaded", "UnitFileState": enabled, "ActiveState": active},
        {"LoadState": "loaded", "UnitFileState": "enabled", "ActiveState": "active"},
    ]
    assert prepare(fixture, True)
    assert [call.args[0][1] for call in fixture[1].await_args_list] == expected
    assert all(call.kwargs["privileged"] for call in fixture[1].await_args_list)


@pytest.mark.parametrize(
    "state,match",
    [
        ({"LoadState": "masked"}, "masked"),
        ({"LoadState": "not-found"}, "missing"),
        (
            {
                "LoadState": "loaded",
                "ActiveState": "inactive",
                "UnitFileState": "disabled",
            },
            "not enabled/active",
        ),
    ],
)
def test_check_rejects_unready_service_without_mutations(fixture, state, match):
    fixture[0].return_value = state
    with pytest.raises(ble.BluetoothSetupError, match=match):
        prepare(fixture)
    fixture[1].assert_not_awaited()
    fixture[2].connect.assert_not_awaited()


def test_failed_start_not_reported_as_ready(fixture):
    fixture[0].return_value = {
        "LoadState": "loaded",
        "ActiveState": "inactive",
        "UnitFileState": "enabled",
    }
    with pytest.raises(ble.BluetoothSetupError, match="did not become active"):
        prepare(fixture, True)
    fixture[2].probe.assert_not_awaited()


def test_unsupported_host_does_nothing(fixture, monkeypatch):
    monkeypatch.setattr(ble, "supported_host", lambda: False)
    with pytest.raises(ble.BluetoothSetupError, match="requires Raspberry"):
        prepare(fixture, True)
    fixture[0].assert_not_awaited()
    fixture[1].assert_not_awaited()


@pytest.mark.parametrize("hard,repair", [(True, True), (False, False)])
def test_blocks_are_not_bypassed(fixture, monkeypatch, hard, repair):
    monkeypatch.setattr(ble, "radio_blocks", lambda: (True, hard))
    with pytest.raises(ble.BluetoothSetupError, match="blocked"):
        prepare(fixture, repair)
    fixture[1].assert_not_awaited()


def test_soft_unblock_targets_bluetooth_only(fixture, monkeypatch):
    blocks = iter([(True, False), (False, False)])
    monkeypatch.setattr(ble, "radio_blocks", lambda: next(blocks))
    monkeypatch.setattr(ble.shutil, "which", lambda _: "/usr/sbin/rfkill")
    assert prepare(fixture, True)
    fixture[1].assert_awaited_once_with(
        ["rfkill", "unblock", "bluetooth"], privileged=True
    )


def test_missing_rfkill_preserves_os(fixture, monkeypatch):
    monkeypatch.setattr(ble, "radio_blocks", lambda: (True, False))
    monkeypatch.setattr(ble.shutil, "which", lambda _: None)
    with pytest.raises(ble.BluetoothSetupError, match="rfkill is missing"):
        prepare(fixture, True)
    fixture[1].assert_not_awaited()


def test_power_on_is_verified(fixture):
    fixture[2].objects.side_effect = [objects(powered=False), objects()]
    assert prepare(fixture, True)
    fixture[2].power_on.assert_awaited_once_with("/org/bluez/hci0")


def test_check_does_not_power_on(fixture):
    fixture[2].objects.return_value = objects(powered=False)
    with pytest.raises(ble.BluetoothSetupError, match="powered off"):
        prepare(fixture)
    fixture[2].power_on.assert_not_awaited()
    fixture[2].close.assert_called_once()


@pytest.mark.parametrize(
    "data,match",
    [
        (objects(active=1), "Another BLE"),
        (objects(available=0), "No BLE advertising"),
        (objects(gatt=False), "lacks BLE"),
        ({}, "No Bluetooth"),
    ],
)
def test_unusable_controller_is_not_restarted(fixture, data, match, monkeypatch):
    fixture[2].objects.return_value = data
    monkeypatch.setattr(ble.asyncio, "sleep", AsyncMock())
    with pytest.raises(ble.BluetoothSetupError, match=match):
        prepare(fixture, True)
    fixture[1].assert_not_awaited()
    fixture[2].probe.assert_not_awaited()
    fixture[2].close.assert_called_once()


def test_legacy_uart_is_conditional(fixture, monkeypatch):
    monkeypatch.setattr(ble, "legacy_uart_available", lambda: True)
    monkeypatch.setattr(ble.Path, "glob", lambda *_: iter(()))
    assert prepare(fixture, True)
    assert [call.args[0] for call in fixture[0].await_args_list] == [
        "hciuart.service",
        "bluetooth.service",
    ]


@pytest.mark.parametrize(
    "failure", [RuntimeError("inert registration failure"), asyncio.CancelledError()]
)
def test_failed_or_canceled_probe_disconnects(fixture, failure):
    fixture[2].probe.side_effect = failure
    with pytest.raises(
        asyncio.CancelledError
        if isinstance(failure, asyncio.CancelledError)
        else ble.BluetoothSetupError
    ):
        prepare(fixture, True)
    fixture[2].close.assert_called_once()


@pytest.mark.parametrize(
    "failure",
    [
        None,
        RuntimeError("registration"),
        asyncio.TimeoutError(),
        asyncio.CancelledError(),
    ],
)
def test_native_probe_always_unregisters_owned_path(failure, monkeypatch):
    async def scenario():
        session = ble.BlueZSession()
        session.bus = Mock()
        manager = SimpleNamespace(
            call_register_advertisement=AsyncMock(side_effect=failure),
            call_unregister_advertisement=AsyncMock(),
        )
        monkeypatch.setattr(session, "interface", AsyncMock(return_value=manager))
        if failure:
            with pytest.raises(type(failure)):
                await session.probe("/org/bluez/hci0")
        else:
            await session.probe("/org/bluez/hci0")
        path = session.bus.export.call_args.args[0]
        assert path.startswith("/org/ninjarobot/readiness/")
        manager.call_unregister_advertisement.assert_awaited_once_with(path)
        session.bus.unexport.assert_called_once_with(path)

    asyncio.run(scenario())


def test_rfkill_reader_ignores_wifi(tmp_path):
    for index, kind, soft, hard in [(0, "wlan", "1", "1"), (1, "bluetooth", "1", "0")]:
        node = tmp_path / f"rfkill{index}"
        node.mkdir()
        for key, val in [("type", kind), ("soft", soft), ("hard", hard)]:
            (node / key).write_text(val + "\n")
    assert ble.radio_blocks(tmp_path) == (True, False)


def test_onboarding_failure_leaves_configuration_and_prompts_untouched(
    tmp_path, monkeypatch
):
    spec = importlib.util.spec_from_file_location(
        "ble_onboard", ROOT / "scripts/onboard.py"
    )
    onboard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(onboard)
    monkeypatch.setattr(onboard, "ROOT", tmp_path)
    original = b'{"robot_type":"spider","movements":{"Poweroff":[]}}'
    (tmp_path / "config.json").write_bytes(original)
    monkeypatch.setattr(ble, "run_setup", lambda **_: False)
    monkeypatch.setattr(
        "builtins.input",
        lambda _: pytest.fail("Identity prompts ran despite failed BLE readiness"),
    )
    assert onboard.worker("identity") == 1
    assert (tmp_path / "config.json").read_bytes() == original


def test_native_cleanup_failure_is_not_success(monkeypatch):
    async def scenario():
        session = ble.BlueZSession()
        session.bus = Mock()
        manager = SimpleNamespace(
            call_register_advertisement=AsyncMock(),
            call_unregister_advertisement=AsyncMock(
                side_effect=RuntimeError("inert cleanup failure")
            ),
        )
        monkeypatch.setattr(session, "interface", AsyncMock(return_value=manager))
        with pytest.raises(ble.BluetoothSetupError, match="cleanup failed"):
            await session.probe("/org/bluez/hci0")
        session.bus.unexport.assert_called_once()

    asyncio.run(scenario())


def test_power_permission_repair_targets_only_selected_adapter(fixture):
    from dbus_next.errors import DBusError

    fixture[2].objects.side_effect = [objects(powered=False), objects()]
    fixture[2].power_on.side_effect = DBusError(
        "org.bluez.Error.NotAuthorized", "inert permission failure"
    )
    assert prepare(fixture, True)
    fixture[1].assert_awaited_once_with(
        [
            "busctl",
            "set-property",
            "org.bluez",
            "/org/bluez/hci0",
            ble.ADAPTER,
            "Powered",
            "b",
            "true",
        ],
        privileged=True,
    )


@pytest.mark.parametrize(
    "privileged,uid,denied",
    [(False, 1000, False), (True, 0, False), (True, 1000, False), (True, 1000, True)],
)
def test_command_permissions_and_sudo_prompt_are_bounded(
    monkeypatch, privileged, uid, denied
):
    calls = []

    def run(args, **kwargs):
        calls.append((args, kwargs))
        return SimpleNamespace(
            returncode=int(denied and args == ["sudo", "-v"]), stdout="inert"
        )

    monkeypatch.setattr(ble.os, "geteuid", lambda: uid)
    monkeypatch.setattr(ble.subprocess, "run", run)
    if denied:
        with pytest.raises(ble.BluetoothSetupError, match="not granted"):
            asyncio.run(
                ble.command(
                    ["systemctl", "start", "bluetooth.service"], privileged=privileged
                )
            )
        assert len(calls) == 1
    else:
        assert (
            asyncio.run(
                ble.command(
                    ["systemctl", "start", "bluetooth.service"], privileged=privileged
                )
            )
            == "inert"
        )
        assert calls[-1][0] == (["sudo", "-n"] if privileged and uid else []) + [
            "systemctl",
            "start",
            "bluetooth.service",
        ]
    if privileged and uid:
        assert calls[0][0] == ["sudo", "-v"]
        assert "capture_output" not in calls[0][1]
        assert calls[0][1]["timeout"] == 60
    assert calls[-1][1]["timeout"] <= 60


def test_missing_unit_result_remains_actionable(monkeypatch):
    monkeypatch.setattr(
        ble,
        "command",
        AsyncMock(
            return_value="LoadState=not-found\nActiveState=inactive\nUnitFileState=\n"
        ),
    )
    with pytest.raises(ble.BluetoothSetupError, match="is missing"):
        asyncio.run(ble.ensure_unit("bluetooth.service", True))


def test_onboarding_success_checks_ble_before_identity_prompts(tmp_path, monkeypatch):
    from ninja_core import config

    spec = importlib.util.spec_from_file_location(
        "ble_onboard_success", ROOT / "scripts/onboard.py"
    )
    onboard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(onboard)
    monkeypatch.setattr(onboard, "ROOT", tmp_path)
    calls = []
    monkeypatch.setattr(
        ble, "run_setup", lambda **kw: calls.append(("BLE", kw)) or True
    )
    monkeypatch.setattr("builtins.input", lambda prompt: calls.append(prompt) or "")
    monkeypatch.setattr(
        config,
        "set_robot_name",
        lambda _: pytest.fail("Blank input should preserve name"),
    )
    monkeypatch.setattr(
        config,
        "set_robot_type",
        lambda _: pytest.fail("Blank input should preserve robot type"),
    )
    assert onboard.worker("identity") == 0
    assert calls[0] == ("BLE", {"repair": True})
    assert len(calls) == 3
    assert not (tmp_path / "config.json").exists()


def test_command_timeout_is_actionable(monkeypatch):
    def run(*args, **kwargs):
        raise ble.subprocess.TimeoutExpired(args[0], kwargs["timeout"])

    monkeypatch.setattr(ble.subprocess, "run", run)
    with pytest.raises(ble.BluetoothSetupError, match="timed out"):
        asyncio.run(ble.command(["systemctl", "show", "bluetooth.service"]))


def test_connect_failure_closes_session(fixture):
    fixture[2].connect.side_effect = asyncio.TimeoutError()
    with pytest.raises(ble.BluetoothSetupError, match="TimeoutError"):
        prepare(fixture, True)
    fixture[2].close.assert_called_once()


def test_kernel_controller_never_starts_legacy_uart(fixture, monkeypatch):
    monkeypatch.setattr(ble, "legacy_uart_available", lambda: True)
    monkeypatch.setattr(ble.Path, "glob", lambda *_: iter(["hci0"]))
    assert prepare(fixture, True)
    fixture[0].assert_awaited_once_with("bluetooth.service")


def test_power_failure_not_success(fixture, monkeypatch):
    fixture[2].objects.return_value = objects(powered=False)
    monkeypatch.setattr(ble.asyncio, "sleep", AsyncMock())
    with pytest.raises(ble.BluetoothSetupError, match="did not power on"):
        prepare(fixture, True)
    fixture[2].probe.assert_not_awaited()
    fixture[2].close.assert_called_once()


def test_dbus_error_name_is_preserved(fixture):
    from dbus_next.errors import DBusError

    fixture[2].probe.side_effect = DBusError(
        "org.bluez.Error.NotPermitted", "inert exhausted slots"
    )
    with pytest.raises(ble.BluetoothSetupError, match="org.bluez.Error.NotPermitted"):
        prepare(fixture, True)
    fixture[2].close.assert_called_once()
