# Web interface refinement validation — 2026-10-11

## 1. Scope of validation

Frontend presentation only: combined Home/menu, dedicated native Movement Tool, Chat/voice, shared floating activity drawer and Help removal. Preserve runtime/driver functions, HTTP request contracts, calibration, session ownership and power confirmation. Implementation plan: [NinjaRobotPi0WebRefinement_261011.md](../../DevelopmentPlanDoc/NinjaRobotPi0WebRefinement_261011.md).

## 2. Environment and prerequisites

Local Raspberry Pi Zero 2W workspace, Node 24.21.0, installed Chromium, existing frontend dependencies and Python 3.13.5. Automated UI tests serve only static built files and replace fetch/WebSocket/SpeechRecognition with inert fixtures. No robot server/device tool is started. The dedicated wiki environment was initially absent; explicit owner authorization allowed locked setup and evidence preparation. Existing uv 0.9.26 failed the wiki's >=0.11 requirement; `uv tool run --no-config --from 'uv>=0.11.0' uv sync --directory <wiki-path> --locked --all-extras` installed only the separate locked wiki environment using a cached compatible tool, without replacing system uv or changing locks. Available RAM is about 415 MB; run memory-intensive build/browser checks sequentially.

## 3. Safety notes

No live servo, GPIO, buzzer, display, provider, microphone or shutdown request is part of automated validation. Existing pigpio/system processes are left alone. The robot's real server can initialize/center hardware, native actions may move/energize devices, and confirmed shutdown may execute Poweroff before halting Linux. Physical readiness is required before owner-controlled checks. Use current calibration and supported clearance/power guidance; mockups are not hardware evidence.

## 4. Safe smoke tests

Run in the existing checkout without starting the backend:

```bash
cd ninja_webapp
npm run lint
npm run build
cd ..
node tests/web_session_hook.cjs
python3 -B scripts/verify_core.py
UI_SCREENSHOTS=/tmp/ninja-web-refinement-screenshots node tests/browser_ui.cjs ninja_webapp/dist
```

The optional browser harness uses an existing Playwright installation on a suitable development host; set `PLAYWRIGHT_MODULE` if its module is outside normal resolution. It serves a temporary static site with inert requests/sockets/speech. The owner waived this check on Raspberry Pi Lite, so no browser dependencies were installed and no completed browser result is claimed. Production build output is retained in the existing dist directory for normal backend serving. Initial frontend dist/bytecode edits predated this task; unrelated bytecode is preserved.

## 5. Communication/interface tests

The optional inert browser matrix is designed to cover 320×568, 360×800, 390×844, 430×932, 844×390, 768×1024 and 1280×900. Every viewport checks English/Japanese/Traditional Chinese/Simplified Chinese labels, document language, navigation, no horizontal overflow, session persistence, chat payloads, recognition locale/start/stop/abort, conversation clear, direct native endpoints, event/log streaming/clear/fold/Escape, telemetry handling, Help redirect. Cancelled staged power confirmation must send no shutdown request.

Pending owner checks: open the existing approved server's local and ngrok URLs and confirm Home is the entry page; inspect iOS/Android safe areas, mobile keyboard and landscape layout; confirm Voice Input with real browser permission and supported recognition service; test an unavailable/denied microphone; verify a second browser remains blocked and normal session reconnect remains functional. Starting/restarting the server requires physical readiness because it can initialize hardware. Remote browsers generally need HTTPS for microphone access; localhost is browser-specific secure-context handling.

## 6. Sensor/display checks

The optional browser fixtures provide valid/negative distance readings, native capability lists and live event messages. Source review covers malformed/disconnected telemetry handling. Browser execution was waived on this host; these fixtures do not establish live sensor behavior. Pending: verify actual distance changes in millimetres, actual event messages and reconnect recovery. Faces/sounds are preserved direct controls; pressing their real execution buttons energizes the display/buzzer and requires readiness. No physical sensor/display acceptance is inferred from Chromium screenshots.

