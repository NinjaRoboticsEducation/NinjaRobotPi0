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
- id: src-20261011-readme-current
  resource: urn:llmwiki:source:src-20261011-readme-current
  title: Web refinement corrected English README
  content_hash: sha256:4058c6f103ff077f356228e7e4fb6728f5314b0c7602db00f231be8a08a5fc77
- id: src-20261011-webrefinementevidence
  resource: urn:llmwiki:source:src-20261011-webrefinementevidence
  title: Web refinement code, design and local validation evidence
  content_hash: sha256:5ce2540bcc10522fc7e7dd5d1295c9738c4b0ed695bc4f39359ba91ddf669e69
- id: src-20261011-readme-final
  resource: urn:llmwiki:source:src-20261011-readme-final
  title: Web refinement final English README navigation
  content_hash: sha256:149b9d5500e321b8e8b4bfd8eee4e056ef7eef77e5bca6107a9086860f8d1a8b
semantic_review:
  version: 1
  performed_by: agent:codex
  performed_at: '2026-10-11T07:05:12.227497+00:00'
  target_hash: sha256:128f5dd795543a2e7078c2dc4d931546a23ac2413b0cd55b9ebe553bbe68eec4
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Current routes, locale sets, HTTP payloads, telemetry/event streams and microphone
    lifecycle checked against current source and new guide/README/evidence.
  - Historical provider-audio gating is explicitly superseded; browser speech-service
    availability and owner-waived browser validation remain limitations.
  - Source fingerprints were checked; unchanged historical evidence retains its prior
    source-grounded review context. AI review is not human verification.
  - Checked the new complete link-corrected log/README navigation source; feature
    claims and validation limits are unchanged and earlier raw versions remain immutable.
---

# ninja_webapp Package

## Current interface and contracts

`ninja_webapp` is the existing React 19.2/Vite SPA with four locale bundles (`en`, `ja`, `zh-TW`, `zh-CN`). The owner-requested refinement changes frontend presentation only; backend/driver APIs, robot configuration, session ownership and shutdown confirmation remain unchanged. BLE advertising is distinct from web controller ownership.[^src-20261011-developmentguide] [^src-20261011-readme-current] [^src-20261011-readme-final]

## Application pages

- **Home (`/`)** combines language, interface selection and confirmed System Power. It is also the hamburger-menu destination.
- **Movement Tool (`/movement`)** contains live distance and server-supplied native movement, face and sound selectors. Execution uses the existing direct POST endpoints and does not call Ninja Agent.
- **Chat (`/agent`)** contains conversation/local clear, a prompt/send row and browser voice transcription into the prompt. It keeps the existing `{message, language}` chat payload and aborts recognition on navigation.
- **Legacy Help (`/help`)** redirects Home; the Help implementation is removed. Unknown frontend routes also return Home.[^src-20261011-developmentguide] [^src-20261011-readme-current]

Movement and Chat share a bottom System Activity drawer, folded by default and expanded above content with timestamp/message rows, local clear and independent scrolling. `/ws/distance` remains a separate millimetre stream; `/ws/events` supplies actual runtime activity. The header badge uses real `/ws/session` ownership, not BLE advertising. Mobile-first columns, bounded widths, wrapping forms/messages, safe areas and localized/document-language labels implement the supplied design.[^src-20261011-developmentguide] [^src-20261011-webrefinementevidence]

Frontend lint/build, locale completeness, inert session/stream checks and protected-core verification passed. Browser validation was explicitly waived on the Pi Lite host; responsive/browser/device acceptance remains manual and is not implied by source checks.[^src-20261011-webrefinementevidence]

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.

[^src-20261007-developmentguide-2]: Current versioned Developmentguide.

## Implementation evidence and acceptance limits

Host validation and the exact code/tooling boundary are recorded in the approved implementation evidence. Real Pi hardware, live accounts and published curl acceptance remain pending; passing host checks do not imply physical acceptance.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.
## Shared session lifecycle and reconnect management (2026-10-10)

