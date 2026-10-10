---
type: Entity
title: ninja_webapp Package
description: React SPA providing Pi0 controls, AI chat, distance telemetry and four
  languages with Pi5-derived presentation.
status: draft
generated:
  by: codex/migration-audit
  at: '2026-10-07T07:13:37.354382+00:00'
sources:
- id: src-20260822-developmentguide
  resource: urn:llmwiki:source:src-20260822-developmentguide
  title: NinjaRobotPi0 Development Guide
  content_hash: sha256:d1f8e19627223cb320b2e05df9a141c768ca0f418a7f77d160b6127d08c439e9
- id: src-20260822-readme
  resource: urn:llmwiki:source:src-20260822-readme
  title: NinjaRobotPi0 Readme
  content_hash: sha256:3f74856140111a6337bf8b83c58bef7be13f91df9742fc0e36be27ebd35b8df2
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
- id: src-20261007-developmentguide-2
  resource: urn:llmwiki:source:src-20261007-developmentguide-2
  title: Developmentguide
  content_hash: sha256:6851b89fb0bf25cf5be3be6f445b8169802b8889809724e81116c9d3b30856d4
- id: src-20261007-2026-10-07-install-onboard-wiki-ui-2
  resource: urn:llmwiki:source:src-20261007-2026-10-07-install-onboard-wiki-ui-2
  title: Pi0 upgrade implementation and current UI contracts
  content_hash: sha256:1545ea683947c315a9ea0d4c30258c228e975a78e39062b2e045669fcff0cb9c
- id: src-20261010-lifecyclerefinementsimplementationplan
  resource: urn:llmwiki:source:src-20261010-lifecyclerefinementsimplementationplan
  title: Lifecyclerefinementsimplementationplan
  content_hash: sha256:5d4be31936118493340340291e66a59c7f76886f26e791ca0963721aab9f21a8
- id: src-20261010-lifecyclerefinementsvalidation
  resource: urn:llmwiki:source:src-20261010-lifecyclerefinementsvalidation
  title: Lifecyclerefinementsvalidation
  content_hash: sha256:01fa07f823e9dedfcc2d243ae107b496758960b0c5be790db9df2a8deef94066
- id: src-20261010-modeladapterimplementation
  resource: urn:llmwiki:source:src-20261010-modeladapterimplementation
  title: Modeladapterimplementation
  content_hash: sha256:2c6480a2595936057adf1550e8860044d7269be1b6a860a1395d893ec7a78895
- id: src-20261010-modeladaptervalidation
  resource: urn:llmwiki:source:src-20261010-modeladaptervalidation
  title: Modeladaptervalidation
  content_hash: sha256:653ade7e3e622c23f29dad7eedb8417a1ed0da58869859db3eb08c7319905938
semantic_review:
  version: 1
  performed_by: agent:antigravity
  performed_at: '2026-10-10T15:28:47.571035+00:00'
  target_hash: sha256:77c91a449b90cec11e84beb48b06be1d38a271ecce79a66c850c8e7a03de3de7
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed ninja_webapp package against Agent page, Agent.module.css, and /api/agent/status
    contracts. Gated voice input states, localized tooltips, and stacking order corrections
    match code.
  - Mocked browser UI tests pass; real hardware microphone testing remains pending.
---

# ninja_webapp Package

## Current visual design

Current frontend metadata declares React 19.2.0; older React 18 descriptions are historical. The Pi5-derived navy/cyan tokens, panels, menu sheet and activity drawer apply to Pi0 Home, Agent and Help. Routes, request payloads, WebSocket events, millimetre units and existing action selectors remain Pi0-specific. BLE advertising is not controller connection. Four locale sets include previously missing labels; power still requires staged user action plus confirmation, with an accessible keyboard alternative.[^src-20261007-developmentguide-2]


`ninja_webapp` is the modern web frontend for NinjaRobotPi0, previously described as React 18, Vite, and `react-router-dom`.[^src-20260822-readme] [^src-20260822-developmentguide]

