---
type: Reference
title: Installation and Hardware Wiring Reference
description: Step-by-step assembly, complete GPIO wiring tables, Raspberry Pi OS Bookworm
  setup, and pigpio compilation.
status: draft
generated:
  by: codex/repository-migration
  at: '2026-10-07T07:00:29.384460+00:00'
sources:
- id: src-20260822-installationguide
  resource: urn:llmwiki:source:src-20260822-installationguide
  title: NinjaRobotPi0 Installation Guide
  content_hash: sha256:8fe90ec3883948bfa196dc62202ee4c22181f706b5797c17eb6f0374f8994adf
- id: src-20260822-developmentguide
  resource: urn:llmwiki:source:src-20260822-developmentguide
  title: NinjaRobotPi0 Development Guide
  content_hash: sha256:43e40f7c8db5734b4e8fe2ffd7d1e9c365cf9ceaad16fb4dbbbbe8eb1be71e7c
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
---

# Installation and Hardware Wiring Reference

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

## Raspberry Pi OS (Bookworm 64-bit) & `pigpio` Setup

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

## Workspace Installation

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
