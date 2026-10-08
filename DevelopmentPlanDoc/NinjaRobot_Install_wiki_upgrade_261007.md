# NinjaRobotPi0 installation, onboarding, wiki, and web UI upgrade

Date: 2026-10-07  
Status: **Owner approved; implementation completed on host. Final Raspberry Pi / live-account acceptance and publication remain pending.**  
Scope: installation tooling, interactive onboarding using existing robot tools, web presentation, documentation, wiki relocation, and developer/agent workflow.

## 1. Outcome and approval boundary

Provide a beginner-friendly curl installation entry point for NinjaRobotPi0 and move the embedded wiki from `Wiki/NinjaRobotPi0_Wiki/` to **`ninjarobot_pi0_Wiki/`**, preserving the exact capitalization requested. Align its operating model with NinjaRobotPi5: explicit environment setup, read-only retrieval, traceable current manuals, implementation-to-documentation checks, reviewed semantic updates, and reproducible validation.

Add a resumable terminal onboarding tool that guides the owner through Pi0's existing display, buzzer, servo, and distance-sensor tools, then Google Gemini and ngrok settings. Apply the existing Pi5 web design language to Pi0's Home, Agent, and Help interfaces. The added scope is orchestration and presentation; robot algorithms and control contracts remain unchanged.

The owner subsequently approved implementation with linting and validation. The approved installation, onboarding, wiki and presentation phases are implemented locally. Publication and physical operation remain separate. Existing user reviews are preserved on unchanged pages.

Preserve existing robot backend/driver source, Python package names, CLI commands, configuration formats and locations, GPIO mappings, calibration semantics, and BLE/REST/WebSocket contracts. New onboarding files may call existing tools/helpers after user selection. Pi0 web CSS, presentation markup, accessible labels, and locale copy may change under the newly requested UI scope; existing routes, API payloads, event handling, and robot control behavior must remain compatible. Leave the legacy `NinjaRobotV4` distribution identity and existing V4/V5 backend strings unchanged. No Pi5 files, Education website files, Librarian wiki copies, or Git remote/default-branch settings change in this task.

## 2. Confirmed decisions and scope interpretation

The owner supplied the following decisions after the interrupted planning session. These replace the earlier pending questions. Implementation was subsequently explicitly approved by the owner.

| ID | Decision | Confirmed direction | Implementation boundary |
| --- | --- | --- | --- |
| D1 | Supported device and OS | Raspberry Pi Zero 2 W with Raspberry Pi OS Bookworm 64-bit only | Other targets are rejected until separately qualified |
| D2 | Onboarding | Create an interactive tool similar to Pi5, reusing existing `pi0*` calibration tools and collecting ngrok/Google API settings | Installation remains non-actuating. Hardware tools and live account checks run only after the user selects their onboarding step; no unattended server start, boot autostart, or reboot |
| D3 | Manual authority | Full immutable versioned manuals inside `ninjarobot_pi0_Wiki/`, with short root manual pointers | Preserve existing public manual URLs without maintaining duplicate full manuals |
| D4 | Web UI brand consistency | Apply Pi5's existing UI style to Pi0's web interface | Preserve Pi0 capabilities and React routes; no Pi5-only camera, voice service, pairing protocol, or new movement feature is implied |

Already specified: use `ninjarobot_pi0_Wiki` exactly, retain robot code and Python package names, and prepare a phased plan before implementation. Existing public manual links must continue to follow the repository's default branch. No release tag/version has been requested.

“Google API” refers to the existing Google Gemini key/model workflow already present in Pi0. “Similar to Pi5” means guided terminal steps, clear progress, reuse/retry/exit, and consistent presentation; it does not add Pi5-only providers, camera, microphone hardware, MCP integrations, or its two-wheel calibration assumptions. UI alignment covers style and the organization of existing controls, not a new Game Pad feature. These interpretations satisfy the requested additions while preserving robot functions; no further requirement clarification is currently needed. The owner subsequently approved the revised implementation scope.

## 3. Review baseline and evidence

### 3.1 Repository and review coverage

Pi0 baseline commit: `3dbc41a4ee3cf9fb1019e3be5e633f5a6b47d862`. Pi5 reference commit: `d620fa4e790fd79c1b5d65bc2b95eb71625076cd`.

Pi0 has pre-existing modifications to `.serena/project.yml`, the source catalog, 21 curated wiki pages, and the wiki log. These include the owner's completed semantic review. Pi5 was clean during inspection. The surrounding Education repository contains unrelated changes and is outside the implementation allowlist.

The review inventoried all 610 tracked Pi0 files, all eight robot/root package manifests, both Python lockfile contexts, the frontend manifest/lockfile, agent adapters, wiki configuration/catalog, and test layout. Static AST inspection covered all 125 Python files outside the embedded wiki, including tests and samples, without importing robot modules; the repository contains 157 tracked Python files overall and 28 frontend source files. Focused Serena symbol/body inspection covered installation-sensitive configuration, CLI, HAL, web-server startup, service management, and source-sync behavior. Pi5 bootstrap, installer, wiki launcher, knowledge checker, workflow guidance, and relevant regression tests were inspected as reference implementations.

This is a repository-wide review of installation and wiki integration impact, extended with focused onboarding and UI inspection. Static inventory is not a claim that every robot algorithm has received a fresh functional/security certification. Runtime algorithms remain outside the change scope. No robot server, driver initialization, calibration command, package installation, or physical-device test was executed.

### 3.2 Wiki evidence and actual validation

| Evidence/check | Observed result |
| --- | --- |
| Pi0 `wiki_source_sync.py --check` | All 12 mapped project/source pairs match |
| Pi0 existing wiki `.venv/bin/llmwiki stats` | 21 pages, 14 sources; 21/21 sourced pages have passing semantic reviews |
| Pi0 existing wiki `.venv/bin/llmwiki lint --strict` | 0 errors, 0 warnings, 0 suggestions |
| Pi0 lifecycle/trust | All 21 pages remain `draft` and `unverified`; passing semantic review does not imply human verification or device qualification |
| Pi5 direct wiki search/stats | Installation/workflow pages retrieved; 11/11 sourced pages have passing semantic reviews, with draft/unverified lifecycle/trust |
| Pi5 `python3 scripts/verify_project_knowledge.py` | Pass: manuals, implementation mappings, adapters, and local links |
| Pi5 `python3 scripts/wiki.py search installation` | Blocked by sandbox access to the existing uv cache; used the already-installed wiki CLI directly, without installing dependencies |
| GitHub raw `HEAD` README check | HTTP 200; downloaded README bytes match local Pi0 README. No remote script was executed |
| Robot tests / Pi installation / installer tests | Not run for this plan-only task; the proposed Pi0 installer does not yet exist |
| Safe UI preview | Rendered Pi0 Home/Agent/Help from its tracked `dist` and Pi5 Agent/Game Pad/menu directly from `web_static`, at 390 × 844, using bundled Node Playwright and temporary localhost-only static servers. Backend/API actions were inert and WebSockets replaced with disconnected mocks; no robot backend ran |
| Preview limitations | Pi0's frontend dependencies are not installed locally; its tracked build was inspected alongside current JSX/CSS, not rebuilt. Screenshots establish a visual baseline, not source-build parity, live connectivity, or functional acceptance |

Pi0 primary pages consulted, relative to the old wiki root:

- `wiki/references/installation-and-wiring.md`: setup, pigpio, web build, and old wiki bootstrap location; sources include `src-20260822-installationguide`, `src-20260822-developmentguide`, and both 2026-10-07 migration evidence sources.
- `wiki/overview.md`: package architecture and current knowledge navigation; sources include `src-20260822-readme` and `src-20260822-developmentguide`.
- Related installation boundaries are mapped to `wiki/references/hardware-calibration-and-tools.md`, `wiki/references/api-and-cli-reference.md`, and the package entity pages; those must be checked again against exact changed claims during implementation.

Pi5 references: `ninjarobot_pi5_wiki/wiki/concepts/installation.md`, `wiki/concepts/development-workflow.md`, `wiki/references/installation-guide.md`, `docs/PROJECT_WORKFLOW.md`, and `project-knowledge.json`. Current installation/development evidence includes `src-20260923-installationguide-2`, `src-20260923-developmentguide-2`, and `src-20260907-knowledgeintegration`.

