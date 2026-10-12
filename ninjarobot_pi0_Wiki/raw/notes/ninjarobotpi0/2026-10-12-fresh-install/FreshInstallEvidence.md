# Fresh Zero 2 W installation evidence — 2026-10-12

This is a new complete English raw candidate for owner manual validation and later publication. No source registration, normalization, ingestion, semantic review, current-pointer change or implementation-map refresh has been performed. Earlier dated sections below are preserved historical evidence; this section supersedes their installation guidance. Runtime, calibration, hardware operation and credentials are unchanged.

Fresh-install refinement: python3-pip is included in OS prerequisites; early preflight/confirmation/lock failures now report the interrupted stage; only owned locks are removed. An existing administrator policy is retained with a specific diagnostic. The daemon and locked Python/frontend setup precede the large Ollama archive. The streamed bootstrap gives the child installer /dev/null stdin (terminal prompts remain on /dev/tty). Read-only --check aggregates core/Ollama status and now rejects missing activation scripts and missing/masked/error pigpiod units. It accepts a loaded inactive unit without starting it. uv/Node reuse and checksum-verified fallbacks remain; private uv does not alter shell profiles.

124 targeted host tests passed using inert dependencies, real archive/hash handling and local Git fixtures. Bash syntax, focused Ruff syntax/Pyflakes and formatting, dry-run and protected-core checks passed. No physical Pi install or service/actuator test occurred. The owner supplied the first error: uv binary download TLS unexpected EOF followed by github.com DNS failure. This explains why later dependencies were absent. The verified upstream uv installer now has at most three attempts with 2/4-second waits, preserving TLS and hashes; persistent connectivity still requires repair. Tests cover transient recovery and exhausted retries.

See the [repair plan](../../../../../docs/FreshInstallRepairPlan-2026-10-12.md) and [validation report](../../../../../docs/validation/FreshInstall-2026-10-12.md).

## External primary-source verification

- [Official OS downloads](https://www.raspberrypi.com/software/operating-systems/): Trixie/Debian13 Lite64, 2026-10-06 release, kernel6.18, Zero 2 W listed; Bookworm is Legacy. Retrieved 2026-10-12.
- [Official Raspberry Pi OS updates](https://www.raspberrypi.com/documentation/computers/os.html#update-your-current-raspberry-pi-software): apt update then full-upgrade within the same OS release; reinstall for major-version migration.
- [Official Trixie ARM64 package index](https://archive.raspberrypi.com/debian/dists/trixie/main/binary-arm64/Packages.gz): downloaded and inspected; no Package names containing pigpio. Therefore do not depend on a Raspberry Pi archive pigpio/pigpiod package for this target.
- [Debian Trixie pigpio source package](https://packages.debian.org/source/trixie/pigpio): binary packages are client libraries, client tools and python3-pigpio; the daemon is not supplied by that source build.
- [Pinned pigpio Makefile](https://github.com/joan2937/pigpio/blob/c33738a320a3e28824af7807edafda440952c05d/Makefile): make pigpiod builds libpigpio.so.1 through LIB1. Existing narrow build avoids global Python setup.py installation.
- [Pinned official uv installer](https://astral.sh/uv/0.11.29/install.sh): downloaded script SHA256 `504a79fd2ed0dcd47e7f04f0792cfd0871f62e24a7fe40fa8ae0f563a369f2bd` matches install-versions.env. No upstream downloaded script was executed on the host.

## Local evidence and limits

Baseline `scripts/wiki.py check` passed. Queried pages: references/installation-guide, references/installation-and-wiring, concepts/development-workflow, analyses/development-history-and-evolution; draft/unverified with ingested sources. Source ingestion is not device validation. Canonical source versions remain those in project-knowledge.json until owner publication.

The README retains its existing headings and four-language order. Fresh OS preparation includes curl/CA certificates/Git/pip/venv, guarded download-to-file, separate cd/check/start, optional activation and private uv discovery, with explicit incomplete-install recovery. No package pin or lockfile changed. Existing tools, config and calibration remain preserved. Git revision updates remain manual.

## Reviewed implementation SHA256

- `README.md`: `7a4a0f401275da732baabe04158809ec39ed8ec3d027f5ef4a9dd36dfccac666`
- `install.sh`: `948dd8a9de75715bb7bbd93f8f8294e27acb87c8f54b57d94689bb3f803e9b01`
- `scripts/install-rpi.sh`: `d2da7e8d6656b70e098fcfaa43bca9e8c607bbfec5532348395c734f4038a5ac`
- `scripts/install_system.py`: `8fc024cf19e8da9806ad5ac64d623d3fdaad6452b9c44ee23c01cb241ef8e27b`
- `scripts/install_check.py`: `c5a8d1bf39e051a8b5e5f328c36ffa1dde779f5ca45c64070bb259bce4463e3a`
- `tests/test_fresh_install.py`: `b5e1d99f9e87e9f5f24dcd54a866ffd6b5d57594e67d2de8ffbbb6665e1c2b9c`
- `tests/test_upgrade_workflows.py`: `4efbe936fa0843064607623941610239c6d52e58e6cbf6d9e1ed44da2989b142`
- `tests/test_cli_entrypoints.py`: `0a2c79fc67fb77073adb30a800374696619a26cfd57fb9af3a4e582301aba6fe`
- `.github/workflows/upgrade-validation.yml`: `96165451865d31f815f3770038b4a0f7d3ad5328eb029700783fdc58204e5730`

## Deferred wiki publication

After owner manual acceptance, register/normalize the new full manuals and English README snapshot with this evidence. Review references/installation-guide, installation-and-wiring, development-guide, concepts/development-workflow, overview and analyses/development-history-and-evolution against the actual source diff before updating pointers and implementation mappings. Do not overwrite registered originals. No human or physical verification is claimed.
