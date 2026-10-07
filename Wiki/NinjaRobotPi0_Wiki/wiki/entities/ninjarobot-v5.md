---
type: Entity
title: NinjaRobotPi0 Entity
description: Complete hardware platform entity specifications, configurations, robot
  types, and safety lifecycle.
status: draft
generated:
  by: codex/migration-audit
  at: '2026-10-07T07:13:37.354382+00:00'
sources:
- id: src-20260822-readme
  resource: urn:llmwiki:source:src-20260822-readme
  title: NinjaRobotPi0 Readme
  content_hash: sha256:3f74856140111a6337bf8b83c58bef7be13f91df9742fc0e36be27ebd35b8df2
- id: src-20260822-developmentguide
  resource: urn:llmwiki:source:src-20260822-developmentguide
  title: NinjaRobotPi0 Development Guide
  content_hash: sha256:d1f8e19627223cb320b2e05df9a141c768ca0f418a7f77d160b6127d08c439e9
- id: src-20260822-installationguide
  resource: urn:llmwiki:source:src-20260822-installationguide
  title: NinjaRobotPi0 Installation Guide
  content_hash: sha256:3748116db5b7241f6cb501b2bea2ff23d74754cab8776cebcbbbe19ff0e9f088
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
---

# NinjaRobotPi0 Entity

**NinjaRobotPi0** is the physical and logical robot entity integrating the Raspberry Pi Zero 2W single-board computer, 8 servo actuators, an ST7789V IPS display, a VL53L0X distance sensor, and a passive buzzer.[^src-20260822-readme] [^src-20260822-installationguide]

## Robot Types & Profiles

NinjaRobotPi0 supports multiple physical configurations through the `robot_type` configuration:[^src-20260822-developmentguide]

* **`tire`**: Wheeled educational robot configuration.[^src-20260822-developmentguide]
* **`humanoid`**: Bipedal/humanoid articulated robot with arms and legs.[^src-20260822-developmentguide]
* **`spider`**: Multi-legged quadruped/hexapod walker configuration.[^src-20260822-developmentguide]

The robot profile is broadcast over BLE (`robot_info`) to enable the Code IDE to adapt Blockly block options dynamically.[^src-20260822-developmentguide]

## Power & Hardware Pinout Summary

```
Raspberry Pi Zero 2W GPIO Pinout (40-Pin Header)
┌─────────────────────────────────────┐
│  3.3V  [1] [2]  5V                  │  ← Sensor/Display Logic Power (3.3V)
│  SDA   [3] [4]  5V                  │  ← VL53L0X I2C Data (GPIO 2)
│  SCL   [5] [6]  GND                 │  ← VL53L0X I2C Clock (GPIO 3)
│  GPIO4 [7] [8]  GPIO14 (DC)         │  ← ST7789V Data/Command
│  GND   [9] [10] GPIO15 (RST)        │  ← ST7789V Reset
│  GPIO17[11] [12] GPIO18             │  ← Passive Buzzer (GPIO 17)
│  ...   [..] [..] ...                │
│  SPI0 MOSI [19] [20] GND            │  ← ST7789V SPI MOSI
│  SPI0 SCLK [23] [24] SPI0 CE0       │  ← ST7789V SPI SCLK & Chip Select
│  GPIO19[35] [36] GPIO16 (BLK)       │  ← ST7789V Backlight PWM
│  GPIO26[37] [38] GPIO20 (Servo 1)   │  ← Servo Motors (GPIO 20–27)
│  GND  [39] [40] GPIO21 (Servo 2)   │
└─────────────────────────────────────┘
```

> [!CAUTION]
> Servo power (5V Red wires) must always be supplied by an external 5V 3A+ power supply with common ground to the Raspberry Pi.[^src-20260822-installationguide]

## Safety & Graceful Shutdown

* **Emergency Halt**: Requests immediate cancellation of active servo motion and resets servo targets.[^src-20260822-readme] [^src-20260822-developmentguide]
* **Graceful Shutdown Sequence**:
  1. Displays `sleepy` face and plays `sleepy` sound in parallel.[^src-20260822-readme] [^src-20260822-developmentguide]
  2. Moves servos to the pre-configured `Poweroff` rest position.[^src-20260822-developmentguide]
  3. Releases all HAL handles and triggers Linux OS shutdown (`sudo poweroff`).[^src-20260822-developmentguide]

[^src-20260822-readme]: NinjaRobotPi0 Readme.
[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.
[^src-20260822-installationguide]: NinjaRobotPi0 Installation Guide.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.