The Education PlatformWiki was queried directly and `wiki/concepts/development-workflow.md` inspected. It is draft/unverified guidance for preserving the separate robot-repository boundary. This Pi0 plan does not change browser contracts and requires no PlatformWiki content update by itself.

### 3.3 Code-backed findings

| ID | Finding and code evidence | Required response |
| --- | --- | --- |
| F1 | Pi0 has no tracked shell installer. `InstallationGuide.md` requires OS setup, pigpio, uv, Node, cloning, Python dependencies, and web build manually | Add a bootstrap and a checkout-local installer with clear stages and actionable failures |
| F2 | The example `github.com/.../install.sh` is not a raw-file download URL, and curl by itself only downloads | Publish raw-content commands with Bash execution, plus a download-inspect-run alternative; do not advertise the URL before the script exists remotely |
| F3 | Pi5 `install.sh` defaults to `public_v07`; its `scripts/install-rpi.sh` installs Pi5-only camera/audio/AI/PWM components | Reuse design patterns, not Pi5 defaults, dependencies, device checks, or hardware overlays |
| F4 | `ninja_core/src/ninja_core/web_server.py:lifespan` initializes HAL and BLE, calls `servos.center_all()`, starts distance monitoring, and schedules network/display setup | Installer and readiness checks must never start the server; a passing install is not hardware readiness |
| F5 | `ninja_utils/src/ninja_utils/service_manager.py:ServiceManager.install` writes and enables `ninjarobot.service`; it does not start it immediately. Its unit runs `uv run ninja_core server --autostart` on a later start/boot | Do not invoke startup installation by default; enabling it is still a future actuator boundary |
| F6 | `config.py:CONFIG_FILE_PATH` is `Path("config.json")`; import expects root `servo.json`, `buzzer.json`, and `pi0disp/display.json`. Driver defaults differ; servo CLI options explicitly default to `servo.json` | Run project commands from the checkout root; preserve all existing paths and files. Do not migrate configuration to Pi5's XDG layout |
| F7 | `init_tool.py:run_init_tool` can configure credentials, import hardware settings, select robot type, and launch the server | Reuse its public helpers from the new onboarding tool; retain the old menu unchanged. Never call its server action unattended or synthesize calibration |
| F8 | `web_server.py:WEBAPP_DIST` resolves to the sibling `ninja_webapp/dist`; local packages are installed editable through `[tool.uv.sources]` | Keep checkout layout and editable installation. Do not relocate packages or build output |
| F9 | Locked Vite/plugin engines require Node `^20.19.0 || >=22.12.0`. The guide uses a floating Node LTS setup script and `npm install` | Select and verify a supported exact Node version in the installer manifest; use `npm ci`, preserving the lockfile |
| F10 | Root packages advertise Python `>=3.9`; wiki tooling requires `>=3.11` and uv `>=0.11.0`; existing runtime code includes newer annotation syntax | Use explicit qualified interpreter selection, provisionally Bookworm Python 3.11. Keep robot metadata/lockfiles unchanged; do not promise Python 3.9 compatibility based only on metadata |
| F11 | The guide downloads pigpio `master.zip`, suggests ignoring a `make install` failure, and offers global `pip --break-system-packages` | Use reviewed pinned source/provenance, successful C-only installation, verified library loading, and the locked Python package in the robot venv. Never ignore a failed install or bypass system Python protections |
| F12 | `wiki_source_sync.py:main` hardcodes the old wiki root and overwrites registered raw mirrors with `atomic_copy` | Under confirmed D3, retire overwrite-sync behavior and replace its completion gate with immutable-version/pointer/fingerprint checks |
| F13 | Pi0 currently has no Pi5-style project knowledge map or root wiki launcher. Query skill examples use `uv run` without `--no-sync` | Separate explicit environment setup/preparation from read-only queries; queries must not download, synchronize dependencies, or rewrite source hashes |
| F14 | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, rules, skills, README, and DevelopmentGuide contain old wiki paths | Update active integration references together; preserve historical log/audit/source text |
| F15 | Root `.gitignore` only excludes four local configuration files. There are 192 tracked bytecode files and six tracked frontend build files | Add narrowly scoped ignores for new installer/wiki environments and state. Do not delete tracked legacy artifacts in this task. Run validation/builds in isolated copies to avoid rewriting them |
| F16 | Wiki `overview.md` says React 18, while frontend metadata declares React 19.2.0 | Correct this specific version claim in new evidence and affected pages; passing semantic review proves source support, not automatically agreement with current code |
| F17 | Current `raw/` hashes, source IDs, citations, and semantic-review hashes are consistent | Preserve them during the pure directory move. Only changed knowledge receives new sources and a new semantic review |
| F18 | Pi5's terminal wizard is `ninjarobot_pi5_agent/.../setup_wizard.py:run_setup_wizard`, not its separate remote-display `onboarding.py` coordinator | Reuse the terminal wizard's sequence/progress/console patterns; do not import its runtime coordinator or Pi5 hardware ownership implementation |
| F19 | Pi0 `pi0servo/.../cli/servo_tool.py:servo_tool` calls `startup_group.center_all()` before showing its menu when calibration exists | Show the movement warning and confirm the robot is physically supported before spawning the tool, even for a returning user |
| F20 | Several Pi0 tools catch initialization failures and return normally. `config.py:load_config` creates a file when absent; `import_and_update_config` substitutes default servo calibration if `servo.json` is missing | Exit code or file presence alone cannot prove calibration. Use read-only inspection for status; block import when required saved calibration is missing/invalid |
| F21 | Pi0's `init_tool.py:configure_gemini_api_key` already discovers models, asks for selection, validates, then persists. `ngrok_config.py:set_ngrok_auth_token` delegates to pyngrok | Reuse these helpers through new onboarding orchestration; do not introduce a second credential format. Token presence is not proof of account/network validity |
| F22 | Pi0 uses white/blue shell tokens and charcoal/coral chat styles. Pi5 uses a dark navy/cyan shell, rounded cyan-bordered panels, status pills, menu sheets, and an activity drawer | Adopt Pi5 tokens and component styling in Pi0's existing React/CSS-module architecture |
| F23 | Pi0 Home preview displays raw `home.systemTitle` and `home.sliderText` keys; these and shutdown labels are absent in all four source locale files | Fill presentation translations and accessible labels for all existing supported languages as part of the UI phase |
| F24 | Pi0 Header reports BLE advertising; Pi5 badge reports controller connection/ownership. Their control protocols differ | Preserve the meaning of Pi0 status labels and control requests; do not label BLE advertising as an authenticated/connected controller |

## 4. Proposed installation design

### 4.1 Public entry point and revision behavior

Planned convenience command, **usable only after implementation and publication**:

```bash
curl -fsSL https://raw.githubusercontent.com/NinjaRoboticsEducation/NinjaRobotPi0/HEAD/install.sh | bash
```

`HEAD` follows the remote default branch, preserving the earlier migration requirement. A branch-following command is mutable; also document a release/commit-pinned command using the same full commit in the raw URL and `--ref`. No tag is invented by this plan. Git's documented `ls-remote --symref` exposes remote HEAD and its target; resolve the selected revision once, record the commit, and execute the checkout-local installer from that verified revision. See [Git reference discovery](https://git-scm.com/docs/git-ls-remote) and [GitHub raw file viewing](https://docs.github.com/en/repositories/working-with-files/using-files/viewing-and-understanding-files).

The bootstrap must collect its implementation into complete function definitions and invoke its entry point only at the end, reducing partial-stream execution risk. Documentation should offer a download-to-file command joined with `&&`, inspection, and execution as the inspectable alternative; a failed download must not execute a partial file. HTTPS transport and a resolved commit provide different guarantees from an independently verified release signature; do not claim signature verification unless implemented.

Proposed interface:

