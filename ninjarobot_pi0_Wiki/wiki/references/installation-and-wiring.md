---
type: Reference
title: Installation and Hardware Wiring Reference
description: Step-by-step assembly, complete GPIO wiring tables, Raspberry Pi OS 64-bit
  setup, and pigpio compilation.
status: draft
generated:
  by: codex/migration-audit
  at: '2026-10-07T07:13:37.354382+00:00'
sources:
- id: src-20260822-installationguide
  resource: urn:llmwiki:source:src-20260822-installationguide
  title: NinjaRobotPi0 Installation Guide
  content_hash: sha256:3748116db5b7241f6cb501b2bea2ff23d74754cab8776cebcbbbe19ff0e9f088
- id: src-20260822-developmentguide
  resource: urn:llmwiki:source:src-20260822-developmentguide
  title: NinjaRobotPi0 Development Guide
  content_hash: sha256:d1f8e19627223cb320b2e05df9a141c768ca0f418a7f77d160b6127d08c439e9
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
- id: src-20261007-2026-10-07-ninjarobot-pi0-migration-audit
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-migration-audit
  title: 2026 10 07 Ninjarobot Pi0 Migration Audit
  content_hash: sha256:6c223e850e920baffe83a0fbcf3f7c4471a97f4fbcc823e93d5cd2e33666d4ab
- id: src-20261009-installationguide
  resource: urn:llmwiki:source:src-20261009-installationguide
  title: Installationguide
  content_hash: sha256:0303e14ce171088cba240df2a0a3a29d88e2db0dc5cc2263f26f95d89ac68945
- id: src-20261007-2026-10-07-install-onboard-wiki-ui-2
  resource: urn:llmwiki:source:src-20261007-2026-10-07-install-onboard-wiki-ui-2
  title: Pi0 upgrade implementation and current UI contracts
  content_hash: sha256:1545ea683947c315a9ea0d4c30258c228e975a78e39062b2e045669fcff0cb9c
- id: src-20261007-2026-10-08-upgrade-audit
  resource: urn:llmwiki:source:src-20261008-upgrade-audit
  title: Pi0 upgrade audit findings and boundaries
  content_hash: sha256:7112a6575c6288875e3fdad33679f094b22908e0ee729b29f5dfbfc55f48de64
- id: src-20261008-2026-10-08-trixie-support
  resource: urn:llmwiki:source:src-20261008-trixie-support
  title: Trixie installer correction and validation boundary
  content_hash: sha256:3aae04cfab13e782c5748e8ca26721d860d0d842ac18c5544fd8ae0f82dc2945
- id: src-20261008-2026-10-08-installer-recovery
  resource: urn:llmwiki:source:src-20261008-installer-recovery
  title: Installer diagnostics and recovery validation
  content_hash: sha256:416eea41c04d6dc6ed633fa695b276a48574d22eacb21db5131de3577dbe4fc3
- id: src-20261008-2026-10-08-installer-compatibility
  resource: urn:llmwiki:source:src-20261008-installer-compatibility
  title: 2026 10 08 Installer Compatibility
  content_hash: sha256:7eaa21e7a1f79122e25e10dc37ae91a488aebe3ccff9db5e6c7b59db0684928f
- id: src-20261009-2026-10-09-builtin-movements
  resource: urn:llmwiki:source:src-20261009-2026-10-09-builtin-movements
  title: 2026 10 09 Builtin Movements
  content_hash: sha256:6bd14ef705bb60c2c228c95940fd6cb771299532f13e10fdc4faae22db3f216a
- id: src-20261010-installationguide-2
  resource: urn:llmwiki:source:src-20261010-installationguide-2
  title: Installationguide
  content_hash: sha256:18d2002125e05e7026c4bc7568ba8fb1f588a466bc7815f850476e07fa922913
semantic_review:
  version: 1
  performed_by: agent:antigravity
  performed_at: '2026-10-10T12:07:31.827347+00:00'
  target_hash: sha256:f12a776d5402071a53ea9c31055db4c70161a8a2410d850bac5d9b782d771947
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed installation and wiring reference against 2026-10-10 InstallationGuide.md.
    Five-launcher verification in .venv/bin and ninjarobotpi0 prompt match installation
    practice.
  - Hardware wiring, power isolation, and physical calibration verification remain
    mandatory before operation.
