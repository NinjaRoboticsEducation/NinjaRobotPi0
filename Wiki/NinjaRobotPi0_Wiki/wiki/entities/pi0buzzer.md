---
type: Entity
title: pi0buzzer Package
description: Non-blocking passive buzzer driver with musical notes, 14 emotion sound
  signatures, and keyboard piano.
status: draft
generated:
  by: codex/migration-audit
  at: '2026-10-07T07:13:37.354382+00:00'
sources:
- id: src-20260822-readme-5
  resource: urn:llmwiki:source:src-20260822-readme-5
  title: pi0buzzer Readme
  content_hash: sha256:2d45a1426b50788922f073ae4e8236e7e16e63c22c329fce016c782ce7b127fa
- id: src-20260822-developmentguide
  resource: urn:llmwiki:source:src-20260822-developmentguide
  title: NinjaRobotPi0 Development Guide
  content_hash: sha256:d1f8e19627223cb320b2e05df9a141c768ca0f418a7f77d160b6127d08c439e9
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
---

# pi0buzzer Package

`pi0buzzer` is a non-blocking passive buzzer driver for Raspberry Pi, generating tones, musical notes, emotion sound signatures, and complete melodies.[^src-20260822-readme-5] [^src-20260822-developmentguide]

## Core Features

* **Non-Blocking Architecture**: Sound playback commands are placed into a thread-safe queue processed by a background worker thread, so queued playback does not run on the calling thread.[^src-20260822-readme-5]
* **Musical Scale**: 35 predefined note frequencies across 5 octaves (C3–B7).[^src-20260822-readme-5]
* **14 Emotion Sounds**: Acoustic signatures for `happy`, `sad`, `exciting`, `angry`, `confusing`, `cry`, `embarrassing`, `idle`, `laughing`, `scary`, `shy`, `sleepy`, `speaking`, and `surprising`.[^src-20260822-readme-5]
* **Built-in Melodies**: `happy_birthday`, `jingle_bells`, `twinkle_twinkle_little_star`, and `head_shoulders_knees_and_toes`.[^src-20260822-developmentguide]
* **Volume Control**: PWM duty cycle scaling (0–255).[^src-20260822-readme-5]

## Key Classes & Modules

* **`Buzzer` (`pi0buzzer.core.driver`)**: Base queue worker class implementing `Actuator` ABC.[^src-20260822-readme-5]
* **`MusicBuzzer` (`pi0buzzer.core.music`)**: High-level music, note, and emotion player.[^src-20260822-readme-5]
* **`notes.py`**: Central repository for frequencies, emotion sequences, and piano key mappings.[^src-20260822-readme-5]

## CLI Commands

* `uv run pi0buzzer init <pin>`: Sets the GPIO pin and verifies connection with a test beep.[^src-20260822-readme-5]
* `uv run pi0buzzer beep [freq] [dur]`: Plays a single tone (default: 440Hz, 0.5s).[^src-20260822-readme-5]
* `uv run pi0buzzer play <emotion>`: Plays an emotion sound effect.[^src-20260822-readme-5]
* `uv run pi0buzzer buzzer-tool`: Interactive menu including real-time keyboard piano mode.[^src-20260822-readme-5]

[^src-20260822-readme-5]: pi0buzzer Readme.
[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.
