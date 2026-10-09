# Built-in movements implementation plan

Date: 2026-10-09. Scope authorized by the owner's request to draft and implement this feature. Hardware operation is not authorized. Wiki ingestion and semantic review are explicitly deferred to the owner.

## Outcome and evidence

Importing subsystem configuration must seed movements for the configured robot type, persist them in `config.json`, and make the same compatible names available to movement-tool, the existing web dropdown, and Ninja agent. The existing canonical wheel type is `tire`; retain it and accept `wheel` as an input alias.

Read `DevelopmentPlanDoc/SpiderBuildinMovements.md` in full, including the 20 JSON definitions and timing, mapping, shutdown and validation caveats. Its 19 `spider_*` trajectories correspond to the repository's 19 `spider_otto_*` entries; its additional `Poweroff` is absent from that pack. Preserve original generator/data and package an equivalent runtime resource. Continue using ordered waypoints and F/M/S; do not implement the separate oscillator proposal implicitly.

Wiki retrieval used tracked pages because CLI search/source-status reports a missing wiki environment. No dependencies were installed. Relevant pages are `wiki/concepts/spider-otto-waypoint-library.md`, `wiki/concepts/motion-system-and-easing.md`, `wiki/entities/ninja-core.md`, `wiki/entities/pi0servo.md`, `wiki/references/installation-and-wiring.md`, and the current complete DevelopmentGuide/InstallationGuide resolved through `project-knowledge.json`. Pages are draft/unverified with recorded passing AI semantic reviews; these are not physical acceptance. Registered evidence includes `src-20261009-2026-10-09-spider-otto`, `src-20261009-developmentguide`, `src-20261008-installationguide-3`, and historical README sources. Baseline `scripts/wiki.py check` passed before implementation.

Code overrides historical documentation: native REST endpoints are `/api/servos/movements` and `/api/servos/movements/{name}/execute`, not the older manual's `/api/movements`; actual command is `config import`. HAL orders channels from `config.servos.calibration` but reads physical calibration from `servo.json`. Existing unknown GPIO targets are silently skipped. Existing agent advertises all names without type checks and uses an invented unprefixed walk example. These discrepancies belong in the raw-source handoff.

## Phase 1 — Registry and configuration lifecycle

1. Add a hardware-free registry using installed package resources. Seed Spider's 19 renamed trajectories and exact document-defined Poweroff; keep legacy names accepted when already configured.
2. Wheel/Humanoid actuator roles and gait definitions are absent from the supplied proposal and repository evidence. The owner confirmed both profiles should receive a `home` movement returning every configured servo to center; other default movements will be implemented by the owner later. Implement only this zero-angle positional-servo reference pose. Do not invent directional mappings or continuous-rotation motor control.
3. Persist additive `movement_robot_types` and `builtin_movement_hashes` metadata, keeping the existing `movements: name -> list` contract. Attach type scope to imported built-ins, including Poweroff. Scope known prefixes and legacy Spider Poweroff data even without metadata.
4. Import after calibration is collected. Seed only when all required pins exist. Reimport is idempotent; preserve custom sequences/collisions and edited built-ins. Remove only unchanged managed entries when type/pin requirements change; retain edited entries with their scope. Reconcile on `config set-type` too. Loading an existing config remains read-only.

## Phase 2 — Shared discovery and execution guards

1. Provide shared compatibility/step validation for CLI, web and agent. Restrict type-specific names, metadata and known Spider trajectories to their robot type, including copied legacy data.
2. Before any sequence executes, validate every step: supported keys, nonempty GPIO targets, configured/active pins, finite nominal signed angles and supported speeds. Reject the whole sequence before its first actuator write when a later step is malformed.
3. Controller rechecks compatibility at execution, rather than relying on UI filtering or model instructions. Preserve GPIO ordering, omissions, per-servo overrides and easing. Serialize controller servo operations; check cancellation between waypoints and stop advancing after driver abort. Document the remaining in-step callback limitation.
4. Web returns clear client errors for invalid/incompatible movement requests before runtime reclamation. Keep route/payload contracts and existing dropdown UI.

## Phase 3 — Agent and CLI integration

1. Advertise only executable compatible movements and include configured robot type in the model prompt. Use exact listed names; remove the unqualified walking example.
2. Validate complete native action chains from both text and audio, with bounded positive repetitions. Reject the entire native chain for unavailable/type-incompatible/malformed names, retain conversational response and record the reason. Controller remains the final execution guard even if a plan bypasses the agent.
3. CLI lists compatible names and handles rejected playback cleanly. Recording/editing preserves metadata on scoped names. Existing custom unscoped names remain compatible when their steps/pins validate; unknown mechanical roles cannot be inferred from arbitrary custom data.

## Phase 4 — Host validation and review

Use existing `.venv` tools without syncing/installing. Test fresh import and repeat import, type switching, pin changes, collisions/edits, packaged resource parity, legacy names/Poweroff, malformed late steps, wrong-type direct execution, inactive channels, shuffled ordering, driver abort, CLI/web discovery and requests, and text/audio agent rejection. Run narrow regressions then the full host suite and focused Ruff. Run generator `--check` and protected-core verification; report intentional authorized runtime diffs instead of refreshing baseline hashes to hide them. Inspect package resource inclusion without installing dependencies.

## Phase 5 — Documentation and manual Pi handoff

Update README/core README and prepare complete NEW dated InstallationGuide, DevelopmentGuide and DevelopmentLog raw versions plus code/validation evidence and package README snapshot. Preserve registered originals. Include English, Japanese and Traditional Chinese usage/safety summaries. Record owner-manual Pi tests in `docs/validation/BuiltinMovements-2026-10-09.md`, separating non-moving config checks from activation and extreme poses. All physical checks remain pending.

Per the owner's explicit instruction, do not register/normalize/ingest sources, update curated pages/reviews, apply semantic plans, refresh knowledge mappings or current manual pointers. List candidate sources and affected pages for their later manual workflow. Consequently source/code drift is expected and the wiki completion gate remains deferred, not passed.

## Acceptance and risks

Host acceptance requires identical permitted movement names across the three interfaces, safe rejection of wrong-type/stale/invalid data before servo writes, deterministic idempotent import preserving user edits, and unchanged native trajectory values/easing. Physical acceptance requires owner verification of GPIO-to-joint placement, runtime `servo.json`, mounting direction, clearance, power and stopping. Spider's ±90 Poweroff and jump/hello poses can stress linkages; sampled gaits do not preserve source oscillator timing or balance. Home commands can move actuators and zero angle is not proof of a safe physical pose. Wheel/Humanoid locomotion remains dependent on supplied build-specific definitions.
