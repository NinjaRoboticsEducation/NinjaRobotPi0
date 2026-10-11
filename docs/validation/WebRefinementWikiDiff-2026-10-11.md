Plan web-refinement-20261011: Owner-authorized frontend page split, preserved contracts and browser-validation waiver; update only the five named pages.
Risk: medium

## write wiki/concepts/web-interface-design.md
--- /home/rogerchang/NinjaRobotPi0/ninjarobot_pi0_Wiki/wiki/concepts/web-interface-design.md
+++ /home/rogerchang/NinjaRobotPi0/ninjarobot_pi0_Wiki/wiki/concepts/web-interface-design.md
@@ -39,28 +39,19 @@
   resource: urn:llmwiki:source:src-20261010-developmentguide-4
   title: Developmentguide
   content_hash: sha256:b82c27e23387051b0280adf428e34299bbfd65bcf2bcc80d3802027c4f3827bc
-semantic_review:
-  version: 1
-  performed_by: agent:antigravity
-  performed_at: '2026-10-10T17:23:23.105961+00:00'
-  target_hash: sha256:2aa28aa133526286fb85112486303e9d33e7e09cbba8505ec9221527d2463faa
-  result: passed
-  checks:
-    source_support: passed
-    contradictions: passed
-    limitations: passed
-    claim_strength: passed
-    visual_evidence: not_applicable
-  notes:
-  - Reviewed client-side Web Speech recognition lifecycle, unmount cleanup, and provider
-    independence against Layout.jsx and Agent/index.jsx.
-  - Automated Chromium browser tests passed; target-device browser confirmation remains
-    pending.
+- id: src-20261011-developmentguide
+  resource: urn:llmwiki:source:src-20261011-developmentguide
+  title: Web refinement current development guide
+  content_hash: sha256:a3cbb8265b1fd651a73fcd826a58f239d60fd28f128d2b82de7d628fec8ec738
+- id: src-20261011-webrefinementevidence
+  resource: urn:llmwiki:source:src-20261011-webrefinementevidence
+  title: Web refinement code, design and local validation evidence
+  content_hash: sha256:5ce2540bcc10522fc7e7dd5d1295c9738c4b0ed695bc4f39359ba91ddf669e69
 ---
 
 # Pi0 web interface design and compatibility
 
-Pi0 retains its React routes and control contracts while adopting Pi5 navy/cyan styling, bordered rounded panels, a menu sheet and an activity drawer. Home, Agent and Help use the same palette. Existing expressions/sounds/movements, chat, browser speech input and distance events remain Pi0 capabilities. The UI adds no Pi5 camera, gamepad, or cloud voice service, while introducing a native single-browser session ownership contract. Automated browser checks use inert API/socket fixtures; they do not establish physical-device acceptance.[^src-20261007-developmentguide-2]
+The current Pi0 interface uses Home (`/`) as the combined landing page/menu, Movement Tool (`/movement`) for distance and direct native controls, and Chat (`/agent`) for prompts and browser voice input. Hamburger links return Home; the removed Help route redirects there. Cyan-outlined dark cards, orange actions and the active/idle voice styles follow the six owner-supplied references. Backend/runtime/driver behavior, session ownership, native endpoint contracts and power confirmation are preserved. Earlier menu-sheet/combined-dashboard descriptions are historical.[^src-20261011-developmentguide] [^src-20261011-webrefinementevidence]
 
 [Project overview](/overview.md).
 
