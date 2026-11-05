# Humanoid defaults replacement — 2026-11-05

## Scope and implementation plan

Owner-authorized replacement with `DevelopmentPlanDoc/humanoid_movements_261105.json`. First validate duplicate-free JSON, every native step and differences; then regenerate the installed resource/update source fingerprint; then verify import/onboarding, managed upgrades, execution and package parity; finally prepare new English raw documentation. No hardware or live configuration operation, dependency installation or wiki ingestion/review is included. Preserve unrelated pre-existing README/manual/wiki edits.

## Environment and prerequisites

Host tests use existing cached Python distributions, inert peripheral/cloud imports and mocked network. Raspberry Pi validation requires updated installed code, backed-up configuration/calibration and a fully configured Humanoid on BCM20–27.

## Safety notes

The six walk/run/turn definitions now command arm trajectories on GPIO24/25 instead of GPIO26/27. Verify physical joint identity, calibrated travel, direction and clearance before operation. Walk speed is S, runs/turns F, other movements M. Poweroff is unchanged. No claim of balance or physical running follows from host validation.

## Safe smoke tests

After installing updated code, run `.venv/bin/ninja_core config set-type humanoid` then `.venv/bin/ninja_core config import` in the calibrated runtime directory. These commands do not initialize HAL. Full fresh configuration must equal the 37 source movements / 1,278 steps exactly. Reimport is idempotent; edited/custom values remain preserved. Restart running tools deliberately to reload.

## Communication/interface tests

Existing shared CLI/web/agent discovery and controller validation remain in use. Tests exercise exact targets and speed for every sequence, onboarding import/identity, profile/channel rejection, Poweroff shutdown and managed upgrades. Legacy geometry recognition now additionally includes the original installed Otto resource, preserving wrong-profile rejection for renamed older saved movements.

## Sensor/display checks

No sensor/display/driver or frontend implementation changes. Physical/browser checks are pending.

## Actuator-moving checks

Owner only, pending: confirm support, external servo power/common ground and collision-free GPIO24/25 motion before any gait. Test short poses before F sequences. Opening/closing movement tools and server can move/energize hardware; Poweroff precedes PWM release where existing lifecycle permits.

## Expected outcomes and source review

37 names / 1,278 steps; no additions/removals. Six trajectories changed, with 34 changed poses each. All other definitions and Poweroff match the prior catalog. Speed totals: 1,056 M, 148 F, 74 S. Native schema requires exactly eight channels, finite nominal angles within ±90 and valid speed/override fields. Source canonical SHA256: `6a2397a7838d091dc1c7eaae2a6fc9eaa59ea8c33dc50c5b29e201d307a8f281`. Source file remains unmodified.

## Execution status

PASS: 462 host tests (two upstream dbus_next deprecation warnings), focused Ruff syntax/Pyflakes, both catalog builders, protected-core and whitespace checks. Standalone wheel and direct zip-resource import match the owner JSON exactly. No Pi/hardware/live agent service acceptance performed. Wiki query returned draft/unverified Humanoid concept, ninja-core, motion/easing and installation/development references; current map resolves 2026-10-13-ble-onboarding complete manuals. New raw copies carry this change; ingestion/review and mapping refresh remain owner-deferred. Existing unrelated wiki changes are preserved.

## Checklist

Host regression, builders, package inspection, lint, protected-core and links: results below. Physical mapping/clearance/balance and Pi browser/actuator acceptance: NOT RUN. Wiki publication: DEFERRED.

## Rollback

Restore previous installed catalog/build-source selection and backed-up config; preserve calibration and custom/edited sequences. Ordinary loading does not reconcile defaults, while import/type selection does. Runtime reload/exit can move the robot.
