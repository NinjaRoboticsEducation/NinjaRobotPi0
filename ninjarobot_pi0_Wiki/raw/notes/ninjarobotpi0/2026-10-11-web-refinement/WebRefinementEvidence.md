# Web interface refinement evidence — 2026-10-11

## Scope and source/code audit

The owner requested a frontend-only refinement and explicitly authorized implementation after wiki retrieval, code review and a written phased plan. The owner later waived browser validation on Raspberry Pi Lite. No robot server/device tool, microphone, native action, provider request or shutdown was operated. Backend/driver functions, configuration, calibration, dependency locks, BLE protocol and OS power behavior are unchanged. Existing unrelated bytecode edits were preserved.

The original frontend combined distance, chat and native controls on `/agent` and had a separate Home/Agent/Help menu sheet. Current source was reviewed for App/Layout/Header/Home/Agent, power/language components, session hook, CSS/i18n/locales, tests and backend endpoint definitions. The draft wiki frontend/design pages had current AI reviews but also historical Help, combined-dashboard and provider-voice-gating claims. Current browser voice is provider-independent transcription into text, subject to browser support, permission, secure context and the browser speech service; it is not guaranteed offline/local speech processing.

## Implemented presentation and preserved contracts

- Home `/` combines language, control-interface and System Power blocks. It is the menu destination. Movement and Chat hamburger links go there directly. Legacy `/help` and unknown frontend paths redirect Home; Help source is removed.
- Movement Tool `/movement` shows distance, movements, faces and sounds. It uses server-supplied names and the same native capability GETs and execution POSTs: `/api/servos/movements/{encoded-name}/execute`, `/api/display/expressions/{encoded-name}`, `/api/sound/emotions/{encoded-name}`. It makes no Agent chat request. Empty lists disable controls; rejected requests are logged. Distance comes from `/ws/distance`, accepts the existing `distance_mm`/legacy `distance` fields and displays unavailable for malformed/negative/disconnected readings.
- Chat `/agent` contains conversation/local clear, a prompt/send row and full-width voice control. It preserves `/api/agent/chat` with `{message, language}` and browser recognition locale/start/result/end/unmount behavior. Active voice is orange/white; idle voice is cyan outlined with a slashed microphone. Transcription fills the prompt for review before Send. No raw-audio/provider-specific endpoint is added.
- Both pages use a collapsed-by-default bottom System Activity drawer. It expands above content, includes timestamp/message rows, up to 50 real `/ws/events` entries, local clearing, Escape/collapse and independent scrolling. The header remains above the drawer. Auxiliary streams retry after 3 seconds and close on navigation. Chat still displays BLE code-received content.
- Shared Layout retains the unchanged `/ws/session` ownership hook and content gating. Controller active means actual web session ownership, not BLE advertising. Power uses the existing staged gesture/keyboard confirmation and unchanged shutdown POST. ResizeObserver adjusts slider geometry only.
- All four UI languages have the same 77 translation keys; literal JSX translation references resolve. Language persists and updates the HTML language. Mobile-first single columns, fluid spacing/type, bounded widths, wrapping text, min-width-zero form fields, safe-area padding and a scrollable fixed drawer are implemented. Browser/device acceptance was waived here; responsive correctness is not claimed as physically observed.

## Actual local validation

Frontend ESLint passed without warnings/errors. The final Vite production build passed, with 97 modules and generated dist assets; it includes the final slider geometry fix. `node tests/web_session_hook.cjs`, `python3 -B scripts/verify_core.py`, optional browser harness syntax and four-locale completeness checks passed. A temporary inert auxiliary-stream harness passed URL construction, message delivery, unavailable callbacks, 3-second reconnect, stale-message filtering and unmount cleanup.

Initial Chromium startup attempts timed out on the low-memory target. A later attempt reached a debugging port but was stopped when the owner waived browser validation. No completed browser assertions or implemented-page screenshot review are claimed. The existing optional Playwright static fixture suite was updated for a suitable development host. No browser packages were installed. Actual mobile browsers, ngrok, microphone, live telemetry, native hardware output and shutdown remain owner-operated acceptance checks.

The initial project knowledge gate passed. The missing independent wiki environment was installed only after explicit owner authorization, using a temporary compatible uv because the installed 0.9.26 failed the wiki >=0.11 requirement. Locked wiki setup and preparation completed without robot/package-lock modifications. Baseline strict wiki lint had zero errors/warnings; final source/mapping/semantic-plan gates follow this evidence capture. AI review is not human verification or physical acceptance.

## Documentation and source boundaries

The plan is `DevelopmentPlanDoc/NinjaRobotPi0WebRefinement_261011.md`; validation is `docs/validation/WebRefinement-2026-10-11.md`. New complete English-only DevelopmentGuide/DevelopmentLog versions and English README snapshots live under the dated web-refinement raw directories. Root README retains English → Japanese → Traditional Chinese → Simplified Chinese. Root manual files are current navigation pointers. InstallationGuide and skills/workflow code are unchanged.

The first registered README snapshot was captured before a later audit corrected remaining introductory Help references. It remains immutable; `README-current.md` is the corrected current English snapshot. Current named wiki scope is frontend package, web design, development guide/workflow and development history. All earlier registered sources are retained.

## Directly inspected design references

The six owner-supplied images were visually inspected before coding, without OCR or image generation. The Home reference has language/control/power blocks; Movement orders distance/movements/faces/sounds; Chat has conversation/clear, prompt/send and full-width voice; the system-log reference shows a floating bottom drawer with timestamp/message rows. VoiceInputOn uses orange/white and VoiceInputOff uses a cyan outline/slashed microphone. These are design observations, not hardware capability evidence; the mockup's Spider name/actions are not hardcoded into the application.

The exact image SHA-256 inventory and pending controlled-device checks are in the linked validation report. No sanitized image publication is needed because no image asset is imported into the wiki or UI; the UI uses code/SVG/native controls.
