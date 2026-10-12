# Fresh-install validation — 2026-10-12

## 1. Scope of validation

Fresh Zero 2 W 64-bit Lite installation, dependency preparation, read-only acceptance, diagnostics, README flow and recovery. Changes: bootstrap stdin isolation; early stage/owned-lock cleanup; python3-pip prerequisite; clear administrator-policy refusal; Python/frontend preparation before Ollama; service/activation checks; aggregate checker failures. Runtime/driver code, pins, credentials and live configuration are unchanged.

## 2. Environment and prerequisites

Executed on the macOS development host, using existing cached CPython3.13/pytest dependencies and inert fixtures. No packages were installed. Official Raspberry Pi downloads checked 2026-10-12 list Trixie (Debian13) Lite64, 2026-10-06 image, kernel6.18 and Zero 2 W compatibility; Bookworm remains Legacy. This does not certify pigpio/device behavior on that kernel.

Read-only upstream checks confirmed the pinned uv install script SHA256, the pinned pigpio Makefile's daemon/shared-library build dependency, and absence of pigpio/pigpiod in the official current Trixie ARM64 package index. Source links are recorded in the raw implementation evidence.

## 3. Safety notes

Host tests use temporary directories, inert downloaded programs, mocked sudo/apt/compiler/systemd and real checksum/archive operations. No actual privileged writes, service activation, GPIO, network inference, or robot startup occurred. Keep actuator power disconnected for software setup. A passing software check is not hardware acceptance.

## 4. Safe smoke tests

Owner-manual on a fresh Pi, pending:

1. Use the README OS update/prerequisite steps, reconnect after reboot.
2. Download and preview the installer; run as normal user and retain the complete first failure if any.
3. Wait for `Software installed`. Enter the checkout with `cd "$HOME/NinjaRobotPi0"`.
4. Run `./install.sh --check` separately. Expect exit0, no FAIL, available uv/Node/npm/pigpiod, launchers, activation, frontend and loaded service. An inactive daemon is expected.
5. `source .venv/bin/activate` should set the ninjarobotpi0 prompt. Use `python3 -B scripts/install_check.py --find-tool uv` to locate reused/private uv.
6. Repeat installation before hardware activation. Expect configuration preservation and tool reuse.

## 5. Communication/interface tests

No live cloud, BLE, web server, SSH, or remote Pi sessions were exercised. Installer download and dependency behavior uses offline fixtures. Actual apt repositories, network availability, frontend ARM64 build and Python wheels on the target remain manual acceptance items.

## 6. Sensor/display checks

Not performed or changed. Continue existing onboarding and component calibration only after software acceptance and physical readiness.

## 7. Actuator-moving or power-risk tests

Not performed. Starting pigpiod can initialize GPIO; start it manually only with the robot supported and actuator power disconnected, then check `systemctl is-active pigpiod`. Opening standalone tools or starting ninja_core can energize components; follow existing readiness steps.

## 8. Expected outcomes

Installer provisions all declared dependencies or exits nonzero with stage/retry guidance. A cloned checkout never implies completion. Missing/masked/error units fail acceptance; no start/enable happens automatically. Existing admin policy and another run's lock are preserved. Missing activation/launchers direct users to complete installation; --check never repairs. Private uv remains discoverable across shells without modifying shell profiles.

## 9. Execution status and evidence

- 124 targeted tests passed: fresh-install, streamed-bootstrap, upgrade/onboarding, CLI entry-point and Ollama suites. No deselections. Real versioned archives in the fresh fixture verify hash/extraction, simulated daemon/library publication, service creation, environment/launchers, frontend, reruns and calibration preservation. Early preflight/apt errors and foreign locks are covered. New cases verify recovery after one inner uv download failure and termination after exactly three failed attempts, with no false success or downstream environment creation.
- Shell syntax (`bash -n`), local `./install.sh --dry-run`, protected-core verification and `git diff --check` passed.
- Ruff0.16.1 syntax/Pyflakes checks (`--isolated --select E4,E7,E9,F`) passed on affected Python and installer suites. Format checks passed on install_check, install_system, fresh-install and upgrade tests. Broader Ruff0.16 defaults report existing style suggestions in older tests/helper code; no unrelated bulk cleanup was performed. ShellCheck was not available locally.
- Cached test runner required UV_CACHE_DIR in writable temporary storage; initial host sandbox cache failure was corrected without changing dependencies. Initial new-fixture path/copy errors were corrected before the final passing run.
- Read-only wiki strict lint: 0 errors, 0 warnings, 5 new unregistered-source suggestions. Link and index checks passed; existing 28 draft/unverified pages retain their prior semantic-review records. No new review was performed.
- Post-change knowledge check reports eight changed implementation fingerprints and one new test needing classification, as expected while publication is deferred; no fingerprints were refreshed.
- README headings/section order and local links checked; complete new raw English manuals/log/evidence prepared. Ingestion/review, current pointers and implementation-map publication remain owner-deferred as previously requested.

Reproduction using an already provisioned project environment:

```bash
.venv/bin/python -B -m pytest tests/test_fresh_install.py tests/test_installer_bootstrap.py tests/test_upgrade_workflows.py tests/test_cli_entrypoints.py tests/test_ollama_install.py -q
bash -n install.sh scripts/install-rpi.sh
./install.sh --dry-run
python3 -B scripts/verify_core.py
```

## 10. Pass/fail checklist

- PASS: host offline fresh/repeated install, failure cleanup/diagnostics, missing service/activation, checksum rejection, existing compatibility and preservation tests.
- PASS: syntax, focused Python lint/format, dry-run, protected runtime boundary.
- PENDING: real fresh Trixie/Bookworm64 Pi installation and service/manual device acceptance.
- DEFERRED: canonical wiki publication/ingestion/review and remote Git publication.
- CONFIRMED from the owner's original log: uv binary download failed with a TLS unexpected EOF at releases.astral.sh, then github.com DNS resolution failed. This caused the downstream missing environment/tools. Bounded retries improve transient recovery; persistent Pi connectivity/DNS failure still needs owner repair.

## 11. Rollback steps

Retain config/calibration and the checkout. Restore only source files from this change if rolling back development. On the Pi, correct the first installation error and rerun the same checkout; do not delete .venv or config as a first response. Do not remove locks or administrator policies without confirming their ownership and purpose. The installer does not update Git; bring the published corrected revision into an existing checkout deliberately before retrying.
