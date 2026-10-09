---
type: Reference
title: Current installation manual
description: Current installation manual.
status: draft
generated:
  by: agent:codex
  at: '2026-10-07T13:03:34.637721+00:00'
sources:
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
- id: src-20261008-2026-10-08-readme-audit
  title: Pi0 README audit evidence and validation limits
  content_hash: sha256:7a945023f45ad2e179e5cae529665df9ed050bfe5cf36f440f857a02e28cfea4
  resource: urn:llmwiki:source:src-20261008-readme-audit
- id: src-20261009-readme-2
  title: Readme
  content_hash: sha256:21ade3212445744ae9fedb7dde760014b69ad3e8413b6ffb895bd27a820aa61d
  resource: urn:llmwiki:source:src-20261009-readme-2
- id: src-20261009-2026-10-09-builtin-movements
  resource: urn:llmwiki:source:src-20261009-2026-10-09-builtin-movements
  title: 2026 10 09 Builtin Movements
  content_hash: sha256:6bd14ef705bb60c2c228c95940fd6cb771299532f13e10fdc4faae22db3f216a
semantic_review:
  version: 1
  performed_by: agent:antigravity
  performed_at: '2026-10-09T17:10:48.021602+00:00'
  target_hash: sha256:065f07bffca803dd26f1ad6d802502ce3ed661b384a9113772187e089706449b
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed installation manual procedures against install.sh, onboard.sh, and InstallationGuide.md. Automated install, profile seeding on config import, and raised-chassis pre-motion safety rules match current manual.
  - Installer execution does not auto-activate robot hardware. Network access and security setup remain explicit.
---

# Current installation manual

Resolve the complete current InstallationGuide through project-knowledge.json or the wiki README. It covers the Raspberry Pi OS 64-bit compatibility requirements, software installation, explicit onboarding, prerequisites, calibration warnings and recovery. Root InstallationGuide.md is a compatibility pointer. Earlier detailed material is preserved as historical reference, with current installation instructions clearly identified.[^src-20261009-installationguide]

[Project overview](/overview.md).

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


## Multilingual user manual audit

The multilingual README explains that an active pigpiod or ninjarobot service stops installation before dependencies. The initial preflight PASS is not Software installed. Recovery supports the robot, disconnects actuator power, stops the robot service before pigpiod and retries the existing checkout without deleting calibration. After successful installation, pigpiod must be started explicitly; boot enablement is optional. The README uses compatible uv discovery for legacy autostart and corrects ngrok/token, actual hostname, QR and shutdown limitations. Software checks and saved onboarding state do not certify physical results.[^src-20261008-2026-10-08-readme-audit]

[^src-20261008-2026-10-08-readme-audit]: Four-language README correctness audit and code evidence.

The complete public walkthrough is preserved in the current README source.[^src-20261009-readme-2]

[^src-20261009-readme-2]: Pi0 four-language user manual.

## Built-in movement configuration and safety readiness (2026-10-09)

The current installation manual records built-in movement seeding during configuration import. Physical safety requirements specify supporting the robot chassis or raising wheels before testing center or movement commands, verifying external servo power and common ground, and inspecting both `config.json` calibration keys and physical `servo.json` before motion.[^src-20261009-installationguide] [^src-20261009-readme-2] [^src-20261009-2026-10-09-builtin-movements]

[^src-20261009-2026-10-09-builtin-movements]: Automatic native built-in movement evidence and architecture boundaries.
