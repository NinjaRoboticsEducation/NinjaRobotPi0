# NinjaRobotPi0 Web Interface Refinement — 2026-10-11

## Outcome and authorization

Implement the owner's five requested presentation refinements using the six supplied images. The owner's Step 5 authorizes frontend implementation and its named documentation/wiki updates. No risky robot/backend coding, live server startup, hardware operation, package installation, or deployment is included. Dependency installation requires separate authorization.

## Phase 1 — Evidence retrieval and current-code review

- Read `ninjarobot_pi0_Wiki/wiki/entities/ninja-webapp.md` and `wiki/concepts/web-interface-design.md`, the current DevelopmentGuide and registered shutdown/voice evidence (`src-20261010-developmentguide-4`, `src-20261010-shutdownvoicefixes`). Also use the existing lifecycle evidence cited by those pages for session ownership.
- Both frontend pages are draft and have recorded AI semantic reviews, not human/device acceptance. Historical Help/combined-dashboard and provider-audio-gating claims require correction in the named pages. Browser recognition uses the browser's speech service and is independent of the model's raw-audio capability; it is not guaranteed offline/local transcription.
- CLI search/source status are initially unavailable because the independent wiki environment is absent; read registered sources directly. `python3 scripts/wiki.py check` initially passes. Ask for explicit setup authorization while continuing frontend work.
- Review complete source for App, Layout, Header, Home, Agent, language/power components, session hook, CSS, i18n/locale files, browser fixtures and backend endpoint definitions. Direct file review is sufficient; Serena is optional.
- Current `/agent` combines distance, chat, three native-action selectors and an activity drawer. Header opens a separate menu containing Home/Agent/Help and languages. Layout holds session ownership and gates content. `/ws/distance` supplies `distance_mm`; `/ws/events` supplies runtime information. Native actions use direct POST endpoints; chat uses `{message, language}`. The power slider stages intent before browser confirmation.

## Phase 2 — Mockup review and presentation specification

Images are under `docs/validation/ui/WebInterfaceUI_Update/` and have been inspected directly:

- `Home and Hamburg Menu.jpg`: black background, cyan outlined navy shell, welcome heading, Language block, Control Interface block, orange Chat action, System Power block and slide control. Home is also the menu destination.
- `Movement tool Interface.jpg`: header with actual controller ownership status and hamburger link; vertically stacked distance, movements, faces and sounds; cyan outlines, orange execution buttons; collapsed activity tab at bottom. Robot capabilities/names remain server supplied; do not hardcode Spider or a capability list.
- `Chat Interface.jpg`: header, large conversation panel with Clear Messages, separate prompt/send row and full-width voice button; no hardware selector cards.
- `SystemLogPannel.jpg`: bottom drawer expands above page content, timestamp/message rows, clear control, independently scrolling history; tab remains usable and header stays above the drawer.
- `VoiceInputOn.png` / `VoiceInputOff.png`: orange/white active microphone, cyan outlined/slashed idle microphone. Use scalable SVG icons in code; preserve recognition startup/result/end/unmount behavior.

## Phase 3 — Small frontend changes

1. Retain `/` and `/agent`; add `/movement`. Remove the Help implementation and redirect legacy `/help` to Home so bookmarks remain usable. Unknown paths also return Home.
2. Keep one unchanged session ownership hook in Layout. Pass actual ownership status to Header; hamburger navigates directly to Home. Remove the separate menu dialog and presentation footer. Home has no duplicate header.
3. Build Home's three blocks with the existing language selector and unchanged power confirmation logic. Restyle slider only.
4. Move the existing native capability fetching and direct-action endpoint mapping to Movement. Preserve names, units, methods and payloads. Disable controls for empty/unavailable capabilities; show failure in activity.
5. Keep Agent's text/voice lifecycle and chat payload. Add local conversation clearing and presentation labels. Do not call raw-audio/provider-specific services.
6. Extract shared activity state/socket handling and drawer for both pages. Keep up to 50 real events, clear displayed entries locally, use timestamp columns and a collapsed-by-default fixed panel. Preserve BLE code-received display in Chat. Clean up sockets and recognition on navigation. Handle malformed/disconnected telemetry without crashing or displaying a stale reading as live.
7. Add every new UI label in English, Japanese, Traditional Chinese and Simplified Chinese; persist language and synchronize the document language. Future project documentation remains English-only except root README.

