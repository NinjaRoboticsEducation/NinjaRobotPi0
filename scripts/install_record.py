"""Write non-secret, installer-owned software provenance after successful checks."""

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def record(root):
    state = root / ".ninjarobot-install"
    if state.is_symlink() or (state / "record.json").is_symlink():
        raise ValueError("Refusing redirected installation state")
    state.mkdir(mode=0o700, exist_ok=True)
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    value = {
        "revision": result.stdout.strip(),
        "hardware": "pending",
        "inputs": {
            name: hashlib.sha256((root / name).read_bytes()).hexdigest()
            for name in (
                "uv.lock",
                "ninja_webapp/package-lock.json",
                "scripts/install-versions.env",
            )
        },
    }
    descriptor, temporary = tempfile.mkstemp(dir=state, prefix=".record-")
    try:
        with os.fdopen(descriptor, "w") as stream:
            json.dump(value, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, state / "record.json")
    finally:
        Path(temporary).unlink(missing_ok=True)


if __name__ == "__main__":
    record(Path(sys.argv[1]))
