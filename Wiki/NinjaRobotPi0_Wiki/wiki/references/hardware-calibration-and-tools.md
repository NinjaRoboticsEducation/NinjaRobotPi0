---
type: Reference
title: Hardware Calibration and Testing Tools Reference
description: Comprehensive guide to interactive calibration TUIs, setup wizards, and
  diagnostic tools.
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
- id: src-20260822-readme-7
  resource: urn:llmwiki:source:src-20260822-readme-7
  title: pi0servo Readme
  content_hash: sha256:23793729576aa0b8f5b460d7fe4e47ab1d7ad4f9a6af4348bf4c8208a6610a76
- id: src-20260822-readme-6
  resource: urn:llmwiki:source:src-20260822-readme-6
  title: pi0disp Readme
  content_hash: sha256:ccc2a3f07c0591dfe2c1828c8e01365b1820b386a68ad30a751959a9f5bb3ba2
- id: src-20260822-readme-5
  resource: urn:llmwiki:source:src-20260822-readme-5
  title: pi0buzzer Readme
  content_hash: sha256:2d45a1426b50788922f073ae4e8236e7e16e63c22c329fce016c782ce7b127fa
- id: src-20260822-readme-8
  resource: urn:llmwiki:source:src-20260822-readme-8
  title: pi0vl53l0x Readme
  content_hash: sha256:ddf100f609e7335b81dc3803c453c3d0dc66fbe0c20a52917d90407bc1d2f35e
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
---

# Hardware Calibration and Testing Tools Reference

The documented NinjaRobotPi0 hardware subsystems provide interactive terminal tools (TUIs) for calibration, verification, or diagnostics without requiring custom scripts.[^src-20260822-installationguide] [^src-20260822-developmentguide]

## Guided System Setup (`uv run ninja_core init-tool`)

The `init-tool` provides a guided top-level menu for end-to-end setup:[^src-20260822-developmentguide]
1. Set the Google Gemini API key and select a model after catalog discovery and a bounded generation check.[^src-20260822-developmentguide]
2. Set ngrok authtoken for remote access.[^src-20260822-developmentguide]
3. Configure custom Bluetooth robot name.[^src-20260822-developmentguide]
4. Select robot type (`tire`, `humanoid`, `spider`).[^src-20260822-developmentguide]
5. Import subsystem hardware configurations.[^src-20260822-developmentguide]
6. Launch web and BLE server.[^src-20260822-developmentguide]

Gemini model validation can take up to 60 seconds for a thinking model. Discovery, validation, or cancellation failures leave the previous Gemini configuration unchanged.[^src-20260822-developmentguide]

## Servo Calibration (`uv run pi0servo servo-tool`)

> [!IMPORTANT]
> Uncalibrated servos will not move. Calibration is required to establish safe pulse width limits.[^src-20260822-readme-7]

* **Menu Option 3 (Calibrate)**:
  * `Tab` / `Shift+Tab`: Cycle between Min (-90°), Center (0°), and Max (+90°) positions.[^src-20260822-readme-7]
  * `Up` / `Down`: Coarse pulse adjustment (±20µs).[^src-20260822-readme-7]
  * `w` / `s`: Fine pulse adjustment (±1µs).[^src-20260822-readme-7]
  * `+` / `-`: Adjust servo maximum speed limit.[^src-20260822-readme-7]
  * `Enter`: Save calibration to `servo.json`.[^src-20260822-readme-7]

## Motion Recording (`uv run ninja_core movement-tool`)

* **Option 2 (Record new movement)**: Interactively create multi-servo postures (e.g. `20:45/21:-30`), preview transitions, and save named movements to `config.json`.[^src-20260822-developmentguide]

## Display Setup & Testing (`uv run pi0disp init` & `display-tool`)

* **`uv run pi0disp init`**: Guided wizard configuring DC, RST, BLK pins, rotation (0/90/180/270°), and brightness.[^src-20260822-readme-6]
* **`uv run pi0disp display-tool`**: 9-option interactive test menu (image rendering, multilingual marquee text, bouncing ball animation, backlight test).[^src-20260822-readme-6]

## Buzzer Initialization & Piano (`uv run pi0buzzer buzzer-tool`)

* **`uv run pi0buzzer init 17`**: Configures pin 17 and performs verification beep.[^src-20260822-readme-5]
* **`uv run pi0buzzer buzzer-tool`**: Menu offering emotion playback, melody demo, volume setting, and real-time keyboard piano mode.[^src-20260822-readme-5]

## Distance Sensor Calibration (`uv run pi0vl53l0x sensor-tool`)

* **Guided Offset Calibration**: Place a flat white target at exactly 100mm from the sensor and run `uv run pi0vl53l0x calibrate --distance 100` to compute and save the zero offset in `vl53l0x.json`.[^src-20260822-readme-8]

[^src-20260822-installationguide]: NinjaRobotPi0 Installation Guide.
[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.
[^src-20260822-readme-7]: pi0servo Readme.
[^src-20260822-readme-6]: pi0disp Readme.
[^src-20260822-readme-5]: pi0buzzer Readme.
[^src-20260822-readme-8]: pi0vl53l0x Readme.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.
