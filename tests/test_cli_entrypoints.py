"""CLI ownership and broken-launcher detection without installs or robot imports."""

import importlib.util
import os
import shlex
import subprocess
import sys
import tomllib
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cli_install_check", ROOT / "scripts/install_check.py")
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


def test_robot_console_scripts_have_exactly_one_provider():
    owners = {}
    for package in (".", "ninja_core", "pi0servo", "pi0disp", "pi0buzzer", "pi0vl53l0x"):
        data = tomllib.loads((ROOT / package / "pyproject.toml").read_text())
        for name, target in data["project"].get("scripts", {}).items():
            owners.setdefault(name, []).append((package, target))
    for command in check.CLI_PROVIDERS:
        expected = f"{command}.__main__:{'main' if command == 'ninja_core' else 'cli'}"
        assert owners[command] == [(command, expected)]
    root = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert root["project"]["name"] == "ninjarobotpi0"


def test_root_uninstall_record_cannot_claim_provider_launchers():
    root_scripts = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"].get("scripts", {})
    provider_files = {f"../../../bin/{command}" for command in check.CLI_PROVIDERS}
    # RECORD uninstallation deletes paths without tracking other owners.
    legacy_root_record = provider_files.copy()
    assert not provider_files - legacy_root_record  # Reproduces the legacy collision.
    new_root_record = {f"../../../bin/{command}" for command in root_scripts}
    assert provider_files - new_root_record == provider_files


@pytest.mark.parametrize("command", check.CLI_PROVIDERS)
def test_all_missing_provider_launchers_are_detected_without_changes(command, tmp_path):
    binary = tmp_path / ".venv/bin"
    binary.mkdir(parents=True)
    for name in check.CLI_PROVIDERS:
        if name != command:
            file = binary / name
            file.write_text("#!/bin/sh\nexit 99\n")
            file.chmod(0o755)
    before = {p: p.read_bytes() for p in binary.iterdir()}
    assert check.launcher_errors(tmp_path) == [
        f"Missing .venv/bin/{command}; project installation is incomplete."
    ]
    assert before == {p: p.read_bytes() for p in binary.iterdir()}


def test_nonexecutable_launcher_is_not_accepted(tmp_path):
    binary = tmp_path / ".venv/bin"
    binary.mkdir(parents=True)
    for name in check.CLI_PROVIDERS:
        file = binary / name
        file.write_text("#!/bin/sh\nexit 99\n")
        file.chmod(0o755 if name != "pi0servo" else 0o644)
    assert check.launcher_errors(tmp_path) == [
        "Not executable: .venv/bin/pi0servo; project environment needs repair."
    ]


def test_uv_without_targeted_reinstall_capability_is_rejected(monkeypatch):
    def run(command, **kwargs):
        output = "uv 0.9.26" if command[-1] == "--version" else " ".join(
            flag for flag in check.UV_FLAGS if flag != "--reinstall-package"
        )
        return SimpleNamespace(returncode=0, stdout=output)
    monkeypatch.setattr(check.subprocess, "run", run)
    assert "--reinstall-package" in check.tool_error("uv", "/inert/uv")


def test_repair_command_is_locked_scoped_and_preserves_dev_environment():
    args = shlex.split(check.cli_repair_command())
    assert args[:6] == ["env", "-u", "UV_PROJECT_ENVIRONMENT", "-u", "UV_PROJECT", "uv"]
    assert args[6:10] == ["sync", "--locked", "--inexact", "--no-dev"]
    assert args[10:] == [word for package in check.CLI_PROVIDERS.values() for word in ("--reinstall-package", package)]
    assert "--clear" not in args and "server" not in args


def test_missing_launcher_diagnostics_provide_repair_without_running_uv(tmp_path, monkeypatch, capsys):
    binary = tmp_path / ".venv/bin"
    binary.mkdir(parents=True)
    python = binary / "python"
    python.write_text("inert interpreter")
    python.chmod(0o755)
    monkeypatch.setattr(check, "platform_errors", lambda: [])
    monkeypatch.setattr(check, "path_errors", lambda _: [])
    monkeypatch.setattr(check, "tool_error", lambda *_: None)
    calls = []

    def run(command, **kwargs):
        calls.append(command)
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(check.subprocess, "run", run)
    monkeypatch.setattr(sys, "argv", ["install_check.py", "--root", str(tmp_path)])
    assert check.main() == 1
    output = capsys.readouterr().out
    assert check.cli_repair_command() in output
    assert all(command[0] == str(python) for command in calls)
    assert all("server" not in command for command in calls)


def test_uv_venv_allow_existing_preserves_inert_launcher(tmp_path):
    import shutil

    uv = shutil.which("uv")
    if not uv:
        pytest.skip("uv unavailable; no tools are installed for this test")
    environment = tmp_path / "inert-env"
    launcher = environment / "bin/ninja_core"
    launcher.parent.mkdir(parents=True)
    launcher.write_text("#!/bin/sh\necho INERT\n")
    launcher.chmod(0o755)
    result = subprocess.run(
        [uv, "venv", "--no-project", "--offline", "--no-python-downloads", "--allow-existing",
         "--prompt", "ninjarobotpi0", "--python", sys.executable, str(environment)],
        capture_output=True, text=True, timeout=30,
        env={**os.environ, "UV_VENV_CLEAR": "false", "UV_VENV_SEED": "false"},
    )
    assert result.returncode == 0, result.stderr
    assert launcher.read_text() == "#!/bin/sh\necho INERT\n"
    assert os.access(launcher, os.X_OK)
