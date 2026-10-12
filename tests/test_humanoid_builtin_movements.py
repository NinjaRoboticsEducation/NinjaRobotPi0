"""Humanoid catalog import and all three native entry points with inert output."""

import asyncio
import json
import runpy
from copy import deepcopy
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from ninja_core.builtin_movements import (
    MovementValidationError,
    available_movements,
    builtin_catalog,
    movement_hash,
    seed_builtin_movements,
)
from ninja_core.config import (
    import_and_update_config,
    load_config,
    save_config,
    set_robot_type,
)
from test_builtin_movements import agent, controller, profile

ROOT = Path(__file__).resolve().parents[1]
HUMANOID = {
    name: steps
    for name, steps in builtin_catalog("humanoid", range(20, 28)).items()
    if name.startswith("humanoid_")
}


def test_pack_matches_complete_reference_and_is_independent():
    builder = runpy.run_path(str(ROOT / "scripts/build_humanoid_movements.py"))
    extracted = builder["extract_movements"]()
    resource = json.loads(
        (ROOT / "ninja_core/src/ninja_core/data/humanoid_otto.json").read_text()
    )
    assert resource == {"robot_type": "humanoid", "movements": extracted}
    assert resource["movements"] == HUMANOID
    assert len(HUMANOID) == 34
    assert sum(map(len, HUMANOID.values())) == 1203
    assert not set(HUMANOID) & set(builtin_catalog("spider", range(20, 28)))
    assert all(
        step["moves"]["24"] == step["moves"]["25"] == 0
        for sequence in HUMANOID.values()
        for step in sequence
    )
    copy = builtin_catalog("humanoid", range(20, 28))
    copy["humanoid_jump"][0]["moves"]["20"] = 42
    assert (
        builtin_catalog("humanoid", range(20, 28))["humanoid_jump"][0]["moves"]["20"]
        == 0
    )


@pytest.mark.parametrize("missing", range(20, 28))
def test_partial_profile_keeps_home_and_blocks_all_full_library(missing):
    pins = set(range(20, 28)) - {missing}
    config = profile("humanoid", pins)
    seed_builtin_movements(config)
    assert set(config.movements) == {"home"}
    config.movements.update(deepcopy(HUMANOID))
    ctrl, servos = controller(config)
    assert ctrl.available_movement_names() == ["home"]
    for name in HUMANOID:
        with pytest.raises(MovementValidationError):
            ctrl.execute_movement(name)
    assert servos.calls == []


def test_empty_and_extra_channels():
    assert builtin_catalog("humanoid", []) == {}
    catalog = builtin_catalog("humanoid", [19, *range(20, 28)])
    assert len(catalog) == 35
    assert catalog["home"][0]["moves"]["19"] == 0
    assert all("19" not in step["moves"] for seq in HUMANOID.values() for step in seq)


