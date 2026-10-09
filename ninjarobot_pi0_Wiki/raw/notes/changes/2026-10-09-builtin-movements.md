# Automatic native built-in movement evidence — 2026-10-09

Candidate raw evidence only. The owner requested implementation and raw updates, and explicitly deferred wiki ingestion/review until manual validation. No source registration, normalization, semantic-plan application, curated-page change, current-pointer update, source-map refresh or semantic/human review was performed.

## Requested and implemented behavior

- Module config import seeds the selected profile after subsystem settings are collected. Robot type changes reconcile using existing configured channels. Existing config loads remain read-only.
- Spider receives the proposal's exact 19 `spider_*` trajectories and `Poweroff` (20 entries, 566 steps) when all BCM GPIO20–27 are configured. The original repository `spider_otto_*` pack/generator remain unchanged; an installed package resource contains equivalent trajectory data.
- Owner clarification: Wheel and Humanoid receive only a movement named `home`, commanding all configured servos to 0° at Slow speed. Other default gaits will be implemented by the owner later. Wheel input normalizes to the existing stored `tire` value.
- Additive `movement_robot_types` metadata scopes imported movements; `builtin_movement_hashes` preserves edits/custom collisions during reimport/type/channel changes. Only unchanged managed values are automatically removed/replaced. Incompatible edited entries remain stored but are not runnable on the new type.
- CLI execute option 4, existing web dropdown/list API and Ninja agent use shared compatible discovery. Controller execution preflights every waypoint against known type scope and active channels before the first servo write. Known prefixes and copied/renamed known Spider pose sequences, including legacy Poweroff with changed speeds/omitted empty overrides, remain guarded without metadata.
- Validate nonempty supported steps, canonical GPIO keys within BCM0–27, available channels, finite nominal ±90 angles, F/M/S speeds and valid overrides. A malformed later step prevents the entire movement from starting.
- Controller lock serializes its own operations. Callback checks occur before/after blocking driver steps; driver abort stops sequence advancement without an unsolicited controller recovery pose. In-step callback interruption and independent driver writers remain limitations.
- Web GET/POST routes and payloads stay compatible: `/api/servos/movements` returns `{"movements": [...]}`; `/api/servos/movements/{name}/execute` returns 404 unknown, 422 invalid/incompatible before runtime reclamation, 409 abort. Frontend logs HTTP errors and encodes movement names; rebuilt generated assets replace the old JS bundle.
- Text/audio agent plans use exact permitted names and configured type. Reject entire invalid native chains while retaining the response/logging the reason. Limits: 32 chain entries, 1–20 positive integer repetitions per entry. Saved Blockly actions remain separate.

## Code, documentation and validation scope

Code: `ninja_core/src/ninja_core/builtin_movements.py`, installed `data/spider_otto.json`, config, movement_controller, movement_cli, ninja_agent, web_server and core package build metadata; frontend Agent page and generated dist. No driver, original Spider pack/generator, live config/calibration, service or hardware setting was changed.

Documentation: root README/core README; `docs/BuiltinMovementsImplementationPlan.md`; `docs/validation/BuiltinMovements-2026-10-09.md`; complete new dated raw manuals, README snapshots and plan snapshot. English, Japanese and Traditional Chinese summaries cover import, home scope and physical readiness; detailed new design/testing sections remain English.

The local environment identifies as **Raspberry Pi Zero 2 W Rev 1.0**, aarch64, existing Python 3.13.5 environment. Tests used inert/mocked hardware and synthetic configuration files. No HAL initialization, servo/GPIO/buzzer/display activation, package installation or live AI/account request was performed. Existing pigpiod was left running and untouched. Physical direction, mapping, clearance, balance, power, timing and stopping acceptance remain pending.

## Verification results