`ninja_webapp` integrates session management in the shared application layout (`Layout.jsx`) using the `useRobotSession.js` hook.[^src-20261010-lifecyclerefinementsimplementationplan] A persistent `/ws/session` socket connects when the app mounts, carrying the server's HttpOnly session cookie across routes, now Home, Movement Tool and Chat.[^src-20261011-developmentguide] Heartbeat pings run every 10 seconds, with automatic retry every 3 seconds if disconnected. If a secondary browser attempts to connect while a session is active, the server closes the socket with code 4409, and the web app presents a busy status message preventing unauthorized control. The four locale bundles (`en`, `ja`, `zh-cn`, `zh-tw`) provide localized notifications for busy and reconnecting states.[^src-20261010-lifecyclerefinementsvalidation]

[^src-20261010-lifecyclerefinementsimplementationplan]: Lifecycle refinements implementation plan.
[^src-20261010-lifecyclerefinementsvalidation]: Lifecycle refinements validation report.

## Historical model-audio UI gating (2026-10-10, superseded)

The earlier Agent page consumed provider, model, and audio capability metadata from `/api/agent/status`.[^src-20261010-modeladapterimplementation] That earlier implementation disabled voice recording controls with descriptive localized tooltips when the active model does not support native audio (OpenAI, Anthropic, Ollama Cloud, or non-allowlisted Google models). Backend voice endpoints reject audio payloads upfront if the active provider does not support it.[^src-20261010-modeladapterimplementation] A historical CSS stacking fix in `Agent.module.css` ensures navigation headers and menu sheets remain fully interactable above open activity panels.[^src-20261010-modeladapterimplementation] [^src-20261010-modeladaptervalidation]

[^src-20261010-modeladapterimplementation]: Pi0 Cloud Model Provider Adapter implementation evidence.
[^src-20261010-modeladaptervalidation]: Cloud model adapter validation report.

## Web Microphone Input and Voice Gating Correction (2026-10-11)

The Agent page microphone control uses client-side browser speech recognition (`SpeechRecognition` / `webkitSpeechRecognition`) to transcribe user voice input into the prompt text area, sending the transcribed text via `/api/agent/chat` when submitted.[^src-20261010-shutdownvoicefixes]
* **Capability Gating Correction**: The previous `supports_audio` gating incorrectly disabled the microphone button for text-only cloud models (OpenAI, Anthropic, Ollama Cloud, and non-audio Google models). The `supports_audio` flag describes direct raw-audio processing at `/api/agent/voice`. Removing that gate from the UI microphone button restores voice typing for all providers regardless of model audio support.[^src-20261010-shutdownvoicefixes] [^src-20261010-developmentguide-4]
* **Lifecycle & Navigation Cleanup**: The Agent page manages its own recognition instance, resets recording state on startup errors, and cleanly aborts active speech recognition when unmounting during navigation.[^src-20261010-shutdownvoicefixes]

[^src-20261010-shutdownvoicefixes]: Server shutdown and browser voice regression repair evidence note.
[^src-20261010-developmentguide-4]: Current versioned DevelopmentGuide (2026-10-11 shutdown & voice fixes).

The historical model-audio UI gate above was corrected before this refinement. Current Chat does not fetch provider audio metadata to gate its Web Speech microphone and makes no raw-audio API request. Availability depends on the browser speech service and permissions, not model audio-file capability.[^src-20261011-developmentguide] [^src-20261011-webrefinementevidence]

[^src-20261011-developmentguide]: Web refinement current development guide (2026-10-11 web refinement).

[^src-20261011-readme-current]: Web refinement corrected English README (2026-10-11 web refinement).

[^src-20261011-webrefinementevidence]: Web refinement code, design and local validation evidence (2026-10-11 web refinement).

[^src-20261011-readme-final]: Web refinement final English README navigation; current complete source corrects navigation links while preserving earlier versions.
