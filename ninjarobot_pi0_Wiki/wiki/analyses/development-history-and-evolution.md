---
type: Analysis
title: Development History and Evolution
description: Chronological milestones, architectural transitions, and classroom reliability audits.
status: draft
generated:
  by: codex/migration-audit
  at: '2026-10-07T07:13:37.354382+00:00'
sources:
- id: src-20260822-developmentlog
  resource: urn:llmwiki:source:src-20260822-developmentlog
  title: NinjaRobotPi0 Development Log
  content_hash: sha256:54cdbd7e50fd0cbfbfaba5073d6ed89379181b78bc3d7267d64518f15e9bfe02
- id: src-20260822-developmentguide
  resource: urn:llmwiki:source:src-20260822-developmentguide
  title: NinjaRobotPi0 Development Guide
  content_hash: sha256:d1f8e19627223cb320b2e05df9a141c768ca0f418a7f77d160b6127d08c439e9
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
- id: src-20261009-developmentlog
  resource: urn:llmwiki:source:src-20261009-developmentlog
  title: Developmentlog
  content_hash: sha256:26c761085d9ad415c759477dc2e33f92bb3feab89dabf58c917bbae373fb8dcc
- id: src-20261007-2026-10-07-install-onboard-wiki-ui-2
  resource: urn:llmwiki:source:src-20261007-2026-10-07-install-onboard-wiki-ui-2
  title: Pi0 upgrade implementation and current UI contracts
  content_hash: sha256:1545ea683947c315a9ea0d4c30258c228e975a78e39062b2e045669fcff0cb9c
- id: src-20261007-2026-10-08-upgrade-audit
  resource: urn:llmwiki:source:src-20261008-upgrade-audit
  title: Pi0 upgrade audit findings and boundaries
  content_hash: sha256:7112a6575c6288875e3fdad33679f094b22908e0ee729b29f5dfbfc55f48de64
- id: src-20261008-2026-10-08-trixie-support
  resource: urn:llmwiki:source:src-20261008-trixie-support
  title: Trixie installer correction and validation boundary
  content_hash: sha256:3aae04cfab13e782c5748e8ca26721d860d0d842ac18c5544fd8ae0f82dc2945
- id: src-20261008-2026-10-08-installer-recovery
  resource: urn:llmwiki:source:src-20261008-installer-recovery
  title: Installer diagnostics and recovery validation
  content_hash: sha256:416eea41c04d6dc6ed633fa695b276a48574d22eacb21db5131de3577dbe4fc3
- id: src-20261008-2026-10-08-installer-compatibility
  resource: urn:llmwiki:source:src-20261008-installer-compatibility
  title: 2026 10 08 Installer Compatibility
  content_hash: sha256:7eaa21e7a1f79122e25e10dc37ae91a488aebe3ccff9db5e6c7b59db0684928f
- id: src-20261008-2026-10-08-readme-audit
  resource: urn:llmwiki:source:src-20261008-readme-audit
  title: 2026 10 08 Readme Audit
  content_hash: sha256:7a945023f45ad2e179e5cae529665df9ed050bfe5cf36f440f857a02e28cfea4
- id: src-20261009-2026-10-09-spider-otto
  resource: urn:llmwiki:source:src-20261009-2026-10-09-spider-otto
  title: 2026 10 09 Spider Otto
  content_hash: sha256:1c35301cb86c71126d626d841c5f648680fb82c8fe857526e22b983e970939cd
- id: src-20261009-2026-10-09-builtin-movements
  resource: urn:llmwiki:source:src-20261009-2026-10-09-builtin-movements
  title: 2026 10 09 Builtin Movements
  content_hash: sha256:6bd14ef705bb60c2c228c95940fd6cb771299532f13e10fdc4faae22db3f216a
- id: src-20261009-developmentlog-2
  resource: urn:llmwiki:source:src-20261009-developmentlog-2
  title: Developmentlog
  content_hash: sha256:d176728a0871bab1ad8a7138df05ca04d87c6782011c7459f49278c07a9c3a88
- id: src-20261009-builtinmovementsvalidation
  resource: urn:llmwiki:source:src-20261009-builtinmovementsvalidation
  title: Builtinmovementsvalidation
  content_hash: sha256:5d551d9332478d7b524e48d7f8f06715498df9a85e13a9099198266f948a6beb
semantic_review:
  version: 1
  performed_by: agent:antigravity
  performed_at: '2026-10-09T17:10:48.021602+00:00'
  target_hash: sha256:4c63758116b7b3319d5a9a6e32f35780933b8146c999ef884292d3750f97ed8f
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed chronological milestones against Git log, development logs, and validation evidence. 2026-10-09 native built-in movements milestone, packaging, and inert Pi Zero 2 W host tests are supported.
  - Historical milestones remain provenance; host test passes do not imply physical robot acceptance.
---

# Development History and Evolution

## 2026-10-07 implementation checkpoint

Approved installation/onboarding tooling, wiki relocation and immutable manual workflow, and Pi5-derived Pi0 web presentation were implemented with host validation. Historical V5 milestones remain history. Real Raspberry Pi and live account validation remain owner-manual; no release publication occurred during this task.[^src-20261009-developmentlog]


The NinjaRobot project evolved from a monolithic educational robot into the modular, AI-powered NinjaRobot V5 platform.[^src-20260822-developmentguide] This document records the chronological milestones, architectural phases, and reliability audits throughout development.[^src-20260822-developmentlog] [^src-20260822-developmentguide]

## Major Development Phases

