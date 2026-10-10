"""Exercise the streamed bootstrap with real private Git remotes and inert setup."""

import os
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def remote(tmp_path):
    source = tmp_path / "remote"
    source.mkdir()

    def git(*args):
        return subprocess.check_output(
            ["git", "-C", str(source), *args], text=True
        ).strip()

    git("init", "-q", "-b", "release/default")
    (source / "scripts").mkdir()
    for name in ("install.sh", "uv.lock", "scripts/install-versions.env"):
        (source / name).write_text("# fixture\n")
    (source / "scripts/install-rpi.sh").write_text(
        "#!/bin/bash\nprintf 'inert:%s\\n' \"$*\"\n"
    )
    git("add", ".")
    git(
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.invalid",
        "commit",
        "-qm",
        "fixture",
    )
    commit = git("rev-parse", "HEAD")
    git("branch", "collision")
    git("tag", "collision")
    git(
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.invalid",
        "tag",
        "-am",
        "annotated",
        "v1",
    )
    config = tmp_path / "gitconfig"
    config.write_text(
        f'[url "{source}"]\n insteadOf = https://github.com/NinjaRoboticsEducation/NinjaRobotPi0.git\n'
    )
    binaries = tmp_path / "bin"
    binaries.mkdir()
    (binaries / "uname").write_text(
        '#!/bin/sh\ncase "$1" in -s) echo Linux;; -m) echo aarch64;; esac\n'
    )
    (binaries / "grep").write_text(
        '#!/bin/sh\ncase "$*" in */proc/device-tree/model*|*/etc/os-release*) exit 0;; esac\nexec /usr/bin/grep "$@"\n'
    )
    if os.uname().sysname == "Darwin":
        # macOS has no GNU -T. This fixture performs only the equivalent no-clobber move.
        (binaries / "mv").write_text(
            "#!/usr/bin/env python3\nimport sys,os\na,b=sys.argv[-2:]\nif not os.path.lexists(b): os.rename(a,b)\n"
        )
    for script in binaries.iterdir():
        script.chmod(0o755)
    return commit, {
        **os.environ,
        "GIT_CONFIG_GLOBAL": str(config),
        "GIT_CONFIG_NOSYSTEM": "1",
        "PATH": f"{binaries}:{os.environ['PATH']}",
    }


@pytest.mark.parametrize(
    "ref",
    [
        "HEAD",
        "v1",
        "COMMIT",
        "refs/heads/collision",
        "refs/tags/collision",
        "collision",
        "missing",
    ],
)
def test_resolved_checkout_and_failure_cleanup(remote, ref, tmp_path):
    commit, environment = remote
    destination = tmp_path / "robot with spaces"
    result = subprocess.run(
        [
            "bash",
            "-s",
            "--",
            "--install-dir",
            str(destination),
            "--ref",
            commit if ref == "COMMIT" else ref,
            "--yes",
        ],
        input=(ROOT / "install.sh").read_text(),
        text=True,
        capture_output=True,
        env=environment,
        timeout=20,
    )
    if ref in ("collision", "missing"):
        assert result.returncode != 0
        assert not destination.exists()
    else:
        assert result.returncode == 0, result.stderr
        assert "inert:--yes" in result.stdout
        assert (
            subprocess.check_output(
                ["git", "-C", str(destination), "rev-parse", "HEAD"], text=True
            ).strip()
            == commit
        )
    assert not list(tmp_path.glob(".ninjarobot-bootstrap.*"))
    assert not destination.with_suffix(".bootstrap-lock").exists()


def test_existing_destination_is_never_overwritten(remote, tmp_path):
    _, environment = remote
    destination = tmp_path / "robot"
    destination.mkdir()
    (destination / "user.txt").write_text("keep")
    result = subprocess.run(
        ["bash", "-s", "--", "--install-dir", str(destination), "--yes"],
        input=(ROOT / "install.sh").read_text(),
        text=True,
        capture_output=True,
        env=environment,
    )
    assert result.returncode != 0
    assert (destination / "user.txt").read_text() == "keep"


