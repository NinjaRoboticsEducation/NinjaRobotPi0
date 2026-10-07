---
type: Concept
title: Action Library and AI Agent
description: Google Gemini-powered agentic AI, saved Blockly action library, action
  chaining, and cooperative interruption.
status: draft
generated:
  by: codex/repository-migration
  at: '2026-10-07T07:00:29.384460+00:00'
sources:
- id: src-20260822-developmentguide
  resource: urn:llmwiki:source:src-20260822-developmentguide
  title: NinjaRobotPi0 Development Guide
  content_hash: sha256:43e40f7c8db5734b4e8fe2ffd7d1e9c365cf9ceaad16fb4dbbbbe8eb1be71e7c
- id: src-20260822-readme-3
  resource: urn:llmwiki:source:src-20260822-readme-3
  title: ninja_core Readme
  content_hash: sha256:c13dcf9055a532fefb03664983e9b5bafcb384e7ff16b65feca801cdbff23ba5
- id: src-20260822-developmentlog
  resource: urn:llmwiki:source:src-20260822-developmentlog
  title: NinjaRobotPi0 Development Log
  content_hash: sha256:65b40cbc41f1966bee59663ab0e61126fef8b9c38bf3f8ca15e785677ce16607
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
---

# Action Library and AI Agent

NinjaRobotPi0 combines large language model intelligence with an extensible on-robot action library, allowing natural language commands to trigger complex multi-modal behaviors.[^src-20260822-readme-3] [^src-20260822-developmentguide]

## Google Gemini Agent (`ninja_core.ninja_agent`)

The AI agent uses the Gemini model selected and validated during API-key setup; legacy configurations without a saved model retain `gemini-3-flash-preview` as their compatibility default.[^src-20260822-readme-3] [^src-20260822-developmentguide] [^src-20260822-developmentlog]

* **Validated Model Selection**: `config set-key gemini` and the guided initializer retrieve models available to the supplied key, require `generateContent`, and save the key/model pair only after a bounded generation probe succeeds.[^src-20260822-developmentguide] [^src-20260822-developmentlog]
* **Gemini 3 Compatibility**: Gemini 3 requests use the REST compatibility path with low thinking and a 60-second bound because the installed legacy SDK cannot express current thinking controls; older models retain the bounded SDK path.[^src-20260822-developmentguide] [^src-20260822-developmentlog]
* **Point-in-Time Validation**: A successful setup probe confirms that the selected model responded during configuration; later quota, network, permission, latency, or model-availability changes can still cause runtime failures.[^src-20260822-developmentguide] [^src-20260822-developmentlog]

* **Natural Language Understanding**: Supports conversational chat in English, Japanese, and Traditional/Simplified Chinese.[^src-20260822-readme-3]
* **Semantic Action Planning**: Maps user intent to structured action plans containing:
  * **Movement**: Pre-recorded sequence or saved Blockly action.[^src-20260822-developmentlog]
  * **Expression**: Display face (`happy`, `scary`, `sleepy`, `speaking`, etc.).[^src-20260822-readme-3]
  * **Sound**: Emotion tone or musical melody.[^src-20260822-readme-3]
  * **Spoken Response**: Natural language response synthesized in the user's language.[^src-20260822-readme-3]
* **Action Chaining**: Combines movements, sounds, and facial expressions into synchronized execution sequences.[^src-20260822-readme-3]

## Saved Blockly Action Library (`ActionLibrary`)

The `ActionLibrary` (`ninja_core.action_library.ActionLibrary`) manages custom actions uploaded from the Code IDE over BLE or Web:[^src-20260822-developmentguide] [^src-20260822-developmentlog]

* **Storage**: Saved as `ninja-action-v1` JSON files under `ninja_actions/*.json`.[^src-20260822-developmentlog]
* **Protected Overwrite**:
  * Native movements defined in `config.json` (e.g. `wave`, `bow`) are protected and cannot be overwritten.[^src-20260822-developmentlog]
  * Existing user actions can be replaced if `overwrite=True` is provided.[^src-20260822-developmentlog]
* **Dynamic Agent Integration**: Saved actions are automatically loaded into the Gemini prompt so the robot can trigger user-created Blockly programs via voice/chat commands.[^src-20260822-developmentlog]

## Cooperative Interruption

When a new user message arrives while a previous movement or action plan is executing, the server executes a cooperative interruption sequence:[^src-20260822-developmentlog]
1. Signals cancellation to `SafeExecutor`.[^src-20260822-developmentlog]
2. Calls `ServoGroup.abort()` to halt active motor trajectories.[^src-20260822-developmentlog]
3. Resets sound and face queues.[^src-20260822-developmentlog]
4. Acquires an async execution lock before starting the new action plan.[^src-20260822-developmentlog]

[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.
[^src-20260822-readme-3]: ninja_core Readme.
[^src-20260822-developmentlog]: NinjaRobotPi0 Development Log.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.
