---
type: Reference
title: Current development manual
description: Current development manual.
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
- id: src-20261010-developmentguide-2
  resource: urn:llmwiki:source:src-20261010-developmentguide-2
  title: Developmentguide
  content_hash: sha256:a79a71113f70fb1e6b443cd73b9cd688c8f7889ebf4a9df97b521cb3b76e3127
- id: src-20261010-developmentguide
  resource: urn:llmwiki:source:src-20261010-developmentguide
  title: Developmentguide
  content_hash: sha256:caf3424992bc5934f04c3fd466e034a5ba2ae9e7bef283abfb5811404ce35cef
- id: src-20261010-clientrypointrepairevidence
  resource: urn:llmwiki:source:src-20261010-clientrypointrepairevidence
  title: Clientrypointrepairevidence
  content_hash: sha256:d0dfc89a29e9fc2b1c02f5a2809c90578e21a92b93c80cb881210d5bbd9c1c8d
- id: src-20261010-lifecyclerefinementsevidence
  resource: urn:llmwiki:source:src-20261010-lifecyclerefinementsevidence
  title: Lifecyclerefinementsevidence
  content_hash: sha256:c34468e740adccacc6546a2afe39fd41562eed229ae5795255577b044d4fd09e
- id: src-20261010-developmentguide-3
  resource: urn:llmwiki:source:src-20261010-developmentguide-3
  title: Developmentguide
  content_hash: sha256:13c766ddb69a6bee5efcf4d831c47596e6191106c19856a37ff904464c7ac947
- id: src-20261010-ninja-core-readme
  resource: urn:llmwiki:source:src-20261010-ninja-core-readme
  title: Ninja Core Readme
  content_hash: sha256:0f7d702569807c8458e0b879e6a44941960b7acb8ecbf358e453bc5184950795
- id: src-20261010-modeladapterimplementation
  resource: urn:llmwiki:source:src-20261010-modeladapterimplementation
  title: Modeladapterimplementation
  content_hash: sha256:2c6480a2595936057adf1550e8860044d7269be1b6a860a1395d893ec7a78895
- id: src-20261010-modeladaptervalidation
  resource: urn:llmwiki:source:src-20261010-modeladaptervalidation
  title: Modeladaptervalidation
  content_hash: sha256:653ade7e3e622c23f29dad7eedb8417a1ed0da58869859db3eb08c7319905938
semantic_review:
  version: 1
  performed_by: agent:antigravity
  performed_at: '2026-10-10T15:31:43.935978+00:00'
  target_hash: sha256:085477e652f7f188c48c2e9449420e1b1fc4f25ea4ed342f1831b7d923ac578e
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed development guide against test_provider_adapter.py, config.pre-provider.json
    rollback, and 2026-10-10 DevelopmentGuide.md. Inert test fixtures, Python 3.10+
    requirement, and rollback procedures match manual.
  - Software test suites pass on host; physical hardware testing remains pending.
---

# Current development manual

Resolve the complete current DevelopmentGuide through project-knowledge.json or the wiki README. It documents protected core/driver functions, additive onboarding, UI contract preservation, immutable source versions, native built-in movement execution, and host/wiki validation. Root DevelopmentGuide.md is a compatibility pointer; earlier detailed API/history material is preserved as historical context.[^src-20261010-developmentguide-3]

[Project overview](/overview.md).

[^src-20261009-developmentguide-2]: Historical 2026-10-09 versioned Developmentguide.

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

## Native built-in movement execution and configuration reconciliation (2026-10-09)

The current development manual records native built-in movement import, type reconciliation, preflight guards, and controller serialization. Installed package resources provide 20 Spider movements when GPIO 20–27 are configured; Wheel and Humanoid profiles receive `home`. Host validation passed 42 feature tests; physical actuator testing remains pending.[^src-20261009-developmentguide-2] [^src-20261009-2026-10-09-builtin-movements]

