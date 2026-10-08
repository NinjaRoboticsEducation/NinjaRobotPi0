---
type: Concept
title: NinjaRobotPi0 Platform Overview
description: Comprehensive overview of the NinjaRobotPi0 AI-powered educational and
  research robotics platform.
status: draft
generated:
  by: codex/migration-audit
  at: '2026-10-07T07:13:37.354382+00:00'
sources:
- id: src-20260822-readme
  resource: urn:llmwiki:source:src-20260822-readme
  title: NinjaRobotPi0 Readme
  content_hash: sha256:3f74856140111a6337bf8b83c58bef7be13f91df9742fc0e36be27ebd35b8df2
- id: src-20260822-developmentguide
  resource: urn:llmwiki:source:src-20260822-developmentguide
  title: NinjaRobotPi0 Development Guide
  content_hash: sha256:d1f8e19627223cb320b2e05df9a141c768ca0f418a7f77d160b6127d08c439e9
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
- id: src-20261007-2026-10-07-ninjarobot-pi0-migration-audit
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-migration-audit
  title: 2026 10 07 Ninjarobot Pi0 Migration Audit
  content_hash: sha256:6c223e850e920baffe83a0fbcf3f7c4471a97f4fbcc823e93d5cd2e33666d4ab
- id: src-20261008-installationguide-3
  resource: urn:llmwiki:source:src-20261008-installationguide-3
  title: Installationguide
  content_hash: sha256:734051f87ce7f447ae50bee7863118612f55b5747cd42e3cb047662a5408081f
- id: src-20261008-developmentguide-3
  resource: urn:llmwiki:source:src-20261008-developmentguide-3
  title: Developmentguide
  content_hash: sha256:0fc10ebdf50056c8d26521e3251d265cf5b2a764c98b9b1c13f2204310385178
- id: src-20261007-2026-10-07-install-onboard-wiki-ui-2
  resource: urn:llmwiki:source:src-20261007-2026-10-07-install-onboard-wiki-ui-2
  title: Pi0 upgrade implementation and current UI contracts
  content_hash: sha256:1545ea683947c315a9ea0d4c30258c228e975a78e39062b2e045669fcff0cb9c
- id: src-20261007-2026-10-08-upgrade-audit
  resource: urn:llmwiki:source:src-20261007-2026-10-08-upgrade-audit
  title: Pi0 upgrade audit findings and boundaries
  content_hash: sha256:7112a6575c6288875e3fdad33679f094b22908e0ee729b29f5dfbfc55f48de64
- id: src-20261008-readme-3
  resource: urn:llmwiki:source:src-20261008-readme-3
  title: Readme
  content_hash: sha256:c9ced856b42efefacbb3800f8abc7048b8f65b5b0237f4d2d640619a39926121
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
semantic_review:
  version: 1
  performed_by: agent:codex
  performed_at: '2026-10-08T05:58:09.896854+00:00'
  target_hash: sha256:90ccdee791ac4c5d3728048d79b0fde38e2ec74fee6350d62a07638d89f18645
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed the current compatibility manual and recorded uv 0.9.26 dry-run against
    the installer/checker, locked Vite engines and 205 passing host regressions on
    Python 3.11 and 3.13. Exact Node/uv equality and codename rules are superseded
    explicitly; device/user requirements, real Node/Python minima, read-only inspection
    and missing-environment failures remain. Compatible tool reuse and checksum fallback
    are distinct. Retained hardware/history claims keep their prior sources; no physical
    or human verification is inferred.
  - Source-grounded AI review of changed claims and retained cited context; draft/unverified.
    Physical tests, live accounts and publication remain pending.
---

# NinjaRobotPi0 Platform Overview

## Current setup and documentation

The installer targets Zero 2 W with Debian-based Raspberry Pi OS 64-bit; current requirements are below. `./install.sh` installs software; `./onboard.sh` guides existing hardware tools and Gemini/ngrok settings. Full current manuals are immutable versions inside `ninjarobot_pi0_Wiki`; root manuals preserve public links. Pi0 uses a Pi5-style navy/cyan web presentation with its existing control contracts. Real-device final validation remains pending. Current React metadata is 19.2.0; descriptions of React 18 in earlier reference material are historical. See [guided onboarding](concepts/guided-onboarding.md), [development workflow](concepts/development-workflow.md), [web design](concepts/web-interface-design.md), [installation manual](references/installation-guide.md), and [development manual](references/development-guide.md).[^src-20261008-installationguide-3] [^src-20261008-developmentguide-3]


