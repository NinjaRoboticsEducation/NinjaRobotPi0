"""Guided Pi0 setup. Existing hardware tools run only after explicit selection."""

from __future__ import annotations

import argparse
import getpass
import hashlib
import json
import math
import os
import signal
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIGS = {
    "display": "pi0disp/display.json",
    "buzzer": "buzzer.json",
    "servo": "servo.json",
    "distance": "pi0vl53l0x/src/pi0vl53l0x/config/vl53l0x.json",
}
TOOLS = {
    "display": ("pi0disp", "display-tool"),
    "buzzer": ("pi0buzzer", "buzzer-tool"),
    "servo": ("pi0servo", "servo-tool", "--config", "servo.json"),
    "distance": ("pi0vl53l0x", "sensor-tool"),
}
STEPS = (*TOOLS, "import", "identity", "gemini", "ngrok")


def read_json(path):
    if path.is_symlink():
        raise ValueError("Refusing redirected configuration")
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError("Expected a saved configuration object")
    return value


def number(value):
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


def config_status(root, step):
    """Read existing bytes only: no driver imports/default creation."""
    path = root / CONFIGS[step]
    try:
        validate_state_path(path)
        raw = path.read_bytes()
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError("Expected a configuration object")
        if step == "servo":
            values = []
            for key, value in data.items():
                try:
                    pin = int(key)
                except ValueError:
                    continue  # Existing importer permits non-numeric metadata.
                if key != str(pin):
                    return {"valid": False, "hash": None}
                values.append((key, value))
            valid = bool(values) and all(
                0 <= int(pin) <= 27
                and isinstance(v, dict)
                and all(
                    number(v.get(k)) for k in ("pulse_min", "pulse_center", "pulse_max")
                )
                and all(
                    alias not in v or v[alias] == v[field]
                    for alias, field in (
                        ("min_pulse", "pulse_min"),
                        ("center_pulse", "pulse_center"),
                        ("max_pulse", "pulse_max"),
                    )
                )
                and 0 < v["pulse_min"] < v["pulse_center"] < v["pulse_max"] <= 2500
                and number(v.get("speed", 80))
                and 0 <= v.get("speed", 80) <= 100
                for pin, v in values
            )
        elif step == "display":
            valid = all(
                isinstance(data.get(k), int)
                and not isinstance(data[k], bool)
                and 0 <= data[k] <= 27
                for k in ("dc_pin", "rst_pin", "backlight_pin")
            )
            valid = (
                valid
                and data.get("rotation") in (0, 90, 180, 270)
                and number(data.get("brightness"))
                and 0 <= data["brightness"] <= 100
            )
        elif step == "buzzer":
            valid = (
                isinstance(data.get("pin"), int)
                and not isinstance(data["pin"], bool)
                and 0 <= data["pin"] <= 27
            )
        else:
            valid = number(data.get("offset_mm"))
        digest = hashlib.sha256(raw).hexdigest() if valid else None
        return {"valid": bool(valid), "hash": digest}
    except (OSError, ValueError, TypeError, KeyError):
        return {"valid": False, "hash": None}


def validate_state_path(path):
    for component in (path, *path.parents):
        if component.is_symlink():
            raise ValueError("Refusing redirected private state")


