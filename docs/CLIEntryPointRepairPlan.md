# CLI entry-point repair plan

## Evidence and root cause

The 2026-10-10 checkout has installed ninjarobotpi0/ninja_core/driver metadata but lacks all five shared `.venv/bin` launchers. `uv run --no-sync -- ninja_core --help` reproduces exit 2/ENOENT without starting hardware. Both the root distribution and the individual packages record the same five launcher paths in installed RECORD files. The preceding root-distribution rename can therefore uninstall files still owned by unchanged packages. Ordinary offline sync preview considers the packages installed and does not repair these files. The collision is confirmed; the exact prior installer transaction was not logged and is inferred from the rename and missing shared paths.

Current wiki setup evidence: installation-guide and the registered 2026-10-09 complete manuals (src-20261009-installationguide, src-20261009-developmentguide-2, src-20261009-developmentlog-2). Source-grounded AI reviews remain draft/unverified, not physical acceptance. Search/source-status environment is missing, so tracked evidence was read directly. Current wiki mappings already have deferred lifecycle/policy drift.

## Phase 1: Single ownership

Keep existing command names and their provider package entry points unchanged. Remove duplicate console-script declarations only from the aggregating root project. Retain the ninjarobotpi0 identity, dependency versions, editable local dependencies and .venv path/prompt. Do not change robot code or protected fingerprints.

## Phase 2: Recovery and installation validation

Have the installer perform locked targeted reinstallation of the five local provider packages, so upgrades from overlapping root metadata recreate launchers regardless of previous ownership. Check all five executable paths, not ninja_core alone. Capability-check uv's reinstall flag. Give read-only diagnostics an actionable minimal repair command while retaining full-install instructions for absent dependencies. Preserve config/calibration and existing environment/dev dependencies when performing the owner's minimal repair. Do not install anything in the local environment without permission, stop services or start hardware.

## Phase 3: Tests and documentation

Test single ownership from TOML, all-launcher detection, capability failures and inert installer invocation/rerun behavior. Use an isolated fake RECORD uninstall simulation to cover overlapping ownership without package installation. Run focused Ruff, shell syntax, offline lock checks and safe CLI --help only if an environment repair is approved. Stage English-only documentation/evidence and complete new English manual versions, preserving registered originals and current pointers. Only root README translations are multilingual in English/Japanese/Traditional Chinese/Simplified Chinese order. Wiki ingestion/review remains owner-deferred.

## Acceptance

Exactly one provider owns each robot command; installer synchronizes locked local providers and checks all launchers. Missing files are distinguished from missing packages and diagnosed without hardware activity. The owner's repaired environment can run ninja_core --help. Server startup remains pending explicit hardware readiness and is not a software smoke test.
