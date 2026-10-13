# BLE readiness and onboarding implementation plan

Date: 2026-10-13 (Asia/Tokyo). Owner requested both a robust plan and implementation. Scope is exclusively Bluetooth service availability and BLE setup. Prior instruction to leave wiki ingestion and semantic review to the owner remains in force.

## Evidence and problem

The current identity worker in `scripts/onboard.py` saves name/type only. `scripts/install_system.py` installs BlueZ but deliberately suppresses service activation while installing packages. `ninja_ble/service.py` tries three advertisement profiles and a best-effort adapter power cycle; it does not enable system services. The supplied advertisement failure does not identify the Pi's underlying OS/controller condition.

Wiki retrieval on 2026-10-13: `search "Bluetooth BLE onboarding advertising BlueZ"` and `check` succeeded. Current manual versions were resolved through `ninjarobot_pi0_Wiki/project-knowledge.json`. `wiki/entities/ninja-ble.md` and `wiki/concepts/dual-connectivity-and-protocols.md` remain draft/unverified with source-grounded semantic reviews; they document BlueZ, the existing GATT UUIDs and identity setup, but do not establish current physical readiness. Preserve those transport contracts.

Primary sources checked:

- [Raspberry Pi configuration/UART documentation](https://www.raspberrypi.com/documentation/computers/configuration.html#configure-device-tree-overlays-for-uarts): disable-bt and UART assignment affect Bluetooth. Do not edit boot/UART overlays automatically.
- [RPi-Distro hciuart unit](https://github.com/RPi-Distro/pi-bluetooth/blob/master/debian/pi-bluetooth.hciuart.service): legacy UART initialization is conditional, not a universal modern-Pi prerequisite.
- [BlueZ advertising API](https://github.com/bluez/bluez/blob/master/doc/org.bluez.LEAdvertisingManager.rst): advertising support, active/available instances, registration and error categories.
- [BlueZ Adapter API](https://github.com/bluez/bluez/blob/master/doc/org.bluez.Adapter.rst): Powered is writable but not itself persistent across controller restart.
- [BlueZ systemd unit](https://github.com/bluez/bluez/blob/master/src/bluetooth.service.in): service activation and D-Bus ownership.
- [util-linux rfkill manual](https://github.com/util-linux/util-linux/blob/master/sys-utils/rfkill.8.adoc): Bluetooth-only soft unblock cannot remove hardware blocks.

## Phase 1 — Isolated readiness and repair helper

Add a Bluetooth-only helper in `ninja_ble/system_setup.py`, using existing D-Bus dependencies and bounded commands. Read-only mode checks platform, systemd service, rfkill, adapters, Powered, GATT and advertising support without changing settings or registering advertisements. Repair mode is allowed only on the supported Raspberry Pi Zero 2 W/Linux host; enable/start bluetooth.service if necessary, unblock only Bluetooth soft blocks, and power the selected controller. Stop with actionable errors for masked policy, hard block, absent packages/controller, missing peripheral support and occupied advertisements. Legacy hciuart is considered only when no controller exists and its legacy device-tree/serial prerequisites exist. Never restart a healthy service, power-cycle controllers, change Wi-Fi, install policy permissions, enable experimental BlueZ, edit boot files, erase pairings or reboot.

Verify a short minimal connectable advertisement in repair mode, with no GATT commands or robot runtime, and unregister/disconnect in every outcome. A failure retains its D-Bus error name and practical troubleshooting steps. No advertisement is registered in read-only mode. Use a distinct process-owned object path and do not unregister anyone else's advertising.

## Phase 2 — Onboarding integration

Run readiness/repair before the existing identity name/type prompts when the owner selects that step. Keep the step identifier and command `./onboard.sh --step identity` compatible. Failed readiness keeps the step marked needs_attention and leaves robot configuration unchanged. Show that the selected step enables the radio and may require sudo authentication. A skipped step makes no OS changes. Add rfkill to the fixed installer Bluetooth prerequisites without changing installer service-activation policy. Other steps and runtime functions remain unchanged.

## Phase 3 — Validation and documentation

Use inert systemd/rfkill/D-Bus fixtures for supported/unsupported hosts, healthy idempotency, stopped/disabled service, soft/hard blocks, masked policy, missing controller, legacy-vs-kernel initialization, powered-off adapter, occupied advertisements, registration failure, cleanup, timeouts and cancellation. Verify onboarding failure/config preservation and success ordering. Run focused tests, Ruff, existing broader regression suite, dry-run and protected-core checks. Review only the approved Bluetooth/installer fingerprints. Preserve all pre-existing dirty files and unrelated robot functions.

Create new complete English manual/log versions and a validation report under dated wiki raw paths. Add minimal README guidance. Do not ingest, normalize, apply wiki plans, update knowledge mappings, run semantic review or overwrite registered originals.

## Target-Pi acceptance and rollback

Host fixtures do not qualify a real controller. Owner runs the identity step, verifies BLE readiness and its temporary advertisement cleanup, then deliberately starts the existing server and checks client connection/robot_info without movements. The server can activate robot hardware and requires normal operator readiness. Record the original Bluetooth unit enabled/active state, radio block and power state; undo only changes deliberately made by BLE setup if desired. Restoring an originally disabled radio/service will restore the original failure. Code rollback affects only helper/onboarding/Bluetooth prerequisite/docs; no calibration, movement, provider, Wi-Fi or protocol migration occurs.

## Implementation status

All three code/host-validation phases are implemented. Full host regression passed (707 tests, 3 subtests), plus Ruff, shell syntax, dry-run, whitespace and protected-core/boundary checks. English manual/log/readme snapshots and validation evidence are prepared under 2026-10-13-ble-onboarding raw paths. Target-Pi/client/reboot acceptance and owner wiki ingestion/review remain pending. Existing runtime/driver/protocol/provider code and unrelated edits are retained.
