# Web gamepad and palette refinement validation — 2026-10-13

Status: approved implementation completed and locally validated. Native Chrome/Safari phone acceptance and physical robot movement acceptance remain pending. This is a new English raw source candidate; no registration, normalization, ingestion, semantic review, wiki plan application, pointer or implementation-map update was performed.

## Approval and evidence

The owner approved [NinjaRobotPi0WebRefinement_261013.md](../../../../../DevelopmentPlanDoc/NinjaRobotPi0WebRefinement_261013.md), explicitly accepting finish-current-cycle release behavior and disabled unsupported/Tire controls. Initial code baseline was commit `78dde3f`. Owner image removals in the old `03 NinjaRobot Web Interface UI` folder and the newly supplied `NinjaRobotPi0 web UI update 261013` images were preexisting and preserved.

Read-only wiki retrieval used concepts/web-interface-design.md, entities/ninja-webapp.md and concepts/motion-system-and-easing.md. All are draft/unverified, with recorded agent semantic reviews passed on 2026-10-11 for the UI pages and 2026-10-13 for motion. Review does not prove physical acceptance. Current complete guide/log sources were resolved from project-knowledge.json (`src-20261013-developmentguide-3`, `src-20261013-developmentlog-3`); their hashes were checked and originals preserved. The initial knowledge gate passed.

All six owner references were visually inspected: Hamburg Menu.jpg, Movement tool Interface.jpg, Chat Interface.jpg, SystemLog.jpg, GamePad.png and GamePad_Plassed.png. Serena and exact code inspection verified the existing native execution endpoint, completion response, controller locking, action catalogs and stop-executor distinction. Both directional catalogs have 37 steps per specified direction and one Home step. No elapsed physical cycle duration was inferred.

## Implemented behavior

- Home default links and header hamburger use medium blue fills; Home selection remains single-orange and resets on reload. Power uses an orange/white thumb and a centered blue label, retaining its previous gesture/keyboard confirmation.
- Voice Input and folded System Activity use blue/white; recording/open activity use orange/white. Existing chat and log behavior is preserved.
- Specified card/panel and colored-message borders use cyan alpha 0.25; assistant-message borders retain gray alpha 0.25. This implements 75% transparency of borders only.
- Movement Tool has unboxed upper-left millimetre distance, a centered cross-shaped pad and three selector cards without description paragraphs. Its landscape layout uses pad and selector columns; exceptionally short/enlarged layouts retain reachable internal scrolling. Document viewport locking, safe areas and fullscreen behavior remain.
- Spider/Humanoid mappings use exact run_forward, run_backward, turn_left, turn_right and home names, conditioned on the actual server-advertised list. Tire, unknown types and missing actions are disabled with localized information.
- Directional holds issue one POST at a time, awaiting exact successful executed completion before repeating. Release prevents another cycle and clears orange immediately; the submitted cycle may finish. Home runs once, while remaining orange until input release. Assistive clicks intentionally issue one cycle.
- Pointer capture, input identity, keyboard autorepeat rejection, focus/blur, hiding/pagehide, opening activity, unmount/session loss and errors invalidate hold intent. A late response cannot revive it. Pad and native Movement selector share a request lock that persists across route navigation, preventing a queue of physical commands.
- A 4xx rejection ends repetition and permits a fresh intentional press. Network/5xx/unconfirmed completion latches an unknown-status lock across routes. The displayed message requires checking the robot before reloading. Browser reload clears this local latch; it is not a stop or completion guarantee. No new backend cancellation contract is claimed.

The backend, drivers, movement data, configuration, calibration, endpoint implementations and protected baseline were unchanged. No hardware, live backend, shutdown, cloud/ngrok, production service or deployment ran. No dependency/lockfile changes or installs occurred.

## Changed code and artifacts

Existing source changes: index.css; Home/Movement/Agent CSS; Header/PowerOffSlider/SystemActivity CSS; Layout.jsx adds existing robotType to Outlet context; Movement/index.jsx composes and gates the pad and serializes selector movement; SystemActivity.jsx calls a frontend release callback on opening. Four locale bundles add the same gamepad keys.

New source: components/common/GamePad.jsx and GamePad.module.css; hooks/useGamePad.js; utils/nativeMovement.js. The shared utility retains unresolved/uncertain request state across Movement page mounts. All native command endpoints/payloads are unchanged.

Tests: existing tests/browser_ui.cjs extended without removing session/fullscreen/voice/native API/confirmation coverage; new tests/browser_gamepad.cjs adds controlled delayed responses and input lifecycle cases. New complete [DevelopmentGuide.md](../../../articles/ninjarobotpi0/2026-10-13-web-gamepad/DevelopmentGuide.md) and [DevelopmentLog.md](DevelopmentLog.md) preserve complete current English content, update current UI guidance and rebase links; their older dated claims remain historical.

The standard Vite build regenerated the tracked dist bundle; generated files were not hand-edited. Tested temporary build and served dist bytes match. Final bundle: assets/index-EacJI26f.css (18.47 kB) and assets/index-BkTd-qRY.js (321.46 kB).

## Local validation actually executed

