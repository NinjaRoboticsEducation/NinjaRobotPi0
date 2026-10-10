# Lifecycle refinements validation — 2026-10-10

## 1. Scope of validation

Movement-tool deliberate exit, single-browser web ownership, reconnect QR/display ownership, disconnect/timeout cancellation, delayed action guards, and installer/root-project/environment prompt. Drivers, wiring and calibration are unchanged. `center_all_servos` gains an optional lifecycle abort callback; existing callers without it retain their behavior.

## 2. Environment and prerequisites

Automated checks run on the local Raspberry Pi Zero 2 W/aarch64 using existing Python 3.13.5 `.venv` and frontend dependencies. Tests use inert HAL/driver/display/socket fixtures; no live server or hardware tool was started. Existing pigpiod and owner changes to tracked bytecode were left alone. No dependencies were installed. The active shell may need `deactivate`, then `source .venv/bin/activate` to display the new prompt.

Wiki evidence: `spider-otto-waypoint-library`, `web-interface-design`, `dual-connectivity-and-protocols`, `installation-guide`, `motion-system-and-easing`, `safe-execution-and-blockly-runtime`; complete current manuals from 2026-10-09-builtins (`src-20261009-installationguide`, `src-20261009-developmentguide-2`, `src-20261009-developmentlog-2`). Source status is draft/unverified with recorded AI semantic reviews, including 2026-10-09 movement review; that is not physical acceptance. Baseline wiki knowledge check passed. CLI search/source-status environment was unavailable, so tracked sources were read directly without setup.

## 3. Safety notes

Starting movement-tool/server can center servos. Deliberate option 6 now commands configured Poweroff; Spider's extreme ±90° targets require explicit clearance readiness. Wheel/Humanoid without Poweroff use configured home. HAL shutdown releases PWM; no holding torque is guaranteed. Support the robot, raise wheels, verify calibration and joint direction, use external servo power/common ground, and keep an accessible power cutoff. Closing the browser requests cooperative abort, not an emergency-rated physical stop. No claim is made about instantaneous interruption of a blocking driver call.

## 4. Safe smoke tests

These checks do not start robot devices:

```bash
uv lock --offline --check
./install.sh --dry-run
bash -n scripts/install-rpi.sh
bash -c 'source .venv/bin/activate; test "$VIRTUAL_ENV_PROMPT" = ninjarobotpi0'
node tests/web_session_hook.cjs
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m pytest -q tests/test_lifecycle_refinements.py tests/test_builtin_movements.py tests/test_runtime_pipeline.py
```

Expected: dependencies remain locked, installation preview names ninjarobotpi0, activation sets the new prompt, and inert exit/session tests pass. `./install.sh` without `--dry-run` is a real installation and was not run.

## 5. Communication/interface tests

Pending owner readiness: start the normal runtime (hardware activation), open the ngrok URL on browser A, then navigate Home → Agent → Help without releasing ownership. Open browser B (separate browser/incognito cookie): it must show busy and must not control any API or distance/events socket. Same-cookie tabs count as one controller; closing one must not restore QR while another remains. Close A's last tab: QR returns and B can connect. Repeat at least five handoffs, including Agent playback/Blockly work. Test browser network loss: after 35 seconds without primary-socket input the controller is released; clients retry every 3 seconds and ping every 10 seconds. Check mobile background/sleep behavior, which can suspend heartbeat timers.

REST routes/payloads are unchanged, but `/api/` now requires the HTML-issued cookie and live `/ws/session`. Inactive requests return 423, shutdown requests 503. Direct diagnostic scripts must follow that session contract. This mechanism is connection ownership, not login/authentication. BLE remains a separate existing protocol; global BLE/web arbitration is not introduced.

## 6. Sensor/display checks

Pending: scan the restored QR from the actual LCD at its native dimensions; confirm it reaches the same running ngrok URL. If ngrok is unavailable, confirm the displayed LAN URL is reachable on the same network. No reachable URL/display means there is no QR to show, but browser ownership must still release. Confirm Blockly completion/late agent responses do not paint idle over the waiting QR. Verify distance/events sockets still function after reconnect. Confirm OS/server shutdown does not repaint QR over the shutdown screen.

