# Installer recovery and diagnostics — 2026-10-08

## Scope and environment

The owner reported Node/uv version failures and missing project Python/CLI, then requested
clear recovery steps and an installer fix. These failures mean the checkout is incomplete or
its detected tools differ from pins; check alone never installs. The first actual installation
error is still required to diagnose a failed Pi transaction. Bookworm/Trixie targets, tool pins,
locked dependencies, robot functions, configuration and hardware activation rules are unchanged.

## Implementation

- `scripts/install_check.py`: read-only banner; required/detected versions and executable paths;
  incomplete/non-executable environment messages; catches executable/timeout failures; shell-quoted
  local install command. Keeps nonzero failure status, and retains exact version checking.
- `scripts/install-rpi.sh`: visible stages; failure exit handler reports stage/exit status and retry
  command, removes its own temporary directory/lock, and preserves settings. Python and frontend
  run as separate stages so failures can be identified. Does not auto-update Git or start hardware.
- `install.sh`: existing destination remains protected and now prints the exact local retry command.
- README/current manuals: explicit fetch-default-HEAD + fast-forward instructions that also work
  for the bootstrap's detached checkout, then install, check, and onboarding preview. Stop on Git
  errors; no forced resets or configuration deletion.

## Safety, expected results and pending Pi checks

Keep actuator power disconnected during software installation. On the Pi, after publishing and
fetching this patch, `./install.sh --check` should explain missing components and print a retry
command without creating settings. Run `./install.sh`, accept its displayed changes and wait for
Software installed; rerun `--check` expecting PASS. Preserve the first error and failure-stage
message if installation stops. Use `./onboard.sh --dry-run` before the existing hardware procedure.

Communication, sensor/display and actuator tests remain the README's separate physical checklist;
no such tool, robot server, live account, or OS package transaction was run here. Physical movement
is not needed to validate these diagnostics. No rollback of settings is needed because they are
not changed by checks; revert this patch to recover the former messages. Install failures retain
already installed software and require repair/retry, not an OS-wide rollback.

## Host verification

Targeted checks passed: first-install diagnostics contain expected/detected versions, remain
read-only, and handle timeout/exec failure. Inert installer fixtures cover successful rerun,
checksum rejection, and injected Python sync failure (exit 7), checking stage reporting,
lock cleanup, absence of later npm work and preservation of calibration. Core, lint and final
knowledge checks are recorded below after documentation integration.

Wiki evidence: current installation-guide, installation-and-wiring, development-workflow and
guided-onboarding pages are draft/unverified. New immutable manual versions retain that boundary.

## Final host results

- Python 3.11 and Python 3.13: **188 root tests passed on each interpreter**.
- Python 3.13 retains eight existing dbus-next deprecation warnings; no failures.
- Ruff lint/format, ShellCheck, whitespace check and protected core/metadata verification passed.
- Current knowledge/manual mapping, strict wiki lint, links and indexes passed. All changed pages
  have source-grounded AI reviews and retain draft/unverified status.
- No real Pi installation, hardware activation, commit or push occurred in this task.
