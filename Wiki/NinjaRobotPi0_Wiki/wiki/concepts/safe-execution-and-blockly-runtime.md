---
type: Concept
title: Safe Code Execution and Blockly Runtime
description: Sandboxed Python execution, AST compilation preflight, runtime ownership
  switching, and GPIO-first wrapper contracts.
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
