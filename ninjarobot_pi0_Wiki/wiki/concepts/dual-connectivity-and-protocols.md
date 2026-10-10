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
- id: src-20261010-lifecyclerefinementsimplementationplan
  resource: urn:llmwiki:source:src-20261010-lifecyclerefinementsimplementationplan
  title: Lifecyclerefinementsimplementationplan
  content_hash: sha256:5d4be31936118493340340291e66a59c7f76886f26e791ca0963721aab9f21a8
- id: src-20261010-lifecyclerefinementsevidence
  resource: urn:llmwiki:source:src-20261010-lifecyclerefinementsevidence
  title: Lifecyclerefinementsevidence
  content_hash: sha256:c34468e740adccacc6546a2afe39fd41562eed229ae5795255577b044d4fd09e
semantic_review:
  version: 1
  performed_by: agent:antigravity
  performed_at: '2026-10-10T12:07:31.827347+00:00'
  target_hash: sha256:45d874d13f415c12c4258ac4a2c9819f955869c3a82cb3db4789904d2790343d
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed connectivity protocols against web_server.py, web_sessions.py, and ninja_ble.
    Session ownership via /ws/session and HttpOnly cookie, 423/503 status codes, and
    BLE independence match code.
  - Session ownership provides connection management, not user authentication. BLE
    advertising is not an active controller.
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
## Web session ownership protocol (2026-10-10)

NinjaRobotPi0 web connectivity enforces a single-browser session ownership protocol via `/ws/session` and a server-issued HttpOnly `ninja_web_session` cookie.[^src-20261010-lifecyclerefinementsimplementationplan]
This protocol governs connection ownership rather than login authentication. API requests require live primary ownership (returning 423 when inactive, 503 during server shutdown), and secondary connections receive close code 4409. BLE remains an independent protocol, and BLE advertising is never counted as an active browser session controller.[^src-20261010-lifecyclerefinementsevidence]

[^src-20261010-lifecyclerefinementsimplementationplan]: Lifecycle refinements implementation plan.
[^src-20261010-lifecyclerefinementsevidence]: Lifecycle refinements implementation evidence.