def test_fresh_type_selection_then_module_import(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    set_robot_type("humanoid")
    import_and_update_config()
    config = load_config()
    assert set(config.movements) == {"home", *HUMANOID}
    assert sum(map(len, config.movements.values())) == 1204
    assert all(config.movement_robot_types[n] == "humanoid" for n in config.movements)
    assert all(
        config.builtin_movement_hashes[n] == movement_hash(s)
        for n, s in config.movements.items()
    )
    before = (tmp_path / "config.json").read_bytes()
    import_and_update_config()
    assert (tmp_path / "config.json").read_bytes() == before
    load_config()
    assert (tmp_path / "config.json").read_bytes() == before


def test_upgrade_old_home_collision_and_user_edits(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    config = profile("humanoid")
    old = [{"moves": {str(p): 0 for p in range(20, 28)}, "speed": "S"}]
    config.movements["home"] = old
    config.builtin_movement_hashes["home"] = movement_hash(old)
    config.movement_robot_types["home"] = "humanoid"
    collision = [{"moves": {"20": 5}, "speed": "M"}]
    config.movements["humanoid_jump"] = deepcopy(collision)
    config.movements["owner_custom"] = deepcopy(collision)
    save_config(config)
    import_and_update_config()
    loaded = load_config()
    assert len(loaded.movements) == 36
    assert loaded.movements["humanoid_jump"] == collision
    assert "humanoid_jump" not in loaded.builtin_movement_hashes
    loaded.movements["humanoid_walk_forward"][0]["moves"]["20"] = 3
    save_config(loaded)
    import_and_update_config()
    assert load_config().movements["humanoid_walk_forward"][0]["moves"]["20"] == 3
    assert load_config().movements["owner_custom"] == collision


def test_managed_update_and_deleted_entry_restore():
    config = profile("humanoid")
    seed_builtin_movements(config)
    prior = deepcopy(config.movements["humanoid_jump"])
    prior[0]["moves"]["20"] = 3
    config.movements["humanoid_jump"] = prior
    config.builtin_movement_hashes["humanoid_jump"] = movement_hash(prior)
    del config.movements["humanoid_wave_right_arm"]
    assert seed_builtin_movements(config)
    assert config.movements["humanoid_jump"] == HUMANOID["humanoid_jump"]
    assert (
        config.movements["humanoid_wave_right_arm"]
        == HUMANOID["humanoid_wave_right_arm"]
    )
    assert not seed_builtin_movements(config)


@pytest.mark.parametrize("other", ["tire", "spider"])
def test_type_switch_preserves_edits_but_filters_them(other, tmp_path):
    config = profile("humanoid")
    seed_builtin_movements(config)
    config.movements["humanoid_jump"][0]["moves"]["20"] = 3
    config.movements["owner_custom"] = [{"moves": {"20": 4}, "speed": "S"}]
    path = tmp_path / "config.json"
    save_config(config, path)
    set_robot_type(other, path)
    loaded = load_config(path)
    assert loaded.movements["humanoid_jump"][0]["moves"]["20"] == 3
    assert loaded.movement_robot_types["humanoid_jump"] == "humanoid"
    assert "humanoid_jump" not in available_movements(loaded)
    assert "owner_custom" in available_movements(loaded)
    assert set(available_movements(loaded)) == set(
        builtin_catalog(other, range(20, 28))
    ) | {"owner_custom"}
    set_robot_type("humanoid", path)
    loaded = load_config(path)
    assert loaded.movements["humanoid_jump"][0]["moves"]["20"] == 3
    assert set(available_movements(loaded)) == {"home", *HUMANOID, "owner_custom"}


@pytest.mark.parametrize("name", sorted(HUMANOID))
def test_every_humanoid_sequence_executes_all_exact_batches(name):
    config = profile("humanoid")
    seed_builtin_movements(config)
    ctrl, servos = controller(config)
    ctrl.execute_movement(name)
    sequence = HUMANOID[name]
    assert len(servos.calls) == len(sequence)
    for i, (step, (targets, modes)) in enumerate(zip(sequence, servos.calls)):
        assert targets == [step["moves"][str(pin)] for pin in servos.pins]
        assert modes["speed_mode"] == ["S"] * 8
        assert modes["force"] is True
        expected = (
            "ease_in_out_cubic"
            if len(sequence) == 1
            else (
                "ease_in_cubic"
                if i == 0
                else "ease_out_cubic"
                if i == len(sequence) - 1
                else "linear"
            )
        )
        assert modes["easing"] == expected


@pytest.mark.parametrize("other", ["tire", "spider"])
@pytest.mark.parametrize("name", sorted(HUMANOID))
@pytest.mark.parametrize("renamed", [False, True])
def test_wrong_profile_blocks_named_and_renamed_trajectories(other, name, renamed):
    if renamed and name == "humanoid_home":
        # A generic center pose has no unique robot geometry to infer.
        return
    config = profile(other)
    sequence = deepcopy(HUMANOID[name])
    for step in sequence:
        step["speed"] = "F"
        step.pop("per_servo_speeds")
        step["moves"] = {int(pin): angle for pin, angle in step["moves"].items()}
    key = "renamed" if renamed else name
    config.movements[key] = sequence
    ctrl, servos = controller(config)
    assert ctrl.available_movement_names() == []
    with pytest.raises(MovementValidationError, match="requires humanoid"):
        ctrl.execute_movement(key)
    assert servos.calls == []


def test_generic_neutral_is_not_claimed_as_humanoid():
    config = profile("tire")
    config.movements["custom_center"] = deepcopy(HUMANOID["humanoid_home"])
    ctrl, servos = controller(config)
    ctrl.execute_movement("custom_center")
    assert len(servos.calls) == 1


def test_conflicting_scope_cannot_override_recognized_geometry():
    config = profile("tire")
    config.movements["renamed"] = deepcopy(HUMANOID["humanoid_jump"])
    config.movement_robot_types["renamed"] = "tire"
    ctrl, servos = controller(config)
    with pytest.raises(MovementValidationError):
        ctrl.execute_movement("renamed")
    assert servos.calls == []


def test_missing_actual_driver_channel_blocks_complete_config():
    config = profile("humanoid")
    seed_builtin_movements(config)
    ctrl, servos = controller(config, pins=range(20, 27))
    assert ctrl.available_movement_names() == []
    with pytest.raises(MovementValidationError):
        ctrl.execute_movement("humanoid_jump")
    assert servos.calls == []


def test_cli_menu_lists_catalog_and_executes_humanoid(monkeypatch, capsys):
    from ninja_core import movement_cli

    config = profile("humanoid")
    seed_builtin_movements(config)
    config.movements["spider_bad"] = [{"moves": {"20": 3}, "speed": "S"}]
    ctrl, servos = controller(config)
    names = ctrl.available_movement_names()
    answers = iter([str(names.index("humanoid_jump") + 1), "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(ctrl, "center_all_servos", lambda: None)
    monkeypatch.setattr(movement_cli.time, "sleep", lambda _: None)
    monkeypatch.setattr(
        movement_cli,
        "NonBlockingKeyboard",
        lambda: nullcontext(SimpleNamespace(kbhit=lambda: False)),
    )
    movement_cli.execute_movement_cli(ctrl)
    output = capsys.readouterr().out
    assert all(name in output for name in HUMANOID)
    assert "spider_bad" not in output
    assert len(servos.calls) == 2


@pytest.mark.parametrize("kind", ["humanoid", "tire", "spider"])
def test_web_dropdown_and_execution_respect_type(kind, monkeypatch):
    from ninja_core import web_server

    config = profile(kind)
    seed_builtin_movements(config)
    config.movements.update(deepcopy(HUMANOID))
    ctrl, servos = controller(config)
    state = SimpleNamespace(
        movement=ctrl, connection_manager=SimpleNamespace(broadcast=AsyncMock())
    )
    request = SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(ninja=state)))
    reclaim = AsyncMock()
    monkeypatch.setattr(web_server, "reclaim_native_runtime", reclaim)
    monkeypatch.setattr(web_server, "safety_check", lambda _: False)
    monkeypatch.setattr(web_server, "session_active", lambda _: True)
    advertised = web_server.get_movements(request)["movements"]
    assert (
        set(HUMANOID) <= set(advertised)
        if kind == "humanoid"
        else not set(HUMANOID) & set(advertised)
    )
    if kind == "humanoid":
        assert asyncio.run(web_server.execute_movement("humanoid_jump", request)) == {
            "status": "executed"
        }
        assert len(servos.calls) == 2
        reclaim.assert_awaited_once()
    else:
        with pytest.raises(HTTPException) as error:
            asyncio.run(web_server.execute_movement("humanoid_jump", request))
        assert error.value.status_code == 422
        reclaim.assert_not_awaited()
        assert servos.calls == []


@pytest.mark.parametrize("kind", ["humanoid", "tire", "spider"])
@pytest.mark.parametrize("audio", [False, True])
def test_agent_text_audio_advertises_and_validates_humanoid(
    kind, audio, tmp_path, monkeypatch
):
    config = profile(kind)
    seed_builtin_movements(config)
    config.movements.update(deepcopy(HUMANOID))
    ninja = agent(config, monkeypatch)
    assert (
        set(HUMANOID) <= set(ninja.robot_capabilities["movements"])
        if kind == "humanoid"
        else not set(HUMANOID) & set(ninja.robot_capabilities["movements"])
    )
    response = json.dumps(
        {
            "response": "Okay",
            "chain": [
                {"name": "humanoid_jump", "repetitions": 2},
            ],
        }
    )
    if audio:
        path = tmp_path / "test.webm"
        path.write_bytes(b"inert")
        monkeypatch.setattr(
            ninja, "_generate_content", AsyncMock(return_value=response)
        )
        result = asyncio.run(ninja.process_audio_command(str(path)))
    else:
        monkeypatch.setattr(
            ninja, "_send_text_command", AsyncMock(return_value=response)
        )
        result = asyncio.run(ninja.process_command("jump"))
    if kind == "humanoid":
        assert result["action_plan"]["chain"] == [
            {"name": "humanoid_jump", "repetitions": 2}
        ]
    else:
        assert "chain" not in result["action_plan"]
        assert "Rejected native movement plan" in result["log"]


def test_agent_rejects_entire_mixed_chain_and_stale_capabilities(monkeypatch):
    config = profile("humanoid")
    seed_builtin_movements(config)
    ninja = agent(config, monkeypatch)
    plan = {"chain": [{"name": "home"}, {"name": "spider_hide"}]}
    logs = []
    ninja._validate_native_plan(plan, logs)
    assert "chain" not in plan and logs
    config.robot_type = "tire"
    plan = {"movement": "humanoid_jump"}
    logs = []
    ninja._validate_native_plan(plan, logs)
    assert not plan and logs
    ninja.refresh_capabilities()
    assert not set(HUMANOID) & set(ninja.robot_capabilities["movements"])


def test_agent_plan_executes_through_existing_server_controller(monkeypatch):
    from ninja_core import web_server

    config = profile("humanoid")
    seed_builtin_movements(config)
    ninja = agent(config, monkeypatch)
    plan = {"chain": [{"name": "humanoid_jump", "repetitions": 2}]}
    logs = []
    ninja._validate_native_plan(plan, logs)
    assert not logs
    ctrl, servos = controller(config)
    state = SimpleNamespace(movement=ctrl, faces=None, sound=None)
    monkeypatch.setattr(web_server, "session_active", lambda _: True)
    monkeypatch.setattr(web_server, "safety_check", lambda _: False)
    # Existing post-agent reset is tested elsewhere; isolate the requested batches.
    center = AsyncMock()
    monkeypatch.setattr(web_server, "center_for_session", center)
    asyncio.run(web_server._execute_action_plan_unlocked(state, plan))
    assert len(servos.calls) == 4
    expected = HUMANOID["humanoid_jump"] * 2
    assert [targets for targets, _ in servos.calls] == [
        [step["moves"][str(pin)] for pin in servos.pins] for step in expected
    ]
    center.assert_awaited_once()


@pytest.mark.parametrize("command", ["import", "import-all"])
def test_real_cli_module_import_seeds_humanoid(command, tmp_path, monkeypatch):
    from click.testing import CliRunner
    from ninja_core.__main__ import main

    monkeypatch.chdir(tmp_path)
    save_config(profile("humanoid"))
    result = CliRunner().invoke(main, ["config", command])
    assert result.exit_code == 0, result.output
    assert set(load_config().movements) == {"home", *HUMANOID}


def test_offline_builder_refuses_duplicate_keys_and_marker_corruption(tmp_path):
    builder = runpy.run_path(str(ROOT / "scripts/build_humanoid_movements.py"))
    original = (ROOT / "DevelopmentPlanDoc/HumanoidBuildinMovements.md").read_text()
    reference = tmp_path / "reference.md"
    reference.write_text(
        original.replace(
            '"humanoid_home": [', '"humanoid_home": [], "humanoid_home": [', 1
        )
    )
    with pytest.raises(ValueError, match="Duplicate JSON key"):
        builder["extract_movements"](reference)
    reference.write_text(
        original.replace(
            "<!-- HUMANOID_LIBRARY_END -->", "<!-- HUMANOID_LIBRARY_START -->", 1
        )
    )
    with pytest.raises(ValueError, match="markers"):
        builder["extract_movements"](reference)