| Option | Behavior |
| --- | --- |
| no options | Fresh install under `$HOME/NinjaRobotPi0`; resolve remote default HEAD; display actions and request confirmation through `/dev/tty` |
| `--install-dir ABSOLUTE_PATH` | Explicit new destination; reject an existing path, including dangling symlinks |
| `--ref REF` | Full SHA, published branch, or tag; disambiguate `refs/heads/...` and `refs/tags/...`; reject ambiguous short branch/tag names |
| `--dry-run` | Local preview only: no network calls, sudo, cache/log creation, downloads, or filesystem mutation; show unresolved revision/version checks honestly |
| `--check` | Read-only installed-software inspection; no bootstrap downloads, dependency sync, repair, hardware imports, or service activation |
| `--yes` | Explicit noninteractive acceptance of the displayed install scope; does not enable hardware/startup steps or grant sudo credentials |
| `--with-wiki` | Explicitly provision the independent wiki environment and text cache after robot software installation; ordinary robot users need not install wiki tooling |
| `--help` | Explain prerequisites, supported target, options, and excluded first-run actions without side effects |

Use separate internal bootstrap and checkout-install argument handling. In a verified local checkout, install that checkout as-is; reject bootstrap-only `--ref`/`--install-dir` options rather than silently ignoring them or switching a user's branch. A streamed script must not delegate to a lookalike `scripts/install-rpi.sh` in the current directory.

The no-network preview guarantee applies to the installer after invocation; fetching the script with curl is itself a network action. Users needing a fully offline preview run an already downloaded script. Reject conflicting modes such as `--check --dry-run` and reject unknown options before any side effect. Use distinct documented nonzero results for invalid arguments, unsupported targets, missing software, and failed installation; hardware-pending status alone must not masquerade as software-install failure or as full robot readiness.

Fresh bootstrap: validate options and platform/prerequisites, obtain consent before persistent changes, stage only under an owned private temporary directory, fetch the official repository, resolve/verify commit and required regular files, then move the checkout to a previously absent destination. Do not build a virtual environment before that move: absolute paths in virtual environments and editable installations would become invalid. A dependency-stage failure after publication leaves a recognizable incomplete checkout for explicit retry; never recursively delete an existing user's directory.

If Git is absent, its minimal, explicit prerequisite installation must happen before the fetch; the checkout-local stage cannot solve that bootstrap dependency. Display any additional system actions from the verified checkout before performing them. Reuse an acceptance already covering the exact displayed actions; do not treat download consent as approval for previously undisclosed OS changes. When an existing local checkout is used, record its dirty state and actual lockfile/tool-manifest hashes instead of falsely reporting that its files equal a pristine commit.

Check destination again before publication and guard concurrent installers with an owned lock. Test symlinked parents, spaces, special characters, missing parent directories, signals, failed downloads, and a destination created by another process. Do not follow untrusted file paths or arbitrary bootstrap repository overrides in the public interface.

### 4.2 Checkout-local software installation

Add `scripts/install-rpi.sh`, `scripts/install-versions.env`, and narrowly scoped helpers only where useful. Run as the normal user; use sudo solely for the reviewed OS operations. The first release must identify all network endpoints, download artifacts, checksums, licenses, and exact tool versions in a reviewed manifest. Select these during Phase 1 qualification; Pi5's version pins are reference evidence, not automatically Pi0-qualified versions.

Ordered stages:

1. Validate OS release, CPU architecture/userland, Zero 2 W model, available disk/memory, Bash, curl, certificates, Git, Python, and privilege availability. A clean supported OS may lack Git: include its installation in the explicit system-prerequisite stage, not an unexplained bootstrap failure after download. Document curl/certificates as initial prerequisites.
2. Show the exact apt packages, privileged file destinations, downloads, installation directory, and first-run actions still pending. Do not run a broad `apt upgrade`.
3. Install only required OS tools for Python/native builds, pigpio, and BlueZ/D-Bus support. Confirm package availability on the selected OS image; avoid guessing an untested universal list.
4. Install/reuse the reviewed uv and Node toolchains. Verify downloads before execution/unpacking; use user-owned paths where possible; avoid replacing unrelated globally installed tools. Record distro package versions separately from pinned tool artifacts.
5. Install the pigpio C daemon/library from a reviewed commit if the selected package source is unsuitable. Use a verified C-only build/install procedure or a small installer-owned helper, with bounded build jobs and explicit file ownership. Keep the Python wrapper in the locked robot environment. Do not copy the guide's partial-failure workaround.
6. Prepare a pigpiod service definition only after reviewing an existing service; preserve existing custom units and service state. Default software installation must not start or enable pigpiod, because starting it initializes GPIO. Document a separate deliberate hardware-preparation action. Require localhost-only daemon exposure for any installer-owned unit unless an approved requirement says otherwise.
7. Synchronize the existing robot lockfile into `<checkout>/.venv` using an explicitly selected interpreter and a production dependency selection. Prefer a lock-consistency check plus `uv sync --locked --no-dev`; if retaining Pi5-style `--frozen`, first validate lock consistency separately because frozen alone skips freshness checks. Preserve both metadata and lockfile bytes. See [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/).
8. Build the frontend using the selected Node and `npm ci` followed by `npm run build` from `ninja_webapp/`. Verify `dist/index.html` and referenced assets without launching FastAPI. Pi Zero 2 W memory pressure must be measured; do not silently create swap or claim a fixed completion time. If a build cannot fit, stop qualification and propose a separately reviewed artifact-based build strategy.
9. If `--with-wiki` is requested, call the explicit wiki setup and preparation path. The robot environment must not receive wiki packages.
10. Write a small installer-owned record of the resolved revision, selected tool versions, completed stages, and remaining steps. Log no environment dumps, tokens, or private config contents. Finish with the new local `./onboard.sh` command and a clear explanation that opening calibration tools can activate hardware. Installation success alone must not launch those tools.

Audit package-maintainer scripts as well as explicit installer commands: apt installation may start or restart services indirectly. Ensure the selected package procedure preserves existing robot/pigpiod service state and does not activate hardware as an incidental post-install action. Any temporary service-start inhibition must preserve an existing administrator policy and restore it even after failure; do not replace a user's policy file blindly. Include this behavior in disposable-image qualification and failure tests. If preservation cannot be guaranteed on a running robot, stop with a clear instruction to use a controlled maintenance session.

Under confirmed D2, interactive onboarding coordinates calibration, configuration import, and Gemini/ngrok settings. Interface configuration (I2C/SPI/UART), Bluetooth permissions, and pigpiod readiness are checked and explained before device tools open. Service activation, robot/server startup, boot autostart, and reboot remain separate explicit operator actions. Do not claim that software installation alone makes the robot ready to operate.

### 4.3 Readiness, retries, and recovery

`--check` should inspect package/distribution metadata, tool versions, lockfiles, entry-point files, expected web assets, daemon binary/library presence, OS identity, and installer state. It may report service/interface status without changing it. It must not import the web server, HAL, BLE service, or instantiate driver/config classes. A separate read-only report should distinguish software complete, hardware setup pending, and failed software checks.

Run read-only Python helpers with bytecode writing disabled and avoid commands that automatically initialize a cache, synchronize dependencies, or download an interpreter. Validate argument/environment isolation for these checks rather than assuming a command named `check` is side-effect-free.

Rerunning the checkout-local installer repairs only its owned software stages, preserves configuration, and never fetches/resets an existing checkout. Refuse replacement of unrelated files, existing launchers, or customized service definitions. Existing environments must be checked for ownership/interpreter compatibility before syncing. If their provenance is ambiguous, provide a concrete recovery path instead of deleting them.

Keep backups for privileged files actually changed and a record of newly installed components. Rollback cannot honestly promise to undo arbitrary apt upgrades/dependency changes; avoid broad upgrades and document the limited reversal procedure. Never automatically uninstall packages shared with other software. Concurrent runs must not corrupt environments or installation state.

### 4.4 Interactive onboarding using existing Pi0 tools

**New entry point:** `./onboard.sh`, backed by `scripts/onboard.py` and the installed robot `.venv/bin/python`. Resolve the checkout from the launcher, change to that root, and use installed entry points without dependency synchronization. This additive interface avoids editing existing `ninja_core`/`pi0*` code or package entry-point metadata. An optional user-local shortcut must use a Pi0-specific name and refuse to replace Pi5's `ninjarobot` launcher. The existing `uv run ninja_core init-tool` remains available unchanged.

