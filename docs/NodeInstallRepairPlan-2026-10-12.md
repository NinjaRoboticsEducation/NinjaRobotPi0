# Node installation failure repair — 2026-10-12

Owner authorizes investigating the Compatible Node tooling exit2 failure and fixing installer/README. Prior fresh-install fixes are committed at this turn's start (clean owning repo); preserve them. No dependency installation, live Pi operation, hardware activation, publication or wiki ingestion/review is authorized here.

## Evidence

Current installer calls unqualified mktemp -d: Linux uses /tmp or inherited TMPDIR. Debian13/Trixie now mounts /tmp as RAM-backed tmpfs (default maximum50%RAM), per official release notes. Pinned Node22.23.3 ARM64 archive was downloaded read-only:30,172,012 bytes, unpacked regular-file payload193,713,814 bytes, repository SHA256 a44aeb94849a299b22df10b9e622ec2f605c2183501bc40590705131de7c740f matches. Combined223,885,826 bytes excludes filesystem metadata, decoder RAM and other temporary files. This exposes a resource defect on Zero2W512MB; The owner subsequently supplied tar errors (short writes and No space left on device), confirming extraction storage exhaustion. The default workspace on Trixie is RAM-backed /tmp; exact Pi filesystem capacity remains owner-manual.

Wiki retrieval: references/installation-guide, installation-and-wiring, development-guide, concepts/development-workflow, overview, development-history-and-evolution. Current pages remain draft/unverified; source ingestion/review does not establish hardware acceptance. Current full manuals resolve to 2026-10-12-humanoid-builtins; earlier fresh-install source versions are preserved.

## Implementation phases

1. Create the installer workspace beneath .ninjarobot-install in the checkout (already ignored/private/path-checked), export its absolute path as TMPDIR for child installers/builds, and require2GB available workspace storage before downloads. Keep tools path and all user/system tools. Report the failed operation and workspace capacity. Never change system tmp.mount.
2. Label Node download, checksum, extraction, publication and capability verification. Verify node and npm before publishing the extracted directory; retain a failed extraction only until controlled cleanup, so a retry cannot see partially published private tools. Preserve incompatible preexisting tools with actionable diagnostics.
3. Test inherited unusable TMPDIR, operation-specific exit2, partial extraction cleanup/retry, downloaded-tool validation and disk-space boundaries; run installer/CLI/Ollama/upgrade regressions, lint, syntax, dry-run and protected-core checks.
4. Refine existing README sections in four languages: distinguish confirmed installer resource defect from unconfirmed owner-specific cause, retry an existing checkout, explain external private tools persist after checkout deletion, show safe TMPDIR workaround for published older installer and failure-log capture. Create complete new raw English manuals/log/snapshot/evidence; prior owner request continues to defer ingestion/review/pointers/maps.

## Rollback and limits

Rollback only these source/document changes. Retain config/calibration, tool directories and completed installation state. Workspace cleanup removes only this invocation's owned temporary directory and lock. No actual Pi install or kernel/pigpio acceptance is claimed.2GB check is an early resource reserve (consistent with the existing Ollama archive requirement), not a guarantee of full dependency disk requirements. If the checkout itself is on a constrained tmpfs, choose a disk-backed installation location.

Primary sources: https://www.debian.org/releases/trixie/release-notes/issues.en.html#the-temporary-files-directory-tmp-is-now-stored-in-a-tmpfs ; https://nodejs.org/dist/v22.23.3/node-v22.23.3-linux-arm64.tar.xz .
