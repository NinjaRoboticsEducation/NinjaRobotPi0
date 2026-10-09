---
type: Concept
title: Motion System and Easing Curves
description: Velocity-based physics motion calculations, position-aware easing curves,
  and the movement command syntax.
status: draft
generated:
  by: codex/migration-audit
  at: '2026-10-07T07:13:37.354382+00:00'
sources:
- id: src-20260822-readme-7
  resource: urn:llmwiki:source:src-20260822-readme-7
  title: pi0servo Readme
  content_hash: sha256:23793729576aa0b8f5b460d7fe4e47ab1d7ad4f9a6af4348bf4c8208a6610a76
- id: src-20260822-readme-3
  resource: urn:llmwiki:source:src-20260822-readme-3
  title: ninja_core Readme
  content_hash: sha256:502427fd1c9031fea178cc56a037d30e880c5b5c78875618d2ab173a8543d2df
- id: src-20260822-developmentguide
  resource: urn:llmwiki:source:src-20260822-developmentguide
  title: NinjaRobotPi0 Development Guide
  content_hash: sha256:d1f8e19627223cb320b2e05df9a141c768ca0f418a7f77d160b6127d08c439e9
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
- id: src-20261009-2026-10-09-spider-otto
  resource: urn:llmwiki:source:src-20261009-2026-10-09-spider-otto
  title: 2026 10 09 Spider Otto
  content_hash: sha256:1c35301cb86c71126d626d841c5f648680fb82c8fe857526e22b983e970939cd
semantic_review:
  version: 1
  performed_by: agent:codex
  performed_at: '2026-10-09T07:08:20.155374+00:00'
  target_hash: sha256:5d8d384eef0435287cb38e7c6935dcc9a621a50b23980e206986f2805e19e48f
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed registered pi0servo/core README sources, development guide motion sections,
    migration note and new code-grounded Spider evidence. Corrected overstrong timing,
    torque/protection, momentum and publication wording. JSON fields, independent
    arrival, easing, nominal velocity and cancellation caveats agree with current
    code; older source claims are explicitly limited by new evidence.
  - Source-grounded AI review, with retained-context reader review where applicable.
    Draft/unverified status remains; no human, visual, physical or remote-publication
    verification is asserted.
---

# Motion System and Easing Curves

The NinjaRobotPi0 motion system uses velocity-based control rather than fixed-duration steps and is designed for smooth movement across up to 8 servo motors.[^src-20260822-readme-7] [^src-20260822-developmentguide]

## Velocity-Based Control Architecture

The legacy NinjaRobot motion path used fixed delays between target positions.[^src-20260822-developmentguide] The rebuilt `pi0servo` instead computes step deltas from target angular velocity (°/sec) and a nominal **10ms software step interval** (not a hard real-time 100Hz guarantee):[^src-20260822-readme-7][^src-20261009-2026-10-09-spider-otto]

* **Speed Modes**:
  * `F` (Fast): Maximum velocity for rapid gestures.[^src-20260822-readme-7]
  * `M` (Medium): Balanced speed (default).[^src-20260822-readme-7]
  * `S` (Slow): Lower nominal velocity; this mode does not establish motor torque.[^src-20260822-readme-7][^src-20261009-2026-10-09-spider-otto]
* **Per-Servo Speed Limits**: Configurable in `servo.json` (0–100%) as nominal velocity inputs; they are not proof of mechanical protection.[^src-20260822-readme-7][^src-20261009-2026-10-09-spider-otto]
* **Thread-Safe Abort**: Calling `ServoGroup.abort()` signals active trajectory loops to terminate from external event threads or safety monitors.[^src-20260822-readme-7]

## Position-Aware Multi-Step Easing

In multi-step sequence playbacks (e.g., walking or waving), traditional easing causes awkward stop-start hesitations between waypoints.[^src-20260822-readme-3] [^src-20260822-developmentguide] `MovementController` solves this by applying **position-aware easing**:[^src-20260822-readme-3] [^src-20260822-developmentguide]

```
Sequence Step:    [ Step 1 (Start) ]  ──▶  [ Step 2..N-1 (Waypoints) ]  ──▶  [ Step N (End) ]
Applied Easing:     ease_in_cubic                   linear                     ease_out_cubic
Behavior:          Accelerate only             Constant velocity             Decelerate to stop
```

This chooses different interpolation curves at the ends of a sequence. It does not guarantee continuous velocity or physical momentum across waypoints: individual joints have different durations and the next step waits for the slowest.[^src-20261009-2026-10-09-spider-otto]

## Movement Command Syntax

Motion steps are defined using a compact string syntax supported by CLI tools and the web interface:[^src-20260822-readme-7] [^src-20260822-readme-3]

```
[GLOBAL_SPEED_]PIN:ANGLE[LOCAL_SPEED][/PIN:ANGLE[LOCAL_SPEED]...]
```

* **Basic Move**: `20:45` (move GPIO 20 to 45° at Medium speed).[^src-20260822-readme-7]
* **Angle Keywords**: `C` (Center, 0°), `M` (Min, -90°), `X` (Max, 90°).[^src-20260822-readme-3]
* **Multi-Servo Step**: `M_20:45/21:-30/22:C` (one batch across 3 servos; arrival times may differ).[^src-20260822-readme-7][^src-20261009-2026-10-09-spider-otto]
* **Speed Overrides**: `S_20:C/21:XF` (global Slow, but pin 21 moves Fast).[^src-20260822-readme-7]
* **Position Auto-Completion**: If a servo pin is omitted in a step, it retains its previous angle, allowing concise sequence scripts.[^src-20260822-readme-3]

[^src-20260822-readme-7]: pi0servo Readme.
[^src-20260822-readme-3]: ninja_core Readme.
[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.

## Repository migration (2026-10-07)

The migration evidence records the local rename to `NinjaRobotPi0/` and the intended destination [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0), with fresh history on `main` and retained Python packages/runtime. That evidence leaves publication and remote default-branch verification pending. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.


## Verified JSON movement contract and Spider adaptation

`MovementController.execute_movement` reads required `moves` (GPIO-to-angle object) and `speed` (F/M/S), plus optional `per_servo_speeds`. It orders targets by driver pins; an omitted pin receives `None`, an unknown pin is silently omitted, and a per-pin mode overrides the global mode. Single-step easing is in/out cubic. Config validates only the outer movement dictionary/list shape.[^src-20261009-2026-10-09-spider-otto]

`move_all_sync` uses one elapsed clock with independent joint durations, calculated as distance divided by `600 × speed_percent/100 × mode_multiplier` (F=1, M=.75, S=.5). The 600 degrees/second constant is nominal, not measured; easing changes peak velocity. Zero calculated velocity gives zero duration, not a stop. Current JSON has no consumed duration, pause, period or repetition field.[^src-20261009-2026-10-09-spider-otto]

Cancellation also has a boundary: the controller does not poll or forward `abort_check`. An unsuccessful driver result with a callback present triggers centering and EmergencyStop; without one it can advance. Driver moves clear their own abort flags on entry. Do not infer a universal emergency-stop guarantee from the lower-level abort method.[^src-20261009-2026-10-09-spider-otto]

The [Spider OTTO library](/concepts/spider-otto-waypoint-library.md) preserves nominal sampled poses using current fields. Exact timing requires the separately proposed controller; it is not implemented. All physical timing, mounting and loading checks remain pending.[^src-20261009-2026-10-09-spider-otto]

[^src-20261009-2026-10-09-spider-otto]: Code-verified movement contract and Spider adaptation evidence, 2026-10-09; supersedes stronger historical timing/protection wording.
