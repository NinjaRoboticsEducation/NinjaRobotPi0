---
type: Reference
title: API and CLI Reference
description: Unified reference of all Python driver classes, wrapper APIs, REST/WebSocket
  endpoints, and CLI tools.
status: draft
generated:
  by: codex/migration-audit
  at: '2026-10-07T07:13:37.354382+00:00'
sources:
- id: src-20260822-developmentguide
  resource: urn:llmwiki:source:src-20260822-developmentguide
  title: NinjaRobotPi0 Development Guide
  content_hash: sha256:d1f8e19627223cb320b2e05df9a141c768ca0f418a7f77d160b6127d08c439e9
- id: src-20260822-readme-3
  resource: urn:llmwiki:source:src-20260822-readme-3
  title: ninja_core Readme
  content_hash: sha256:502427fd1c9031fea178cc56a037d30e880c5b5c78875618d2ab173a8543d2df
- id: src-20260822-readme-5
  resource: urn:llmwiki:source:src-20260822-readme-5
  title: pi0buzzer Readme
  content_hash: sha256:2d45a1426b50788922f073ae4e8236e7e16e63c22c329fce016c782ce7b127fa
- id: src-20260822-readme-6
  resource: urn:llmwiki:source:src-20260822-readme-6
  title: pi0disp Readme
  content_hash: sha256:ccc2a3f07c0591dfe2c1828c8e01365b1820b386a68ad30a751959a9f5bb3ba2
- id: src-20260822-readme-7
  resource: urn:llmwiki:source:src-20260822-readme-7
  title: pi0servo Readme
  content_hash: sha256:23793729576aa0b8f5b460d7fe4e47ab1d7ad4f9a6af4348bf4c8208a6610a76
- id: src-20260822-readme-8
  resource: urn:llmwiki:source:src-20260822-readme-8
  title: pi0vl53l0x Readme
  content_hash: sha256:ddf100f609e7335b81dc3803c453c3d0dc66fbe0c20a52917d90407bc1d2f35e
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
- id: src-20261009-2026-10-09-builtin-movements
  resource: urn:llmwiki:source:src-20261009-2026-10-09-builtin-movements
  title: 2026 10 09 Builtin Movements
  content_hash: sha256:6bd14ef705bb60c2c228c95940fd6cb771299532f13e10fdc4faae22db3f216a
- id: src-20261009-developmentguide-2
  resource: urn:llmwiki:source:src-20261009-developmentguide-2
  title: Developmentguide
  content_hash: sha256:80ef9c89176a6b0a3749f9127697464f197c2972bf2a41ae533fa2cb7afdc0ab
- id: src-20261010-developmentguide-2
  resource: urn:llmwiki:source:src-20261010-developmentguide-2
  title: Developmentguide
  content_hash: sha256:a79a71113f70fb1e6b443cd73b9cd688c8f7889ebf4a9df97b521cb3b76e3127
- id: src-20261010-clientrypointrepairplan
  resource: urn:llmwiki:source:src-20261010-clientrypointrepairplan
  title: Clientrypointrepairplan
  content_hash: sha256:05eb8fe221519b45022eb360c7441b1ff7a1b41e542502ab9759ca93ca2701fc
- id: src-20261010-lifecyclerefinementsevidence
  resource: urn:llmwiki:source:src-20261010-lifecyclerefinementsevidence
  title: Lifecyclerefinementsevidence
  content_hash: sha256:c34468e740adccacc6546a2afe39fd41562eed229ae5795255577b044d4fd09e
semantic_review:
  version: 1
  performed_by: agent:antigravity
  performed_at: '2026-10-10T12:07:31.827347+00:00'
  target_hash: sha256:4e0602b2d11d5c4728b1dd731f8185ba0add79a6d67094953f5694876f9064f5
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed REST endpoints, CLI commands, and WebSocket contracts against web_server.py,
    web_sessions.py, and movement_cli.py. /ws/session endpoint, 423/503/4409 codes,
    option 6 Poweroff, and single-ownership launchers match code.
  - Host CLI help checks do not imply remote network acceptance or physical robot
    readiness.
