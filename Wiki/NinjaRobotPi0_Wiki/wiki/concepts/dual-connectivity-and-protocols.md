---
type: Concept
title: Dual Connectivity and Communication Protocols
description: Dual Wi-Fi and Bluetooth Low Energy connectivity, GATT service specifications,
  and chunked transfer protocols.
status: draft
generated:
  by: codex/migration-audit
  at: '2026-10-07T07:13:37.354382+00:00'
sources:
- id: src-20260822-readme-2
  resource: urn:llmwiki:source:src-20260822-readme-2
  title: ninja_ble Readme
  content_hash: sha256:7323f365547e7e9f413122533d7d7ec27ed3367f555540dc8b51df6078b09061
- id: src-20260822-developmentguide
  resource: urn:llmwiki:source:src-20260822-developmentguide
  title: NinjaRobotPi0 Development Guide
  content_hash: sha256:d1f8e19627223cb320b2e05df9a141c768ca0f418a7f77d160b6127d08c439e9
- id: src-20260822-readme
  resource: urn:llmwiki:source:src-20260822-readme
  title: NinjaRobotPi0 Readme
  content_hash: sha256:3f74856140111a6337bf8b83c58bef7be13f91df9742fc0e36be27ebd35b8df2
- id: src-20260822-developmentlog
  resource: urn:llmwiki:source:src-20260822-developmentlog
  title: NinjaRobotPi0 Development Log
  content_hash: sha256:54cdbd7e50fd0cbfbfaba5073d6ed89379181b78bc3d7267d64518f15e9bfe02
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
---

# Dual Connectivity and Communication Protocols

NinjaRobotPi0 features dual connectivity that allows users to interact with the robot over local Wi-Fi, remote ngrok tunnels, or zero-configuration Bluetooth Low Energy (BLE).[^src-20260822-readme] [^src-20260822-developmentguide]

## Connectivity Architecture

All input channels funnel into the central `CommandDispatcher` in `ninja_core`, which routes actions to the HAL, AI Agent, or SafeExecutor:[^src-20260822-readme-2] [^src-20260822-developmentguide]

```
┌──────────────────┐       HTTP / WebSockets       ┌────────────────────────┐
│  Web / Mobile    │ ───────────────────────────▶  │ ninja_core.web_server  │
│  (React WebApp)  │ ◀───────────────────────────  │ (FastAPI on Port 8000) │
└──────────────────┘                               └───────────┬────────────┘
                                                               │
┌──────────────────┐         BLE GATT Protocol                 │
│ Code IDE App /   │ ───────────────────────────▶  ┌───────────▼────────────┐
│ nRF Connect      │ ◀───────────────────────────  │ ninja_ble.NinjaBLE     │
└──────────────────┘                               └───────────┬────────────┘
                                                               │
                                                   ┌───────────▼────────────┐
                                                   │   CommandDispatcher    │
                                                   └────────────────────────┘
```

## BLE GATT Service Specification

The BLE peripheral is implemented using `bless` with BlueZ on Linux:[^src-20260822-readme-2] [^src-20260822-developmentguide]

* **Service Name**: Configurable via `bluetooth.name` (default: `NinjaRobot`).[^src-20260822-developmentguide] [^src-20260822-developmentlog]
* **Service UUID**: `00000001-710e-4a5b-8d75-3e5b444bc3cf` [^src-20260822-readme-2]

### Characteristics

| Characteristic | UUID | Properties | Purpose |
|----------------|------|------------|---------|
| **Command** | `00000002-710e-4a5b-8d75-3e5b444bc3cf` | Write | Inbound JSON commands & chunks [^src-20260822-readme-2] |
| **Response** | `00000003-710e-4a5b-8d75-3e5b444bc3cf` | Read, Notify | Live notification stream [^src-20260822-readme-2] |
| **Command Status** | `00000004-710e-4a5b-8d75-3e5b444bc3cf` | Read | Cached status readback by `request_id` [^src-20260822-developmentlog] |

## Binary Chunking Protocol

For payloads exceeding BLE MTU limits (e.g. Blockly code uploads >160 bytes), a binary chunking protocol provides sequence tracking and CRC32 integrity checking:[^src-20260822-readme-2] [^src-20260822-developmentlog]

| Packet Type | Magic Byte | Format |
|-------------|------------|--------|
| **HEADER** | `0x01` | `[0x01][total_chunks: 2B][crc32: 4B][payload_len: 4B]` [^src-20260822-readme-2] |
| **DATA** | `0x02` | `[0x02][sequence: 2B][chunk_data: N bytes]` [^src-20260822-readme-2] |
| **EOF** | `0x03` | `[0x03][chunks_received: 2B]` [^src-20260822-readme-2] |

Each packet is ACKed (`{"type": "ack", "seq": N, "status": "ok"}`). On EOF, the server computes the CRC32 checksum before dispatching.[^src-20260822-readme-2]

## Command Status Caching

To prevent false timeout errors in web browsers when Bluetooth notification packets are dropped, `NinjaBLEService` caches command execution and save results by `request_id`.[^src-20260822-developmentlog] The browser can query characteristic `00000004` to recover confirmation state deterministically.[^src-20260822-developmentlog]

[^src-20260822-readme-2]: ninja_ble Readme.
[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.
[^src-20260822-readme]: NinjaRobotPi0 Readme.
[^src-20260822-developmentlog]: NinjaRobotPi0 Development Log.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.
