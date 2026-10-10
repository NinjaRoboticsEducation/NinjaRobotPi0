# Lifecycle refinements — 2026-10-10

Owner-authorized scope: movement-tool option 6 reaches Poweroff; closing the web interface restores the reconnect QR and permits one browser controller at a time; default environment prompt/project identity becomes ninjarobotpi0. No real hardware activation or dependency installation is part of implementation. New documentation sources are staged for owner ingestion/review after manual validation.

## Evidence and compatibility

Read the updated wiki README and project-knowledge.json. Current complete manuals are the 2026-10-09-builtins versions: src-20261009-installationguide, src-20261009-developmentguide-2, src-20261009-developmentlog-2. Relevant pages: spider-otto-waypoint-library, web-interface-design, dual-connectivity-and-protocols, installation-guide, motion-system-and-easing, safe-execution-and-blockly-runtime. They remain draft/unverified with recorded source-grounded AI semantic reviews, including the 2026-10-09 automatic movement review; no physical verification is inferred. Baseline knowledge check passed. Search/source-status CLI reports a missing wiki environment; no setup/install is performed.

Code is authoritative: run_cli finally centers then calls HAL.shutdown; /ws/events sleeps and cannot reliably receive browser close events; only Agent creates sockets, so those sockets cannot identify a complete browser visit. ConnectionManager allows multiple clients. QR URL/image is not retained. RuntimePipeline can restart idle faces after actions. The .venv directory remains the supported path, while its actual prompt is ninjarobotv4 because root pyproject/lock metadata still name NinjaRobotV4.

## Phase 1: Movement-tool exit

On deliberate option 6, validate and execute configured Poweroff before releasing hardware, with no subsequent center command. Wheel/Humanoid without Poweroff use their configured home; preserve type preflight and give an explicit fallback message. Error/interrupt cleanup releases resources without unexpected recovery motion. Ensure shutdown and config save still occur if pose playback fails or initialization is incomplete. Driver off releases PWM after the pose; physical holding torque after exit is not claimed.

## Phase 2: Browser ownership and reconnect screen

Add a hardware-free, single-browser session manager. A server-issued HttpOnly same-origin session cookie and persistent /ws/session socket identify a browser; tabs sharing that cookie are one user. Keep the socket in the shared layout, not the Agent route. Existing REST routes/payloads and distance/events messages remain; API calls and auxiliary sockets require the active session. Another browser gets a clear busy state and cannot operate the robot. BLE remains its existing separate protocol, and advertising is never counted as a browser/controller.

Receive disconnect events and use a bounded heartbeat for lost-network clients. Keep ownership until disconnect cleanup finishes; close auxiliary sockets, cancel pending HTTP/greeting work, abort active robot work and suppress later native idle restoration while the reconnect screen owns the display. Old request contexts must not continue their movement/face/sound chains or post-task centering after ownership is lost. Reuse the stored public URL; fall back to local URL when tunneling fails. Offload blocking ngrok/QR/display work from asyncio. Missing/failing displays must not prevent releasing ownership or future connections. Do not redraw QR during server/OS shutdown. Preserve existing power confirmation.

## Phase 3: Environment branding

Rename root distribution and its lock entry to ninjarobotpi0, retain all dependency versions and .venv paths. Installer explicitly creates/reuses .venv with uv venv --allow-existing --prompt ninjarobotpi0 before locked sync, and checks required venv capabilities. Do not clear environments. Update existing local activation prompt strings only, retaining installed packages/calibration. Locked offline checks and inert installer tests verify consistency without installing.

## Phase 4: Validation and documentation

Run targeted inert tests for exit order/failure, simultaneous sessions, extra tabs, API/socket rejection, disconnect/timeout/cancellation, late callbacks, QR failures/shutdown, pipeline display hold and installer prompt/lock consistency. Run one Python test process at a time on the constrained Pi; frontend lint/build separately. Use generator/core checks as relevant and report protected baseline drift rather than refreshing hashes. Existing dirty tracked bytecode belongs to the owner and is preserved; use PYTHONDONTWRITEBYTECODE.

Update public/package documentation and create complete new dated raw InstallationGuide, DevelopmentGuide and DevelopmentLog plus evidence/snapshots. Rebase links; retain registered originals and current mappings/pointers. Prepare a Pi validation report separating inert software tests from owner-ready actuator/display/network acceptance. Do not ingest, register/normalize, apply wiki plans or add semantic/human reviews; owner runs that workflow later.

## Acceptance and limits

Exit plays the permitted final pose exactly once before HAL shutdown, with no following center. Browser route navigation retains ownership, final close restores QR, another browser is blocked while occupied and can connect afterward. Heartbeat timeout releases stale clients. API and delayed action guards reject former owners. .venv prompt is ninjarobotpi0 on fresh/reused installer environments, with locked dependencies unchanged. Physical clearance of extreme Poweroff, PWM release, QR scanability, browser/ngrok heartbeat behavior and interruption timing require owner validation.
