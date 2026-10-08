---
type: Analysis
title: Development History and Evolution
description: Chronological development history of NinjaRobot V5 across major phases,
  version milestones, and reliability audits.
status: draft
generated:
  by: codex/migration-audit
  at: '2026-10-07T07:13:37.354382+00:00'
sources:
- id: src-20260822-developmentlog
  resource: urn:llmwiki:source:src-20260822-developmentlog
  title: NinjaRobot V5 Development Log
  content_hash: sha256:54cdbd7e50fd0cbfbfaba5073d6ed89379181b78bc3d7267d64518f15e9bfe02
- id: src-20260822-developmentguide
  resource: urn:llmwiki:source:src-20260822-developmentguide
  title: NinjaRobot V5 Development Guide
  content_hash: sha256:d1f8e19627223cb320b2e05df9a141c768ca0f418a7f77d160b6127d08c439e9
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
- id: src-20261007-developmentlog-2
  resource: urn:llmwiki:source:src-20261007-developmentlog-2
  title: Pi0 development log — audit 2026-10-08
  content_hash: sha256:d3cb9f70b8b62cfe3609fb4101897a359cb9a843156f3c2ab6de05df3e02e149
- id: src-20261007-2026-10-07-install-onboard-wiki-ui-2
  resource: urn:llmwiki:source:src-20261007-2026-10-07-install-onboard-wiki-ui-2
  title: Pi0 upgrade implementation and current UI contracts
  content_hash: sha256:1545ea683947c315a9ea0d4c30258c228e975a78e39062b2e045669fcff0cb9c
- id: src-20261007-2026-10-08-upgrade-audit
  resource: urn:llmwiki:source:src-20261007-2026-10-08-upgrade-audit
  title: Pi0 upgrade audit findings and boundaries
  content_hash: sha256:7112a6575c6288875e3fdad33679f094b22908e0ee729b29f5dfbfc55f48de64
semantic_review:
  version: 1
  performed_by: agent:codex
  performed_at: '2026-10-07T17:40:02.420226+00:00'
  target_hash: sha256:1986a7084576416f982774cba2b24aa78e641fae80f33da8df9f30a6ac35b655
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Chronology distinguishes prior implementation from this audit. New complete DevelopmentLog
    records source/code scope and pending physical/account/remote acceptance. No publication
    or human verification invented.
  - Source-grounded AI review of changed claims and retained cited context; draft/unverified.
    Physical tests, live accounts and publication remain pending.
---

# Development History and Evolution

## 2026-10-07 implementation checkpoint

Approved installation/onboarding tooling, wiki relocation and immutable manual workflow, and Pi5-derived Pi0 web presentation were implemented with host validation. Historical V5 milestones remain history. Real Raspberry Pi and live account validation remain owner-manual; no release publication occurred during this task.[^src-20261007-developmentlog-2]


The NinjaRobot project evolved from a monolithic educational robot into the modular, AI-powered NinjaRobot V5 platform.[^src-20260822-developmentguide] This document records the chronological milestones, architectural phases, and reliability audits throughout development.[^src-20260822-developmentlog] [^src-20260822-developmentguide]

## Major Development Phases

* **Phase 1 (Modularity & ABCs)**: Decoupled hardware into independent packages (`pi0servo`, `pi0buzzer`, `pi0disp`, `pi0vl53l0x`, `ninja_utils`) and introduced `Sensor` and `Actuator` ABCs with dynamic HAL loading.[^src-20260822-developmentguide]
* **Phase 2 (Dual Connectivity)**: Implemented `ninja_ble` BLE GATT server and central `CommandDispatcher` in `ninja_core`.[^src-20260822-developmentguide]
* **Phase 3 (Binary Chunking)**: Designed binary packet fragmentation and CRC32 verification for transferring large payloads over BLE.[^src-20260822-developmentguide]
* **Phase 4 (Agent Intelligence & Sandboxing)**: Integrated Google Gemini AI agent and built `SafeExecutor` sandboxed Python runtime.[^src-20260822-developmentguide]
* **Phase 5 (Modern Web Application)**: Developed the React 18 + Vite SPA frontend (`ninja_webapp`) with WebSockets telemetry and multilingual support.[^src-20260822-developmentguide]

