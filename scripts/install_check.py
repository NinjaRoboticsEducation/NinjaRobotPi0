"""Read-only installation inspection. Never import a robot or open a device."""

import argparse
import os
import platform
import re
import sys
import shutil
import shlex
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
    if fields.get("ID") not in (
        "debian",
        "raspbian",
    ):
        errors.append(
            "Debian-based Raspberry Pi OS required; "
            f"detected ID={fields.get('ID', 'missing')}, "
            f"VERSION_CODENAME={fields.get('VERSION_CODENAME', 'missing')}."
        )
    if sys.version_info < (3, 10):
        errors.append("Python 3.10+ required by robot runtime type annotations.")
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


# Vite 7 and @vitejs/plugin-react engines in the committed package-lock.json.
NODE_REQUIREMENT = "Node 20.19+ in 20.x, or >=22.12.0"
UV_FLAGS = ("--locked", "--no-dev", "--python", "--directory", "--all-extras")
UV_VENV_FLAGS = ("--allow-existing", "--prompt", "--python")


def tool_error(command, executable):
    """Probe capabilities only; never sync, create a cache, or contact hardware."""
    if not executable:
        return f"Missing {command}."
    option = "-v" if command == "pigpiod" else "--version"
    try:
        result = subprocess.run(
            [str(executable), option], capture_output=True, text=True, timeout=20
        )
        actual = result.stdout.strip()
        if result.returncode:
            return f"Cannot read {command} version at {executable} (exit {result.returncode})."
        if command == "node":
            match = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", actual)
            version = tuple(map(int, match.groups())) if match else (0, 0, 0)
            if not (
                version[0] == 20 and version >= (20, 19, 0) or version >= (22, 12, 0)
            ):
                return f"Incompatible node: requires {NODE_REQUIREMENT}; detected {actual[:160]!r} at {executable}."
        elif command == "uv":
            result = subprocess.run(
                [str(executable), "sync", "--help"],
                capture_output=True,
                text=True,
                timeout=20,
            )
            missing = [flag for flag in UV_FLAGS if flag not in result.stdout.split()]
            if result.returncode or missing:
                return f"Incompatible uv at {executable}: uv sync must support {', '.join(UV_FLAGS)}."
            result = subprocess.run(
                [str(executable), "venv", "--help"],
                capture_output=True, text=True, timeout=20,
            )
            missing = [flag for flag in UV_VENV_FLAGS if flag not in result.stdout.split()]
            if result.returncode or missing:
                return f"Incompatible uv at {executable}: uv venv must support {', '.join(UV_VENV_FLAGS)}."
        elif command == "pigpiod" and actual != "79":
            return f"pigpiod version mismatch: required 79, detected {actual[:160]!r} at {executable}."
    except (OSError, subprocess.TimeoutExpired):
        return f"Cannot read {command} version/capabilities at {executable}."
    return None


def compatible_path(command):
    """Prefer caller PATH, then installer tools, skipping incompatible candidates."""
    tools = Path.home() / ".local/share/ninjarobot_pi0/tools"
    paths = os.environ.get("PATH", "").split(os.pathsep)
    paths += [str(tools / "uv"), str(tools / "node/bin")]
    for directory in dict.fromkeys(paths):
        if not directory:
            continue
        candidate = Path(directory) / command
        if candidate.is_file() and os.access(candidate, os.X_OK):
            if tool_error(command, candidate) is None:
                return str(candidate.absolute())
    return None


def check(root):
    errors = platform_errors() + path_errors(root)
    for command in ("node", "uv", "npm", "pigpiod"):
        error = tool_error(command, shutil.which(command))
        if error:
            errors.append(error)
    for relative in (
        ".venv/bin/python",
        ".venv/bin/ninja_core",
        "ninja_webapp/dist/index.html",
    ):
        if not (root / relative).is_file():
            errors.append(f"Missing {relative}; project installation is incomplete.")
        elif relative.startswith(".venv/bin/") and not os.access(
            root / relative, os.X_OK
        ):
            errors.append(
                f"Not executable: {relative}; project environment needs repair."
            )
    python = root / ".venv/bin/python"
    if python.is_file() and os.access(python, os.X_OK):
        try:
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
        except (OSError, subprocess.TimeoutExpired):
            errors.append(
                "Project Python could not run; the environment is incomplete or broken."
            )
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", action="store_true")
    parser.add_argument("--find-tool", choices=("node", "uv"))
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    args = parser.parse_args()
    if args.find_tool:
        executable = compatible_path(args.find_tool)
        if executable:
            print(executable)
        return 0 if executable else 1
    errors = (
        (platform_errors() + path_errors(args.root))
        if args.platform
        else check(args.root)
    )
    if not args.platform:
        print("Read-only installation check: no software was installed or changed.")
    for error in errors:
        print(f"FAIL: {error}")
    if errors and not args.platform:
        print("Installation is incomplete or a required tool is incompatible.")
        print(
            "Run the installer as your normal user (it requests sudo only where needed):"
        )
        print(f"  cd -- {shlex.quote(str(args.root.resolve()))} && ./install.sh")
        print("After it reports 'Software installed', run ./install.sh --check again.")
        print(
            "Compatible tools on your PATH are reused; do not uninstall your system tools."
        )
    if not errors:
        print(
            "PASS: software prerequisites. Hardware activation/calibration remains a separate step."
        )
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
