# Installer inputs and provenance

The installer downloads upstream artifacts; it does not vendor or relabel them. Existing
Python/frontend dependencies and their licenses remain governed by the unchanged lockfiles.
Review `scripts/install-versions.env` before changing any tool pin or digest.

| Input | Reviewed version/source | License |
| --- | --- | --- |
| uv | 0.11.29, versioned astral.sh installer; installer SHA-256 recorded | [MIT](https://github.com/astral-sh/uv/blob/0.11.29/LICENSE-MIT) or Apache-2.0; retain upstream notices |
| Node.js | 22.23.3 Linux arm64 archive; digest checked against official SHASUMS256 | [MIT and bundled third-party notices](https://github.com/nodejs/node/blob/v22.23.3/LICENSE); archive preserves its LICENSE |
| pigpio | v79 commit c33738a320a3e28824af7807edafda440952c05d; codeload archive digest recorded | [Unlicense](https://github.com/joan2937/pigpio/blob/c33738a320a3e28824af7807edafda440952c05d/UNLICENCE) |

Node archive and pigpio source digests authenticate the reviewed bytes; the uv digest checks
its versioned installer script. That script downloads uv's upstream release artifact, so this
is not an independent digest check of every transitive downloaded binary. Upstream HTTPS,
package registries and Debian signed repository metadata remain supply-chain dependencies.
`apt-get install` uses Bookworm repository updates rather than pinning OS patch packages.
ShellCheck-py 0.11.0.1 and Playwright 1.62.1 are isolated development/CI tools, not robot runtime
requirements. CI actions are pinned to reviewed commit IDs. No service is activated by CI.
