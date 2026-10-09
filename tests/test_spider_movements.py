"""Offline data/loader/controller checks. No HAL or GPIO objects are created."""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
from types import SimpleNamespace

import pytest

from ninja_core.config import NinjaConfig, load_config
from ninja_core.movement_controller import MovementController

ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "ninja_core/movements/spider_otto.json"
PACK = json.loads(PACK_PATH.read_text())
MOVES = PACK["movements"]
EXPECTED_NAMES = {
    "dance",
    "front_back",
    "hello",
    "hide",
    "home",
    "jump",
    "moonwalk_left",
    "omni_false",
    "omni_true",
    "push_up",
    "run_backward",
    "run_forward",
    "scared",
    "turn_left",
    "turn_right",
    "up_down",
    "walk_backward",
    "walk_forward",
    "wave_hand",
}


class RecordingServos:
    # Deliberately shuffled, to expose source-index/list-index confusion.
    pins = [27, 20, 25, 22, 24, 21, 26, 23]

    def __init__(self):
        self.calls = []

    def move_all_sync(self, targets, **kwargs):
        self.calls.append((dict(zip(self.pins, targets)), kwargs))
        return True


def controller(config):
    servos = RecordingServos()
    return MovementController(SimpleNamespace(servos=servos), config), servos


def test_complete_names_and_actual_config_loader():
    assert set(MOVES) == {"spider_otto_" + n for n in EXPECTED_NAMES}
    config = load_config(PACK_PATH)
    assert config.robot_type == "spider"
    assert config.movements == MOVES
    assert config.servos.calibration == {}  # Not a pretend calibrated runtime config.


@pytest.mark.parametrize("name", sorted(MOVES))
def test_each_definition_has_only_executable_fields_and_valid_angles(name):
    assert MOVES[name]
    for step in MOVES[name]:
        assert set(step) == {"moves", "speed"}
        assert step["speed"] == "M"
        assert set(step["moves"]) == {str(p) for p in range(20, 28)}
        assert all(math.isfinite(a) and -90 <= a <= 90 for a in step["moves"].values())


@pytest.mark.parametrize("name", sorted(MOVES))
def test_real_executor_preserves_every_gpio_target_and_step_order(name):
    ctrl, servos = controller(load_config(PACK_PATH))
    ctrl.execute_movement(name)
    steps = MOVES[name]
    assert len(servos.calls) == len(steps)
    for i, ((actual, options), step) in enumerate(zip(servos.calls, steps)):
        assert actual == {int(k): v for k, v in step["moves"].items()}
        assert options["speed_mode"] == ["M"] * 8
        expected = (
            "ease_in_out_cubic"
            if len(steps) == 1
            else "ease_in_cubic"
            if i == 0
            else "ease_out_cubic"
            if i == len(steps) - 1
            else "linear"
        )
        assert options["easing"] == expected
        assert options["force"] is True


def test_existing_optional_speed_override_and_omitted_servo_semantics():
    config = NinjaConfig(
        movements={
            "example": [
                {
                    "moves": {"20": 20, "27": -10},
                    "speed": "S",
                    "per_servo_speeds": {"27": "F"},
                },
                {"moves": {"20": 0}, "speed": "M"},
            ]
        }
    )
    ctrl, servos = controller(config)
    ctrl.execute_movement("example")
    angles, options = servos.calls[0]
    assert angles == {p: {20: 20, 27: -10}.get(p) for p in servos.pins}
    assert options["speed_mode"] == ["F", "S", "S", "S", "S", "S", "S", "S"]
    assert servos.calls[1][0][27] is None


def test_source_home_mapping_and_wave_hand_negative_amplitude():
    # Independent manually evaluated source vectors, in target GPIO order.
    assert MOVES["spider_otto_home"][0]["moves"] == {
        "20": 20,
        "21": -20,
        "22": 0,
        "23": 0,
        "24": -20,
        "25": 20,
        "26": 0,
        "27": 0,
    }
    hand = MOVES["spider_otto_wave_hand"]
    assert hand[0]["moves"]["27"] == -60
    assert hand[9]["moves"]["27"] == -80
    assert hand[27]["moves"]["27"] == -40
    assert hand[9]["moves"]["20"] == 85  # S5, not S0.


def test_walk_double_frequency_and_direction_variation():
    forward = MOVES["spider_otto_walk_forward"]
    backward = MOVES["spider_otto_walk_backward"]
    assert [forward[i]["moves"]["27"] for i in [0, 9, 18, 27, 36]] == [
        -10,
        30,
        -10,
        30,
        -10,
    ]
    assert forward[0]["moves"]["25"] == 5
    assert backward[0]["moves"]["25"] == 35
    assert all(a["moves"]["27"] == b["moves"]["27"] for a, b in zip(forward, backward))


def test_omni_default_aliases_and_non_cardinal_moonwalk_phase():
    assert MOVES["spider_otto_omni_true"] == MOVES["spider_otto_omni_false"]
    moon = MOVES["spider_otto_moonwalk_left"][0]["moves"]
    assert moon["26"] == pytest.approx(45 * math.sin(math.radians(120)), abs=0.0005)
    assert moon["22"] == pytest.approx(45 * math.sin(math.radians(290)), abs=0.0005)


def test_jump_scared_reuse_poses_in_reverse_order_and_end_home():
    jump, scared = MOVES["spider_otto_jump"], MOVES["spider_otto_scared"]
    assert len(jump) == len(scared) == 3
    assert jump[0] == scared[1] and jump[1] == scared[0]
    assert jump[-1] == scared[-1] == MOVES["spider_otto_home"][0]
    assert jump[0]["moves"]["27"] == -60
    assert jump[1]["moves"]["27"] == 80


def test_hello_represents_actual_small_helper_writes_and_clips_wave():
    hello = MOVES["spider_otto_hello"]
    assert len(hello) == 39
    assert hello[0]["moves"]["27"] == -4.333  # (25-90)/15, not intended -65.
    assert hello[1]["moves"]["25"] == 1.4  # (160-90)/50, not intended 70.
    assert min(s["moves"]["24"] for s in hello[2:]) == -90
    assert hello[-1] != MOVES["spider_otto_home"][0]


def test_generator_matches_pack_and_retains_all_eight_independent_pins():
    spec = importlib.util.spec_from_file_location(
        "spider_builder", ROOT / "scripts/build_spider_movements.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.build_pack() == PACK
    # Unique per-source values catch every element of the source->target permutation.
    assert module.pose([90 + i for i in range(8)])["moves"] == {
        "20": 5,
        "21": 4,
        "22": 7,
        "23": 6,
        "24": 1,
        "25": 0,
        "26": 3,
        "27": 2,
    }
