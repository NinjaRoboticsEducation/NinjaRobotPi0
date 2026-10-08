---
type: Reference
title: Current development manual
description: Current development manual.
status: draft
generated:
  by: agent:codex
  at: '2026-10-07T13:03:34.637721+00:00'
sources:
- id: src-20261008-developmentguide-3
  resource: urn:llmwiki:source:src-20261008-developmentguide-3
  title: Developmentguide
  content_hash: sha256:0fc10ebdf50056c8d26521e3251d265cf5b2a764c98b9b1c13f2204310385178
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
  performed_at: '2026-10-08T05:58:13.337368+00:00'
  target_hash: sha256:4d2d190f7570b360468c8f32886f769774d69fc4835d3e0884707a96571deb85
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

# Current development manual

Resolve the complete current DevelopmentGuide through project-knowledge.json or the wiki README. It documents protected core/driver functions, additive onboarding, UI contract preservation, immutable source versions and host/wiki validation. Root DevelopmentGuide.md is a compatibility pointer; earlier detailed API/history material is preserved as historical context.[^src-20261008-developmentguide-3]

[Project overview](/overview.md).

[^src-20261008-developmentguide-3]: Current versioned Developmentguide.

## Implementation evidence and acceptance limits

Host validation and the exact code/tooling boundary are recorded in the approved implementation evidence. Real Pi hardware, live accounts and published curl acceptance remain pending; passing host checks do not imply physical acceptance.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.


## Historical 2026-10-08 audit follow-up (superseded policy)

The following records the earlier implementation; current compatibility policy below supersedes exact-version, codename and private-tool-precedence claims.

The current manual reflects the audit regressions and README publication role. Explicit wiki setup clears UV_PROJECT and can discover installer-owned private uv; read-only commands still never install dependencies. Core/driver behavior is protected and physical acceptance remains separate.[^src-20261007-2026-10-08-upgrade-audit]

[^src-20261007-2026-10-08-upgrade-audit]: Pi0 upgrade audit findings and boundaries.


## Historical Trixie support correction (superseded policy)

The following records the earlier implementation; current compatibility policy below supersedes exact-version, codename and private-tool-precedence claims.

The current complete development manual adds the Bookworm/Trixie target matrix and Python 3.11/3.13 CI. Keep shell and Python release rejection tests consistent. Locked host tests do not certify Debian arm64 installation or physical operation.[^src-20261008-2026-10-08-trixie-support]

[^src-20261008-2026-10-08-trixie-support]: Trixie installer correction and validation boundary.


## Historical Installation recovery and diagnostics (superseded policy)

The following records the earlier implementation; current compatibility policy below supersedes exact-version, codename and private-tool-precedence claims.

The new complete manual records read-only diagnostic tests and failure-stage recovery. Inert fixtures inject checksum and Python-sync failures, retain nonzero status, assert lock cleanup and calibration preservation, and prevent later npm work. Core/runtime behavior remains unchanged.[^src-20261008-2026-10-08-installer-recovery]

[^src-20261008-2026-10-08-installer-recovery]: Installer diagnostics and recovery validation.


## Current software compatibility policy

Regression tests cover the Node engine boundaries and the reported Node 24.21.0 / uv 0.9.26, missing uv sync flags, PATH preference over incompatible private tools, OS codenames without an allowlist, and Python 3.10 minimum. Inert installation fixtures still cover hash rejection, sync failure exit/cleanup, reruns and calibration retention. No core or dependency lock change is required.[^src-20261008-2026-10-08-installer-compatibility]

[^src-20261008-2026-10-08-installer-compatibility]: Installer compatibility requirements and validation evidence.
