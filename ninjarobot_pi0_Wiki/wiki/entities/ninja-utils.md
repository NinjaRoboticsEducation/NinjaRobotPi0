---
type: Entity
title: ninja_utils Package
description: Shared utilities package containing Abstract Base Classes, centralized
  logging, and systemd service managers.
status: draft
generated:
  by: codex/migration-audit
  at: '2026-10-07T07:13:37.354382+00:00'
sources:
- id: src-20260822-readme-4
  resource: urn:llmwiki:source:src-20260822-readme-4
  title: ninja_utils Readme
  content_hash: sha256:67508fde5377631a44c87d1c9c207da2c86f09531ab3d9e5d229af985e999d05
- id: src-20260822-developmentguide
  resource: urn:llmwiki:source:src-20260822-developmentguide
  title: NinjaRobotPi0 Development Guide
  content_hash: sha256:d1f8e19627223cb320b2e05df9a141c768ca0f418a7f77d160b6127d08c439e9
- id: src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  resource: urn:llmwiki:source:src-20261007-2026-10-07-ninjarobot-pi0-repository-migration
  title: 2026 10 07 Ninjarobot Pi0 Repository Migration
  content_hash: sha256:2651e2d6d359620e3f5f2b1080132a84c74321b4a018c92d672ffe9d420573aa
- id: src-20261008-2026-10-08-readme-audit
  title: Pi0 README audit evidence and validation limits
  content_hash: sha256:7a945023f45ad2e179e5cae529665df9ed050bfe5cf36f440f857a02e28cfea4
  resource: urn:llmwiki:source:src-20261008-2026-10-08-readme-audit
semantic_review:
  version: 1
  performed_by: agent:codex
  performed_at: '2026-10-08T14:34:38.939183+00:00'
  target_hash: sha256:f537243f57ee7b88adef3bfe0410dc902d1d3605f29ab6bfde246d0e18309c23
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed the owner-authored four-language README and registered audit evidence
    against installer preflight, service-manager uv/PATH and enable behavior, ngrok
    presence/connection checks, core movement parser, GPIO terminology and shutdown
    permission/animation limits. Corrections retain the manual structure; optional
    recovery/status details remain in Troubleshooting/Appendix C. All 54 shell examples
    parse and four isolated core parser examples pass. No runtime code or physical
    hardware operation is claimed. Earlier historical sources remain cited; draft/unverified
    status is preserved.
  - Source-grounded AI review of changed claims and retained cited context; draft/unverified.
    Physical tests, live accounts and publication remain pending.
---

# ninja_utils Package

`ninja_utils` provides shared foundation utilities and interface contracts across all NinjaRobotPi0 packages.[^src-20260822-readme-4] [^src-20260822-developmentguide]

## Module Summary

* **`interfaces.py`**: Defines the `Actuator` and `Sensor` Abstract Base Classes (ABCs) and the `DistanceData` dataclass.[^src-20260822-readme-4] [^src-20260822-developmentguide]
* **`my_logger.py`**: Centralized, formatted logging system for console and file output.[^src-20260822-readme-4]
* **`keyboard.py`**: Non-blocking single-keypress terminal input helper for interactive TUIs.[^src-20260822-readme-4]
* **`service_manager.py`**: Manages Linux systemd service configuration for autostarting the robot on boot.[^src-20260822-developmentguide]

## Legacy uv-based CLI examples

* `uv run ninja_utils install-startup`: Installs and enables the `ninjarobot.service` systemd unit.[^src-20260822-readme-4]
* `uv run ninja_utils remove-startup`: Disables and removes the autostart service.[^src-20260822-readme-4]
* `uv run ninja_utils status-startup`: Checks the status of the systemd service.[^src-20260822-readme-4]

[^src-20260822-readme-4]: ninja_utils Readme.
[^src-20260822-developmentguide]: NinjaRobotPi0 Development Guide.

## Repository migration (2026-10-07)

The former NinjaRobotV5 repository is now NinjaRobotPi0 at [NinjaRoboticsEducation/NinjaRobotPi0](https://github.com/NinjaRoboticsEducation/NinjaRobotPi0). The local folder is `NinjaRobotPi0/`. The new repository starts with fresh history on `main`; Python packages and robot runtime behavior are retained. Manual links use `blob/HEAD` to follow the GitHub default branch. Historical names and audit findings remain provenance; this migration does not resolve them.[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]

[^src-20261007-2026-10-07-ninjarobot-pi0-repository-migration]: Registered evidence for the approved 2026-10-07 repository migration.


## Multilingual user manual audit

For an installed checkout, the README uses .venv/bin/ninja_utils for install-startup, status-startup and remove-startup. The install command selects a compatible uv with scripts/install_check.py --find-tool uv and scopes PATH for the helper, which records its absolute uv path. The helper validates config.json, running pigpiod, ninja_core import and uv; it installs/enables ninjarobot.service but does not start it immediately. The generated service still runs uv run ninja_core server --autostart and can sync dependencies at boot. These are documentation corrections to existing behavior, not service-manager changes.[^src-20261008-2026-10-08-readme-audit]

[^src-20261008-2026-10-08-readme-audit]: Four-language README correctness audit and code evidence.
