"""Configuration and execution checks with inert drivers and mocked AI/network."""

import asyncio
import json
from copy import deepcopy
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import HTTPException

from ninja_core.builtin_movements import (
    MovementValidationError,
    SPIDER_POWEROFF,
    available_movements,
    builtin_catalog,
    seed_builtin_movements,
)
from ninja_core.config import (
    NinjaConfig,
    import_and_update_config,
    load_config,
    save_config,
    set_robot_type,
)
from ninja_core.movement_controller import EmergencyStop, MovementController
from ninja_core.ninja_agent import NinjaAgent


class InertServos:
    def __init__(self, pins, completed=True):
        self.pins = list(reversed(pins))
        self.calls = []
        self.completed = completed

    def move_all_sync(self, targets, **kwargs):
        self.calls.append((targets, kwargs))
        return self.completed


def profile(kind="spider", pins=range(20, 28)):
    return NinjaConfig(robot_type=kind, servos={
        "calibration": {str(pin): {} for pin in pins},
    })


def controller(config, pins=None, completed=True):
    pins = list(map(int, config.servos.calibration)) if pins is None else pins
    servos = InertServos(pins, completed)
    return MovementController(SimpleNamespace(servos=servos), config), servos


@pytest.mark.parametrize("kind,name,count", [
    ("spider", "spider_home", 20),
    ("humanoid", "home", 1),
    ("wheel", "home", 1),
])
def test_import_seeds_profiles_and_is_idempotent(kind, name, count, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_config(profile(kind))
    (tmp_path / "servo.json").write_text(json.dumps({
        str(pin): {"pulse_min": 600, "pulse_center": 1500, "pulse_max": 2400}
        for pin in range(20, 28)
    }))
    import_and_update_config()
    config = load_config()
    assert name in config.movements
    assert len(config.movements) == count
    assert config.movement_robot_types[name] == config.robot_type
    before = (tmp_path / "config.json").read_bytes()
    import_and_update_config()
    assert (tmp_path / "config.json").read_bytes() == before
    assert config.movements == load_config().movements


def test_fresh_default_import_and_existing_load_are_non_actuating(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    import_and_update_config()
    assert "home" in load_config().movements
    before = (tmp_path / "config.json").read_bytes()
    load_config()
    assert (tmp_path / "config.json").read_bytes() == before


def test_resource_matches_original_pack_and_document():
    root = Path(__file__).resolve().parents[1]
    original = json.loads((root / "ninja_core/movements/spider_otto.json").read_text())
    catalog = builtin_catalog("spider", range(20, 28))
    assert catalog == {
        **{name.replace("spider_otto_", "spider_", 1): sequence
           for name, sequence in original["movements"].items()},
        "Poweroff": SPIDER_POWEROFF,
    }
    # Parse all 20 documented movement fragments and check exact parity.
    text = (root / "DevelopmentPlanDoc/SpiderBuildinMovements.md").read_text()
    section = text.split("### Complete copyable JSON for every movement")[1]
    documented = {}
    for block in section.split("```json\n")[1:]:
        documented.update(json.loads(block.split("```", 1)[0])["movements"])
    assert catalog == documented
    catalog["spider_home"][0]["moves"]["20"] = 50
    assert builtin_catalog("spider", range(20, 28))["spider_home"][0]["moves"]["20"] == 20


def test_type_switch_preserves_edits_and_custom_sequences(tmp_path):
    config = profile()
    seed_builtin_movements(config)
    config.movements["spider_home"][0]["moves"]["20"] = 10
    config.movements["custom"] = [{"moves": {"20": 5}, "speed": "S"}]
    save_config(config, tmp_path / "config.json")
    set_robot_type("wheel", tmp_path / "config.json")
    loaded = load_config(tmp_path / "config.json")
    assert loaded.robot_type == "tire"
    assert set(loaded.movements) == {"custom", "spider_home", "home"}
    assert loaded.movements["spider_home"][0]["moves"]["20"] == 10
    assert available_movements(loaded) == ["custom", "home"]
    set_robot_type("spider", tmp_path / "config.json")
    assert load_config(tmp_path / "config.json").movements["spider_home"][0]["moves"]["20"] == 10


def test_collision_is_preserved_and_not_claimed_as_managed():
    config = profile()
    custom = [{"moves": {"20": 2}, "speed": "S"}]
    config.movements["Poweroff"] = deepcopy(custom)
    seed_builtin_movements(config)
    assert config.movements["Poweroff"] == custom
    assert "Poweroff" not in config.builtin_movement_hashes


def test_missing_pins_remove_only_unchanged_managed_values():
    config = profile()
    seed_builtin_movements(config)
    config.movements["spider_home"][0]["moves"]["20"] = 10
    del config.servos.calibration["27"]
    seed_builtin_movements(config)
    assert set(config.movements) == {"spider_home"}
    assert available_movements(config) == []
    assert builtin_catalog("spider", range(20, 27)) == {}
    assert builtin_catalog("tire", []) == {}


@pytest.mark.parametrize("kind", ["tire", "humanoid"])
@pytest.mark.parametrize("name", ["spider_home", "spider_otto_home", "Poweroff", "renamed"])
def test_wrong_type_legacy_and_renamed_spider_are_rejected_before_writes(kind, name):
    config = profile(kind)
    sequence = SPIDER_POWEROFF if name == "Poweroff" else builtin_catalog("spider", range(20, 28))["spider_home"]
    config.movements[name] = deepcopy(sequence)
    ctrl, servos = controller(config)
    assert ctrl.available_movement_names() == []
    with pytest.raises(MovementValidationError, match="requires spider"):
        ctrl.execute_movement(name)
    assert servos.calls == []


@pytest.mark.parametrize("bad_step", [
    {"moves": {"20": float("nan")}, "speed": "M"},
    {"moves": {"20": True}, "speed": "M"},
    {"moves": {"20": 91}, "speed": "M"},
    {"moves": {"28": 0}, "speed": "M"},
    {"moves": {"020": 0}, "speed": "M"},
    {"moves": {"20": 0}, "speed": "INVALID"},
    {"moves": {}, "speed": "M"},
    {"moves": {"20": 0}, "speed": "M", "duration": 1},
    {"moves": {"20": 0}, "speed": "M", "per_servo_speeds": {"99": "S"}},
    None,
])
def test_malformed_late_step_rejects_entire_sequence(bad_step):
    config = profile()
    config.movements["custom"] = [{"moves": {"20": 1}, "speed": "S"}, bad_step]
    ctrl, servos = controller(config)
    with pytest.raises(MovementValidationError):
        ctrl.execute_movement("custom")
    assert servos.calls == []


def test_missing_active_channel_rejected():
    config = profile()
    seed_builtin_movements(config)
    ctrl, servos = controller(config, pins=[20])
    assert ctrl.available_movement_names() == []
    with pytest.raises(MovementValidationError):
        ctrl.execute_movement("spider_home")
    assert servos.calls == []


def test_legacy_poweroff_with_speed_edit_and_no_empty_overrides_is_still_spider():
    config = profile("tire")
    sequence = deepcopy(SPIDER_POWEROFF)
    sequence[0].pop("per_servo_speeds")
    sequence[0]["speed"] = "F"
    config.movements["Poweroff"] = sequence
    ctrl, servos = controller(config)
    with pytest.raises(MovementValidationError, match="requires spider"):
        ctrl.execute_movement("Poweroff")
    assert servos.calls == []


def test_driver_abort_stops_sequence_without_recovery_commands():
    config = profile()
    seed_builtin_movements(config)
    ctrl, servos = controller(config, completed=False)
    with pytest.raises(EmergencyStop):
        ctrl.execute_movement("spider_walk_forward")
    assert len(servos.calls) == 1


def test_safety_callback_stops_before_first_write():
    config = profile()
    seed_builtin_movements(config)
    ctrl, servos = controller(config)
    with pytest.raises(EmergencyStop):
        ctrl.execute_movement("spider_home", abort_check=lambda: True)
    assert servos.calls == []


def test_web_discovery_and_wrong_type_request_do_not_reclaim_runtime(monkeypatch):
    from ninja_core import web_server

    config = profile("humanoid")
    seed_builtin_movements(config)
    config.movements["spider_home"] = builtin_catalog("spider", range(20, 28))["spider_home"]
    ctrl, servos = controller(config)
    state = SimpleNamespace(movement=ctrl)
    request = SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(ninja=state)))
    reclaim = AsyncMock()
    monkeypatch.setattr(web_server, "reclaim_native_runtime", reclaim)
    assert web_server.get_movements(request) == {"movements": ["home"]}
    with pytest.raises(HTTPException) as error:
        asyncio.run(web_server.execute_movement("spider_home", request))
    assert error.value.status_code == 422
    reclaim.assert_not_awaited()
    assert servos.calls == []