## V5.2.x Refinements & Classroom Reliability Chronology

* **V5.2.0 (Graceful Shutdown)**: Added `_perform_shutdown_animation()` executing parallel sleepy face/sound, rest posture, and safe power-off sequence.[^src-20260822-developmentguide]
* **V5.2.1 (pi0servo Integration)**: Rebuilt servo control with velocity-based motion, abort mechanism, and calibration managers.[^src-20260822-developmentguide]
* **V5.2.2 (Movement Fluidity)**: Introduced position-aware multi-step cubic easing (`ease_in_cubic` → `linear` → `ease_out_cubic`).[^src-20260822-developmentguide]
* **V5.2.3 (pi0vl53l0x V2)**: Hardened sensor init, thread-safe I2C, transaction-level locking, and interactive CLI.[^src-20260822-developmentguide]
* **V5.2.4 (pi0disp V2)**: Thread-safe SPI locking, delta rendering with numpy LUT, and `TextTicker`.[^src-20260822-developmentguide]
* **V5.2.5 (Blockly Runtime Reliability)**: AST preflight syntax checking, correlation of events by `request_id`, and distance fallback to `9999`.[^src-20260822-developmentguide] [^src-20260822-developmentlog]
* **V5.2.6 (Dual Pipeline)**: Created `RuntimePipeline` to eliminate expression/display ownership conflicts between native idle and Blockly code.[^src-20260822-developmentguide] [^src-20260822-developmentlog]
* **V5.2.7 (GPIO Motion Contract)**: Added `robot.servos.move_pin()` and `move_pins()` for Blockly code generation.[^src-20260822-developmentguide] [^src-20260822-developmentlog]
* **V5.2.8 (Blockly Text & Music)**: Added multilingual `robot.display.text()` and built-in melody playback in `pi0buzzer`.[^src-20260822-developmentguide] [^src-20260822-developmentlog]
* **V5.2.9 (BLE Robot Naming)**: Added persistent `bluetooth.name` configuration and custom BlueZ advertisement naming.[^src-20260822-developmentguide] [^src-20260822-developmentlog]
* **V5.2.10 (Saved Action Library)**: Implemented `ActionLibrary` for on-robot storage of Code IDE Blockly programs with AI agent replay.[^src-20260822-developmentguide] [^src-20260822-developmentlog]
* **V5.2.11 (Guided Setup & Profile Sync)**: Added `init-tool` CLI and synchronized `robot_info` (robot type, servo pin mappings) over BLE with Code IDE.[^src-20260822-developmentguide] [^src-20260822-developmentlog]
* **V5.2.12 (Gemini Model Selection)**: Replaced the fixed agent model setup with API-key-specific catalog discovery, interactive selection, and backward-compatible `gemini.model` configuration.[^src-20260822-developmentguide] [^src-20260822-developmentlog]
* **V5.2.13 (Gemini 3 Runtime Compatibility)**: Added selection-time generation validation, low-thinking REST generation for Gemini 3, bounded runtime requests, and model-specific diagnostics.[^src-20260822-developmentguide] [^src-20260822-developmentlog]
* **2026-05-17 (Code IDE Assistant Compatibility)**: Audited and synchronized documentation ensuring AI assistant provider keys and comments maintain client-server boundary security.[^src-20260822-developmentlog]

[^src-20260822-developmentlog]: NinjaRobot V5 Development Log.
[^src-20260822-developmentguide]: NinjaRobot V5 Development Guide.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.

[^src-20261007-developmentlog-2]: Current versioned Developmentlog.

## Implementation evidence and acceptance limits

Host validation and the exact code/tooling boundary are recorded in the approved implementation evidence. Real Pi hardware, live accounts and published curl acceptance remain pending; passing host checks do not imply physical acceptance.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.


## 2026-10-08 audit follow-up

The 2026-10-08 follow-up audit corrected onboarding validation/privacy/progress/retry, installer preflight/provenance handling and wiki environment isolation. It rewrote the public README and created new immutable manuals/evidence. Host checks do not substitute for physical Pi, live accounts, remote CI or publication; no core robot code was changed.[^src-20261007-2026-10-08-upgrade-audit]

[^src-20261007-2026-10-08-upgrade-audit]: Pi0 upgrade audit findings and boundaries.
