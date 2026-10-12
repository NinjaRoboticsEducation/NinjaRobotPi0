# Humanoid Built-in Movement Validation — 2026-10-12

## 1. Scope

Native registration of the exact 34 documented `humanoid_*` sequences / 1,203 keyframes during module import/type reconciliation. Full eight-channel Humanoid profiles retain generic `home`: 35 defaults / 1,204 steps. Shared preflight also recognizes renamed known non-neutral Humanoid trajectories. Existing CLI, web API/dropdown and Ninja Agent discovery/execution paths are reused.

Changed runtime file: `ninja_core/src/ninja_core/builtin_movements.py`. New installed resource: `ninja_core/src/ninja_core/data/humanoid_otto.json`. Added deterministic offline extractor and feature tests; updated existing Humanoid count/discovery expectations. Controller, config import functions, Ninja Agent, API routes, frontend, drivers, installed Spider data and calibration are unchanged.

## 2. Environment and prerequisites

macOS host; cached CPython 3.13.14 dependencies and Ruff 0.14.6. Existing cached Python environments lacked some source entry points, so the temporary test runner used their existing CPython 3.13 bytecode as an import fallback. Compatible FastAPI/Starlette came from the robot dependency cache; other available dependencies were reused. No dependency/lockfile installation or environment rewrite occurred.

Host-only pigpio, Google SDK and pyngrok imports were replaced with temporary inert mocks; peripheral construction was forbidden. Agent generation and web runtime reclamation were mocked by the tests. Configuration save/import operated only inside pytest temporary directories. These mocks test native catalog/control logic, not actual cloud SDK, daemon, tunnel or physical GPIO operation. Standard tests on an already installed Pi environment use its real imports plus test-defined mocks.

Evidence: draft/unverified wiki motion, Spider/Humanoid catalog, agent/action and API pages; current raw manuals resolved through project-knowledge.json. Older wiki claims that load seeds defaults or ignores unknown pins are superseded by exact current code. Existing wiki drift remains recorded separately; no ingestion/review is run for this feature.

## 3. Safety and power notes

The reference mapping is GPIO20/21/22/23 for hips/feet, 26/27 for arms, 24/25 for added shoulders at nominal 0. Required channel presence does not establish calibrated/measured neutral. Verify display/buzzer pin conflicts, separate servo power/common ground, support, direction, limits and clearance before physical motion. Walk/turn source arms reach ±90. S mode is a nominal velocity factor, not a physical safety certificate. Pauses, source duration, detach and balance fidelity remain unsupported.

## 4. Executed non-moving checks

- **344 tests passed / 1 baseline test deselected** across `test_humanoid_builtin_movements.py`, `test_builtin_movements.py`, `test_spider_movements.py`, `test_lifecycle_refinements.py` and `test_action_library.py` (exit 0). The single excluded test is `test_resource_matches_owner_validated_pack_and_document`, which depends on the already missing `DevelopmentPlanDoc/spider_movement.json`. Existing installed Spider sequences and original research data are still exercised by the remaining tests.
- All 34 Humanoid definitions execute all 1,203 exact ordered batches through the real MovementController and inert driver. Speed/easing, shoulders, profile restrictions, actual missing driver pins, renamed copies/speed edits/integer GPIO keys and generic-neutral compatibility are checked.
- Fresh Humanoid selection/config import and both real CLI import aliases seed 35 entries. Reimport preserves bytes, custom collisions/edits, deletes/restores managed values correctly, and upgrades old home-only data. Switching to Tire/Spider preserves user edits while hiding incompatible ones.
- Existing movement-tool execute menu lists the catalog and executes Humanoid Jump. Web dropdown backend advertises the catalog; wrong-type execution returns 422 before runtime reclaim or output. Ninja Agent text/audio accepts correct names, rejects incompatible/mixed plans, refreshes after type changes, and a valid plan executes two Jump repetitions through the existing server/controller path.
- Offline builder `--check` passed exact package/reference parity and canonical fingerprint `49f6c4fe998b3c8500347f56eeeb7e165fb442c206ac373485310af7d280d2d6`. Duplicate-key and corrupt-marker input fail.
- Ruff check passed changed/new Python files; new-file Ruff format check passed. Protected-core verification and `git diff --check` passed.
- Offline Hatch build produced a standalone `ninja_core-0.1.0-py3-none-any.whl` in `/private/tmp/humanoid-wheel-validation/`. Its Humanoid JSON equals repository bytes, existing Spider JSON remains present, and importing the catalog directly from the wheel returns 35 defaults/ 1,204 steps. Build used existing cached backends/dependencies without install.

