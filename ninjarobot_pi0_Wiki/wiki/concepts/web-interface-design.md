---
type: Concept
title: Pi0 web interface design and compatibility
description: Pi0 web interface design and compatibility.
status: draft
generated:
  by: agent:codex
  at: '2026-10-07T13:03:34.637721+00:00'
sources:
- id: src-20261007-developmentguide-2
  resource: urn:llmwiki:source:src-20261007-developmentguide-2
  title: Developmentguide
  content_hash: sha256:6851b89fb0bf25cf5be3be6f445b8169802b8889809724e81116c9d3b30856d4
- id: src-20261007-2026-10-07-install-onboard-wiki-ui-2
  resource: urn:llmwiki:source:src-20261007-2026-10-07-install-onboard-wiki-ui-2
  title: Pi0 upgrade implementation and current UI contracts
  content_hash: sha256:1545ea683947c315a9ea0d4c30258c228e975a78e39062b2e045669fcff0cb9c
semantic_review:
  version: 1
  performed_by: agent:codex
  performed_at: '2026-10-07T13:11:41.096764+00:00'
  target_hash: sha256:75e4f4d312bcdcfae2eda11de92fd0a4b23f3437a55a49ca18aa526300b97eb0
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Presentation claims match source CSS/JSX and inspected built renders. Inert fixture
    coverage establishes host compatibility only; Pi5-only features are excluded.
  - Source-grounded AI review; lifecycle stays draft/unverified. This is not human
    or hardware verification.
---

# Pi0 web interface design and compatibility

Pi0 retains its React routes and control contracts while adopting Pi5 navy/cyan styling, bordered rounded panels, a menu sheet and an activity drawer. Home, Agent and Help use the same palette. Existing expressions/sounds/movements, chat, browser speech input and distance events remain Pi0 capabilities. The UI adds no Pi5 camera, gamepad, voice service or controller ownership protocol. Automated browser checks use inert API/socket fixtures; they do not establish physical-device acceptance.[^src-20261007-developmentguide-2]

[Project overview](/overview.md).

[^src-20261007-developmentguide-2]: Current versioned Developmentguide.

## Implementation evidence and acceptance limits

Host validation and the exact code/tooling boundary are recorded in the approved implementation evidence. Real Pi hardware, live accounts and published curl acceptance remain pending; passing host checks do not imply physical acceptance.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.
