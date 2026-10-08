"""Read-only installation inspection. Never import a robot or open a device."""

import argparse
import os
import platform
import shutil
import subprocess
from pathlib import Path


def platform_errors(
    model=Path("/proc/device-tree/model"), release=Path("/etc/os-release")
):
    errors = []
    if platform.system() != "Linux" or platform.machine() != "aarch64":
        errors.append("Linux aarch64 required.")
    if os.geteuid() == 0:
        errors.append("Run as your normal user, not root.")
    if not model.is_file() or "Raspberry Pi Zero 2" not in model.read_text():
        errors.append("Raspberry Pi Zero 2 W required.")
    fields = {}
    if release.is_file():
        fields = dict(
            line.split("=", 1)
            for line in release.read_text().splitlines()
            if "=" in line
        )
        fields = {key: value.strip('"') for key, value in fields.items()}
    if fields.get("VERSION_CODENAME") not in ("bookworm", "trixie") or fields.get(
        "ID"
    ) not in (
        "debian",
        "raspbian",
    ):
        errors.append(
            "Raspberry Pi OS Bookworm (12) or Trixie (13) required; "
            f"detected ID={fields.get('ID', 'missing')}, "
            f"VERSION_CODENAME={fields.get('VERSION_CODENAME', 'missing')}."
        )
    return errors


def path_errors(root):
    """Reject redirected installer-owned environments before privileged changes."""
    tools = Path.home() / ".local/share/ninjarobot_pi0/tools"
    for target in (
        tools,
        tools / "uv",
        tools / "node",
        root / ".venv",
        root / ".ninjarobot-install",
    ):
        if any(part.is_symlink() for part in (target, *target.parents)):
            return ["Installer paths must not contain symbolic links."]
    return []


def check(root):
    errors = platform_errors() + path_errors(root)
    pins = dict(
        line.split("=", 1)
        for line in (root / "scripts/install-versions.env").read_text().splitlines()
        if line and not line.startswith("#")
    )
    for command in ("uv", "node", "npm", "pigpiod"):
        if not shutil.which(command):
            errors.append(f"Missing {command}.")
    for command, expected in (
        ("node", "v" + pins["NODE_VERSION"]),
        ("uv", "uv " + pins["UV_VERSION"]),
        ("pigpiod", "79"),
    ):
        if shutil.which(command):
            option = "-v" if command == "pigpiod" else "--version"
            result = subprocess.run(
                [command, option], capture_output=True, text=True, timeout=20
            )
            actual = result.stdout.strip()
            matches = actual == expected or (
                command == "uv" and actual.startswith(expected + " (")
            )
            if result.returncode or not matches:
                errors.append(f"Unreviewed {command} version.")
    for relative in (
        ".venv/bin/python",
        ".venv/bin/ninja_core",
        "ninja_webapp/dist/index.html",
    ):
        if not (root / relative).is_file():
            errors.append(f"Missing {relative}.")
    python = root / ".venv/bin/python"
    if python.is_file():
        result = subprocess.run(
            [
                str(python),
                "-B",
                "-c",
                "from importlib.metadata import version; print(version('ninja_core'), version('pigpio'))",
            ],
            capture_output=True,
            timeout=20,
        )
        if result.returncode:
            errors.append("Installed package metadata is incomplete.")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", action="store_true")
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    args = parser.parse_args()
    errors = (
        (platform_errors() + path_errors(args.root))
        if args.platform
        else check(args.root)
    )
    for error in errors:
        print(f"FAIL: {error}")
    if not errors:
        print(
            "PASS: software prerequisites. Hardware activation/calibration remains a separate step."
        )
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
