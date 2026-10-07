---
type: Concept
title: Architecture and Hardware Abstraction Layer
description: Monorepo structure, dynamic driver loading, interface ABCs, and centralized
  configuration in NinjaRobotPi0.
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
- id: src-20260822-readme-4
  resource: urn:llmwiki:source:src-20260822-readme-4
  title: ninja_utils Readme
  content_hash: sha256:67508fde5377631a44c87d1c9c207da2c86f09531ab3d9e5d229af985e999d05
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
---

# Architecture and Hardware Abstraction Layer

NinjaRobotPi0 adopts a layered, modular architecture where independent hardware driver packages are decoupled from the core application logic through a Hardware Abstraction Layer (HAL).[^src-20260822-developmentguide] [^src-20260822-readme-3]

## Monorepo Package Layout

The project consists of 7 standalone Python packages and 1 React web application:[^src-20260822-developmentguide]

```
NinjaRobotPi0/
├── pyproject.toml              # Root workspace definition
├── config.json                 # Centralized master runtime configuration
├── servo.json, buzzer.json...  # Subsystem configuration files
├── ninja_utils/                # Shared logging, keyboard, and ABC interfaces
├── ninja_ble/                  # BLE GATT server and chunking protocol
├── ninja_webapp/               # React 18 + Vite web interface
├── pi0servo/                   # Velocity-based servo controller
├── pi0buzzer/                  # Non-blocking passive buzzer driver
├── pi0vl53l0x/                 # Thread-safe VL53L0X distance sensor driver
├── pi0disp/                    # Thread-safe ST7789V display driver
└── ninja_core/                 # Main application, HAL, web server, AI agent
```

## Abstract Base Classes (`ninja_utils.interfaces`)

The shared interfaces define the expected sensor and actuator contracts; individual drivers can satisfy those contracts directly or through compatibility behavior.[^src-20260822-developmentguide]

* **`Actuator`**: Defines standard lifecycle methods for output devices:
  * `initialize()`: Establishes the hardware connection and prepares a safe default state.[^src-20260822-developmentguide]
  * `execute(command: dict)`: Executes a structured command dictionary (e.g. `{"angles": [...]}` or `{"image": img}`).[^src-20260822-readme-4]
  * `off()`: Silences or disables the device safely.[^src-20260822-readme-4]
* **`Sensor`**: Defines standard methods for input sensors:
  * `initialize()`: Establishes the sensor connection and performs required setup.[^src-20260822-developmentguide]
  * `get_data() -> dict[str, Any]`: Returns sensor-specific data, including distance and validity fields for distance sensors.[^src-20260822-developmentguide]
  * `close()`: Releases sensor and bus resources.[^src-20260822-developmentguide]

## Dynamic Driver Registry (`ninja_core.hal`)

The HAL (`ninja_core/hal.py`) initializes and coordinates drivers using dynamic module loading via `importlib` rather than hardcoded static imports:[^src-20260822-readme-3] [^src-20260822-developmentguide]

```python
DRIVER_REGISTRY = {
    "servos": {"module": "pi0servo.core.multi_servos", "class": "ServoGroup"},
    "buzzer": {"module": "pi0buzzer.driver", "class": "MusicBuzzer"},
    "display": {"module": "pi0disp.core.driver", "class": "ST7789V"},
    "distance_sensor": {"module": "pi0vl53l0x.driver", "class": "VL53L0X"},
}
```

This design allows individual drivers to be updated, replaced, or mocked during automated testing without modifying the core server.[^src-20260822-developmentguide]

## Centralized Configuration (`config.json`)

All runtime settings are consolidated into a master `config.json` managed by `ninja_core.config.NinjaConfig`:[^src-20260822-readme-3] [^src-20260822-developmentguide]
* **Hardware settings**: Servo pulse calibrations, buzzer volume, display rotation/brightness, sensor offsets.[^src-20260822-developmentguide]
* **System settings**: Robot name (`bluetooth.name`), robot type (`robot_type`: `tire`, `humanoid`, `spider`), API keys, selected Gemini agent model, and ngrok authtoken.[^src-20260822-developmentguide]
* **Synchronization**: Subsystem configurations can be synchronized via `uv run ninja_core config import` or `config import-all`.[^src-20260822-readme-3] [^src-20260822-developmentguide]

[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.
[^src-20260822-readme-3]: ninja_core Readme.
[^src-20260822-readme-4]: ninja_utils Readme.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.