Support normal interactive mode, `--resume`, `--step`, `--status`, `--dry-run`, and `--help`. Status/preview must not instantiate hardware, create default robot config, access Google/ngrok, or alter progress. Real onboarding requires a controlling terminal; do not consume the remainder of a curl script as answers. Do not offer a flag that bypasses actuator confirmation. Test paths with spaces and invocation outside the checkout.

The guided flow follows Pi5's numbered-step presentation, using Pi0 instructions and hardware:

```text
Welcome and saved progress
  -> prerequisites and robot identity/type
  -> display -> buzzer -> servos -> distance sensor
  -> review/import saved hardware settings
  -> Google Gemini key and model -> ngrok token
  -> readiness summary, save and exit
```

| Step | Existing Pi0 behavior to reuse | Completion and boundary |
| --- | --- | --- |
| Prerequisites | Inspect OS, installed software, terminal, existing service status, and required interfaces without opening devices | Explain corrective steps for unavailable pigpiod/interfaces. Detect a running robot server/service and require the operator to stop it before calibration; never silently stop another process |
| Identity/type | `set_robot_name`, `set_robot_type`, and current supported `tire`/`humanoid`/`spider` options | Preserve existing values unless the user deliberately changes them; use type-appropriate physical support instructions |
| Display | `pi0disp display-tool`; its Init action provides current setup, with existing display/test choices | Observe `pi0disp/display.json`; validate saved values and separately ask whether the displayed result was checked. No new display driver logic |
| Buzzer | `pi0buzzer buzzer-tool` | Warn before starting because it initializes the device; Init can beep. Inspect root `buzzer.json`; software validation and operator hearing confirmation are distinct |
| Servos | `pi0servo servo-tool --config <checkout>/servo.json` | The tool can center configured servos immediately. Before spawn, confirm clearance/support for all attached limbs/wheels and access to power removal. Never copy Pi5's GPIO12/13 or two-wheel neutral values |
| Distance sensor | `pi0vl53l0x sensor-tool` using its existing default config path | Preserve `pi0vl53l0x/src/pi0vl53l0x/config/vl53l0x.json`, also used by the existing driver/HAL path. Confirm a measured target and save result through the tool; do not silently relocate it to root |
| Hardware import | `ninja_core.config.import_and_update_config` through an isolated worker or existing CLI | First require validated saved inputs and show a sanitized before/after summary. Prevent the existing missing-servo fallback from being mistaken for calibrated hardware. Keep sensor settings in their current separate file |
| Gemini | `init_tool.configure_gemini_api_key` | Hidden input, existing model discovery/selection/validation, then existing persistence. Do not pass keys in shell arguments or print them. Explain live validation before selection; failure/cancel preserves prior settings |
| ngrok | `ngrok_config.has_ngrok_auth_token` and `set_ngrok_auth_token` | Hidden input and existing pyngrok storage. A token-presence check only reports configured/unverified. Saving may invoke/download ngrok; disclose that operation. Do not open a tunnel or start the robot to test it |
| Finish | Sanitized `build_robot_profile` from explicitly read/validated configuration | Show software/configuration/operator-check status separately; no automatic server, autostart, or reboot. Provide existing start instructions for a later deliberate action |

Use foreground subprocesses with inherited terminal I/O for the existing hardware tools. Allow one tool at a time and prevent concurrent onboarding writers. Handle cancellation, child failure, terminal restoration, and save-and-exit. A timed kill can leave PWM active; do not claim that killing a process guarantees safe hardware. Prefer the tool's normal cleanup, signal/wait on interruption, and give an explicit power-removal instruction if cleanup cannot be confirmed. Any discovered driver cleanup defect is a separately approved repair, not a silent expansion of this task.

Progress belongs in a private, installer/onboarding-owned file such as `${XDG_STATE_HOME:-$HOME/.local/state}/ninjarobot_pi0/onboarding.json`; this is new workflow state, not relocation of robot settings. Store step/version/result, non-secret file fingerprints, and timestamps, never credentials or full configs. Use atomic writes, restrictive permissions, containment checks, and a single-writer lock. Resume revalidates current saved inputs instead of trusting stale “complete” flags.

Offer **reuse saved settings**, **open tool**, **retry**, and **save and exit**. A valid saved config can be reused as software-validated; it does not prove physical calibration. Do not convert a simulation result, missing device, skipped step, zero exit status, or default-created config into a completed hardware check. Existing files take precedence over defaults.

Inspect JSON through read-only schema/range checks; avoid `load_config()` for status because it creates missing files. For deliberate updates, use existing public functions in a narrow worker boundary, preserve private backups, and validate the resulting file. Where helper cancellation/network behavior cannot provide safe preservation, stop that step and propose the smallest separate core change rather than changing robot code without review. Catch errors at the onboarding boundary with sanitized user messages; secret values must not enter progress, stdout/stderr logs, fixtures, or Git.

No key/model or token is mandatory merely to calibrate hardware. Users can skip/defer network-dependent steps and return later; completion summaries must show the corresponding AI or remote-access limitation. No Google Calendar, new provider, MCP server, camera, or microphone-hardware setup is added.

### 4.5 Pi5-style web presentation on existing Pi0 capabilities

**Design reference inspected:** Pi5 `ninjarobot_pi5_agent/src/ninjarobot_pi5_agent/web_static/{styles.css,agent.html,gamepad.html,app-shared.js}`. Pi0 targets are `ninja_webapp/src/index.css`, layout/common components and CSS modules, Home/Agent/Help pages, and four locale JSON files. Keep React, CSS modules, i18next, existing images/logo, and the current build stack; do not paste Pi5's HTML/JavaScript application over Pi0.

| Design element | Pi0 current baseline | Planned Pi5-derived treatment |
| --- | --- | --- |
| Canvas | White shell, saturated blue header | Navy `#03080c`, subtle `#06131b` gradient and cyan ambient accent; no remote font/image dependency |
| Text and accents | Dark body text, blue/coral controls | Light ink `#f2f6fa`, muted `#bdc4ca`, cyan `#00a3ff`; user bubbles `#1e5bc8`, assistant surfaces `#0a1c2c` |
| Semantic colors | Mixed local hardcoded styles | Green `#4de2a4`, amber `#ffc843`, danger `#ff526d`, power orange `#ff8a00`; pair color with text/icon state |
| Panels | Charcoal cards with heavy shadows | `rgba(6,19,27,.96)` panels, `rgba(0,163,255,.22)` borders, approximately 18px radii; modest shadows and optional inexpensive blur |
| Typography | Inter/system fallbacks with mixed scale | Preserve local Inter/system fallback family; use Pi5's compact cyan section labels and clear hierarchy, with readable body text and minimum 16px form text |
| Header/menu | Blue nav bar with mobile dropdown | Pi0 brand header, truthful status pills, cyan menu control, dark accessible menu sheet containing existing Home/Agent/Help and language choices |
| Conversation | Coral send button and user bubbles | Navy chat panel, blue user bubbles, bordered assistant bubbles, cyan primary action, existing text/voice-input behavior |
| Quick controls | Three selects with circular orange play controls | Consistent bordered rows for Expressions, Sounds, and Movements, retaining actual Pi0 options and action mappings |
| Activity | Black bottom log panel | Pi5-style cyan-accented bottom activity drawer; preserve Pi0 event content and current log behavior |
| Home/Help/power | Light hero/help and red power slider | Shared dark brand surfaces and Pi0 imagery; style the existing slide-plus-confirm power control distinctly without weakening either action gate |

The reference screenshots show Pi5's compact 600px-centered mobile controller. For Pi0, use a similarly focused Agent column (about 600–720px where content fits) and a wider readable Home/Help layout. Match the visual family while preserving all Pi0 controls. Do not blindly inherit Pi5's tiny text, whole-body overflow lock, fullscreen entry requirement, portrait-only blocker, or camera/voice/controller controls. Support mobile portrait, landscape, desktop, zoom, and on-screen keyboards.

Proposed Agent arrangement:

```text
Pi0 brand       BLE/status text       Menu
Distance telemetry (existing mm units)
Conversation panel and existing composer
Expressions / Sounds / Movements controls
Bottom activity drawer
```

Route/capability preservation matrix:

