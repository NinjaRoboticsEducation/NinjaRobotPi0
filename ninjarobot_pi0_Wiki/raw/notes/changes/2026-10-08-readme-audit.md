# Four-language README correctness audit — 2026-10-08

## Scope and owner direction
The owner supplied a four-language README and requested a correctness audit. The follow-up
explicitly retained intentional omissions and requested concise corrections, with necessary
recovery/check guidance only in Troubleshooting or appendices. The user-authored structure
is preserved. Only README and required knowledge provenance/navigation are edited.

## Verified corrections and code evidence
- scripts/install-rpi.sh exits on active pigpiod/ninjarobot before OS/Python installation.
  Its platform checker PASS is not installation success. README troubleshooting distinguishes
  Software installed from preflight, preserves calibration, stops robot service before daemon,
  disconnects actuator power before stopping hardware processes, and retries local checkout.
- scripts/install_check.py validates compatibility; pinned downloads are fallbacks. Bookworm/
  Trixie are reference OS releases, not a codename allowlist. README Appendix C preserves this.
- ninja_utils/src/ninja_utils/service_manager.py locates uv with shutil.which, checks config,
  pigpiod and ninja_core; install enables ninjarobot.service but does not start it. Unit ExecStart
  is uv run ninja_core server --autostart, so startup can sync Python dependencies. README uses
  the installer checker --find-tool uv and .venv/bin/ninja_utils commands, with PATH scoped to
  install-startup. It explains inactive-before-start and actual hostname/IP instead of a fixed
  ninjarobot.local URL or guaranteed one/two minute startup. Removal stops the service.
- ninja_core/src/ninja_core/web_server.py: run_server prompts for token; an existing token can
  be retained with Enter; normal input is not hidden. README directs token changes to onboarding.
  setup network code attempts ngrok even without configured token; skipping onboarding ngrok
  is not local-only mode. Autostart checks presence, not token validity. QR requires public URL
  and display. Power slider requests confirmation; shutdown attempts Poweroff movement and runs
  sudo shutdown. Animation success/idle LED do not guarantee OS shutdown.
- ninja_core/src/ninja_core/movement_cli.py parse_movement_command accepts numeric speed suffixes
  but rejects XF because a trailing speed after an alphabetic special target is not stripped.
  Replaced M_20:C/21:XF with M_20:C/21:45F. Positional servo guidance requires calibrated pins
  and mechanical limits; movement recording centers servos. Existing multi-step easing wording
  is retained: movement_controller selects ease-in, linear, ease-out by step position.
- English/Japanese/Traditional/Simplified Chinese corrections cover manual pigpiod activation,
  installation success, autostart, server behavior, credentials and recovery. Simplified Chinese
  autostart had copied Traditional Chinese prose; it is now Simplified Chinese.
- Clarified BCM versus physical pin numbers, 3.3 V GPIO logic versus module supply voltage,
  servo supply sizing, positional versus continuous-rotation servos, and UART/display pin conflicts.
- Google API usage is not guaranteed free. Quotas/model/region/billing and ngrok plan limits
  are account-dependent; source links remain in the manual. Credentials/config are private.

## External primary references inspected
https://www.raspberrypi.com/documentation/computers/configuration.html
https://ai.google.dev/gemini-api/docs/billing/
https://ai.google.dev/gemini-api/docs/pricing
https://github.com/ngrok/ngrok-docs/blob/main/pricing-limits/free-plan-limits.mdx
These support configuration/account caveats, not a claim of physical acceptance.

## Validation performed
- Read all four language sections and compared installer, checker, onboard launcher/wizard,
  service manager, server/ngrok/shutdown flow and both servo/core command parsers.
- bash -n parsed all 54 README shell blocks. No documented command was executed on hardware.
- Four corrected movement examples passed the isolated core parser using fixture definitions,
  without importing or initializing robot modules.
- Four-language command presence/parity, fenced-block balance and relative file links passed.
- Protected core source/metadata fingerprint check passed. No code, installer, lock or frontend edit.
- Required wiki plans/reviews/gates follow this evidence registration; no human verification claimed.

## Limits
No Pi, daemon, service, GPIO, calibration, server, account API or deployment was operated.
Documentation corrects existing behavior; it does not repair the legacy service implementation.
No new full runtime suite was needed for this documentation-only change. Old sources remain
immutable and retain historical wording.
