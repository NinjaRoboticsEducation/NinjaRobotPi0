---
type: Concept
title: Guided Pi0 onboarding
description: Guided Pi0 onboarding.
status: draft
generated:
  by: agent:codex
  at: '2026-10-07T13:03:34.637721+00:00'
sources:
- id: src-20261007-installationguide-3
  resource: urn:llmwiki:source:src-20261007-installationguide-3
  title: Pi0 installation and onboarding — audit 2026-10-08
  content_hash: sha256:45ef29b63b279aa880cd4858de3e1150be12291f5c2b758219d63847268d1b5b
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
  performed_at: '2026-10-07T17:39:54.317631+00:00'
  target_hash: sha256:50e71b3eb8e2bd23469ed7b0f58e660a4158201c9b3de3c3dd3c8f52a2370f34
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Compared the corrected flow with Pi5 setup_wizard and current Pi0 orchestration.
    Retry/reuse/resume and invalidation are supported; saved configuration is not
    physical acceptance. No launch feature is implied.
  - Source-grounded AI review of changed claims and retained cited context; draft/unverified.
    Physical tests, live accounts and publication remain pending.
---

# Guided Pi0 onboarding

The local ./onboard.sh entry point guides existing Pi0 interactive tools, saved configuration review/import, identity, Gemini key/model, and ngrok token. Tools can activate devices immediately; servo-tool can center saved servos before its menu. Reuse is software validation rather than physical acceptance. Progress is private and contains no credentials. Network-dependent setup can be deferred. Server, boot startup and reboot are later deliberate actions.[^src-20261007-installationguide-3]

[Project overview](/overview.md).

[^src-20261007-installationguide-3]: Current versioned Installationguide.

## Implementation evidence and acceptance limits

Host validation and the exact code/tooling boundary are recorded in the approved implementation evidence. Real Pi hardware, live accounts and published curl acceptance remain pending; passing host checks do not imply physical acceptance.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.


## 2026-10-08 audit follow-up

The terminal now follows Pi5 welcome, numbered What/Why/What-to-do guidance, bulk or per-module reuse, retry-in-place, Enter to continue and a readable summary. Resume skips only unchanged valid completed hardware. Changed settings invalidate operator observations, including in read-only status. Invalid saved progress is rejected without overwriting it. Credential workers use private permissions from first write and pass platform checks. Conflicting servo aliases and invalid numeric GPIO keys cannot bypass the import gate. Server startup remains manual.[^src-20261007-2026-10-08-upgrade-audit]

[^src-20261007-2026-10-08-upgrade-audit]: Pi0 upgrade audit findings and boundaries.