def atomic_private(path, value):
    if path.is_symlink():
        raise ValueError("Refusing redirected progress file")
    validate_state_path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    for parent in (path.parent, *path.parent.parents):
        if parent.is_symlink():
            raise ValueError("Refusing redirected state directory")
    descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=".onboard-")
    try:
        with os.fdopen(descriptor, "w") as stream:
            json.dump(value, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


@contextmanager
def progress_lock(path):
    validate_state_path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    lock = path.with_suffix(".lock")
    descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        yield
    finally:
        os.close(descriptor)
        lock.unlink()


def run_child(command, root):
    """Inherit the real TTY; give existing tools time for their own cleanup."""
    process = subprocess.Popen(command, cwd=root)
    try:
        return process.wait()
    except KeyboardInterrupt:
        if process.poll() is None:
            process.send_signal(signal.SIGINT)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print(
                    "Tool cleanup is not confirmed. Remove actuator power before continuing."
                )
                # Do not silently SIGKILL an active device tool.
                process.wait()
        raise


def hardware_ready():
    for service in ("ninjarobot",):
        if (
            subprocess.run(
                ["systemctl", "is-active", "--quiet", service], check=False
            ).returncode
            == 0
        ):
            raise ValueError("Stop the robot server before standalone calibration.")
    if subprocess.run(
        ["systemctl", "is-active", "--quiet", "pigpiod"], check=False
    ).returncode:
        raise ValueError(
            "Activate pigpiod deliberately first: sudo systemctl start pigpiod"
        )


def _worker(action):
    """Secret input stays in this foreground process, never in command arguments."""
    config = ROOT / "config.json"
    prior = (
        config.read_bytes() if config.is_file() and not config.is_symlink() else None
    )
    validate_state_path(config)
    if config.is_symlink():
        raise ValueError("Refusing redirected robot configuration")
    ngrok_path = None
    ngrok_prior = None
    try:
        if action == "gemini":
            from ninja_core.init_tool import configure_gemini_api_key

            key = getpass.getpass("Google Gemini API key (blank to cancel): ").strip()
            if not key:
                return 2
            configure_gemini_api_key(key)
            config.chmod(0o600)
        elif action == "ngrok":
            from pyngrok import conf
            from ninja_core.ngrok_config import set_ngrok_auth_token

            token = getpass.getpass("ngrok token (blank to cancel): ").strip()
            if not token:
                return 2
            # Back up the actual helper-selected path before it can write/download.
            candidate = (
                Path(conf.get_config_path(conf.get_default())).expanduser().absolute()
            )
            validate_state_path(candidate)
            ngrok_prior = candidate.read_bytes() if candidate.exists() else None
            ngrok_path = candidate
            if candidate.exists():
                candidate.chmod(0o600)
            if not set_ngrok_auth_token(token):
                raise ValueError("Token was not saved")
            if ngrok_path.exists():
                ngrok_path.chmod(0o600)
            print(
                "ngrok token saved through existing storage; remote access not tested."
            )
        elif action == "identity":
            from ninja_core.config import set_robot_name, set_robot_type

            name = input("Robot name (blank to keep): ").strip()
            kind = input("Type tire/humanoid/spider (blank to keep): ").strip()
            if name:
                set_robot_name(name)
            if kind:
                set_robot_type(kind)
        elif action == "import":
            if not all(
                config_status(ROOT, step)["valid"]
                for step in ("display", "buzzer", "servo")
            ):
                raise ValueError("Saved hardware configuration is incomplete")
            from ninja_core.config import import_and_update_config

            import_and_update_config()
        if config.exists():
            config.chmod(0o600)
        return 0
    except (Exception, KeyboardInterrupt):
        if ngrok_path is not None:
            restore_private(ngrok_path, ngrok_prior)
        # Helpers validate before commit; keep a private rollback for partial changes.
        restore_private(config, prior)
        print(
            "Step failed or cancelled. Previous robot settings retained; retry when ready."
        )
        return 1


def restore_private(path, prior):
    """Restore in-memory settings without recording credentials in progress/logs."""
    validate_state_path(path)
    if prior is None:
        path.unlink(missing_ok=True)
        return
    descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=".config-restore-")
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(prior)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def worker(action):
    """Keep helper-created credentials private from their first write."""
    mask = os.umask(0o077)
    try:
        config = ROOT / "config.json"
        validate_state_path(config)
        if config.exists():
            config.chmod(0o600)
        return _worker(action)
    finally:
        os.umask(mask)


def load_progress(path):
    validate_state_path(path)
    if not path.exists():
        return {"version": 1, "steps": {}}
    if path.stat().st_size > 1_048_576:
        raise ValueError("Oversized progress file; retained without changes")
    value = read_json(path)
    if value.get("version") != 1 or not isinstance(value.get("steps"), dict):
        raise ValueError("Unsupported progress schema; retained without changes")
    for name, record in value["steps"].items():
        if name not in STEPS or not isinstance(record, dict):
            raise ValueError("Invalid progress step; retained without changes")
        if record.get("result") not in (
            "software_validated",
            "configured_unverified",
            "needs_attention",
        ):
            raise ValueError("Invalid progress result; retained without changes")
        if name in TOOLS and (
            not isinstance(record.get("valid"), bool)
            or record.get("observation") not in ("not_checked", "operator_checked")
            or (
                record.get("hash") is not None
                and (
                    not isinstance(record["hash"], str)
                    or len(record["hash"]) != 64
                    or any(c not in "0123456789abcdef" for c in record["hash"])
                )
            )
        ):
            raise ValueError("Invalid hardware progress; retained without changes")
    return value


def reconcile(progress, root):
    """Changed/missing settings cannot retain a previous physical observation."""
    for step in TOOLS:
        prior = progress["steps"].get(step)
        current = config_status(root, step)
        if prior and (not current["valid"] or prior.get("hash") != current["hash"]):
            prior.update(current, result="needs_attention", observation="not_checked")