| Pi0 surface | Preserve | Do not import from Pi5 |
| --- | --- | --- |
| `/` | Home navigation, robot identity imagery, shutdown slider plus confirmation | A replacement Game Pad landing route |
| `/agent` | Chat POST to `/api/agent/chat` with existing message/language payload, browser speech input, `/ws/distance`, `/ws/events`, existing action selectors | Pi5 WebSocket ownership/pairing protocol, AI motion arming, camera actions, USB microphone service, resume/emergency endpoints |
| Quick controls | Existing expression/sound/movement list and action endpoint paths, units, selected values, execution handlers | New continuous-drive D-pad semantics or invented movement names |
| Header | `/api/ble/status` means advertising, not client connection | Pi5 controller-owned/connected status presented without Pi0 evidence |
| `/help` | Existing help route and verified Pi0 instructions, with new onboarding/manual navigation | Pi5 instructions that claim unavailable Pi0 features |
| Power | `/api/system/shutdown` only after existing deliberate gesture and confirmation | Unconditional one-click power-off or Pi5 deployment permission assumptions |

Use a coherent token mapping instead of a late CSS override layer. Update all component styles so light backgrounds/hardcoded coral colors do not remain accidentally. Add missing English, Japanese, Traditional Chinese, and Simplified Chinese labels; retain resource filenames and supported language codes. Label icon-only controls and status changes, make the menu/dialog keyboard-operable with focus restoration/Escape handling, respect reduced motion, provide visible focus, and verify contrast. Do not silently change business logic while fixing presentation.

Before implementation, record existing handlers/payload fixtures. Afterward, compare request method/path/body and WebSocket event handling under mocks for every preserved action. CSS/markup may change, but voice permission remains user-triggered and a visual element must never send a robot command merely because it mounts, gains focus, opens a menu, or changes language.

Browser acceptance covers 360/390px mobile, a short landscape viewport, tablet, desktop, and 200% zoom; all four languages; long chat/log entries; missing API key/offline/error/loading/empty capability states; menu focus; activity drawer; keyboard reachability; and power cancellation. Automated tests use inert API/WebSocket fixtures and mocked speech APIs. Any live microphone, robot action, or shutdown test remains separately controlled.

Preview evidence for this plan is limited to the current UI, not a mockup of the future implementation. Screenshots were saved temporarily during review; reproducible before/after source-build screenshots and design sign-off belong to the UI implementation phase. No Pi0 or Pi5 frontend source was modified to create the baseline previews.

## 5. Proposed wiki and documentation design

### 5.1 Target layout

```text
NinjaRobotPi0/
├── install.sh
├── onboard.sh
├── scripts/
│   ├── install-rpi.sh
│   ├── install-versions.env
│   ├── onboard.py
│   ├── wiki.py
│   └── verify_project_knowledge.py
├── AGENTS.md / AGENT.md / CLAUDE.md / GEMINI.md
├── .agents/skills/ and tool adapters
├── InstallationGuide.md             # compatibility pointer under confirmed D3
├── DevelopmentGuide.md              # compatibility pointer under confirmed D3
├── DevelopmentLog.md                # compatibility pointer under confirmed D3
├── ninja_webapp/src/                # Pi5-style presentation; Pi0 contracts retained
├── ninjarobot_pi0_Wiki/
│   ├── README.md / AGENTS.md
│   ├── project-knowledge.json
│   ├── docs/PROJECT_WORKFLOW.md
│   ├── raw/                        # old registered evidence preserved
│   │   ├── articles/ninjarobotpi0/<version>/
│   │   ├── notes/ninjarobotpi0/<version>/
│   │   └── _catalog/
│   ├── wiki/                       # existing page slugs preserved
│   ├── src/llmwiki/ / schemas/ / tests/
│   └── pyproject.toml / uv.lock / llmwiki.yaml
└── DevelopmentPlanDoc/NinjaRobot_Install_wiki_upgrade_261007.md
```

Keep the wiki embedded in the existing Pi0 Git repository. Do not create a nested Git repository, submodule, separate GitHub wiki, or second canonical Librarian copy. Pi5 uses lowercase `ninjarobot_pi5_wiki`; the Pi0 spelling above intentionally follows the user's request. Validate exact case on Linux.

### 5.2 Preserve the completed semantic review

Separate the physical move from knowledge changes. Capture a file/hash manifest of the **working tree**, not just HEAD, and move the populated wiki with its current reviewed content. Preserve source IDs, original raw bytes, catalog hashes, page slugs, review metadata, unknown frontmatter, assets, and history. There must be no active writer/transaction during the move.

Ignored `.venv`, derived caches, and `.llmwiki` plans/backups need explicit handling. Preserve the owner's plans/backups privately, without adding them to Git. Do not treat a moved virtual environment as portable: its scripts/editable paths can retain the old absolute location. Recreate the wiki environment at its final path only in the later approved setup phase. A clean clone must work without any local environment/cache from before the move.

Do not globally replace old paths in historical raw sources or logs. Update current navigation and policy links; classify historical references as provenance. A root-folder relocation alone should not invalidate page/source hashes. Where an active curated page mentions the obsolete workflow/path, update it through a semantic plan using new evidence and review that changed page again. Preserve valid review records on untouched pages.

### 5.3 Manual authority and compatibility under confirmed D3

Create new complete dated versions of InstallationGuide, DevelopmentGuide, and DevelopmentLog inside the wiki. Preserve all old registered sources unchanged. Root README remains an onboarding/navigation entry point with direct links to current manuals. Package READMEs remain at their existing locations because package metadata can reference them; use concise package onboarding/API pointers and register new immutable snapshots when their content changes.

Keep `ProjectUpgradePlan.md` and `WikiIntegrationWorkflowPlan.md` as historical planning evidence, not continuously updated setup authorities. The new plan is also a decision artifact rather than a replacement manual.

The short root InstallationGuide and DevelopmentGuide files preserve existing Education website URLs using `blob/HEAD`. They point readers to the current full manuals; Markdown pointers do not implement an HTTP redirect. Audit known fragment links and retain useful anchor aliases where needed. These compatibility pointers are a deliberate Pi0 exception to Pi5's removal of root manual files. They must contain no duplicated installation procedure or competing technical authority.

All three existing documentation languages—English, Japanese, Traditional Chinese—must receive consistent installation/workflow changes. Do not rewrite unrelated historical text or silently drop sections when making a new complete manual version.

The owner selected wiki authority. Do not retain a parallel root-manual editing workflow or overwrite registered provenance just to make a check pass.

### 5.4 Launcher and knowledge map

Adapt Pi5's `scripts/wiki.py` to resolve roots from its own file, independent of CWD. Support:

```text
python3 scripts/wiki.py setup
python3 scripts/wiki.py prepare
python3 scripts/wiki.py check
python3 scripts/wiki.py search "installation"
python3 scripts/wiki.py source status
python3 scripts/wiki.py lint --strict
python3 scripts/wiki.py link check
python3 scripts/wiki.py index check
python3 scripts/wiki.py stats
```

From the wiki directory, the equivalent prefix is `python3 ../scripts/wiki.py`. `setup` is the only dependency-provisioning command. `prepare` rebuilds ignored text evidence from unchanged registered sources; it must refuse source-hash drift and must not refresh catalog fingerprints. Query/check commands are read-only, use the existing wiki interpreter/environment, and return actionable setup instructions if unavailable. Remove inherited robot `VIRTUAL_ENV`/`UV_PROJECT_ENVIRONMENT` contamination. Avoid unnecessary cache access in read-only commands where direct execution suffices.

Preparation must validate source containment, symlinks, expected formats, catalog/source changes during execution, and concurrent writers. Stage before publishing derived output; on partial failure leave a clear retryable condition without corrupting tracked sources. Root-level `check` should use standard-library-only code where practical. Avoid importing robot packages anywhere in wiki tooling.

`project-knowledge.json` follows Pi5's conceptual fields: schema version, reviewed checkout/context, reviewer/date, current documents/source IDs/hashes, previous version pointers, implementation files and their topic pages, adapters, link documents, integration status, and review notes. Add explicit reviewed exclusions where appropriate. Cover Pi0's seven packages, robot frontend sources, install/workflow scripts, and package metadata; classify tests/assets separately. Exclude generated output, bytecode, node_modules, environments, private calibration/config, caches, and immutable history from current implementation drift scanning.