**NinjaRobotPi0** is an advanced, modular AI robot platform designed for research and STEAM education, powered by the Raspberry Pi Zero 2W.[^src-20260822-readme] It integrates a Google Gemini agent with a mobile-first web interface, dual connectivity (Wi-Fi and Bluetooth Low Energy), and rebuilt non-blocking hardware drivers.[^src-20260822-readme] [^src-20260822-developmentguide]

## Hardware Specifications

| Component | Specification | Details |
|-----------|---------------|---------|
| **Brain / SBC** | Raspberry Pi Zero 2W | Quad-core ARM Cortex-A53 @ 1.0 GHz, 512MB RAM [^src-20260822-readme] |
| **Display** | 2.0" / 2.8" ST7789V IPS LCD | 240×320 pixels, SPI interface, PWM brightness control [^src-20260822-readme] [^src-20260822-developmentguide] |
| **Distance Sensor** | VL53L0X Time-of-Flight | Up to 2m documented range, I2C interface, distance readings in millimetres [^src-20260822-readme] |
| **Sound / Audio** | Passive Buzzer | GPIO 17, 35 musical notes (C3–B7), 14 emotion sounds [^src-20260822-readme] |
| **Actuators** | 8× SG90 / MG90S Servos | GPIO 20–27, velocity-based physics control [^src-20260822-readme] |
| **Connectivity** | Wi-Fi & Bluetooth | Wi-Fi 802.11n (2.4GHz), BLE 4.2 GATT Server [^src-20260822-readme] |

## Software Architecture

The NinjaRobot software stack is organized as a layered monorepo with 7 independent Python packages and a modern web application:[^src-20260822-developmentguide]

* **[Architecture & Hardware Abstraction Layer](concepts/architecture-and-hal.md)**: Dynamic driver registry and ABC interfaces in `ninja_utils`.[^src-20260822-developmentguide]
* **[Motion System & Easing](concepts/motion-system-and-easing.md)**: Velocity-based servo control and position-aware cubic easing curves.[^src-20260822-developmentguide]
* **[Dual Connectivity & Protocols](concepts/dual-connectivity-and-protocols.md)**: Centralized command dispatching across BLE and Web interfaces with chunked transport.[^src-20260822-developmentguide]
* **[Safe Execution & Blockly Runtime](concepts/safe-execution-and-blockly-runtime.md)**: Sandboxed code execution engine and dual runtime pipeline.[^src-20260822-developmentguide]
* **[Action Library & AI Agent](concepts/action-library-and-ai-agent.md)**: Validated user-selected Gemini models, bounded Gemini 3 compatibility, and a persistent Blockly action library.[^src-20260822-readme] [^src-20260822-developmentguide]
* **[Perception & Expression](concepts/perception-and-expression.md)**: Distance monitoring, animated facial expressions, and emotion audio queues.[^src-20260822-developmentguide]

## Component Packages

* **[NinjaRobotPi0 Entity](entities/ninjarobot-v5.md)**: High-level robot platform entity.[^src-20260822-readme]
* **[ninja_core](entities/ninja-core.md)**: Central application server, HAL, motion system, and web controllers.[^src-20260822-developmentguide]
* **[ninja_ble](entities/ninja-ble.md)**: BLE GATT server service supporting zero-network mobile connection.[^src-20260822-developmentguide]
* **[ninja_utils](entities/ninja-utils.md)**: Shared interfaces (`Sensor`, `Actuator`), logging, and system utilities.[^src-20260822-developmentguide]
* **[pi0servo](entities/pi0servo.md)**: Velocity-based multi-servo controller with easing.[^src-20260822-developmentguide]
* **[pi0disp](entities/pi0disp.md)**: Thread-safe ST7789V display driver with delta rendering.[^src-20260822-developmentguide]
* **[pi0buzzer](entities/pi0buzzer.md)**: Non-blocking passive buzzer driver with emotion sounds and melodies.[^src-20260822-developmentguide]
* **[pi0vl53l0x](entities/pi0vl53l0x.md)**: Hardened VL53L0X Time-of-Flight distance sensor driver.[^src-20260822-developmentguide]
* **[ninja_webapp](entities/ninja-webapp.md)**: React 18 + Vite frontend SPA with multilingual support.[^src-20260822-developmentguide]

## References & Deep Dives

