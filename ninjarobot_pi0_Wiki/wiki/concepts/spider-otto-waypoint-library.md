---
type: Concept
title: Spider OTTO waypoint library and native movement integration
description: Installed Spider movements, native execution preflights, and profile
  reconciliation.
status: draft
generated:
  by: agent:codex
  at: '2026-10-09T06:57:52.051688+00:00'
sources:
- id: src-20261009-2026-10-09-spider-otto
  resource: urn:llmwiki:source:src-20261009-2026-10-09-spider-otto
  title: 2026 10 09 Spider Otto
  content_hash: sha256:1c35301cb86c71126d626d841c5f648680fb82c8fe857526e22b983e970939cd
- id: src-20261009-2026-10-09-builtin-movements
  resource: urn:llmwiki:source:src-20261009-2026-10-09-builtin-movements
  title: 2026 10 09 Builtin Movements
  content_hash: sha256:6bd14ef705bb60c2c228c95940fd6cb771299532f13e10fdc4faae22db3f216a
- id: src-20261009-builtinmovementsimplementationplan
  resource: urn:llmwiki:source:src-20261009-builtinmovementsimplementationplan
  title: Builtinmovementsimplementationplan
  content_hash: sha256:3472c9ab43ab152d13ffe12099cf8f6e539339a5197e5f513a5f15779575d3c2
- id: src-20261009-builtinmovementsvalidation
  resource: urn:llmwiki:source:src-20261009-builtinmovementsvalidation
  title: Builtinmovementsvalidation
  content_hash: sha256:5d551d9332478d7b524e48d7f8f06715498df9a85e13a9099198266f948a6beb
- id: src-20261011-2026-10-11-spider-validated
  resource: urn:llmwiki:source:src-20261011-2026-10-11-spider-validated
  title: 2026 10 11 Spider Validated
  content_hash: sha256:66fbb23415a3ac62be62f096b6fb7bd5ba400538dabe8a29442f92c50d64847e
semantic_review:
  version: 1
  performed_by: agent:codex
  performed_at: '2026-10-11T14:26:52.015630+00:00'
  target_hash: sha256:b4190f443ad7b41d25228d07f3837427f045235eca99a382cd07d1f1f880a81b
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Replacement claims reviewed against the registered new evidence, exact owner-source/resource/document
    parity and 146 host tests. Older trajectory statements are explicitly historical;
    unchanged managed values migrate and edits persist. Prior review by agent:antigravity
    at 2026-10-09T17:10:48.021602+00:00 remains provenance for retained historical/context
    claims; this update does not rerun their unrelated validation.
  - Draft/unverified status remains. Owner-reported movement validation is attributed;
    no new physical, visual or human wiki verification event is asserted.
---

# Spider OTTO waypoint library and native movement integration

The original research repository asset `ninja_core/movements/spider_otto.json` contains 19 named entries (565 steps), covering 16 OTTO methods and selected direction variants. `scripts/build_spider_movements.py` regenerates it offline; `--check` verifies exact bytes. No existing movement-control function, driver, API, live config, calibration or original OTTO source was changed.[^src-20261009-2026-10-09-spider-otto]

## Native built-in movement integration and robot profile scoping

In the initial 2026-10-09 native integration, `ninja_core` integrates an installed package resource `data/spider_otto.json` containing the 19 `spider_*` trajectories and `Poweroff` (20 entries, 566 steps). When all BCM GPIO 20–27 are configured, module configuration import (`ninja_core config import`) automatically seeds these 20 entries into the Spider profile.[^src-20261009-2026-10-09-builtin-movements]

The implementation plan establishes profile reconciliation and non-destructive built-in seeding.[^src-20261009-builtinmovementsimplementationplan] By owner confirmation, the Wheel and Humanoid robot profiles receive only an all-configured-servo center movement named `home` (commanding all configured servos to 0° at Slow speed); other default gaits will be implemented later.[^src-20261009-2026-10-09-builtin-movements] Wheel inputs normalize to the canonical `tire` configuration value.[^src-20261009-2026-10-09-builtin-movements]

Additive metadata `movement_robot_types` scopes imported movements to their robot type, and `builtin_movement_hashes` preserves user edits or custom collisions during reimport or type changes. Only unchanged managed values are automatically removed or replaced; custom or edited entries are preserved.[^src-20261009-2026-10-09-builtin-movements]

## Preflight validation and execution guards

`MovementController` enforces strict preflight validation before the first actuator write: every step is verified for canonical GPIO keys within BCM 0–27, available channels, finite nominal ±90° angles, valid speed modes (F/M/S), and valid per-servo overrides. Any malformed later step causes the entire movement to abort before beginning.[^src-20261009-2026-10-09-builtin-movements]

The controller serializes its operations with an execution lock and performs callback checks before and after blocking driver steps. A driver abort halts sequence advancement without issuing an unsolicited controller recovery pose.[^src-20261009-2026-10-09-builtin-movements]

## Use with the existing executor

