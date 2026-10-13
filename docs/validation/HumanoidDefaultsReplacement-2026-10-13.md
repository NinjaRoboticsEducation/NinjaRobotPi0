# Owner Humanoid defaults validation — 2026-10-13

## 1. Scope of validation

Replace full Humanoid defaults with [the supplied list](../../DevelopmentPlanDoc/humanoid_movements_updated.json), exactly 37 movements / 1,278 steps, including Poweroff. See [plan](../HumanoidDefaultsReplacementPlan-2026-10-13.md). Only the extra terminal closing brace in the owner file was removed; all movement values are preserved.

## 2. Environment and prerequisites

Host Python tests use cached dependencies directly with inert peripheral/cloud imports and network mocks. No dependencies were installed or lockfiles/environment modified. Owner Pi validation requires updated installed code, backed-up config/calibration, calibrated BCM20–27 and the Humanoid type. No Pi was accessed.

## 3. Safety notes

The supplied ordinary steps use M (1,204 steps), and the two new 37-step runs use F (74 steps). Faster execution does not prove walking/running balance or travel. Poweroff retains shoulders +30/−30 and arms +90/−90. Verify calibrated joint directions/clearance, support and external servo power/common ground before grouped motion. Tool/server startup and exit can move/energize hardware; shutdown releases PWM.

## 4. Safe smoke tests

After updating installed code, in the calibrated runtime directory:

```bash
.venv/bin/ninja_core config set-type humanoid
.venv/bin/ninja_core config import
```

These configuration commands do not initialize HAL. A fresh full profile should equal the supplied movements list exactly; repeat import should be idempotent. Existing custom/edited entries are preserved, so an upgraded owner's list can intentionally differ. Unchanged managed generic home is removed; custom/edited home is retained. Partial profiles still receive fallback home. Deliberately reload a running runtime to read changes.

## 5. Communication/interface tests

459 host tests passed across Humanoid/Spider defaults, lifecycle, Spider waypoints, action library and installation/onboarding workflows. The real onboarding worker import then identity steps produce exact source parity; subsequent reimport is stable. CLI/web/NinjaAgent shared discovery and controller preflight accept supported movements and reject wrong types/missing pins. Every current sequence executes exact target batches and supplied speeds with inert drivers. Poweroff menu/exit, web/agent dispatch and shutdown animation tests passed.

## 6. Sensor/display checks

No sensor/display/driver/controller/frontend/onboarding implementation changed. Host lifecycle regressions use inert dependencies. Physical peripherals and browser layout were not tested.

## 7. Actuator-moving or power-risk tests

Owner only, pending: support the commissioned robot and confirm physical readiness, then test small poses before grouped gaits or F runs. Verify Poweroff through movement-tool/web/NinjaAgent and deliberate shutdown before PWM release. Starting these tools and commanding movements may energize/move actuators. No host check proves physical acceptance.

## 8. Expected outcomes

Fresh full Humanoid: exact 37 source names/sequences, no extra generic home. All prior 34 names/geometry persist with new M speed; new forward/backward runs match walk geometry at F. Poweroff is unchanged. Partial Humanoid: fallback home. Tire/Spider defaults unchanged. Managed old defaults update; edited/custom movements and calibration are preserved. Scope guards still recognize legacy geometry after rename/speed edits.

## 9. Execution status and evidence

**PASS:** 459 relevant host tests. New strict builder and unchanged Otto builder parity, Ruff E4/E7/E9/F and formatting, protected-core, whitespace, standalone wheel/direct zip import and local document links passed. The reviewed canonical movement SHA256 is `2497b7a778be779f97fd8c271398f5261711874c32b2d18e74de57f99a992a24`.

Wiki raw candidates extend the latest full Poweroff manuals/log, preserving Node-storage/fresh-install evidence. Curated pages/manual pointers/maps remain owner-deferred and contain superseded counts/speeds; the read-only knowledge gate reports that drift. No ingestion/review or fingerprint refresh is performed. Read-only strict lint/link/index checks passed with 0 errors/0 warnings; raw unregistered-source suggestions are expected. No live config, hardware, service or external agent call occurred.

## 10. Pass/fail checklist

- Full owner JSON/schema/duplicate/range/name/source fingerprint review: PASS.
- Import, actual onboarding worker, upgrade preservation, type/pin guards, M/F batch execution, CLI/web/agent/shutdown regressions: PASS, 459 tests.
- New/current-resource and original-reference parity, lint/protected-core/package/local links: PASS.
- Pi browser/actuator/balance/power acceptance: NOT RUN.
- Raw documentation prepared; wiki ingestion/review/current mappings: OWNER-DEFERRED.

## 11. Rollback steps

Back up config and servo calibration. Revert the installed resource/loader change through the normal update workflow, restore the backed-up config, and deliberately reload runtime. Do not clear calibration or overwrite custom/edited movements. Ordinary load does not reconcile defaults; module import/type selection does. Stop safely with awareness that exit can execute Poweroff.
