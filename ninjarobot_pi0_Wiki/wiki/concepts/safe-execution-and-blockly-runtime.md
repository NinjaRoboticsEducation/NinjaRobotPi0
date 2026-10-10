---
type: Concept
title: Safe Code Execution and Blockly Runtime
description: Sandboxed Python execution, AST compilation preflight, runtime ownership
  switching, and GPIO-first wrapper contracts.
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
- id: src-20261010-lifecyclerefinementsimplementationplan
  resource: urn:llmwiki:source:src-20261010-lifecyclerefinementsimplementationplan
  title: Lifecyclerefinementsimplementationplan
  content_hash: sha256:5d4be31936118493340340291e66a59c7f76886f26e791ca0963721aab9f21a8
- id: src-20261010-lifecyclerefinementsvalidation
  resource: urn:llmwiki:source:src-20261010-lifecyclerefinementsvalidation
  title: Lifecyclerefinementsvalidation
  content_hash: sha256:01fa07f823e9dedfcc2d243ae107b496758960b0c5be790db9df2a8deef94066
semantic_review:
  version: 1
  performed_by: agent:antigravity
  performed_at: '2026-10-10T12:07:31.827347+00:00'
  target_hash: sha256:7b3920fa4e8b0cf06cbce8c129c9bd0c2cd9d90beeb3f8ca9a24aed1188354a9
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed safe execution against RuntimePipeline, web_sessions.py, and test_lifecycle_refinements.py.
    Browser disconnect cancellation, 35s inactivity timeout, generation token checks,
    and waiting QR hold match code.
  - Cancellation is cooperative across step boundaries and motion locks; instant hardware
    abort is not guaranteed.
---

# Safe Code Execution and Blockly Runtime

NinjaRobotPi0 enables students and researchers to execute generated Python scripts and Blockly visual code through a restricted on-robot execution path.[^src-20260822-readme-3] [^src-20260822-developmentguide]

## Sandboxed Python Execution Engine (`SafeExecutor`)

`SafeExecutor` runs user and AI scripts in an isolated execution thread with AST validation:[^src-20260822-readme-3] [^src-20260822-developmentguide]

* **AST Preflight Compilation**: Code is compiled and checked for dangerous imports (`os`, `sys`, `subprocess`, `shutil`) before starting the worker thread.[^src-20260822-developmentguide] [^src-20260822-developmentlog]
* **Syntax Error Isolation**: Syntax and compilation errors return structured diagnostic events (`line`, `offset`, `text`) without triggering hardware cleanup or stopping native face animations.[^src-20260822-developmentlog]
* **Cooperative Cancellation**: Generated loops periodically call `check_stop()`, allowing web UI or BLE `stop` commands to request a halt.[^src-20260822-developmentlog]

> [!IMPORTANT]
> Cancellation is cooperative rather than a forced thread kill. Python loops that never call `check_stop()` may require the Stop Robot path or a server restart.[^src-20260822-developmentguide]

## Dual Pipeline & Ownership Management (`RuntimePipeline`)

To prevent conflicts between native robot behavior (such as idle face animations and web UI commands) and uploaded Blockly programs, `RuntimePipeline` coordinates execution ownership:[^src-20260822-developmentguide] [^src-20260822-developmentlog]

1. **Native Idle Mode**: The robot displays natural blinking and breathing expressions.[^src-20260822-developmentlog]
2. **Blockly Execution Mode**: Upon valid script launch, native idle loops pause, allowing the script exclusive control over servos, display, and buzzer.[^src-20260822-developmentlog]
3. **Display Clear Hold**: When script calls `robot.display.clear()`, the screen stays intentionally blank until native interaction, the next upload, or Disconnect.[^src-20260822-developmentlog]
4. **Restoration**: On script completion, stop button press, or BLE disconnection, native ownership and idle animations resume gracefully.[^src-20260822-developmentlog]

## GPIO-First Motion & Sensor Wrapper Contract

For visual Blockly code generation (`web-blockly-v2`), `ninja_core.api_wrappers` exposes high-level, safe APIs:[^src-20260822-developmentguide] [^src-20260822-developmentlog]

* **`robot.servos.move_pin(pin, angle, speed_mode="M")`**: Moves a specific GPIO pin (`20..27`) with angle clamping (`-90..90`).[^src-20260822-developmentlog]
* **`robot.servos.move_pins({pin: angle}, per_servo_speeds={...})`**: Synchronized multi-pin motion routed to `pi0servo.move_all_sync()`.[^src-20260822-developmentlog]
* **`robot.distance.read()`**: Returns distance in millimeters. If the physical sensor is disconnected or I2C errors occur, it safely returns `9999` (fallback) to prevent accidental obstacle emergency halts.[^src-20260822-developmentguide] [^src-20260822-developmentlog]
* **`robot.display.text(text, scroll=False, lang="auto")`**: Displays static or scrolling multilingual text using Noto fonts.[^src-20260822-developmentguide] [^src-20260822-developmentlog]
* **`robot.buzzer.play_song(name)`**: Plays named songs (`happy_birthday`, `jingle_bells`, etc.) asynchronously.[^src-20260822-developmentguide] [^src-20260822-developmentlog]

[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.
[^src-20260822-readme-3]: ninja_core Readme.
[^src-20260822-developmentlog]: NinjaRobotPi0 Development Log.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.
## Browser disconnect cooperative cancellation (2026-10-10)

Closing the controlling browser or timing out after 35 seconds of inactivity triggers cooperative cancellation across active Blockly and native robot tasks.[^src-20261010-lifecyclerefinementsimplementationplan] `RuntimePipeline` aborts running movements and greeting tasks, restores the waiting reconnect QR on the display, and suppresses idle face expressions until reconnection. Generation tokens ensure stale callbacks from disconnected sessions cannot resume control even if the same cookie reconnects.[^src-20261010-lifecyclerefinementsvalidation]

[^src-20261010-lifecyclerefinementsimplementationplan]: Lifecycle refinements implementation plan.
[^src-20261010-lifecyclerefinementsvalidation]: Lifecycle refinements validation report.
