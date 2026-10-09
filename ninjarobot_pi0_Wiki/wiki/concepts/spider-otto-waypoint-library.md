---
type: Concept
title: Spider OTTO waypoint library and native movement integration
description: Installed Spider movements, native execution preflights, and profile reconciliation.
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
semantic_review:
  version: 1
  performed_by: agent:antigravity
  performed_at: '2026-10-09T17:10:48.021602+00:00'
  target_hash: sha256:fb77dee3794994a67495b192f2c5c44efa7215284d14d0fbe4a624aaff454901
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed native Spider OTTO pack against package asset data/spider_otto.json, builtin_movements.py, and test_builtin_movements.py. Seeding (20 entries, 566 steps), BCM 0–27 channel preflights, mode overrides, and inert Pi Zero 2 W host validation (42 passes) are supported.
  - Absolute terms ('every', 'all') reflect code-level preflight validation; physical balance, dynamic clearance, and real servo load acceptance remain pending.
---

# Spider OTTO waypoint library and native movement integration

The implemented repository asset `ninja_core/movements/spider_otto.json` contains 19 named entries (565 steps), covering 16 OTTO methods and selected direction variants. `scripts/build_spider_movements.py` regenerates it offline; `--check` verifies exact bytes. No existing movement-control function, driver, API, live config, calibration or original OTTO source was changed.[^src-20261009-2026-10-09-spider-otto]

## Native built-in movement integration and robot profile scoping

Following the initial opt-in repository pack, `ninja_core` integrates an installed package resource `data/spider_otto.json` containing the 19 `spider_*` trajectories and `Poweroff` (20 entries, 566 steps). When all BCM GPIO 20–27 are configured, module configuration import (`ninja_core config import`) automatically seeds these 20 entries into the Spider profile.[^src-20261009-2026-10-09-builtin-movements]

The implementation plan establishes profile reconciliation and non-destructive built-in seeding.[^src-20261009-builtinmovementsimplementationplan] By owner confirmation, the Wheel and Humanoid robot profiles receive only an all-configured-servo center movement named `home` (commanding all configured servos to 0° at Slow speed); other default gaits will be implemented later.[^src-20261009-2026-10-09-builtin-movements] Wheel inputs normalize to the canonical `tire` configuration value.[^src-20261009-2026-10-09-builtin-movements]

Additive metadata `movement_robot_types` scopes imported movements to their robot type, and `builtin_movement_hashes` preserves user edits or custom collisions during reimport or type changes. Only unchanged managed values are automatically removed or replaced; custom or edited entries are preserved.[^src-20261009-2026-10-09-builtin-movements]

## Preflight validation and execution guards

`MovementController` enforces strict preflight validation before the first actuator write: every step is verified for canonical GPIO keys within BCM 0–27, available channels, finite nominal ±90° angles, valid speed modes (F/M/S), and valid per-servo overrides. Any malformed later step causes the entire movement to abort before beginning.[^src-20261009-2026-10-09-builtin-movements]

The controller serializes its operations with an execution lock and performs callback checks before and after blocking driver steps. A driver abort halts sequence advancement without issuing an unsolicited controller recovery pose.[^src-20261009-2026-10-09-builtin-movements]

## Use with the existing executor

Each movement is an ordered list of `moves` plus `speed`; existing optional `per_servo_speeds` overrides a commanded GPIO's mode. GPIO keys are strings in JSON. Missing targets receive no new command. Modes F/M/S select nominal velocity rather than duration. The driver starts one elapsed-time loop but joints have independent arrival times; each step waits for the slowest. No explicit period or pause field is consumed.[^src-20261009-2026-10-09-spider-otto]

## Mapping and coverage

The owner-corrected source mapping is S0→GPIO25, S1→24, S2→27, S3→26, S4→21, S5→20, S6→23, S7→22 (BCM numbers). Nominal conversion is source q−90 degrees. OTTO's own S2 reversal and EEPROM trim are not evidence for a Pi0 inversion; target mounting/clearance is unverified.[^src-20261009-2026-10-09-spider-otto]

The pack covers home, hide, run forward/backward, turn left/right, dance, front-back, up-down, push-up, wave-hand, moonwalk-left, omni true/false at factor2, walk forward/backward, jump, scared and hello. Each periodic entry uses 37 endpoint-inclusive samples at native M; source periods are provenance, not preserved timing. Walk feet have twice the hip frequency. Default omni variants have equal ideal waveforms. Jump/scared pauses are unavailable. Hello is only a representative adaptation of state-dependent buggy helpers and a clipped wave; it is not an exact behavioral port.[^src-20261009-2026-10-09-spider-otto]

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