## 7. Actuator-moving or power-risk tests

Owner-controlled and pending: support the robot, verify existing calibration/wiring and clear its travel area; select a short known movement and execute it once from Movement Tool with no Agent prompt. Verify its existing motion behavior. In a separate ready session, issue a harmless Chat prompt and confirm the existing agent workflow. Finally test the Home power slider and confirmation only when safe to execute Poweroff and halt the Pi. Confirm the OS has halted before power removal. Do not use the mockup's Spider example as proof of compatibility for another robot type.

Relevant existing evidence: [web design](../../ninjarobot_pi0_Wiki/wiki/concepts/web-interface-design.md), [frontend package](../../ninjarobot_pi0_Wiki/wiki/entities/ninja-webapp.md), current guide resolved by [project-knowledge.json](../../ninjarobot_pi0_Wiki/project-knowledge.json), and registered shutdown/voice evidence `src-20261010-shutdownvoicefixes`. These pages are draft/unverified; their AI semantic reviews do not establish physical acceptance.

## 8. Expected outcomes

Home provides language, interface and power blocks. Hamburger navigation returns there. Movement performs native requests without chat calls; Chat retains `/agent` and the `{message, language}` contract. Activity floats above content and stays folded by default. Voice active/idle matches the inspected references. Local clear controls affect displayed history. Robot/backend/driver behavior remains unchanged. All four UI languages fit the viewport; documentation remains English-only outside root README.

## 9. Execution status and evidence

- Initial knowledge check: passed before edits; initial CLI retrieval unavailable, then succeeded after authorized wiki setup/prepare.
- Six supplied mockups visually inspected before implementation; source evidence is listed below.
- Session lifecycle harness and protected-core check: passed. Locale completeness check passed: all four locale files have the same 77 keys and all literal JSX translation references resolve. Optional browser harness syntax check passed. An inert auxiliary-stream harness passed URL construction, message delivery, unavailable reporting, 3-second reconnect, stale-message filtering and unmount cleanup.
- Initial frontend ESLint and production build: passed. Final production rebuild passed and includes viewport-aware slider geometry; final frontend ESLint passed without warnings/errors.
- Chromium startup attempts timed out; one later isolated attempt reached a debugging port. The owner then explicitly waived browser validation on Raspberry Pi Lite. All browser attempts were stopped. No browser assertions, visual screenshot acceptance or physical operation are claimed.
- Baseline strict wiki lint: zero errors/warnings, with three new unregistered-source suggestions during drafting.
- Browser matrix and screenshot inspection: waived by owner on this host; manual acceptance remains pending. Final knowledge check, strict wiki lint, link check, index check, stats, core verification, session harness, optional browser-suite syntax and whitespace checks all passed (exit 0). Strict lint: zero errors/warnings and four unused historical source-citation suggestions. All 27 sourced pages have current passed AI semantic reviews (100% coverage); they remain draft/unverified by humans. No current source/code mapping drift remains.
- The first completion gate found a copied-log relative link to ShutdownVoiceFixes.md. A new complete link-corrected log version and final README snapshot were registered; the earlier registered versions were preserved. Current pointers and the named history/frontend citations were updated through the reviewed corrective plan.
- Actual robot-connected telemetry, microphone, native motion/output and power-off checks: not executed.

## 10. Pass/fail checklist

- [x] Existing code, wiki and six design images reviewed.
- [x] Session lifecycle and protected-core checks passed.
- [x] Final frontend lint/build passed.
- [ ] Optional browser matrix passed on a suitable host (waived here by owner).
- [ ] Implemented-page screenshots visually reviewed (waived here by owner; reference images were inspected).
- [x] Named source updates, semantic plans/reviews and knowledge/wiki gates passed.
- [ ] Real mobile browser, microphone and ngrok acceptance completed by owner.
- [ ] Controlled native actions, live telemetry and confirmed power-off accepted by owner.

