---
type: Entity
title: pi0servo Package
description: Velocity-based servo control library for SG90/MG90S servos with cubic
  easing and interactive calibration.
status: draft
generated:
  by: codex/migration-audit
  at: '2026-10-07T07:13:37.354382+00:00'
sources:
- id: src-20260822-readme-7
  resource: urn:llmwiki:source:src-20260822-readme-7
  title: pi0servo Readme
  content_hash: sha256:23793729576aa0b8f5b460d7fe4e47ab1d7ad4f9a6af4348bf4c8208a6610a76
- id: src-20260822-developmentguide
  resource: urn:llmwiki:source:src-20260822-developmentguide
  title: NinjaRobotPi0 Development Guide
  content_hash: sha256:d1f8e19627223cb320b2e05df9a141c768ca0f418a7f77d160b6127d08c439e9
- id: src-20260822-projectupgradeplan
  resource: urn:llmwiki:source:src-20260822-projectupgradeplan
  title: NinjaRobotPi0 Project Upgrade Plan
  content_hash: sha256:a3fd621f63d909ebdc02081a0d832b13f872d6e669ae61a7b619adb4130c43f6
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
semantic_review:
  version: 1
  performed_by: agent:antigravity
  performed_at: '2026-10-07T07:47:00+00:00'
  target_hash: sha256:0519533c59294aa7531532e47c0232688957508a4bb441346f532f23bd996a52
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Velocity controller and multi-servo calibration match pi0servo README and ProjectUpgradePlan.
  - Absolute matches ('safe') describe movement abort signaling.
---

# pi0servo Package

`pi0servo` is a velocity-based servo control library designed for Raspberry Pi Zero 2W, controlling up to 8 SG90 or MG90S micro servos.[^src-20260822-readme-7] [^src-20260822-developmentguide]

## Core Features

* **Velocity-Based Calculations**: Angular displacement is calculated per 10ms step (100Hz update rate), reducing dependence on arbitrary fixed delays.[^src-20260822-readme-7]
* **Cubic Easing**: Default `ease_in_out_cubic` provides smooth S-curve acceleration and deceleration.[^src-20260822-readme-7]
* **Per-Servo Speed Limits**: Configurable in `servo.json` (0–100%) to prevent mechanical overshoot and gear wear.[^src-20260822-readme-7]
* **Abort Mechanism**: Thread-safe cancellation signaling for active movements via `ServoGroup.abort()`.[^src-20260822-readme-7]

## Key Classes & Modules

* **`ServoGroup` (`pi0servo.core.multi_servos`)**: Multi-channel controller used by the HAL and providing actuator-compatible lifecycle methods.[^src-20260822-developmentguide]
* **`Servo` (`pi0servo.core.servo`)**: Individual servo channel model with angle-to-pulse interpolation.[^src-20260822-projectupgradeplan]
* **`ConfigManager` (`pi0servo.config.config_manager`)**: Manages `servo.json` calibration profiles.[^src-20260822-readme-7]

## CLI & Calibration TUI

* `uv run pi0servo servo-tool`: Launches the interactive calibration and testing TUI.[^src-20260822-readme-7]
* `uv run pi0servo calib <pin>`: Calibrates Min, Center, and Max pulse widths for a given GPIO pin.[^src-20260822-readme-7]
* `uv run pi0servo cmd "<command>"`: Executes a movement command string (e.g. `F_20:45/21:-30`).[^src-20260822-readme-7]

[^src-20260822-readme-7]: pi0servo Readme.
[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.
[^src-20260822-projectupgradeplan]: NinjaRobotPi0 Project Upgrade Plan.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.
