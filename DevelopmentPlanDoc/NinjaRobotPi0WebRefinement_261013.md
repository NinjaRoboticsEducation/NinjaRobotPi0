# NinjaRobotPi0 web refinement — 2026-10-13

Status: owner-approved implementation and local validation completed on 2026-10-13. Native phone and physical robot acceptance remain pending. On 2026-10-13 the owner confirmed finish-current-cycle release behavior and disabled unsupported/Tire buttons. The owner explicitly approved this plan before code changes.

## 1. Scope and boundaries

Refine Home/hamburger navigation, Chat, Movement Tool, and System Activity using the six owner references. Add a five-button gamepad that invokes only existing, advertised native movements. Preserve the existing fitted viewport, internal scrolling, fullscreen-on-interface-selection behavior, four UI languages, session ownership, and shutdown confirmation.

Only frontend source, inert tests, generated frontend build outputs, this plan, and new English raw documentation/evidence are in scope. Robot Python functions, drivers, motion sequences, calibration, configuration, API implementations, BLE, agent execution, locks and package dependencies remain unchanged. No live robot, GPIO, motion, shutdown, remote service, deployment or package installation will run during host validation.

Continue the owner's existing instruction to prepare raw wiki documents without ingestion or semantic review. Current wiki pages, catalogs, pointers and fingerprints remain unchanged pending owner processing.

Risk: styling is low risk; browser scheduling of existing physical movement is behaviorally significant even when all robot functions remain unchanged. The UI must not imply an emergency-stop guarantee.

## 2. Evidence and review

Baseline Pi0 commit: `78dde3f`. Initial Pi0 working-tree differences are owner image removals under `docs/validation/ui/03 NinjaRobot Web Interface UI/` and new mockups under `docs/validation/ui/NinjaRobotPi0 web UI update 261013/`. Preserve them. Root platform changes are unrelated and out of scope.

Read-only wiki searches: `web interface` and `movement stop`; source status inspected. `python3 scripts/wiki.py check` passes before this change. Current InstallationGuide, DevelopmentGuide and DevelopmentLog hashes match `project-knowledge.json`. `python3 scripts/verify_core.py` passes before this change.

Relevant current pages:

| Page | Trust/review | Evidence used |
| --- | --- | --- |
| `ninjarobot_pi0_Wiki/wiki/concepts/web-interface-design.md` | Draft, unverified; recorded agent semantic review passed 2026-10-11 | Existing routes, selection, fullscreen, spacing, messages and activity |
| `ninjarobot_pi0_Wiki/wiki/entities/ninja-webapp.md` | Draft, unverified; recorded agent semantic review passed 2026-10-11 | React/i18next app and native API contracts |
| `ninjarobot_pi0_Wiki/wiki/concepts/motion-system-and-easing.md` | Draft, unverified; recorded agent semantic review passed 2026-10-13 | Native preflight, serialization, step-boundary cancellation and current Humanoid defaults |

The UI pages cite `src-20261011-developmentguide-3` and `src-20261011-mobilespacingvalidation`; the latter is registered and ingested. Current complete manual: `raw/articles/ninjarobotpi0/2026-10-13-humanoid-owner-defaults/DevelopmentGuide.md`, source `src-20261013-developmentguide-3`, SHA256 `39169f1ed923edcc159141b97c4b7499c9f3bbf4a241ce8e9dd578c3ac932d3a`. Current log: `raw/notes/ninjarobotpi0/2026-10-13-humanoid-owner-defaults/DevelopmentLog.md`, source `src-20261013-developmentlog-3`. Semantic review is not physical acceptance. Historical statements in full manuals are superseded by current dated sections and executable code.

Code inspected directly and through Serena:

