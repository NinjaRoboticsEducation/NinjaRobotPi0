# Trixie installation correction — 2026-10-08

## Scope and root cause

The reported Pi is a Zero 2 W running Debian 13 (Trixie) 64-bit. `install.sh` explicitly
required `VERSION_CODENAME=bookworm`; `scripts/install_check.py` repeated that restriction
for local install, software checks and onboarding. Architecture (`aarch64`) and release
codename are independent checks. The error occurs before cloning, apt, or hardware activity.
It followed the original Bookworm-only requirement; the owner's new request extends the
installer target to Bookworm **or Trixie** on the same hardware and architecture.

Changes: release allowlists/help in bootstrap, local installer and onboarding; actionable
Python preflight diagnostics; release/rejection regressions; Python 3.11/3.13 CI matrix;
current README and immutable manual/wiki versions. Robot packages, GPIO behavior, lockfiles,
tool pins and system Python remain unchanged. No bypass flag or `/etc/os-release` edit is used.

## Environment and dependency evidence

Raspberry Pi's [Trixie announcement](https://www.raspberrypi.com/news/trixie-the-new-version-of-raspberry-pi-os/)
confirms the Raspberry Pi OS release. Debian's [release notes](https://www.debian.org/releases/trixie/release-notes/whats-new.en.html)
list the change from Python 3.11 to 3.13. The existing installer selects `/usr/bin/python3`
and `python3-dev`/`python3-venv`, so Trixie uses its own 3.13 interpreter. Existing locked host
environments exercise both Python versions without changing the robot dependency lock.
This is not a full Debian arm64 OS/package-transaction or physical-device certification.

Wiki evidence: current overview, installation-guide, installation-and-wiring, guided-onboarding,
and development-workflow pages; all are draft/unverified. Their old Bookworm-only statements
are superseded by this user-authorized target expansion; historical raw sources stay immutable.

## Safety and smoke checks on the Pi (pending)

Keep actuator power disconnected during installation. After publishing this fix to the official
default branch, rerun the original curl command. HEAD follows the repository default branch.
If a checkout already exists, update it to the fixed revision and use its local installer;
the bootstrap refuses to overwrite an existing destination. Never delete calibration to retry.

```bash
uname -m                 # aarch64
cat /etc/os-release      # VERSION_CODENAME=trixie (or bookworm)
# After downloading/updating the fixed checkout:
cd "$HOME/NinjaRobotPi0"
./install.sh --dry-run
./install.sh
./install.sh --check
./onboard.sh --dry-run
./onboard.sh --status
```

Expected: Trixie passes the release gate, software installs/checks complete, and read-only
onboarding modes create no default robot settings and activate no hardware.

## Communication, sensor/display and actuator acceptance (pending)

Use the README first-test checklist after software installation. Start pigpiod deliberately,
verify I2C/SPI and use `./onboard.sh` with the robot supported. Display/buzzer/sensor tools
activate their devices. Servo-tool can center servos before its menu; server start can also
move hardware and attempts ngrok. Verify each component, import saved calibration, then test
web/BLE/Google/ngrok with your own accounts. These live checks were not executed on this host.

## Execution status and rollback

Host release tests cover quoted/unquoted Bookworm/Trixie, the reported Debian identity, and
rejection of unknown/old releases, 32-bit architecture, other Pi hardware, root and other OS IDs.
The existing private Git/bootstrap fixtures remain in use. Final host results are appended below.
Python 3.13 emits existing dbus-next deprecation warnings about removal in Python 3.15; it passes
current tests. Future Python releases are not qualified by this change.

There is no OS migration or dependency upgrade to undo. Reverting this patch reinstates the
Bookworm-only gate. Preserve robot settings and stop after any failed install stage; repair and
retry locally. Actual apt/pigpio/arm64 dependency installation, physical tests and remote CI remain
pending. The fix is local until committed/pushed; no remote publication was performed by this task.

## Final host results

- Python 3.11: **184 root tests passed**.
- Python 3.13: **184 root tests passed**, with eight existing dbus-next deprecation warnings.
- Python 3.13 driver suites: **265 passed** (servo 82, display 57, buzzer 65, sensor 61).
- Ruff lint/format, ShellCheck and diff whitespace checks passed.
- Protected core/metadata gate passed; robot package sources and lockfiles unchanged.
- Current manual/code mappings, strict wiki lint, links and indexes passed. Seven relevant pages
  have new source-grounded review records; lifecycle remains draft/unverified.
- No Pi hardware, OS package transaction, live account, GitHub CI run or publication was performed.

On-device next step: publish this correction, rerun the original curl command on the reported
Trixie system, then follow the non-moving software checks before any onboarding hardware action.
