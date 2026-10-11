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
- id: src-20261011-developmentguide
  resource: urn:llmwiki:source:src-20261011-developmentguide
  title: Web refinement current development guide
  content_hash: sha256:a3cbb8265b1fd651a73fcd826a58f239d60fd28f128d2b82de7d628fec8ec738
- id: src-20261011-webrefinementevidence
  resource: urn:llmwiki:source:src-20261011-webrefinementevidence
  title: Web refinement code, design and local validation evidence
  content_hash: sha256:5ce2540bcc10522fc7e7dd5d1295c9738c4b0ed695bc4f39359ba91ddf669e69
- id: src-20261011-developmentguide-2
  resource: urn:llmwiki:source:src-20261011-developmentguide-2
  title: Mobile refinement current development guide
  content_hash: sha256:d17ec03fe789cd0f8f13824ef0d773c7608fe1efae29150fa1c07610ee4febed
- id: src-20261011-webmobilerefinement
  resource: urn:llmwiki:source:src-20261011-webmobilerefinement
  title: Web mobile refinement evidence
  content_hash: sha256:f8d7f1c9bdec974150d098e9c6d8b3fd0910b7ee6318368329dc06228c4525f4
semantic_review:
  version: 1
  performed_by: agent:antigravity
  performed_at: '2026-10-11T09:54:05.388246+00:00'
  target_hash: sha256:d3ff94c6fa147f82e5aba320608c3bec78a82128e18b27164f16119cc72c0ba8
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: passed
  notes:
  - Reviewed mobile viewport tracking, body scroll lock, persistent link selection,
    and GET /api/robot/status against DevelopmentGuide.md and WebMobileRefinement.md.
  - Inspected visual screenshot evidence across 9 screen resolutions from inert Chromium
    test matrix.
  - Automated tests passed; native mobile browser, hardware touchscreen, and live
    robot acceptance remain pending.
---

# Pi0 web interface design and compatibility

The current Pi0 interface uses Home (`/`) as the combined landing page/menu, Movement Tool (`/movement`) for distance and direct native controls, and Chat (`/agent`) for prompts and browser voice input. Hamburger links return Home; the removed Help route redirects there. Cyan-outlined dark cards, orange actions and the active/idle voice styles follow the six owner-supplied references. Backend/runtime/driver behavior, session ownership, native endpoint contracts and power confirmation are preserved. Earlier menu-sheet/combined-dashboard descriptions are historical.[^src-20261011-developmentguide] [^src-20261011-webrefinementevidence]

[Project overview](/overview.md).

[^src-20261007-developmentguide-2]: Historical versioned Developmentguide UI contracts.[^src-20261007-developmentguide-2]

## Implementation evidence and acceptance limits

Host validation and the exact code/tooling boundary are recorded in the approved implementation evidence. Real Pi hardware, live accounts and published curl acceptance remain pending; passing host checks do not imply physical acceptance.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.
## Single-browser session ownership and reconnect screen (2026-10-10)

The shared application layout (`Layout.jsx`) maintains a persistent `/ws/session` WebSocket carrying a server-issued HttpOnly `ninja_web_session` cookie across Home, Movement Tool and Chat routes; current presentation retains that ownership hook.[^src-20261011-developmentguide][^src-20261010-lifecyclerefinementsimplementationplan] [^src-20261010-readme-2]
- **Session Exclusivity**: Exactly one browser controls web APIs; multiple tabs sharing the cookie act as one controller. Secondary connections receive a 4409 close code and a busy status message.[^src-20261010-lifecyclerefinementsevidence]
- **Endpoint Gating**: All `/api/` endpoints and auxiliary sockets (`/ws/distance`, `/ws/events`) require active session ownership (returning 423 if inactive, 503 during server shutdown).[^src-20261010-lifecyclerefinementsevidence]
- **Disconnect Cleanup**: Closing the browser or reaching a 35s timeout aborts ongoing native and Blockly tasks, cancels pending HTTP/greeting work, and restores the waiting QR code (ngrok URL or LAN URL) on the robot display.[^src-20261010-lifecyclerefinementsimplementationplan] [^src-20261010-lifecyclerefinementsvalidation]
- **Idle Suppression**: `RuntimePipeline` suppresses automatic idle face animation painting while waiting on the reconnect screen.[^src-20261010-lifecyclerefinementsimplementationplan]

[^src-20261010-lifecyclerefinementsimplementationplan]: Lifecycle refinements implementation plan.
[^src-20261010-lifecyclerefinementsevidence]: Lifecycle refinements implementation evidence.
[^src-20261010-lifecyclerefinementsvalidation]: Lifecycle refinements validation report.
[^src-20261010-readme-2]: NinjaRobotPi0 English README snapshot (2026-10-10 lifecycle).

## Browser Speech Recognition and Lifecycle Management (2026-10-11)