def test_stream_does_not_delegate_to_cwd_lookalike(tmp_path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts/install-rpi.sh").write_text("exit 99")
    (tmp_path / "uv.lock").write_text("fixture")
    result = subprocess.run(
        ["bash", "-s", "--", "--dry-run"],
        input=(ROOT / "install.sh").read_text(),
        text=True,
        capture_output=True,
        cwd=tmp_path,
    )
    assert result.returncode == 0
    assert "Preview: official Pi0 repository" in result.stdout


@pytest.mark.parametrize(
    "bad_download, uv_failure, user_tools",
    [
        (False, False, False),
        (True, False, False),
        (False, True, False),
        (False, False, True),
    ],
)
def test_local_install_is_rerunnable_or_stops_on_bad_hash(
    tmp_path, bad_download, uv_failure, user_tools
):
    checkout = tmp_path / "checkout"
    (checkout / "scripts").mkdir(parents=True)
    (checkout / "ninja_webapp").mkdir()
    (checkout / "servo.json").write_text("preserve calibration")
    for name in ["install-rpi.sh", "install-versions.env", "install_check.py"]:
        shutil_source = ROOT / "scripts" / name
        (checkout / "scripts" / name).write_bytes(shutil_source.read_bytes())
    binaries = tmp_path / "bin"
    binaries.mkdir()
    log = tmp_path / "calls"
    scripts = {
        # Selecting the host's /usr/bin/node would prepend /usr/bin and bypass
        # the inert systemctl fixture on a real Pi. Tool selection itself is
        # covered separately; constrain this integration fixture to its tools.
        "python3": f'case "$*" in *--find-tool*node) printf "%s\\n" "$FIXTURE_NODE";; *--find-tool*) exec {__import__("sys").executable} "$@";; *) exit 0;; esac',
        "sudo": 'printf "sudo:%s\\n" "$*" >> "$CALL_LOG"',
        "systemctl": 'case "$1" in is-active) exit 3;; cat) exit 0;; esac',
        "pigpiod": "echo 79",
        "uv": "exit 1",
        "node": "exit 1",
        "npm": 'printf "npm:%s\\n" "$*" >> "$CALL_LOG"',
        "curl": 'while [ "$1" != -o ]; do shift; done; printf invalid > "$2"',
    }
    for name, body in scripts.items():
        p = binaries / name
        p.write_text("#!/bin/sh\n" + body + "\n")
        p.chmod(0o755)
    tools = tmp_path / "home/.local/share/ninjarobot_pi0/tools"
    (tools / "node/bin").mkdir(parents=True)
    p = tools / "node/bin/node"
    p.write_text("#!/bin/sh\necho v22.23.3\n")
    p.chmod(0o755)
    if not bad_download:
        (tools / "uv").mkdir()
        p = tools / "uv/uv"
        p.write_text(
            '#!/bin/sh\n[ -z "${UV_PROJECT_ENVIRONMENT:-}${UV_PROJECT:-}${VIRTUAL_ENV:-}" ] || exit 7\ncase "$1" in --version) echo "uv 0.9.26";; venv) if [ "${2:-}" = --help ]; then echo "--allow-existing --prompt --python"; exit 0; fi; [ "${UV_FAIL:-0}" = 0 ] || exit 7; printf "uv:%s\\n" "$*" >> "$CALL_LOG";; sync) if [ "${2:-}" = --help ]; then echo "--locked --no-dev --python --directory --all-extras"; exit 0; fi; [ "${UV_FAIL:-0}" = 0 ] || exit 7; printf "uv:%s\\n" "$*" >> "$CALL_LOG";; *) [ "${UV_FAIL:-0}" = 0 ] || exit 7; printf "uv:%s\\n" "$*" >> "$CALL_LOG";; esac\n'
        )
        p.chmod(0o755)
    if user_tools:
        (binaries / "node").write_text("#!/bin/sh\necho v24.21.0\n")
        (binaries / "uv").write_bytes((tools / "uv/uv").read_bytes())
        # These older private versions must not override compatible user tools.
        (tools / "node/bin/node").write_text("#!/bin/sh\nexit 91\n")
        (tools / "uv/uv").write_text("#!/bin/sh\nexit 92\n")
    env = {
        **os.environ,
        "HOME": str(tmp_path / "home"),
        "CALL_LOG": str(log),
        "FIXTURE_NODE": str(binaries / "node" if user_tools else tools / "node/bin/node"),
        "UV_FAIL": "1" if uv_failure else "0",
        "UV_PROJECT_ENVIRONMENT": str(tmp_path / "unrelated-venv"),
        "UV_PROJECT": str(tmp_path / "unrelated-project"),
        "VIRTUAL_ENV": str(tmp_path / "unrelated-venv"),
        "PATH": str(binaries) + ":/usr/bin:/bin",
    }
    for _ in range(2 if not (bad_download or uv_failure) else 1):
        result = subprocess.run(
            ["bash", str(checkout / "scripts/install-rpi.sh"), "--yes"],
            env=env,
            capture_output=True,
            text=True,
        )
        assert result.returncode == (1 if bad_download else 7 if uv_failure else 0), (
            result.stderr
        )
        assert (checkout / "servo.json").read_text() == "preserve calibration"
        assert not (checkout / ".ninjarobot-install.lock").exists()
    calls = log.read_text()
    if uv_failure:
        assert (
            "Installation stopped during: Locked Python environment (.venv) (exit 7)"
            in result.stderr
        )
        assert "./install.sh" in result.stderr
        assert "npm:ci" not in calls and "npm:run" not in calls
    elif bad_download:
        assert "Installation stopped during: Compatible uv tooling" in result.stderr
        assert "checksum mismatch" in result.stderr
        assert "npm:ci" not in calls and "npm:run" not in calls
    else:
        assert calls.count("npm:ci --include=dev --no-audit --no-fund") == 2
        assert calls.count("uv:venv --allow-existing --prompt ninjarobotpi0 --python /usr/bin/python3 .venv") == 2
    assert "systemctl start" not in calls and "ninja_core server" not in calls
