---
type: Concept
title: Perception and Expression Systems
description: Time-of-Flight distance sensing, thread-safe measurement locks, animated
  LCD expressions, and emotion audio synthesis.
status: draft
generated:
  by: codex/migration-audit
  at: '2026-10-07T07:13:37.354382+00:00'
sources:
- id: src-20260822-readme-5
  resource: urn:llmwiki:source:src-20260822-readme-5
  title: pi0buzzer Readme
  content_hash: sha256:2d45a1426b50788922f073ae4e8236e7e16e63c22c329fce016c782ce7b127fa
- id: src-20260822-readme-6
  resource: urn:llmwiki:source:src-20260822-readme-6
  title: pi0disp Readme
  content_hash: sha256:ccc2a3f07c0591dfe2c1828c8e01365b1820b386a68ad30a751959a9f5bb3ba2
- id: src-20260822-readme-8
  resource: urn:llmwiki:source:src-20260822-readme-8
  title: pi0vl53l0x Readme
  content_hash: sha256:ddf100f609e7335b81dc3803c453c3d0dc66fbe0c20a52917d90407bc1d2f35e
- id: src-20260822-developmentguide
  resource: urn:llmwiki:source:src-20260822-developmentguide
  title: NinjaRobotPi0 Development Guide
  content_hash: sha256:d1f8e19627223cb320b2e05df9a141c768ca0f418a7f77d160b6127d08c439e9
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
---

# Perception and Expression Systems

NinjaRobotPi0 combines environmental perception with multi-modal expressions (visual and acoustic) to deliver an engaging, interactive personality.[^src-20260822-developmentguide]

## Distance Perception (`pi0vl53l0x` & `DistanceMonitor`)

Distance sensing uses the VL53L0X Time-of-Flight sensor over I2C:[^src-20260822-readme-8]

* **Transaction-Level Locking**: Ranging requires multi-register read/write sequences. `pi0vl53l0x` wraps transactions in a `threading.RLock` so background polling in `DistanceMonitor` and user code in Blockly (`robot.distance.read()`) do not corrupt I2C bus state.[^src-20260822-readme-8] [^src-20260822-developmentguide]
* **Automatic Bus Recovery**: Transient I2C communication failures trigger exponential backoff (10→20→50ms) and automatic bus reset.[^src-20260822-readme-8]
* **Obstacle Safety**: In autonomous mode, proximity < 50mm immediately halts movements, displays a `scary` face, and triggers a warning sound.[^src-20260822-developmentguide]

## Visual Expressions (`pi0disp` & `AnimatedFaces`)

The visual expression engine renders expressive eyes and faces onto the 240×320 IPS display:[^src-20260822-readme-6] [^src-20260822-developmentguide]

* **Smart Delta Rendering**: `pi0disp` calculates bounding boxes of modified pixels via `PIL.ImageChops.difference()`, transmitting only changed areas over SPI; the source documentation reports approximately 90% bandwidth reduction for animations.[^src-20260822-readme-6]
* **Thread-Safe SPI Lock**: Protects display transfers against concurrent access by web server status threads and facial animation loops.[^src-20260822-readme-6]
* **Expression Library**: Pre-rendered and dynamic animations including `happy`, `sad`, `angry`, `confusing`, `cry`, `embarrassing`, `idle`, `laughing`, `scary`, `shy`, `sleepy`, `speaking`, and `surprising`.[^src-20260822-readme-6] [^src-20260822-developmentguide]

## Acoustic Emotion Synthesis (`pi0buzzer`)

Audio is generated using a passive buzzer driven by hardware PWM on GPIO 17:[^src-20260822-readme-5]

* **Non-Blocking Queue Worker**: Sound sequences are processed in a dedicated background worker thread, keeping queued playback work off the calling thread.[^src-20260822-readme-5]
* **Musical Notes**: 35 standard note frequencies across 5 octaves (C3–B7).[^src-20260822-readme-5]
* **14 Emotion Sound Effects**: Acoustic signatures mapped to matching facial expressions.[^src-20260822-readme-5]
* **Built-in Song Catalog**: Melodies including `happy_birthday`, `jingle_bells`, `twinkle_twinkle_little_star`, and `head_shoulders_knees_and_toes`.[^src-20260822-developmentguide]

[^src-20260822-readme-5]: pi0buzzer Readme.
[^src-20260822-readme-6]: pi0disp Readme.
[^src-20260822-readme-8]: pi0vl53l0x Readme.
[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.
