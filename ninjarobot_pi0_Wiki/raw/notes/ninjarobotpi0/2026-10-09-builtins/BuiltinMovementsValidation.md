# Built-in movement validation — 2026-10-09

## 1. Scope of validation

Configuration import/type reconciliation, installed Spider resource, native controller, movement-tool, web movement endpoints/dropdown and Ninja agent text/audio plans. Drivers, wiring and oscillator scheduling were not changed. Wheel/Humanoid have only the owner-confirmed all-servo `home`; Spider has 20 documented entries (566 waypoints including Poweroff).

## 2. Environment and prerequisites

The local environment identifies as Raspberry Pi Zero 2 W Rev 1.0, aarch64. Automated software checks ran here using the existing repository `.venv` (Python 3.13.5), inert/mocked hardware and existing frontend dependencies without installation. Physical Pi acceptance requires the owner-confirmed Spider mapping, valid `servo.json`, known pulse/angle limits and an external servo supply with common ground. HAL obtains channel identities from config calibration keys but physical calibration from `servo.json`; inspect both. Generated fallback calibration is not device acceptance.

Evidence: draft/unverified wiki pages `spider-otto-waypoint-library`, `motion-system-and-easing`, `ninja-core`, `pi0servo`, and `installation-and-wiring`. Source IDs include `src-20261009-2026-10-09-spider-otto`, `src-20261009-developmentguide` and `src-20261008-installationguide-3`. Existing semantic reviews are AI source reviews, not human or physical verification. Wiki search environment was unavailable; tracked sources/pages were read directly. Code corrects historical motion timing/API claims.

## 3. Safety notes

No HAL/device initialization or servo operation was performed in this task. Starting the server or movement-tool can initialize hardware. Server shutdown can execute Spider `Poweroff`, whose ±90° targets are owner-supplied but not clearance-tested. Zero-degree home can move every configured servo and does not establish mechanical safety. Support the body/raise wheels, use known calibration and keep an accessible power cutoff. Do not infer continuous-rotation wheel motor semantics from positional-servo center commands.

## 4. Safe smoke tests

With robot applications stopped, back up private config/calibration outside version control. These commands change configuration only:

```bash
.venv/bin/ninja_core config set-type spider
.venv/bin/ninja_core config import
.venv/bin/python -B -c 'from ninja_core.config import load_config; from ninja_core.builtin_movements import available_movements; c=load_config(); print(c.robot_type, available_movements(c))'
```

Expected: 20 Spider names with all GPIO20–27 configured; reimport preserves edits/custom names. Repeat on separate backed-up configurations with `wheel` and `humanoid`: stored type is `tire`/`humanoid`, and `home` centers exactly the configured pins. Test missing pins and stale wrong-type definitions using inert host tests, not hardware. Never print the full config because it can contain credentials.

## 5. Communication/interface tests

After explicit owner readiness, start the normal runtime; this can energize hardware. Confirm movement-tool option 4, web Agent dropdown and agent capabilities agree for the selected build. The web list is `GET /api/servos/movements`; execute is `POST /api/servos/movements/{name}/execute`. Inert host checks cover 422 rejection before runtime reclamation and 404 missing-name handling. Confirm the page reports an error, not success, when a request is rejected. Restart deliberately after config changes. Test AI rejection with mocked model output before any live account/device test.

## 6. Sensor/display checks

Drivers were not changed. Check face/sound/sensor regression only after normal hardware readiness. Obstacle callbacks now run at waypoint boundaries; the blocking driver does not receive the callback, so immediate interruption inside a single waypoint is not guaranteed. Existing external driver abort and runtime ownership need their own physical acceptance.

## 7. Actuator-moving or power-risk tests

All pending owner validation. First verify one joint at a time at limited travel and confirm the documented GPIO mapping/direction. Then test Wheel/Humanoid `home` or Spider `spider_home` once with the body supported. Only after clearance and power checks test a finite gait cycle. Extreme `Poweroff`, hello, jump and scared require separate explicit readiness; source timing/pauses are not preserved. Do not start with infinite loops or assume a named jump actually jumps safely.

## 8. Expected outcomes

Correct joints respond with calibrated limits, no stall/collision or Pi power reset; type-incompatible movement produces no sequence writes. Import itself produces no hardware activity. Unknown/malformed/partial-channel sequences are rejected before the first step. Driver abort stops later steps without an unsolicited controller centering command. Existing CLI and agent post-task centering remain separate behavior.

## 9. Execution status and evidence

Final software result: **42 feature tests passed** (exit 0), including CLI/web success and rejection, text/audio agent rejection, type switching, reimport, late-step preflight and edited-speed legacy Poweroff. An earlier combined run reported 101 passed, and the original targeted config/Spider/agent run passed 60 tests. These automated checks ran on the Pi with inert drivers. Generator reproducibility, focused Ruff, git diff whitespace checks, frontend lint/build, standalone wheel resource inclusion and loading from the wheel archive passed. No physical motion, hardware acceptance test, dynamics simulation, dependency installation or live AI call occurred.

The earlier full regression run reached 100% with four failures: three installer-bootstrap environment failures due to the existing active pigpiod daemon, and the intentional unchanged-core baseline failure. Full-suite/combined-run Python teardown remained heavily paging after test reporting; those two identified test processes were terminated (exit 143) after their results were captured. The final 42-case feature run exited normally. No daemon/robot process was stopped. The detailed raw evidence records this distinction.

`scripts/verify_core.py` detects six intentional protected changes: core package metadata, config, movement CLI/controller, agent and web server. Baseline fingerprints were not refreshed. Wiki ingestion/review and source mapping updates are deferred at the owner's request; wiki completion is not claimed.

## 10. Pass/fail checklist

- Local configuration/idempotency/legacy/type rejection: PASS, final 42-case feature suite exit 0.
- Full trajectory parity and shuffled GPIO mapping: PASS in inert tests.
- Frontend lint/build and standalone wheel resource smoke: PASS. Full regression run: four failures, followed by terminated teardown; not a clean full-suite pass.
- Protected unchanged-core gate: FAIL by design for six authorized feature changes; review pending.
- Wiki ingestion/strict semantic review/index gates: NOT RUN, deferred to owner.
- Physical mapping, direction, clearance, balance, power, timing and stopping: NOT RUN.

## 11. Rollback steps

Support the robot and disconnect actuator power before stopping an active runtime; shutdown may execute Poweroff. Restore the backed-up private `config.json` and `servo.json` deliberately, then restart only after readiness. To remove imported data manually, remove the named built-ins and their matching metadata; reimport will seed them again. Revert the reviewed feature code as a coordinated change if reverting runtime behavior. Registered old wiki raw originals remain available; new candidate versions have not been ingested.