---

# API and CLI Reference

## Additive workflow commands

`./install.sh --dry-run` previews software setup; `--check` is read-only. `./onboard.sh` adds interactive setup while the existing robot CLI remains unchanged. `python3 scripts/wiki.py` offers explicit setup/prepare, then read-only query/check. These commands do not replace the existing robot API or transport contracts.[^src-20261007-developmentguide-2]


This document provides a consolidated reference for all Python APIs, scriptable CLI commands, REST endpoints, and WebSocket channels.[^src-20260822-developmentguide]

## Python User API (`robot.*` Wrapper in SafeExecutor)

| Object / Method | Parameters | Description |
|-----------------|------------|-------------|
| `robot.servos.move_pin(pin, angle, speed_mode)` | `pin: int`, `angle: int`, `speed_mode: str="M"` | Move single GPIO pin (`20..27`) with speed `F`/`M`/`S`.[^src-20260822-developmentguide] [^src-20260822-readme-7] |
| `robot.servos.move_pins(targets, per_servo_speeds)` | `targets: dict[int, int]`, `per_servo_speeds: dict` | Simultaneous multi-pin move.[^src-20260822-developmentguide] [^src-20260822-readme-7] |
| `robot.expression(name)` | `name: str` | Display animated facial expression.[^src-20260822-developmentguide] [^src-20260822-readme-6] |
| `robot.display.text(text, scroll, lang)` | `text: str`, `scroll: bool`, `lang: str="auto"` | Render static or marquee text.[^src-20260822-developmentguide] [^src-20260822-readme-6] |
| `robot.display.clear()` | None | Clears display and maintains blank hold.[^src-20260822-developmentguide] [^src-20260822-readme-6] |
| `robot.buzzer.play_sound(freq, dur)` | `freq: int`, `dur: float` | Play tone in background thread.[^src-20260822-developmentguide] [^src-20260822-readme-5] |
| `robot.buzzer.play_emotion(name)` | `name: str` | Play predefined emotion sound effect.[^src-20260822-developmentguide] [^src-20260822-readme-5] |
| `robot.buzzer.play_song(name)` | `name: str` | Play named song melody.[^src-20260822-developmentguide] [^src-20260822-readme-5] |
| `robot.distance.read()` | None | Returns distance in mm (or `9999` fallback).[^src-20260822-developmentguide] [^src-20260822-readme-8] |
| `robot.check_stop()` | None | Cooperative cancellation check.[^src-20260822-developmentguide] |

## Web Server REST & WebSocket Endpoints

| Endpoint | Method | Payload / Params | Description |
|----------|--------|------------------|-------------|
| `/api/agent/chat` | `POST` | `{"message": "...", "language": "en"}` | AI conversational agent endpoint.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2] |
| `/api/code/execute` | `POST` | `{"code": "..."}` | Submit Python script for sandboxed execution.[^src-20260822-developmentguide] [^src-20260822-readme-3] |
| `/api/code/stop` | `POST` | None | Requests cooperative cancellation of the active script; non-cooperative loops may require the Stop Robot path or server restart.[^src-20260822-developmentguide] |
| `/api/system/shutdown` | `POST` | None | Triggers graceful shutdown animation and OS poweroff.[^src-20260822-developmentguide] [^src-20260822-readme-3] |
| `/api/ble/status` | `GET` | None | Returns BLE advertising status and service name.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2] |
| `/api/servos/movements` | `GET` | None | Lists available compatible movement names for the configured robot type.[^src-20261009-2026-10-09-builtin-movements] |
| `/api/servos/movements/{name}/execute` | `POST` | None | Executes named movement; returns 404 for unknown, 422 for invalid/incompatible before runtime reclamation, 409 on abort.[^src-20261009-2026-10-09-builtin-movements] |
| `/ws/distance` | `WebSocket` | None | Distance telemetry with `distance_mm`.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2] |
| `/ws/events` | `WebSocket` | None | Real-time activity/log event stream.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2] |

## Scriptable CLI Command Reference

