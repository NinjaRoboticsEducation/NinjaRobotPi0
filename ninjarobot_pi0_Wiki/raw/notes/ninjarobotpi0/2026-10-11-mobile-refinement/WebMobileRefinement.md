# Mobile web interface refinement — 2026-10-11

Status: implemented software candidate; owner manual validation pending. These new English raw sources are unregistered, unnormalized and semantically unreviewed. Ingestion, review, current-manual pointers, curated pages and implementation-map updates are intentionally deferred to the owner.

## Review evidence and approved plan

The owner approved viewport adaptation and responsive spacing/type, internally scrollable messages/logs with short-screen fallback, mutually exclusive Home button selection remembered until reload, fullscreen requested during interface selection where available, localized configured robot type, local lint/browser validation and new complete raw guide/log versions.

Read-only retrieval used `python3 scripts/wiki.py search "web interface"`, `source status` and `check`. The original knowledge check passed. Relevant pages: [web interface design](../../../../wiki/concepts/web-interface-design.md), [webapp entity](../../../../wiki/entities/ninja-webapp.md), [development guide](../../../../wiki/references/development-guide.md). The first two are draft/unverified, with existing passed AI semantic reviews dated 2026-10-11; those reviews are not human/mobile acceptance and do not review this new implementation. Current sources used: `src-20261011-developmentguide`, `src-20261011-webrefinementevidence`, `src-20261011-developmentlog-2`, and their immutable raw versions. Existing current manual hashes were checked after implementation and remain unchanged.

All four requested images were directly viewed in this session: Home and Hamburg Menu.jpg, Movement tool Interface.jpg, Chat Interface.jpg and SystemLogPannel.jpg under `docs/validation/ui/WebInterfaceUI_Update/`. They establish visual intent only. Spider/125 mm/action examples are mock data, never inferred robot configuration or hardware acceptance.

The code review traced App routes, persistent Layout ownership, Home links/power confirmation, Header badge, Movement capabilities/POST actions, Agent text/recognition lifecycle, stream/event hooks, SystemActivity scrolling, locale/document language, server configuration and session middleware. Findings and resolutions:

- Document/body and the min-height shell allowed vertical page overflow: fixed visible-viewport shell, document scroll lock and bounded internal fallbacks.
- Chat's independent `100dvh - 440px` calculation/minimum message height did not account for its other controls, header or keyboard: remaining-height grid/flex allocation and VisualViewport resize/pan observation.
- Generous fixed spacing and single-column landscape layout consumed short screens: compact height breakpoints, landscape columns, wrapping and minimum 44 px controls, without whole-content scaling.
- Chat entry was always orange: shared dark-blue base style, one persistent selected link, reload reset and accessible selection state.
- Header had no verified type: only the canonical validated type from a new read-only metadata endpoint; localized suffix and no guessed type on failure.
- Existing browser assertion checked Chat before navigation committed: explicit route-heading waits. Fullscreen fixtures must disable both standard and WebKit capability flags when simulating absence.

Implementation phases: viewport/layout, selection/fullscreen/type presentation, deterministic frontend/backend checks, screenshot refinement, then raw documentation handoff. No dependency installation, lockfile change, deployment, live account/service request, driver change or hardware operation was approved or performed.

## 1. Scope of validation

Frontend: `ninja_webapp/index.html`; index.css; Layout/Header; useAppViewport; fullscreen utility; Home/Movement/Agent styles; SystemActivity/LanguageSelector/power-slider styles; all four locale bundles. Backend: additive `GET /api/robot/status` in `ninja_core/src/ninja_core/web_server.py`. Validation: `tests/browser_ui.cjs`, `tests/test_web_robot_status.py`, and the single reviewed server fingerprint in `docs/validation/core_baseline.json`.

The metadata response contains only `robot_type`. It reads validated in-memory HAL configuration without configuration writes or hardware I/O. Existing `/api/` session middleware returns 423 to inactive/non-owner browsers and 503 during shutdown. A missing HAL returns 503. Existing control routes, request payloads, controller sockets, native operations and staged/confirmed power-off remain compatible.

## 2. Environment and prerequisites

