---
type: Reference
title: Current installation manual
description: Current installation manual.
status: draft
generated:
  by: agent:codex
  at: '2026-10-07T13:03:34.637721+00:00'
sources:
- id: src-20261008-installationguide-3
  resource: urn:llmwiki:source:src-20261008-installationguide-3
  title: Installationguide
  content_hash: sha256:734051f87ce7f447ae50bee7863118612f55b5747cd42e3cb047662a5408081f
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
- id: src-20261008-2026-10-08-installer-recovery
  resource: urn:llmwiki:source:src-20261008-2026-10-08-installer-recovery
  title: Installer diagnostics and recovery validation
  content_hash: sha256:416eea41c04d6dc6ed633fa695b276a48574d22eacb21db5131de3577dbe4fc3
- id: src-20261008-2026-10-08-installer-compatibility
  resource: urn:llmwiki:source:src-20261008-2026-10-08-installer-compatibility
  title: 2026 10 08 Installer Compatibility
  content_hash: sha256:7eaa21e7a1f79122e25e10dc37ae91a488aebe3ccff9db5e6c7b59db0684928f
semantic_review:
  version: 1
  performed_by: agent:codex
  performed_at: '2026-10-08T05:58:11.230446+00:00'
  target_hash: sha256:1698b560eb8c5df38e899372944717d11a840a3744f2e31666ebee0e0e1bc946
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed the current compatibility manual and recorded uv 0.9.26 dry-run against
    the installer/checker, locked Vite engines and 205 passing host regressions on
    Python 3.11 and 3.13. Exact Node/uv equality and codename rules are superseded
    explicitly; device/user requirements, real Node/Python minima, read-only inspection
    and missing-environment failures remain. Compatible tool reuse and checksum fallback
    are distinct. Retained hardware/history claims keep their prior sources; no physical
    or human verification is inferred.
  - Source-grounded AI review of changed claims and retained cited context; draft/unverified.
    Physical tests, live accounts and publication remain pending.
---

# Current installation manual

Resolve the complete current InstallationGuide through project-knowledge.json or the wiki README. It covers the Raspberry Pi OS 64-bit compatibility requirements, software installation, explicit onboarding, prerequisites, calibration warnings and recovery. Root InstallationGuide.md is a compatibility pointer. Earlier detailed material is preserved as historical reference, with current installation instructions clearly identified.[^src-20261008-installationguide-3]

[Project overview](/overview.md).

[^src-20261008-installationguide-3]: Current versioned Installationguide.

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