## Phase 4 — Local lint and inert browser validation

- Run `npm run lint` and `npm run build` using existing frontend dependencies. Build output is required for the backend's existing dist serving; preserve unrelated preexisting changes.
- Update `tests/browser_ui.cjs` with inert API/WebSocket/speech fixtures. Never launch the robot server. Verify route navigation and stable session ownership, native-action POST endpoints, absence of chat calls from Movement, telemetry, log streaming/clearing/folding, chat payload, clear messages, voice state/transcription/unmount abort, empty lists, failed requests, session busy/disconnect and cancelled power confirmation.
- Check all four locales at 320, 360, 390 and 430 pixel portrait widths, mobile landscape, tablet and desktop. Assert no horizontal content overflow, usable controls, drawer/header stacking and accessible keyboard controls. Capture screenshots and inspect representative layouts against mockups. Browser execution depends on an already installed automation module/browser; report unavailable tools rather than install without approval.
- Run the existing inert `tests/web_session_hook.cjs` and `python3 scripts/verify_core.py`. Compare protected source diff against the initial working tree; no robot source modifications are allowed.

## Phase 5 — Documentation and reviewed wiki completion

- Create complete English-only new dated versions of DevelopmentGuide and DevelopmentLog; keep InstallationGuide unchanged unless setup information actually changes. Update root navigation pointers and root README's four language sections to describe Home, Movement and Chat.
- Create an English evidence/validation note identifying actual checks and pending device acceptance. Preserve all registered originals.
- Named semantic wiki scope: `wiki/entities/ninja-webapp.md`, `wiki/concepts/web-interface-design.md`, `wiki/references/development-guide.md`, `wiki/concepts/development-workflow.md`, and `wiki/analyses/development-history-and-evolution.md`. Update only affected claims, correct superseded historical voice/menu claims with citations and keep limitations explicit.
- Register/normalize new source versions using the existing CLI after separately authorized setup. Prepare schema-v2 plans with expected source/target hashes, display their exact semantic diffs before applying, then record source-grounded AI reviews without human-verification claims. This named scope is included in the owner's implementation request; expanded semantic scope requires new approval.
- Review changed/new implementation files before updating knowledge fingerprints. Run knowledge check, strict lint, link check, index check and stats. Do not call the task complete while required wiki updates remain unapplied; report any externally blocked gate explicitly.

## Phase 6 — Raspberry Pi acceptance and handoff

- Record a `pi-validation` report separating host mocks from pending owner-operated checks: local/ngrok entry, four languages, mobile browsers, microphone permission/recognition, real telemetry/events and controlled native actions.
- No hardware operations are authorized in this host validation. Movement, faces, sounds and shutdown require explicit physical readiness; shutdown may move the robot to Poweroff and halt the OS. Keep the robot supported and use its current approved calibration/safety guidance.
- Rollback is the previous frontend source/build; backend APIs, runtime, drivers and settings remain unchanged.
- Handoff reports changed frontend/docs/tests, actual results, evidence pages/source IDs, wiki status/drift and pending Pi/browser verification.


## Owner steering and executed scope

The owner explicitly waived browser validation on Raspberry Pi Lite during implementation. Stop browser launch/testing attempts. Browser matrix and screenshot acceptance remain optional/manual, with no completed result claimed. Required local validation is frontend lint/build, inert session checks, locale completeness, protected-core verification, source review and the wiki completion gate. Retain an updated optional browser fixture suite for a suitable development host; do not add browser packages to this Pi.


## Final execution record

Frontend implementation and the required local lint/build, locale, session/stream, protected-core and wiki gates are complete. The six design references were inspected. Browser testing was stopped and waived on this host by the owner; physical acceptance remains pending. All named semantic updates and their AI reviews were applied after exact-diff publication. The knowledge map has no current source/code drift; strict wiki lint has zero errors/warnings with four retained historical unused-source suggestions. The copied-log link issue was corrected in a new complete immutable source version, preserving its registered predecessor. See the validation report for executed checks, source IDs, changed file groups and controlled-device follow-up.