* **Phase 1 (Modularity & ABCs)**: Decoupled hardware into independent packages (`pi0servo`, `pi0buzzer`, `pi0disp`, `pi0vl53l0x`, `ninja_utils`) and introduced `Sensor` and `Actuator` ABCs with dynamic HAL loading.[^src-20260822-developmentguide]
* **Phase 2 (Dual Connectivity)**: Implemented `ninja_ble` BLE GATT server and central `CommandDispatcher` in `ninja_core`.[^src-20260822-developmentguide]
* **Phase 3 (Binary Chunking)**: Designed binary packet fragmentation and CRC32 verification for transferring large payloads over BLE.[^src-20260822-developmentlog]
* **Phase 4 (Agent Intelligence & Sandboxing)**: Integrated Google Gemini AI agent and built `SafeExecutor` sandboxed Python runtime.[^src-20260822-developmentguide]
* **Phase 5 (Modern Web Application)**: Developed the React 18 + Vite SPA frontend (`ninja_webapp`) with WebSockets telemetry and multilingual support.[^src-20260822-developmentguide]

## V5.2.x Refinements & Classroom Reliability Chronology

* **V5.2.0 (Graceful Shutdown)**: Added `_perform_shutdown_animation()` executing parallel sleepy face/sound, rest posture, and safe power-off sequence.[^src-20260822-developmentguide]
* **V5.2.1 (pi0servo Integration)**: Rebuilt servo control with velocity-based motion, abort mechanism, and calibration managers.[^src-20260822-developmentguide]
* **V5.2.2 (Movement Fluidity)**: Introduced position-aware multi-step cubic easing (`ease_in_cubic` → `linear` → `ease_out_cubic`).[^src-20260822-developmentguide]
* **V5.2.3 (pi0vl53l0x V2)**: Hardened sensor init, thread-safe I2C, transaction-level locking, and interactive CLI.[^src-20260822-developmentguide]

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.
[^src-20260822-developmentlog]: NinjaRobotPi0 Development Log.
[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.

[^src-20261009-developmentlog]: Current versioned Developmentlog.

## Implementation evidence and acceptance limits

Host validation and the exact code/tooling boundary are recorded in the approved implementation evidence. Real Pi hardware, live accounts and published curl acceptance remain pending; passing host checks do not imply physical acceptance.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.


## Historical 2026-10-08 audit follow-up (superseded policy)

The following records the earlier implementation; current compatibility policy below supersedes exact-version, codename and private-tool-precedence claims.

The audit strengthens only the external onboarding wrapper: conflicting imported pulse aliases are rejected, credentials are private from first write, and worker execution respects platform preflight. Existing core helpers and runtime are unchanged. Manual server start still initializes hardware and attempts ngrok; onboarding does not add Pi5 authentication or offline isolation.[^src-20261007-2026-10-08-upgrade-audit]

[^src-20261007-2026-10-08-upgrade-audit]: Pi0 upgrade audit findings and boundaries.


## Historical Trixie support correction (superseded policy)

The following records the earlier implementation; current compatibility policy below supersedes exact-version, codename and private-tool-precedence claims.

The owner reported Debian 13/trixie on Zero 2 W. Both bootstrap and shared Python preflight still enforced Bookworm-only. Extended the allowlist to Bookworm/Trixie, retained guards, added regression cases and Python 3.11/3.13 CI. Host validation passed; real Pi validation and publication of this correction remain pending.[^src-20261008-2026-10-08-trixie-support]

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


## Spider OTTO movement data and future timing design (2026-10-09)

An opt-in repository JSON pack adds 19 entries covering 16 source methods and selected variants, with 565 waypoint steps and no existing controller/driver changes. The offline generator, actual config/executor tests and two design documents explain corrected GPIO mapping, native speed modes and lost period/dwell fidelity. Seventy-one targeted host tests, generator verification, Ruff and core protection passed; physical validation remains pending. See [Spider OTTO waypoint library](/concepts/spider-otto-waypoint-library.md) for current behavior and the separate, unimplemented timed-controller proposal.[^src-20261009-2026-10-09-spider-otto]

[^src-20261009-2026-10-09-spider-otto]: Registered Spider implementation, code inspection, host validation and proposal boundaries.

## Automatic native built-in movements and profile reconciliation (2026-10-09)

The owner requested automatic native movement import, CLI/web/agent integration, and wrong-type execution guards. The implementation introduces `ninja_core.builtin_movements` with installed package resource `data/spider_otto.json` providing 19 `spider_*` trajectories and `Poweroff` (20 entries, 566 steps) for Spider when GPIO 20–27 are configured. By owner confirmation, Wheel and Humanoid receive only an all-configured-servo center movement named `home`.[^src-20261009-2026-10-09-builtin-movements] [^src-20261009-developmentlog-2]

Additive metadata `movement_robot_types` and `builtin_movement_hashes` ensure idempotent reimport and preserve user customizations or name collisions. Controller preflight validates every step before servo writes, the controller lock serializes operations, and boundary callback checks halt advancing on driver abort. Automated testing on Raspberry Pi Zero 2 W with inert drivers confirmed 42 feature test passes, frontend build parity, and standalone wheel packaging; physical robot validation remains pending.[^src-20261009-2026-10-09-builtin-movements] [^src-20261009-builtinmovementsvalidation]

[^src-20261009-2026-10-09-builtin-movements]: Automatic native built-in movement evidence and architecture boundaries.
[^src-20261009-developmentlog-2]: NinjaRobotPi0 development log with built-in movements implementation records.
[^src-20261009-builtinmovementsvalidation]: Built-in movement validation on Raspberry Pi Zero 2 W with inert hardware.