def choice(ask, prompt, allowed):
    while True:
        answer = ask(prompt).strip().lower()
        if answer in allowed:
            return answer
        print("Choose one of the displayed options.")


def reuse(progress, step, status):
    prior = progress["steps"].get(step, {})
    progress["steps"][step] = {
        **status,
        "result": "software_validated",
        "observation": prior.get("observation", "not_checked")
        if prior.get("hash") == status["hash"]
        else "not_checked",
    }


def summary(progress):
    print("\nSetup summary")
    for step in STEPS:
        record = progress["steps"].get(step, {})
        result = record.get("result", "pending")
        observation = record.get("observation")
        print(f"  {step}: {result}" + (f" ({observation})" if observation else ""))
    print(
        "Saved. Resume with ./onboard.sh --resume. Server/startup/reboot remain manual."
    )


GUIDANCE = {
    "display": (
        "The display shows the robot face and status.",
        "Wiring, rotation and brightness must match your display.",
        "Use the existing tool to configure, show text and clear; inspect the orientation.",
    ),
    "buzzer": (
        "The buzzer is the robot's sound output.",
        "The saved GPIO and audible output must match your wiring.",
        "Configure the pin, play a short tone and confirm silence before exiting.",
    ),
    "servo": (
        "Servos move the wheels or limbs of your selected robot.",
        "Every connected servo needs its own verified calibration.",
        "Support all wheels/limbs. Calibrate each connected servo in the existing tool.",
    ),
    "distance": (
        "The distance sensor measures objects ahead.",
        "The sensor must produce plausible readings before saving an offset.",
        "Read a stationary target, then calibrate against a measured distance.",
    ),
}


def hardware_step(root, step, progress, ask, execute):
    what, why, action = GUIDANCE[step]
    print(f"What is this? {what}\nWhy is this needed? {why}\nWhat to do: {action}")
    while True:
        status = config_status(root, step)
        print(
            "Status: "
            + ("valid saved configuration" if status["valid"] else "setup needed")
        )
        options = "1) Open setup tool\n" + (
            "2) Reuse validated settings\n" if status["valid"] else ""
        )
        selected = choice(
            ask,
            options + "Q) Save and exit\nChoose: ",
            {"1", "2", "q"} if status["valid"] else {"1", "q"},
        )
        if selected == "q":
            return False
        if selected == "2":
            reuse(progress, step, status)
            print(
                "Saved configuration checked; this does not prove physical operation."
            )
            ask("Press ENTER to continue: ")
            return True
        print(
            "All configured servos may center immediately. Support every limb/wheel, clear travel, and be ready to remove power."
            if step == "servo"
            else "This opens the existing device tool and can activate the component."
        )
        if ask("Type READY to open the tool: ").strip() != "READY":
            print("Tool not opened.")
            continue
        try:
            hardware_ready()
            code = execute(
                [str(root / ".venv/bin" / TOOLS[step][0]), *TOOLS[step][1:]], root
            )
        except (OSError, ValueError):
            print(
                "Could not open setup. Check installation, stop the robot server and deliberately start pigpiod."
            )
            code = 1
        current = config_status(root, step)
        success = current["valid"] and code == 0
        observed = (
            success
            and choice(
                ask, "Did you physically verify this component? yes/no: ", {"yes", "no"}
            )
            == "yes"
        )
        progress["steps"][step] = {
            **current,
            "result": "software_validated" if success else "needs_attention",
            "observation": "operator_checked" if observed else "not_checked",
        }
        if success:
            print(
                "Saved settings validated. Physical result: "
                + progress["steps"][step]["observation"]
            )
            ask("Press ENTER to continue: ")
            return True
        print("Setup needs attention. Review the tool output; retry or save and exit.")