Local macOS host, existing frontend npm lockfile/dependencies, existing bundled Playwright JavaScript and installed Chromium. Builds were produced through Vite in `/private/tmp/pi0-ui-refinement`, then the normal `npm run build` refreshed the ignored local `ninja_webapp/dist` used by the server. Generated assets are not committed. The existing JavaScript browser suite is reused because the available Python runtimes lack Python Playwright. Existing cached FastAPI/Starlette/httpx packages are reused for an isolated endpoint app; no packages are installed. Full robot environment dependencies are not available, so the full hardware/runtime Python suite was not run.

The browser suite serves only local built static assets, intercepts every robot API with fixtures, replaces WebSockets and recognition, cancels shutdown confirmation, and mocks fullscreen. It never imports or starts the production server lifespan.

## 3. Safety notes

All executed checks are inert. Real Movement execution, speech/chat-controlled actions and confirmed power-off can affect hardware. Owner manual tests involving motion require clearance, stable power and physical readiness. Do not start a robot/server/device tool solely for visual acceptance. Browser layout and screenshot acceptance can use these inert fixtures.

## 4. Safe smoke tests

From `ninja_webapp/`: `npm run lint`; `npm run build -- --outDir /private/tmp/pi0-ui-refinement`. From robot root: `node --check tests/browser_ui.cjs`; `node tests/web_session_hook.cjs`; `python3 scripts/verify_core.py`; `git diff --check`.

Browser reproduction with an already installed Playwright package/browser:

```bash
PLAYWRIGHT_MODULE=/absolute/path/to/existing/playwright \
UI_SCREENSHOTS=/private/tmp/pi0-ui-refinement-shots \
node tests/browser_ui.cjs /private/tmp/pi0-ui-refinement
```

Run `python tests/test_web_robot_status.py` using an existing development Python containing FastAPI, Starlette and httpx. The test compiles only the reviewed local route AST into an inert app and uses the real session middleware. It checks all types, exact minimal response, owner/non-owner gating, missing HAL and shutdown. This does not claim a production lifespan or robot acceptance test.

## 5. Communication/interface tests

Browser fixtures preserve exact direct action endpoints, text `{message, language}` payload, recognition locales, cleanup on navigation and persistent session ownership. Tests verify initial styles, each selected style, return Home, reload reset, standard fullscreen rejection/success, unsupported fullscreen and prefixed fallback. Fullscreen is only requested during interface activation; actual browser permissions can deny it.

Phone/tablet contexts enable Chromium mobile emulation and touch; initial interface selection is activated with a tap. The desktop context remains desktop. Nine CSS-pixel screen sizes: 320×568, 360×640, 360×800, 390×844, 430×932, 568×320, 844×390, 768×1024, 1280×900. English, Japanese, Traditional Chinese and Simplified Chinese are exercised across Home/Movement/Chat. Checks cover no document overflow/scroll, control reachability, localized type, separate log scrolling and the 50-entry limit. Keyboard tests emulate VisualViewport height 300 px and offset 20 px, then restore it; these are geometry checks, not real OS keyboard tests.

## 6. Sensor/display checks

Inert distance fixture accepts 125 mm and renders unavailable for negative readings. No physical distance sensor, robot display, safe-area/notch device or telemetry connection was tested. Header type is configuration metadata, separate from the controller-ownership badge. No type-specific actions are invented by the UI.

## 7. Actuator-moving or power-risk tests

No actuator-moving, servo, GPIO, buzzer, robot display, remote execution or real power-off test was performed. Cancelled keyboard slider confirmation is verified to send no shutdown request. Owner-controlled direct action/power tests remain pending and must follow the project's existing safety and shutdown procedure.

## 8. Expected outcomes and owner acceptance

- Fresh Home fits the viewport; both links are dark blue/cyan. Select one, return Home, see only it orange; switch and verify exclusivity; reload and see both default.
- Movement/Chat title reflects configured Tire/Humanoid/Spider in the selected UI language. A metadata error does not display a fabricated type.
- Supported browsers request fullscreen when an interface is selected. Unsupported/denied cases remain usable. Exiting fullscreen remains a browser-controlled action.
- Portrait spacing responds to width/height; short landscape screens use columns. Very short/enlarged-content cases scroll internally. No whole-document drag/scroll occurs.
- Long chat/log entries wrap and scroll inside their panels. Activity stays below the header, folds/clears locally and remains capped at 50.
- Soft keyboard, browser toolbar changes, orientation and safe areas leave input, Send, Voice and navigation reachable; actual iOS/Android verification is pending.
- Browser zoom restrictions apply where honored. Browser/OS accessibility overrides and fullscreen support cannot be guaranteed across every browser.

