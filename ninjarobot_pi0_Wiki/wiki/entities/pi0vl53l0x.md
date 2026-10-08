---
type: Entity
title: pi0vl53l0x Package
description: Hardened VL53L0X Time-of-Flight distance sensor driver with transaction-level
  locking and bus recovery.
status: draft
generated:
  by: codex/migration-audit
  at: '2026-10-07T07:13:37.354382+00:00'
sources:
- id: src-20260822-readme-8
  resource: urn:llmwiki:source:src-20260822-readme-8
  title: pi0vl53l0x Readme
  content_hash: sha256:ddf100f609e7335b81dc3803c453c3d0dc66fbe0c20a52917d90407bc1d2f35e
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
semantic_review:
  version: 1
  performed_by: agent:antigravity
  performed_at: '2026-10-07T07:47:00+00:00'
  target_hash: sha256:81d35a5a809de25596b23ff82148ecca587b31c4daebb914935b01f484a92cbb
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - VL53L0X I2C timing budgets and error handling match pi0vl53l0x README.
  - Absolute matches ('safe') describe thread-safe I2C bus wrapper.
---

# pi0vl53l0x Package

`pi0vl53l0x` is a robust Python driver for the VL53L0X Time-of-Flight distance sensor using `pigpio` I2C on Raspberry Pi.[^src-20260822-readme-8] [^src-20260822-developmentguide]

## Core Features

* **Transaction-Level Locking**: Wraps complete single-shot ranging transactions in a `threading.RLock`, preventing race conditions when both the background `DistanceMonitor` and Blockly user scripts query the sensor.[^src-20260822-readme-8] [^src-20260822-developmentlog]
* **Hardened Boot Initialization**: Firmware boot polling (up to 1.0s timeout) resolves the legacy "returns 0mm after reboot" issue.[^src-20260822-readme-8]
* **Automatic Bus Recovery**: Exponential backoff retry (10→20→50ms) with bus reinitialization upon repeated communication failures.[^src-20260822-readme-8]
* **Async Ready**: `get_range_async()` runs ranging in a thread pool executor for seamless asyncio integration.[^src-20260822-readme-8]

## Key Classes & Modules

* **`VL53L0X` (`pi0vl53l0x.core.sensor`)**: Main sensor driver providing sensor-compatible initialization, data, and cleanup methods.[^src-20260822-readme-8] [^src-20260822-developmentguide]
* **`I2CBus` (`pi0vl53l0x.core.i2c`)**: Thread-safe I2C bus wrapper with retry and error handling.[^src-20260822-readme-8]
* **`registers.py`**: Semantic register constants (~60 registers) for full hardware control.[^src-20260822-readme-8]
* **`ConfigManager` (`pi0vl53l0x.config.config_manager`)**: Manages `vl53l0x.json` offset calibration data.[^src-20260822-readme-8]

## CLI Commands

* `uv run pi0vl53l0x get [--count N] [--interval S]`: Reads distance measurements.[^src-20260822-readme-8]
* `uv run pi0vl53l0x test`: Runs quick 5-sample diagnostic read.[^src-20260822-readme-8]
* `uv run pi0vl53l0x calibrate --distance <mm>`: Guided offset calibration at known target distance.[^src-20260822-readme-8]
* `uv run pi0vl53l0x sensor-tool`: Launches the 8-option interactive TUI.[^src-20260822-readme-8]

[^src-20260822-readme-8]: pi0vl53l0x Readme.
[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.
[^src-20260822-developmentlog]: NinjaRobotPi0 Development Log.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.
