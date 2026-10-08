# Installer compatibility validation — 2026-10-08

## 1. Scope
Replace exact Node/uv checks and OS release allowlists with genuine requirements.
Bootstrap, installation inspection, tool selection and onboarding share the policy.
Core robot packages, locks, wiring, calibration and runtime behavior are unchanged.

## 2. Environment and evidence
macOS host; isolated Python 3.11/3.13 environments. No Raspberry Pi attached.
Vite 7/plugin lock engines: ^20.19.0 || >=22.12.0; all other locked Node engines
admit those ranges. Official reference: https://v7.vite.dev/guide/migration .
uv CLI reference: https://docs.astral.sh/uv/reference/cli/#uv-sync .
Real uv 0.9.26 was downloaded into /private/tmp only. Its sync help exposes all
required flags and its offline locked dry-run resolved 103 packages using Python 3.11.
The first sandbox run hit uv's macOS SystemConfiguration panic; the same offline
non-installing check outside the sandbox passed. This is not a Pi installation test.
Python 3.10 runtime annotations appear without postponed evaluation in config/servo modules;
optional wiki metadata requires >=3.11. No exact Python release gate is introduced.

## 3. Safety
No services or devices were started. Install retries preserve configuration/calibration.
Read-only check does not install or repair; fallback artifacts still require checksum verification.

## 4. Safe smoke tests (Pi pending)
After publishing/fetching the fix: ./install.sh --dry-run; ./install.sh; ./install.sh --check.
Use a normal account. Wait for Software installed. Node 24.21.0 and uv 0.9.26 must
be reused; missing project Python/CLI stays a failure until installation completes.

## 5. Communication/interface tests
No network protocol change. No live account or remote service operation was performed.

## 6. Sensor/display checks
Not run; no sensor/display code changed.

## 7. Actuator tests
Not run or authorized by this installer change. Keep actuator power disconnected while installing.

## 8. Expected outcomes
No Bookworm/Trixie codename equality or exact Node/uv version mismatch.
Genuine Node engine/capability and missing-environment errors remain actionable.
Newer/other OS releases passing preflight are not hardware-qualified by that alone.

## 9. Execution status
89 initial targeted regressions passed before the final extra reuse/minimum tests.
Final validation results are recorded below after completion. Physical Pi validation is pending.

## 10. Checklist
- Real uv 0.9.26 help and offline locked dry-run: passed.
- No dependency lock or robot core modifications: verify_core gate required.
- Full regression/lint/wiki results: appended after final runs.
- Raspberry Pi installation and hardware/account acceptance: pending owner validation.

## 11. Rollback
Retain existing checkout and configuration. If installation fails, preserve the first error
and retry locally after resolving it; do not reset/delete calibration or uninstall system tools.
Git updates use fetch origin HEAD followed by merge --ff-only FETCH_HEAD; stop on Git errors.

## Software compatibility policy

The installer checks capabilities, not exact OS/Node/uv release equality:

- Raspberry Pi Zero 2 W, Linux `aarch64`, Debian-based Raspberry Pi OS (`ID=debian`
  or `raspbian`), and a normal user are required. No release-codename allowlist remains.
  Bookworm and Trixie are the reference targets; other releases are not automatically
  hardware-qualified merely because they pass preflight.
- Python 3.10+ is needed by existing runtime annotations (for example `ninja_core/config.py`
  and `pi0servo/core/servo.py`). Optional wiki development requires Python 3.11+.
  Existing metadata still says >=3.9; this installer check reflects the stricter runtime
  requirement without changing the robot packages. Locked dependencies remain authoritative.
- Node 20.19+ within 20.x, or Node >=22.12.0, matches the committed Vite 7/plugin engines.
  Node 24.21.0 qualifies. npm must be executable; `npm ci` and the build still have to succeed.
- uv has no exact-version gate. Its `sync --help` must expose `--locked`, `--no-dev`,
  `--python`, `--directory`, and `--all-extras`. uv 0.9.26 satisfies this and passed an
  offline host `sync --locked --no-dev --dry-run` against the existing lockfile.
  The capability probe alone does not certify every future uv version; real locked sync
  must succeed, with its original error preserved if it fails.
- Compatible tools on PATH are reused before compatible private tools. Missing/incompatible
  tools use checksum-verified fallback downloads. Download pins are not installed-version
  requirements. System tools and calibration files are retained. The existing pigpio daemon
  qualification remains separate and unchanged.

`./install.sh --check` stays read-only. Missing `.venv/bin/python` or `.venv/bin/ninja_core`
still means installation is incomplete: run `./install.sh`, wait for **Software installed**,
then run `./install.sh --check`. Publish/fetch this change before retrying on the Pi.
No physical Pi, hardware, account, or network-service acceptance is implied by host checks.

日本語：OS のコードネームと Node/uv の完全一致チェックを廃止し、実際の必要条件を確認します。
互換性のある既存ツールを再利用します。`.venv` がない場合は `./install.sh` による導入が必要です。
繁體中文：取消 OS 代號及 Node/uv 的固定版本比對，改查實際需求並重用相容工具。
缺少 `.venv` 時仍須執行 `./install.sh` 完成安裝；實機驗收另行進行。
简体中文：取消 OS 代号及 Node/uv 的固定版本比对，改查实际需求并复用兼容工具。
缺少 `.venv` 时仍须运行 `./install.sh` 完成安装；实机验收单独进行。
