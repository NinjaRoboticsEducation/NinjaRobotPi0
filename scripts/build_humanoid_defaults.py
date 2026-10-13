"""Validate and package the owner's current Humanoid defaults without hardware."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from build_humanoid_movements import render_resource, unique_object

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "DevelopmentPlanDoc/humanoid_movements_updated.json"
RESOURCE = ROOT / "ninja_core/src/ninja_core/data/humanoid_defaults.json"
FINGERPRINT = "2497b7a778be779f97fd8c271398f5261711874c32b2d18e74de57f99a992a24"


def extract_defaults(source: Path = SOURCE) -> dict[str, list]:
    """Reject malformed or unreviewed data before writing installed defaults."""
    pack = json.loads(
        source.read_text(encoding="utf-8"), object_pairs_hook=unique_object
    )
    if not isinstance(pack, dict) or set(pack) != {"movements"}:
        raise ValueError("Expected only a movements object")
    movements = pack["movements"]
    if not isinstance(movements, dict) or len(movements) != 37:
        raise ValueError("Expected reviewed catalog: 37 movements")
    sys.path.insert(0, str(ROOT / "ninja_core/src"))
    from ninja_core.builtin_movements import validate_sequence

    for name, sequence in movements.items():
        if not (name.startswith("humanoid_") or name == "Poweroff"):
            raise ValueError(f"Invalid Humanoid movement name: {name}")
        validate_sequence(sequence, range(20, 28))
        if any(
            set(step["moves"]) != {str(pin) for pin in range(20, 28)}
            for step in sequence
        ):
            raise ValueError("Every default step must address exactly GPIO20–27")
    if sum(map(len, movements.values())) != 1278:
        raise ValueError("Expected reviewed catalog: 1278 steps")
    canonical = json.dumps(
        movements, sort_keys=True, separators=(",", ":"), allow_nan=False
    )
    if hashlib.sha256(canonical.encode()).hexdigest() != FINGERPRINT:
        raise ValueError("Owner catalog changed; review before updating fingerprint")
    return movements


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Verify exact installed data"
    )
    args = parser.parse_args()
    content = render_resource(extract_defaults())
    if args.check:
        if not RESOURCE.is_file() or RESOURCE.read_text(encoding="utf-8") != content:
            print("Humanoid defaults differ from reviewed owner JSON", file=sys.stderr)
            return 1
        print("PASS: installed Humanoid defaults match 37 movements / 1278 steps")
    else:
        RESOURCE.write_text(content, encoding="utf-8")
        print(f"Wrote {RESOURCE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
