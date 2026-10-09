---
type: Entity
title: ninja_core Package
description: Core application package containing HAL, dispatcher, web server, safe executor, and AI agent.
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
- id: src-20261007-developmentguide-3
  resource: urn:llmwiki:source:src-20261007-developmentguide-3
  title: Pi0 development guide — audit 2026-10-08
  content_hash: sha256:af9d4c121796a7373ef9bb02ca590931d7d88e4a86184f870c780c0e067d77d1
- id: src-20261007-2026-10-07-install-onboard-wiki-ui-2
  resource: urn:llmwiki:source:src-20261007-2026-10-07-install-onboard-wiki-ui-2
  title: Pi0 upgrade implementation and current UI contracts
  content_hash: sha256:1545ea683947c315a9ea0d4c30258c228e975a78e39062b2e045669fcff0cb9c
- id: src-20261007-2026-10-08-upgrade-audit
  resource: urn:llmwiki:source:src-20261008-upgrade-audit
  title: Pi0 upgrade audit findings and boundaries
  content_hash: sha256:7112a6575c6288875e3fdad33679f094b22908e0ee729b29f5dfbfc55f48de64
- id: src-20261009-readme
  resource: urn:llmwiki:source:src-20261009-readme
  title: Readme
  content_hash: sha256:5698950059c4deff1c761e48645e1a01a591d00d7d4371f86884526e74c8149c
- id: src-20261009-2026-10-09-builtin-movements
  resource: urn:llmwiki:source:src-20261009-2026-10-09-builtin-movements
  title: 2026 10 09 Builtin Movements
  content_hash: sha256:6bd14ef705bb60c2c228c95940fd6cb771299532f13e10fdc4faae22db3f216a
semantic_review:
  version: 1
  performed_by: agent:antigravity
  performed_at: '2026-10-09T17:10:48.021602+00:00'
  target_hash: sha256:bff25bbc3a6c6736560bfa4e4bb1fb92ab752700274674c26b2ce898d405ca99
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed ninja_core package architecture against modules, entrypoints, and FastAPI routes. builtin_movements.py module, profile seeding, REST routes (/api/servos/movements), and CLI commands match implementation.
  - Absolute matches ('safe') reflect thread-safe drivers and neutral home positions. Manual server initialization and ngrok boundaries remain as documented.
---

# ninja_core Package

## Existing helpers reused by onboarding

New onboarding orchestration calls existing core settings/import helpers from an isolated foreground worker. Core and driver source files remain unchanged. Status does not call load_config because that function can create defaults. Missing saved servo calibration blocks onboarding import rather than counting factory defaults as calibration.[^src-20261007-developmentguide-3]


`ninja_core` is the central orchestration package of NinjaRobotPi0, binding hardware drivers, communication protocols, AI services, and web APIs into a cohesive runtime.[^src-20260822-readme-3] [^src-20260822-developmentguide]

## Module Inventory