Use a defined candidate-file inventory, including new relevant files, instead of indiscriminately walking every file as code. Detect added, deleted, renamed, and changed implementation files and stale adapter/manual pointers. A hash match means the mapped bytes were reviewed, not that every behavior is proven or documentation is automatically correct. Do not mark the map ready until all required semantic updates and reviews pass. Never regenerate hashes merely to silence CI.

Replace the old mirror completion gate atomically with this new gate when authority changes. Preserve a clear diagnostic for obsolete `wiki_source_sync.py --sync` invocations; it must not silently resume overwriting immutable sources. Decide whether to retain a read-only compatibility entry point or remove it after updating every caller; include tests for the chosen behavior.

### 5.5 Agent/developer workflow

Update Pi0 root `AGENTS.md`, its `AGENT.md` adapter, `CLAUDE.md`, `GEMINI.md`, `.agents/rules/ninjarobot-development.md`, `.cursor/rules/ninjarobot-development.mdc`, root skills, legacy workflows, and Claude wrappers. Update nested wiki README/AGENTS/tool adapters to point to `../AGENTS.md` and the root launcher correctly.

Retain existing root `robot-wiki-query` and `robot-wiki-maintain` names as stable workflow entry points; rewrite their authority, paths, and commands. Adapt `project-documentation`, `pi-validation`, and the documentation/completion references in `pi0driver-development`. Add a Pi5-style `ninjarobot-knowledge` overview skill and uniquely named root `ninja-wiki-*` wrappers only if they simplify discovery; nested canonical `wiki-*` procedures remain the single procedural source. Do not create conflicting duplicate skill names or copy Pi5 runtime policies into Pi0.

Required development sequence:

1. Read root policy, knowledge map, relevant pages/manual versions, and their trust/review state.
2. Verify behavior with Serena/code/tests; identify installation, contract, documentation, and hardware impact.
3. Obtain approval for a concrete phased implementation plan.
4. Implement and validate only that scope.
5. Create new immutable evidence/manual versions; register and normalize them explicitly.
6. Prepare schema-v2 page changes with current hashes; validate and show the exact semantic diff. Apply only with authorization covering that diff/scope.
7. Review changed sourced pages honestly; never fabricate human verification or retain stale passing reviews.
8. Update current pointers and implementation mappings after evidence review; run knowledge, lint, links, indexes, and isolated tests.
9. Report software checks separately from controlled Pi validation and any remaining publication steps.

Read-only questions never trigger setup, normalization, source registration, sync, or hardware commands. Imported commands remain untrusted evidence. For a genuinely documentation-neutral change, record the specific reason rather than creating meaningless source churn.

## 6. Phased implementation plan

### Phase 0 — Confirm design and protect the baseline

Record confirmed D1–D4 and obtain approval of this revised implementation plan. Recheck Git state in Pi0 and Pi5; inventory pre-existing dirty/untracked files, local wiki plans/backups, and ignored environments without collecting secrets. Capture hashes for protected backend/driver/lockfiles and for the owner's reviewed wiki working tree. Capture current frontend source/build evidence and request fixtures separately because presentation files are intentionally changing. Record exact current source/page/review state.

**Gate:** agreed OS/system-action/manual-authority matrix; 12 mirror matches and strict wiki lint baseline retained or any later user edits explained. No hidden reliance on an uncommitted local wiki environment.

**Rollback:** no implementation yet; retain the current checkout and private baseline evidence. No stash/reset or automatic commit of the owner's work.

### Phase 1 — Qualify installer inputs and define contracts

Prepare the installer option/exit/status contract, dependency manifest, provenance/licenses, minimum resource checks, privileged-action table, and retry/rollback rules. Verify locked dependencies on a clean supported image or isolated qualified target. Select exact uv/Node/pigpio inputs and checksum verification. Resolve missing Git/curl bootstrap prerequisites and Python interpreter policy. Measure the frontend build on Zero 2 W before committing to its delivery strategy.

**Files:** new `scripts/install-versions.env`, installer design/validation evidence under `docs/validation/`, proposed installer tests/fixtures. Do not change runtime package manifests or locks to make qualification pass.

**Gate:** every download/tool source is identified and verified; dependencies and frontend build fit the support matrix. Any required runtime/dependency change returns to the owner as a separate proposal.

**Rollback:** discard only new installer qualification artifacts from this phase; no installed-system rollback is required for host fixture tests. Preserve device qualification logs separately.

### Phase 2 — Implement and test bootstrap in isolation

Add root `install.sh` with default-HEAD resolution, exact-ref selection, local-checkout handling, staging, containment, cleanup, concurrency control, terminal confirmation, dry-run/check/help, and failure propagation. Test against local temporary Git remotes and an inert delegated installer, following Pi5's real-Git fixture approach.

**Tests:** default branch renamed after first run; branch names with slashes; annotated/lightweight tags; full SHA; branch/tag ambiguity; unpublished/missing ref; missing required files; invalid options; piped stdin; no TTY; explicit `--yes`; hostile lookalike CWD; existing/symlinked destinations; destination race; signal interruption and network failure; detached verified revision; bootstrap/installer version compatibility.

**Gate:** `bash -n`, ShellCheck if available/approved in CI, and isolated bootstrap tests pass. Preview/help/check execute no mutating tool. Fixture tests never contact GitHub or use sudo.

**Rollback:** remove/revert only phase-owned bootstrap files/commits; preserve user work and existing installation directories.

### Phase 3 — Implement checkout-local installation and read-only checks

Add software stages from section 4.2 and an installer-owned verification helper if needed. Add dry-run output that shows actual selected versions/paths, explicit privileged steps, and hardware actions still pending. Add targeted `.gitignore` entries for new environments/state; do not untrack legacy bytecode or frontend output as incidental cleanup.

**Tests:** fake apt/sudo/curl/uv/npm/systemctl commands with an invocation log; root/unsupported-platform rejection; checksum mismatch; lock inconsistency; missing/incorrect Node; pigpio build/library failures; partial install; second-run idempotence; preserved config/calibration/service bytes; ownership conflicts; interrupted writes; no secret logging; no robot/hardware startup. Verify builds and regression tests in isolated copies so tracked artifacts remain unchanged.

**Gate:** no failed step is swallowed; install/check reports distinguish software success from hardware pending. No `pip --break-system-packages`, broad OS upgrade, robot server, autostart enable, GPIO initialization, or private configuration overwrite occurs in default installation.

**Rollback:** use phase-owned file backups/state; preserve checkout and private config on failure. Explain manual recovery for packages already installed rather than promising an atomic OS rollback.

### Phase 3A — Add guided onboarding without modifying robot drivers

Implement section 4.4 in new `onboard.sh` and `scripts/onboard.py`, with new focused tests such as `tests/test_onboarding.py` and temporary config/process fixtures. Follow Pi5's injectable console/progress approach while preserving the existing Pi0 tools and public settings helpers. Installation hands off to the new local command without launching hardware. Add private workflow-state ignores where needed.

**Risk:** hardware can activate when a selected child tool starts; Gemini/ngrok steps involve credentials and external services. Automated tests must fake child tools and network helpers.

**Tests:** arbitrary CWD; no terminal; help/status/preview with no writes/imports/network; first run; resume after interruption; changed saved config; reuse; missing/invalid/empty calibration; missing servo config must block default-based import; each child tool launch/path/argument order; failure returning zero; nonzero exit; prompt cancellation; no concurrent tool/writer; Ctrl-C/EOF cleanup; robot type retained; simulated/unchecked states not promoted to physically checked; private atomic progress file without secrets; Gemini discovery/validation failure preserving prior key/model; ngrok failure preserving prior settings; token presence labeled unverified; denied/deferred account setup; no server/autostart/reboot launched at completion.

**Gate:** backend and all `pi0*` source hashes remain identical; every physical action is preceded by the correct Pi0-specific warning/selection; config import never treats manufactured defaults as successful calibration. A saved outcome accurately distinguishes software validation, explicit operator observation, incomplete, and failed checks. The wizard works with the actual existing CLI options and config locations.

