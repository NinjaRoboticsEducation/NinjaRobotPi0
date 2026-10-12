"""Package the reviewed Humanoid reference without importing hardware or config."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "DevelopmentPlanDoc/HumanoidBuildinMovements.md"
RESOURCE = ROOT / "ninja_core/src/ninja_core/data/humanoid_otto.json"
FINGERPRINT = "49f6c4fe998b3c8500347f56eeeb7e165fb442c206ac373485310af7d280d2d6"


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def extract_movements(reference: Path = REFERENCE) -> dict[str, list]:
    """Read only complete library blocks, excluding commissioning examples."""
    text = reference.read_text(encoding="utf-8")
    starts = list(re.finditer(r"^<!-- HUMANOID_LIBRARY_START -->$", text, re.M))
    ends = list(re.finditer(r"^<!-- HUMANOID_LIBRARY_END -->$", text, re.M))
    if len(starts) != 1 or len(ends) != 1 or starts[0].end() >= ends[0].start():
        raise ValueError("Expected one ordered pair of library markers")
    section = text[starts[0].end() : ends[0].start()]
    blocks = re.findall(r"^```json\n(.*?)\n```", section, re.M | re.S)
    movements = {}
    for block in blocks:
        fragment = json.loads(block, object_pairs_hook=unique_object)
        if not isinstance(fragment, dict) or set(fragment) != {"movements"}:
            raise ValueError("Unexpected movement envelope")
        entries = fragment["movements"]
        if not isinstance(entries, dict):
            raise ValueError("Movements must be an object")
        for name, sequence in entries.items():
            if not name.startswith("humanoid_") or name in movements:
                raise ValueError(f"Invalid or duplicate movement: {name}")
            movements[name] = sequence
    if len(movements) != 34 or sum(map(len, movements.values())) != 1203:
        raise ValueError("Expected reviewed library: 34 movements / 1203 steps")

    # This module is hardware-free; do not import NinjaConfig, HAL or drivers.
    sys.path.insert(0, str(ROOT / "ninja_core/src"))
    from ninja_core.builtin_movements import validate_sequence

    for sequence in movements.values():
        validate_sequence(sequence, range(20, 28))
        for step in sequence:
            if set(step["moves"]) != {str(pin) for pin in range(20, 28)}:
                raise ValueError("Every step must address exactly GPIO20–27")
            if step["moves"]["24"] != 0 or step["moves"]["25"] != 0:
                raise ValueError("Unverified shoulders must remain nominal neutral")
    canonical = json.dumps(
        movements, sort_keys=True, separators=(",", ":"), allow_nan=False
    )
    if hashlib.sha256(canonical.encode()).hexdigest() != FINGERPRINT:
        raise ValueError(
            "Reference differs from reviewed library; review before updating fingerprint"
        )
    return movements


def render_resource(movements: dict[str, list]) -> str:
    """Keep one complete waypoint per line for reviewable package data."""
    entries = []
    for name, sequence in movements.items():
        steps = ",\n".join(
            "      " + json.dumps(step, allow_nan=False) for step in sequence
        )
        entries.append(f"    {json.dumps(name)}: [\n{steps}\n    ]")
    return (
        '{\n  "robot_type": "humanoid",\n  "movements": {\n'
        + ",\n".join(entries)
        + "\n  }\n}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Verify exact resource bytes"
    )
    args = parser.parse_args()
    content = render_resource(extract_movements())
    if args.check:
        if not RESOURCE.is_file() or RESOURCE.read_text(encoding="utf-8") != content:
            print("Humanoid package data differs from the reference", file=sys.stderr)
            return 1
        print("PASS: packaged Humanoid library matches all 34 definitions / 1203 steps")
    else:
        RESOURCE.write_text(content, encoding="utf-8")
        print(f"Wrote {RESOURCE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