- Initial 39 new feature tests and 60 existing config/Spider/agent regressions passed.
- After the owner-confirmed home naming and CLI/web success tests, the combined targeted run reported **101 passed**.
- The final feature suite reported **42 passed in 284.93s**, exited normally (0), and includes the legacy-Poweroff pose-recognition regression.
- The broader earlier suite reached 100% with four failures: three installer-bootstrap cases failed because the existing pigpiod daemon was active; `test_protected_robot_sources_unchanged` detected six authorized feature changes. Installer tests used mocks and did not perform installation. These failures do not establish movement regression; they are retained for owner review, not suppressed or fixed outside scope.
- Focused Ruff and `git diff --check` passed. Frontend `npm run lint` and `npm run build` passed (94 modules, generated new JS bundle).
- `python3 scripts/build_spider_movements.py --check` passed: original 19-entry pack is byte-for-byte reproducible. Feature tests compare all 20 JSON fragments in the supplied proposal with the runtime catalog, preserving trajectory values and exact Poweroff.
- Built a standalone core wheel using existing cached Hatchling dependencies without installing anything. Its archive contains the Spider JSON resource; the catalog loads 20 Spider entries directly from the wheel without repository movement assets.
- Current README/core README/plan/validation-report local links passed the repository's link checker function.
- `verify_core.py` flags only six intended protected changes: core pyproject.toml, config.py, movement_cli.py, movement_controller.py, ninja_agent.py and web_server.py. Baseline hashes remain unchanged. Unrelated tracked bytecode produced by early tests was restored.
- Two earlier pytest processes remained heavily paging during teardown after reporting completed tests; only those identified test subprocesses were terminated (exit 143) to release memory. Their captured test results are retained; the full suite is not described as a clean process pass. The final feature suite exited normally. The robot's existing processes and daemon were untouched.

## Wiki evidence and discrepancies

Wiki search/source-status CLI was unavailable because the independent wiki environment is missing. No setup/dependency installation was attempted. Tracked pages were read directly: Motion System and Easing, Spider OTTO Waypoint Library, ninja_core, pi0servo, and Installation and Wiring. They are draft/unverified, with recorded passing AI semantic reviews; those reviews do not imply human/physical acceptance. Version-current complete manuals were resolved through project-knowledge.json. Baseline project-knowledge check passed before implementation.

Sources used include `src-20261009-2026-10-09-spider-otto`, `src-20261009-developmentguide`, `src-20261008-installationguide-3`, and historical core/servo README sources. Original relevant hashes are preserved:

| Registered original | SHA256 |
| --- | --- |
| Compatibility InstallationGuide | 734051f87ce7f447ae50bee7863118612f55b5747cd42e3cb047662a5408081f |
| Spider DevelopmentGuide | b8d75dba21189f9521728ca3726b00660c19cb77fb58bc6c619c7bb54a2c2708 |
| Spider DevelopmentLog | 26c761085d9ad415c759477dc2e33f92bb3feab89dabf58c917bbae373fb8dcc |
| Earlier Spider evidence note | 1c35301cb86c71126d626d841c5f648680fb82c8fe857526e22b983e970939cd |

Code supersedes historical manual claims about fixed movement durations and `/api/movements` routes. Those affected descriptions were corrected in the new candidate DevelopmentGuide. Earlier opt-in/unchanged-controller claims are explicitly historical. The new implementation now rejects unknown GPIOs and checks callbacks at waypoint boundaries, but still does not implement source periods/dwells or an oscillator controller. Physical calibration remains separate from config-key presence.

## Candidate sources for owner manual ingestion/review

- `raw/articles/ninjarobotpi0/2026-10-09-builtins/InstallationGuide.md`
- `raw/articles/ninjarobotpi0/2026-10-09-builtins/DevelopmentGuide.md`
- `raw/notes/ninjarobotpi0/2026-10-09-builtins/DevelopmentLog.md`
- `raw/articles/ninjarobotpi0/2026-10-09-builtins/README.md`
- `raw/articles/ninja_core/2026-10-09-builtins/README.md`
- `raw/notes/ninjarobotpi0/2026-10-09-builtins/BuiltinMovementsImplementationPlan.md`
- This evidence note and the final validation-report snapshot.

Affected page candidates: `wiki/concepts/spider-otto-waypoint-library.md`, `wiki/concepts/motion-system-and-easing.md`, `wiki/entities/ninja-core.md`, `wiki/references/api-and-cli-reference.md`, current installation/development reference pages, configuration/profile descriptions and `wiki/analyses/development-history-and-evolution.md`. Review code/source drift and new-file classification before updating implementation mappings. The owner will register/normalize evidence, prepare/review/apply the exact semantic diff, update current pointers/maps and run wiki quality gates after physical/manual validation. No current wiki completion gate is claimed here.

## Remaining limits and rollback

Spider's sampled trajectories are not qualified floor locomotion. Poweroff/hello/jump/scared include extreme poses or lost source waits. Wheel/Humanoid have only home. Arbitrary unscoped custom mechanics cannot be inferred from JSON. Callbacks do not interrupt inside a blocking driver step, and the controller lock is not a universal independent-writer lock. Existing CLI/agent post-task centering is separate from driver-abort handling.

Back up private config/calibration and support/disconnect actuator power before stopping an active runtime; shutdown can run Poweroff. Restore the reviewed previous runtime/config together if rolling back. Removing a built-in entry alone is temporary because import seeds it again. Registered old raw sources remain intact. No physical rollout was performed.