**Documentation:** installation steps, command reference, prerequisites, reuse/resume behavior, secrets handling, physical precautions for each robot type, and unfinished-step recovery. Explain the sensor's separate configuration file instead of claiming `import-all` imports it.

**Rollback:** remove/revert only the additive onboarding files and owned shortcut/state. Never delete existing config or roll back calibration automatically; restore a private backup only on explicit selection after checking for newer user changes. No credential contents enter version control.

### Phase 3B — Align Pi0 web presentation with Pi5

Implement section 4.5 in `ninja_webapp/src/index.css`, layout/common CSS modules and presentation JSX, `pages/Home/`, `pages/Agent/`, `pages/Help/`, and `locales/{en,ja,zh-tw,zh-cn}.json`. Use a small shared token vocabulary with Pi5-derived values. Keep `App.jsx` route definitions and existing transport/action handlers functionally unchanged; permit only necessary presentation wiring and accessible menu interactions. No new frontend runtime dependency or lockfile change is planned.

**Risk:** presentation regressions can hide controls, obscure state, or make robot actions easier to trigger. Preserve shutdown gesture/confirmation and distinguish BLE advertising from connection. The design reference is Pi5's current UI, not a new branding concept.

**Tests:** build the current source in an isolated locked environment, then use inert API/WebSocket/speech fixtures for route/menu/language navigation, payload comparisons, chat states, action selection, telemetry units, log drawer, shutdown cancellation, and no command on mounting/focus. Run frontend lint/build plus focused regression/browser tests. Check all four languages, missing-key detection, keyboard/focus/Escape behavior, contrast, reduced motion, long text, mobile keyboard, responsive layouts, and zoom. Record before/after screenshots from the same fixtures and viewports.

**Gate:** consistent Pi5 visual family across all Pi0 pages; no raw translation keys; no copied Pi5-only controls; existing control request/response contracts preserved; no overflow or obscured critical controls at the acceptance sizes. Show the rendered result for design review before calling the UI phase complete. Do not count the current tracked-build previews as testing the new source.

**Build delivery:** Pi0 currently tracks six `ninja_webapp/dist` files. Generate any intentionally published new UI artifacts through the locked build after source review; do not hand-edit bundles. Record source commit/build inputs and review only expected generated changes. Avoid shipping old tracked assets alongside new source. If the release relies entirely on installer builds, explicitly document that delivery decision and keep clean-clone/installed-UI tests consistent; do not silently change artifact policy or mass-untrack files.

**Documentation:** new Pi0 UI guide/presentation evidence, screenshots with mocked/live context labeled, locale/style conventions, and the exact unchanged robot APIs.

**Rollback:** revert the coherent UI source and any intentionally generated build as a unit. Preserve unrelated frontend work, API behavior, language preferences, and robot/user configuration.

### Phase 4 — Relocate wiki without altering knowledge

Move the current populated wiki to `ninjarobot_pi0_Wiki/`. Update active path references and ignore rules. Preserve raw/catalog/page bytes during the pure-move checkpoint; isolate intentional navigation/policy changes from evidence changes. Check all root-relative paths and tool adapter resolution after the one-level shallower move. Preserve local transaction history privately; explicitly recreate the environment later.

**Gate:** every tracked old wiki file has an accounted-for destination; unchanged source/page hashes and semantic reviews match baseline; no nested Git repository or duplicate canonical wiki exists. Linux case-sensitive path checks pass. No raw-source global replacement.

**Rollback:** reverse the directory mapping and phase-owned path edits using the captured working-tree baseline, preserving later user edits. Do not restore old HEAD over the owner's semantic reviews.

### Phase 5 — Integrate launcher, knowledge map, skills, and authority

Add `scripts/wiki.py`, `scripts/verify_project_knowledge.py`, `project-knowledge.json`, `docs/PROJECT_WORKFLOW.md`, and regression tests. Complete the agreed D3 manual migration, current README links, root compatibility pointers, and retirement of overwrite-sync. Update every adapter/skill/completion rule as one coherent change.

**Tests:** root/wiki/arbitrary CWD; paths with spaces; missing environment; contaminated environment variables; query offline/no writes; source drift refusal; symlink/path escape; concurrent writer; interrupted prepare; current-versus-historical source separation; missing/renamed/new code classification; broken manual anchors; wrong adapter relative target; stale public manual pointer; clean clone without `_derived` or `.venv`.

**Gate:** knowledge check detects meaningful drift without scanning generated/private files. Queries perform no setup/sync. Old raw bytes remain unchanged; current docs have one authority. Static adapter checks and actual editor discovery checks are reported separately.

**Rollback:** revert the complete authority/adapter/map change together, not individual pointers. Keep new registered source versions as provenance if already published; update current pointers through a reviewed forward correction when necessary.

### Phase 6 — Update and review canonical knowledge

Create new dated implementation evidence and complete manual versions reflecting the verified installation and workflow. Register/normalize new sources. Prepare schema-v2 plans with current target/source hashes. Validate and display the exact diff, then apply within approved scope and review each changed page.

**Existing pages expected to change:**

- `wiki/overview.md`: new navigation/installation workflow and verified frontend version claim.
- `wiki/references/installation-and-wiring.md`: installer versus hardware preparation, supported target, pigpio guidance, new wiki location.
- `wiki/references/hardware-calibration-and-tools.md`: onboarding sequence, tool-start side effects, reuse/resume, configuration verification, and explicit startup boundary.
- `wiki/references/api-and-cli-reference.md`: additive installer/onboarding/wiki commands clearly separated from unchanged robot CLI commands.
- `wiki/entities/ninjarobot-v5.md`: preserve slug; update current project install/wiki navigation.
- `wiki/entities/ninja-webapp.md`: Pi5-derived presentation, existing Pi0 routes/controls, localization, accessibility, and locked build facts.
- `wiki/entities/ninja-core.md`: existing init/config helper roles and their new onboarding caller, without claiming core runtime changes.
- `wiki/analyses/development-history-and-evolution.md`: append the implemented workflow milestone without rewriting history.

**New pages:** `wiki/concepts/development-workflow.md`, `wiki/concepts/guided-onboarding.md`, `wiki/concepts/web-interface-design.md`, `wiki/references/installation-guide.md`, and `wiki/references/development-guide.md`, providing concise cited entry points. Index/log outputs are generated/appended through the wiki CLI, not hand-edited.

Other existing pages containing old path claims must be classified: preserve historical statements; update current guidance only with evidence and a new review. Do not unnecessarily rewrite all 21 pages or reset their review status.

**Gate:** normal and strict lint, links, indexes, stats, knowledge checks, and representative searches pass. Preserve 100% current review coverage for sourced pages, including added pages. Lifecycle/trust remain honest. Historical raw files remain byte-identical.

**Rollback:** use wiki transaction recovery for applied page changes, then restore reviewed map/navigation pointers consistently. Preserve later edits and evidence history; no blanket repository reset.

### Phase 7 — CI, clean-clone acceptance, and controlled Pi qualification

Add CI for installer/onboarding shell and process-fixture tests, frontend lint/build/mock-browser tests, and independent wiki validation, using pinned action revisions, minimal read permissions, and no device/cloud credentials. Linux is the installer/onboarding execution target; wiki portability can cover Linux/macOS/Windows, with appropriate interpreter paths and separate environment setup. Keep wiki pytest and robot pytest in separate processes to avoid test-name/import collisions.

Run the existing relevant robot tests with mocked hardware in an isolated copy and the frozen dependency context, grouping driver suites separately. Verify byte equality of protected backend/driver sources and locks; verify functional request/event parity for intentionally restyled frontend files. Run all new workflow/installer/onboarding/UI tests. Do not broaden this into runtime cleanup when unrelated baseline tests fail; report those failures and their scope.

On a separately authorized Zero 2 W test device, perform a fresh software install, rerun, failure/recovery test, and read-only check with actuator power isolated. Record OS image/version, architecture, Python/Node/uv/pigpio versions, resolved Git commit, duration, disk/memory peak, sudo actions, logs, and remaining interface/service setup. Hardware bring-up, calibration, server start, BLE advertising, and movement each require an explicit controlled procedure and operator authorization.

