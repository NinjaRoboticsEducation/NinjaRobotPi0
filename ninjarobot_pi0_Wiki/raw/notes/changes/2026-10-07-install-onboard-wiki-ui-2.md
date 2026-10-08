# Approved Pi0 installation, onboarding, wiki and interface evidence

Owner approved the phased plan on 2026-10-07. This records implementation evidence, not
human or physical-device verification. Base Pi0 commit is 3dbc41a4ee3cf9fb1019e3be5e633f5a6b47d862.
Pi5 d620fa4e790fd79c1b5d65bc2b95eb71625076cd was a read-only design/workflow reference.

## Implementation and boundaries

- `install.sh`: complete-stream bootstrap, real remote HEAD resolution, explicit branch/tag/full
  commit selection, ambiguity rejection, private staging and no-clobber publication. Target is
  Zero 2 W / Linux aarch64 / Raspberry Pi OS Bookworm. Quoted/unquoted codename checking is tested.
- `scripts/install-rpi.sh`, `install_system.py`, `install_check.py`, `install_record.py`:
  pinned tooling with artifact checksums, locked production Python and npm build; narrow apt
  prerequisites with temporary service-start inhibition. Existing admin policy is never overwritten;
  policy cleanup removes only the owned inode. Existing custom pigpiod units are retained.
  No daemon, calibration, server, boot enable or reboot starts automatically. Rerun and failure
  checksum paths use inert fixtures. Tool pins are in install-versions.env; uv's versioned script
  hash is verified, but its transitive binary download relies on the upstream installer/HTTPS.
- `onboard.sh`, `scripts/onboard.py`: existing display/buzzer/servo/sensor interactive tools
  in foreground, explicit READY before activation, valid saved config required for reuse/import,
  separate software and operator-observation status, private resumable progress. Sensor config
  remains package-local. Servo tool can center saved servos before its menu; no default fallback
  is accepted as calibration. Existing identity/Gemini/ngrok helpers run only on selected steps.
  Hidden credentials do not enter arguments/progress. Exceptions and cancellation restore prior
  robot settings and the actual pyngrok-selected config. Simulated failures use dummy inputs.
- `ninja_webapp/src`: Pi5 navy/cyan tokens, rounded bordered panels, Home/Agent/Help presentation,
  menu sheet with focus restoration and Escape, dark activity drawer, four locales, labelled
  selectors/microphone/actions. BLE badge means advertising, not controller connection. React
  metadata is 19.2.0; old React 18 documentation is historical. Existing chat/action endpoints,
  request bodies, distance_mm WebSocket telemetry and units remain compatible. Power-off requires
  deliberate staged input and the original confirmation; arrow keys stage it, Enter confirms.
  No camera, Game Pad, USB voice service or Pi5 ownership protocol is introduced.
- `scripts/wiki.py`: independent explicit locked setup, direct existing-environment retrieval,
  stdlib read-only knowledge check, locked staged text prepare without catalog hash refresh.
  Wiki moved to ninjarobot_pi0_Wiki with all old raw originals and unchanged page reviews retained.
  New complete manuals are immutable registered dated versions; root manual URLs are short pointers.
  AGENTS/shared skills/adapters and project-knowledge.json govern the workflow. Drift requires
  investigation and review, not automatic fingerprint acceptance. Independent wiki source code
  is unchanged. New CI exercises host-only validation with read-only permissions.

## Executed evidence

On this macOS host: Python 3.11.15 full root tests 148 passed; earlier Python 3.13.14 root
136 passed before final added rollback/map cases (8 existing DBus deprecation warnings).
Standalone driver suites: servo 82, display 57, buzzer 65 and distance 61 passed. Independent
wiki suite 61 passed. Focused new installer/onboarding/knowledge tests 44 passed. Ruff and
ShellCheck passed; frontend lint had no warnings/errors and Vite build passed with existing
lockfile. Inert Chromium checks passed 64 assertions at 360/390/844/1280-pixel viewports,
covering contracts, locales, menu focus, navigation and canceled power confirmation.
120 protected robot source/test/metadata/lock inputs match the captured baseline.

No real Pi, GPIO, actuator, sensor, speech input, live Gemini/ngrok account, tunnel, startup
service, actual shutdown, commit, push or deployment was used. Browser fixtures are inert;
installation fixtures emulate platform/system commands and are not ARM/apt hardware acceptance.
Public curl acceptance remains pending publication. Physical/resource usage and slow Pi build
acceptance remain owner-manual. Draft/unverified lifecycle must not be promoted by AI review.

## Current UI contract corrections found during source review

The current server and frontend use POST `/api/agent/chat` with `message` and `language`,
GET `/api/ble/status` for advertising status, `/ws/distance` for `distance_mm`, and
`/ws/events` for activity/log events. Historical tables omitting `/api` or using `/api/chat`
are documentation drift, not compatibility aliases. Code source: ninja_core web_server.py
route definitions and ninja_webapp Agent/Header components; inert browser fixtures assert these.
Uncalibrated motion must not be described as impossible: core can synthesize fallback calibration,
and the standalone servo tool can initialize/center configured servos before its menu. The new
onboarding import/reuse gate requires ordered saved pulses; it does not alter existing core
or standalone-tool behavior and cannot certify physical calibration.
