"""Fresh software installation and error recovery with inert, offline artifacts."""

import hashlib
import importlib.util
import os
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("state", ["loaded", "not-found", "masked", "error", ""])
def test_service_check_never_activates(state, monkeypatch):
    check = load("install_check")
    calls = []

    def run(command, **kwargs):
        calls.append(command)
        return SimpleNamespace(returncode=0, stdout=state + "\n")

    monkeypatch.setattr(check.subprocess, "run", run)
    assert bool(check.service_errors()) == (state != "loaded")
    assert calls == [
        ["systemctl", "show", "pigpiod.service", "--property=LoadState", "--value"]
    ]


def test_system_packages_include_fresh_lite_requirements(tmp_path, monkeypatch):
    setup = load("install_system")
    monkeypatch.setattr(setup.os, "geteuid", lambda: 0)
    calls = []
    policy = tmp_path / "policy-rc.d"

    def run(command, **kwargs):
        assert policy.read_text() == "#!/bin/sh\nexit 101\n"
        calls.append(command)

    setup.install_packages(policy, run)
    assert calls[0] == ["apt-get", "update"]
    assert {
        "git",
        "python3-pip",
        "python3-venv",
        "build-essential",
        "curl",
        "zstd",
    } <= set(calls[1])
    assert not policy.exists()


