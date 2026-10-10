---
type: Concept
title: Pi0 web interface design and compatibility
description: Pi0 web interface design and compatibility.
status: draft
generated:
  by: agent:codex
  at: '2026-10-07T13:03:34.637721+00:00'
sources:
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
- id: src-20261010-lifecyclerefinementsevidence
  resource: urn:llmwiki:source:src-20261010-lifecyclerefinementsevidence
  title: Lifecyclerefinementsevidence
  content_hash: sha256:c34468e740adccacc6546a2afe39fd41562eed229ae5795255577b044d4fd09e
- id: src-20261010-lifecyclerefinementsvalidation
  resource: urn:llmwiki:source:src-20261010-lifecyclerefinementsvalidation
  title: Lifecyclerefinementsvalidation
  content_hash: sha256:01fa07f823e9dedfcc2d243ae107b496758960b0c5be790db9df2a8deef94066
- id: src-20261010-readme-2
  resource: urn:llmwiki:source:src-20261010-readme-2
  title: Readme
  content_hash: sha256:61178b7920f399c303a8f0f19fd6a05b5f1ed43e510c47b261f3ae7bc5fba0c6
- id: src-20261010-shutdownvoicefixes
  resource: urn:llmwiki:source:src-20261010-shutdownvoicefixes
  title: Shutdownvoicefixes
  content_hash: sha256:bc56cba07d2aade0773ca839cb060aceb625af2a002344892a6e81f6c0b5c6fb
- id: src-20261010-developmentguide-4
  resource: urn:llmwiki:source:src-20261010-developmentguide-4
  title: Developmentguide
  content_hash: sha256:b82c27e23387051b0280adf428e34299bbfd65bcf2bcc80d3802027c4f3827bc
semantic_review:
  version: 1
  performed_by: agent:antigravity
  performed_at: '2026-10-10T17:23:23.105961+00:00'
  target_hash: sha256:2aa28aa133526286fb85112486303e9d33e7e09cbba8505ec9221527d2463faa
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed client-side Web Speech recognition lifecycle, unmount cleanup, and provider
    independence against Layout.jsx and Agent/index.jsx.
  - Automated Chromium browser tests passed; target-device browser confirmation remains
    pending.
---

# Pi0 web interface design and compatibility

Pi0 retains its React routes and control contracts while adopting Pi5 navy/cyan styling, bordered rounded panels, a menu sheet and an activity drawer. Home, Agent and Help use the same palette. Existing expressions/sounds/movements, chat, browser speech input and distance events remain Pi0 capabilities. The UI adds no Pi5 camera, gamepad, or cloud voice service, while introducing a native single-browser session ownership contract. Automated browser checks use inert API/socket fixtures; they do not establish physical-device acceptance.[^src-20261007-developmentguide-2]

[Project overview](/overview.md).

[^src-20261007-developmentguide-2]: Current versioned Developmentguide.

## Implementation evidence and acceptance limits

Host validation and the exact code/tooling boundary are recorded in the approved implementation evidence. Real Pi hardware, live accounts and published curl acceptance remain pending; passing host checks do not imply physical acceptance.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.
## Single-browser session ownership and reconnect screen (2026-10-10)

The shared application layout (`Layout.jsx`) maintains a persistent `/ws/session` WebSocket carrying a server-issued HttpOnly `ninja_web_session` cookie across Home, Agent, and Help routes.[^src-20261010-lifecyclerefinementsimplementationplan] [^src-20261010-readme-2]
- **Session Exclusivity**: Exactly one browser controls web APIs; multiple tabs sharing the cookie act as one controller. Secondary connections receive a 4409 close code and a busy modal.[^src-20261010-lifecyclerefinementsevidence]
- **Endpoint Gating**: All `/api/` endpoints and auxiliary sockets (`/ws/distance`, `/ws/events`) require active session ownership (returning 423 if inactive, 503 during server shutdown).[^src-20261010-lifecyclerefinementsevidence]
- **Disconnect Cleanup**: Closing the browser or reaching a 35s timeout aborts ongoing native and Blockly tasks, cancels pending HTTP/greeting work, and restores the waiting QR code (ngrok URL or LAN URL) on the robot display.[^src-20261010-lifecyclerefinementsimplementationplan] [^src-20261010-lifecyclerefinementsvalidation]
- **Idle Suppression**: `RuntimePipeline` suppresses automatic idle face animation painting while waiting on the reconnect screen.[^src-20261010-lifecyclerefinementsimplementationplan]

[^src-20261010-lifecyclerefinementsimplementationplan]: Lifecycle refinements implementation plan.
[^src-20261010-lifecyclerefinementsevidence]: Lifecycle refinements implementation evidence.
[^src-20261010-lifecyclerefinementsvalidation]: Lifecycle refinements validation report.
[^src-20261010-readme-2]: NinjaRobotPi0 English README snapshot (2026-10-10 lifecycle).

## Browser Speech Recognition and Lifecycle Management (2026-10-11)

The Agent page provides browser-based voice input powered by the Web Speech API (`SpeechRecognition` / `webkitSpeechRecognition`). Speech is converted locally in the browser into text inside the chat input box and submitted as normal text messages to `/api/agent/chat`.[^src-20261010-shutdownvoicefixes]
* **Provider Independence**: Because recognition happens client-side before text transmission, microphone voice input is supported across all cloud AI providers (Google, OpenAI, Anthropic, Ollama Cloud) and does not require provider-level raw audio ingestion capabilities.[^src-20261010-shutdownvoicefixes] [^src-20261010-developmentguide-4]
* **Component Lifecycle**: The speech recognition instance is tied to the Agent page lifecycle, ensuring recording aborts immediately upon route navigation or component unmount.[^src-20261010-shutdownvoicefixes]

[^src-20261010-shutdownvoicefixes]: Server shutdown and browser voice regression repair evidence note.
[^src-20261010-developmentguide-4]: Current versioned DevelopmentGuide (2026-10-11 shutdown & voice fixes).
