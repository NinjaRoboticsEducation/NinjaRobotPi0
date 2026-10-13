# BLE onboarding validation and implementation evidence

Date: 2026-10-13 (Asia/Tokyo). Bluetooth-only scope, implemented at the owner's request. Wiki ingestion and semantic review remain owner-controlled; the new complete English manuals/log and evidence are unregistered sources.

## 1. Scope of validation

OS Bluetooth readiness, conditional enable/start, Bluetooth soft unblock, controller power, peripheral manager support, temporary advertisement registration/cleanup and onboarding success/failure. The robot runtime, drivers, movement library, calibration, AI providers, web UI and GATT/chunking contracts are unchanged. An existing movement-catalog test now stubs the new BLE prerequisite on the macOS host; its catalog assertions remain intact.

## 2. Environment and prerequisites

macOS host, Python 3.11.15. The previous temporary test environments had missing package files. Created `/private/tmp/pi0-ble-tests` with a separate cache and installed hash-verified requirements exported from the existing uv lockfile, excluding local packages; source paths were provided to pytest. No project environment, lockfile or Pi installation was changed. New installer versions include rfkill with existing BlueZ/DBus requirements. The setup helper never installs packages.

## 3. Safety notes

All OS commands, sudo calls, adapter operations and advertisements in tests use inert fixtures. No host Bluetooth operation, real system service change, advertisement, robot server, live network provider or actuator was started. Repair on Pi deliberately enables Bluetooth and briefly advertises a connectable device without a GATT robot command surface. The existing server later activates hardware and may move servos; it requires normal readiness and support.

## 4. Safe smoke tests and evidence

Before implementation, wiki search and knowledge check passed. Current manuals were resolved from project-knowledge.json. Relevant canonical pages: `wiki/entities/ninja-ble.md`, `wiki/concepts/dual-connectivity-and-protocols.md`, `wiki/references/api-and-cli-reference.md` and `wiki/references/hardware-calibration-and-tools.md`. They remain draft/unverified with source-grounded semantic reviews, not physical acceptance. The BLE entity review is dated 2026-10-07 and supports the existing transport; it does not verify this new setup workflow.

Code evidence: `scripts/install_system.py` deliberately inhibits Debian service activation during package install; prior `scripts/onboard.py::_worker(identity)` only saved name/type; `ninja_ble/service.py` retries advertisement profiles/power recovery but does not enable BlueZ services. Therefore a setup-readiness gap is confirmed, while the reported advertisement failure's exact Pi cause remains unverified. A running system service alone does not prove advertising works.

Primary official/current sources retrieved on this date are linked in [the phased implementation plan](../../../../../DevelopmentPlanDoc/BLEOnboardingImplementation.md): Raspberry Pi configuration/UART documentation, RPi-Distro's conditional legacy hciuart unit, BlueZ advertising/adapter/systemd APIs and the util-linux rfkill manual. SupportedInstances describes available instances; the implementation avoids comparing it against ActiveInstances as though it were a total slot count. An existing active advertisement makes onboarding fail with instructions to stop the owning application, without unregistering it.

## 5. Communication/interface tests

Read-only mode checks service/radio/controller support and never repairs, powers on or advertises. Repair mode enables/starts only missing unit states, unblocks Bluetooth only, powers the selected controller and verifies it, then probes an owned advertisement path. Registration timeout/failure/cancellation attempts cleanup of only that path, unexports the object and disconnects the private bus connection. A successful registration whose explicit cleanup fails is not reported as ready. D-Bus error names are preserved. Sudo uses its own terminal password prompt and bounded authentication/commands; passwords are never captured by the application.

Failures cover missing/masked/stopped services, hard/soft blocks, missing rfkill, unavailable controllers, missing GATT/advertising managers, busy/zero advertising instances, permission denial, power failure, timeout and cancellation. No healthy daemon restart, adapter power cycle, boot edit, pairing erase, Wi-Fi change or experimental/policy permission change is attempted. Legacy UART initialization requires absent kernel controller plus existing serial1/device-tree UART prerequisites; modern controller paths skip it.

## 6. Sensor/display checks

Not applicable to this feature. Existing protected runtime/driver sources remain unchanged. Full inert regression includes their existing behavior; no physical sensor/display test is claimed.

## 7. Actuator-moving or power-risk checks

The Bluetooth-only check/repair module does not instantiate HAL or touch actuators. Owner may run `.venv/bin/python -m ninja_ble.system_setup --check` safely without launching the robot. Testing `ninja_core server` afterward can initialize/center servos and execute Poweroff at exit; only do this with supported wiring/calibration, a stable supply and clear travel area. Prefer a client `robot_info` exchange without movement commands for BLE acceptance.

## 8. Expected outcomes and pending Pi acceptance

With the server stopped, run `./onboard.sh --step identity`, choose Configure, authorize sudo if asked, and press ENTER to preserve existing name/type. A ready system prints service/controller/advertisement success and removes the test advertisement. Repeat setup to check idempotency. Reboot during an owner-controlled maintenance session and rerun the read-only check; BlueZ's OS policy controls power across reboot, so actual reboot readiness must be verified. Then deliberately start the server and confirm advertising, BLE connection and robot_info from the intended browser/mobile client. Confirm occupied advertisements, denied sudo, soft-blocked radio and failed firmware produce actionable failure rather than a success summary. If administrator policy masks Bluetooth or boot config disables it, have that policy reviewed manually.

## 9. Execution status and actual results

Focused BLE/service/onboarding tests: 130 passed. After adapting the host-only identity fixture, focused BLE/movement-catalog/onboarding tests: 355 passed. Final full `tests/` regression: 707 passed and 3 subtests passed on Python 3.11.15 (55.67 seconds). Ruff checks for BLE/scripts/tests passed. Shell syntax and `./onboard.sh --dry-run` passed. Protected-core verification passed without changing existing baseline fingerprints. No production package installation or physical Pi test occurred.

## 10. Pass/fail checklist

- [x] Bluetooth-only helper and onboarding integration implemented.
- [x] Focused inert success/failure/cleanup tests, full regression (707 tests, 3 subtests) and Ruff passed.
- [x] Installer service-activation policy and other robot functions retained.
- [ ] Owner accepted actual Pi service/radio/advertisement and reboot behavior.
- [ ] Owner accepted an end-to-end BLE client robot_info exchange.
- [ ] Owner ingested/reviewed the new English evidence and classified new implementation files.

## 11. Rollback

The helper prints enable/start/unblock/power actions when it performs them. Record original Bluetooth service enabled/active state and radio power/block state before target-device validation. If rollback is needed, restore only those Bluetooth states deliberately changed; reverting to a disabled service/radio also restores the original availability failure. No boot, Wi-Fi, pairing, calibration or provider rollback is needed. Code rollback affects the helper, its onboarding invocation and rfkill prerequisite. Preserve existing administrator masks and unrelated repository changes.

Read-only completion checks: pre-existing modified files were byte-for-byte preserved except the scoped README addition. Runtime/driver/UI/lockfile diffs remained empty. Wiki normal lint reported only suggestions, with no errors/warnings; source status reported 139 ingested and 15 pending sources. New BLE sources are intentionally unregistered, and changed/new implementation mappings remain pending owner ingestion. No ingestion, normalization, semantic review, canonical-page edit or knowledge-map refresh was run.
