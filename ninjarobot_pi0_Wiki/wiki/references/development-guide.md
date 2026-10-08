---
type: Reference
title: Current development manual
description: Current development manual.
status: draft
generated:
  by: agent:codex
  at: '2026-10-07T13:03:34.637721+00:00'
sources:
- id: src-20261007-developmentguide-3
  resource: urn:llmwiki:source:src-20261007-developmentguide-3
  title: Pi0 development guide — audit 2026-10-08
  content_hash: sha256:af9d4c121796a7373ef9bb02ca590931d7d88e4a86184f870c780c0e067d77d1
- id: src-20261007-2026-10-07-install-onboard-wiki-ui-2
  resource: urn:llmwiki:source:src-20261007-2026-10-07-install-onboard-wiki-ui-2
  title: Pi0 upgrade implementation and current UI contracts
  content_hash: sha256:1545ea683947c315a9ea0d4c30258c228e975a78e39062b2e045669fcff0cb9c
- id: src-20261007-2026-10-08-upgrade-audit
  resource: urn:llmwiki:source:src-20261007-2026-10-08-upgrade-audit
  title: Pi0 upgrade audit findings and boundaries
  content_hash: sha256:7112a6575c6288875e3fdad33679f094b22908e0ee729b29f5dfbfc55f48de64
semantic_review:
  version: 1
  performed_by: agent:codex
  performed_at: '2026-10-07T17:39:58.353039+00:00'
  target_hash: sha256:9f762add3c6905966f1864f03290478e4893b8b7771629101d9603db8d6c637c
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - New current manual maps additive audit fixes, README role and environment isolation
    to current code. Historical full guide retained. Human/device verification remains
    absent.
  - Source-grounded AI review of changed claims and retained cited context; draft/unverified.
    Physical tests, live accounts and publication remain pending.
---

# Current development manual

Resolve the complete current DevelopmentGuide through project-knowledge.json or the wiki README. It documents protected core/driver functions, additive onboarding, UI contract preservation, immutable source versions and host/wiki validation. Root DevelopmentGuide.md is a compatibility pointer; earlier detailed API/history material is preserved as historical context.[^src-20261007-developmentguide-3]

[Project overview](/overview.md).

[^src-20261007-developmentguide-3]: Current versioned Developmentguide.

## Implementation evidence and acceptance limits

Host validation and the exact code/tooling boundary are recorded in the approved implementation evidence. Real Pi hardware, live accounts and published curl acceptance remain pending; passing host checks do not imply physical acceptance.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.


## 2026-10-08 audit follow-up

The current manual reflects the audit regressions and README publication role. Explicit wiki setup clears UV_PROJECT and can discover installer-owned private uv; read-only commands still never install dependencies. Core/driver behavior is protected and physical acceptance remains separate.[^src-20261007-2026-10-08-upgrade-audit]

[^src-20261007-2026-10-08-upgrade-audit]: Pi0 upgrade audit findings and boundaries.