---

# Installation and Hardware Wiring Reference

This document provides complete physical wiring diagrams, pinout tables, and installation prerequisites for assembling the NinjaRobotPi0 platform on Raspberry Pi Zero 2 W.[^src-20260822-installationguide] [^src-20260822-developmentguide]

## Hardware Bill of Materials (BOM)

| Component | Interface / Pins | Role | Power Source |
|-----------|------------------|------|--------------|
| **Raspberry Pi Zero 2 W** | Broadcom BCM2837B0 | Central controller | 5V / 2.5A Micro-USB / GPIO header |
| **MicroSD Card (32GB+)** | SDIO | Raspberry Pi OS 64-bit | Pi 3.3V bus |
| **8x Micro Servos (SG90)** | GPIO 20–27 (PWM) | Articulation / Wheels / Legs | External 5V/3A UBEC/regulator (common GND) |
| **ST7789 SPI LCD (240x240)** | SPI0 (MOSI, SCLK, CE0, DC, RST, BLK) | Facial expressions / status | Pi 3.3V rail |
| **Passive Buzzer** | GPIO 12 (PWM) | Audio expressions & tones | Pi 3.3V / 5V rail |
| **VL53L0X ToF Sensor** | I2C1 (SDA: GPIO 2, SCL: GPIO 3) | Distance measurement | Pi 3.3V rail |

## Complete GPIO Pinout Assignment Table

| Pin # | Broadcom BCM | Function / Device | Wire Color / Notes |
|-------|--------------|-------------------|-------------------|
| 1 | 3V3 | Display / Sensor / Buzzer VCC | Red (3.3V) |
| 2 | 5V | External regulator / Pi power | Red (5V) |
| 3 | GPIO 2 (SDA) | VL53L0X I2C Data | Blue |
| 5 | GPIO 3 (SCL) | VL53L0X I2C Clock | Yellow |
| 6 | GND | Common Ground | Black |
| 19 | GPIO 10 (MOSI)| ST7789 SPI Data | Green |
| 23 | GPIO 11 (SCLK)| ST7789 SPI Clock | Yellow |
| 24 | GPIO 8 (CE0)  | ST7789 Chip Select | Orange |
| 22 | GPIO 25       | ST7789 DC (Data/Command)| White |
| 18 | GPIO 24       | ST7789 RST (Reset) | Brown |
| 12 | GPIO 18       | ST7789 BLK (Backlight)| Purple |
| 32 | GPIO 12       | Passive Buzzer PWM | Blue |
| 38 | GPIO 20       | Servo Ch 0 (PWM via pigpio) | Signal wire |
| 40 | GPIO 21       | Servo Ch 1 (PWM via pigpio) | Signal wire |
| 15 | GPIO 22       | Servo Ch 2 (PWM via pigpio) | Signal wire |
| 16 | GPIO 23       | Servo Ch 3 (PWM via pigpio) | Signal wire |
| 35 | GPIO 19 / 24  | Servo Ch 4 (PWM via pigpio) | Signal wire |
| 37 | GPIO 26       | Servo Ch 5 (PWM via pigpio) | Signal wire |
| 13 | GPIO 27       | Servo Ch 6 (PWM via pigpio) | Signal wire |
| 36 | GPIO 16 / 25  | Servo Ch 7 (PWM via pigpio) | Signal wire |

## Power Isolation Rules

* **CRITICAL**: Never power servos directly from the Raspberry Pi 5V header pins. Servo stall currents cause inductive voltage dips that reboot the Pi Zero 2W or corrupt SD card contents.[^src-20260822-installationguide]
* **Common Ground**: All servo power supplies must share a common ground (GND) connection with the Raspberry Pi.[^src-20260822-installationguide]

## Prerequisites and Software Installation

* Install Raspberry Pi OS Lite (64-bit).[^src-20260822-installationguide]
* Enable I2C and SPI via `raspi-config`.[^src-20260822-installationguide]
* Install and run the `pigpio` daemon (`sudo pigpiod`).[^src-20260822-installationguide]
* Clone repository and run automated installation:[^src-20260822-installationguide] [^src-20261007-2026-10-07-ninjarobot-pi0-migration-audit]
  ```bash
  ./install.sh
  ```