Then qualify the interactive onboarding sequence with an operator at the supported device: exercise existing calibration tools, save/exit/resume, intentional failure, and optional Google/ngrok setup with the owner's account only when authorized. Verify the new web presentation on a phone using mocked service data first, then perform only explicitly selected live actions. Do not retain account secrets or label network/device tests passed from fixtures alone.

**Gate:** clean clone has zero tracked source changes after wiki preparation/query/checks; full installer succeeds on the supported device without running robot functions. Hardware acceptance is reported as pending unless actually performed. A clean software CI run is not permission to label physical operation tested.

**Rollback:** restore test-image/system-file backups or remove only installer-owned artifacts as documented. Preserve saved calibration/private files and unrelated software. No production/device-wide rollback command is run automatically.

### Phase 8 — Review and publication handoff

Present changed-file scope, protected-source comparison, exact test results, wiki source/page/review status, unresolved OS/device limitations, and finalized public commands. Publication/commit/push approval is separate from this plan-only request. After authorized publication, verify the raw installer endpoint, default-branch navigation, and root compatibility manual URLs. Test default-branch switching in a fixture repository rather than changing the production repository solely for a test.

**Gate:** no placeholder versions/checksums or unimplemented advertised commands; no claims of unperformed device validation; no changes to Pi5 or the Education website. The public curl command must retrieve the published installer successfully before being presented as ready for users.

## 7. Validation matrix and completion criteria

| Area | Host/fixture gate | Real-device or interactive gate |
| --- | --- | --- |
| Bootstrap | Real temporary Git remotes, renamed default branch, exact commit, bad refs, path/concurrency/TTY/failure cases | Official endpoint download and target-device invocation after publication approval |
| Dependencies | Manifest/hash failures, lock freshness, command-order/privilege mocks, no mutation in preview/check | Bookworm 64-bit packages, Python dependency install, pigpio binary/library, Node build under Zero 2 W resource limits |
| Runtime preservation | Backend/driver hashes; unchanged package identity/config/API/GPIO; frontend request/event parity and isolated regression tests | Separately authorized existing-function acceptance |
| Hardware boundary | Installer/preview/status reject hardware actions; onboarding requires explicit step selection and validated inputs | Operator checks calibration and interruption safely; no unattended server/autostart/reboot |
| Onboarding | Fake TTY/child tools and account helpers; save/reuse/resume/error tests; no secrets in logs/state | Existing Pi0 calibration tools and authorized Google/ngrok settings on Zero 2 W |
| Web presentation | Pi5 token mapping, four locales, route/API parity, mocked browser tests, responsive/accessibility screenshots | Phone/desktop design review and separately authorized live control checks |
| Wiki relocation | File mapping/raw/page/review hashes; case-sensitive paths; adapter links | Open root and wiki-only workspaces in supported editors |
| Wiki lifecycle | Setup isolated; prepare writes only ignored derived evidence; queries/check read-only; drift fails | Editor rule/skill activation verified, without implying static tests prove activation |
| Documentation | Current manual/map/source consistency; translations; anchors; default-branch compatibility links | Beginner follows installation instructions on the qualified image |
| Recovery | Interrupted stages, reruns, preserved dirty/config files, symlinks, simultaneous writers | Test system-file restore procedure on a disposable image |

The implementation is complete only when all approved installation/onboarding/UI/wiki phases pass their gates, protected robot backend/driver code remains unchanged, Pi0 control contracts are preserved, the owner's prior review work is retained, updated sourced pages have current honest semantic reviews, and any unperformed device/publication steps are explicitly listed. D1–D4 are resolved requirements. Do not make physical-validation or release-readiness claims solely from this plan.

## 8. File impact allowlist and exclusions

**Expected new/changed areas:** root installer/onboarding launchers; new `scripts/` helpers; focused installer/onboarding/wiki/UI tests; CI workflow files; targeted ignore entries; Pi0 frontend CSS, presentation JSX, locale files, and intentionally generated UI build artifacts; root policy/adapters/skills; root README/manual pointers; relocated wiki integration files, new evidence/manual versions, approved curated-page changes, and this plan/validation evidence.

**Protected existing files:** all runtime `.py` files beneath the seven robot packages, existing robot package metadata and `uv.lock`, frontend `package.json`/`package-lock.json`, models/assets, runtime service-manager code, and existing raw evidence bytes. Existing calibration/config files are never changed by repository tests or migration; the future onboarding tool may update them only through deliberate user-selected existing setup functions. Frontend source is now presentation-editable, but API/event handlers and route contracts are protected behavior. Add focused tests rather than rewriting runtime expectations.

**Generated artifacts:** installer use on a target creates `.venv`, node_modules, and frontend build output. Validate in isolated copies and inspect Git diffs explicitly. Permit only intentional, reproducible UI build output under Phase 3B; do not commit incidental bytecode regeneration or a mass untracking cleanup.

**Outside scope:** Pi5 changes; robot algorithms/driver refactors; new control protocols or Pi5-only features; adding external accounts/providers; live credential entry during this planning task; auto-update service; new release tag; remote/default-branch migration; Librarian-copy synchronization; Education website deployment. Future owner-selected existing Gemini/ngrok setup is explicitly in onboarding scope. Existing website manual URLs stay valid through the confirmed root pointers. If external workflow consumers require new canonical wiki paths, list their exact changes for a separate reviewed cross-repository follow-up rather than silently changing them here.

## 9. Historical planning-task handoff (superseded by approved implementation)

Completed: repository inventory and installation/wiki-impact review, Serena inspection, Pi5 comparison, Pi0 mirror/strict-lint/review baseline, Pi5 knowledge check, raw default-branch README URL verification, and this phased draft.

Interruption recovery check: the draft was present and complete; all 610 previously hashed tracked Pi0 files still matched the planning baseline. `install.sh` was absent, the old wiki directory remained present, and the proposed new directory was absent. Only the untracked plan document was added during this planning task. A second plan review clarified Git bootstrap ordering, indirect package-service activation, read-only cache/bytecode behavior, and the difference between previewing a local script and downloading it first.

Latest revision: D1 (Bookworm 64-bit) and D3 (versioned wiki manuals/root pointers) confirmed; D2 expanded to interactive Pi0 onboarding; D4 added Pi5-style web presentation. Inspected both web designs, safely rendered their current interfaces, and added dedicated onboarding/UI design, compatibility, validation, documentation, and rollback phases. No requirement question remains pending.

At the planning checkpoint, pending: owner review/approval before implementation; then installer/toolchain qualification, onboarding/UI development, tests/CI, wiki relocation and source/page updates, controlled device validation, and authorized publication. Only this plan file changed during planning; existing robot functions, frontend source, and the owner's semantic reviews remain untouched.


## Implementation handoff — 2026-10-07

The approved phases are implemented locally. See
[the validation report](../docs/validation/UpgradeValidation-2026-10-07.md) for actual commands,
results, limitations, recovery and the pending real-Pi checklist. The core/driver baseline is
checked by `python3 scripts/verify_core.py`; no robot runtime or driver source was changed.
Installer bootstrapping follows remote HEAD; onboarding wraps existing tools/helpers.
Current full manuals and code mappings are in the relocated embedded wiki. The rebuilt Pi0
frontend adopts Pi5 navy/cyan presentation without adding Pi5 capabilities. No commit, push,
publication, live-account validation or hardware operation occurred in this upgrade task.
The original phase descriptions below/above remain the approved design history, not claims
that every planned external acceptance check has already run.

## Owner-requested implementation audit — 2026-10-08

A subsequent audit corrected onboarding validation, credential-file privacy, progress/resume and
retry behavior, aligned its terminal flow with Pi5, strengthened installer checks/record cleanup,
and corrected standalone wiki setup isolation. README now provides the owner-requested comprehensive
Pi5-structured introduction, curl installation, initialization and physical test walkthrough.
See [the audit report](../docs/validation/UpgradeAudit-2026-10-08.md) for findings, phase coverage and
final validation: 168 root tests, 61 wiki tests, 64 inert browser assertions, clean lint/knowledge gates,
and unchanged original robot package files. Physical Pi/account acceptance and publication remain pending.
