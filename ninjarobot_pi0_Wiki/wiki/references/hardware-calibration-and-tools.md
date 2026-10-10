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
- id: src-20261007-installationguide-3
  resource: urn:llmwiki:source:src-20261007-installationguide-3
  title: Pi0 installation and onboarding — audit 2026-10-08
  content_hash: sha256:45ef29b63b279aa880cd4858de3e1150be12291f5c2b758219d63847268d1b5b
- id: src-20261007-2026-10-07-install-onboard-wiki-ui-2
  resource: urn:llmwiki:source:src-20261007-2026-10-07-install-onboard-wiki-ui-2
  title: Pi0 upgrade implementation and current UI contracts
  content_hash: sha256:1545ea683947c315a9ea0d4c30258c228e975a78e39062b2e045669fcff0cb9c
- id: src-20261007-2026-10-08-upgrade-audit
  resource: urn:llmwiki:source:src-20261007-2026-10-08-upgrade-audit
  title: Pi0 upgrade audit findings and boundaries
  content_hash: sha256:7112a6575c6288875e3fdad33679f094b22908e0ee729b29f5dfbfc55f48de64
- id: src-20261010-lifecyclerefinementsimplementationplan
  resource: urn:llmwiki:source:src-20261010-lifecyclerefinementsimplementationplan
  title: Lifecyclerefinementsimplementationplan
  content_hash: sha256:5d4be31936118493340340291e66a59c7f76886f26e791ca0963721aab9f21a8
- id: src-20261010-lifecyclerefinementsevidence
  resource: urn:llmwiki:source:src-20261010-lifecyclerefinementsevidence
  title: Lifecyclerefinementsevidence
  content_hash: sha256:c34468e740adccacc6546a2afe39fd41562eed229ae5795255577b044d4fd09e
- id: src-20261010-installationguide-3
  resource: urn:llmwiki:source:src-20261010-installationguide-3
  title: Installationguide
  content_hash: sha256:116e93e529583e57b2f300536c8a2367030727c584a83a1a826cd5a53b0d4001
- id: src-20261010-modeladapterimplementation
  resource: urn:llmwiki:source:src-20261010-modeladapterimplementation
  title: Modeladapterimplementation
  content_hash: sha256:2c6480a2595936057adf1550e8860044d7269be1b6a860a1395d893ec7a78895
semantic_review:
  version: 1
  performed_by: agent:antigravity
  performed_at: '2026-10-10T15:28:47.571035+00:00'
  target_hash: sha256:76335ab22373367193edee3afb1e164b4be47eb77a38384f1d46a4f8cd817010
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed calibration tools against init_tool.py option 1 (Select AI model) and
    provider_setup.py. Terminal-only probe validation without hardware actuation matches
    implementation.
  - Physical servo clearance and external power remain required before running motor
    calibration.
---

# Hardware Calibration and Testing Tools Reference

## Guided calibration boundary

`./onboard.sh` provides selected display, buzzer, servo and distance tools, reuse/status/resume, and existing Gemini/ngrok settings. It checks saved configuration after tool exit; a zero exit status or file presence is insufficient. Servo calibration must exist before hardware import, avoiding the core default fallback. Sensor offset stays in its package-local configuration, outside core import-all. Operator observation and software validation are recorded separately.[^src-20261007-installationguide-3]


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
> Do not assume missing calibration prevents motion. Existing core fallback and standalone-tool initialization can move/center servos. Support the robot and clear travel before opening a tool. Onboarding requires valid ordered saved pulses for reuse/import; this is software validation, not physical certification.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

* **Menu Option 3 (Calibrate)**:
  * `Tab` / `Shift+Tab`: Cycle between Min (-90°), Center (0°), and Max (+90°) positions.[^src-20260822-readme-7]
  * `Up` / `Down`: Coarse pulse adjustment (±20µs).[^src-20260822-readme-7]
  * `w` / `s`: Fine pulse adjustment (±1µs).[^src-20260822-readme-7]
  * `+` / `-`: Adjust servo maximum speed limit.[^src-20260822-readme-7]
  * `Enter`: Save calibration to `servo.json`.[^src-20260822-readme-7]

## Motion Recording (`uv run ninja_core movement-tool`)

* **Option 2 (Record new movement)**: Interactively create multi-servo postures (e.g. `20:45/21:-30`), preview transitions, and save named movements to `config.json`.[^src-20260822-developmentguide]
* **Option 6 (Deliberate exit)**: Executes configured `Poweroff` (for Spider) or `home` (for Wheel and Humanoid) before HAL shutdown and saving configuration, releasing PWM without subsequent centering.[^src-20261010-lifecyclerefinementsimplementationplan] [^src-20261010-lifecyclerefinementsevidence]

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

[^src-20261007-installationguide-3]: Current versioned Installationguide.

## Implementation evidence and acceptance limits

Host validation and the exact code/tooling boundary are recorded in the approved implementation evidence. Real Pi hardware, live accounts and published curl acceptance remain pending; passing host checks do not imply physical acceptance.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.


## 2026-10-08 audit follow-up

Onboarding validates every numeric servo key and rejects conflicting pulse aliases that the unchanged core importer would otherwise prefer. Its fingerprint covers the exact validated bytes. Resume revalidates current files; changed settings invalidate previous physical observations. Failed tools offer retry or save/exit. This is software validation, not proof of correct physical limits or wiring.[^src-20261007-2026-10-08-upgrade-audit]

[^src-20261007-2026-10-08-upgrade-audit]: Pi0 upgrade audit findings and boundaries.
## Deliberate exit motion and power release (2026-10-10)

Movement-tool option 6 commands configured `Poweroff` once before HAL shutdown and configuration save, with no subsequent centering. HAL releases PWM rather than electrically holding the position. For Spider robots, verify physical clearance for ±90° targets before selecting option 6.[^src-20261010-lifecyclerefinementsimplementationplan] [^src-20261010-lifecyclerefinementsevidence]

[^src-20261010-lifecyclerefinementsimplementationplan]: Lifecycle refinements implementation plan.
[^src-20261010-lifecyclerefinementsevidence]: Lifecycle refinements implementation evidence.

## AI Model Selection in Initial Configuration Tool (2026-10-10)

In `uv run ninja_core init-tool`, option 1 is updated to **Select AI model** (supporting Google, OpenAI, Anthropic, and Ollama Cloud).[^src-20261010-installationguide-3] [^src-20261010-modeladapterimplementation] Model discovery, input, and verification probe execute in the terminal without energizing robot servos, playing audio, or launching the robot web server.[^src-20261010-installationguide-3] [^src-20261010-modeladapterimplementation]

[^src-20261010-installationguide-3]: Current versioned Installationguide (2026-10-10 model adapter release).
[^src-20261010-modeladapterimplementation]: Pi0 Cloud Model Provider Adapter implementation evidence.