def executable(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    path.chmod(0o755)


@pytest.fixture
def fresh(tmp_path):
    checkout = tmp_path / "robot"
    (checkout / "scripts").mkdir(parents=True)
    (checkout / "ninja_webapp").mkdir()
    (checkout / "servo.json").write_text("owner calibration")
    for name in ("install-rpi.sh", "install_check.py", "install-versions.env"):
        shutil.copyfile(ROOT / "scripts" / name, checkout / "scripts" / name)
    binaries = tmp_path / "bin"
    binaries.mkdir()
    artifacts = tmp_path / "artifacts"
    artifacts.mkdir()
    log = tmp_path / "calls"
    home_dir = tmp_path / "user"
    home_dir.mkdir()
    # Real checksum verification/extraction; downloaded programs perform only fixture writes.
    uv_body = """#!/bin/sh
case "$1" in
--version) echo 'uv 0.11.29';;
venv)
  if [ "$2" = --help ]; then echo '--allow-existing --prompt --python'; exit; fi
  mkdir -p .venv/bin
  printf '# fixture activation\n' > .venv/bin/activate
  printf '#!/bin/sh\nexit 0\n' > .venv/bin/python
  chmod +x .venv/bin/python;;
sync)
  if [ "$2" = --help ]; then echo '--locked --no-dev --python --directory --all-extras --reinstall-package'; exit; fi
  for name in ninja_core pi0servo pi0disp pi0buzzer pi0vl53l0x; do cp .venv/bin/python ".venv/bin/$name"; done;;
esac
printf 'uv:%s\n' "$*" >> "$CALL_LOG"
"""
    (artifacts / "uv-program").write_text(uv_body)
    executable(
        artifacts / "uv.sh",
        """#!/bin/sh
attempt=0
if [ -f "$ARTIFACTS/uv-attempts" ]; then attempt=$(cat "$ARTIFACTS/uv-attempts"); fi
attempt=$((attempt + 1))
printf '%s' "$attempt" > "$ARTIFACTS/uv-attempts"
[ "$attempt" -gt "${UV_NETWORK_FAILURES:-0}" ] || { echo 'fixture TLS/DNS failure' >&2; exit 1; }
mkdir -p "$UV_INSTALL_DIR"
cp "$ARTIFACTS/uv-program" "$UV_INSTALL_DIR/uv"
chmod +x "$UV_INSTALL_DIR/uv"
""",
    )
    node_dir = artifacts / "node-v22.23.3-linux-arm64"
    executable(node_dir / "bin/node", "#!/bin/sh\necho v22.23.3\n")
    executable(
        node_dir / "bin/npm",
        """#!/bin/sh
[ "$1" != --version ] || { echo 10.0.0; exit; }
printf 'npm:%s\n' "$*" >> "$CALL_LOG"
if [ "$1" = run ]; then mkdir -p dist; printf fixture > dist/index.html; fi
""",
    )
    with tarfile.open(artifacts / "node.tar.xz", "w:xz") as archive:
        archive.add(node_dir, arcname=node_dir.name)
    pigpio = artifacts / "pigpio-fixture"
    pigpio.mkdir()
    (pigpio / "README").write_text("inert compile input")
    with tarfile.open(artifacts / "pigpio.tar.gz", "w:gz") as archive:
        archive.add(pigpio, arcname=pigpio.name)
    versions = (checkout / "scripts/install-versions.env").read_text()
    for key, name in [
        ("UV_INSTALLER_SHA256", "uv.sh"),
        ("NODE_ARM64_SHA256", "node.tar.xz"),
        ("PIGPIO_SHA256", "pigpio.tar.gz"),
    ]:
        versions = re.sub(
            rf"^{key}=.*$",
            f"{key}={hashlib.sha256((artifacts / name).read_bytes()).hexdigest()}",
            versions,
            flags=re.MULTILINE,
        )
    versions = re.sub(
        r"^PIGPIO_COMMIT=.*$", "PIGPIO_COMMIT=fixture", versions, flags=re.M
    )
    (checkout / "scripts/install-versions.env").write_text(versions)
    # Always preserve inert command resolution; do not prepend host tools.
    executable(
        binaries / "python3",
        f"""#!/bin/sh
case "$*" in
*--find-tool*) exec {shlex.quote(sys.executable)} "$@";;
*--platform*) exit "${{PREFLIGHT_EXIT:-0}}";;
*install_check.py*)
  for file in .venv/bin/activate .venv/bin/python .venv/bin/ninja_core .venv/bin/pi0servo .venv/bin/pi0disp .venv/bin/pi0buzzer .venv/bin/pi0vl53l0x ninja_webapp/dist/index.html; do
    test -f "$FIXTURE_ROOT/$file" || exit 91
  done
  test -f "$ARTIFACTS/service" || exit 92;;
*install_ollama.py*) printf 'ollama:%s\\n' "$*" >> "$CALL_LOG";;
*) exit 0;;
esac
""",
    )
    executable(
        binaries / "sudo",
        """#!/bin/sh
printf 'sudo:%s\n' "$*" >> "$CALL_LOG"
case "$1" in
python3) exit "${APT_EXIT:-0}";;
install)
  for last do :; done
  case "$last" in
  /usr/local/bin/pigpiod) cp "$4" "$FIXTURE_BIN/pigpiod"; chmod +x "$FIXTURE_BIN/pigpiod";;
  /etc/systemd/system/pigpiod.service) cp "$4" "$ARTIFACTS/service";;
  esac;;
esac
""",
    )
    executable(
        binaries / "systemctl",
        """#!/bin/sh
case "$1" in
is-active) exit 3;;
cat) test -f "$ARTIFACTS/service";;
*) exit 99;;
esac
""",
    )
    executable(
        binaries / "make",
        """#!/bin/sh
printf '#!/bin/sh\necho 79\n' > pigpiod
chmod +x pigpiod
printf fixture > libpigpio.so.1
printf 'make:%s\n' "$*" >> "$CALL_LOG"
""",
    )
    executable(
        binaries / "curl",
        """#!/bin/sh
for arg do
  case "$arg" in *astral.sh*) file=uv.sh;; *nodejs.org*) file=node.tar.xz;; *codeload.github.com*) file=pigpio.tar.gz;; esac
  destination="$arg"
done
cp "$ARTIFACTS/$file" "$destination"
""",
    )
    for name in ("node", "uv", "npm"):
        executable(binaries / name, "#!/bin/sh\nexit 1\n")
    # macOS lacks sha256sum; use the system shasum equivalent, still verifying bytes.
    if os.uname().sysname == "Darwin":
        executable(
            binaries / "sha256sum",
            "#!/bin/sh\nexec /usr/bin/shasum -a 256 -c --status\n",
        )
    environment = {
        **os.environ,
        "HOME": str(home_dir),
        "PATH": f"{binaries}:/usr/bin:/bin",
        "ARTIFACTS": str(artifacts),
        "CALL_LOG": str(log),
        "FIXTURE_ROOT": str(checkout),
        "FIXTURE_BIN": str(binaries),
    }
    return checkout, environment, log


def run_install(fresh, **extra):
    checkout, environment, _ = fresh
    return subprocess.run(
        ["bash", str(checkout / "scripts/install-rpi.sh"), "--yes"],
        env={**environment, **extra},
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )


def test_fresh_downloads_create_environment_daemon_and_unit_then_rerun(fresh):
    checkout, environment, log = fresh
    for _ in range(2):
        result = run_install(fresh)
        assert result.returncode == 0, result.stdout + result.stderr
        assert "Software installed." in result.stdout
        assert (checkout / "servo.json").read_text() == "owner calibration"
        assert not (checkout / ".ninjarobot-install.lock").exists()
    calls = log.read_text()
    assert calls.count("make:-j1 pigpiod") == 1
    assert calls.count("npm:run build") == 2
    assert calls.index("uv:sync") < calls.index("ollama:")
    assert "systemctl start" not in calls and "systemctl enable" not in calls
    unit = (Path(environment["ARTIFACTS"]) / "service").read_text()
    assert " -g -l" in unit


@pytest.mark.parametrize(
    "stage,extra",
    [
        ("Platform and maintenance preflight", {"PREFLIGHT_EXIT": "12"}),
        ("OS prerequisites", {"APT_EXIT": "13"}),
    ],
)
def test_failure_diagnoses_first_stage_without_false_success(fresh, stage, extra):
    result = run_install(fresh, **extra)
    assert result.returncode != 0
    assert f"Installation stopped during: {stage}" in result.stderr
    assert "Software installed." not in result.stdout
    assert not (fresh[0] / ".ninjarobot-install.lock").exists()
    assert not (fresh[0] / ".venv").exists()


def test_foreign_lock_is_preserved(fresh):
    lock = fresh[0] / ".ninjarobot-install.lock"
    lock.mkdir()
    result = run_install(fresh)
    assert result.returncode != 0 and lock.is_dir()
    assert "Installation lock exists" in result.stderr


def test_missing_activation_is_reported_without_repair(tmp_path, monkeypatch):
    check = load("install_check")
    monkeypatch.setattr(check, "platform_errors", list)
    monkeypatch.setattr(check, "path_errors", lambda _: [])
    monkeypatch.setattr(check, "launcher_errors", lambda _: [])
    monkeypatch.setattr(check, "service_errors", list)
    monkeypatch.setattr(check, "tool_error", lambda *_: None)
    before = list(tmp_path.iterdir())
    assert (
        "Missing .venv/bin/activate; project installation is incomplete."
        in check.check(tmp_path)
    )
    assert list(tmp_path.iterdir()) == before


@pytest.mark.parametrize("failures,success,attempts", [(1, True, 2), (9, False, 3)])
def test_uv_inner_download_retries_are_bounded(fresh, failures, success, attempts):
    checkout, environment, log = fresh
    executable(Path(environment["FIXTURE_BIN"]) / "sleep", "#!/bin/sh\nexit 0\n")
    result = run_install(fresh, UV_NETWORK_FAILURES=str(failures))
    assert (result.returncode == 0) == success, result.stdout + result.stderr
    assert (Path(environment["ARTIFACTS"]) / "uv-attempts").read_text() == str(attempts)
    assert not (checkout / ".ninjarobot-install.lock").exists()
    if not success:
        assert "after 3 attempts" in result.stderr
        assert "releases.astral.sh and github.com" in result.stderr
        assert "Software installed." not in result.stdout
        assert not (checkout / ".venv").exists()
        assert "npm:" not in log.read_text()
