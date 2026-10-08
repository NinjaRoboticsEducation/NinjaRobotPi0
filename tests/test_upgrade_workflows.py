"""Installation/onboarding boundaries tested without hardware or network."""

import importlib.util
import json
import os
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


onboard = load("onboard")


@pytest.mark.parametrize(
    "script", ["install.sh", "scripts/install-rpi.sh", "onboard.sh"]
)
def test_preview_does_not_mutate(script, tmp_path):
    environment = {
        **os.environ,
        "HOME": str(tmp_path),
        "XDG_STATE_HOME": str(tmp_path / "state"),
    }
    result = subprocess.run(
        ["bash", str(ROOT / script), "--dry-run"],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize("args", [["--unknown"], ["--check", "--dry-run"], ["--ref"]])
def test_installer_invalid_arguments_fail_before_install(args):
    result = subprocess.run(
        ["bash", str(ROOT / "install.sh"), *args], capture_output=True
    )
    assert result.returncode == 2


def test_missing_calibration_read_is_nonmutating(tmp_path):
    assert onboard.config_status(tmp_path, "servo") == {"valid": False, "hash": None}
    assert not list(tmp_path.iterdir())


def calibration(root, value):
    (root / "servo.json").write_text(json.dumps({"20": value}))


@pytest.mark.parametrize(
    "pulses,valid",
    [
        ((500, 1500, 2500), True),
        ((1500, 1500, 1500), False),
        ((500, 3000, 2500), False),
    ],
)
def test_calibration_not_defaults_or_reversed(pulses, valid, tmp_path):
    calibration(tmp_path, dict(zip(("pulse_min", "pulse_center", "pulse_max"), pulses)))
    assert onboard.config_status(tmp_path, "servo")["valid"] == valid


def test_progress_is_private_and_secret_free(tmp_path):
    state = tmp_path / "state/onboarding.json"
    value = {"steps": {"gemini": {"result": "configured_unverified"}}}
    onboard.atomic_private(state, value)
    assert json.loads(state.read_text()) == value
    assert state.stat().st_mode & 0o777 == 0o600
    assert not list(state.parent.glob(".onboard-*"))


def test_progress_refuses_symlink(tmp_path):
    target = tmp_path / "private"
    target.write_text("untouched")
    link = tmp_path / "onboarding.json"
    link.symlink_to(target)
    with pytest.raises(ValueError):
        onboard.atomic_private(link, {})
    assert target.read_text() == "untouched"


def test_progress_lock_excludes_second_writer(tmp_path):
    state = tmp_path / "state/progress.json"
    with onboard.progress_lock(state):
        with pytest.raises(FileExistsError):
            with onboard.progress_lock(state):
                pytest.fail("Second writer entered")
    assert not state.with_suffix(".lock").exists()


def test_import_blocks_default_calibration_without_calling_core(tmp_path):
    called = []
    answers = iter(["1"])
    onboard.wizard(
        tmp_path,
        tmp_path / "progress.json",
        SimpleNamespace(step="import"),
        ask=lambda _: next(answers),
        execute=lambda *args: called.append(args),
    )
    assert called == []
    assert not (tmp_path / "config.json").exists()


def test_servo_tool_requires_prelaunch_confirmation(tmp_path):
    called = []
    answers = iter(["1", "not ready", "q"])
    onboard.wizard(
        tmp_path,
        tmp_path / "progress.json",
        SimpleNamespace(step="servo"),
        ask=lambda _: next(answers),
        execute=lambda *args: called.append(args),
    )
    assert called == []


def test_zero_exit_without_configuration_is_not_success(tmp_path, monkeypatch):
    monkeypatch.setattr(onboard, "hardware_ready", lambda: None)
    answers = iter(["1", "READY", "q"])
    state = tmp_path / "progress.json"
    onboard.wizard(
        tmp_path,
        state,
        SimpleNamespace(step="servo"),
        ask=lambda _: next(answers),
        execute=lambda *_: 0,
    )
    assert (
        json.loads(state.read_text())["steps"]["servo"]["result"] == "needs_attention"
    )


def test_reuse_never_claims_physical_validation(tmp_path):
    calibration(tmp_path, {"pulse_min": 500, "pulse_center": 1500, "pulse_max": 2500})
    state = tmp_path / "progress.json"
    onboard.wizard(
        tmp_path,
        state,
        SimpleNamespace(step="servo"),
        ask=lambda _: "2",
        execute=lambda *_: pytest.fail("Unexpected hardware launch"),
    )
    assert (
        json.loads(state.read_text())["steps"]["servo"]["observation"] == "not_checked"
    )


def test_protected_robot_sources_unchanged():
    checker = load("verify_core")
    assert checker.verify(ROOT) == []


def test_system_policy_restored_after_apt_failure(tmp_path, monkeypatch):
    setup = load("install_system")
    monkeypatch.setattr(setup.os, "geteuid", lambda: 0)
    policy = tmp_path / "policy-rc.d"

    def fail(*_args, **_kwargs):
        assert policy.read_text() == "#!/bin/sh\nexit 101\n"
        raise subprocess.CalledProcessError(1, "apt-get")

    with pytest.raises(subprocess.CalledProcessError):
        setup.install_packages(policy, run=fail)
    assert not policy.exists()


def test_existing_admin_policy_preserved(tmp_path, monkeypatch):
    setup = load("install_system")
    monkeypatch.setattr(setup.os, "geteuid", lambda: 0)
    policy = tmp_path / "policy-rc.d"
    policy.write_text("administrator policy")
    with pytest.raises(FileExistsError):
        setup.install_packages(policy, run=lambda *_: pytest.fail("Unexpected apt"))
    assert policy.read_text() == "administrator policy"


def test_private_state_parent_symlink_rejected(tmp_path):
    target = tmp_path / "real"
    target.mkdir()
    alias = tmp_path / "alias"
    alias.symlink_to(target)
    with pytest.raises(ValueError):
        onboard.atomic_private(alias / "progress.json", {})
    assert not list(target.iterdir())


@pytest.mark.parametrize("failure", [RuntimeError, KeyboardInterrupt])
@pytest.mark.parametrize("existing", [True, False])
def test_ngrok_failure_restores_selected_file(
    tmp_path, monkeypatch, failure, existing, capsys
):
    import sys
    from types import ModuleType

    robot = tmp_path / "config.json"
    robot.write_bytes(b'{"identity": "existing"}')
    ngrok = tmp_path / "ngrok.yml"
    prior = b"version: 3\nold-setting: retain\n" if existing else None
    if existing:
        ngrok.write_bytes(prior)
    fake = ModuleType("pyngrok")
    fake.conf = SimpleNamespace(
        get_default=lambda: None, get_config_path=lambda _: str(ngrok)
    )
    helper = ModuleType("ninja_core.ngrok_config")

    def fail(_token):
        ngrok.write_bytes(b"partial new settings")
        robot.write_bytes(b"partial robot settings")
        raise failure("Do not disclose secret input")

    helper.set_ngrok_auth_token = fail
    monkeypatch.setitem(sys.modules, "pyngrok", fake)
    monkeypatch.setitem(sys.modules, "ninja_core.ngrok_config", helper)
    monkeypatch.setattr(onboard, "ROOT", tmp_path)
    monkeypatch.setattr(onboard.getpass, "getpass", lambda _: "dummy-private-input")
    assert onboard.worker("ngrok") == 1
    assert robot.read_bytes() == b'{"identity": "existing"}'
    assert (ngrok.read_bytes() if ngrok.exists() else None) == prior
    assert "dummy-private-input" not in capsys.readouterr().out
    assert not list(tmp_path.glob(".config-restore-*"))


def test_bootstrap_release_allowlist_accepts_bookworm_and_trixie(tmp_path):
    # Exercise the actual shell expression; hardware identity is independently gated.
    script = (ROOT / "install.sh").read_text()
    line = next(
        line.strip() for line in script.splitlines() if "VERSION_CODENAME=" in line
    )
    command = line.split(" || ", 1)[0].replace(
        "/etc/os-release", str(tmp_path / "release")
    )
    for release, expected in [
        ("VERSION_CODENAME=bookworm", 0),
        ('VERSION_CODENAME="bookworm"', 0),
        ("VERSION_CODENAME=trixie", 0),
        ('VERSION_CODENAME="trixie"', 0),
        ("VERSION_CODENAME=bullseye", 1),
        ("VERSION_CODENAME=forky", 1),
        ("VERSION_CODENAME=trixie-testing", 1),
        ("", 1),
    ]:
        (tmp_path / "release").write_text(release + "\n")
        assert subprocess.run(["bash", "-c", command]).returncode == expected


@pytest.mark.parametrize("record", [None, "invalid", {"result": "invented"}])
def test_invalid_progress_retained_without_overwrite(tmp_path, record):
    state = tmp_path / "progress.json"
    original = json.dumps({"version": 1, "steps": {"servo": record}})
    state.write_text(original)
    with pytest.raises(ValueError):
        onboard.wizard(
            tmp_path, state, SimpleNamespace(step="servo"), ask=lambda _: "q"
        )
    assert state.read_text() == original


def test_resume_skips_only_unchanged_valid_hardware(tmp_path):
    calibration(tmp_path, {"pulse_min": 500, "pulse_center": 1500, "pulse_max": 2500})
    state = tmp_path / "progress.json"
    progress = {"version": 1, "steps": {}}
    onboard.reuse(progress, "servo", onboard.config_status(tmp_path, "servo"))
    onboard.atomic_private(state, progress)
    onboard.wizard(
        tmp_path,
        state,
        SimpleNamespace(step="servo", resume=True),
        ask=lambda _: pytest.fail("Unchanged hardware should be skipped"),
    )
    calibration(tmp_path, {"pulse_min": 600, "pulse_center": 1500, "pulse_max": 2500})
    onboard.wizard(
        tmp_path, state, SimpleNamespace(step="servo", resume=True), ask=lambda _: "q"
    )
    record = json.loads(state.read_text())["steps"]["servo"]
    assert record["result"] == "needs_attention"
    assert record["observation"] == "not_checked"


def test_failed_hardware_can_retry_in_same_session(tmp_path, monkeypatch):
    monkeypatch.setattr(onboard, "hardware_ready", lambda: None)
    attempts = []

    def execute(*_):
        attempts.append(1)
        if len(attempts) == 2:
            calibration(
                tmp_path, {"pulse_min": 500, "pulse_center": 1500, "pulse_max": 2500}
            )
        return 0

    answers = iter(["invalid", "1", "READY", "1", "READY", "yes", ""])
    state = tmp_path / "progress.json"
    onboard.wizard(
        tmp_path,
        state,
        SimpleNamespace(step="servo"),
        ask=lambda _: next(answers),
        execute=execute,
    )
    assert len(attempts) == 2
    assert (
        json.loads(state.read_text())["steps"]["servo"]["observation"]
        == "operator_checked"
    )


def test_credential_worker_uses_private_umask_and_restores_it(tmp_path, monkeypatch):
    monkeypatch.setattr(onboard, "ROOT", tmp_path)

    def helper(_):
        (tmp_path / "config.json").write_text("{}")
        assert (tmp_path / "config.json").stat().st_mode & 0o777 == 0o600
        raise RuntimeError("cancel")

    monkeypatch.setattr(onboard, "_worker", helper)
    mask = os.umask(0o022)
    try:
        with pytest.raises(RuntimeError):
            onboard.worker("identity")
        current = os.umask(0o022)
        assert current == 0o022
    finally:
        os.umask(mask)


@pytest.mark.parametrize(
    "addition",
    [
        {"min_pulse": 2400},
        {"center_pulse": 3000},
        {"max_pulse": 500},
    ],
)
def test_import_cannot_override_validated_servo_pulses(tmp_path, addition):
    calibration(
        tmp_path,
        {"pulse_min": 500, "pulse_center": 1500, "pulse_max": 2500, **addition},
    )
    assert not onboard.config_status(tmp_path, "servo")["valid"]


@pytest.mark.parametrize("pin", ["-1", "+20", "020", "28"])
def test_import_checks_every_numeric_servo_key(tmp_path, pin):
    value = {"pulse_min": 500, "pulse_center": 1500, "pulse_max": 2500}
    (tmp_path / "servo.json").write_text(json.dumps({"20": value, pin: value}))
    assert not onboard.config_status(tmp_path, "servo")["valid"]


def test_installer_rejects_nested_tool_symlink_before_changes(tmp_path, monkeypatch):
    check = load("install_check")
    monkeypatch.setattr(check.Path, "home", lambda: tmp_path)
    tools = tmp_path / ".local/share/ninjarobot_pi0/tools"
    tools.mkdir(parents=True)
    target = tmp_path / "elsewhere"
    target.mkdir()
    (tools / "uv").symlink_to(target)
    assert check.path_errors(tmp_path)
    assert not list(target.iterdir())


def test_wiki_environment_does_not_redirect_project(monkeypatch):
    wiki = load("wiki")
    for name in ("VIRTUAL_ENV", "UV_PROJECT_ENVIRONMENT", "UV_PROJECT"):
        monkeypatch.setenv(name, "/unrelated/project")
    environment = wiki.child_environment()
    assert all(
        name not in environment
        for name in ("VIRTUAL_ENV", "UV_PROJECT_ENVIRONMENT", "UV_PROJECT")
    )


def test_wiki_setup_finds_installer_private_uv(tmp_path, monkeypatch):
    wiki = load("wiki")
    private = tmp_path / ".local/share/ninjarobot_pi0/tools/uv/uv"
    private.parent.mkdir(parents=True)
    private.write_text("#!/bin/sh\nexit 0\n")
    private.chmod(0o700)
    monkeypatch.setattr(wiki.Path, "home", lambda: tmp_path)
    monkeypatch.setattr(wiki.shutil, "which", lambda _: None)
    calls = []
    monkeypatch.setattr(
        wiki.subprocess,
        "run",
        lambda command, **kwargs: calls.append(command)
        or SimpleNamespace(returncode=0),
    )
    assert wiki.main(["setup"]) == 0
    assert calls[0][0] == str(private)
    assert "--locked" in calls[0]


def test_bulk_reuse_guides_missing_hardware_without_launch(tmp_path):
    calibration(tmp_path, {"pulse_min": 500, "pulse_center": 1500, "pulse_max": 2500})
    answers = iter(["2", "", "q"])
    state = tmp_path / "progress.json"
    onboard.wizard(
        tmp_path,
        state,
        SimpleNamespace(step=None),
        ask=lambda _: next(answers),
        execute=lambda *_: pytest.fail("No tool selected"),
    )
    progress = json.loads(state.read_text())
    assert progress["steps"]["servo"]["result"] == "software_validated"
    assert progress["steps"]["servo"]["observation"] == "not_checked"
    assert "display" not in progress["steps"]


def test_worker_cannot_bypass_supported_platform(tmp_path, monkeypatch):
    import sys

    check = load("install_check")
    monkeypatch.setitem(sys.modules, "install_check", check)
    monkeypatch.setattr(check, "platform_errors", lambda: ["unsupported"])
    monkeypatch.setattr(sys, "argv", ["onboard.py", "--worker", "identity"])
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(
        onboard, "worker", lambda _: pytest.fail("Worker bypassed preflight")
    )
    with pytest.raises(ValueError, match="Bookworm"):
        onboard.main()


def test_record_failure_removes_temporary_file(tmp_path, monkeypatch):
    recorder = load("install_record")
    for name in (
        "uv.lock",
        "ninja_webapp/package-lock.json",
        "scripts/install-versions.env",
    ):
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture")
    monkeypatch.setattr(
        recorder.subprocess,
        "run",
        lambda *a, **kw: SimpleNamespace(stdout="fixture-commit"),
    )
    monkeypatch.setattr(
        recorder.os,
        "replace",
        lambda *a: (_ for _ in ()).throw(OSError("disk failure")),
    )
    with pytest.raises(OSError):
        recorder.record(tmp_path)
    assert not list((tmp_path / ".ninjarobot-install").iterdir())


def test_cancel_after_tool_invalidates_old_physical_observation(tmp_path, monkeypatch):
    monkeypatch.setattr(onboard, "hardware_ready", lambda: None)
    calibration(tmp_path, {"pulse_min": 500, "pulse_center": 1500, "pulse_max": 2500})
    progress = {"version": 1, "steps": {}}
    onboard.reuse(progress, "servo", onboard.config_status(tmp_path, "servo"))
    progress["steps"]["servo"]["observation"] = "operator_checked"
    state = tmp_path / "progress.json"
    onboard.atomic_private(state, progress)
    answers = iter(["1", "READY"])

    def ask(_):
        try:
            return next(answers)
        except StopIteration:
            raise KeyboardInterrupt from None

    def execute(*_):
        calibration(
            tmp_path, {"pulse_min": 600, "pulse_center": 1500, "pulse_max": 2500}
        )
        return 0

    onboard.wizard(
        tmp_path, state, SimpleNamespace(step="servo"), ask=ask, execute=execute
    )
    record = json.loads(state.read_text())["steps"]["servo"]
    assert record["observation"] == "not_checked"
    assert record["result"] == "needs_attention"


@pytest.mark.parametrize(
    "codename", ["bookworm", "trixie", "bullseye", "forky", "trixie-testing", ""]
)
@pytest.mark.parametrize("quoted", [False, True])
def test_platform_release_matrix(tmp_path, monkeypatch, codename, quoted):
    check = load("install_check")
    monkeypatch.setattr(check.platform, "system", lambda: "Linux")
    monkeypatch.setattr(check.platform, "machine", lambda: "aarch64")
    monkeypatch.setattr(check.os, "geteuid", lambda: 1000)
    model = tmp_path / "model"
    model.write_text("Raspberry Pi Zero 2 W Rev 1.0\0")
    release = tmp_path / "os-release"
    value = f'"{codename}"' if quoted else codename
    release.write_text(
        f'PRETTY_NAME="Debian GNU/Linux 13 (trixie)"\nID=debian\nVERSION_CODENAME={value}\n'
    )
    errors = check.platform_errors(model, release)
    assert (not errors) == (codename in ("bookworm", "trixie"))
    if errors:
        assert "detected ID=debian" in errors[0]


@pytest.mark.parametrize(
    "machine,model_name,uid,identity",
    [
        ("armv7l", "Raspberry Pi Zero 2 W", 1000, "debian"),
        ("aarch64", "Raspberry Pi 5", 1000, "debian"),
        ("aarch64", "Raspberry Pi Zero 2 W", 0, "debian"),
        ("aarch64", "Raspberry Pi Zero 2 W", 1000, "ubuntu"),
    ],
)
def test_trixie_keeps_hardware_arch_user_distribution_gates(
    tmp_path, monkeypatch, machine, model_name, uid, identity
):
    check = load("install_check")
    monkeypatch.setattr(check.platform, "system", lambda: "Linux")
    monkeypatch.setattr(check.platform, "machine", lambda: machine)
    monkeypatch.setattr(check.os, "geteuid", lambda: uid)
    model = tmp_path / "model"
    model.write_text(model_name)
    release = tmp_path / "release"
    release.write_text(f"ID={identity}\nVERSION_CODENAME=trixie\n")
    assert check.platform_errors(model, release)
