# Fresh Raspberry Pi OS installation repair — 2026-10-12

Owner request: repair the fresh Zero 2 W / 64-bit Lite installation and refine README in place. Implementation is authorized by the explicit request to fix installer and documentation issues. No live Pi, dependency installation on this workstation, runtime/driver changes, or publication is included.

## Evidence and diagnosis

- Read `install.sh`, `scripts/install-rpi.sh`, `install_system.py`, `install_check.py`, `install_ollama.py`, installer tests, README and the current InstallationGuide resolved by the knowledge map.
- Wiki query: `references/installation-guide`, `references/installation-and-wiring`, `concepts/development-workflow`, `analyses/development-history-and-evolution`. Pages are draft/unverified; source status is ingested, which does not establish physical validation. Baseline `scripts/wiki.py check` passes.
- The reported check is read-only and confirms installation stopped before prerequisites/environment creation. The owner subsequently supplied the first failure: interrupted TLS download from releases.astral.sh followed by DNS resolution failure for github.com while downloading uv. Add three bounded attempts around the verified upstream installer, which performs the inner binary download; preserve TLS/checksum verification and nonzero failure. Existing scripts already attempt uv, Node and source-built pigpio, so missing binaries alone do not establish those steps were absent.
- Official Raspberry Pi downloads (checked 2026-10-12) list Trixie/Debian13, 2026-10-06, kernel6.18 for 64-bit Lite, compatible with Zero 2 W. Bookworm is Legacy. Official update instructions use apt update then full-upgrade.
- Current official Trixie ARM64 package index contains neither pigpio nor pigpiod. A mandatory `apt install pigpio` would break this target. Keep the checksum-verified source fallback. The pinned upstream Makefile confirms `make pigpiod` produces the required shared library. Official pinned uv installer SHA256 matches the repository.
- Gaps: pip is omitted from OS prerequisites; preflight failures occur outside the diagnostic trap; the checker does not inspect pigpiod.service or activation script; a large Ollama download precedes core environment creation; README joins check/start commands and lacks fresh OS updating and clear missing-unit/environment recovery.

## Phases

1. Repair installer diagnostics and dependencies: report early stage failures; clean only owned locks; install python3-pip; report existing administrator service policy clearly without overwriting it; keep uv/Node checksum validation and retry the inner uv installation at most three times (2/4-second waits); prepare pigpio and Python before the cloud CLI; detach installer child stdin from streamed bootstrap.
2. Strengthen read-only acceptance: include .venv activation and loaded, unmasked pigpiod systemd unit, without starting services. Test missing units and failures as well as successful clean fallback downloads and reruns using inert fixtures.
3. Refine existing README sections in all four languages: current OS guidance, update/prerequisite commands, download-before-run with explicit error handling, separate cd/check/start, activation only after success, private uv discovery and existing-checkout repair. Preserve section structure and unrelated robot instructions.
4. Run targeted installer/upgrade/CLI/Ollama tests, Python lint, shell syntax, dry-run and protected-core checks; inspect diff. Prepare complete new English raw InstallationGuide, DevelopmentGuide and DevelopmentLog versions plus evidence and README English snapshot. Preserve the owner's prior request to defer wiki ingestion/review; do not register or refresh pointers/mappings in this task.

## Impacts and rollback

System packages and inactive daemon installation remain normal-user/sudo tasks, never automatic hardware activation. Existing Git files, calibration and config are retained. Errors must prevent the success message. Read-only checks must not mutate installation. Restore only this change's source files to roll back; do not delete environments or user data. Package/service deployment and hardware acceptance remain owner-manual.

Expected eventual wiki pages: installation-guide, installation-and-wiring, development-guide, development-workflow, overview, development-history-and-evolution. Source registration, normalization, ingestion, semantic review and current-pointer publication are deferred to owner manual validation.