Each movement is an ordered list of `moves` plus `speed`; existing optional `per_servo_speeds` overrides a commanded GPIO's mode. GPIO keys are strings in JSON. Missing targets receive no new command. Modes F/M/S select nominal velocity rather than duration. The driver starts one elapsed-time loop but joints have independent arrival times; each step waits for the slowest. No explicit period or pause field is consumed.[^src-20261009-2026-10-09-spider-otto]

## Mapping and coverage

The owner-corrected source mapping is S0→GPIO25, S1→24, S2→27, S3→26, S4→21, S5→20, S6→23, S7→22 (BCM numbers). Nominal conversion is source q−90 degrees. OTTO's own S2 reversal and EEPROM trim are not evidence for a Pi0 inversion; target mounting/clearance is unverified.[^src-20261009-2026-10-09-spider-otto]

The original research pack covers home, hide, run forward/backward, turn left/right, dance, front-back, up-down, push-up, wave-hand, moonwalk-left, omni true/false at factor2, walk forward/backward, jump, scared and hello. Each periodic entry uses 37 endpoint-inclusive samples at native M; source periods are provenance, not preserved timing. Walk feet have twice the hip frequency. Default omni variants have equal ideal waveforms. Jump/scared pauses are unavailable. Hello is only a representative adaptation of state-dependent buggy helpers and a clipped wave; it is not an exact behavioral port.[^src-20261009-2026-10-09-spider-otto]

## Separate future controller

`DevelopmentPlanDoc/Pi0BuildinMovementsRefinement.md` proposes a distinct versioned registry/controller for timed poses, cancellable dwells and analytic amplitude/offset/phase/period actions. These fields and APIs are not implemented or accepted by the existing executor. Feasibility depends on strict limits, a shared monotonic clock, cancellation and exclusive servo ownership across native/Blockly/web writers. Calling the old blocking interpolation loop per sample would distort timing and reset abort flags.[^src-20261009-2026-10-09-spider-otto]

Oscillator peak velocity is `2*pi*abs(A)/Tseconds`. OTTO walking feet (20 degrees, 275 ms) require about 456.96 degrees/second, above hypothetical M-at-80-percent nominal 360. A new controller should reject or explicitly stretch coupled timing together, then require physical validation. Passing a software limit is not proof of physical feasibility.[^src-20261009-2026-10-09-spider-otto]

## Validation and limitations

Host validation on Raspberry Pi Zero 2 W with inert drivers confirmed full trajectory parity, preflight validation, type switching, reimport idempotency, and web/CLI error reporting (42 final feature tests passed, exit 0).[^src-20261009-builtinmovementsvalidation] In-step callback interruption remains limited by the blocking driver loop. Real hardware mapping, direction, clearance, balance, power, timing, and stopping acceptance remain pending.[^src-20261009-builtinmovementsvalidation]

See [Motion system and easing](/concepts/motion-system-and-easing.md), [Current development manual](/references/development-guide.md) and [Development history](/analyses/development-history-and-evolution.md).

[^src-20261009-2026-10-09-spider-otto]: Registered 2026-10-09 Spider implementation and code evidence; measured direction, clearance, power, load, timing and stopping remain pending.
[^src-20261009-2026-10-09-builtin-movements]: Automatic native built-in movement evidence and architecture boundaries.
[^src-20261009-builtinmovementsvalidation]: Built-in movement validation on Raspberry Pi Zero 2 W with inert hardware.

[^src-20261009-builtinmovementsimplementationplan]: Implementation plan for automatic native built-in movements and profile reconciliation, 2026-10-09.


## Current owner-validated catalog replacement (2026-10-11)

The installed `ninja_core/src/ninja_core/data/spider_otto.json` now uses the exact 20 movement definitions and 566 steps supplied by the owner in `DevelopmentPlanDoc/spider_movement.json`. The source is a movements-key fragment; the installed resource adds only enclosing braces and `robot_type: spider`. `spider_moonwalk_right` replaces the earlier left-labelled name; six run/walk/turn definitions use the owner's revised direction choices. `Poweroff` is preserved exactly. No `Wave_Left_Hand` is added. The original research pack/generator remain historical and do not regenerate the installed resource.[^src-20261011-2026-10-11-spider-validated]

Existing config import/load reconciliation replaces unchanged managed definitions, removes the unchanged managed old moonwalk name and seeds the new one, while preserving custom edits and collisions. The loader, controllers and calibration are unchanged. Deploy the updated package and restart/reload through the normal workflow; this task did not overwrite live configuration or operate hardware. A same-name user-edited entry may retain its prior value.[^src-20261011-2026-10-11-spider-validated]

The movement document's 20 inline JSON blocks equal the installed data and supplied source. Host validation passed 146 targeted tests, including every current movement with inert output and old-managed-catalog migration with edited/custom data preservation. Ruff and protected-core checks passed. The owner reports validation, but this update performs no additional physical or Pi acceptance. Timing/pause semantics remain unchanged.[^src-20261011-2026-10-11-spider-validated]

[^src-20261011-2026-10-11-spider-validated]: Owner-requested Spider data replacement, exact source parity and host validation evidence.