The Agent page provides browser-based voice input powered by the Web Speech API (`SpeechRecognition` / `webkitSpeechRecognition`). The browser speech service transcribes voice into text inside the chat input box and the user submits it as normal text messages to `/api/agent/chat`.[^src-20261010-shutdownvoicefixes]
* **Provider Independence**: Because recognition happens client-side before text transmission, microphone voice input is supported across all cloud AI providers (Google, OpenAI, Anthropic, Ollama Cloud) and does not require provider-level raw audio ingestion capabilities.[^src-20261010-shutdownvoicefixes] [^src-20261010-developmentguide-4]
* **Component Lifecycle**: The speech recognition instance is tied to the Agent page lifecycle, ensuring recording aborts immediately upon route navigation or component unmount.[^src-20261010-shutdownvoicefixes]

[^src-20261010-shutdownvoicefixes]: Server shutdown and browser voice regression repair evidence note.
[^src-20261010-developmentguide-4]: Current versioned DevelopmentGuide (2026-10-11 shutdown & voice fixes).

## Current control pages and acceptance — 2026-10-11

Movement reads the existing server capability lists and posts selected actions directly without an Agent prompt. Distance remains millimetres from `/ws/distance`; invalid or disconnected telemetry displays unavailable. Chat retains the text `message`/`language` request, local conversation clearing and recognition abort on navigation. Recording is orange/white; idle is cyan outlined with a slashed microphone.[^src-20261011-developmentguide] [^src-20261011-webrefinementevidence]

Both pages share a folded-by-default floating System Activity drawer containing timestamped `/ws/events` entries, local clear, Escape/collapse, independent scrolling and a 50-entry bound. The header stays above it. The power slider still requires staged intent and browser confirmation; viewport observation adjusts geometry only.[^src-20261011-developmentguide] [^src-20261011-webrefinementevidence]

Four-language keys, frontend lint/build, inert session/stream checks and protected-core verification passed. The owner waived browser validation on Raspberry Pi Lite after startup attempts; no completed browser assertions or implemented-page screenshot review are claimed. Real mobile layout, microphone, ngrok, telemetry/output and controlled motion/power acceptance remain pending. Browser recognition is not guaranteed offline and depends on support, permission, secure context and its speech service.[^src-20261011-webrefinementevidence]

[^src-20261011-developmentguide]: Web refinement current development guide (2026-10-11 web refinement).
[^src-20261011-webrefinementevidence]: Web refinement code, design and local validation evidence (2026-10-11 web refinement).

## Mobile Viewport Adaptation, Selection State, and Fullscreen (2026-10-11)

The mobile web interface refinement resolves short-screen and on-screen keyboard clipping through reactive viewport tracking and stateful UI adaptation:[^src-20261011-developmentguide-2] [^src-20261011-webmobilerefinement]
* **Visible Viewport Shell**: The `useAppViewport` hook subscribes to `window.visualViewport` resize and scroll events, dynamically locking whole-document scrolling (`overflow: hidden`) and allocating bounded remaining-height regions for chat messages, prompts, and system logs to prevent layout shifting during keyboard pan/resize.[^src-20261011-webmobilerefinement]
* **Responsive Layout & Short-Screen Fallbacks**: Replaces fixed vertical height deductions with CSS container allocations, landscape two-column wrapping, compact vertical breakpoints, and minimum 44px tap targets.[^src-20261011-webmobilerefinement]
* **Mutually Exclusive Interface Selection**: Home (`/`) presents Movement Tool and Chat entry buttons in dark-blue/cyan styling. Activating either route stores that selection in persistent `Layout` state for the session visit. Returning Home exclusively highlights the selected link in orange/white while restoring the other to dark blue; reloading the page resets both to the default base style.[^src-20261011-developmentguide-2] [^src-20261011-webmobilerefinement]
* **Synchronous Fullscreen Activation**: Interface entry buttons invoke standard and WebKit-prefixed Fullscreen APIs synchronously within the user activation gesture, remaining gracefully interactive when unsupported or denied.[^src-20261011-developmentguide-2] [^src-20261011-webmobilerefinement]
* **Header Robot Type Status**: Upon acquiring web session ownership, `Layout` retrieves validated HAL metadata via `GET /api/robot/status` and displays `NINJA ROBOT Pi0 - <localized type>` (`Tire`, `Humanoid`, or `Spider`) in the header across English, Japanese, Traditional Chinese, and Simplified Chinese, omitting the suffix on error without guessing.[^src-20261011-developmentguide-2] [^src-20261011-webmobilerefinement]
* **Browser Validation Matrix**: 612 automated assertions in `tests/browser_ui.cjs` across 9 screen dimensions (320×568 to 1280×900) validated viewport fit, control reachability, selection persistence, and fullscreen fallback; native WebKit/Safari, physical touchscreens, and hardware actuation remain pending owner acceptance.[^src-20261011-webmobilerefinement]

[^src-20261011-developmentguide-2]: Mobile refinement current development guide (2026-10-11 mobile refinement).
[^src-20261011-webmobilerefinement]: Mobile refinement code, design and local validation evidence (2026-10-11 mobile refinement).