## Architecture & Technology

* **Earlier framework description**: React 18 + Vite.[^src-20260822-developmentguide]
* **Styling**: Vanilla CSS with curated responsive tokens and modern micro-animations.[^src-20260822-developmentguide]
* **Internationalization**: `react-i18next` translations for English (`en`), Japanese (`ja`), Traditional Chinese (`zh-tw`), and Simplified Chinese (`zh-cn`).[^src-20260822-readme] [^src-20260822-developmentguide]
* **Real-Time Communication**: `/ws/distance` supplies `distance_mm`; `/ws/events` supplies activity/log events. The old combined-distance description was documentation drift.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

## Application Pages

* **Home (`/`)**: Hero branding display and interactive slide-to-confirm power-off slider for safe robot shutdown.[^src-20260822-developmentguide]
* **Agent (`/agent`)**: Main control dashboard featuring:
  * **AI Chat Dialog**: Conversational text and voice chat with active cloud provider (Google, OpenAI, Anthropic, Ollama Cloud) and capability-gated voice input.[^src-20260822-readme] [^src-20261010-modeladapterimplementation]
  * **Hardware Quick Controls**: Direct triggering of facial expressions, sounds, and recorded movements.[^src-20260822-developmentguide]
  * **Real-Time Telemetry**: Distance sensor reading display with safety indicators.[^src-20260822-readme] [^src-20260822-developmentguide]
  * **Slidable System Log Panel**: Real-time log monitor for debugging and telemetry.[^src-20260822-developmentguide]
* **Help (`/help`)**: User manual and quick reference documentation.[^src-20260822-developmentguide]

[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.
[^src-20260822-readme]: NinjaRobotPi0 Readme.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.

[^src-20261007-developmentguide-2]: Current versioned Developmentguide.

## Implementation evidence and acceptance limits

Host validation and the exact code/tooling boundary are recorded in the approved implementation evidence. Real Pi hardware, live accounts and published curl acceptance remain pending; passing host checks do not imply physical acceptance.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.
## Shared session lifecycle and reconnect management (2026-10-10)

`ninja_webapp` integrates session management in the shared application layout (`Layout.jsx`) using the `useRobotSession.js` hook.[^src-20261010-lifecyclerefinementsimplementationplan] A persistent `/ws/session` socket connects when the app mounts, carrying the server's HttpOnly session cookie across Home, Agent, and Help views. Heartbeat pings run every 10 seconds, with automatic retry every 3 seconds if disconnected. If a secondary browser attempts to connect while a session is active, the server closes the socket with code 4409, and the web app presents a busy modal preventing unauthorized control. The four locale bundles (`en`, `ja`, `zh-cn`, `zh-tw`) provide localized notifications for busy and reconnecting states.[^src-20261010-lifecyclerefinementsvalidation]

[^src-20261010-lifecyclerefinementsimplementationplan]: Lifecycle refinements implementation plan.
[^src-20261010-lifecyclerefinementsvalidation]: Lifecycle refinements validation report.

## Voice capability gating and provider status display (2026-10-10)

The Agent page consumes provider, model, and audio capability metadata from `/api/agent/status`.[^src-20261010-modeladapterimplementation] Voice recording controls are disabled with descriptive localized tooltips when the active model does not support native audio (OpenAI, Anthropic, Ollama Cloud, or non-allowlisted Google models). Backend voice endpoints reject audio payloads upfront if the active provider does not support it.[^src-20261010-modeladapterimplementation] A CSS stacking fix in `Agent.module.css` ensures navigation headers and menu sheets remain fully interactable above open activity panels.[^src-20261010-modeladapterimplementation] [^src-20261010-modeladaptervalidation]

[^src-20261010-modeladapterimplementation]: Pi0 Cloud Model Provider Adapter implementation evidence.
[^src-20261010-modeladaptervalidation]: Cloud model adapter validation report.