## 7. Actuator-moving or power-risk tests

Pending, only after explicit physical readiness: back up private config/calibration, support the robot and launch `.venv/bin/ninja_core movement-tool` (startup moves servos). Choose 6 once. Expected order: permitted Poweroff (or home if absent) → HAL shutdown → configuration save, no subsequent center. Observe power/PWM release separately from actual pose holding. For Spider verify every extreme Poweroff target has clearance before selecting 6. Wheel/Humanoid should center only configured joints. Use inert tests, not wrong-type physical commands, to verify rejection.

During browser playback, close the controller and observe abort latency, no continued sequence or later centering, no collision/stall and QR restoration. Separate servo-only, face-only, sound-only and Blockly interruptions before combined work. Do not assume abort can halt arbitrary uploaded code instantaneously.

## 8. Expected outcomes

Exit pose precedes resource release and survives failure via cleanup/save. Exactly one browser identity controls web APIs; last disconnect releases it after cleanup, while stale callbacks remain invalid even when the same cookie reconnects. Missing/failing display cannot deadlock handoff. QR is square, centered and not stretched; native idle restoration remains suppressed while waiting. Installer reuses `.venv` without `--clear`, sets prompt ninjarobotpi0 and syncs the unchanged dependency versions.

## 9. Execution status and evidence

Executed: 72 movement/session/runtime tests passed (exit 0); 93 installer/upgrade tests passed, one protected-baseline case deliberately deselected (exit 0). Full root regression: **319 passed, 1 deselected, 31 existing dbus_next deprecation warnings, exit 0** (207.44 seconds). Initial installer run had three failures caused by a fixture selecting host Node and bypassing inert systemctl; test isolation was corrected, without changing or stopping services. Focused Ruff, shell syntax, Node hook harness and browser fixture syntax passed. Offline lock validation, installer dry-run and local activation prompt check passed. Frontend `npm run lint` and `npm run build` passed; Vite built 95 modules in 6m45s on the constrained Pi. Tracked production assets were regenerated, replacing the old hashed JavaScript bundle. Documentation links for both public READMEs, plan/report and all eight new raw manual/snapshot/evidence documents passed; old registered manual hashes are unchanged.

Protected source check reports nine changes against its older baseline: root pyproject/lock, core metadata, config, movement CLI/controller, agent, runtime pipeline and web server. Some are from the already-reviewed previous built-in feature. Fingerprints are not refreshed. Wiki knowledge check reports changed/new implementation mappings, as expected while new evidence is deliberately un-ingested; current raw originals and pointers are unchanged. Live Playwright is unavailable and was not installed; hook tests are not an actual browser/ngrok test. No servo, display, buzzer or live network service acceptance test occurred.

## 10. Pass/fail checklist

- Inert exit order, errors and type-preserving movement behavior: PASS.
- Inert ownership, tabs, cleanup, timeout, stale-generation/centering guards and QR failures: PASS.
- Inert installer rerun/prompt/lock tests and Node hook checks: PASS.
- Frontend lint/build, documentation links and full root regression excluding unchanged-source baseline: PASS (319 tests).
- Protected unchanged-core gate: FAIL by design; review authorized diffs before updating baseline.
- Wiki ingestion, normalization, curated updates and semantic review: NOT RUN, explicitly deferred to owner.
- Live browser/ngrok reconnect and actual LCD scanability: NOT RUN.
- Physical Poweroff/home, holding behavior, power and abort latency: NOT RUN.

## 11. Rollback steps

Support the robot and isolate actuator power before stopping a runtime, because shutdown may move it. Restore backed-up private config/calibration deliberately. Revert reviewed lifecycle changes together (web backend, session hook/layout, installer metadata) if rolling back: an old frontend without `/ws/session` cannot use the new API guard. Rebuild frontend assets after changing frontend versions. Revert root pyproject and root lock entry together if restoring distribution identity; `.venv` prompt-only activation changes do not alter installed dependencies. Prior immutable wiki raw manuals remain available; new lifecycle sources are candidates and no current pointers were switched.