- `ninja_webapp/src/pages/{Home,Movement,Agent}/index.jsx` and corresponding CSS: Home selection state is already implemented; Movement has finite one-shot POST actions, distance card and explanation paragraphs; Chat preserves text payloads and browser speech transcription.
- `components/layout/Layout.jsx`, Header CSS, App routes, session/activity/stream hooks: the session gates route rendering; robot type is already fetched but is not yet passed through Outlet context. Streams and ownership must stay unchanged.
- `components/common/SystemActivity.jsx`/CSS and PowerOffSlider JSX/CSS: drawer open state already exists; color changes need no log or power behavior changes.
- `ninja_core/src/ninja_core/web_server.py:923`: native execution validates the name, reclaims native runtime, executes in a thread and responds after the entire movement. The callback checks session loss and existing safety conditions, not a frontend button-release signal.
- `web_server.py:838` and `dispatcher.py`: `/api/code/stop` targets SafeExecutor/Blockly. It is not a supported cancellation contract for this native gamepad. Aborting fetch is also not proof that the robot stopped.
- `movement_controller.py`: one controller lock serializes native movement; cancellation is checked around blocking driver steps. No new server cancellation or continuous-motion contract will be invented.
- `builtin_movements.py` plus `data/spider_otto.json` and `data/humanoid_defaults.json`: all ten requested names exist. Each directional default contains 37 steps; each Home contains one. Actual robot availability still depends on its active configuration and advertised list.
- `tests/browser_ui.cjs`: existing inert Chromium suite covers eleven viewports/four languages, geometry, session, voice, API contracts and navigation. Its old palette and four-card Movement assertions need deliberate updates, while retaining relevant coverage.

## 3. Visual specification

All six mockups were visually inspected in this session from `docs/validation/ui/NinjaRobotPi0 web UI update 261013/`:

| Reference | Intended change |
| --- | --- |
| `Hamburg Menu.jpg` | Blue-filled default interface buttons, light text/icons; orange selected interface; orange power thumb with white icon and blue track label |
| `Movement tool Interface.jpg` | Unboxed distance at upper left; centered cross-shaped gamepad above three compact selector cards; remove three description paragraphs |
| `Chat Interface.jpg` | Blue idle Voice Input and collapsed activity tab; keep existing send treatment and conversation composition |
| `SystemLog.jpg` | Open activity tab orange with white handle/text; translucent panel boundary |
| `GamePad.png` | Five separate blue gradient buttons, white triangles/center circle, rounded outer ends |
| `GamePad_Plassed.png` | Orange gradient on the currently held button; other buttons retain default blue |

Retain the current font families and responsive type scale. Proposed shared palette: existing near-black `#03070a`, surface `#051017`, cyan `#00a3ff`, orange `#ff8a00`, light text `#f2f6fa`; use reference-matched medium/deep blue for default fills and blue/orange gradients for the pad. Final color values will be recorded after implementation screenshot review.

Interpret **75% transparency as alpha 0.25**, applied to border colors only, never whole-card opacity. Use a cyan translucent border token for Home outer/inner cards, Movement cards, Chat container and colored message borders, and activity panel. Assistant message borders retain their gray hue at alpha 0.25. Interactive control outlines and keyboard focus stay clearly visible; their opacity is not reduced merely because surrounding card borders are reduced.

Home keeps the prior initial-both-blue / single-selected-orange behavior. Update the header hamburger to blue fill and light icon to match the new references. Voice recording remains orange. Keep the existing localized System Activity label/count rather than changing behavior or copying mockup placeholder logs.

## 4. Confirmed gamepad decisions

### A. Release semantics

Owner-approved frontend-only behavior: start one native movement on press, await its successful response, then start the next cycle only if the same press remains active. Release immediately clears the held state and prevents subsequent cycles; **the already submitted cycle may finish**. A 37-step cycle can continue after release; its duration depends on configuration/poses and is not established by this review. This is not immediate stopping or uninterrupted gait across cycles.

If immediate mid-cycle stopping is required, do not implement this proposal as though it met that requirement. Return to a separately authorized backend cancellation design because the present UI-only guardrail cannot provide that guarantee.

### B. Unsupported robots/actions

Owner-approved behavior: display disabled pad buttons when robot type is unknown/Tire or the exact mapped action is absent from the advertised movement list. Provide localized availability information. Do not guess wheel/tire movement names or substitute generic Home without owner agreement.

| Button | Spider | Humanoid | Interaction |
| --- | --- | --- | --- |
| Up | `spider_run_forward` | `humanoid_run_forward` | Repeat complete cycles while held, subject to A |
| Down | `spider_run_backward` | `humanoid_run_backward` | Repeat complete cycles while held, subject to A |
| Left | `spider_turn_left` | `humanoid_turn_left` | Repeat complete cycles while held, subject to A |
| Right | `spider_turn_right` | `humanoid_turn_right` | Repeat complete cycles while held, subject to A |
| Center | `spider_home` | `humanoid_home` | Once per intentional press; never autorepeat |

The explicit run names above take precedence over the introductory walk examples.

### Input and request lifecycle

