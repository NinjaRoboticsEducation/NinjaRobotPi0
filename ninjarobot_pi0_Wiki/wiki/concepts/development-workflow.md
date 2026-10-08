---
type: Concept
title: Development and immutable documentation workflow
description: Development and immutable documentation workflow.
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
  performed_at: '2026-10-07T17:39:59.317071+00:00'
  target_hash: sha256:12ee6744b728b3639ab81050ff335068f915273d65b704a0a36e4a6502cb97ca
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Root manual pointers, public README, immutable sources and explicit wiki setup
    match agent policy/launcher. Private uv fallback is setup-only; no read command
    gains installation side effects.
  - Source-grounded AI review of changed claims and retained cited context; draft/unverified.
    Physical tests, live accounts and publication remain pending.
---

# Development and immutable documentation workflow

Read the current wiki/manual map and verify important claims against code before development. Create a new dated full manual version instead of replacing registered sources. Register/normalize explicitly, validate/show a schema-v2 page diff, apply within owner-approved scope, and review changed sourced pages. Update current pointers and implementation classifications after review; do not refresh fingerprints merely to silence errors. Wiki setup/prepare is explicit; queries and checks do not install dependencies.[^src-20261007-developmentguide-3]

[Project overview](/overview.md).

[^src-20261007-developmentguide-3]: Current versioned Developmentguide.

## Implementation evidence and acceptance limits

Host validation and the exact code/tooling boundary are recorded in the approved implementation evidence. Real Pi hardware, live accounts and published curl acceptance remain pending; passing host checks do not imply physical acceptance.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.


## 2026-10-08 audit follow-up

The root README is now the owner-requested comprehensive public introduction and quick-start manual with clearly labelled non-English summaries. The three root manual files remain compatibility pointers to immutable versions. Explicit wiki setup clears inherited project redirection and can use private installer uv. Registered old sources remain immutable.[^src-20261007-2026-10-08-upgrade-audit]

[^src-20261007-2026-10-08-upgrade-audit]: Pi0 upgrade audit findings and boundaries.