## 9. Execution status and evidence

Frontend lint/build, isolated route/session tests, Python fatal-error lint, new-test Ruff lint, session hook harness, reviewed core fingerprint and diff whitespace checks pass. Server AST comparison against HEAD confirms that removing the new robot_status definition restores the prior AST exactly; only that protected file's hash was refreshed after inspection/testing. No wiki implementation hashes were refreshed.

The final mobile/touch-enabled browser matrix passed 612 assertions, including control occlusion, viewport meta/touch-action, standard/prefixed fullscreen and fallback behavior. The isolated route/session suite passed 3 tests; all four locale bundles have matching nonempty keys. Default and temporary-output builds passed. The reused Starlette/httpx test runtime emitted a deprecation warning; no dependency change was made. Screenshot inspection is AI visual QA, not owner physical acceptance. Chromium emulation is not native Safari/WebKit or Firefox verification; their Playwright browser binaries are absent and were not installed. Actual iOS Safari/Chrome, Android Chrome/Firefox, keyboard/fullscreen/microphone, safe-area devices, Pi and live runtime/provider checks remain pending.

Read-only `python3 scripts/wiki.py check` now reports expected implementation-review/classification drift against the previous map. No ingestion, normalization, source registration, semantic review, curated-page change, pointer update, map refresh or wiki lint repair was run. This is a raw-document handoff and does not claim the curated wiki is current.

## 10. Pass/fail checklist

Software checks pass subject to the final browser result below. All four locales and nine screen sizes are covered by inert Chromium assertions. Native browser/device, microphone, telemetry and hardware acceptance are pending. New complete [guide](../../../../raw/articles/ninjarobotpi0/2026-10-11-mobile-refinement/DevelopmentGuide.md) and [log](DevelopmentLog.md) preserve registered originals and await owner ingestion/review.

## 11. Rollback

Use the reviewed diff to revert only these frontend files, the metadata endpoint, its protected fingerprint and associated tests together. Rebuild through Vite before serving the reverted UI. Preserve later user changes, configuration/calibration, existing registered raw originals and historical evidence. No migration, production data change or dependency/lock change requires rollback. The earlier Home/Movement/Chat behavior remains the pre-change reference at Git commit a10a3c1.


## Retained visual evidence

Screenshots below were produced by inert Chromium fixtures and visually inspected. Displayed Spider, distance and log data are fixtures.

- [home-320.png](../../../../raw/media/ninjarobotpi0/2026-10-11-mobile-refinement/home-320.png)
- [home-390.png](../../../../raw/media/ninjarobotpi0/2026-10-11-mobile-refinement/home-390.png)
- [home-selected-390.png](../../../../raw/media/ninjarobotpi0/2026-10-11-mobile-refinement/home-selected-390.png)
- [movement-390.png](../../../../raw/media/ninjarobotpi0/2026-10-11-mobile-refinement/movement-390.png)
- [chat-390.png](../../../../raw/media/ninjarobotpi0/2026-10-11-mobile-refinement/chat-390.png)
- [long-log-390.png](../../../../raw/media/ninjarobotpi0/2026-10-11-mobile-refinement/long-log-390.png)
- [home-568.png](../../../../raw/media/ninjarobotpi0/2026-10-11-mobile-refinement/home-568.png)
- [movement-568.png](../../../../raw/media/ninjarobotpi0/2026-10-11-mobile-refinement/movement-568.png)
- [chat-568.png](../../../../raw/media/ninjarobotpi0/2026-10-11-mobile-refinement/chat-568.png)

Reviewed server hashes: pre-change `52097d5cac03b3286e7ca8f6cdc36984c880afa2cca34750318f1c2f66688d28`; metadata-route candidate `e30a038147586f531f1880383bbbc96a2a1e2566caa35c628351c31d2fefbf95`. The additive endpoint is the only server AST difference.