* **[Installation & Wiring Guide](references/installation-and-wiring.md)**: Step-by-step assembly, wiring tables, and OS setup.[^src-20260822-developmentguide]
* **[Hardware Calibration & Tools](references/hardware-calibration-and-tools.md)**: Guided initialization and interactive TUIs for each subsystem.[^src-20260822-developmentguide]
* **[API & CLI Reference](references/api-and-cli-reference.md)**: Unified Python API, REST endpoints, and CLI commands.[^src-20260822-developmentguide]
* **[Driver Rebuild & Vulnerability Analysis](analyses/driver-rebuild-and-vulnerability-analysis.md)**: Evolution from legacy blocking drivers to non-blocking architectures.[^src-20260822-developmentguide]
* **[Development History & Evolution](analyses/development-history-and-evolution.md)**: Detailed chronology of V5 development phases and audits.[^src-20260822-developmentguide]

[^src-20260822-readme]: NinjaRobotPi0 Readme.
[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.


## Historical migration audit follow-up (2026-10-07)

Current repository documentation uses NinjaRobotPi0; historical audits and V5 version milestones retain their original identity. Robot runtime code and package names are unchanged. After a clean clone, prepare the embedded wiki with the normalization bootstrap in `NinjaRobotPi0/Wiki/NinjaRobotPi0_Wiki/README.md` before lint: its derived manifests are intentionally untracked. The tested bootstrap regenerates these through the existing CLI and restores zero-error normal lint. Website manuals use `blob/HEAD` and clone commands omit branch selection.[^src-20261007-2026-10-07-ninjarobot-pi0-migration-audit]

[^src-20261007-2026-10-07-ninjarobot-pi0-migration-audit]: Audit evidence covering documentation attribution, current naming, default-branch links, and clean-clone wiki normalization.

[^src-20261008-installationguide-3]: Current versioned Installationguide.

[^src-20261008-developmentguide-3]: Current versioned DevelopmentGuide.

## Implementation evidence and acceptance limits

Host validation and the exact code/tooling boundary are recorded in the approved implementation evidence. Real Pi hardware, live accounts and published curl acceptance remain pending; passing host checks do not imply physical acceptance.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.


## Historical 2026-10-08 audit follow-up (superseded policy)

The following records the earlier implementation; current compatibility policy below supersedes exact-version, codename and private-tool-precedence claims.

A comprehensive public README now follows Pi5 introduction, hardware/OS preparation, curl installation, guided initialization, browser access, first tests and troubleshooting. Japanese and Chinese sections are explicitly summaries. The wizard aligns its console flow with Pi5 while preserving Pi0 capabilities and manual runtime startup. See the current full manuals for the audit corrections and pending device acceptance.[^src-20261007-2026-10-08-upgrade-audit]

[^src-20261007-2026-10-08-upgrade-audit]: Pi0 upgrade audit findings and boundaries.

The public walkthrough is preserved as versioned README evidence.[^src-20261008-readme-3]

[^src-20261008-readme-3]: Pi0 public README — audit 2026-10-08.


## Historical Trixie support correction (superseded policy)

The following records the earlier implementation; current compatibility policy below supersedes exact-version, codename and private-tool-precedence claims.

The installer target now includes Bookworm (Debian 12) and Trixie (Debian 13), both 64-bit on Zero 2 W. The earlier rejection was the explicit Bookworm-only release check, not a failure of 64-bit detection. Both bootstrap and local/onboarding preflight have matching allowlists. Real Trixie hardware acceptance remains pending.[^src-20261008-2026-10-08-trixie-support]

[^src-20261008-2026-10-08-trixie-support]: Trixie installer correction and validation boundary.


## Historical Installation recovery and diagnostics (superseded policy)

The following records the earlier implementation; current compatibility policy below supersedes exact-version, codename and private-tool-precedence claims.

The current README provides explicit recovery steps: update Git by fetching default HEAD and fast-forwarding, run the installer, then check. Checks remain read-only and report versions, paths and retry commands. Installation failures identify their stage. This does not operate hardware or automatically update Git.[^src-20261008-2026-10-08-installer-recovery]

[^src-20261008-2026-10-08-installer-recovery]: Installer diagnostics and recovery validation.


## Current software compatibility policy

Installer checks now use compatibility instead of exact OS/Node/uv versions. No OS codename allowlist remains. The device, Linux aarch64, Debian-family OS, normal-user and Python 3.10+ requirements remain; optional wiki needs Python 3.11+. Bookworm/Trixie are reference targets, not a complete allowlist or proof of physical acceptance.[^src-20261008-2026-10-08-installer-compatibility]

[^src-20261008-2026-10-08-installer-compatibility]: Installer compatibility requirements and validation evidence.
