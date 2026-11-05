# Humanoid default replacement evidence

## Humanoid default replacement — 2026-11-05

The current default authority is DevelopmentPlanDoc/humanoid_movements_261105.json, packaged as ninja_core/data/humanoid_defaults.json. It supplies exactly 37 movements / 1,278 steps. Six walk/run/turn sequences transfer arm trajectories from GPIO26/27 to GPIO24/25. Walks use S, runs/turns F, others M; totals are 74 S, 148 F and 1,056 M steps. Poweroff and all other movements are unchanged. Native schema, duplicate keys, channel availability and reviewed fingerprint were checked before packaging. Canonical movements SHA256 is 6a2397a7838d091dc1c7eaae2a6fc9eaa59ea8c33dc50c5b29e201d307a8f281.

Onboarding/import/type selection use the existing managed reconciliation: unchanged managed values update, edited/custom values and calibration remain. All eight configured channels are required; partial profiles keep fallback home. CLI/web/agent share the same catalog and controller preflight. Old original Otto poses remain recognized for wrong-profile rejection after renaming. No frontend, driver, onboarding or movement schema change was needed.

462 inert host tests passed, with two upstream dbus_next deprecation warnings. Ruff, both builders, protected-core, whitespace, standalone wheel/direct zip resource parity and document links passed. No package installation, live config, hardware or real external agent call occurred. Physical Pi/browser acceptance remains pending: confirm calibrated GPIO24/25 joint direction and clearance, support and power before moving. Tools/server can center on startup and execute Poweroff on exit before PWM release.

After updating installed code, run .venv/bin/ninja_core config set-type humanoid then .venv/bin/ninja_core config import from the calibrated runtime directory; deliberately reload a running runtime. Back up config/calibration first. Restore prior code/resource and backed-up config for rollback without overwriting custom sequences.

This is new English raw evidence only. Owner-deferred ingestion/review/current pointers/maps remain unchanged. Existing unrelated wiki/manual edits are preserved. Earlier sections below are historical and superseded for Humanoid source, speeds and arm-channel geometry. See [validation](../../../../../docs/validation/HumanoidDefaults-2026-11-05.md).