- Native buttons with localized accessible names, visible focus and at least 44px targets. Pointer capture for touch/mouse/pen; touch gestures disabled only on the pad.
- One held direction and one pending movement at a time. Ignore additional fingers, repeated keyboard keydown events and conflicting presses. Do not queue another direction or Home while a movement is unresolved; require a fresh press after completion.
- Support focused-button Space/Enter hold/release, with Center once. Prevent a synthetic click from duplicating a pointer/keyboard activation. Do not add global arrow shortcuts that interfere with selectors or scrolling.
- Release, pointer cancel/lost capture, focus loss, page hiding, navigation, unmount, session loss and errors invalidate repeat intent. Opening the activity overlay also clears repeat intent. A reconnect never resumes a prior hold.
- Resolve responses against the original press generation; a late response must not revive a released hold or start a newly selected direction.
- Serialize existing Movement selector execution against pad requests to prevent this page from building a motion queue. Do not change endpoints or payloads. Keep unrelated face/sound contracts intact.
- Network error or uncertain completion stops scheduling and shows a localized failure; do not automatically retry a physical command or imply a timeout cancelled it. Retain an unresolved-request lock while a request remains pending.
- Only the physically held button appears orange; pending completion after release is represented separately, with concise localized guidance that the current movement finishes before stopping, if A is approved.

## 5. Phased implementation and validation

### Phase 0 — Confirm this draft

A/B are resolved by the owner's answers above. Obtain explicit approval of this plan. If decisions change scope, revise the plan before code edits. Existing evidence review and plan creation do not execute hardware.

### Phase 1 — Shared palette and borders

Files: `ninja_webapp/src/index.css`; Home, Agent, Header, PowerOffSlider and SystemActivity CSS modules. Add focused shared tokens; apply new fills, foregrounds and border alpha to the named components. Use existing drawer open and recording classes. Preserve slider geometry and confirmation code.

Validate: `npm run lint`; inspect diff; browser computed-style assertions for blue/default and orange/active states, 0.25 border alpha, unchanged full-opacity text, centered readable power label and visible focus. Capture Home, idle/recording Chat, folded/open activity screenshots.

Rollback: revert only this phase's source changes and regenerate the build, preserving all owner changes.

### Phase 2 — Movement composition and pad appearance

Files: `pages/Movement/index.jsx`, `Movement.module.css`; new focused GamePad component/CSS under `components/common/` if that keeps event logic separate; `components/layout/Layout.jsx` passes its existing robotType through Outlet context. No new backend/API.

Place distance at the upper-left of the pad region, retaining `/ws/distance` and accessible unavailable/status content. Center the cross-shaped pad. Keep three selector cards and remove only their explanation text from rendering. Preserve consistent gaps and readable headings. In short landscape, place the pad/distance region beside the selector column; allow bounded internal scrolling on exceptionally short/enlarged layouts. Preserve document scroll lock and activity clearance.

Validate: actual available-height resizing, portrait and landscape, no distance/pad collisions, no covered controls, at least 44px pad targets, keyboard focus and all existing selectors reachable. Inspect representative 390×670/740/844 and 568×320 screenshots against references.

Rollback: remove new composition/component changes and restore previous Movement structure without touching motion sources.

### Phase 3 — Confirmed input scheduling and locales

Files: new `hooks/useGamePad.js` or equivalent isolated scheduler, GamePad component, Movement integration, four locale JSON files (`en`, `ja`, `zh-tw`, `zh-cn`). Implement only the confirmed section 4 contract. Use exact advertised movement names and current robotType; gate unknown/unavailable states. Add localized direction/Home labels, unavailable, pending completion, release guidance and error messages.

Validate using delayed inert POST responses: correct ten mappings; one in-flight request; hold repetition only after success; release/cancel/no-extra-cycle; Center once; rapid direction changes; multi-pointer and keyboard repeat; response-after-unmount; blur/visibility/overlay/session loss; unsupported/Tire/missing names; 404/409/422/423/503 and network failures; no automatic resume or retry. Assert no code-execution/stop/chat/shutdown endpoint is used by the pad. Test selector/pad serialization and no queue buildup.

Rollback: remove scheduler and pad wiring, keeping independently validated cosmetic changes if desired.

### Phase 4 — Regression validation and build

