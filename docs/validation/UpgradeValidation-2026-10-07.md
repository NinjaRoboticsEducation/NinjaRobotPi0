# Pi0 upgrade validation and real-device handoff

## 1. Scope of validation

Installer/default-branch bootstrap, guided onboarding, embedded wiki/manual workflow, and
Pi5-derived Pi0 web presentation. Robot algorithms, drivers, Python identity, GPIO mappings
and transport contracts remain unchanged. `core_baseline.json` records 120 protected source,
test, metadata and lock inputs against Pi0 commit `3dbc41a4ee3cf9fb1019e3be5e633f5a6b47d862`.
Pi5 reference commit: `d620fa4e790fd79c1b5d65bc2b95eb71625076cd`; Pi5 remains read-only.

## 2. Environment and prerequisites

Executed on macOS with isolated locked Python 3.11.15 and 3.13.14 environments, Node 24.18.0,
existing frontend lock (Vite 7.3.0), ShellCheck 0.11.0 via shellcheck-py 0.11.0.1, and Chromium
via Playwright 1.62.1. Installer pins are uv 0.11.29, Node 22.23.3 Linux arm64 and pigpio v79
commit c33738a320a3e28824af7807edafda440952c05d. Host build is not ARM resource qualification. Installation clears unrelated developer environment
overrides and explicitly includes frontend build dependencies even with NODE_ENV=production.
CI uses Python 3.11 and pinned Node 22.23.3; its remote run remains pending publication.

Manual acceptance target: Raspberry Pi Zero 2 W, Raspberry Pi OS Bookworm 64-bit, normal user
with deliberate sudo authorization, sufficient disk space/network and unchanged saved configs.
Full source-version manuals are linked by the wiki README and project-knowledge.json.

## 3. Safety notes

Disconnect actuator power for software installation. Installation never activates pigpiod,
calibration, robot server, boot autostart or reboot. Standalone tools and server initialization
can activate devices immediately; servo-tool can center saved servos before its menu.
Support limbs/wheels, clear travel and keep power removal available before typing READY.
Software-valid saved calibration is not physical verification. Stop any existing robot server
before standalone tools. Review wiring against the current manual before activating GPIO.
No real hardware, remote tunnel or account was used in the host checks.

## 4. Safe smoke tests — pending on Pi

From the approved checkout, before connecting actuator power:

```bash
./install.sh --dry-run
./onboard.sh --dry-run
./onboard.sh --status
python3 scripts/verify_core.py
```

Then deliberately run `./install.sh` and `./install.sh --check`. Expect locked dependencies,
verified tool versions, frontend build and private non-secret installation record. Rerun to
check repair/idempotence. Inspect `systemctl is-active pigpiod ninjarobot` before and afterward:
installation must not start or enable robot services. Confirm existing calibration/config
bytes remain intact. Wrong OS, architecture, device or root execution must fail before setup.

## 5. Communication/interface tests — pending on Pi

After wiring/calibration acceptance, deliberately start the existing robot server. This initializes
devices and can move servos. Verify Home/Agent/Help, four languages, portrait/landscape, menu
keyboard focus/Escape, distance in millimetres, activity drawer, expressions, sounds and movements.
Check the existing chat request (`/api/agent/chat`) and dedicated `/ws/distance` / `/ws/events`
channels. The BLE indicator reports advertising only. Test speech permission/recognition using
an appropriate browser; the host test did not record audio. Exercise server disconnect/reconnect,
long messages and a slow connection. Use the shutdown control only when physical shutdown is
intended; confirm first that cancel issues no request.

## 6. Sensor/display checks — pending on Pi

Deliberately enable I2C/SPI as required by OS setup, with a separate reboot if needed. Start
pigpiod manually when ready. Run `./onboard.sh --step display`, `--step buzzer`, and
`--step distance` separately. Tools can activate output. Check display pin/rotation/brightness,
buzzer pin and silence after exit, and sensor readings against a measured flat target.
Sensor offset remains in its existing package-local JSON; import-all does not relocate it.

## 7. Actuator-moving or power-risk tests — pending on Pi

Run `./onboard.sh --step servo` only after support/power precautions above. The wrapper uses
existing `pi0servo servo-tool --config servo.json`. Verify each saved ordered pulse limit and
movement mechanically; opening the tool may already center servos. Save/exit, then check
`--status`. Missing/invalid/equal default pulses must block reuse/import. Resume should retain
software state and distinguish operator-checked observations from unverified components.
Cancel normally and confirm existing tool cleanup; remove actuator power if cleanup is uncertain.
Hardware tool recovery must never be inferred from exit status alone.

## 8. Expected outcomes

