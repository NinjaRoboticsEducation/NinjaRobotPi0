# Humanoid Poweroff validation — 2026-10-13

## 1. Scope of validation

Add the owner's exact Humanoid `Poweroff` at speed M: GPIO20–23=0, 24=30, 25=-30, 26=90, 27=-90, empty per-servo overrides. Full Humanoid profiles have 36 defaults / 1,205 steps. The 34 Otto movements and Spider defaults remain unchanged. See [plan](../HumanoidPoweroffPlan-2026-10-13.md).

## 2. Environment and prerequisites

Host validation uses cached Python dependencies directly with inert peripheral/cloud imports and network mocks, without installing packages or editing the project environment. Raspberry Pi Zero 2W acceptance requires the updated installed package, backed-up runtime `config.json`/`servo.json`, Humanoid type and all BCM20–27 channels. No actual Pi was accessed.

## 3. Safety notes

GPIO24/25 shoulders now receive the explicit owner targets rather than nominal zero. Verify joint identity/direction and collision-free travel; GPIO26/27 reach nominal ±90. Support the robot, confirm calibrated limits and external servo power/common ground. Starting a server or movement-tool can center/energize hardware, and exiting can execute Poweroff before releasing PWM. Removing power is not a software test.

## 4. Safe smoke tests

From the calibrated runtime directory after deploying the new code:

```bash
.venv/bin/ninja_core config set-type humanoid
.venv/bin/ninja_core config import
```

These commands update configuration without HAL initialization. Inspect `config.json`: `movements.Poweroff` must match the requested pose, `movement_robot_types.Poweroff` must be `humanoid`, and managed hashes must match for an unchanged default. Reimport is idempotent. Custom/edited name collisions are intentionally preserved; do not expect replacement.

## 5. Communication/interface tests

Host tests exercise actual CLI configuration import/import-all, controller discovery, web dropdown/endpoint, NinjaAgent plan validation/server dispatch and shutdown animation with inert output. Owner browser/Pi confirmation is pending: after deliberate runtime reload, Poweroff should appear and execute via all three interfaces; incompatible named or renamed known copies must be hidden/rejected before output.

## 6. Sensor/display checks

No sensor/display implementation changed. Host shutdown test has absent face/sound devices; full coordinated shutdown regressions verify existing lifecycle behavior separately. Display/sound/hardware acceptance remains pending.

## 7. Actuator-moving or power-risk tests

**Owner only, pending:** with clearance and support confirmed, command Poweroff once through movement-tool option 4, web dropdown, and NinjaAgent. Verify one synchronized batch at M and exact target ordering for actual driver channels. Deliberate movement-tool option 6 and coordinated server exit should attempt Poweroff before HAL cleanup, without a following center command in the CLI exit path. Agent post-action centering remains existing behavior. These checks can move/energize servos; no host test establishes physical safety or holding after PWM release.

## 8. Expected outcomes

Full profile: 34 Otto definitions + generic home + Poweroff = 36 entries / 1,205 steps. Partial profile: generic home only; full pose fails preflight if a required configured or actual channel is absent. Unchanged managed Spider/Humanoid Poweroff is replaced correctly on type switch. Edited/custom entries remain preserved; wrong-scope retained entries cannot run. No Wave_Left_Hand is added.

## 9. Execution status and evidence

**PASS: 364 host tests** across Humanoid/Spider catalog, import/reconciliation, lifecycle, Spider waypoint and action-library suites. Exact owner pose, independent values, scoped hashes, eight configured missing-channel cases, missing actual channel, custom/edited collisions, managed profile switching, wrong-profile copies with/without misleading metadata, int GPIO keys, speed edits, CLI menu/exit, web dropdown/execute, agent plan/server dispatch and shutdown animation passed with inert output.

Ruff E4/E7/E9/F and test formatting passed. Otto generator `--check` confirms unchanged 34 definitions / 1,203 steps. Protected-core check and `git diff --check` passed. A standalone wheel was built without installation; packaged catalog/resources match source bytes, and direct zip-resource import returns the exact Poweroff and 36 defaults / 1,205 steps. Local document links passed.

The initial reused temporary test environment was cleared. The replacement host runner reads existing cached distributions directly, prioritizing locked versions; peripheral/cloud imports are inert and all calls are mocked. No packages were installed. The raw candidates extend the latest Node-storage manuals/log, preserving their installer fixes although the current knowledge map still points to the earlier Humanoid-builtins versions.

Read-only wiki strict lint, links and index checks passed (0 errors/0 warnings; unregistered-source suggestions are expected). The knowledge check intentionally reports current changes and prior installer source/mapping drift because ingestion/review/current-pointer updates remain owner-deferred. No source hashes or implementation maps were refreshed to hide that drift. Pi/browser/physical acceptance and wiki ingestion/review are owner-pending. No hardware, live configuration, production/cloud calls or service startup occurred.

## 10. Pass/fail checklist

- Host exact pose, import, scope, execution and lifecycle regressions: **PASS, 364 tests**.
- Ruff, immutable Otto generator parity, protected-core, package inspection and local document links: **PASS**.
- Calibrated GPIO/joint mapping, shoulder direction, physical travel/support/balance and Pi interface/shutdown checks: **NOT RUN**.
- Wiki raw candidates prepared; curated knowledge/publication: **DEFERRED by owner**.

## 11. Rollback steps

Back up configuration/calibration first. Revert the additive code change and reinstall the prior package through the normal owner workflow if necessary. Restore backed-up config or remove only the newly managed Poweroff definition/scope/hash. Preserve all existing custom movements and calibration. Ordinary config loading does not seed or delete defaults. Stop/reload runtime deliberately; tool exit itself can move the robot.