```bash
# ninja_core
uv run ninja_core server [--autostart]    # Launch server and BLE
uv run ninja_core chat                    # Terminal AI chat
uv run ninja_core movement-tool           # Servo tool (option 4 runs configured movements)
uv run ninja_core init-tool               # Guided setup wizard
uv run ninja_core config set-name "<n>"   # Set Bluetooth name
uv run ninja_core config set-key gemini <key>  # Discover, validate, and save model
uv run ninja_core config set-key <k> <v>       # Generic non-Gemini key save
uv run ninja_core config import           # Merge configs and seed profile built-in movements[^src-20261009-developmentguide-2]
uv run ninja_core config set-type <type>  # Set robot type (spider, wheel/tire, humanoid)

# pi0servo
uv run pi0servo calib <pin>               # Calibrate servo pin
uv run pi0servo cmd "<command>"           # Execute move command

# pi0disp
uv run pi0disp init [--defaults]          # Setup wizard
uv run pi0disp image <path>               # Display image
uv run pi0disp text "<text>" [--scroll]   # Display text
uv run pi0disp brightness <0-100>         # Adjust backlight

# pi0buzzer
uv run pi0buzzer init <pin>               # Initialize pin
uv run pi0buzzer beep [freq] [dur]        # Play tone
uv run pi0buzzer play <emotion>           # Play emotion

# pi0vl53l0x
uv run pi0vl53l0x get [--count N]         # Read distance
uv run pi0vl53l0x calibrate --distance D  # Calibrate offset
uv run pi0vl53l0x status                  # Health check
```

[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.
[^src-20260822-readme-3]: ninja_core Readme.
[^src-20260822-readme-5]: pi0buzzer Readme.
[^src-20260822-readme-6]: pi0disp Readme.
[^src-20260822-readme-7]: pi0servo Readme.
[^src-20260822-readme-8]: pi0vl53l0x Readme.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.

[^src-20261007-developmentguide-2]: Current versioned Developmentguide.

## Implementation evidence and acceptance limits

Host validation and the exact code/tooling boundary are recorded in the approved implementation evidence. Real Pi hardware, live accounts and published curl acceptance remain pending; passing host checks do not imply physical acceptance.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.

## AI Agent Native Movement Plan Execution

Agent action plans validate complete native movement chains against permitted type-scoped names, with limits of 32 chain entries and 1–20 positive integer repetitions per entry. Invalid chains are rejected in full while retaining conversational output and logging the reason.[^src-20261009-2026-10-09-builtin-movements]

[^src-20261009-2026-10-09-builtin-movements]: Automatic native built-in movement evidence and architecture boundaries.

[^src-20261009-developmentguide-2]: NinjaRobotPi0 Development Guide, 2026-10-09.
## Single-ownership CLI launchers and session endpoint contracts (2026-10-10)

The five robot CLI commands (`ninja_core`, `pi0servo`, `pi0disp`, `pi0buzzer`, `pi0vl53l0x`) are declared and owned exclusively by their provider packages, preventing root packaging collision and missing launchers in `.venv/bin`.[^src-20261010-clientrypointrepairplan]
Targeted environment repair synchronizes locked providers without altering other packages:
```bash
env -u UV_PROJECT_ENVIRONMENT -u UV_PROJECT uv sync --locked --inexact --no-dev \
  --reinstall-package ninja-core --reinstall-package pi0servo \
  --reinstall-package pi0disp --reinstall-package pi0buzzer \
  --reinstall-package pi0vl53l0x
```
Web API access requires an active primary session identified by the HttpOnly `ninja_web_session` cookie; requests from inactive sessions return HTTP 423, and requests during server shutdown return HTTP 503.[^src-20261010-developmentguide-2] [^src-20261010-lifecyclerefinementsevidence]

[^src-20261010-developmentguide-2]: Current versioned Developmentguide (2026-10-10 CLI recovery).
[^src-20261010-clientrypointrepairplan]: CLI launcher repair plan and root packaging reconciliation.
[^src-20261010-lifecyclerefinementsevidence]: Lifecycle refinements implementation evidence.
