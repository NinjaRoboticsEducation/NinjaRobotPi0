---
type: Concept
title: Humanoid Otto movement reference and native catalog integration
description: Complete Humanoid waypoint library, native built-in catalog integration,
  and validation boundaries.
status: draft
generated:
  by: agent:codex
  at: '2026-10-12T00:43:10.742914+00:00'
sources:
- id: src-20261012-humanoidmovementreferenceevidence
  resource: urn:llmwiki:source:src-20261012-humanoidmovementreferenceevidence
  title: Humanoidmovementreferenceevidence
  content_hash: sha256:7925e73616d27f362c88bf902aa43e5bccfb09cbfc550b2692c3c5df079db9e1
- id: src-20261012-developmentlog
  resource: urn:llmwiki:source:src-20261012-developmentlog
  title: Developmentlog
  content_hash: sha256:43c971abf2590fbea4b1c75a0e387338aa21c95f8aecbb5894afc2b70ae05804
- id: src-20261012-humanoidreferencelinkvalidation
  resource: urn:llmwiki:source:src-20261012-humanoidreferencelinkvalidation
  title: Humanoidreferencelinkvalidation
  content_hash: sha256:f103c92694c27838b136c7836156a88520a6e14654e9b8c8613f77118d722c41
- id: src-20261012-humanoidbuiltinmovementsevidence
  resource: urn:llmwiki:source:src-20261012-humanoidbuiltinmovementsevidence
  title: Humanoid built-in movements implementation evidence
  content_hash: sha256:95c750e66ffcc4577a463531569d3d000845fe1b32d612e5ce2f09bf89003f4c
- id: src-20261012-developmentlog-2
  resource: urn:llmwiki:source:src-20261012-developmentlog-2
  title: Humanoid built-in movements development log
  content_hash: sha256:73de870ccfd7a010dec09e97fe68c4c5b24929d14043d3e7e6b57410f2df519e
- id: src-20261012-developmentguide
  resource: urn:llmwiki:source:src-20261012-developmentguide
  title: Humanoid built-in movements development guide
  content_hash: sha256:0d1ea579a0cf0a798defd67eef35d1830227e52bac179927956e162fae8f0f2a
- id: src-20261012-installationguide
  resource: urn:llmwiki:source:src-20261012-installationguide
  title: Humanoid built-in movements installation guide
  content_hash: sha256:30b40b3338f5e9b912b63cb4146f3fa369a13b3d6848869efbce8ebf3f7eed19
semantic_review:
  version: 1
  performed_by: agent:antigravity
  performed_at: '2026-10-12T02:44:00+00:00'
  target_hash: sha256:a11e709f30e77dc34d991edc15765d6e298374c0388e724974d527407b01f13a
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed Humanoid native catalog integration against src-20261012-humanoidbuiltinmovementsevidence,
    DevelopmentLog.md, DevelopmentGuide.md, and InstallationGuide.md.
  - Catalog packaging (35 defaults / 1,204 steps with GPIO 20–27), deterministic extraction,
    and host validation verified without asserting physical Pi hardware acceptance.
---

# Humanoid Otto movement reference and native catalog integration

`DevelopmentPlanDoc/HumanoidBuildinMovements.md` contains 34 complete JSON sequences (1,203 keyframes): 24 variants covering all 16 public Otto servo motion methods and 10 servo-containing gestures.[^src-20261012-humanoidmovementreferenceevidence] Following the reference deliverable, the library has been packaged as an installed package resource in `ninja_core/data/humanoid_otto.json` and integrated into native built-in movements.[^src-20261012-humanoidbuiltinmovementsevidence] [^src-20261012-developmentlog-2] Full Humanoid profiles with all BCM GPIO 20–27 configured receive all 34 `humanoid_*` sequences plus generic `home` (35 defaults / 1,204 steps), while partial profiles keep only generic `home`.[^src-20261012-humanoidbuiltinmovementsevidence]

## Native built-in movement integration and CLI configuration

Configuration import (`ninja_core config import` or alias `import-all`) automatically seeds native Humanoid movements when the robot profile is set via `ninja_core config set-type humanoid`.[^src-20261012-installationguide] Seeding requires all GPIO 20–27 present in core servo-calibration keys.[^src-20261012-installationguide] Reimport preserves custom collisions and user edits through fingerprint-based provenance, updating only unchanged managed defaults.[^src-20261012-humanoidbuiltinmovementsevidence]

