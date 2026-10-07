---
type: Entity
title: ninja_webapp Package
description: Mobile-first React 18 SPA frontend providing real-time controls, AI chat,
  telemetry, and internationalization.
status: draft
generated:
  by: codex/repository-migration
  at: '2026-10-07T07:00:29.384460+00:00'
sources:
- id: src-20260822-developmentguide
  resource: urn:llmwiki:source:src-20260822-developmentguide
  title: NinjaRobotPi0 Development Guide
  content_hash: sha256:43e40f7c8db5734b4e8fe2ffd7d1e9c365cf9ceaad16fb4dbbbbe8eb1be71e7c
- id: src-20260822-readme
  resource: urn:llmwiki:source:src-20260822-readme
  title: NinjaRobotPi0 Readme
  content_hash: sha256:f8becc32b9999e418981bf11025a09959dd03b9175fdcb7f86dfbd7f190db909
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
---

# ninja_webapp Package

`ninja_webapp` is the modern web frontend for NinjaRobotPi0, built with React 18, Vite, and `react-router-dom`.[^src-20260822-readme] [^src-20260822-developmentguide]

## Architecture & Technology

* **Framework**: React 18 + Vite.[^src-20260822-developmentguide]
* **Styling**: Vanilla CSS with curated responsive tokens and modern micro-animations.[^src-20260822-developmentguide]
* **Internationalization**: `react-i18next` translations for English (`en`), Japanese (`ja`), Traditional Chinese (`zh-tw`), and Simplified Chinese (`zh-cn`).[^src-20260822-readme] [^src-20260822-developmentguide]
* **Real-Time Communication**: WebSocket connection (`/ws/events`) streaming distance telemetry, execution logs, and robot status.[^src-20260822-developmentguide]

## Application Pages

* **Home (`/`)**: Hero branding display and interactive slide-to-confirm power-off slider for safe robot shutdown.[^src-20260822-developmentguide]
* **Agent (`/agent`)**: Main control dashboard featuring:
  * **AI Chat Dialog**: Conversational text and voice input with Google Gemini.[^src-20260822-readme] [^src-20260822-developmentguide]
  * **Hardware Quick Controls**: Direct triggering of facial expressions, sounds, and recorded movements.[^src-20260822-developmentguide]
  * **Real-Time Telemetry**: Distance sensor reading display with safety indicators.[^src-20260822-readme] [^src-20260822-developmentguide]
  * **Slidable System Log Panel**: Real-time log monitor for debugging and telemetry.[^src-20260822-developmentguide]
* **Help (`/help`)**: User manual and quick reference documentation.[^src-20260822-developmentguide]

[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.
[^src-20260822-readme]: NinjaRobotPi0 Readme.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.
