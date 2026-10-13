# Owner Humanoid defaults replacement evidence — 2026-10-13

New complete English raw candidates for owner manual validation. Registration, normalization, ingestion, semantic review, current pointers and implementation mapping updates remain owner-deferred. Prior source versions, including the earlier 2026-10-13 Poweroff-only candidates, remain unchanged. Earlier dated sections below are historical; this section supersedes prior Humanoid default counts, generic-home policy and installed-resource/speed statements.

The owner supplied DevelopmentPlanDoc/humanoid_movements_updated.json as the replacement Humanoid defaults. One syntax defect was repaired: an extra closing brace after the complete JSON document. All supplied movement values were retained. Duplicate-aware parsing and every-step native validation passed: 37 unique movements / 1,278 complete eight-channel GPIO20–27 steps, finite angles within nominal ±90, supported fields, 1,204 M steps, 74 F steps and empty overrides. All 34 previous movement names/geometry are unchanged except for S→M speed; new humanoid_run_forward and humanoid_run_backward reproduce corresponding walk geometry at F, 37 steps each. Poweroff retains its exact M pose, shoulders +30/−30 and arms +90/−90. Canonical movements SHA256: 2497b7a778be779f97fd8c271398f5261711874c32b2d18e74de57f99a992a24.

The installed data/humanoid_defaults.json is generated from the source by scripts/build_humanoid_defaults.py; --check verifies strict schema, reviewed fingerprint and exact rendered parity. Runtime _humanoid_catalog loads this package resource without overriding any entry. A full Humanoid catalog equals the supplied 37-entry list exactly, with humanoid_home and no extra generic home. Partial profiles retain the prior generic-home fallback. The original 34-entry Otto reference/resource/generator remain unchanged historical research. Runtime does not need DevelopmentPlanDoc files after installation. Tire/Spider catalogs, native movement/controller schema, frontend/agent APIs and onboarding implementation remain unchanged.

Existing module import and robot-type selection reconcile managed defaults. Actual onboarding import then identity workers were tested: selecting Humanoid after importing saved modules seeds exact source parity; repeat import is idempotent. Unchanged managed old entries update to the owner list, and unchanged managed generic home is removed. Edited/custom defaults/home/collisions and calibration are preserved, so an owner's upgraded config may intentionally differ from the fresh list. Prefix/known-geometry guards still recognize the unchanged prior trajectories on wrong profiles after rename/speed edits.

459 inert host tests passed across current/default movement, lifecycle, waypoint/action and installation/onboarding workflows. Every current sequence reaches exact targets and M/F modes; type/channel guards, old managed upgrade, edited preservation, CLI/web/agent discovery/execution and Poweroff shutdown passed. Ruff syntax/Pyflakes/format, both current and original builder parity, protected-core, whitespace, standalone wheel/direct zip import and local links passed. The wheel contains exact current/legacy/Spider resource bytes, and direct package import equals all 37 owner movements. Read-only wiki strict lint/link/index checks pass; the knowledge gate reports expected new/current and prior installer mapping drift. No dependency installation, fingerprint refresh, live configuration, hardware/service/real agent operation, ingestion or review occurred. Pi/browser/physical acceptance remains owner-pending.

After updating installed code, from the calibrated runtime directory use .venv/bin/ninja_core config set-type humanoid and .venv/bin/ninja_core config import (or import-all), then deliberately reload a running runtime. Configuration commands do not initialize HAL. Support the robot and verify joint directions/limits/clearance/power before testing M/F movements; software run names do not establish physical running. Poweroff can move during deliberate tool/server exit and PWM is released afterward. Back up config/calibration before resolving edited collisions or rolling back.

See [replacement plan](../../../../../docs/HumanoidDefaultsReplacementPlan-2026-10-13.md), [validation](../../../../../docs/validation/HumanoidDefaultsReplacement-2026-10-13.md) and [owner JSON](../../../../../DevelopmentPlanDoc/humanoid_movements_updated.json).

## Reviewed code and wiki evidence

- builtin_movements.py: new package resource selection; full catalog exact source; partial fallback; unchanged managed reconciliation/shared preflight.
- config.py: import_and_update_config and set_robot_type both seed defaults without HAL initialization.
- scripts/onboard.py: existing _worker(import) and _worker(identity) dispatch those functions. Tested actual workers with inert imports and isolated config directory.
- movement_cli.py, web_server.py, ninja_agent.py: unchanged shared catalog/controller consumers. Exact target/speed and shutdown integration regressions pass.
- Queried draft/unverified Humanoid waypoint concept, ninja-core, motion/easing, API/CLI and installation/development references. Existing registered source IDs include src-20261012-humanoidbuiltinmovementsevidence and src-20261012-developmentguide. The knowledge map still points to prior complete Humanoid-builtins manuals; newest full candidates carry forward Poweroff/Node-storage repairs. Source-grounded semantic review is not human/device acceptance.

## SHA256 of reviewed artifacts

- `DevelopmentPlanDoc/humanoid_movements_updated.json`: `655d06ffbb6fb2fba4b25572bc64b30ef4888175d4911d026f2fe978e9cf1d35`
- `ninja_core/src/ninja_core/data/humanoid_defaults.json`: `e9550b4d62fcb68fc76feac4e3e140d4687a07524ddc8be59dc76a9ee6201de5`
- `ninja_core/src/ninja_core/builtin_movements.py`: `b72dfbf946f8fb13857151bc3dd4817700e77e6446d97f214c5678909e216fda`
- `scripts/build_humanoid_defaults.py`: `9d971706cbd513ee23fbe2db4378ccea36481126d1289fa9fb549a940e10cda6`
- `tests/test_builtin_movements.py`: `07ecc91cb734fd2468566c024da6c9858f8ca687445748a7a7a1ad76627d3091`
- `tests/test_humanoid_builtin_movements.py`: `8d9ef603d97c0f91e0303e670813c753f5ccc10d8587bc01a80419fb9adb881f`
- `DevelopmentPlanDoc/HumanoidBuildinMovements.md`: `336eaef620ea617ae224b0e288f4150e54fe2b8062f70e9d893d3b8e31af546e`
- `README.md`: `9cf8847dcd6385b29c8e4e41f78f4981e347215ed52b71fc666ac19143820b6b`
- `docs/HumanoidDefaultsReplacementPlan-2026-10-13.md`: `e97cace62e72682970d49626637bbe75bd707d62ae96d4b3be58b0e47a3a9548`
- `docs/validation/HumanoidDefaultsReplacement-2026-10-13.md`: `dbbe1862e1e549e5d4f03c5484c518175fabe3494c99d7f297115a600b78027a`

## Owner publication scope

After manual validation, ingest these full manuals/log/English README/evidence, then update Humanoid waypoint concept, motion/easing, ninja-core, API/CLI, hardware-tools, installation/development references and history. Reconcile prior raw candidates before refreshing current pointers and reviewed implementation maps. No publication/ingestion/review occurred in this task.
