---
type: Concept
title: Development and immutable documentation workflow
description: Development and immutable documentation workflow.
status: draft
generated:
  by: agent:codex
  at: '2026-10-07T13:03:34.637721+00:00'
sources:
- id: src-20261009-developmentguide-2
  resource: urn:llmwiki:source:src-20261009-developmentguide-2
  title: Developmentguide
  content_hash: sha256:80ef9c89176a6b0a3749f9127697464f197c2972bf2a41ae533fa2cb7afdc0ab
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
- id: src-20261009-2026-10-09-spider-otto
  resource: urn:llmwiki:source:src-20261009-2026-10-09-spider-otto
  title: 2026 10 09 Spider Otto
  content_hash: sha256:1c35301cb86c71126d626d841c5f648680fb82c8fe857526e22b983e970939cd
- id: src-20261009-2026-10-09-builtin-movements
  resource: urn:llmwiki:source:src-20261009-2026-10-09-builtin-movements
  title: 2026 10 09 Builtin Movements
  content_hash: sha256:6bd14ef705bb60c2c228c95940fd6cb771299532f13e10fdc4faae22db3f216a
semantic_review:
  version: 1
  performed_by: agent:antigravity
  performed_at: '2026-10-09T17:10:48.021602+00:00'
  target_hash: sha256:d4cf42c98a875ea70b7d2763e5194ffc6df6a6cbd83725bde736558d5412dc57
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed development workflow against scripts/wiki.py, project-knowledge.json, and CI workflows. Immutable manual lifecycle, schema-v2 plans, and isolated testing match documented practice.
  - Host test execution does not imply remote deployment or physical acceptance.
---

# Development and immutable documentation workflow

Development follows an immutable manual lifecycle. Full current manuals live only as versioned sources under `raw/` and resolve through project-knowledge.json; root files are compatibility navigation pointers only.[^src-20261009-developmentguide-2]

Registered raw originals are immutable. Do not overwrite them; create a new complete dated version, preserve previous versions, register and normalize new evidence, and update cited pages through an approved change plan.[^src-20261009-developmentguide-2]

[Project overview](/overview.md).

[^src-20261009-developmentguide-2]: Current versioned Developmentguide.

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

The current compatibility policy uses actual Node engine requirements, the Python minimum and required uv sync capabilities rather than exact version or OS-codename gates. The registered compatibility record includes an offline uv 0.9.26 dry-run and initial host regressions; it does not establish physical Pi acceptance. Core and dependency locks remain protected.[^src-20261008-2026-10-08-installer-compatibility]

[^src-20261008-2026-10-08-installer-compatibility]: Installer compatibility requirements and validation evidence.


## Spider OTTO movement data and future timing design (2026-10-09)

An opt-in repository JSON pack adds 19 entries covering 16 source methods and selected variants, with 565 waypoint steps and no existing controller/driver changes. The offline generator, actual config/executor tests and two design documents explain corrected GPIO mapping, native speed modes and lost period/dwell fidelity. Seventy-one targeted host tests, generator verification, Ruff and core protection passed; physical validation remains pending. See [Spider OTTO waypoint library](/concepts/spider-otto-waypoint-library.md) for current behavior and the separate, unimplemented timed-controller proposal.[^src-20261009-2026-10-09-spider-otto]

[^src-20261009-2026-10-09-spider-otto]: Registered Spider implementation, code inspection, host validation and proposal boundaries.

## Built-in movements development workflow (2026-10-09)

The current development workflow records native built-in movement integration using packaged resources, inert Raspberry Pi Zero 2 W automated tests, and strict separation between software verification and physical hardware acceptance. The full development manual is versioned in `raw/` and resolved via project knowledge.[^src-20261009-developmentguide-2] [^src-20261009-2026-10-09-builtin-movements]

[^src-20261009-2026-10-09-builtin-movements]: Automatic native built-in movement evidence and architecture boundaries.
