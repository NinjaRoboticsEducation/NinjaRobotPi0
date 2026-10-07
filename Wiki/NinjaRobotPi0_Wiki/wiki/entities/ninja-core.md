---
type: Entity
title: ninja_core Package
description: Core application package containing HAL, dispatcher, web server, safe
  executor, and AI agent.
status: draft
generated:
  by: codex/migration-audit
  at: '2026-10-07T07:13:37.354382+00:00'
sources:
- id: src-20260822-readme-3
  resource: urn:llmwiki:source:src-20260822-readme-3
  title: ninja_core Readme
  content_hash: sha256:502427fd1c9031fea178cc56a037d30e880c5b5c78875618d2ab173a8543d2df
- id: src-20260822-developmentguide
  resource: urn:llmwiki:source:src-20260822-developmentguide
  title: NinjaRobotPi0 Development Guide
  content_hash: sha256:d1f8e19627223cb320b2e05df9a141c768ca0f418a7f77d160b6127d08c439e9
- id: src-20260822-developmentlog
  resource: urn:llmwiki:source:src-20260822-developmentlog
  title: NinjaRobotPi0 Development Log
  content_hash: sha256:54cdbd7e50fd0cbfbfaba5073d6ed89379181b78bc3d7267d64518f15e9bfe02
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
---

# ninja_core Package

`ninja_core` is the central orchestration package of NinjaRobotPi0, binding hardware drivers, communication protocols, AI services, and web APIs into a cohesive runtime.[^src-20260822-readme-3] [^src-20260822-developmentguide]

## Module Inventory

| Module | Purpose |
|--------|---------|
| **`hal.py`** | Hardware Abstraction Layer with dynamic driver loading via `DRIVER_REGISTRY`.[^src-20260822-readme-3] |
| **`config.py`** | `NinjaConfig` manager for master `config.json`, robot naming, robot types, Gemini keys, and the selected agent model.[^src-20260822-readme-3] [^src-20260822-developmentguide] [^src-20260822-developmentlog] |
| **`dispatcher.py`** | `CommandDispatcher` central message router bridging Web, BLE, and AI inputs.[^src-20260822-readme-3] [^src-20260822-developmentguide] |
| **`safe_executor.py`** | Sandboxed Python code executor with AST import filters and syntax preflight.[^src-20260822-readme-3] [^src-20260822-developmentlog] |
| **`runtime_pipeline.py`** | Coordinator managing native robot idle state vs uploaded Blockly execution ownership.[^src-20260822-developmentlog] |
| **`action_library.py`** | Storage and retrieval engine for saved Blockly actions in `ninja_actions/*.json`.[^src-20260822-developmentlog] |
| **`api_wrappers.py`** | High-level `RobotWrapper`, `ServoArrayWrapper`, `DisplayWrapper`, `BuzzerWrapper`, and `DistanceWrapper`.[^src-20260822-readme-3] [^src-20260822-developmentlog] |
| **`gemini_models.py`** | Paginated API-key-specific Gemini model discovery filtered to `generateContent` models.[^src-20260822-developmentguide] [^src-20260822-developmentlog] |
| **`gemini_runtime.py`** | Bounded Gemini 3 REST generation with low thinking, safe errors, and non-blocking thread offload.[^src-20260822-developmentguide] [^src-20260822-developmentlog] |
| **`ninja_agent.py`** | Gemini AI integration using the configured model for natural language understanding and multi-modal action planning.[^src-20260822-readme-3] [^src-20260822-developmentguide] |
| **`movement_controller.py`** | Motion sequence playback engine with position-aware cubic easing.[^src-20260822-readme-3] [^src-20260822-developmentguide] |
| **`web_server.py`** | FastAPI web server serving REST endpoints, WebSockets (`/ws/events`), and SPA static assets.[^src-20260822-readme-3] [^src-20260822-developmentguide] |
| **`init_tool.py`** | Interactive setup wizard for validated Gemini key/model selection, tokens, robot naming, robot type, and hardware import.[^src-20260822-developmentguide] [^src-20260822-developmentlog] |

## CLI Entrypoints

* `uv run ninja_core server [--autostart]`: Launches the web server and BLE GATT service.[^src-20260822-readme-3]
* `uv run ninja_core chat`: Starts an interactive terminal chat session with the robot's AI agent.[^src-20260822-readme-3]
* `uv run ninja_core movement-tool`: Launches the interactive servo calibration and motion recording TUI.[^src-20260822-readme-3]
* `uv run ninja_core init-tool`: Launches the guided initial configuration wizard.[^src-20260822-developmentlog]
* `uv run ninja_core config import-all`: Merges individual subsystem configs into `config.json`.[^src-20260822-readme-3]

[^src-20260822-readme-3]: ninja_core Readme.
[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.
[^src-20260822-developmentlog]: NinjaRobotPi0 Development Log.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.
