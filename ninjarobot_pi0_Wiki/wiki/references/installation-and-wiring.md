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
- id: src-20261008-installationguide-3
  resource: urn:llmwiki:source:src-20261008-installationguide-3
  title: Installationguide
  content_hash: sha256:734051f87ce7f447ae50bee7863118612f55b5747cd42e3cb047662a5408081f
- id: src-20261007-2026-10-07-install-onboard-wiki-ui-2
  resource: urn:llmwiki:source:src-20261007-2026-10-07-install-onboard-wiki-ui-2
  title: Pi0 upgrade implementation and current UI contracts
  content_hash: sha256:1545ea683947c315a9ea0d4c30258c228e975a78e39062b2e045669fcff0cb9c
- id: src-20261007-2026-10-08-upgrade-audit
  resource: urn:llmwiki:source:src-20261007-2026-10-08-upgrade-audit
  title: Pi0 upgrade audit findings and boundaries
  content_hash: sha256:7112a6575c6288875e3fdad33679f094b22908e0ee729b29f5dfbfc55f48de64
- id: src-20261008-2026-10-08-trixie-support
  resource: urn:llmwiki:source:src-20261008-2026-10-08-trixie-support
  title: Trixie installer correction and validation boundary
  content_hash: sha256:3aae04cfab13e782c5748e8ca26721d860d0d842ac18c5544fd8ae0f82dc2945
- id: src-20261008-2026-10-08-installer-recovery
  resource: urn:llmwiki:source:src-20261008-2026-10-08-installer-recovery
  title: Installer diagnostics and recovery validation
  content_hash: sha256:416eea41c04d6dc6ed633fa695b276a48574d22eacb21db5131de3577dbe4fc3
- id: src-20261008-2026-10-08-installer-compatibility
  resource: urn:llmwiki:source:src-20261008-2026-10-08-installer-compatibility
  title: 2026 10 08 Installer Compatibility
  content_hash: sha256:7eaa21e7a1f79122e25e10dc37ae91a488aebe3ccff9db5e6c7b59db0684928f
semantic_review:
  version: 1
  performed_by: agent:codex
  performed_at: '2026-10-08T05:58:12.277510+00:00'
  target_hash: sha256:574e4c44daa58e991751a181fb42d958578749ba11ce89ec96ad19c71958309e
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed the current compatibility manual and recorded uv 0.9.26 dry-run against
    the installer/checker, locked Vite engines and 205 passing host regressions on
    Python 3.11 and 3.13. Exact Node/uv equality and codename rules are superseded
    explicitly; device/user requirements, real Node/Python minima, read-only inspection
    and missing-environment failures remain. Compatible tool reuse and checksum fallback
    are distinct. Retained hardware/history claims keep their prior sources; no physical
    or human verification is inferred.
  - Source-grounded AI review of changed claims and retained cited context; draft/unverified.
    Physical tests, live accounts and publication remain pending.
---

# Installation and Hardware Wiring Reference

## Current installer and onboarding

Use the current complete InstallationGuide linked by the wiki README. It replaces historical floating downloads and global-pip installation commands. The verified installer uses locked Python/frontend dependencies and verified fallback tool inputs. It does not activate hardware/services or start the robot. Onboarding opens a selected existing tool only after readiness confirmation; opening the servo tool can center calibrated servos immediately.[^src-20261008-installationguide-3]


This reference summarizes hardware requirements, pinout connections, and operating system setup for NinjaRobotPi0 on the Raspberry Pi Zero 2W.[^src-20260822-installationguide] [^src-20260822-developmentguide]

## Hardware Requirements

* **Raspberry Pi Zero 2W** (with 40-pin header soldered).[^src-20260822-installationguide]
* **MicroSD Card** (16GB+ Class 10).[^src-20260822-installationguide]
* **8× SG90 / MG90S Micro Servos** (5V).[^src-20260822-installationguide]
* **External 5V 3A+ Power Supply** for servos.[^src-20260822-installationguide]
* **ST7789V 2.0" / 2.8" IPS LCD Display** (240×320, SPI).[^src-20260822-installationguide]
* **VL53L0X Time-of-Flight Distance Sensor** (I2C).[^src-20260822-installationguide]
* **Passive Buzzer** (3–5V, GPIO 17).[^src-20260822-installationguide]

## Complete Pinout Connection Table

| Subsystem | Component Pin | Raspberry Pi Pin | Pin Description |
|-----------|---------------|------------------|-----------------|
| **Power (Logic)** | Sensor/Display VCC | Pin 1 (3.3V) | 3.3V Logic Supply [^src-20260822-installationguide] |
| **Ground** | All Component GND | Pin 6 / 9 / 14 / 20 / 25 / 30 / 34 / 39 | Common Ground [^src-20260822-installationguide] |
| **VL53L0X** | SDA | Pin 3 (GPIO 2) | I2C Data [^src-20260822-installationguide] |
| **VL53L0X** | SCL | Pin 5 (GPIO 3) | I2C Clock [^src-20260822-installationguide] |
| **ST7789V** | DIN (MOSI) | Pin 19 (SPI0 MOSI) | SPI Data [^src-20260822-installationguide] |
| **ST7789V** | CLK (SCLK) | Pin 23 (SPI0 SCLK) | SPI Clock [^src-20260822-installationguide] |
| **ST7789V** | CS | Pin 24 (SPI0 CE0) | Chip Select [^src-20260822-installationguide] |
| **ST7789V** | DC | Pin 8 (GPIO 14) | Data/Command (configurable) [^src-20260822-installationguide] |
| **ST7789V** | RST | Pin 10 (GPIO 15) | Reset (configurable) [^src-20260822-installationguide] |
| **ST7789V** | BLK | Pin 36 (GPIO 16) | Backlight PWM (configurable) [^src-20260822-installationguide] |
| **Buzzer** | Signal (+) | Pin 11 (GPIO 17) | Hardware PWM [^src-20260822-installationguide] |
| **Servos 1–8**| Signals 1–8 | Pins 38, 40, 15, 16, 18, 22, 37, 13 (GPIO 20–27) | PWM Signal Channels [^src-20260822-installationguide] |