| Module | Purpose |
|--------|---------|
| **`hal.py`** | Hardware Abstraction Layer with dynamic driver loading via `DRIVER_REGISTRY`.[^src-20260822-readme-3] |
| **`config.py`** | `NinjaConfig` manager for master `config.json`, robot naming, robot types, Gemini keys, selected agent model, and built-in movement profile reconciliation.[^src-20260822-readme-3] [^src-20260822-developmentguide] [^src-20261009-2026-10-09-builtin-movements] |
| **`builtin_movements.py`** | Hardware-free movement catalog, installed package resource loader (`data/spider_otto.json`), profile seeding, and preflight step validation.[^src-20261009-readme] [^src-20261009-2026-10-09-builtin-movements] |
| **`dispatcher.py`** | `CommandDispatcher` central message router bridging Web, BLE, and AI inputs.[^src-20260822-readme-3] [^src-20260822-developmentguide] |
| **`safe_executor.py`** | Sandboxed Python code executor with AST import filters and syntax preflight.[^src-20260822-readme-3] [^src-20260822-developmentlog] |
| **`runtime_pipeline.py`** | Coordinator managing native robot idle state vs uploaded Blockly execution ownership.[^src-20260822-developmentlog] |
| **`action_library.py`** | Storage and retrieval engine for saved Blockly actions in `ninja_actions/*.json`.[^src-20260822-developmentlog] |
| **`api_wrappers.py`** | High-level `RobotWrapper`, `ServoArrayWrapper`, `DisplayWrapper`, `BuzzerWrapper`, and `DistanceWrapper`.[^src-20260822-readme-3] [^src-20260822-developmentlog] |
| **`gemini_models.py`** | Paginated API-key-specific Gemini model discovery filtered to `generateContent` models.[^src-20260822-developmentguide] [^src-20260822-developmentlog] |
| **`gemini_runtime.py`** | Bounded Gemini 3 REST generation with low thinking, safe errors, and non-blocking thread offload.[^src-20260822-developmentguide] [^src-20260822-developmentlog] |
| **`ninja_agent.py`** | Gemini AI integration using configured model for natural language chat, multi-modal action planning, and native movement validation.[^src-20260822-readme-3] [^src-20260822-developmentguide] [^src-20261009-2026-10-09-builtin-movements] |
| **`movement_controller.py`** | Motion sequence playback engine with position-aware cubic easing, preflight validation, serialized execution locking, and boundary callback checks.[^src-20260822-readme-3] [^src-20260822-developmentguide] [^src-20261009-2026-10-09-builtin-movements] |
| **`web_server.py`** | FastAPI web server serving REST endpoints (including `/api/servos/movements`), WebSockets (`/ws/events`), and SPA static assets.[^src-20260822-readme-3] [^src-20260822-developmentguide] [^src-20261009-2026-10-09-builtin-movements] |
| **`init_tool.py`** | Interactive setup wizard for validated Gemini key/model selection, tokens, robot naming, robot type, and hardware import.[^src-20260822-developmentguide] [^src-20260822-developmentlog] |

## CLI Entrypoints

* `uv run ninja_core server [--autostart]`: Launches the web server and BLE GATT service.[^src-20260822-readme-3]
* `uv run ninja_core chat`: Starts an interactive terminal chat session with the robot's AI agent.[^src-20260822-readme-3]
* `uv run ninja_core movement-tool`: Launches the interactive servo calibration and motion recording TUI with movement execution option 4.[^src-20260822-readme-3] [^src-20261009-2026-10-09-builtin-movements]
* `uv run ninja_core init-tool`: Launches the guided initial configuration wizard.[^src-20260822-developmentlog]
* `uv run ninja_core config import-all`: Merges individual subsystem configs into `config.json`.[^src-20260822-readme-3]
* `uv run ninja_core config import`: Merges subsystem configs and seeds profile built-in movements.[^src-20261009-2026-10-09-builtin-movements]

[^src-20260822-readme-3]: ninja_core Readme.
[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.
[^src-20260822-developmentlog]: NinjaRobotPi0 Development Log.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.

[^src-20261007-developmentguide-3]: Current versioned Developmentguide.

## Implementation evidence and acceptance limits

Host validation and the exact code/tooling boundary are recorded in the approved implementation evidence. Real Pi hardware, live accounts and published curl acceptance remain pending; passing host checks do not imply physical acceptance.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.

## 2026-10-08 audit follow-up

The audit strengthens only the external onboarding wrapper: conflicting imported pulse aliases are rejected, credentials are private from first write, and worker execution respects platform preflight. Existing core helpers and runtime are unchanged. Manual server start still initializes hardware and attempts ngrok; onboarding does not add Pi5 authentication or offline isolation.[^src-20261007-2026-10-08-upgrade-audit]

[^src-20261007-2026-10-08-upgrade-audit]: Pi0 upgrade audit findings and boundaries.

## Automatic native built-in movement support (2026-10-09)

`ninja_core` adds automatic seeding of native movements for configured robot types during `config import`. Spider receives 19 `spider_*` trajectories and `Poweroff` (20 entries, 566 steps) from installed package data `data/spider_otto.json` when GPIO 20–27 are configured; Wheel and Humanoid receive `home`.[^src-20261009-readme] [^src-20261009-2026-10-09-builtin-movements] `movement_robot_types` and `builtin_movement_hashes` track managed versus customized movements, preflight checks prevent partial actuation on invalid data, and REST endpoints `/api/servos/movements` and `/api/servos/movements/{name}/execute` expose the catalog.[^src-20261009-readme] [^src-20261009-2026-10-09-builtin-movements]

[^src-20261009-readme]: ninja_core package README with built-in movements metadata.
[^src-20261009-2026-10-09-builtin-movements]: Automatic native built-in movement evidence and architecture boundaries.
