# CLI entry-point repair validation

## 1. Scope of validation

Fix duplicate console-script ownership in root packaging, recreate local provider launchers during installation, and detect all five missing/nonexecutable launchers in read-only setup checks. Robot runtime, drivers, calibration and movement definitions are unchanged.

## 2. Environment and prerequisites

Local Raspberry Pi Zero 2 W/aarch64, Python 3.13.5, uv 0.9.26, existing .venv. Installed root/provider metadata are present; ninja_core, pi0servo, pi0disp, pi0buzzer and pi0vl53l0x launchers are absent. Root and provider RECORD files both claim identical paths. Prior rename transaction logs are unavailable; removal during the rename is the strongest explanation, not a separately logged event. No account/config secrets were printed.

Wiki evidence: installation-guide (draft/unverified, AI review 2026-10-09), registered InstallationGuide src-20261009-installationguide, DevelopmentGuide src-20261009-developmentguide-2 and DevelopmentLog src-20261009-developmentlog-2. CLI retrieval environment was missing, so tracked sources were inspected directly. Existing lifecycle/policy source drift remains owner-deferred.

## 3. Safety notes

No server/device tool is launched by these tests or the repair command. CLI --help and package metadata checks do not initialize HAL. Stop an active robot only in an owner-controlled session with mechanical support/power readiness; shutdown may execute Poweroff. Do not automatically stop pigpiod, run apt, recreate .venv or delete configuration to fix missing launchers.

## 4. Safe smoke tests

```bash
uv lock --offline --check
./install.sh --dry-run
bash -n scripts/install-rpi.sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m pytest -q tests/test_cli_entrypoints.py tests/test_installer_bootstrap.py tests/test_upgrade_workflows.py -k 'not protected_robot_sources_unchanged'
```

Expected: root has no duplicated scripts, each provider retains its command, all launcher checks fail clearly when files are missing and installer fixtures force locked provider reinstallation. The isolated uv venv test creates an unseeded temporary environment only, preserving an inert launcher without installing packages or touching the real environment.

## 5. Communication/interface tests

After the fix is available in the checkout and environment repair is authorized:

```bash
env -u UV_PROJECT_ENVIRONMENT -u UV_PROJECT uv sync --locked --inexact --no-dev \
  --reinstall-package ninja-core --reinstall-package pi0servo \
  --reinstall-package pi0disp --reinstall-package pi0buzzer \
  --reinstall-package pi0vl53l0x
uv run --no-sync ninja_core --help
./install.sh --check
```

This is a real local Python installation/repair, not a diagnostic. It also rebuilds changed root metadata; locked third-party dependency versions stay unchanged. --inexact retains extra/development packages. If uv is private, use the compatible private uv path rather than installing another copy. Run from the project root; wrong directories/environment overrides can select another environment. Normal uv run may synchronize packages; --no-sync explicitly uses the repaired environment.

## 6. Sensor/display checks

Not applicable to launcher repair; no driver change. Actual LCD/QR/sensor acceptance remains separate and pending. No screen or GPIO was activated.

## 7. Actuator-moving or power-risk tests

Server startup is pending owner readiness, not performed here. Once CLI help/setup checks succeed and wiring/calibration/power are ready, the owner may run `.venv/bin/ninja_core server` or `uv run --no-sync ninja_core server`. Startup can energize/center servos, operate display/buzzer and open ngrok; stopping may command Poweroff.

## 8. Expected outcomes

Five existing command names remain available from their packages; root rebuild/uninstall no longer owns/removes those files. Targeted reinstall restores missing launchers even when provider metadata already exists. Environment inspection checks all five paths, never runs a hardware tool and suggests minimal recovery alongside full installation for missing dependencies/interpreter.

## 9. Execution status and evidence

Reproduced ENOENT with `uv run --no-sync -- ninja_core --help` (exit 2). Python module help `.venv/bin/python -B -m ninja_core --help` passed (exit 0), proving code imports without the missing launcher and without starting hardware. 105 focused tests passed, one unchanged-source-baseline test deliberately excluded (exit 0). Full root regression: **331 passed, 1 deselected, 31 existing dbus_next deprecation warnings, exit 0** (88.52 seconds). Focused Ruff, shell syntax, offline lock check and installer dry-run passed. Locked offline repair dry-run plans only six local builds/reinstallations (root plus five providers), no third-party version changes.

Local environment repair and repaired-console help have not been executed without owner approval. No dependency installation in the real environment, server startup, service stop or hardware operation is claimed. Original protected/source fingerprints were not refreshed. Wiki check still reports deferred lifecycle/policy drift plus new repair changes; ingestion, normalization and semantic reviews are intentionally not run.

Read-only installer inspection correctly reports the five missing launchers. An initial npm version probe exceeded its 20-second timeout on this constrained Pi; a direct retry succeeded (npm 11.19.0, Node v24.21.0). This independent transient probe failure is not the cause of Python ENOENT, and no Node/npm replacement was performed. The environment check cannot pass until the missing launchers are repaired.

## 10. Pass/fail checklist

- Failure reproduction and direct module help: PASS.
- Single-provider ownership, RECORD collision simulation and missing/nonexecutable launcher checks: PASS.
- Installer targeted-reinstall fixtures, uv flag compatibility and rerun behavior: PASS.
- Ruff/shell/offline lock/preview: PASS.
- Real environment repair and console help: PENDING owner approval/execution.
- Protected unchanged-source baseline: remains FAIL for authorized accumulated metadata/runtime changes; no fingerprints updated.
- Wiki registration/ingestion/review gates: DEFERRED to owner.
- Server/actuator/display/ngrok acceptance: NOT RUN.

## 11. Rollback steps

Preserve private configuration/calibration and unrelated local changes. Avoid reverting root metadata to duplicate launcher ownership. If a repair fails, retain its first error and retry only after resolving it; do not delete .venv first. An interrupted packaging transaction can require reinstalling the same local providers again. Revert packaging/installer/diagnostic changes together only after review. Original raw sources/current pointers remain unchanged; new English candidates have no invented source IDs/reviews.