Temporary runner command (this host only, not a Pi setup requirement):

```bash
PYTHONPATH=/private/tmp:/private/tmp/ninjapi0-robot-env/lib/python3.13/site-packages:/Users/ninjaagent/.local/share/uv/tools/serena-agent/lib/python3.13/site-packages \
PYTHONDONTWRITEBYTECODE=1 /private/tmp/ninjapi0-robot-env/bin/python -B \
/private/tmp/run_humanoid_pytest.py \
tests/test_humanoid_builtin_movements.py tests/test_builtin_movements.py \
tests/test_spider_movements.py tests/test_lifecycle_refinements.py tests/test_action_library.py \
-q --tb=short -k 'not resource_matches_owner_validated_pack_and_document'
```

Normal equivalent in an already configured environment:

```bash
.venv/bin/python -B -m pytest -p no:cacheprovider \
tests/test_humanoid_builtin_movements.py tests/test_builtin_movements.py \
tests/test_spider_movements.py tests/test_lifecycle_refinements.py tests/test_action_library.py \
-q -k 'not resource_matches_owner_validated_pack_and_document'
python3 -B scripts/build_humanoid_movements.py --check
```

The missing Spider source fixture should be restored through its separate owner workflow before requesting a completely green unfiltered repository suite. It was not recreated or hidden by this feature.

## 5. Communication/interface acceptance — pending

On the intended Pi with the updated installed package and commissioned servo module data, stop/reload deliberately around config changes. Select `humanoid`, import modules, then inspect private config locally for 35 defaults and managed scope/hash metadata. Confirm CLI option 4, web Movement dropdown and Ninja Agent show the expected names. Web requires the active primary browser/power flow. Tools/server startup can initialize/center hardware; readiness must precede launching them.

Observed software success should match host checks: incompatible type/pins fail before movement; reimport retains custom edits. Real browser display/scrolling, cloud responses and native Pi package/import acceptance remain pending. No browser UI screenshot/build is required for unchanged frontend code, and none was performed for this feature.

## 6. Sensor and display acceptance — pending

Inventory actual pin assignments against GPIO20–27 and confirm distance/display/buzzer coexist without conflicts. Older wiring examples use servo channels for display signals; do not copy them into this profile without reconciliation. No sensor/display/device tool was run here.

## 7. Actuator-moving tests — pending

Follow the reference's progressive physical checklist: measured neutral and small single-joint moves before combined poses or gaits; inspect entry/final transitions and full source endpoints; record actual forward/left/right directions, current draw, power sag, balance and abort behavior. Keep shoulders at confirmed neutral until their physical signs are measured. No physical movement, pulse calibration or safety acceptance is claimed.

## 8. Expected outcomes

Full Humanoid import 35 defaults; partial Humanoid only generic home; Tire unchanged generic home; Spider unchanged catalog. Wrong-type known trajectories fail shared validation whether requested by CLI, web or agent. All source data remains the documented waypoint approximation; current speed/timing limitations are unchanged.

## 9. Execution status and wiki handoff

Host software validation passed as above. Pi/device/browser/cloud acceptance is pending. New complete English raw manuals/log and an implementation evidence note are prepared under `raw/.../2026-10-12-humanoid-builtins/`. They are **unregistered, unnormalized, un-ingested and unreviewed**, pending owner manual validation. No current pointer, project-knowledge map, curated page, registered raw source or prior review record was changed during this implementation turn.

## 10. Acceptance checklist

- [x] Exact 34-entry reference/resource parity and standalone wheel resource loading.
- [x] Automatic import and both CLI aliases; scoped managed defaults; reimport/custom-preservation/profile-switch checks.
- [x] Actual CLI/web/agent control paths and wrong-type/missing-channel guards with inert output.
- [x] Relevant software regression, Ruff, protected-core and whitespace checks.
- [ ] Real Pi installation/import and browser/cloud acceptance.
- [ ] Measured joint mapping/neutral/limits, power/balance/clearance and physical stopping.
- [ ] Owner manual validation, source registration/ingestion and wiki semantic review/publication.

## 11. Rollback

Stop the controlling runtime, restore the saved private config and driver calibration backups, and roll back catalog code/resource together if needed. Do not delete user edits or guess a recovery pose. The old home-only catalog removes unchanged managed Humanoid entries on deliberate import/type reconciliation; edited ones persist and need owner review. A stale mixed package/resource version is not a supported rollback. This task did not alter live robot files or publish/install a release.