Extend repository-native `tests/browser_ui.cjs` and add a focused inert gamepad test only where it improves delayed-response/input-lifecycle coverage. Reuse installed Node/Playwright; no new dependencies. Test all four languages at 320×568, 360×640, 360×800, 390×670, 390×740, 390×844, 430×932, 568×320, 844×390, 768×1024 and 1280×900. Exercise visualViewport toolbar/keyboard changes, long translated labels, enlarged text, safe areas and internal scrolling. Visually inspect screenshots, not only numeric assertions.

Run frontend lint/build, browser suite(s), `node tests/web_session_hook.cjs`, locale key parity, `python3 scripts/verify_core.py`, and `git diff --check`. The protected-core baseline must stay unchanged. Run against a temporary build, then regenerate tracked `ninja_webapp/dist` with the standard build and verify parity with the tested output. Never hand-edit generated bundles.

Preserve existing session, fullscreen, Home selection/reset, navigation, voice cleanup, native API and shutdown-confirmation assertions. Replace only assertions that encode the intentionally superseded palette or Movement layout. Record actual results; the earlier 813 checks are historical, not a pass for this revision.

No real backend is started: browser tests serve static assets on localhost and intercept APIs/sockets/speech. Chromium emulation cannot prove Safari/iOS/Android device behavior. If an installed WebKit/Firefox runner is unavailable, record that limitation without installing it.

### Phase 5 — Raw documentation and owner handoff

Create complete new English DevelopmentGuide/DevelopmentLog versions under `ninjarobot_pi0_Wiki/raw/{articles,notes}/ninjarobotpi0/2026-10-13-web-gamepad/`, plus an implementation/validation evidence note and inert screenshots under `raw/media/ninjarobotpi0/2026-10-13-web-gamepad/`. Copy from the current mapped complete manuals, update current UI guidance and rebase links; do not overwrite registered originals.

Record approved release semantics, exact code changes, actual checks, remaining native-browser/Pi acceptance, and rollback. Future owner ingestion targets: `wiki/concepts/web-interface-design.md`, `wiki/entities/ninja-webapp.md`, `wiki/references/development-guide.md`, `wiki/concepts/development-workflow.md`, and `wiki/analyses/development-history-and-evolution.md`. Motion-system evidence is referenced, not rewritten, because robot functions stay unchanged.

Run read-only wiki check and report expected implementation-map drift caused by deferred ingestion. Do not register/normalize/ingest/review sources, apply wiki plans, or refresh mapping hashes/pointers in this task.

## 6. Acceptance and manual validation

- UI matches the supplied composition/colors while retaining prior spacing, readable text and full viewport fit.
- 75% transparency applies to specified borders only.
- Gamepad type/availability/mapping and release semantics match the owner's explicit answer; no concurrent or queued pad commands occur.
- All four locales render without untranslated keys, clipped pad labels or unreachable controls.
- Robot source, data, configuration, endpoint implementations and protected baseline have no task changes.
- Host checks and inert screenshots are recorded; native Chrome/Safari and physical movement acceptance remain separately marked pending.

Owner manual checks after reviewing the build: inspect Home/default/selected colors and centered power label without confirming shutdown; inspect Chat/Voice and activity states; inspect portrait/landscape and browser toolbar heights. Physical gamepad validation is a separate deliberate actuator-moving check with the actual calibrated robot, clear movement space and readiness confirmed by the owner. Verify one short press, release tail, sustained hold, each direction and Home on each supported robot; do not infer physical performance from mocked tests. Stop testing if release behavior differs from the approved contract.

No hardware acceptance or production publication is implied by completing this plan.

## 7. Execution record — 2026-10-13

Phases 1–5 completed under owner approval. Frontend lint/build, 1,043 responsive/UI browser assertions, 117 delayed-response gamepad checks, four-locale parity, session-hook checks, protected-core verification and whitespace checks passed. Generated served dist bytes match the tested temporary build. Complete new English raw guide/log/evidence and representative screenshots are saved under raw/{articles,notes,media}/ninjarobotpi0/2026-10-13-web-gamepad/.

Read-only wiki strict lint/link/index checks passed; the knowledge gate reports expected changed/new implementation fingerprints. No ingestion, semantic review, current-pointer or mapping refresh occurred, as directed. Robot functions/data/API implementations/baseline remained unchanged. No physical robot or live service ran. Full results and manual acceptance/rollback are in [WebGamePadValidation.md](../ninjarobot_pi0_Wiki/raw/notes/ninjarobotpi0/2026-10-13-web-gamepad/WebGamePadValidation.md).