`scripts/build_humanoid_movements.py` extracts standalone library-marker JSON blocks from the reference, verifying exact installed-resource parity against canonical inner-object hash `49f6c4fe998b3c8500347f56eeeb7e165fb442c206ac373485310af7d280d2d6` via `--check`.[^src-20261012-developmentguide] Shared `validate_movement` recognizes known non-neutral Humanoid trajectories even after renaming or speed edits, normalizing string and integer GPIO keys, while excluding all-neutral center geometry from Humanoid inference.[^src-20261012-developmentguide]

CLI movement-tool option 4, the web Movement dropdown (which returns HTTP 422 on stale/incompatible requests), and Ninja Agent share profile-aware discovery and preflight guards.[^src-20261012-installationguide]

## Mapping and execution limits

Source YL/YR/RL/RR/LA/RA map to BCM GPIO20/21/22/23/26/27, subtracting 90 from logical source angles. GPIO24/25 are additional shoulders and remain at nominal 0, pending measured neutral and fore/aft direction. Older display wiring examples conflict with these channels; check the actual GPIO20–27 inventory before enabling hardware.[^src-20261012-humanoidmovementreferenceevidence]

The reference uses only `moves`, `speed` and optional `per_servo_speeds`, at S mode. Fixed source targets and sampled oscillator geometry are expanded into explicit waypoints: 36 intervals per cycle with endpoints. Each new oscillator subcall starts at mathematical phase zero. Timing, pauses, audio/display and servo detach are unsupported by this schema and are not reproduced. VICTORY's first-ramp YL9 is explicitly adapted to 90; MAGIC and WAVE-animation have no servo trajectory; FAIL is omitted because release/collapse/recovery cannot be represented faithfully.[^src-20261012-humanoidmovementreferenceevidence]

## Use and validation boundary

The document explains existing configuration registration and triggering, and provides a collision-refusing offline preview script. It does not replace live config or create managed native hashes. Names require Humanoid scope and all eight active GPIO channels. Physical endpoint clearance and direction are unverified; source walk/turn arms reach signed ±90. Commission small individual movements before any complete gait.[^src-20261012-humanoidmovementreferenceevidence]

Host checks passed actual configuration save/load, native preflight and controller execution with an inert driver for every step. Negative checks cover 272 missing-channel cases, 68 incompatible-profile cases, invalid later steps before output and driver abort. All 36 JSON blocks parse, the 34 library blocks equal the validated pack, local links resolve, and the preview script preserves existing config while refusing collisions/overwrite. Independent reader review found no actionable issue. No physical acceptance, live hardware or automatic installation is claimed.[^src-20261012-humanoidmovementreferenceevidence]

The new complete DevelopmentLog version records this documentation deliverable. Installation and runtime behavior are unchanged, so existing InstallationGuide and DevelopmentGuide versions remain current. Pre-existing unrelated knowledge-map fingerprints and the missing historical Spider source link remain unresolved.[^src-20261012-developmentlog]

See [native Spider integration](/concepts/spider-otto-waypoint-library.md) for the installed Spider catalog and [motion system](/concepts/motion-system-and-easing.md) for existing waypoint semantics.

[^src-20261012-humanoidmovementreferenceevidence]: Humanoid reference code inspection, exact JSON validation and remaining physical limits, 2026-10-12.
[^src-20261012-developmentlog]: Complete immutable DevelopmentLog with the Humanoid reference milestone.

The Otto research files are referenced by their explicit sibling-workspace directory and filenames so the Pi0 document contains no cross-repository Markdown links. The final artifact hash is recorded separately; all movement JSON and its canonical fingerprint remain unchanged.[^src-20261012-humanoidreferencelinkvalidation]

[^src-20261012-humanoidreferencelinkvalidation]: Final reference link portability and artifact-integrity record.
[^src-20261012-humanoidbuiltinmovementsevidence]: Humanoid built-in movement implementation evidence, exact hashes, and host validation, 2026-10-12.
[^src-20261012-developmentlog-2]: Complete immutable DevelopmentLog with the Humanoid native built-in movements release.
[^src-20261012-developmentguide]: Current versioned DevelopmentGuide with Humanoid native movement integration and validation details.
[^src-20261012-installationguide]: Current versioned InstallationGuide with Humanoid configuration import and channel wiring guidance.
