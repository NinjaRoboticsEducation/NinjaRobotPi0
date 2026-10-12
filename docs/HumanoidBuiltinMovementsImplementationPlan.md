# Humanoid Built-in Movements Implementation Plan

Date: 2026-10-12. Owner authorization: add the documented Humanoid defaults automatically during module configuration import, expose them through Movement Tool, web selection and Ninja Agent, validate thoroughly, and prepare raw wiki content only. Existing unrelated workspace changes are preserved.

## Outcome and boundaries

Install the exact 34 `humanoid_*` sequences (1,203 steps) from `DevelopmentPlanDoc/HumanoidBuildinMovements.md` as package data. For `robot_type=humanoid` with all BCM GPIO20–27 configured, configuration import/type reconciliation seeds these sequences in addition to the existing generic `home`: 35 defaults / 1,204 steps. Partial Humanoid configurations retain only their existing all-configured-channel `home`; the full library must not seed when any required channel is absent. Tire/Wheel defaults and installed Spider data are unchanged.

Use existing JSON `moves`, `speed`, optional `per_servo_speeds`, profile metadata and managed hashes. Retain custom movements, edited managed values and same-name collisions. Existing imports/type selection remain non-actuating; loading an existing config remains read-only and does not silently migrate it. No driver timing, calibration, GPIO wiring, web payload, cloud-provider or motion interpretation change is planned. No hardware/service launch, installation, live configuration replacement or publication is included.

The user's requested implementation authorizes the phases below. Wiki source registration, normalization, ingestion, semantic review, current-manual pointer changes and implementation-map publication are deferred by explicit owner instruction.

## Evidence and findings

Read the complete Humanoid reference: all narrative, per-movement source/adaptation descriptions, 34 decoded sequences and all 1,203 keyframes. Exact mapping: YL/YR/RL/RR/LA/RA → GPIO20/21/22/23/26/27; shoulders24/25 remain nominal0. Preserve all source/adaptation choices including asymmetric arm wave repetitions and VICTORY's documented correction. No Poweroff or Wave_Left_Hand is added. Source timing, dwell, detach and multimodal effects are still unsupported; physical movement qualification remains pending.

Retrieved wiki pages:

- `wiki/concepts/humanoid-otto-waypoint-library.md`: draft/unverified, current AI semantic review; documents proposed library only.
- `wiki/concepts/spider-otto-waypoint-library.md`: draft/unverified, AI semantic review; existing native catalog/reconciliation and type guards.
- `wiki/concepts/motion-system-and-easing.md`: draft/unverified, AI semantic review; older permissive-pin/cancellation descriptions are superseded by the later preflight section and executable code.
- `wiki/concepts/action-library-and-ai-agent.md`, `wiki/references/api-and-cli-reference.md`: capability and execution contracts, verified against code.

Current raw manuals resolved through `project-knowledge.json`: InstallationGuide `src-20261010-installationguide-3`, DevelopmentGuide `src-20261011-developmentguide-4`, DevelopmentLog `src-20261012-developmentlog`. Current software still gives Humanoid only `home`; older Spider page wording that load reconciles is inaccurate—`load_config` does not seed/write an existing file. Existing global knowledge-map drift and missing `DevelopmentPlanDoc/spider_movement.json` are baseline issues, not a license to refresh unrelated hashes.

Serena/code tracing:

- `config.import_and_update_config` imports subsystem settings, calls `seed_builtin_movements` and saves changes. `set_robot_type` also reconciles.
- `builtin_catalog`, `seed_builtin_movements`, `available_movements`, `validate_movement` centralize native catalog/scoping/preflight.
- `MovementController.execute_movement` validates the full sequence before driver calls; discovery uses actual active driver pins.
- `movement_cli.execute_movement_cli` lists filtered names and executes through the controller.
- `web_server.get_movements` supplies the existing dropdown; `execute_movement` preflights before reclaiming runtime and returns422 on incompatibility. `ninja_webapp/src/pages/Movement/index.jsx` already consumes these endpoints.
- `NinjaAgent._load_robot_capabilities` advertises filtered names; `_validate_native_plan` strips an entire invalid native chain for text/audio. Server execution still uses the guarded controller.

Existing `humanoid_` prefix and metadata prevent wrong-type execution. A legacy renamed copy without either can bypass those checks. Add recognition of exact known Humanoid non-neutral pose sequences, independent of speed changes and string/integer GPIO spelling. Exclude the all-neutral `humanoid_home` geometry so generic Wheel/Humanoid center moves remain usable. Arbitrary heavily modified unscoped trajectories cannot be inferred reliably; preserve custom movement compatibility rather than declaring every eight-channel motion Humanoid. Controller preflight remains authoritative at execution even if advertised capabilities become stale.

