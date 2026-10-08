---
type: Concept
title: Development and immutable documentation workflow
description: Development and immutable documentation workflow.
status: draft
generated:
  by: agent:codex
  at: '2026-10-07T13:03:34.637721+00:00'
sources:
- id: src-20261008-developmentguide
  resource: urn:llmwiki:source:src-20261008-developmentguide
  title: 'Pi0 development: dual Python target'
  content_hash: sha256:2cbe76f7887674f3c4974297f9f1ef85e9ecd3b4d88eeea802abc04c669d41d1
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
  performed_at: '2026-10-08T00:53:53.204074+00:00'
  target_hash: sha256:8154b4eb48313c04a00cc58a30b2bb54c13196e4df4b384fa19e900bf5206e2a
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

# Development and immutable documentation workflow

Read the current wiki/manual map and verify important claims against code before development. Create a new dated full manual version instead of replacing registered sources. Register/normalize explicitly, validate/show a schema-v2 page diff, apply within owner-approved scope, and review changed sourced pages. Update current pointers and implementation classifications after review; do not refresh fingerprints merely to silence errors. Wiki setup/prepare is explicit; queries and checks do not install dependencies.[^src-20261008-developmentguide]

[Project overview](/overview.md).

[^src-20261008-developmentguide]: Current versioned Developmentguide.

## Implementation evidence and acceptance limits

Host validation and the exact code/tooling boundary are recorded in the approved implementation evidence. Real Pi hardware, live accounts and published curl acceptance remain pending; passing host checks do not imply physical acceptance.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.


## 2026-10-08 audit follow-up

The root README is now the owner-requested comprehensive public introduction and quick-start manual with clearly labelled non-English summaries. The three root manual files remain compatibility pointers to immutable versions. Explicit wiki setup clears inherited project redirection and can use private installer uv. Registered old sources remain immutable.[^src-20261007-2026-10-08-upgrade-audit]

[^src-20261007-2026-10-08-upgrade-audit]: Pi0 upgrade audit findings and boundaries.


## Trixie support correction

CI is configured for Python 3.11 and 3.13 to cover the Bookworm/Trixie interpreter difference. Unknown OS releases remain rejected; no blanket unsupported-platform override was added. Current README/manual versions supersede the original Bookworm-only requirement.[^src-20261008-2026-10-08-trixie-support]

[^src-20261008-2026-10-08-trixie-support]: Trixie installer correction and validation boundary.
