---
type: Reference
title: Current installation manual
description: Current installation manual.
status: draft
generated:
  by: agent:codex
  at: '2026-10-07T13:03:34.637721+00:00'
sources:
- id: src-20261009-installationguide
  resource: urn:llmwiki:source:src-20261009-installationguide
  title: Installationguide
  content_hash: sha256:0303e14ce171088cba240df2a0a3a29d88e2db0dc5cc2263f26f95d89ac68945
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
- id: src-20261008-2026-10-08-readme-audit
  title: Pi0 README audit evidence and validation limits
  content_hash: sha256:7a945023f45ad2e179e5cae529665df9ed050bfe5cf36f440f857a02e28cfea4
  resource: urn:llmwiki:source:src-20261008-readme-audit
- id: src-20261009-readme-2
  title: Readme
  content_hash: sha256:21ade3212445744ae9fedb7dde760014b69ad3e8413b6ffb895bd27a820aa61d
  resource: urn:llmwiki:source:src-20261009-readme-2
- id: src-20261009-2026-10-09-builtin-movements
  resource: urn:llmwiki:source:src-20261009-2026-10-09-builtin-movements
  title: 2026 10 09 Builtin Movements
  content_hash: sha256:6bd14ef705bb60c2c228c95940fd6cb771299532f13e10fdc4faae22db3f216a
- id: src-20261010-installationguide-2
  resource: urn:llmwiki:source:src-20261010-installationguide-2
  title: Installationguide
  content_hash: sha256:18d2002125e05e7026c4bc7568ba8fb1f588a466bc7815f850476e07fa922913
- id: src-20261010-installationguide
  resource: urn:llmwiki:source:src-20261010-installationguide
  title: Installationguide
  content_hash: sha256:daf4f218e05c0f9deec2f93a28e679b86ccc0372f86f7a0962d9000d2bf6392f
- id: src-20261010-clientrypointrepairplan
  resource: urn:llmwiki:source:src-20261010-clientrypointrepairplan
  title: Clientrypointrepairplan
  content_hash: sha256:05eb8fe221519b45022eb360c7441b1ff7a1b41e542502ab9759ca93ca2701fc
- id: src-20261010-clientrypointsvalidation
  resource: urn:llmwiki:source:src-20261010-clientrypointsvalidation
  title: Clientrypointsvalidation
  content_hash: sha256:7a38fdff3c9c1e9bcb8eb98d85bcd773d2504e6936381994778fb42a95699ce3
- id: src-20261010-lifecyclerefinementsimplementationplan
  resource: urn:llmwiki:source:src-20261010-lifecyclerefinementsimplementationplan
  title: Lifecyclerefinementsimplementationplan
  content_hash: sha256:5d4be31936118493340340291e66a59c7f76886f26e791ca0963721aab9f21a8
- id: src-20261010-lifecyclerefinementsvalidation
  resource: urn:llmwiki:source:src-20261010-lifecyclerefinementsvalidation
  title: Lifecyclerefinementsvalidation
  content_hash: sha256:01fa07f823e9dedfcc2d243ae107b496758960b0c5be790db9df2a8deef94066
- id: src-20261010-readme-3
  resource: urn:llmwiki:source:src-20261010-readme-3
  title: Readme
  content_hash: sha256:dd7aadd29af3a65ecd5a300f54a41534f0a212e9b4512ece03d3d21ec9b24922
semantic_review:
  version: 1
  performed_by: agent:antigravity
  performed_at: '2026-10-10T12:07:31.827347+00:00'
  target_hash: sha256:8035d6d72bf75c3843fe62f0e253f08738309f69fb18a82ea22956fd35ff8315
  result: passed
  checks:
    source_support: passed
    contradictions: passed
    limitations: passed
    claim_strength: passed
    visual_evidence: not_applicable
  notes:
  - Reviewed installation manual procedures against install.sh, onboard.sh, and 2026-10-10
    InstallationGuide.md. ninjarobotpi0 venv prompt, single-ownership launcher verification
    in .venv/bin, and targeted --reinstall-package repair match current manual.
  - Installer checks do not auto-activate robot hardware. Real environment repair
    requires explicit owner authorization.
---

