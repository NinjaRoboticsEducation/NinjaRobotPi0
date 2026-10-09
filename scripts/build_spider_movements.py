"""Offline OTTO logical-angle waypoint pack; never imports/operates robot hardware.

See DevelopmentPlanDoc/SpiderBuildinMovements.md for fidelity limitations.
This is not a trajectory executor or an installer for the live config.json.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "ninja_core/movements/spider_otto.json"
# User-corrected source ID -> BCM GPIO; this is not driver list order.
SOURCE_TO_GPIO = (25, 24, 27, 26, 21, 20, 23, 22)
SAMPLES = 36  # 10-degree phase spacing, including both cycle endpoints.
SPEED = "M"  # Existing target default, NOT a conversion of OTTO period.
HOME = (110, 70, 90, 90, 70, 110, 90, 90)
SIT = (105, 75, 30, 150, 110, 70, 150, 30)
STRETCH = (110, 70, 170, 10, 30, 150, 10, 170)

# Source parameters: amplitude, offset, phase, per-servo cycles per hip cycle.
# Period is provenance only: the existing target JSON cannot schedule it.
BASE = (105, 75, 90, 90, 75, 105, 90, 90)
WAVES = {
    "run_forward": (
        "run(0)",
        550,
        (15,) * 8,
        BASE,
        (0, 0, 90, 90, 180, 180, 90, 90),
        (1,) * 8,
    ),
    "run_backward": (
        "run(1)",
        550,
        (15,) * 8,
        BASE,
        (180, 180, 90, 90, 0, 0, 90, 90),
        (1,) * 8,
    ),
    "turn_left": (
        "turnL",
        550,
        (15,) * 8,
        BASE,
        (0, 180, 90, 90, 180, 0, 90, 90),
        (1,) * 8,
    ),
    "turn_right": (
        "turnR",
        550,
        (15,) * 8,
        BASE,
        (180, 0, 90, 90, 0, 180, 90, 90),
        (1,) * 8,
    ),
    "dance": (
        "dance",
        1000,
        (0, 0, 40, 40, 0, 0, 40, 40),
        (120, 60, 90, 90, 60, 120, 90, 90),
        (0, 0, 0, 270, 0, 0, 90, 180),
        (1,) * 8,
    ),
    "front_back": (
        "frontBack",
        750,
        (30, 30, 25, 25, 30, 30, 25, 25),
        HOME,
        (0, 180, 270, 90, 0, 180, 90, 270),
        (1,) * 8,
    ),
    "up_down": (
        "upDown",
        500,
        (0, 0, 35, 35, 0, 0, 35, 35),
        HOME,
        (0, 0, 90, 270, 180, 180, 270, 90),
        (1,) * 8,
    ),
    "push_up": (
        "pushUp",
        5000,
        (0, 0, 40, 40, 0, 0, 0, 0),
        (90, 90, 90, 90, 25, 155, 90, 90),
        (0, 0, 0, 180, 0, 0, 0, 180),
        (1,) * 8,
    ),
    "wave_hand": (
        "waveHAND",
        700,
        (0, 0, -20, 0, 0, 0, 0, 0),
        (90, 90, 30, 60, 25, 175, 90, 90),
        (0,) * 8,
        (1,) * 8,
    ),
    "moonwalk_left": (
        "moonwalkL",
        2000,
        (0, 0, 45, 45, 0, 0, 45, 45),
        (90,) * 8,
        (0, 0, 0, 120, 0, 0, 180, 290),
        (1,) * 8,
    ),
    "omni_true": (
        "omniWalk(true,1000,2)",
        1000,
        (15,) * 8,
        (123, 57, 67, 113, 93, 87, 113, 67),
        (0, 360, 90, 90, 180, -180, 90, 90),
        (1,) * 8,
    ),
    "omni_false": (
        "omniWalk(false,1000,2)",
        1000,
        (15,) * 8,
        (123, 57, 67, 113, 93, 87, 113, 67),
        (360, 0, 90, 90, -180, 180, 90, 90),
        (1,) * 8,
    ),
    "walk_forward": (
        "walk(1)",
        550,
        (15, 15, 20, 20, 15, 15, 20, 20),
        (110, 70, 100, 80, 70, 110, 80, 100),
        (270, 270, 270, 90, 90, 90, 90, 270),
        (1, 1, 2, 2, 1, 1, 2, 2),
    ),
    "walk_backward": (
        "walk(0)",
        550,
        (15, 15, 20, 20, 15, 15, 20, 20),
        (110, 70, 100, 80, 70, 110, 80, 100),
        (90, 90, 270, 90, 270, 270, 90, 270),
        (1, 1, 2, 2, 1, 1, 2, 2),
    ),
}
HELLO_WAVE = (
    "hello",
    350,
    (0, 50, 0, 50, 0, 0, 0, 0),
    (105, 40, 80, 100, 110, 70, 155, 90),
    (0, 0, 0, 90, 0, 0, 0, 0),
    (1,) * 8,
)


def pose(source_angles):
    """Nominal q-90; clamp source's negative hello wave at its angle endpoint.

    No source EEPROM trims or source S2 mounting reversal are assumed for Pi0.
    """
    if len(source_angles) != 8:
        raise ValueError("Expected eight source angles")
    angles = {}
    for pin, value in zip(SOURCE_TO_GPIO, source_angles):
        if not math.isfinite(value):
            raise ValueError("Non-finite source angle")
        converted = round(max(0.0, min(180.0, value)) - 90.0, 3)
        angles[str(pin)] = 0.0 if converted == 0 else converted
    return {"moves": dict(sorted(angles.items())), "speed": SPEED}


def wave(parameters):
    _, _, amplitude, offset, phase, cycles = parameters
    return [
        pose(
            [
                o + a * math.sin(2 * math.pi * c * sample / SAMPLES + math.radians(p))
                for a, o, p, c in zip(amplitude, offset, phase, cycles)
            ]
        )
        for sample in range(SAMPLES + 1)
    ]


def build_pack():
    movements = {"spider_otto_" + name: wave(params) for name, params in WAVES.items()}
    movements["spider_otto_home"] = [pose(HOME)]
    movements["spider_otto_hide"] = [pose((90, 90, 10, 170, 90, 90, 170, 10))]
    movements["spider_otto_jump"] = [pose(SIT), pose(STRETCH), pose(HOME)]
    movements["spider_otto_scared"] = [pose(STRETCH), pose(SIT), pose(HOME)]
    # Actual long-helper q at zero source trim, not its unachieved desired pose.
    hello_sit = (105, 75, 25, 155, 110, 70, 100, 80)
    hello_rise = (160, 20, 90, 90, 70, 110, 100, 80)
    movements["spider_otto_hello"] = [
        pose([90 + (v - 90) / 15 for v in hello_sit]),
        pose([90 + (v - 90) / 50 for v in hello_rise]),
        *wave(HELLO_WAVE),
    ]
    return {"robot_type": "spider", "movements": dict(sorted(movements.items()))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Verify committed pack without writing"
    )
    args = parser.parse_args()
    content = json.dumps(build_pack(), indent=2, allow_nan=False) + "\n"
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text() != content:
            parser.exit(1, "Spider pack is missing or differs from the generator.\n")
        print("PASS: 19 Spider movement entries match the offline generator.")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(content)
        print(f"Wrote {OUTPUT}; live config.json was not touched.")


if __name__ == "__main__":
    main()
