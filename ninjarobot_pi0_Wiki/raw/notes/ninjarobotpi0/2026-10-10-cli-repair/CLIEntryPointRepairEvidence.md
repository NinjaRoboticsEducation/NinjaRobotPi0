# CLI launcher repair evidence — 2026-10-10

English-only raw candidate; no ingestion, normalization, curated edits, source registration or semantic/human review is performed. Existing originals/current pointers remain unchanged.

## Observed failure

On the current Zero 2 W, all five .venv/bin robot launchers are absent. Their installed distribution metadata remains present. ninja-core's installed RECORD lists ../../../bin/ninja_core, and ninjarobotpi0's RECORD lists that same path plus the other four providers' launchers. The corresponding provider packages also list their own launcher paths. The preceding root-project rename is in commit 5e8377243c3219624850fe4c73d26cc64226cfee. Its transaction log is not available; exact deletion timing is inferred, not fabricated. Duplicate file ownership is directly confirmed.

`uv run --no-sync -- ninja_core --help` reproduces ENOENT/exit 2. `.venv/bin/python -B -m ninja_core --help` succeeds/exit 0 and lists server, movement-tool and configuration commands without hardware initialization. Thus the missing launcher is distinct from a robot/config/driver failure. Ordinary locked offline sync preview does not reinstall the already-installed provider packages, so a generic retry is insufficient.

## Scoped fix

Root pyproject no longer declares the five duplicate console scripts; provider metadata and command names are unchanged. The installer performs locked targeted reinstallation of ninja-core, pi0servo, pi0disp, pi0buzzer and pi0vl53l0x. Read-only installation inspection checks every executable path and prints a minimal locked --inexact repair command when needed. uv compatibility now requires --reinstall-package. No driver/runtime code, configuration, calibration or dependency version is changed.

Repair preview plans six local builds/reinstallations: changed root metadata plus the five providers. --inexact keeps unrelated/dev packages. Real environment repair requires permission; it was not executed without owner approval. No services are stopped/started, no system installation or server/device tool is run. An isolated unseeded uv venv fixture confirms --allow-existing preserves an inert launcher, distinguishing that prompt step from the ownership problem.

## Validation

- Focused installer/ownership/diagnostics: 105 passed, one protected-baseline test excluded, exit 0.
- Full root regression: 331 passed, one excluded, 31 existing dbus_next deprecation warnings, exit 0 (88.52 seconds).
- Focused Ruff, shell syntax, lock validation, installer dry-run and repair dry-run: PASS.
- Read-only inspection detects all five missing launchers. A cold npm probe timed out, then direct retry returned npm 11.19.0/Node v24.21.0; no tool replacement occurred. This is separate from Python ENOENT.
- All new raw sources contain no Japanese/Chinese text. Root README translations remain in the requested language-section order; its raw snapshot contains English only.
- Local Markdown target checks pass for root documentation and all new candidate documents. Registered current InstallationGuide/DevelopmentGuide/DevelopmentLog hashes retain 0303e14ce171088cba240df2a0a3a29d88e2db0dc5cc2263f26f95d89ac68945, 80ef9c89176a6b0a3749f9127697464f197c2972bf2a41ae533fa2cb7afdc0ab and d176728a0871bab1ad8a7138df05ca04d87c6782011c7459f49278c07a9c3a88 respectively.
- Protected source checks retain the nine accumulated differences from the older baseline, including pre-existing feature changes. No fingerprints are refreshed. Wiki mappings remain deferred; search/source-status environment is unavailable and tracked evidence was read instead.
- Repaired actual-console help, server/ngrok startup and physical acceptance: NOT RUN without repair/readiness authorization.

## Candidate versions

Complete new English manuals and English README snapshot are under raw/articles/ninjarobotpi0/2026-10-10-cli-repair. Complete English DevelopmentLog, plan, validation and this evidence are under raw/notes/ninjarobotpi0/2026-10-10-cli-repair. They preserve English guidance from the preceding full lifecycle candidates while excluding their translated sections; original versions are unchanged. Recovery behavior above supersedes historical setup descriptions below the new manuals' dated introductory section.

For owner ingestion after validation, review setup/installation/package/CLI pages against this fix, register complete new source versions and update current pointers/implementation maps deliberately. No new source IDs or reviews are invented. See [plan](CLIEntryPointRepairPlan.md) and [validation](CLIEntryPointsValidation.md).