[^src-20260822-installationguide]: NinjaRobotPi0 Installation Guide.
[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.

[^src-20261007-2026-10-07-ninjarobot-pi0-migration-audit]: Initial migration audit.

[^src-20261009-installationguide]: Current versioned Installationguide.

## Implementation evidence and acceptance limits

Host validation and the exact code/tooling boundary are recorded in the approved implementation evidence. Real Pi hardware, live accounts and published curl acceptance remain pending; passing host checks do not imply physical acceptance.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.


## Historical 2026-10-08 audit follow-up (superseded policy)

The following records the earlier implementation; current compatibility policy below supersedes exact-version, codename and private-tool-precedence claims.

The 2026-10-08 full manual documents the corrected guided flow and uses `.venv/bin/ninja_core server` because the installer keeps uv private. Starting the existing server can initialize/center hardware and attempts ngrok. Skipping token setup is not network isolation. Publication and physical/account acceptance remain pending.[^src-20261007-2026-10-08-upgrade-audit]

[^src-20261007-2026-10-08-upgrade-audit]: Pi0 upgrade audit findings and boundaries.


## Historical Trixie support correction (superseded policy)

The following records the earlier implementation; current compatibility policy below supersedes exact-version, codename and private-tool-precedence claims.

The current complete manual accepts Bookworm or Trixie on Zero 2 W / aarch64. Publish the correction before retrying the default-branch curl command. Do not modify os-release or bypass platform checks. Existing checkout users update to the fixed revision and run the local installer.[^src-20261008-2026-10-08-trixie-support]

[^src-20261008-2026-10-08-trixie-support]: Trixie installer correction and validation boundary.


## Historical Installation recovery and diagnostics (superseded policy)

The following records the earlier implementation; current compatibility policy below supersedes exact-version, codename and private-tool-precedence claims.

Missing project Python/CLI means an incomplete or broken environment. Run ./install.sh to install or retry; --check alone installs nothing. The current manual gives exact default-HEAD fast-forward steps for existing/detached checkouts and says to stop on Git errors, then wait for Software installed before checking. New diagnostics require publication before the Pi can fetch them.[^src-20261008-2026-10-08-installer-recovery]

[^src-20261008-2026-10-08-installer-recovery]: Installer diagnostics and recovery validation.


## Current software compatibility policy

The current complete manual documents Node 20.19+ within 20.x or >=22.12.0 from locked Vite engines. Node 24.21.0 qualifies. uv is checked for required sync flags rather than exact version; real uv 0.9.26 passed an offline host locked-sync dry-run. Compatible PATH tools are reused before private fallbacks. Missing .venv/bin/python or ninja_core still requires completing ./install.sh; --check remains read-only.[^src-20261008-2026-10-08-installer-compatibility]

[^src-20261008-2026-10-08-installer-compatibility]: Installer compatibility requirements and validation evidence.

## Built-in movement channel requirements (2026-10-09)

Spider built-in movement import requires all eight BCM GPIO channels 20–27 to be configured and active; missing channels prevent the full trajectory pack from seeding. Wheel and Humanoid profiles require valid configured servo channels for their respective `home` center command. Inspect both `config.json` channel definitions and physical `servo.json` limits before energizing actuators.[^src-20261009-installationguide] [^src-20261009-2026-10-09-builtin-movements]

[^src-20261009-2026-10-09-builtin-movements]: Automatic native built-in movement evidence and architecture boundaries.
## CLI launcher verification and environment branding (2026-10-10)

The current installation manual records the updated virtual environment branding (`ninjarobotpi0` prompt) and launcher verification. The installer verifies all five launcher executables (`ninja_core`, `pi0servo`, `pi0disp`, `pi0buzzer`, `pi0vl53l0x`) in `.venv/bin` after locked provider reinstallation, ensuring wiring calibration tools can be launched independently.[^src-20261010-installationguide-2]

[^src-20261010-installationguide-2]: Current versioned Installationguide (2026-10-10 CLI recovery).