## Phase 1 — Freeze and package the reference data

Add `scripts/build_humanoid_movements.py`, an offline deterministic extractor restricted to the standalone library markers. Reject duplicate JSON keys/names, incorrect envelopes, unexpected names/counts/channels, nonzero shoulders and invalid native steps. Output `ninja_core/src/ninja_core/data/humanoid_otto.json` with `robot_type=humanoid`; include `--check` for exact parity. No runtime dependency on the Markdown or external Otto checkout.

Validation: every source sequence equals packaged data, canonical inner-object fingerprint `49f6c4fe998b3c8500347f56eeeb7e165fb442c206ac373485310af7d280d2d6`, 34/1203 counts, installed-package resource inspection where existing build tools permit. Rollback: remove only the new extractor/resource before integration.

## Phase 2 — Catalog and profile protection

Extend `builtin_movements.py` with cached Humanoid resource loading, required-pin guard and independent deep copies. Keep generic `home`. Use existing managed-hash reconciliation; do not alter configuration schema or run import against the live robot.

Recognize known non-neutral Humanoid pose sequences in shared `validate_movement`, in addition to existing prefix/metadata safeguards. Normalize supported integer/string GPIO keys for geometry comparison. Preserve Spider recognition and common neutral home. Reject incompatible profiles, conflicting metadata and missing actual driver pins before output.

Validation: full/partial/extra channels, first import, repeat import byte stability, old home-only upgrade, edited/custom collisions, deletion/reimport, stale managed updates, profile switches in both directions, caller mutation isolation, named/renamed/no-metadata and speed-edited copies, invalid later steps and abort. Rollback: restore catalog code/resource together; retain config backup. Managed reconciliation intentionally preserves user-edited entries.

## Phase 3 — Existing entry-point integration

Verify complete catalog discovery/execution via actual MovementController, existing CLI menu, web list/execute endpoints and Ninja Agent text/audio plans. Add endpoint/agent refinements only if tests expose an actual gap. No frontend redesign or duplicate control path is needed: the existing dropdown renders backend movement names.

Validation: execute all34 sequences using inert drivers in reversed GPIO order, compare all1,203 batches and easing/speed modes, reject wrong-type manual/web/agent plans before servo writes or native-runtime reclaim, test agent whole-chain rejection and valid plan preservation. Recheck behavior after type change. Network/model calls are mocked; no cloud request or server lifecycle starts.

## Phase 4 — Lint, regression and packaging

Run targeted pytest checks, relevant existing config/catalog/controller/agent/web regressions, generator parity, Ruff, Python compilation and `git diff --check`. Compare the protected-core baseline, review each intended changed source and update only approved changed fingerprints after tests; preserve all unrelated baseline entries. Verify package build metadata includes JSON and inspect a standalone wheel if an existing offline build backend is available. Record environment limitations rather than claiming missing tests passed.

Physical commissioning is deferred: mapping/neutral/limits, GPIO conflicts, power/balance, full arm endpoints, source timing differences and stop behavior remain owner-manual tests. Software acceptance does not imply physical gait safety.

## Phase 5 — Documentation and raw wiki handoff

Update the Humanoid reference's current installation/registration guidance while retaining all34 definitions unchanged. Add `docs/validation/HumanoidBuiltinMovements-2026-10-12.md` with actual checks and pending Pi acceptance. Create new complete English raw InstallationGuide, DevelopmentGuide and DevelopmentLog versions under `ninjarobot_pi0_Wiki/raw/.../2026-10-12-humanoid-builtins/`, rebasing links as needed, plus an implementation evidence note with changed paths, hashes, tests and limitations. Preserve all existing registered originals, catalog/review records, curated pages, current pointers and `project-knowledge.json` from the start of this task.

Do not run source add/normalize, plan apply, ingestion or review. Owner manual validation will precede wiki publication. Raw-only handoff deliberately leaves the current curated/manual map describing the prior implementation; list pages requiring subsequent owner updates instead of manufacturing review completion.

## Acceptance checklist

- Full Humanoid module import produces35 defaults and exact managed/scoped34-entry library.
- Repeat import preserves bytes and user edits; profile switching hides/removes only unchanged managed entries appropriately.
- Partial channels never expose the full library; actual missing driver pins prevent execution.
- All three requested interfaces discover and execute the new movements through shared preflight.
- Wrong-type prefixed/scoped/known renamed trajectories are refused before output; generic center moves remain valid.
- The documented34 sequences and packaged resource match exactly; existing Spider data and schema remain intact.
- Relevant lint/tests/packaging checks pass or an observable environmental blocker is documented.
- New raw manuals/evidence are prepared, while ingestion/review/publication remain owner-deferred.
