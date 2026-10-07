---
type: Entity
title: pi0disp Package
description: Thread-safe SPI display driver for ST7789V LCDs with smart delta rendering
  and multilingual text tickers.
status: draft
generated:
  by: codex/migration-audit
  at: '2026-10-07T07:13:37.354382+00:00'
sources:
- id: src-20260822-readme-6
  resource: urn:llmwiki:source:src-20260822-readme-6
  title: pi0disp Readme
  content_hash: sha256:ccc2a3f07c0591dfe2c1828c8e01365b1820b386a68ad30a751959a9f5bb3ba2
- id: src-20260822-developmentguide
  resource: urn:llmwiki:source:src-20260822-developmentguide
  title: NinjaRobotPi0 Development Guide
  content_hash: sha256:d1f8e19627223cb320b2e05df9a141c768ca0f418a7f77d160b6127d08c439e9
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
---

# pi0disp Package

`pi0disp` is a thread-safe SPI driver for ST7789V-based 2.0" and 2.8" IPS LCD displays (240×320 resolution).[^src-20260822-readme-6] [^src-20260822-developmentguide]

## Core Features

* **Smart Delta Rendering**: Computes bounding boxes of modified pixels via `RegionOptimizer` and `PIL.ImageChops.difference()`, transmitting only dirty regions; the source documentation reports approximately 90% bandwidth savings for face animations.[^src-20260822-readme-6]
* **Thread-Safe SPI Locking**: All SPI bus transactions are guarded by `threading.Lock()` for concurrent safety across web and animation threads.[^src-20260822-readme-6]
* **PWM Backlight Control**: Smooth brightness adjustment (0–100%) via hardware/software PWM.[^src-20260822-readme-6]
* **TextTicker**: Scrolling marquee text with bundled multilingual Noto fonts (English, Japanese, Traditional Chinese).[^src-20260822-readme-6]

## Key Classes & Modules

* **`ST7789V` (`pi0disp.core.driver`)**: Main driver class implementing `Actuator` ABC.[^src-20260822-readme-6]
* **`ColorConverter` (`pi0disp.core.renderer`)**: Fast RGB to RGB565 conversion using numpy lookup tables (LUT).[^src-20260822-readme-6]
* **`RegionOptimizer` (`pi0disp.core.renderer`)**: Dirty region bounding box calculation and merging.[^src-20260822-readme-6]
* **`ConfigManager` (`pi0disp.config.config_manager`)**: Manages `display.json` settings.[^src-20260822-readme-6]

## CLI Commands

* `uv run pi0disp init`: Interactive setup wizard for GPIO pins (DC, RST, BLK) and display profile.[^src-20260822-readme-6]
* `uv run pi0disp image <path>`: Displays an image file (auto-resized).[^src-20260822-readme-6]
* `uv run pi0disp text "<text>" [--scroll] [--lang ja|zh-tw|en]`: Displays static or scrolling text.[^src-20260822-readme-6]
* `uv run pi0disp display-tool`: Launches the 9-option interactive test menu.[^src-20260822-readme-6]

[^src-20260822-readme-6]: pi0disp Readme.
[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.
