# Node installation validation — 2026-10-12

## 1. Scope of validation

Repair the reported Node-stage exit2 with tar short writes / No space left on device. Create a private temporary workspace under checkout/.ninjarobot-install; export it as TMPDIR; check actual free storage before downloads; label Node failure operations; validate node/npm before publication. Refine existing README in all four languages. Core/drivers, dependencies/pins, credentials and configuration are unchanged.

## 2. Environment and prerequisites

Host: macOS, existing cached CPython3.13/pytest and Ruff0.16.1; no dependencies installed. Owner target: Raspberry Pi Zero2W512MB, Raspberry Pi OS Lite64/Trixie. Debian release notes confirm default RAM-backed /tmp (maximum50%RAM). Pinned Node22.23.3 ARM64 archive is30,172,012 bytes; file payload193,713,814 bytes; combined223,885,826 bytes excludes metadata and decoder RAM. SHA256 matches the committed pin. Workspace must be on disk with at least2GB available; this is a reserve, not a guarantee of every dependency's storage requirements.

## 3. Safety notes

Host fixtures use inert commands and temporary paths. No sudo/apt/service/GPIO or hardware operation occurred. Real ARM64 archive inspection/extraction is passive; its binaries were not executed on the host. Keep actuator power disconnected during software maintenance.

## 4. Safe smoke tests

Owner pending, from the existing checkout:

```bash
cd "$HOME/NinjaRobotPi0"
df -h "$HOME" /tmp
./install.sh --dry-run
./install.sh
```

Expect a disk workspace, no Node extraction ENOSPC and eventual Software installed. Then run ./install.sh --check separately. For published older code, the README supplies mkdir -p -m700 "$HOME/.cache/ninjarobot-install-tmp" followed by TMPDIR="$HOME/.cache/ninjarobot-install-tmp" ./install.sh. Ensure HOME has2GBfree. No checkout deletion or system tmp.mount changes are needed.

## 5. Communication/interface tests

No SSH/live Pi or cloud inference. A real official Node archive was downloaded to temporary host storage and hash-checked. Test downloads, compiler, privileged installation, services and package setup remain inert/offline fixtures. Network faults remain separate from ENOSPC.

## 6. Sensor/display checks

Not affected and not performed. Existing onboarding applies after software acceptance.

## 7. Actuator-moving or power-risk tests

Not performed. Service activation/tool startup remains a separate owner readiness step; the installer does not start/enable robot or pigpio services.

## 8. Expected outcomes

Child uv/Python build tools inherit disk TMPDIR. Low capacity fails early with actual workspace/free-space guidance. Failed Node extraction cleans this invocation's partial files and lock, does not publish tools/node, and permits retry. Broken downloaded Node/npm cannot be published. Existing compatible tools are reused, even if checkout was removed; incompatible private tools remain preserved for deliberate repair.

## 9. Execution status and evidence

- Focused fresh-install suite:19 passed. Cases include workspace capacity boundaries/inspection failure, unusable inherited TMPDIR, extraction exit2 with partial files, retry after cleanup and broken downloaded npm rejection.
- Complete targeted fresh-install/bootstrap/upgrade/CLI/Ollama suite: **130 passed**, exit0,41.68 seconds.
- Ruff syntax/Pyflakes checks and format checks on affected Python passed. Bash syntax, dry-run, protected-core and whitespace checks passed.
- Official Node archive SHA256/passive size analysis passed; real complete extraction on host disk was checked separately. Host cannot establish ARM64 execution or on-device memory behavior.
- Read-only wiki strict lint passed (0 errors,0 warnings,5 new unregistered-source suggestions); link/index checks passed. Knowledge mapping check still flags eight implementation fingerprints and the fresh-install test classification pending owner publication; no hashes were refreshed.
- README structure and local links verified with existing project checker. New complete English raw manual/log/README/evidence candidates are prepared; ingestion/review, pointers/maps remain owner-deferred. Current curated pages remain draft/unverified.

Reproduction with a provisioned environment:

```bash
.venv/bin/python -B -m pytest tests/test_fresh_install.py tests/test_installer_bootstrap.py tests/test_upgrade_workflows.py tests/test_cli_entrypoints.py tests/test_ollama_install.py -q
bash -n scripts/install-rpi.sh
./install.sh --dry-run
python3 -B scripts/verify_core.py
```

## 10. Pass/fail checklist

PASS: deterministic host workspace/cleanup/retry/capability tests, syntax/lint/format, protected runtime and passive archive verification. PENDING: real Pi installation using corrected code or older-code workaround. DEFERRED: remote Git and canonical wiki publication. Owner log confirms extraction ENOSPC; the default Trixie RAM-backed workspace explains why SD free space alone was insufficient. Check df on the Pi if failure persists on disk.

## 11. Rollback steps

Restore only this task's installer/helper/test/README changes if rolling back development; keep prior fresh-install fixes, private tools and configuration. Retry using a disk-backed TMPDIR with published older code. Never remove an active installer lock. A failed controlled extraction cleans its own workspace, so deleting the checkout is unnecessary.

Primary evidence: [Debian Trixie temporary-directory change](https://www.debian.org/releases/trixie/release-notes/issues.en.html#the-temporary-files-directory-tmp-is-now-stored-in-a-tmpfs), [official pinned Node archive](https://nodejs.org/dist/v22.23.3/node-v22.23.3-linux-arm64.tar.xz). Local wiki retrieval used references/installation-guide, installation-and-wiring, development-guide, concepts/development-workflow, overview and development-history-and-evolution.
