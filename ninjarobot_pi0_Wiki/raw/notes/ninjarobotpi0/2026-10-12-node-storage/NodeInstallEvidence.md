# Node installation storage evidence — 2026-10-12

This is a new complete English raw candidate for owner manual validation. Registration, normalization, ingestion, semantic review, current pointers and implementation mappings remain owner-deferred. Prior registered sources and earlier fresh-install candidates are unchanged. Earlier sections below retain their dated historical status; this section governs temporary storage and Node recovery.

The owner supplied Node-stage exit2 plus tar short writes and No space left on device. The installer used unqualified mktemp -d, which selects /tmp by default; Trixie stores /tmp in RAM. The verified Node22.23.3 ARM64 archive is30,172,012 bytes and expands to193,713,814 bytes of regular-file payload before filesystem metadata. Together223,885,826 bytes creates excessive temporary-storage pressure on Zero2W512MB. This is an installer resource defect; the archive SHA256 matches and it extracts successfully on host disk. No ARM64 binary execution or physical Pi acceptance is claimed.

The installer now creates a private work.* directory under checkout/.ninjarobot-install, exports that absolute path as TMPDIR to children and checks at least2GBfree before setup. Node operations are labelled download/checksum/extraction/capability/publication, and failure diagnostics report the workspace and filesystem free space before cleanup. Extracted node/npm must work before tools/node is published. Failed extraction removes this invocation's partial workspace/lock so reruns remain possible. Existing tools/config/calibration are retained. The README preserves headings and multilingual order, gives a disk-backed TMPDIR workaround for published earlier code, explains tools persist outside a deleted checkout, and supplies Bash pipefail/tee log capture.

130 targeted host tests passed, including new disk-capacity boundaries, workspace inspection failure, unusable inherited TMPDIR, simulated extraction ENOSPC, cleanup/retry and broken downloaded npm rejection. Ruff syntax/Pyflakes/format, Bash syntax, dry-run, protected-core, whitespace and document links passed. The real pinned archive was hash-checked, fully extracted on host disk, and its node ELF ARM64 header/npm inspected passively. Read-only wiki strict lint has0errors/0warnings and5new-source suggestions; link/index checks passed. Knowledge mapping remains pending owner publication and no fingerprints were refreshed. Actual Pi rerun remains owner-manual.

See the [implementation plan](../../../../../docs/NodeInstallRepairPlan-2026-10-12.md) and [validation report](../../../../../docs/validation/NodeInstall-2026-10-12.md).

## Primary sources

- [Debian Trixie temporary-directory release notes](https://www.debian.org/releases/trixie/release-notes/issues.en.html#the-temporary-files-directory-tmp-is-now-stored-in-a-tmpfs): /tmp is RAM-backed by default, up to50%RAM; large temporary files may exhaust it. Retrieved2026-10-12.
- [Official pinned Node archive](https://nodejs.org/dist/v22.23.3/node-v22.23.3-linux-arm64.tar.xz): downloaded read-only, SHA256 a44aeb94849a299b22df10b9e622ec2f605c2183501bc40590705131de7c740f matches install-versions.env. Complete host disk extraction passed; the ARM64 ELF header and npm are present. No binary executed.
- Owner's supplied installation log: tar reports Wrote only3072 of10240 bytes then Cannot write: No space left on device across Node headers and exits2. Do not confuse this with the prior uv network failure. Exact on-device df output has not been obtained; if disk-backed rerun fails, inspect the actual filesystem's space/inodes.

## Local knowledge and limits

Queried installation-guide, installation-and-wiring, development-guide, development-workflow, overview and development-history-and-evolution. Existing curated pages are draft/unverified; prior semantic review is not physical acceptance. Current manuals remain those resolved by project-knowledge.json; earlier fresh-install source versions are preserved. Package pins/locks and runtime/driver/config source are unchanged.2GBcheck is a reserve consistent with the earlier Ollama requirement, not total installation sizing. No system tmp.mount change or tool deletion occurs.

## Implementation SHA256

- `README.md`: `a20d94829c62a79004eed625202e149dee1ba72f5c879f617e8ceaefabd9dc5a`
- `scripts/install-rpi.sh`: `6153337db9d1d90a638750e2f07c927cb2fff4355704a64330af171b10dfe971`
- `scripts/install_check.py`: `63b3c33f6e6ea0ab1836e00727f06b8604369ab69e9b80b5bd1ba20fd430a96f`
- `tests/test_fresh_install.py`: `2b1dfffba9ae00da4d1490e0ae44ecfc47bcace7915c6f12e87d7b6c906185ee`
- `docs/NodeInstallRepairPlan-2026-10-12.md`: `c2b7bcb6f33f1d9acb8cae27fb838e6a12831c9098fbc51293d2d9c41b75baef`
- `docs/validation/NodeInstall-2026-10-12.md`: `8f81f25bf67b2050150cf85b7b52c4956c28da74d25086c59185217dc2a68db4`

## Owner publication scope

After manual Pi validation, ingest this evidence/full manuals/English README and review installation-guide, installation-and-wiring, development-guide, development-workflow, overview and development-history-and-evolution. Update current source pointers and implementation mappings only after source-grounded review. No registration/ingestion/review/apply was performed in this task.
