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
---

# Motion System and Easing Curves

The NinjaRobotPi0 motion system uses velocity-based control rather than fixed-duration steps and is designed for smooth movement across up to 8 servo motors.[^src-20260822-readme-7] [^src-20260822-developmentguide]

## Velocity-Based Control Architecture

The legacy NinjaRobot motion path used fixed delays between target positions.[^src-20260822-developmentguide] The rebuilt `pi0servo` instead computes step deltas from target angular velocity (°/sec) and a fixed **100Hz update frequency** (10ms step intervals):[^src-20260822-readme-7]

* **Speed Modes**:
  * `F` (Fast): Maximum velocity for rapid gestures.[^src-20260822-readme-7]
  * `M` (Medium): Balanced speed (default).[^src-20260822-readme-7]
  * `S` (Slow): Gentle, high-torque positioning.[^src-20260822-readme-7]
* **Per-Servo Speed Limits**: Configurable in `servo.json` (0–100%) to protect delicate mechanical linkages.[^src-20260822-readme-7]
* **Thread-Safe Abort**: Calling `ServoGroup.abort()` signals active trajectory loops to terminate from external event threads or safety monitors.[^src-20260822-readme-7]

## Position-Aware Multi-Step Easing

In multi-step sequence playbacks (e.g., walking or waving), traditional easing causes awkward stop-start hesitations between waypoints.[^src-20260822-readme-3] [^src-20260822-developmentguide] `MovementController` solves this by applying **position-aware easing**:[^src-20260822-readme-3] [^src-20260822-developmentguide]

```
Sequence Step:    [ Step 1 (Start) ]  ──▶  [ Step 2..N-1 (Waypoints) ]  ──▶  [ Step N (End) ]
Applied Easing:     ease_in_cubic                   linear                     ease_out_cubic
Behavior:          Accelerate only             Constant velocity             Decelerate to stop
```

This preserves momentum across waypoints and creates fluid, organic motion.[^src-20260822-readme-3]

## Movement Command Syntax

Motion steps are defined using a compact string syntax supported by CLI tools and the web interface:[^src-20260822-readme-7] [^src-20260822-readme-3]

```
[GLOBAL_SPEED_]PIN:ANGLE[LOCAL_SPEED][/PIN:ANGLE[LOCAL_SPEED]...]
```

* **Basic Move**: `20:45` (move GPIO 20 to 45° at Medium speed).[^src-20260822-readme-7]
* **Angle Keywords**: `C` (Center, 0°), `M` (Min, -90°), `X` (Max, 90°).[^src-20260822-readme-3]
* **Multi-Servo Step**: `M_20:45/21:-30/22:C` (simultaneous move across 3 servos).[^src-20260822-readme-7]
* **Speed Overrides**: `S_20:C/21:XF` (global Slow, but pin 21 moves Fast).[^src-20260822-readme-7]
* **Position Auto-Completion**: If a servo pin is omitted in a step, it retains its previous angle, allowing concise sequence scripts.[^src-20260822-readme-3]

[^src-20260822-readme-7]: pi0servo Readme.
[^src-20260822-readme-3]: ninja_core Readme.
[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.