| Check | Result |
| --- | --- |
| npm run lint | Passed, no lint diagnostics |
| npm run build -- --outDir /private/tmp/pi0-gamepad-build | Passed |
| npm run build | Passed; served artifact parity verified |
| node --check tests/browser_ui.cjs and tests/browser_gamepad.cjs | Passed |
| tests/browser_ui.cjs against final build | 1,043 inert Chromium assertions passed |
| tests/browser_gamepad.cjs against final build | 117 delayed-response checks passed |
| node tests/web_session_hook.cjs | Passed |
| Four-locale key parity | Passed |
| python3 scripts/verify_core.py | Passed; protected baseline unchanged |
| git diff --check | Passed |
| Current mapped manual hashes and local links in new documents | Verified |
| Read-only wiki strict lint, links and indexes | Passed; no errors or warnings, source suggestions remain |
| python3 scripts/wiki.py check after UI changes | Expected implementation-map drift; not refreshed because ingestion/review is deferred |

Browser tests used installed Node/Playwright and a localhost static server. APIs, WebSockets, speech and power confirmation were mocked; external requests were denied. Chromium was installed; no Firefox/WebKit browser validation is claimed. Tests are software evidence, not real motor or speech-service acceptance.

Responsive matrix: 320×568, 360×640, 360×800, 390×670, 390×740, 390×844, 430×932, 568×320, 844×390, 768×1024 and 1280×900. English, Japanese, Traditional Chinese and Simplified Chinese were checked for keys, labels, document language, geometry, minimum targets and reachability. Visual viewport toolbar/keyboard resizing and 150% text enlargement on representative Chat/Movement pages were exercised. Short/enlarged screens can scroll internally to reach all controls.

The gamepad checks cover all ten exact mappings, real mouse capture/release outside the pad, switching focus from one direction to another without cancelling the new hold, real touch tap, keyboard hold/autorepeat, Home once, assistive click, stale pointer release, secondary pointer rejection, selector duplicate requests, cancellation/lost capture, blur/focus, visibility/pagehide, overlay opening, route unmount/remount and session loss/recovery. Delayed success, 404/409/422/423 rejection, 503/network/unconfirmed response, missing capability, Tire and unknown types were validated without physical execution. A test-only strict-selector ambiguity was corrected; it did not require a product change. Screenshot capture waits for fonts/two paint frames. The bundled headless Chromium intermittently omitted layers that DOM/hit tests confirmed present. An already installed alternate Chromium produced a complete independently captured Movement preview and passed the responsive suite. Review screenshots were recaptured with that executable and an independent settled-fixture preview. Some Chat captures still omit header layers despite DOM/hit checks; those captures are limited visual evidence. The independently inspected Movement preview includes the complete shared header and all controls, consistent with a headless capture issue; native browser acceptance remains pending. Browser runners accept optional PLAYWRIGHT_EXECUTABLE_PATH to select an existing executable without installation.

## Retained visual evidence

Screenshots show inert Chromium fixtures and contain no real robot/account credentials. Representative Home, selected Home, Movement, Chat, open/long activity, held Humanoid button, enlarged Japanese Movement and short landscape were visually inspected.

- [Home default](../../../media/ninjarobotpi0/2026-10-13-web-gamepad/home-390x740.png)
- [Home selected](../../../media/ninjarobotpi0/2026-10-13-web-gamepad/home-selected-390x740.png)
- [Movement](../../../media/ninjarobotpi0/2026-10-13-web-gamepad/movement-390x740.png)
- [Chat — header capture limited](../../../media/ninjarobotpi0/2026-10-13-web-gamepad/chat-390x740.png)
- [Open activity](../../../media/ninjarobotpi0/2026-10-13-web-gamepad/long-log-390x740.png)
- [Held gamepad](../../../media/ninjarobotpi0/2026-10-13-web-gamepad/gamepad-pressed.png)
- [Enlarged Japanese Movement](../../../media/ninjarobotpi0/2026-10-13-web-gamepad/movement-enlarged-ja-390x740.png)
- [Short landscape](../../../media/ninjarobotpi0/2026-10-13-web-gamepad/movement-568x320.png)

## Owner acceptance pending

First inspect the revised build in native Chrome and Safari, normal/fullscreen, portrait/landscape, browser toolbar changes, enlarged text, all four languages and keyboard/focus as applicable. Check Home palette/selection, border transparency, power label without confirming shutdown, voice input and activity states. Physical microphone service behavior remains browser-dependent.

Gamepad hardware acceptance is actuator-moving work: use the actual calibrated supported robot, clear movement space, appropriate support, verified joint direction/limits and a ready owner. Begin with one short direction press, observe the full remaining cycle after release, then test each mapping, a sustained hold and Home. Confirm no second cycle after release and no automatic resume after focus/session changes. The release tail may be a complete 37-step motion, not immediate stopping. Do not test movement or power simply by opening a document or running host browser tests.

If a response is lost, stop issuing commands and inspect the robot before deliberately reloading. The UI does not supply an emergency-stop mechanism. Existing server session/safety checks remain their existing behavior and limitations.

Future owner ingestion targets are named in the approved plan. Current wiki catalogs/pages/maps/pointers were intentionally preserved; do not interpret existing reviews as reviews of this new source.

## Rollback

Restore only this task's frontend source/test changes from baseline commit 78dde3f, remove its newly added pad/scheduler test/source files if reverting the feature, and regenerate dist with the existing npm build. Preserve owner image changes, robot calibration/configuration and all other existing work. Stop any deliberate physical validation before rebuilding/reloading. Preserve these raw documents as provenance rather than overwriting registered sources or history. No robot runtime rollback is needed because this task did not modify it.