def agent(config, monkeypatch):
    monkeypatch.setattr("ninja_core.ninja_agent.genai.configure", Mock())
    monkeypatch.setattr("ninja_core.ninja_agent.genai.GenerativeModel", Mock())
    config.api_keys["gemini"] = "inert-test-key"
    library = Mock()
    library.list_names.return_value = []
    return NinjaAgent(config, library)


@pytest.mark.parametrize("audio", [False, True])
def test_agent_filters_capabilities_and_rejects_whole_mixed_chain(audio, tmp_path, monkeypatch):
    config = profile("humanoid")
    seed_builtin_movements(config)
    config.movements["spider_home"] = builtin_catalog("spider", range(20, 28))["spider_home"]
    ninja = agent(config, monkeypatch)
    assert ninja.robot_capabilities["movements"] == ["home"]
    assert "Configured robot type: humanoid" in ninja.system_prompt
    response = json.dumps({"response": "Okay", "chain": [
        {"name": "home"}, {"name": "spider_home"},
    ]})
    if audio:
        audio_path = tmp_path / "inert.webm"
        audio_path.write_bytes(b"test")
        monkeypatch.setattr(ninja, "_generate_content", AsyncMock(return_value=response))
        result = asyncio.run(ninja.process_audio_command(str(audio_path)))
    else:
        monkeypatch.setattr(ninja, "_send_text_command", AsyncMock(return_value=response))
        result = asyncio.run(ninja.process_command("move"))
    assert "chain" not in result["action_plan"]
    assert "Rejected native movement plan" in result["log"]
    assert result["response"] == "Okay"