def wizard(root, state_path, args, ask=input, execute=run_child):
    print(
        "\n========================================\n          NINJAROBOT PI0\n========================================"
    )
    print("Welcome! Hardware > saved settings > Google Gemini > ngrok > summary")
    print(
        "Required hardware comes first. Tools can activate devices. Q saves and exits."
    )
    with progress_lock(state_path):
        progress = load_progress(state_path)
        reconcile(progress, root)
        try:
            reused = set()
            if not args.step and not getattr(args, "resume", False):
                saved = {step: config_status(root, step) for step in TOOLS}
                if any(item["valid"] for item in saved.values()):
                    selected = choice(
                        ask,
                        "1) Open setup tools step by step\n2) Apply existing settings for all modules\nQ) Save and exit\nChoose: ",
                        {"1", "2", "q"},
                    )
                    if selected == "q":
                        return 0
                    if selected == "2":
                        for step, status in saved.items():
                            if status["valid"]:
                                reuse(progress, step, status)
                                reused.add(step)
                                print(f"{step}: saved settings checked (software only)")
                            else:
                                print(f"{step}: setup still needed")
                        ask("Press ENTER to continue: ")
            for step in [args.step] if args.step else STEPS:
                prior = progress["steps"].get(step, {})
                if step in reused:
                    continue
                print(
                    f"\nStep {STEPS.index(step) + 1} of {len(STEPS)} — {step.title()} "
                    + ("[Hardware]" if step in TOOLS else "[Settings]")
                )
                if step in TOOLS:
                    if (
                        getattr(args, "resume", False)
                        and prior.get("result") == "software_validated"
                        and prior.get("valid")
                    ):
                        print(
                            "Saved verification still present; use --step to re-open this tool."
                        )
                        continue
                    if not hardware_step(root, step, progress, ask, execute):
                        break
                else:
                    if step == "gemini":
                        print(
                            "Google model discovery/validation uses the network. Your key is hidden and stored in config.json."
                        )
                    elif step == "ngrok":
                        print(
                            "Optional remote-access token. Setup may download ngrok. No tunnel is opened."
                        )
                    elif step == "import":
                        print(
                            "Copy validated display, buzzer and servo settings into the existing robot configuration."
                        )
                    else:
                        print(
                            "Set the BLE name and select tire, humanoid or spider to match your robot."
                        )
                    if prior.get("result") == "configured_unverified":
                        print(
                            "Previously configured; account validity is not rechecked automatically."
                        )
                    while True:
                        selected = choice(
                            ask,
                            "1) Configure this step\nENTER) Skip / keep existing\nQ) Save and exit\nChoose: ",
                            {"1", "", "q"},
                        )
                        if selected == "q":
                            return 0
                        if selected == "":
                            break
                        if step == "import" and not all(
                            config_status(root, key)["valid"]
                            for key in ("display", "buzzer", "servo")
                        ):
                            print(
                                "Import blocked: validate display, buzzer and servo first. Factory defaults do not count."
                            )
                            break
                        try:
                            code = execute(
                                [
                                    sys.executable,
                                    "-B",
                                    str(Path(__file__).resolve()),
                                    "--worker",
                                    step,
                                ],
                                root,
                            )
                        except OSError:
                            code = 1
                        progress["steps"][step] = {
                            "result": "configured_unverified"
                            if code == 0
                            else "needs_attention"
                        }
                        atomic_private(state_path, progress)
                        if code == 0:
                            print("Settings saved. Verify operation separately.")
                            ask("Press ENTER to continue: ")
                            break
                        print(
                            "Step failed or cancelled. Retry, skip, or save and exit."
                        )
                atomic_private(state_path, progress)
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled. Progress retained; hardware cleanup must be confirmed.")
        finally:
            reconcile(progress, root)
            atomic_private(state_path, progress)
            summary(progress)
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Reopen saved progress and revalidate settings",
    )
    parser.add_argument("--step", choices=STEPS)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--status", action="store_true")
    mode.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--worker",
        choices=("identity", "gemini", "ngrok", "import"),
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args()
    state = (
        Path(os.environ.get("XDG_STATE_HOME", str(Path.home() / ".local/state")))
        / "ninjarobot_pi0/onboarding.json"
    )
    if args.dry_run:
        print(
            "Preview: "
            + " > ".join(STEPS)
            + ". No tools, accounts, files or hardware accessed."
        )
        return 0
    if args.status:
        progress = load_progress(state)
        reconcile(progress, ROOT)
        print(
            json.dumps(
                {
                    "progress": progress,
                    "hardware_settings": {
                        step: config_status(ROOT, step) for step in TOOLS
                    },
                },
                indent=2,
            )
        )
        return 0
    if not sys.stdin.isatty():
        raise ValueError("Use an interactive terminal for onboarding.")
    from install_check import platform_errors

    if platform_errors():
        raise ValueError("Onboarding requires Bookworm/Trixie 64-bit on Zero 2 W.")
    if args.worker:
        return worker(args.worker)
    return wizard(ROOT, state, args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError):
        print(
            "Setup unavailable: check platform, terminal, private files and prerequisite services.",
            file=sys.stderr,
        )
        raise SystemExit(1) from None