## Historical manual pigpio setup (superseded)

On Raspberry Pi OS Bookworm, `pigpio` must be compiled from source due to upstream repository package changes:[^src-20260822-installationguide]

```bash
# 1. Install build tools
sudo apt update && sudo apt install -y build-essential unzip wget git python3-pip

# 2. Download and compile C library
wget https://github.com/joan2937/pigpio/archive/master.zip
unzip master.zip && cd pigpio-master
make && sudo make install

# 3. Update library cache
sudo ldconfig

# 4. Install Python wrapper
sudo apt install python3-pigpio || sudo pip3 install pigpio --break-system-packages

# 5. Enable and start daemon
sudo systemctl enable pigpiod
sudo systemctl start pigpiod
```

## Historical workspace installation (superseded)

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repository and install dependencies
git clone https://github.com/NinjaRoboticsEducation/NinjaRobotPi0.git
cd NinjaRobotPi0
uv sync

# Build web application frontend
cd ninja_webapp && npm install && npm run build && cd ..
```

[^src-20260822-installationguide]: NinjaRobotPi0 Installation Guide.
[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.


## Historical migration audit follow-up (2026-10-07)

Current repository documentation uses NinjaRobotPi0; historical audits and V5 version milestones retain their original identity. Robot runtime code and package names are unchanged. After a clean clone, prepare the embedded wiki with the normalization bootstrap in `NinjaRobotPi0/Wiki/NinjaRobotPi0_Wiki/README.md` before lint: its derived manifests are intentionally untracked. The tested bootstrap regenerates these through the existing CLI and restores zero-error normal lint. Website manuals use `blob/HEAD` and clone commands omit branch selection.[^src-20261007-2026-10-07-ninjarobot-pi0-migration-audit]

[^src-20261007-2026-10-07-ninjarobot-pi0-migration-audit]: Audit evidence covering documentation attribution, current naming, default-branch links, and clean-clone wiki normalization.

[^src-20261008-installationguide-3]: Current versioned Installationguide.

## Implementation evidence and acceptance limits

Host validation and the exact code/tooling boundary are recorded in the approved implementation evidence. Real Pi hardware, live accounts and published curl acceptance remain pending; passing host checks do not imply physical acceptance.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.


## Historical 2026-10-08 audit follow-up (superseded policy)

The following records the earlier implementation; current compatibility policy below supersedes exact-version, codename and private-tool-precedence claims.

Installer preflight now rejects redirected tool/environment paths before privileged changes. Read-only version matching is exact and installation-record publication cleans temporary files on failure. The README provides the current beginner walkthrough; old floating/global-pip commands remain historical. Hardware and network activation occur later through explicit tools/server start.[^src-20261007-2026-10-08-upgrade-audit]

[^src-20261007-2026-10-08-upgrade-audit]: Pi0 upgrade audit findings and boundaries.


## Historical Trixie support correction (superseded policy)

The following records the earlier implementation; current compatibility policy below supersedes exact-version, codename and private-tool-precedence claims.

The current release gate accepts Bookworm and Trixie. Other releases, architectures, devices and root execution remain rejected. System Python is selected explicitly by the existing installer: 3.11 on Bookworm, 3.13 on Trixie. No tool pins, dependency locks or GPIO behavior changed. Host tests are not real Pi qualification.[^src-20261008-2026-10-08-trixie-support]

[^src-20261008-2026-10-08-trixie-support]: Trixie installer correction and validation boundary.


## Historical Installation recovery and diagnostics (superseded policy)

The following records the earlier implementation; current compatibility policy below supersedes exact-version, codename and private-tool-precedence claims.

Version diagnostics now include required/detected versions and executable paths, with timeout/exec failures handled as errors. The installer installs its private tools ahead of system tools; do not remove system Node/uv to satisfy the checker. Missing .venv components are installation failures, not wiring or calibration results.[^src-20261008-2026-10-08-installer-recovery]

[^src-20261008-2026-10-08-installer-recovery]: Installer diagnostics and recovery validation.


## Current software compatibility policy

Exact Node/uv version equality and OS codename allowlists have been removed. Device/architecture/distribution/user and genuine Python/Node requirements remain. Compatible existing tools are reused; checksum-verified downloads are fallbacks, not mandatory installed versions. pigpio qualification and wiring remain unchanged. Host capability checks do not certify hardware or every future OS/tool release.[^src-20261008-2026-10-08-installer-compatibility]

[^src-20261008-2026-10-08-installer-compatibility]: Installer compatibility requirements and validation evidence.