@pytest.mark.parametrize("plan", [
    {"movement": "spider_home"}, {"chain": "home"},
    {"chain": [{"name": "home", "repetitions": 0}]},
    {"chain": [{"name": "home", "repetitions": True}]},
    {"chain": [{"name": "home", "repetitions": 21}]},
    {"chain": [{"name": "home", "repetitions": 1.5}]},
])
def test_agent_rejects_bad_repetitions_and_legacy_cross_type(plan, monkeypatch):
    config = profile("humanoid")
    seed_builtin_movements(config)
    ninja = agent(config, monkeypatch)
    logs = []
    ninja._validate_native_plan(plan, logs)
    assert not plan
    assert logs


def test_valid_agent_plan_preserved_and_controller_discovery_agrees(monkeypatch):
    config = profile()
    seed_builtin_movements(config)
    ninja = agent(config, monkeypatch)
    ctrl, servos = controller(config)
    assert ninja.robot_capabilities["movements"] == ctrl.available_movement_names()
    plan = {"chain": [{"name": "spider_home", "repetitions": 2}]}
    before = deepcopy(plan)
    logs = []
    ninja._validate_native_plan(plan, logs)
    assert plan == before
    assert not logs
    ctrl.execute_movement("Poweroff")
    assert dict(zip(servos.pins, servos.calls[0][0])) == {
        int(pin): value for pin, value in SPIDER_POWEROFF[0]["moves"].items()
    }


def test_cli_execute_menu_filters_wrong_type_and_runs_home(monkeypatch, capsys):
    from ninja_core import movement_cli

    config = profile("humanoid", pins=[20, 21])
    seed_builtin_movements(config)
    config.movements["spider_bad"] = [{"moves": {"20": 5}, "speed": "M"}]
    ctrl, servos = controller(config)
    answers = iter(["1", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(ctrl, "center_all_servos", lambda: None)
    monkeypatch.setattr(movement_cli, "NonBlockingKeyboard", lambda: nullcontext(
        SimpleNamespace(kbhit=lambda: False)
    ))
    movement_cli.execute_movement_cli(ctrl)
    output = capsys.readouterr().out
    assert "1. home" in output
    assert "spider_bad" not in output
    assert servos.calls[0][0] == [0, 0]


def test_web_valid_home_execution_and_unknown_name(monkeypatch):
    from ninja_core import web_server

    config = profile("tire", pins=[20, 21])
    seed_builtin_movements(config)
    ctrl, servos = controller(config)
    state = SimpleNamespace(movement=ctrl, connection_manager=SimpleNamespace(broadcast=AsyncMock()))
    request = SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(ninja=state)))
    monkeypatch.setattr(web_server, "reclaim_native_runtime", AsyncMock())
    monkeypatch.setattr(web_server, "safety_check", lambda _: False)
    assert asyncio.run(web_server.execute_movement("home", request)) == {"status": "executed"}
    assert servos.calls[0][0] == [0, 0]
    with pytest.raises(HTTPException) as error:
        asyncio.run(web_server.execute_movement("missing", request))
    assert error.value.status_code == 404