[^src-20261009-2026-10-09-builtin-movements]: Automatic native built-in movement evidence and architecture boundaries.
## Lifecycle refinements and reconnect screen (2026-10-10)

Movement-tool deliberate exit (option 6) validates and executes configured `Poweroff` before releasing hardware, without subsequent centering. When `Poweroff` is absent (Wheel/Humanoid), configured `home` is executed. HAL shutdown releases PWM rather than electrically holding the final pose.
The web interface adds a single-browser session ownership contract: the shared layout maintains a persistent `/ws/session` socket and an opaque HttpOnly `ninja_web_session` cookie across Home, Agent, and Help views. Only one browser controls web APIs; another browser receives a busy 4409 modal and cannot trigger actions. Every `/api/` endpoint and auxiliary socket requires live primary ownership (returning 423 if inactive, 503 during shutdown). Browser disconnect or a 35s timeout cooperatively cancels pending browser tasks, aborts active native/Blockly work, and restores the waiting QR on the display while suppressing idle animations.[^src-20261010-developmentguide] [^src-20261010-lifecyclerefinementsevidence]

## CLI launcher recovery and single-ownership packaging (2026-10-10)

The root package `ninjarobotpi0` delegates console scripts exclusively to `ninja-core`, `pi0servo`, `pi0disp`, `pi0buzzer`, and `pi0vl53l0x`, eliminating overlapping RECORD entries. Missing launchers can be recreated via locked targeted sync:
```bash
env -u UV_PROJECT_ENVIRONMENT -u UV_PROJECT uv sync --locked --inexact --no-dev \
  --reinstall-package ninja-core --reinstall-package pi0servo \
  --reinstall-package pi0disp --reinstall-package pi0buzzer \
  --reinstall-package pi0vl53l0x
```
followed by verification with `uv run --no-sync ninja_core --help` and `./install.sh --check`. Inert tests passed 105 focused and 331 root regression tests (1 excluded baseline). Real environment repair requires explicit owner approval.[^src-20261010-developmentguide-2] [^src-20261010-clientrypointrepairevidence]

[^src-20261010-developmentguide-2]: Historical 2026-10-10 Developmentguide (CLI recovery).
[^src-20261010-developmentguide]: Versioned Developmentguide (2026-10-10 lifecycle refinements).
[^src-20261010-clientrypointrepairevidence]: CLI launcher repair evidence and validation records.
[^src-20261010-lifecyclerefinementsevidence]: Lifecycle refinements implementation evidence.

## Cloud model provider adapter development and testing (2026-10-10)

Development guidelines for `ninja_core.providers` and cloud adapters:[^src-20261010-developmentguide-3] [^src-20261010-ninja-core-readme] [^src-20261010-modeladapterimplementation]
* **Inert Testing**: Automated test suites (`pytest tests/test_provider_adapter.py`, `tests/test_gemini_runtime.py`, `tests/test_gemini_models.py`, `tests/test_init_tool.py`, `tests/test_ollama_install.py`) use inert HTTP and SDK fixtures; live provider calls are never performed in automated CI.[^src-20261010-modeladaptervalidation]
* **Rollback and Migration**: Pre-migration configurations are snapshotted to `config.pre-provider.json`. Rolling back requires restoring the previous code/lockfile and config snapshot.[^src-20261010-modeladapterimplementation]
* **Python Runtime Boundary**: Package manifests require Python 3.10+.[^src-20261010-modeladapterimplementation] [^src-20261010-modeladaptervalidation]

[^src-20261010-developmentguide-3]: Current versioned Developmentguide (2026-10-10 model adapter release).
[^src-20261010-ninja-core-readme]: ninja_core package README (2026-10-10 model adapter release).
[^src-20261010-modeladapterimplementation]: Pi0 Cloud Model Provider Adapter implementation evidence.
[^src-20261010-modeladaptervalidation]: Cloud model adapter validation report.