- Software setup is repeatable and fails clearly on unsupported targets or checksum failures.
- Onboarding uses existing tools/helpers, can defer optional settings and retains private progress.
- Gemini/ngrok failures/cancellations preserve prior settings; test using your own accounts without
  recording keys/tokens. Gemini discovery/model probe uses network; ngrok may download its binary,
  but onboarding opens no tunnel. Core import requires valid saved display/buzzer/servo settings.
- Wiki queries/checks do not sync/install or refresh fingerprints. Fresh explicit prepare reconstructs
  ignored text evidence. Full immutable manuals and short root pointers agree.
- Web styling is consistent with Pi5 while existing Pi0 controls and routes remain compatible.

## 9. Execution status and evidence

Final interruption-recovery checks completed on 2026-10-08: the interrupted full Python run
finished with 148 passing tests; the final repository bundle passed all 64 browser assertions.
All 323 pre-existing tracked robot-package files remain byte-identical. Nested wiki commands
now use the explicit launcher as well as the robot-level adapters. No hardware was used.

| Executed host check | Result |
| --- | --- |
| Python 3.11 full root suite | 148 passed |
| Earlier Python 3.13 root suite before final added cases | 136 passed; 8 existing dbus-next deprecation warnings |
| Focused installer/onboarding/knowledge tests | 44 passed |
| Standalone servo / display / buzzer / sensor suites | 82 / 57 / 65 / 61 passed (265 total) |
| Independent wiki suite | 61 passed |
| Ruff new scripts/tests, format | Passed |
| Bash syntax / ShellCheck | Passed |
| Frontend lint / locked build | Passed, no lint errors or warnings |
| Inert Chromium browser fixtures | 64 assertions passed at 360/390/844/1280 widths |
| Protected core baseline | 120 inputs unchanged; all pre-existing tracked robot package files byte-identical |
| Wiki strict lint / links / indexes / knowledge map | Passed: zero errors, warnings or suggestions; 26/26 semantic reviews, draft/unverified |
| Fresh-copy wiki setup / prepare / query | Passed on Python 3.11; 21 text sources reconstructed, 459 copied inputs unchanged |
| Fresh-copy drift and writer-lock failure fixtures | Passed; no source or catalog fingerprint rewritten |
| Original raw / unchanged owner-reviewed pages | 18 original raw files and 13 unchanged curated pages preserved |

Installer tests use a real private Git remote with default branch `release/default`, annotated
tag/full SHA/ambiguous ref cases, streamed invocation from unrelated CWD, existing destinations,
cleanup, two inert successful reruns and checksum failure. Onboarding tests cover readiness,
invalid calibration, no default config creation, locks, private state, import gate and ngrok
rollback/cancel with dummy inputs. Knowledge tests detect changed/new code, bad pointers,
missing sources/anchors and wrong adapters without modifying their fixture.
Browser requests, sockets, speech and power confirmation are mocked; no robot backend runs.
The rebuilt tracked dist comes from the existing lock, not hand-edited bundles.

## 10. Pass/fail checklist

- [x] Authorized host implementation, lint, root/driver/wiki regression tests and browser fixtures.
- [x] Protected robot source and existing dependency metadata/lockfiles preserved.
- [ ] Owner real Bookworm arm64 installation/rerun, services inactive, memory/disk/build duration.
- [ ] Owner existing/new calibration, cancel/resume/import, cleanup and mechanical limits.
- [ ] Owner live Gemini/ngrok setup, failure recovery and privacy; no tunnel unless deliberate.
- [ ] Owner browser reconnect, microphone, physical output and deliberate shutdown.
- [ ] Published raw HEAD endpoint and pinned-public-commit installation acceptance.
- [ ] Remote CI run after publication.

## 11. Rollback and recovery

Preserve user configs/calibration and custom system units before system work. Installer does not
reset/check out an existing repository or remove user data. Read the failed stage and retry locally
instead of recloning over the installation. Existing Node/pigpiod version or admin service policy
conflicts stop for review. No OS-wide uninstall or automatic system rollback is provided.

Normal apt failure/termination removes only the temporary owned `/usr/sbin/policy-rc.d` inode.
Power loss/SIGKILL can leave it: confirm no installer/apt process is active, inspect its exact
`#!/bin/sh` / `exit 101` content and ownership, then remove only the installer-created file.
Never remove an administrator's existing policy. Similarly inspect stale installer/onboarding/wiki
locks and confirm no writer before removing one. Onboarding config rollback is private/in-memory;
it cannot survive a machine power loss while an existing helper writes, so keep backups.
Use wiki recoverable transaction backups and Git diff; never overwrite later user edits or
force-refresh evidence hashes. Revert presentation/tooling changes from a known reviewed revision
while keeping private user configs. Core source should still match the protected baseline.