# Current installation manual

Resolve the complete current InstallationGuide through project-knowledge.json or the wiki README. It covers the Raspberry Pi OS 64-bit compatibility requirements, software installation, explicit onboarding, prerequisites, calibration warnings and recovery. Root InstallationGuide.md is a compatibility pointer. Earlier detailed material is preserved as historical reference, with current installation instructions clearly identified.[^src-20261010-installationguide-2]

[Project overview](/overview.md).

[^src-20261009-installationguide]: Historical 2026-10-09 versioned Installationguide.

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


## Multilingual user manual audit

The multilingual README explains that an active pigpiod or ninjarobot service stops installation before dependencies. The initial preflight PASS is not Software installed. Recovery supports the robot, disconnects actuator power, stops the robot service before pigpiod and retries the existing checkout without deleting calibration. After successful installation, pigpiod must be started explicitly; boot enablement is optional. The README uses compatible uv discovery for legacy autostart and corrects ngrok/token, actual hostname, QR and shutdown limitations. Software checks and saved onboarding state do not certify physical results.[^src-20261008-2026-10-08-readme-audit]

[^src-20261008-2026-10-08-readme-audit]: Four-language README correctness audit and code evidence.

The complete public walkthrough is preserved in the current README source.[^src-20261009-readme-2]

[^src-20261009-readme-2]: Pi0 four-language user manual.

## Built-in movement configuration and safety readiness (2026-10-09)

The current installation manual records built-in movement seeding during configuration import. Physical safety requirements specify supporting the robot chassis or raising wheels before testing center or movement commands, verifying external servo power and common ground, and inspecting both `config.json` calibration keys and physical `servo.json` before motion.[^src-20261009-installationguide] [^src-20261009-readme-2] [^src-20261009-2026-10-09-builtin-movements]

[^src-20261009-2026-10-09-builtin-movements]: Automatic native built-in movement evidence and architecture boundaries.
## Lifecycle refinements and virtual environment branding (2026-10-10)

Root distribution, lock identity, and default virtual environment prompt become `ninjarobotpi0` (replacing `ninjarobotv4`). The directory remains `.venv`. The installer explicitly creates or reuses the environment with `uv venv --allow-existing --prompt ninjarobotpi0 --python /usr/bin/python3 .venv`, without `--clear`, before locked sync. uv preflight checks its venv capability flags.[^src-20261010-installationguide] [^src-20261010-lifecyclerefinementsimplementationplan] [^src-20261010-lifecyclerefinementsvalidation]

## CLI launcher recovery and single-ownership packaging (2026-10-10)

Packaging delegates the five robot console commands (`ninja_core`, `pi0servo`, `pi0disp`, `pi0buzzer`, `pi0vl53l0x`) exclusively to their provider packages; the root project `ninjarobotpi0` no longer declares duplicate console scripts, preventing RECORD collision and uninstallation during root upgrades. The installer forces locked targeted reinstallation of the five local providers (`--reinstall-package ninja-core --reinstall-package pi0servo ...`) and verifies that all five executable launcher files exist in `.venv/bin`. Read-only `./install.sh --check` detects missing launchers and reports a minimal locked repair command using `--inexact` without modifying third-party packages or system services. Real environment repair requires explicit owner authorization.[^src-20261010-installationguide-2] [^src-20261010-clientrypointrepairplan] [^src-20261010-clientrypointsvalidation] [^src-20261010-readme-3]

[^src-20261010-installationguide-2]: Current versioned Installationguide (2026-10-10 CLI recovery).
[^src-20261010-installationguide]: Versioned Installationguide (2026-10-10 lifecycle refinements).
[^src-20261010-clientrypointrepairplan]: CLI launcher repair plan and root packaging reconciliation.
[^src-20261010-clientrypointsvalidation]: CLI launcher recovery validation on Raspberry Pi Zero 2 W.
[^src-20261010-lifecyclerefinementsimplementationplan]: Lifecycle refinements implementation plan.
[^src-20261010-lifecyclerefinementsvalidation]: Lifecycle refinements validation report.
[^src-20261010-readme-3]: NinjaRobotPi0 English README snapshot (2026-10-10 CLI recovery).
