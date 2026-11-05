---
type: Entity
title: ninja_ble Package
description: Bluetooth Low Energy peripheral service package implementing GATT characteristics
  and binary chunking.
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
- id: src-20260822-developmentlog
  resource: urn:llmwiki:source:src-20260822-developmentlog
  title: NinjaRobotPi0 Development Log
  content_hash: sha256:54cdbd7e50fd0cbfbfaba5073d6ed89379181b78bc3d7267d64518f15e9bfe02
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
- id: src-20261013-ninja-ble-readme
  resource: urn:llmwiki:source:src-20261013-ninja-ble-readme
  title: 20261013 Ninja Ble Readme
  content_hash: sha256:ad753692c64d2f1dbd3053dc3dccd0a9f6a9b62a7c4e1cfa669e76b388ee4b0d
- id: src-20261013-bleonboardingvalidation
  resource: urn:llmwiki:source:src-20261013-bleonboardingvalidation
  title: 20261013 Bleonboardingvalidation
  content_hash: sha256:075fc0ec0750428ab1b408ba66b4e81100528d3bbb6e0498ca84eb3e5b04f181
semantic_review:
  version: 1
  performed_by: agent:antigravity
  performed_at: '2026-10-13T05:55:00+00:00'
  target_hash: sha256:1e069c87a86ad4b3c45eb8c7295f1ef7dd735044920e29ab848d2e433b5501a6
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed ninja_ble.system_setup implementation against ninja-ble-README and BLEOnboardingValidation.
  - Verified systemd unit verification, sysfs rfkill parsing, D-Bus adapter power
    toggling, and temporary advertisement lifecycle.
  - Physical Raspberry Pi Bluetooth radio operation and reboot power persistence remain
    unverified.
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

## Bluetooth System Readiness and Repair Helper (2026-10-13)

`ninja_ble` introduces `ninja_ble.system_setup` (`system_setup.py`) to verify and repair OS Bluetooth prerequisites prior to launching the robot runtime:[^src-20261013-ninja-ble-readme] [^src-20261013-bleonboardingvalidation]
* **System Service Verification**: Inspects `bluetooth.service` unit state via systemd D-Bus/systemctl; rejects masked units and enables/starts loaded inactive units during repair.[^src-20261013-bleonboardingvalidation] Legacy `hciuart.service` is evaluated only if no kernel controller exists and serial1 UART prerequisites are met.[^src-20261013-ninja-ble-readme]
* **RFKill Block Inspection**: Directly parses kernel attributes in `/sys/class/rfkill` (type `bluetooth`) for soft and hard radio blocks rather than parsing localized CLI output; executes `rfkill unblock bluetooth` during repair.[^src-20261013-bleonboardingvalidation]
* **Controller Power Verification**: Uses BlueZ D-Bus (`org.bluez.Adapter1`) to verify controller presence and toggles `Powered=True` if disabled.[^src-20261013-ninja-ble-readme]
* **Temporary Advertisement Probe**: Registers a short-lived connectable peripheral advertisement (`org.bluez.LEAdvertisement1` type `peripheral` via `org.bluez.LEAdvertisingManager1`) without robot command characteristics, verifies registration, and explicitly unregisters it.[^src-20261013-bleonboardingvalidation]
* **Safety & Isolation**: Readiness inspection does not instantiate HAL, energize GPIO, start the GATT robot server, cycle controller power, modify Wi-Fi, edit boot/UART settings, remove pairings, or alter system security policies.[^src-20261013-ninja-ble-readme] [^src-20261013-bleonboardingvalidation]

[^src-20261013-ninja-ble-readme]: ninja_ble package README with Bluetooth readiness contracts (2026-10-13).
[^src-20261013-bleonboardingvalidation]: BLE onboarding validation evidence and system setup records (2026-10-13).
