# Spider default replacement — 2026-11-06

## Scope and plan

Owner-authorized replacement with DevelopmentPlanDoc/spider_movements_261106.json. Validate every step and duplicate key; generate installed data/spider_defaults.json using a strict source/fingerprint checker; use the installed resource directly; preserve legacy geometry recognition and edited/custom movements; run host regressions and package checks; prepare raw documentation without ingestion/review. Original research and previously installed spider_otto resources remain historical, unchanged.

## Environment and prerequisites

Host Python with cached dependencies and inert hardware/cloud imports. No package installation, live configuration, service startup or Pi access. Updated installed package, calibrated GPIO20–27 and backed-up config/servo calibration are needed on the Pi.

## Safety notes

Both walks change geometry on all 37 steps and use S; both runs retain geometry but change to F. Verify actual calibrated direction, clearance, support and external servo power/common ground. All nominal angles must be within ±90. Poweroff remains exact and can run during exit before PWM release.

## Safe smoke tests

After deploying updated code, run `.venv/bin/ninja_core config set-type spider` then `.venv/bin/ninja_core config import` in the runtime directory. These commands do not initialize HAL. Fresh full Spider config must equal all supplied entries; reimport is idempotent. Edited/custom collisions remain preserved. Partial Spider profiles do not seed full defaults. Deliberately reload a running runtime.

## Communication/interface tests

Shared CLI/web/NinjaAgent catalog/controller paths remain unchanged. Host regressions verify exact batches/speeds for every movement, managed upgrades, preserved edits, type/channel rejection and lifecycle behavior. Legacy installed poses still reject renamed copies on other profiles.

## Sensor/display checks

No driver/sensor/display/frontend change. Physical/browser acceptance is pending.

## Actuator-moving tests

Owner only, pending: support the robot, verify directions/travel and test small poses before grouped gaits or F runs. Tools/server may energize/center hardware on startup and execute Poweroff on exit. No hardware was operated here.

## Expected outcomes

20 movements / 566 steps, unchanged names; 417 M, 75 S, 74 F steps, empty/absent overrides. All steps address GPIO20–27. Poweroff unchanged. Canonical movement SHA256: f2c7a50dd9458182e3eac8a73fb749370269c58443d37645a9562d7fb02e1b3c. Source JSON remains unchanged.

## Execution status and checklist

PASS: 463 host tests, with two upstream dbus_next deprecation warnings. Focused Ruff, strict source/resource parity, protected-core, whitespace and standalone wheel/direct zip-resource parity checks passed. Wiki query: Spider waypoint concept, ninja-core, motion/easing and API/development references are draft/unverified. Source-grounded review is not physical acceptance. Raw manual/evidence updates only; ingestion/review/current mappings remain owner-deferred.

## Rollback

Restore prior loader/resource and backed-up config; preserve calibration and custom movements. Ordinary config load does not seed defaults; import/type selection reconciles only unchanged managed entries. Exit/reload itself may move hardware.
