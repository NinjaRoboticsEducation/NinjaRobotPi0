---
type: Entity
title: ninja_utils Package
description: Shared utilities package containing Abstract Base Classes, centralized
  logging, and systemd service managers.
status: draft
generated:
  by: codex/repository-migration
  at: '2026-10-07T07:00:29.384460+00:00'
sources:
- id: src-20260822-readme-4
  resource: urn:llmwiki:source:src-20260822-readme-4
  title: ninja_utils Readme
  content_hash: sha256:c8224fa991d7331e188187187def4af8e454464a762d05f7ad91fba5e7104cde
- id: src-20260822-developmentguide
  resource: urn:llmwiki:source:src-20260822-developmentguide
  title: NinjaRobotPi0 Development Guide
  content_hash: sha256:43e40f7c8db5734b4e8fe2ffd7d1e9c365cf9ceaad16fb4dbbbbe8eb1be71e7c
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
---

# ninja_utils Package

`ninja_utils` provides shared foundation utilities and interface contracts across all NinjaRobotPi0 packages.[^src-20260822-readme-4] [^src-20260822-developmentguide]

## Module Summary

* **`interfaces.py`**: Defines the `Actuator` and `Sensor` Abstract Base Classes (ABCs) and the `DistanceData` dataclass.[^src-20260822-readme-4] [^src-20260822-developmentguide]
* **`my_logger.py`**: Centralized, formatted logging system for console and file output.[^src-20260822-readme-4]
* **`keyboard.py`**: Non-blocking single-keypress terminal input helper for interactive TUIs.[^src-20260822-readme-4]
* **`service_manager.py`**: Manages Linux systemd service configuration for autostarting the robot on boot.[^src-20260822-developmentguide]

## CLI Commands

* `uv run ninja_utils install-startup`: Installs and enables the `ninjarobot.service` systemd unit.[^src-20260822-readme-4]
* `uv run ninja_utils remove-startup`: Disables and removes the autostart service.[^src-20260822-readme-4]
* `uv run ninja_utils status-startup`: Checks the status of the systemd service.[^src-20260822-readme-4]

[^src-20260822-readme-4]: ninja_utils Readme.
[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.
