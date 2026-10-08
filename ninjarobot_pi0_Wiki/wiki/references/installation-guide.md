---
type: Reference
title: Current installation manual
description: Current installation manual.
status: draft
generated:
  by: agent:codex
  at: '2026-10-07T13:03:34.637721+00:00'
sources:
- id: src-20261008-installationguide
  resource: urn:llmwiki:source:src-20261008-installationguide
  title: 'Pi0 installation: Bookworm and Trixie'
  content_hash: sha256:2b1dad2fba1ea44f8f380b636658e4aae8aa87961076d23610cbafa1eb00c45e
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
semantic_review:
  version: 1
  performed_by: agent:codex
  performed_at: '2026-10-08T00:53:48.937611+00:00'
  target_hash: sha256:3f3b426efcdb7fdc0d53d3ae10c729871cd72e777baf46faf5ac7201729186c9
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Checked the current full manual and Trixie correction evidence against the narrow
    release-gate diff and interpreter tests. Prior unrelated claims retain their cited
    sources. Both Bookworm and Trixie are allowed on Zero 2 W/aarch64; physical Trixie
    acceptance and publication of this fix are pending.
  - Source-grounded AI review of changed claims and retained cited context; draft/unverified.
    Physical tests, live accounts and publication remain pending.
---

# Current installation manual

Resolve the complete current InstallationGuide through project-knowledge.json or the wiki README. It covers the Bookworm/Trixie 64-bit targets, software installation, explicit onboarding, prerequisites, calibration warnings and recovery. Root InstallationGuide.md is a compatibility pointer. Earlier detailed material is preserved as historical reference, with current installation instructions clearly identified.[^src-20261008-installationguide]

[Project overview](/overview.md).

[^src-20261008-installationguide]: Current versioned Installationguide.

## Implementation evidence and acceptance limits

Host validation and the exact code/tooling boundary are recorded in the approved implementation evidence. Real Pi hardware, live accounts and published curl acceptance remain pending; passing host checks do not imply physical acceptance.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.


## 2026-10-08 audit follow-up

The 2026-10-08 full manual documents the corrected guided flow and uses `.venv/bin/ninja_core server` because the installer keeps uv private. Starting the existing server can initialize/center hardware and attempts ngrok. Skipping token setup is not network isolation. Publication and physical/account acceptance remain pending.[^src-20261007-2026-10-08-upgrade-audit]

[^src-20261007-2026-10-08-upgrade-audit]: Pi0 upgrade audit findings and boundaries.


## Trixie support correction

The current complete manual accepts Bookworm or Trixie on Zero 2 W / aarch64. Publish the correction before retrying the default-branch curl command. Do not modify os-release or bypass platform checks. Existing checkout users update to the fixed revision and run the local installer.[^src-20261008-2026-10-08-trixie-support]

[^src-20261008-2026-10-08-trixie-support]: Trixie installer correction and validation boundary.
