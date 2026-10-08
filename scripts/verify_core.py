"""Check the reviewed protected robot-source baseline without importing robot code."""

import hashlib
import json
from pathlib import Path


def verify(root):
    baseline = json.loads((root / "docs/validation/core_baseline.json").read_text())
    errors = []
    for name, expected in baseline["files"].items():
        path = root / name
        if (
            not path.is_file()
            or hashlib.sha256(path.read_bytes()).hexdigest() != expected
        ):
            errors.append(f"Protected robot source changed: {name}")
    return errors


if __name__ == "__main__":
    errors = verify(Path(__file__).resolve().parents[1])
    print(
        "\n".join(errors)
        if errors
        else "PASS: protected robot source and metadata unchanged."
    )
    raise SystemExit(bool(errors))