## 11. Rollback steps

Restore the previous frontend source/build in a maintenance window, preserving later user edits and the preexisting working-tree changes. No backend, driver, calibration, credentials, robot settings or dependency-lock rollback is required. Preserve immutable wiki sources/history and use reviewed corrective versions/plans if documentation is reverted. Do not restart the robot server merely to test a rollback without physical readiness.

## Inspected design evidence

These are direct visual observations of owner-supplied images, not OCR or physical acceptance.

| File | SHA-256 | Observed presentation |
|---|---|---|
| Home and Hamburg Menu.jpg | `6a57a6af21616d6ceafeac6cf6dfa5f0f7ef7834363b43d69643c4bcb7ea40b3` | Home shell with language/control/power blocks, cyan outlines and orange Chat action. |
| Movement tool Interface.jpg | `b0a7a4838354af379a1cb75e0409e036f34dee2a8553a0d9a31cfd547ea3d993` | Distance, movement, face and sound cards in that order; orange execution controls. |
| Chat Interface.jpg | `299fdd48fe38ad004879b1e153230b4aea92a16d7f90ec82183bcc12432091e7` | Conversation with clear control, separate prompt/send row and full-width voice control. |
| SystemLogPannel.jpg | `96418403672a818dcae06ab990cdc70658d3329c575225a1b0dd8a0bb7674271` | Expanded dark bottom drawer overlays content with timestamp/message rows and clear control. |
| VoiceInputOn.png | `3dde5701d924b73c3a60aaa6228bf03f360fa435705f4d8b6a62555377b740fe` | Orange active button, white microphone and label. |
| VoiceInputOff.png | `db78383d85d07a257af26c5480d32c2a57c41ac93a2f8b97aa71d8e55e592ac3` | Cyan outlined idle button with slashed microphone and cyan label. |


## Changed files and handoff

- Frontend: App routes; Home, Movement and Chat pages/CSS; shared Header/Layout; language and power presentation; new SystemActivity component and auxiliary activity/stream hooks; i18n and four locale bundles; rebuilt production dist assets. Removed Help source and redirected its bookmark. Existing Footer source remains unused; robot/backend/driver functions are unchanged.
- Tests: updated the optional `tests/browser_ui.cjs` fixture suite; syntax checked only. Existing session harness and a temporary inert stream harness passed. No new browser/test packages were installed.
- Documentation: requested phased plan, root README in its four-language order, DevelopmentGuide/DevelopmentLog navigation pointers, complete English-only new guide/log sources, immutable English README versions, code/design evidence and this validation report. Skills, install/workflow scripts, InstallationGuide content and dependency locks are unchanged.
- Wiki: five named pages, source catalog, generated indexes/log, current manual/implementation map and three exact-diff artifacts. Initial, review and corrective plans were shown before their approved-scope applications. AI source review is not human/physical verification.

Evidence used: draft frontend/design pages, current code/endpoint definitions and registered `src-20261010-developmentguide-4` / `src-20261010-shutdownvoicefixes` plus their cited lifecycle sources. Current new sources include `src-20261011-developmentguide`, `src-20261011-developmentlog-2`, `src-20261011-readme-final` and `src-20261011-webrefinementevidence`; earlier candidate versions remain immutable provenance. Resolve the current complete manuals using project-knowledge.json. The four unused-source suggestions concern retained historical frontend source entries, not changed hashes or current source drift.

Remaining acceptance: actual mobile-browser layout/keyboard/safe areas, microphone permission and speech service, ngrok/local entry, live telemetry/events, controlled native output/motion and confirmed power-off. Browser validation on the Pi was explicitly waived by the owner. No robot runtime, device tool, microphone, provider or OS-shutdown action was executed by this task. The built frontend is available in `ninja_webapp/dist`; no deployment or server restart was performed.
