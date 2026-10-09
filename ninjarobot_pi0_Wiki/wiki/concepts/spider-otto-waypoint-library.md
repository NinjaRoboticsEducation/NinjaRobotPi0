---
type: Concept
title: Spider OTTO waypoint library and timing proposal
description: Opt-in current-schema Spider movements, verified speed semantics and
  a separate future timed controller.
status: draft
generated:
  by: agent:codex
  at: '2026-10-09T06:57:52.051688+00:00'
sources:
- id: src-20261009-2026-10-09-spider-otto
  resource: urn:llmwiki:source:src-20261009-2026-10-09-spider-otto
  title: 2026 10 09 Spider Otto
  content_hash: sha256:1c35301cb86c71126d626d841c5f648680fb82c8fe857526e22b983e970939cd
semantic_review:
  version: 1
  performed_by: agent:codex
  performed_at: '2026-10-09T07:08:20.155374+00:00'
  target_hash: sha256:a65328400f95718e275a7a748e1aa7d10613d52b633e54933a71c2b38c9baa04
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed the registered Spider evidence against the pack/generator, actual loader/controller
    tests and both design documents. Mapping, 19 entries/16 methods/565 steps, M default,
    partial hello, lost source timing and proposed scheduler boundary are supported.
    The mathematical velocity example is command-space analysis, not physical validation.
  - Source-grounded AI review, with retained-context reader review where applicable.
    Draft/unverified status remains; no human, visual, physical or remote-publication
    verification is asserted.
---

# Spider OTTO waypoint library and timing proposal

The implemented repository asset `ninja_core/movements/spider_otto.json` contains 19 named entries (565 steps), covering 16 OTTO methods and selected direction variants. `scripts/build_spider_movements.py` regenerates it offline; `--check` verifies exact bytes. No existing movement-control function, driver, API, live config, calibration or original OTTO source was changed.[^src-20261009-2026-10-09-spider-otto]

## Use with the existing executor

Each movement is an ordered list of `moves` plus `speed`; existing optional `per_servo_speeds` overrides a commanded GPIO's mode. GPIO keys are strings in JSON. Missing targets receive no new command. Modes F/M/S select nominal velocity rather than duration. The driver starts one elapsed-time loop but joints have independent arrival times; each step waits for the slowest. No explicit period or pause field is consumed.[^src-20261009-2026-10-09-spider-otto]

The pack is not automatically discovered, installed as package data or merged into runtime config. It has no servo calibration. `DevelopmentPlanDoc/SpiderBuildinMovements.md` documents loader-compatible examples and an offline preview merge that preserves existing settings and rejects name collisions. Actual calibrated hardware setup and deployment remain deliberate separate steps.[^src-20261009-2026-10-09-spider-otto]

## Mapping and coverage

The owner-corrected source mapping is S0→GPIO25, S1→24, S2→27, S3→26, S4→21, S5→20, S6→23, S7→22 (BCM numbers). Nominal conversion is source q−90 degrees. OTTO's own S2 reversal and EEPROM trim are not evidence for a Pi0 inversion; target mounting/clearance is unverified.[^src-20261009-2026-10-09-spider-otto]

The pack covers home, hide, run forward/backward, turn left/right, dance, front-back, up-down, push-up, wave-hand, moonwalk-left, omni true/false at factor2, walk forward/backward, jump, scared and hello. Each periodic entry uses 37 endpoint-inclusive samples at native M; source periods are provenance, not preserved timing. Walk feet have twice the hip frequency. Default omni variants have equal ideal waveforms. Jump/scared pauses are unavailable. Hello is only a representative adaptation of state-dependent buggy helpers and a clipped wave; it is not an exact behavioral port.[^src-20261009-2026-10-09-spider-otto]

## Separate future controller

`DevelopmentPlanDoc/Pi0BuildinMovementsRefinement.md` proposes a distinct versioned registry/controller for timed poses, cancellable dwells and analytic amplitude/offset/phase/period actions. These fields and APIs are not implemented or accepted by the existing executor. Feasibility depends on strict limits, a shared monotonic clock, cancellation and exclusive servo ownership across native/Blockly/web writers. Calling the old blocking interpolation loop per sample would distort timing and reset abort flags.[^src-20261009-2026-10-09-spider-otto]

Oscillator peak velocity is `2*pi*abs(A)/Tseconds`. OTTO walking feet (20 degrees, 275 ms) require about 456.96 degrees/second, above hypothetical M-at-80-percent nominal 360. A new controller should reject or explicitly stretch coupled timing together, then require physical validation. Passing a software limit is not proof of physical feasibility.[^src-20261009-2026-10-09-spider-otto]

## Validation and limitations

Seventy-one targeted host tests passed, using the actual config loader/executor with an inert shuffled servo group, including every waypoint, mapping, modes, easing and source landmarks. Ruff, generator reproducibility and protected-core checks passed. Existing callback cancellation limitations remain. No installation, servo actuation, Pi execution, dynamics simulation or physical acceptance is claimed.[^src-20261009-2026-10-09-spider-otto]

See [Motion system and easing](/concepts/motion-system-and-easing.md), [Current development manual](/references/development-guide.md) and [Development history](/analyses/development-history-and-evolution.md).

[^src-20261009-2026-10-09-spider-otto]: Registered 2026-10-09 Spider implementation and code evidence; measured direction, clearance, power, load, timing and stopping remain pending.
