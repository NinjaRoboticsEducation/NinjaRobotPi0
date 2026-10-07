---
type: Entity
title: ninja_ble Package
description: Bluetooth Low Energy peripheral service package implementing GATT characteristics
  and binary chunking.
status: draft
generated:
  by: codex/repository-migration
  at: '2026-10-07T07:00:29.384460+00:00'
sources:
- id: src-20260822-readme-2
  resource: urn:llmwiki:source:src-20260822-readme-2
  title: ninja_ble Readme
  content_hash: sha256:76bbd36ab8a5d9d81b4e73fd2e3910e4c8a9b79c82e7558e94044e6c81871910
- id: src-20260822-developmentguide
  resource: urn:llmwiki:source:src-20260822-developmentguide
  title: NinjaRobotPi0 Development Guide
  content_hash: sha256:43e40f7c8db5734b4e8fe2ffd7d1e9c365cf9ceaad16fb4dbbbbe8eb1be71e7c
- id: src-20260822-developmentlog
  resource: urn:llmwiki:source:src-20260822-developmentlog
  title: NinjaRobotPi0 Development Log
  content_hash: sha256:65b40cbc41f1966bee59663ab0e61126fef8b9c38bf3f8ca15e785677ce16607
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
---

# ninja_ble Package

`ninja_ble` provides the Bluetooth Low Energy (BLE) peripheral interface for NinjaRobotPi0, enabling direct zero-configuration control from web browsers (Web Bluetooth) and mobile apps.[^src-20260822-readme-2] [^src-20260822-developmentguide]

## Architecture & Dependencies

* **`service.py`**: Implements `NinjaBLEService` using `bless` (GATT server) on top of BlueZ (`dbus-fast`) on Linux.[^src-20260822-readme-2]
* **`chunking.py`**: Handles packet fragmentation and reassembly for large payloads (>160 bytes) with CRC32 verification.[^src-20260822-readme-2] [^src-20260822-developmentlog]

## GATT Services and Characteristics

* **Service UUID**: `00000001-710e-4a5b-8d75-3e5b444bc3cf` [^src-20260822-readme-2]
* **Command Characteristic** (`...0002...`): Write JSON command or binary chunk.[^src-20260822-readme-2]
* **Response Characteristic** (`...0003...`): Read/Notify JSON events, status updates, and execution logs.[^src-20260822-readme-2]
* **Command Status Characteristic** (`...0004...`): Read cached response status by `request_id`.[^src-20260822-developmentlog]

## Custom Naming & Robot Info

The BLE advertisement name is configured in `config.json` under `bluetooth.name` (max 29 UTF-8 bytes).[^src-20260822-developmentlog] When queried via `{"type": "robot_info"}`, the service responds with the robot's configured name, type, and sanitized GPIO pin assignments.[^src-20260822-developmentlog]

[^src-20260822-readme-2]: ninja_ble Readme.
[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.
[^src-20260822-developmentlog]: NinjaRobotPi0 Development Log.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.
