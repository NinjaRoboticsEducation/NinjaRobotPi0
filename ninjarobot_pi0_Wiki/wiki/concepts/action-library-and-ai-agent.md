---
type: Concept
title: Action Library and AI Agent
description: Google Gemini-powered agentic AI, saved Blockly action library, action chaining, and cooperative interruption.
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
- id: src-20260822-developmentlog
  resource: urn:llmwiki:source:src-20260822-developmentlog
  title: NinjaRobotPi0 Development Log
  content_hash: sha256:54cdbd7e50fd0cbfbfaba5073d6ed89379181b78bc3d7267d64518f15e9bfe02
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
- id: src-20261009-2026-10-09-builtin-movements
  resource: urn:llmwiki:source:src-20261009-2026-10-09-builtin-movements
  title: 2026 10 09 Builtin Movements
  content_hash: sha256:6bd14ef705bb60c2c228c95940fd6cb771299532f13e10fdc4faae22db3f216a
semantic_review:
  version: 1
  performed_by: agent:antigravity
  performed_at: '2026-10-09T17:10:48.021602+00:00'
  target_hash: sha256:7cab523a151bf38f67a8020d464fa09f6dc7b93298583d49c6e3a8fae9ab4cf3
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed ActionLibrary and Gemini AI agent native movement planning against ninja_agent.py. Action planning schema, permitted robot-type filtering, repetition bounds, and whole-chain validation match implementation.
  - Agent relies on configured API keys; configuration actions remain protected.
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
  * **Movement**: Pre-recorded sequence, permitted native movement, or saved Blockly action.[^src-20260822-developmentlog] [^src-20261009-2026-10-09-builtin-movements]
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

## Native movement action chaining and execution limits

The Gemini AI agent restricts native movement suggestions to executable movements matching the active robot type (`spider`, `wheel`/`tire`, or `humanoid`). Native movement chains from text and audio plans are validated with strict bounds: maximum 32 entries per chain and 1–20 positive integer repetitions per entry. Any unavailable or type-incompatible movement causes the entire native chain to be rejected while preserving the conversational response and logging the rejection reason.[^src-20261009-2026-10-09-builtin-movements]

[^src-20261009-2026-10-09-builtin-movements]: Automatic native built-in movement evidence and architecture boundaries.