@@ -73,8 +64,8 @@
 [^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.
 ## Single-browser session ownership and reconnect screen (2026-10-10)
 
-The shared application layout (`Layout.jsx`) maintains a persistent `/ws/session` WebSocket carrying a server-issued HttpOnly `ninja_web_session` cookie across Home, Agent, and Help routes.[^src-20261010-lifecyclerefinementsimplementationplan] [^src-20261010-readme-2]
-- **Session Exclusivity**: Exactly one browser controls web APIs; multiple tabs sharing the cookie act as one controller. Secondary connections receive a 4409 close code and a busy modal.[^src-20261010-lifecyclerefinementsevidence]
+The shared application layout (`Layout.jsx`) maintains a persistent `/ws/session` WebSocket carrying a server-issued HttpOnly `ninja_web_session` cookie across Home, Movement Tool and Chat routes; current presentation retains that ownership hook.[^src-20261011-developmentguide][^src-20261010-lifecyclerefinementsimplementationplan] [^src-20261010-readme-2]
+- **Session Exclusivity**: Exactly one browser controls web APIs; multiple tabs sharing the cookie act as one controller. Secondary connections receive a 4409 close code and a busy status message.[^src-20261010-lifecyclerefinementsevidence]
 - **Endpoint Gating**: All `/api/` endpoints and auxiliary sockets (`/ws/distance`, `/ws/events`) require active session ownership (returning 423 if inactive, 503 during server shutdown).[^src-20261010-lifecyclerefinementsevidence]
 - **Disconnect Cleanup**: Closing the browser or reaching a 35s timeout aborts ongoing native and Blockly tasks, cancels pending HTTP/greeting work, and restores the waiting QR code (ngrok URL or LAN URL) on the robot display.[^src-20261010-lifecyclerefinementsimplementationplan] [^src-20261010-lifecyclerefinementsvalidation]
 - **Idle Suppression**: `RuntimePipeline` suppresses automatic idle face animation painting while waiting on the reconnect screen.[^src-20261010-lifecyclerefinementsimplementationplan]
@@ -86,9 +77,21 @@
 
 ## Browser Speech Recognition and Lifecycle Management (2026-10-11)
 
-The Agent page provides browser-based voice input powered by the Web Speech API (`SpeechRecognition` / `webkitSpeechRecognition`). Speech is converted locally in the browser into text inside the chat input box and submitted as normal text messages to `/api/agent/chat`.[^src-20261010-shutdownvoicefixes]
+The Agent page provides browser-based voice input powered by the Web Speech API (`SpeechRecognition` / `webkitSpeechRecognition`). The browser speech service transcribes voice into text inside the chat input box and the user submits it as normal text messages to `/api/agent/chat`.[^src-20261010-shutdownvoicefixes]
 * **Provider Independence**: Because recognition happens client-side before text transmission, microphone voice input is supported across all cloud AI providers (Google, OpenAI, Anthropic, Ollama Cloud) and does not require provider-level raw audio ingestion capabilities.[^src-20261010-shutdownvoicefixes] [^src-20261010-developmentguide-4]
 * **Component Lifecycle**: The speech recognition instance is tied to the Agent page lifecycle, ensuring recording aborts immediately upon route navigation or component unmount.[^src-20261010-shutdownvoicefixes]
 
 [^src-20261010-shutdownvoicefixes]: Server shutdown and browser voice regression repair evidence note.
 [^src-20261010-developmentguide-4]: Current versioned DevelopmentGuide (2026-10-11 shutdown & voice fixes).
+
+## Current control pages and acceptance — 2026-10-11
+
+Movement reads the existing server capability lists and posts selected actions directly without an Agent prompt. Distance remains millimetres from `/ws/distance`; invalid or disconnected telemetry displays unavailable. Chat retains the text `message`/`language` request, local conversation clearing and recognition abort on navigation. Recording is orange/white; idle is cyan outlined with a slashed microphone.[^src-20261011-developmentguide] [^src-20261011-webrefinementevidence]
+
+Both pages share a folded-by-default floating System Activity drawer containing timestamped `/ws/events` entries, local clear, Escape/collapse, independent scrolling and a 50-entry bound. The header stays above it. The power slider still requires staged intent and browser confirmation; viewport observation adjusts geometry only.[^src-20261011-developmentguide] [^src-20261011-webrefinementevidence]
+
+Four-language keys, frontend lint/build, inert session/stream checks and protected-core verification passed. The owner waived browser validation on Raspberry Pi Lite after startup attempts; no completed browser assertions or implemented-page screenshot review are claimed. Real mobile layout, microphone, ngrok, telemetry/output and controlled motion/power acceptance remain pending. Browser recognition is not guaranteed offline and depends on support, permission, secure context and its speech service.[^src-20261011-webrefinementevidence]
+
+[^src-20261011-developmentguide]: Web refinement current development guide (2026-10-11 web refinement).
+
+[^src-20261011-webrefinementevidence]: Web refinement code, design and local validation evidence (2026-10-11 web refinement).

## write wiki/entities/ninja-webapp.md
--- /home/rogerchang/NinjaRobotPi0/ninjarobot_pi0_Wiki/wiki/entities/ninja-webapp.md
+++ /home/rogerchang/NinjaRobotPi0/ninjarobot_pi0_Wiki/wiki/entities/ninja-webapp.md
@@ -52,53 +52,36 @@
   resource: urn:llmwiki:source:src-20261010-developmentguide-4
   title: Developmentguide
   content_hash: sha256:b82c27e23387051b0280adf428e34299bbfd65bcf2bcc80d3802027c4f3827bc
-semantic_review:
-  version: 1
-  performed_by: agent:antigravity
-  performed_at: '2026-10-10T17:23:23.105961+00:00'
-  target_hash: sha256:d9cf8f06faeb5ef4932a751a5e954af36ba560cca8ce6b06cb874d6c7073f9f1
-  result: passed
-  checks:
-    source_support: passed
-    contradictions: passed
-    limitations: passed
-    claim_strength: passed
-    visual_evidence: not_applicable
-  notes:
-  - Reviewed browser speech recognition decoupling from supports_audio flag against
-    Agent/index.jsx and ShutdownVoiceFixes.md.
-  - Mock browser test assertions passed; real microphone and physical device validation
-    remain pending.
+- id: src-20261011-developmentguide
+  resource: urn:llmwiki:source:src-20261011-developmentguide
+  title: Web refinement current development guide
+  content_hash: sha256:a3cbb8265b1fd651a73fcd826a58f239d60fd28f128d2b82de7d628fec8ec738
+- id: src-20261011-readme-current
+  resource: urn:llmwiki:source:src-20261011-readme-current
+  title: Web refinement corrected English README
+  content_hash: sha256:4058c6f103ff077f356228e7e4fb6728f5314b0c7602db00f231be8a08a5fc77
+- id: src-20261011-webrefinementevidence
+  resource: urn:llmwiki:source:src-20261011-webrefinementevidence
+  title: Web refinement code, design and local validation evidence
+  content_hash: sha256:5ce2540bcc10522fc7e7dd5d1295c9738c4b0ed695bc4f39359ba91ddf669e69
 ---
 
 # ninja_webapp Package
 
-## Current visual design
+## Current interface and contracts
 
-Current frontend metadata declares React 19.2.0; older React 18 descriptions are historical. The Pi5-derived navy/cyan tokens, panels, menu sheet and activity drawer apply to Pi0 Home, Agent and Help. Routes, request payloads, WebSocket events, millimetre units and existing action selectors remain Pi0-specific. BLE advertising is not controller connection. Four locale sets include previously missing labels; power still requires staged user action plus confirmation, with an accessible keyboard alternative.[^src-20261007-developmentguide-2]
+`ninja_webapp` is the existing React 19.2/Vite SPA with four locale bundles (`en`, `ja`, `zh-TW`, `zh-CN`). The owner-requested refinement changes frontend presentation only; backend/driver APIs, robot configuration, session ownership and shutdown confirmation remain unchanged. BLE advertising is distinct from web controller ownership.[^src-20261011-developmentguide] [^src-20261011-readme-current]
 
+## Application pages
 
-`ninja_webapp` is the modern web frontend for NinjaRobotPi0, previously described as React 18, Vite, and `react-router-dom`.[^src-20260822-readme] [^src-20260822-developmentguide]
+- **Home (`/`)** combines language, interface selection and confirmed System Power. It is also the hamburger-menu destination.
+- **Movement Tool (`/movement`)** contains live distance and server-supplied native movement, face and sound selectors. Execution uses the existing direct POST endpoints and does not call Ninja Agent.
+- **Chat (`/agent`)** contains conversation/local clear, a prompt/send row and browser voice transcription into the prompt. It keeps the existing `{message, language}` chat payload and aborts recognition on navigation.
+- **Legacy Help (`/help`)** redirects Home; the Help implementation is removed. Unknown frontend routes also return Home.[^src-20261011-developmentguide] [^src-20261011-readme-current]
 
-## Architecture & Technology
+Movement and Chat share a bottom System Activity drawer, folded by default and expanded above content with timestamp/message rows, local clear and independent scrolling. `/ws/distance` remains a separate millimetre stream; `/ws/events` supplies actual runtime activity. The header badge uses real `/ws/session` ownership, not BLE advertising. Mobile-first columns, bounded widths, wrapping forms/messages, safe areas and localized/document-language labels implement the supplied design.[^src-20261011-developmentguide] [^src-20261011-webrefinementevidence]
 
-* **Earlier framework description**: React 18 + Vite.[^src-20260822-developmentguide]
-* **Styling**: Vanilla CSS with curated responsive tokens and modern micro-animations.[^src-20260822-developmentguide]
-* **Internationalization**: `react-i18next` translations for English (`en`), Japanese (`ja`), Traditional Chinese (`zh-tw`), and Simplified Chinese (`zh-cn`).[^src-20260822-readme] [^src-20260822-developmentguide]
-* **Real-Time Communication**: `/ws/distance` supplies `distance_mm`; `/ws/events` supplies activity/log events. The old combined-distance description was documentation drift.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]
-
-## Application Pages
-
-* **Home (`/`)**: Hero branding display and interactive slide-to-confirm power-off slider for safe robot shutdown.[^src-20260822-developmentguide]
-* **Agent (`/agent`)**: Main control dashboard featuring:
-  * **AI Chat Dialog**: Conversational text and voice chat with active cloud provider (Google, OpenAI, Anthropic, Ollama Cloud) and capability-gated voice input.[^src-20260822-readme] [^src-20261010-modeladapterimplementation]
-  * **Hardware Quick Controls**: Direct triggering of facial expressions, sounds, and recorded movements.[^src-20260822-developmentguide]
-  * **Real-Time Telemetry**: Distance sensor reading display with safety indicators.[^src-20260822-readme] [^src-20260822-developmentguide]
-  * **Slidable System Log Panel**: Real-time log monitor for debugging and telemetry.[^src-20260822-developmentguide]
-* **Help (`/help`)**: User manual and quick reference documentation.[^src-20260822-developmentguide]
-
-[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.
-[^src-20260822-readme]: NinjaRobotPi0 Readme.
+Frontend lint/build, locale completeness, inert session/stream checks and protected-core verification passed. Browser validation was explicitly waived on the Pi Lite host; responsive/browser/device acceptance remains manual and is not implied by source checks.[^src-20261011-webrefinementevidence]
 
 ## Repository migration (2026-10-07)
 
@@ -115,14 +98,14 @@
 [^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.
 ## Shared session lifecycle and reconnect management (2026-10-10)
 
-`ninja_webapp` integrates session management in the shared application layout (`Layout.jsx`) using the `useRobotSession.js` hook.[^src-20261010-lifecyclerefinementsimplementationplan] A persistent `/ws/session` socket connects when the app mounts, carrying the server's HttpOnly session cookie across Home, Agent, and Help views. Heartbeat pings run every 10 seconds, with automatic retry every 3 seconds if disconnected. If a secondary browser attempts to connect while a session is active, the server closes the socket with code 4409, and the web app presents a busy modal preventing unauthorized control. The four locale bundles (`en`, `ja`, `zh-cn`, `zh-tw`) provide localized notifications for busy and reconnecting states.[^src-20261010-lifecyclerefinementsvalidation]
+`ninja_webapp` integrates session management in the shared application layout (`Layout.jsx`) using the `useRobotSession.js` hook.[^src-20261010-lifecyclerefinementsimplementationplan] A persistent `/ws/session` socket connects when the app mounts, carrying the server's HttpOnly session cookie across routes, now Home, Movement Tool and Chat.[^src-20261011-developmentguide] Heartbeat pings run every 10 seconds, with automatic retry every 3 seconds if disconnected. If a secondary browser attempts to connect while a session is active, the server closes the socket with code 4409, and the web app presents a busy status message preventing unauthorized control. The four locale bundles (`en`, `ja`, `zh-cn`, `zh-tw`) provide localized notifications for busy and reconnecting states.[^src-20261010-lifecyclerefinementsvalidation]
 
 [^src-20261010-lifecyclerefinementsimplementationplan]: Lifecycle refinements implementation plan.
 [^src-20261010-lifecyclerefinementsvalidation]: Lifecycle refinements validation report.
 
-## Voice capability gating and provider status display (2026-10-10)
+## Historical model-audio UI gating (2026-10-10, superseded)
 
-The Agent page consumes provider, model, and audio capability metadata from `/api/agent/status`.[^src-20261010-modeladapterimplementation] Voice recording controls are disabled with descriptive localized tooltips when the active model does not support native audio (OpenAI, Anthropic, Ollama Cloud, or non-allowlisted Google models). Backend voice endpoints reject audio payloads upfront if the active provider does not support it.[^src-20261010-modeladapterimplementation] A CSS stacking fix in `Agent.module.css` ensures navigation headers and menu sheets remain fully interactable above open activity panels.[^src-20261010-modeladapterimplementation] [^src-20261010-modeladaptervalidation]
+The earlier Agent page consumed provider, model, and audio capability metadata from `/api/agent/status`.[^src-20261010-modeladapterimplementation] That earlier implementation disabled voice recording controls with descriptive localized tooltips when the active model does not support native audio (OpenAI, Anthropic, Ollama Cloud, or non-allowlisted Google models). Backend voice endpoints reject audio payloads upfront if the active provider does not support it.[^src-20261010-modeladapterimplementation] A historical CSS stacking fix in `Agent.module.css` ensures navigation headers and menu sheets remain fully interactable above open activity panels.[^src-20261010-modeladapterimplementation] [^src-20261010-modeladaptervalidation]
 
 [^src-20261010-modeladapterimplementation]: Pi0 Cloud Model Provider Adapter implementation evidence.
 [^src-20261010-modeladaptervalidation]: Cloud model adapter validation report.
@@ -135,3 +118,11 @@
 
 [^src-20261010-shutdownvoicefixes]: Server shutdown and browser voice regression repair evidence note.
 [^src-20261010-developmentguide-4]: Current versioned DevelopmentGuide (2026-10-11 shutdown & voice fixes).
+
+The historical model-audio UI gate above was corrected before this refinement. Current Chat does not fetch provider audio metadata to gate its Web Speech microphone and makes no raw-audio API request. Availability depends on the browser speech service and permissions, not model audio-file capability.[^src-20261011-developmentguide] [^src-20261011-webrefinementevidence]
+
+[^src-20261011-developmentguide]: Web refinement current development guide (2026-10-11 web refinement).
+
+[^src-20261011-readme-current]: Web refinement corrected English README (2026-10-11 web refinement).
+
+[^src-20261011-webrefinementevidence]: Web refinement code, design and local validation evidence (2026-10-11 web refinement).

## write wiki/references/development-guide.md
--- /home/rogerchang/NinjaRobotPi0/ninjarobot_pi0_Wiki/wiki/references/development-guide.md
+++ /home/rogerchang/NinjaRobotPi0/ninjarobot_pi0_Wiki/wiki/references/development-guide.md
@@ -79,28 +79,19 @@
   resource: urn:llmwiki:source:src-20261010-shutdownvoicefixes
   title: Shutdownvoicefixes
   content_hash: sha256:bc56cba07d2aade0773ca839cb060aceb625af2a002344892a6e81f6c0b5c6fb
-semantic_review:
-  version: 1
-  performed_by: agent:antigravity
-  performed_at: '2026-10-10T17:23:23.105961+00:00'
-  target_hash: sha256:6e3753e732c3bfa06940ef04109bb924cf8f35c5074ac81ed05f0d7604fe0070
-  result: passed
-  checks:
-    source_support: passed
-    contradictions: passed
-    limitations: passed
-    claim_strength: passed
-    visual_evidence: not_applicable
-  notes:
-  - Reviewed current DevelopmentGuide (2026-10-11) manual pointers, shutdown sequence,
-    and regression test records.
-  - Offline test suites passed on Python 3.11 and 3.13; target-device hardware checks
-    remain pending.
+- id: src-20261011-developmentguide
+  resource: urn:llmwiki:source:src-20261011-developmentguide
+  title: Web refinement current development guide
+  content_hash: sha256:a3cbb8265b1fd651a73fcd826a58f239d60fd28f128d2b82de7d628fec8ec738
+- id: src-20261011-webrefinementevidence
+  resource: urn:llmwiki:source:src-20261011-webrefinementevidence
+  title: Web refinement code, design and local validation evidence
+  content_hash: sha256:5ce2540bcc10522fc7e7dd5d1295c9738c4b0ed695bc4f39359ba91ddf669e69
 ---
 
 # Current development manual
 
-Resolve the complete current DevelopmentGuide through project-knowledge.json or the wiki README. It documents protected core/driver functions, additive onboarding, UI contract preservation, immutable source versions, native built-in movement execution, and host/wiki validation. Root DevelopmentGuide.md is a compatibility pointer; earlier detailed API/history material is preserved as historical context.[^src-20261010-developmentguide-4]
+Resolve the complete current DevelopmentGuide through project-knowledge.json or the wiki README. It documents protected core/driver functions, additive onboarding, UI contract preservation, immutable source versions, native built-in movement execution, and host/wiki validation. Root DevelopmentGuide.md is a compatibility pointer; earlier detailed API/history material is preserved as historical context. The current complete English-only web-refinement version adds Home/menu, Movement and Chat guidance, preserved native/session/power contracts and the owner's browser-validation waiver.[^src-20261011-developmentguide]
 
 [Project overview](/overview.md).
 
@@ -161,7 +152,7 @@
 ## Lifecycle refinements and reconnect screen (2026-10-10)
 
 Movement-tool deliberate exit (option 6) validates and executes configured `Poweroff` before releasing hardware, without subsequent centering. When `Poweroff` is absent (Wheel/Humanoid), configured `home` is executed. HAL shutdown releases PWM rather than electrically holding the final pose.
-The web interface adds a single-browser session ownership contract: the shared layout maintains a persistent `/ws/session` socket and an opaque HttpOnly `ninja_web_session` cookie across Home, Agent, and Help views. Only one browser controls web APIs; another browser receives a busy 4409 modal and cannot trigger actions. Every `/api/` endpoint and auxiliary socket requires live primary ownership (returning 423 if inactive, 503 during shutdown). Browser disconnect or a 35s timeout cooperatively cancels pending browser tasks, aborts active native/Blockly work, and restores the waiting QR on the display while suppressing idle animations.[^src-20261010-developmentguide] [^src-20261010-lifecyclerefinementsevidence]
+The web interface adds a single-browser session ownership contract: the shared layout maintains a persistent `/ws/session` socket and an opaque HttpOnly `ninja_web_session` cookie across frontend routes (historically Home, Agent and Help). Only one browser controls web APIs; another browser receives a busy/4409 response and cannot trigger actions. Every `/api/` endpoint and auxiliary socket requires live primary ownership (returning 423 if inactive, 503 during shutdown). Browser disconnect or a 35s timeout cooperatively cancels pending browser tasks, aborts active native/Blockly work, and restores the waiting QR on the display while suppressing idle animations.[^src-20261010-developmentguide] [^src-20261010-lifecyclerefinementsevidence]
 
 ## CLI launcher recovery and single-ownership packaging (2026-10-10)
 
@@ -200,3 +191,11 @@
 
 [^src-20261010-developmentguide-4]: Current versioned DevelopmentGuide (2026-10-11 shutdown & voice fixes).
 [^src-20261010-shutdownvoicefixes]: Server shutdown and browser voice regression repair evidence note.
+
+## Current web refinement workflow — 2026-10-11
+
+The phased frontend plan and code review keep robot behavior unchanged. New complete manual/log versions and corrected English README evidence preserve registered originals; root README retains its four-language order. Local lint/build, locale/session/stream checks and core verification passed. Browser validation on Pi Lite was waived; controlled physical and real-browser checks remain pending.[^src-20261011-developmentguide] [^src-20261011-webrefinementevidence]
+
+[^src-20261011-developmentguide]: Web refinement current development guide (2026-10-11 web refinement).
+
+[^src-20261011-webrefinementevidence]: Web refinement code, design and local validation evidence (2026-10-11 web refinement).

## write wiki/concepts/development-workflow.md
--- /home/rogerchang/NinjaRobotPi0/ninjarobot_pi0_Wiki/wiki/concepts/development-workflow.md
+++ /home/rogerchang/NinjaRobotPi0/ninjarobot_pi0_Wiki/wiki/concepts/development-workflow.md
@@ -67,22 +67,14 @@
   resource: urn:llmwiki:source:src-20261010-shutdownvoicefixes
   title: Shutdownvoicefixes
   content_hash: sha256:bc56cba07d2aade0773ca839cb060aceb625af2a002344892a6e81f6c0b5c6fb
-semantic_review:
-  version: 1
-  performed_by: agent:antigravity
-  performed_at: '2026-10-10T17:23:23.105961+00:00'
-  target_hash: sha256:5ac953bf123f4300fb38192e7bd6e7e71e25e513b090f1e2b1f451188be73b28
-  result: passed
-  checks:
-    source_support: passed
-    contradictions: passed
-    limitations: passed
-    claim_strength: passed
-    visual_evidence: not_applicable
-  notes:
-  - Reviewed regression testing workflow, test_server_shutdown.py inert test suite,
-    and browser_ui.cjs mock assertions.
-  - Host test results documented; physical Raspberry Pi validation remains pending.
+- id: src-20261011-developmentguide
+  resource: urn:llmwiki:source:src-20261011-developmentguide
+  title: Web refinement current development guide
+  content_hash: sha256:a3cbb8265b1fd651a73fcd826a58f239d60fd28f128d2b82de7d628fec8ec738
+- id: src-20261011-webrefinementevidence
+  resource: urn:llmwiki:source:src-20261011-webrefinementevidence
+  title: Web refinement code, design and local validation evidence
+  content_hash: sha256:5ce2540bcc10522fc7e7dd5d1295c9738c4b0ed695bc4f39359ba91ddf669e69
 ---
 
 # Development and immutable documentation workflow
@@ -171,3 +163,13 @@
 
 [^src-20261010-developmentguide-4]: Current versioned DevelopmentGuide (2026-10-11 shutdown & voice fixes).
 [^src-20261010-shutdownvoicefixes]: Server shutdown and browser voice regression repair evidence note.
+
+## Frontend refinement and validation boundary — 2026-10-11
+
+The frontend-only refinement uses wiki evidence, current code and inspected owner mockups, then a phased plan and small presentation changes. It preserves robot/runtime/driver behavior, session ownership, native request contracts and power confirmation. Current complete English-only manuals remain immutable dated sources; root README alone keeps four languages.[^src-20261011-developmentguide]
+
+Frontend lint/build, four-locale completeness, inert session/auxiliary-stream checks and protected-core verification passed. The existing optional Playwright suite was updated for the new routes. The owner explicitly waived browser testing on Raspberry Pi Lite; there are no completed browser assertions or implemented-page screenshot acceptance results for this refinement. Real microphone/mobile/ngrok/hardware tests remain controlled owner acceptance. Wiki dependency setup occurred only after explicit authorization and retained project locks/system uv.[^src-20261011-webrefinementevidence]
+
+[^src-20261011-developmentguide]: Web refinement current development guide (2026-10-11 web refinement).
+
+[^src-20261011-webrefinementevidence]: Web refinement code, design and local validation evidence (2026-10-11 web refinement).

## write wiki/analyses/development-history-and-evolution.md
--- /home/rogerchang/NinjaRobotPi0/ninjarobot_pi0_Wiki/wiki/analyses/development-history-and-evolution.md
+++ /home/rogerchang/NinjaRobotPi0/ninjarobot_pi0_Wiki/wiki/analyses/development-history-and-evolution.md
@@ -108,23 +108,14 @@
   resource: urn:llmwiki:source:src-20261010-shutdownvoicefixes
   title: Shutdownvoicefixes
   content_hash: sha256:bc56cba07d2aade0773ca839cb060aceb625af2a002344892a6e81f6c0b5c6fb
-semantic_review:
-  version: 1
-  performed_by: agent:antigravity
-  performed_at: '2026-10-10T17:23:23.105961+00:00'
-  target_hash: sha256:95f5bef3fcd34403e11327199092122f0be2c4fd63ea82ae463a0932515339e3
-  result: passed
-  checks:
-    source_support: passed
-    contradictions: passed
-    limitations: passed
-    claim_strength: passed
-    visual_evidence: not_applicable
-  notes:
-  - Reviewed 2026-10-11 shutdown and browser voice regression milestone against DevelopmentLog.md
-    and ShutdownVoiceFixes.md.
-  - Chronological milestones reflect host-verified test suite results; physical hardware
-    verification remains pending.
+- id: src-20261011-developmentlog
+  resource: urn:llmwiki:source:src-20261011-developmentlog
+  title: Web refinement current development log
+  content_hash: sha256:db27140d13ea4df882914e313f8e2ed5e5684dae297f590a6985bac83951216b
+- id: src-20261011-webrefinementevidence
+  resource: urn:llmwiki:source:src-20261011-webrefinementevidence
+  title: Web refinement code, design and local validation evidence
+  content_hash: sha256:5ce2540bcc10522fc7e7dd5d1295c9738c4b0ed695bc4f39359ba91ddf669e69
 ---
 
 # Development History and Evolution
@@ -227,7 +218,7 @@
 ## Lifecycle refinements and reconnect screen (2026-10-10)
 
 Movement-tool deliberate exit (option 6) executes configured `Poweroff` (or `home` fallback) before HAL shutdown and configuration save, without subsequent centering. HAL shutdown releases PWM rather than holding torque.
-The web interface adds a single-browser session ownership contract: the shared layout maintains a persistent `/ws/session` socket and an opaque HttpOnly `ninja_web_session` cookie. Only one browser controls web APIs; another browser receives a busy 4409 modal and cannot trigger actions. Every `/api/` endpoint and auxiliary socket requires live primary ownership (returning 423 if inactive, 503 during shutdown). Browser disconnect or a 35s timeout cooperatively cancels pending browser tasks, aborts active native/Blockly work, and restores the waiting QR on the display while suppressing idle animations.
+The web interface adds a single-browser session ownership contract: the shared layout maintains a persistent `/ws/session` socket and an opaque HttpOnly `ninja_web_session` cookie. Only one browser controls web APIs; another browser receives a busy/4409 response and cannot trigger actions. Every `/api/` endpoint and auxiliary socket requires live primary ownership (returning 423 if inactive, 503 during shutdown). Browser disconnect or a 35s timeout cooperatively cancels pending browser tasks, aborts active native/Blockly work, and restores the waiting QR on the display while suppressing idle animations.
 The root package and virtual environment prompt are updated to `ninjarobotpi0`.[^src-20261010-developmentlog] [^src-20261010-lifecyclerefinementsimplementationplan] [^src-20261010-lifecyclerefinementsvalidation]
 
 ## CLI launcher recovery and packaging reconciliation (2026-10-10)
@@ -261,3 +252,13 @@
 
 [^src-20261010-developmentlog-4]: Current versioned DevelopmentLog (2026-10-11 shutdown & voice fixes).
 [^src-20261010-shutdownvoicefixes]: Server shutdown and browser voice regression repair evidence note.
+
+## Home, Movement and Chat presentation refinement — 2026-10-11
+
+The owner-requested frontend refinement combined Home with the menu, split direct native controls into Movement Tool, retained Chat at `/agent`, added the shared floating folded activity drawer and removed Help with a legacy redirect. It adopted the inspected voice active/idle references and added four-language labels/document language without changing robot/runtime/driver behavior or API/power contracts.[^src-20261011-developmentlog] [^src-20261011-webrefinementevidence]
+
+Frontend lint/build, locale/session/stream checks and protected-core verification passed. Browser startup attempts were stopped when the owner waived testing on Pi Lite; no completed browser assertions, implemented-page screenshot review, real microphone or hardware acceptance is claimed. New complete English manual/log versions, corrected English README evidence and current pointers preserve earlier sources.[^src-20261011-developmentlog] [^src-20261011-webrefinementevidence]
+
+[^src-20261011-developmentlog]: Web refinement current development log (2026-10-11 web refinement).
+
+[^src-20261011-webrefinementevidence]: Web refinement code, design and local validation evidence (2026-10-11 web refinement).

