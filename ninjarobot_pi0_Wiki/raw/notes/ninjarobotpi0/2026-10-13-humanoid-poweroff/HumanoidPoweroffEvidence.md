# Humanoid Poweroff implementation evidence — 2026-10-13

This is a new complete English raw candidate for owner manual validation. Registration, normalization, ingestion, semantic review, current pointers and implementation mappings remain owner-deferred. Prior registered sources and earlier Node-storage candidates are unchanged. Earlier dated sections below retain their historical status; this section supersedes earlier Humanoid default counts and statements that no Humanoid Poweroff exists.

The owner requested an exact Humanoid Poweroff with unchanged name: one step at speed M, GPIO20/21/22/23=0, GPIO24=30, GPIO25=-30, GPIO26=90, GPIO27=-90, per_servo_speeds={}. `builtin_movements.py` adds this pose alongside the 34 unchanged Otto definitions and generic home: 36 defaults / 1,205 steps for a Humanoid with all BCM20–27 configured. Partial Humanoid profiles retain only generic home. Spider Poweroff and all Otto resource bytes/fingerprint remain unchanged. No Wave_Left_Hand is added.

After updating installed code, from the calibrated runtime directory run `.venv/bin/ninja_core config set-type humanoid` then `.venv/bin/ninja_core config import` (alias import-all). These config commands do not initialize HAL. Ordinary config loading does not seed defaults; deliberately restart a running runtime to reload. Managed hashes/scopes retain custom or edited Poweroff collisions. Unchanged managed Poweroff changes to the correct pose on Spider/Humanoid type switch; edited incompatible entries stay preserved and blocked. To restore the default after a collision, first back up configuration, remove only the conflicting entry and reimport. Never overwrite calibration or other owner movements.

Shared catalog discovery/preflight exposes Poweroff through movement-tool option4, web dropdown/execute and NinjaAgent. Deliberate movement-tool option6 and existing coordinated server shutdown attempt configured Poweroff before hardware cleanup. Existing safety/cancellation checks still apply; HAL releases PWM afterward. Known Humanoid pose geometry is rejected on incompatible profiles even with renamed movements, integer GPIO keys or speed edits. No controller, agent, frontend or shutdown implementation change was required.

364 inert host tests passed. Ruff syntax/Pyflakes, test formatting, unchanged Otto generator parity, protected-core, whitespace, standalone wheel/direct zip import and local links passed. Wiki strict lint/link/index checks pass, while the read-only knowledge gate reports expected pending source/mapping review for this and prior implementation changes. No fingerprint refresh, ingestion or semantic review was performed. No hardware, live config, real agent/cloud call or service startup occurred. Physical Pi/browser acceptance remains pending. Shoulders24/25 receive the explicit owner targets rather than the Otto library's nominal zero; verify calibrated direction, clearance, support, arm ±90 travel and external power/common ground before operation.

See [plan](../../../../../docs/HumanoidPoweroffPlan-2026-10-13.md), [validation report](../../../../../docs/validation/HumanoidPoweroff-2026-10-13.md) and [complete reference](../../../../../DevelopmentPlanDoc/HumanoidBuildinMovements.md).

## Traceable code and knowledge evidence

- `builtin_movements.py`: owner constant, cached catalog addition, independent profile catalog, known non-neutral pose scope recognition and managed reconciliation.
- `config.py`: existing import/type selection invokes seeding without HAL initialization.
- `movement_cli.py`: existing option6 selects Poweroff if present before shutdown/save.
- `web_server.py`: existing dropdown/execute/action-plan and coordinated shutdown paths consume the same controller.
- `ninja_agent.py`: existing shared capabilities/plan preflight; actual execution uses the controller.
- Queried draft/unverified `wiki/concepts/humanoid-otto-waypoint-library.md`, `wiki/concepts/motion-system-and-easing.md`, `wiki/entities/ninja-core.md`, API/CLI and development references. Prior reviewed source IDs include src-20261012-humanoidbuiltinmovementsevidence and src-20261012-developmentguide. Curated 35-default/home-only-shutdown statements need later publication updates; semantic review is not human or physical acceptance.
- Owner file `DevelopmentPlanDoc/humanoid_movements_updated.json` was already untracked and remains untouched. No replacement of other movements was authorized by this Poweroff task.

## SHA256 of implementation artifacts

- `ninja_core/src/ninja_core/builtin_movements.py`: `255dc24d8323b1a240873a31b7278d0d778db5b1204e02032afee8c3a2eadd16`
- `tests/test_builtin_movements.py`: `4d2654484ca36235f7035124a9926960d7b80631c57bc2609393392877fae5e8`
- `tests/test_humanoid_builtin_movements.py`: `e75f357fd07748c226d0d9f78095096ac1d77ec103ac8594dbd2a28b63b4f923`
- `DevelopmentPlanDoc/HumanoidBuildinMovements.md`: `791ec87590789cf299d72f7e671ab0508b29907a293468abe10450771de92686`
- `README.md`: `a097c79927beb287621acca5a507ee23087bad557498af8bdfe28c7d4f252844`
- `docs/HumanoidPoweroffPlan-2026-10-13.md`: `82a6e097e997c40026859bc9854abc246393884d19a8a07c020ad37347bda3cc`
- `docs/validation/HumanoidPoweroff-2026-10-13.md`: `f9f2f545b63f0c12bb784585a7d83e5ac8dd0d5862852077188fce23528ca085`

## Later owner publication scope

After manual validation, ingest these complete manuals/log/English README and evidence; review the Humanoid waypoint concept, motion/easing, ninja-core, API/CLI, hardware-tools, installation/development references and history. Reconcile prior installer candidates before changing current pointers or reviewed implementation mappings. This task deliberately leaves ingestion/semantic review and physical/browser acceptance pending.
