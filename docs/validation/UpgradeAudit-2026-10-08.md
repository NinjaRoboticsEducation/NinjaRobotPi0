# Pi0 installation, onboarding, wiki and UI audit — 2026-10-08

Scope: the approved `DevelopmentPlanDoc/NinjaRobot_Install_wiki_upgrade_261007.md`,
followed by the owner's explicit request to audit/fix new features, align the terminal
onboarding with Pi5 and rewrite the README. No core robot/driver behavior change is authorized.
Pi0 baseline: `3dbc41a4ee3cf9fb1019e3be5e633f5a6b47d862`.
Pi5 reference: `d620fa4e790fd79c1b5d65bc2b95eb71625076cd` (read-only).

## Findings and fixes

| Priority | Finding | Correction and regression evidence |
| --- | --- | --- |
| High | Servo import could prefer conflicting legacy pulse aliases over the fields onboarding validated; signed/noncanonical numeric keys could evade the numeric-key filter | Validate every numeric GPIO key in canonical form and reject conflicting aliases; seven regression cases cover override fields and invalid keys. Existing importer unchanged |
| Medium | Settings helpers could create credential files with a normal process umask before the wrapper restricted permissions | Set owner-only umask around the worker, restrict existing files before writes, restore original mask afterward; test verifies permissions at first write, including exception path |
| Medium | `--resume` repeated hardware setup; saved physical observations could outlive their calibration | Reconcile current saved bytes/hash, invalidate changed observations and skip only unchanged, valid previously completed hardware; status performs the same reconciliation without writing |
| Medium | Malformed saved progress could crash with an attribute error, and arbitrary results were accepted | Bound size, validate schema/step/record types, hardware hashes and status enums before entering write-finally; invalid state stays byte-identical |
| Medium | Hardware setup failure or an invalid menu choice advanced to later steps without recovery | Pi5-style numbered guidance, valid-choice prompts, bulk/per-module reuse, retry-in-place, Enter to continue, and readable summary; tests cover failure→retry→success and bulk reuse |
| Medium | Hidden worker bypassed the supported-platform preflight | All interactive execution now passes the same TTY/platform gate, including internal workers; test proves no helper executes on rejection |
| Medium | Nested private tool paths could redirect writes through symlinks and rejection occurred after privileged package work | Preflight now rejects symlinked ancestors/tool subdirectories/environments before privileged installation; direct regression test |
| Medium | Standalone wiki setup could inherit `UV_PROJECT`, and fresh installer users lacked globally discoverable uv | Clear the project override and fall back to the installer-owned uv executable for explicit setup only; both behaviors tested |
| Low | Read-only tool-version checks accepted arbitrary version prefixes | Exact Node/pigpio matching and exact uv version with optional parenthesized build metadata |
| Low | Failed installation-record publication could leave a partial temporary file | Flush/fsync and finally-cleanup before/after atomic replacement; injected failure test |
| Documentation | Root README lacked a beginner installation/test manual; first-operation guidance assumed global uv and understated runtime ngrok behavior | Rewritten in Pi5-style sections with private-venv commands, default-branch curl, onboarding, test checklist, troubleshooting and multilingual summaries. Runtime start/servo initialization/ngrok attempts clearly separated from onboarding |

Calibration status hashes the exact bytes it validated, preventing a second read from associating
one configuration's validation with another configuration's fingerprint. Software checks still do
not establish correct physical wiring, pulse limits for a particular servo, or actual calibration.

## Plan coverage

