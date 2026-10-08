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
- id: src-20261008-developmentlog-4
  title: 'Pi0 development log: multilingual manual audit'
  content_hash: sha256:5f036bf4ec4a29be102c9bcbf0a1749ab31975702de8a83979fe8155d4cf45c4
  resource: urn:llmwiki:source:src-20261008-developmentlog-4
- id: src-20261007-2026-10-07-install-onboard-wiki-ui-2
  resource: urn:llmwiki:source:src-20261007-2026-10-07-install-onboard-wiki-ui-2
  title: Pi0 upgrade implementation and current UI contracts
  content_hash: sha256:1545ea683947c315a9ea0d4c30258c228e975a78e39062b2e045669fcff0cb9c
- id: src-20261007-2026-10-08-upgrade-audit
  resource: urn:llmwiki:source:src-20261007-2026-10-08-upgrade-audit
  title: Pi0 upgrade audit findings and boundaries
  content_hash: sha256:7112a6575c6288875e3fdad33679f094b22908e0ee729b29f5dfbfc55f48de64
- id: src-20261008-2026-10-08-trixie-support
  resource: urn:llmwiki:source:src-20261008-2026-10-08-trixie-support
  title: Trixie installer correction and validation boundary
  content_hash: sha256:3aae04cfab13e782c5748e8ca26721d860d0d842ac18c5544fd8ae0f82dc2945
- id: src-20261008-2026-10-08-installer-recovery
  resource: urn:llmwiki:source:src-20261008-2026-10-08-installer-recovery
  title: Installer diagnostics and recovery validation
  content_hash: sha256:416eea41c04d6dc6ed633fa695b276a48574d22eacb21db5131de3577dbe4fc3
- id: src-20261008-2026-10-08-installer-compatibility
  resource: urn:llmwiki:source:src-20261008-2026-10-08-installer-compatibility
  title: 2026 10 08 Installer Compatibility
  content_hash: sha256:7eaa21e7a1f79122e25e10dc37ae91a488aebe3ccff9db5e6c7b59db0684928f
- id: src-20261008-2026-10-08-readme-audit
  title: Pi0 README audit evidence and validation limits
  content_hash: sha256:7a945023f45ad2e179e5cae529665df9ed050bfe5cf36f440f857a02e28cfea4
  resource: urn:llmwiki:source:src-20261008-2026-10-08-readme-audit
semantic_review:
  version: 1
  performed_by: agent:codex
  performed_at: '2026-10-08T14:34:39.927213+00:00'
  target_hash: sha256:13ad720c9d6cdd702a1c037cba171badcfb74eda9459fca7ee56891e08586959
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed the owner-authored four-language README and registered audit evidence
    against installer preflight, service-manager uv/PATH and enable behavior, ngrok
    presence/connection checks, core movement parser, GPIO terminology and shutdown
    permission/animation limits. Corrections retain the manual structure; optional
    recovery/status details remain in Troubleshooting/Appendix C. All 54 shell examples
    parse and four isolated core parser examples pass. No runtime code or physical
    hardware operation is claimed. Earlier historical sources remain cited; draft/unverified
    status is preserved.
  - Source-grounded AI review of changed claims and retained cited context; draft/unverified.
    Physical tests, live accounts and publication remain pending.
---

# Development History and Evolution

## 2026-10-07 implementation checkpoint

Approved installation/onboarding tooling, wiki relocation and immutable manual workflow, and Pi5-derived Pi0 web presentation were implemented with host validation. Historical V5 milestones remain history. Real Raspberry Pi and live account validation remain owner-manual; no release publication occurred during this task.[^src-20261008-developmentlog-4]


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

[^src-20261008-developmentlog-4]: Current versioned Developmentlog.

## Implementation evidence and acceptance limits

Host validation and the exact code/tooling boundary are recorded in the approved implementation evidence. Real Pi hardware, live accounts and published curl acceptance remain pending; passing host checks do not imply physical acceptance.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.


## Historical 2026-10-08 audit follow-up (superseded policy)

The following records the earlier implementation; current compatibility policy below supersedes exact-version, codename and private-tool-precedence claims.

The 2026-10-08 follow-up audit corrected onboarding validation/privacy/progress/retry, installer preflight/provenance handling and wiki environment isolation. It rewrote the public README and created new immutable manuals/evidence. Host checks do not substitute for physical Pi, live accounts, remote CI or publication; no core robot code was changed.[^src-20261007-2026-10-08-upgrade-audit]

[^src-20261007-2026-10-08-upgrade-audit]: Pi0 upgrade audit findings and boundaries.


## Historical Trixie support correction (superseded policy)

The following records the earlier implementation; current compatibility policy below supersedes exact-version, codename and private-tool-precedence claims.

The owner reported the published bootstrap rejecting Debian 13/trixie. A follow-up corrected both release gates and expanded interpreter CI while preserving robot source and locks. This correction is local until publication; physical Trixie acceptance is still pending.[^src-20261008-2026-10-08-trixie-support]

[^src-20261008-2026-10-08-trixie-support]: Trixie installer correction and validation boundary.


## Historical Installation recovery and diagnostics (superseded policy)

The following records the earlier implementation; current compatibility policy below supersedes exact-version, codename and private-tool-precedence claims.

A follow-up request clarified checkout updates versus software installation. The installer gained actionable read-only diagnostics, visible stages and failure/retry messages. Documentation includes fast-forward default-HEAD updates for existing detached clones. Real Pi follow-up remains pending; no automatic publication or hardware operation occurred.[^src-20261008-2026-10-08-installer-recovery]

[^src-20261008-2026-10-08-installer-recovery]: Installer diagnostics and recovery validation.


## Current software compatibility policy

After the earlier Bookworm/Trixie and diagnostic fixes, the owner requested genuine minimum/capability checks. The follow-up removes exact Node/uv equality and OS codename gates, reuses compatible tools and retains checked download fallbacks. A real uv 0.9.26 offline host dry-run read the unchanged lockfile. No Pi installation, hardware activation or publication is claimed.[^src-20261008-2026-10-08-installer-compatibility]

[^src-20261008-2026-10-08-installer-compatibility]: Installer compatibility requirements and validation evidence.


## Multilingual user manual audit

The owner supplied an expanded four-language README and requested a narrow correctness audit. Corrections preserved its sections and intentional omissions, moved recovery/optional checks to troubleshooting/appendices, and translated the copied Traditional Chinese autostart prose into Simplified Chinese. All 54 shell blocks parsed and four movement examples passed the isolated core parser; command parity, links and core protection checks passed. No installation, service, hardware or live account operation occurred.[^src-20261008-2026-10-08-readme-audit]

[^src-20261008-2026-10-08-readme-audit]: Four-language README correctness audit and code evidence.
