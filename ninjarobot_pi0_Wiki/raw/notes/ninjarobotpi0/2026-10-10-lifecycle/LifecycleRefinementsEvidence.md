# Lifecycle refinements implementation evidence — 2026-10-10

Raw candidate only. Owner requested implementation and raw documentation updates but explicitly deferred ingestion, normalization, semantic/human review and current-pointer updates. No wiki plan is applied. The previous feature's owner-reported ingestion/review is not evidence of physical validation for this change.

## Exact behavior changes for later wiki review

1. Movement-tool formerly centered on exit. Deliberate option 6 now attempts exact configured Poweroff, or home if absent, before HAL shutdown/configuration save. No following center. Initialization errors/KeyboardInterrupt do not request extra recovery motion. Incompatible/invalid/missing exit pose refuses playback and still cleans up. Existing startup centering is unchanged. PWM is released after reaching the pose, not held indefinitely.
2. Web interface formerly had only Agent-route auxiliary sockets and permitted multiple clients. Shared layout now keeps `/ws/session` for the whole visit. Server-generated opaque HttpOnly same-origin cookie identifies one browser; same-cookie tabs share it. Another identity is busy/4409; every `/api/` request and distance/events socket requires live ownership. Inactive API responses are 423; shutdown responses 503. Existing URLs, request bodies and auxiliary message formats remain. This is a session contract change for direct REST scripts, not authentication. BLE remains separate.
3. Final primary-socket close (or 35-second no-input timeout) cancels pending browser requests/greetings, cooperatively aborts native/Blockly outputs and restores the saved public ngrok QR, or LAN QR if no tunnel exists. The reconnect screen suppresses native idle restoration; first reconnect restores native behavior. QR/startup/disconnect/handoff transitions are serialized, failures release ownership, shutdown does not repaint QR. Generation context rejects old threads even after the same cookie reconnects; optional centering callback rechecks ownership within the controller lock. Driver stopping remains cooperative and needs physical acceptance.
4. Legacy root distribution/lock identity and `.venv` prompt become ninjarobotpi0. `.venv` directory and locked dependency versions stay unchanged. Installer explicitly uses `uv venv --allow-existing --prompt ninjarobotpi0 --python /usr/bin/python3 .venv`, without `--clear`, before production sync; uv preflight checks its venv capabilities. Existing local prompt-only files were updated without dependency installation. An already active shell must re-activate to show the new label.

## Software and safety evidence

Full root tests: 319 passed, one unchanged-source-baseline case deliberately deselected, 31 existing dbus_next warnings, exit 0. Feature/runtime subset: 72 passed; installer subset: 93 passed/1 deselected. Focused Ruff, frontend lint/production build, shell syntax, Node hook tests/browser-fixture syntax, offline lock check, installation dry-run, local activation prompt check and raw/public documentation links passed. Tests use inert hardware. No live server, actuator/display output, ngrok/AI call, package installation or daemon/service change occurred.

Three initial installer fixture failures were fixed by constraining fixture Node selection: choosing real `/usr/bin/node` had prepended `/usr/bin` and bypassed mocked systemctl on this real Pi. Selection logic has separate unit coverage. No real pigpiod stop was performed. Generated frontend assets replace the previous bundle. Pre-existing owner bytecode changes remain untouched.

Nine protected source/metadata fingerprints differ from the older baseline (including previous built-in implementation); no baseline is refreshed. Current wiki check reports changed implementation mappings and four new files needing classification. These are expected deferred-review findings, not a completed wiki gate. Strict lint, ingestion/normalization, semantic review, links/index/stats workflows are not run. Local Markdown target checks are separate and passed.

## Original evidence retained

- InstallationGuide: src-20261009-installationguide; sha256:0303e14ce171088cba240df2a0a3a29d88e2db0dc5cc2263f26f95d89ac68945.
- DevelopmentGuide: src-20261009-developmentguide-2; sha256:80ef9c89176a6b0a3749f9127697464f197c2972bf2a41ae533fa2cb7afdc0ab.
- DevelopmentLog: src-20261009-developmentlog-2; sha256:d176728a0871bab1ad8a7138df05ca04d87c6782011c7459f49278c07a9c3a88.

Final hash comparison confirms those registered originals are unchanged. Relevant wiki pages: spider-otto-waypoint-library, motion-system-and-easing, web-interface-design, dual-connectivity-and-protocols, installation-guide and safe-execution-and-blockly-runtime. Their draft/unverified lifecycle and recorded AI reviews are not physical acceptance. CLI retrieval environment was missing, so tracked content/current code was used; no dependencies were installed for retrieval.

## Candidate inventory and future mapping scope

New complete manuals and root README snapshot: `raw/articles/ninjarobotpi0/2026-10-10-lifecycle/`. Core README snapshot: `raw/articles/ninja_core/2026-10-10-lifecycle/`. Complete DevelopmentLog, plan, validation and this evidence: `raw/notes/ninjarobotpi0/2026-10-10-lifecycle/`. All sources remain unregistered until owner ingestion; no source IDs or reviews are invented.

After owner validation, register complete new sources, review the exact behavior changes above against code, and update movement/CLI pages, web-interface/connectivity/runtime pages, installation/setup pages and current source maps. Account for changed CLI/controller/pipeline/web server, new web_sessions module, hook/layout/locales, installer/preflight, root metadata/lock, tests, READMEs and built assets. Existing current pointers remain on the prior ingested versions until that workflow runs.

See [plan](LifecycleRefinementsImplementationPlan.md), [validation](LifecycleRefinementsValidation.md) and [current candidate log](DevelopmentLog.md). Physical clearance, pose holding, interruption timing, actual QR scanability, mobile timers and live ngrok/browser handoff remain pending for this refinement.