| Plan phase | Audit result |
| --- | --- |
| 0 — Baseline | Existing robot packages protected; original user/wiki work preserved |
| 1 — Installer inputs | Existing pinned uv/Node/pigpio manifest, hashes and provenance retained; this audit does not claim new supply-chain attestation |
| 2 — Bootstrap | Existing isolated Git fixtures exercise default branch, explicit refs, ambiguity, destination refusal and checkout behavior |
| 3 — Local installation | Reviewed preflight, locks, apt policy cleanup, checksum failure, environment isolation, inactive services, locked dependencies and recording; added path/version/cleanup fixes |
| 3A — Onboarding | Compared directly with Pi5 `setup_wizard.py`, not its separate web coordinator; corrected guidance/reuse/retry/resume/summary and configuration boundaries |
| 3B — Web interface | Reviewed changed JSX/CSS/locale scope and control payload preservation; lint/build and 64 inert browser assertions pass without changing the bundle |
| 4 — Wiki relocation | Retains populated wiki and original immutable sources; no re-copy from Librarian or Pi5 |
| 5 — Integration | Launcher/checker/agent adapters reviewed; fixed standalone wiki uv discovery and project override isolation |
| 6 — Current knowledge | New complete dated manuals, README snapshot and audit evidence; exact reviewed semantic diffs and source-grounded page reviews; earlier evidence preserved |
| 7 — Validation | Local checks below; physical Pi, live accounts and remote CI remain pending |
| 8 — Publication | No commit, push or deployment; curl publication still pending |

## Pi5 onboarding consistency

Shared flow: branded welcome, ordered hardware steps, explanation/action/status text, saved-setting
reuse across all modules, individual tools, retry, Enter-to-continue, Q/save/exit, resume and summary.
Pi0 keeps display/buzzer/servo/distance and its existing import/identity/Gemini/ngrok settings.
It deliberately retains the approved READY warning for all Pi0 devices, multi-limb servo wording,
independent operator observations and manual server start. Pi5's two-wheel assumptions, extra
hardware/providers/MCP, simulation and launch controls are not imported.

## Local validation

- Python 3.11 locked root environment: 160 tests passed excluding the seven project-knowledge tests pending final document-map update; final combined result recorded below.
- Ruff checks/format, ShellCheck: pass for upgrade tooling/tests.
- Frontend lint/build: pass; isolated source and built output match the workspace exactly.
- Inert Playwright: 64 assertions pass at 360, 390, 844 and 1280 pixel widths; routes, locales, API payloads, WebSockets, focus return and shutdown cancellation checked. No backend/hardware ran.
- Core protection: 120 recorded source/test/metadata/lock files pass; original package-file comparison recorded below.
- Final knowledge/source/review/link/index checks are recorded below after new evidence is applied.

## Remaining acceptance

Run the README's physical checklist on Zero 2 W / Bookworm 64-bit, including fresh install and retry,
real calibration/cancellation, Gemini discovery, ngrok and first server start. No physical or account
operation was performed here. Pi0 retains its existing public-tunnel/control security model; it has
not acquired Pi5 pairing/authentication. Server start may move hardware and attempts ngrok; skipping
onboarding's token step does not promise offline isolation. These existing runtime boundaries were
documented without modifying core code.

Shell fixtures and host tests do not prove an OS package transaction, pigpio C build or npm build
will fit every microSD/RAM/network condition on a real Pi. GitHub CI and published curl acceptance
require publication and are not claimed as executed.

## Final audit gate results

- **168 root tests passed** on Python 3.11, including 20 added audit regressions. The final run includes cancellation after calibration changes; observations are reconciled before saving even when the operator interrupts the verification prompt.
- **61 wiki tests passed** in the independent wiki environment.
- **64 inert browser assertions passed**; frontend lint/build passed and output is byte-identical to the checked workspace bundle.
- **Ruff lint/format, ShellCheck, and diff whitespace checks passed.**
- **Knowledge check, strict wiki lint, links and indexes passed:** zero errors, warnings or suggestions; 26/26 sourced pages have current passing AI semantic reviews and remain draft/unverified. Three historical pending source versions are preserved; all five newly registered audit/manual/README sources were ingested.
- **323 original tracked robot package files are byte-identical** to the captured pre-upgrade baseline. The 120-file protected core/metadata gate also passes. All 18 original raw evidence files retain their bytes after relocation. Pi5 remains clean and unchanged.
- No robot service, hardware tool, live account or public tunnel was started during this audit. No Git commit or push was made.

The earlier local-validation paragraph records the intermediate checkpoint copied into immutable
raw audit evidence. These final results supersede its pending combined-test and knowledge-gate notes.
