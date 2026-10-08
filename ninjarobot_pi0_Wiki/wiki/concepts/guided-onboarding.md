---
type: Concept
title: Guided Pi0 onboarding
description: Guided Pi0 onboarding.
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
- id: src-20261008-2026-10-08-installer-compatibility
  resource: urn:llmwiki:source:src-20261008-2026-10-08-installer-compatibility
  title: 2026 10 08 Installer Compatibility
  content_hash: sha256:7eaa21e7a1f79122e25e10dc37ae91a488aebe3ccff9db5e6c7b59db0684928f
semantic_review:
  version: 1
  performed_by: agent:codex
  performed_at: '2026-10-08T05:58:15.313130+00:00'
  target_hash: sha256:bafcd585854d7fa9b597ca14e4b5c0127918874519f62b03226f07001e76c596
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

# Guided Pi0 onboarding

The local ./onboard.sh entry point guides existing Pi0 interactive tools, saved configuration review/import, identity, Gemini key/model, and ngrok token. Tools can activate devices immediately; servo-tool can center saved servos before its menu. Reuse is software validation rather than physical acceptance. Progress is private and contains no credentials. Network-dependent setup can be deferred. Server, boot startup and reboot are later deliberate actions.[^src-20261008-installationguide-3]

[Project overview](/overview.md).

[^src-20261008-installationguide-3]: Current versioned Installationguide.

## Implementation evidence and acceptance limits

Host validation and the exact code/tooling boundary are recorded in the approved implementation evidence. Real Pi hardware, live accounts and published curl acceptance remain pending; passing host checks do not imply physical acceptance.[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]

[^src-20261007-2026-10-07-install-onboard-wiki-ui-2]: Pi0 upgrade implementation and current UI contracts.


## Historical 2026-10-08 audit follow-up (superseded policy)

The following records the earlier implementation; current compatibility policy below supersedes exact-version, codename and private-tool-precedence claims.

The terminal now follows Pi5 welcome, numbered What/Why/What-to-do guidance, bulk or per-module reuse, retry-in-place, Enter to continue and a readable summary. Resume skips only unchanged valid completed hardware. Changed settings invalidate operator observations, including in read-only status. Invalid saved progress is rejected without overwriting it. Credential workers use private permissions from first write and pass platform checks. Conflicting servo aliases and invalid numeric GPIO keys cannot bypass the import gate. Server startup remains manual.[^src-20261007-2026-10-08-upgrade-audit]

[^src-20261007-2026-10-08-upgrade-audit]: Pi0 upgrade audit findings and boundaries.


## Historical Trixie support correction (superseded policy)

The following records the earlier implementation; current compatibility policy below supersedes exact-version, codename and private-tool-precedence claims.

The shared platform preflight now accepts Bookworm/Trixie 64-bit on Zero 2 W, so Trixie users are not blocked again after bootstrap. Step order, permissions, validation, hardware confirmation and manual server start are unchanged.[^src-20261008-2026-10-08-trixie-support]

[^src-20261008-2026-10-08-trixie-support]: Trixie installer correction and validation boundary.


## Current software compatibility policy

Onboarding inherits the same codename-independent preflight as the installer and surfaces the actual prerequisite errors. Zero 2 W/aarch64, Debian-family OS, normal-user execution and Python 3.10+ remain required. Step order, hardware readiness confirmations, calibration tools and robot behavior are unchanged.[^src-20261008-2026-10-08-installer-compatibility]

[^src-20261008-2026-10-08-installer-compatibility]: Installer compatibility requirements and validation evidence.
