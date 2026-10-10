# Server shutdown and browser voice regression repair

Date: 2026-10-11 (Asia/Tokyo). User-authorized regression fixes following the model adapter implementation. This is new English source evidence for owner manual ingestion and review; registered originals, canonical pages, semantic review records and the knowledge map are unchanged.

## 1. Scope of validation

Restore the configured Poweroff rest pose on ordinary `ninja_core server` exit and restore browser microphone input independently of cloud model selection. Preserve provider-specific direct audio-file capability checks. Keep servo drivers, calibration, GPIO mapping, cloud adapters and credentials unchanged.

## 2. Environment and prerequisites

Host: macOS; isolated Python 3.11.15 and 3.13.14 test environments, existing locked frontend dependencies. Use `PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/ninjapi0-uv-cache` for tests. Browser fixtures serve a temporary Vite build and intercept API requests and sockets. No dependency installation or lockfile change was needed.

## 3. Safety notes

No real server, GPIO, servo, display, buzzer, provider account, microphone or OS power-off was activated. All hardware and recognition objects are inert fixtures. On the physical Pi, startup can center servos, and exit deliberately executes the configured rest movement. Support the robot, confirm wiring/calibration and clear its travel area before testing. Forced termination or abrupt power loss cannot guarantee a completed rest pose.

## 4. Safe smoke tests and root-cause evidence

The installed Uvicorn `Server.capture_signals` restores original signal handlers and replays captured signals after lifespan shutdown. The old application handler then attempted Poweroff against the HAL/pigpio connection already released by lifespan. This explains the reported `NoneType.send` failure without changing or bypassing the servo driver.

Shutdown now runs in one shared asynchronous task. Lifespan and web power-off join that task. The task invalidates pending inference, interrupts current actions, stops services/background work, waits for the action lock, attempts Poweroff and then stops outputs and releases HAL. Shielding prevents cancellation of a waiting caller from interrupting the hardware sequence. Duplicate calls do not repeat the movement or release. A pose failure is reported and still attempts release; an executor that refuses to stop prevents a conflicting rest movement. The web endpoint alone requests Linux shutdown, after hardware cleanup. Ctrl+C exits the server without requesting Linux shutdown.

Phase 1 retrieved current wiki evidence and inspected signal, lifecycle, action-lock and browser paths. Phase 2 implemented the coordinated shutdown and microphone correction with regression tests. Phase 3 ran host lint, build and regression checks and prepared immutable English manual/log snapshots. No hardware test is inferred from these phases.

## 5. Communication/interface tests

The existing microphone uses `SpeechRecognition`/`webkitSpeechRecognition`, converts speech into text in the input box and sends it through `/api/agent/chat` when the user presses Send. It does not upload audio to `/api/agent/voice`. The adapter incorrectly gated this button with `supports_audio`, which describes raw model audio input. Removing that gate restores browser speech input for Google, OpenAI, Anthropic and Ollama text models, including when the status request fails or the model is not audio-capable. The page now owns its recognition instance and aborts it when unmounted; synchronous recognition startup failures reset the recording state.

Direct audio uploads remain capability-gated and bounded, as approved in the original API-key release. Browser support, permissions, secure context and the browser's speech service remain relevant; no new external transcription service or credentials were introduced.

## 6. Sensor/display checks

Shutdown stops distance monitoring before the rest movement and stops face/sound outputs afterward. Display clearing and HAL release remain part of the final cleanup. Pi sensor/display acceptance is pending; host fixtures only verify sequencing and control flow.

## 7. Actuator-moving or power-risk tests — owner controlled and pending

On a safely supported, calibrated Pi, start `uv run ninja_core server` and press Ctrl+C once. Confirm the configured Poweroff movement completes before servo release and terminal exit, without `NoneType.send` or a second movement. Repeat once during a short, known existing action and verify the action stops before the rest pose. Test service SIGTERM only in a maintenance session. In a separate session, test the Home power slider and confirmation, then confirm Linux has halted before removing power. Do not treat forced termination as a graceful-exit test.

Before browser validation, rebuild the deployed frontend from the Pi0 checkout (`cd ninja_webapp && npm run build`), then restart the server and reload the page. The host validation build was written to a temporary directory; committed/generated production assets were not edited. Use a browser that supports Web Speech recognition and grants microphone permission. Select each configured provider in turn, restart the agent as documented, speak a harmless phrase, confirm text appears, then Send. Leave the Agent page while recognition is active and verify it stops. Neither this check nor changing providers should require audio-file support.

## 8. Expected outcomes

Exactly one Poweroff attempt precedes HAL release on ordinary server shutdown. Failed rest poses are reported; cleanup still attempts hardware release. Browser microphone activation and recognized-text submission are independent of provider audio flags. Direct uploaded audio remains restricted to supported models. The power-off API retains its response shape and confirmed user flow.

## 9. Execution status and evidence

- Eight new inert shutdown regressions cover concurrent/repeated callers, pose failure, action-lock waiting, cancellation during movement, uncooperative executors, repeated web power-off and actual Uvicorn SIGINT/SIGTERM capture/replay. No network server is started by these tests.
- Complete `tests/` suite: 385 passed on Python 3.11; 385 passed on Python 3.13, with eight existing `dbus-next` deprecation warnings.
- Ruff checks over `ninja_core/src/ninja_core scripts tests`, frontend ESLint and temporary-output production build passed.
- Protected core baseline reviewed specifically for the approved `web_server.py` lifecycle change; other protected hashes were preserved. Core verification passed.
- Mocked Chromium browser suite: 96 assertions passed, including enabled microphone, recording start/stop, recognized transcript submitted through text chat, navigation cleanup, responsive layout, locale and existing control contracts. All four provider/audio-capability fixtures were exercised without a live service.
- Final whitespace, English snapshot and repository-boundary checks passed; servo drivers, generated assets and canonical wiki files were unchanged.
- The first broad test run correctly reported the changed server fingerprint; after reviewing the lifecycle diff and passing the new regressions, only that fingerprint was updated. Browser fixture timing waits were added for React transcript/effect completion, and the activity drawer is explicitly closed through its UI before microphone interaction. No forced clicks or disabled assertions were used.
- JEV credential presence was checked safely; the execution environment still had no `JEV_API_KEY`. No JEV request or result is claimed.

Wiki retrieval succeeded: `search "shutdown Poweroff voice audio"`, `source status`, and pre-change `check` (passed). Relevant pages were `wiki/entities/ninjarobot-v5.md` (sleepy face/sound, rest pose and hardware release; source-grounded AI review dated 2026-10-07), `wiki/concepts/web-interface-design.md` (browser speech input; source-grounded AI review dated 2026-10-10), `wiki/concepts/action-library-and-ai-agent.md` and `wiki/references/api-and-cli-reference.md` (adapter audio gating). These pages remain draft/unverified; their semantic reviews are not human or physical acceptance. Model-adapter evidence conflated browser text recognition with raw-audio capability and must be corrected during owner ingestion. The mapped current manuals and source records were inspected, and registered sources were ingested before this task.

## 10. Pass/fail checklist

- [x] Corrected signal/lifespan ownership and shutdown ordering verified with inert regression tests.
- [x] Python 3.11 and 3.13 host suites passed.
- [x] Python/frontend lint, build and core verification passed.
- [ ] Actual Pi Ctrl+C/SIGTERM, rest pose and physical Stop timing accepted.
- [ ] Actual browser microphone and all live provider selections accepted by owner.
- [ ] Owner ingested/reviewed the new English sources and updated canonical pages and mappings.

No ingestion, normalization, semantic review or map refresh was run. Current-source/code fingerprints will report the expected pending documentation drift until owner ingestion.

Read-only post-change wiki checks: normal lint reported zero errors/warnings and five unregistered-source suggestions (the new evidence versions); link check passed and indexes are current. The knowledge check reports five changed mapped files and the new shutdown regression file awaiting classification. Strict release review was not run; the owner-deferred ingestion and semantic review remain outstanding. These read-only checks do not register or review the new implementation.

## 11. Rollback

Stop the server in a safe maintenance session. Revert only this task's shutdown, microphone and test/doc changes to the prior revision; preserve provider profiles, private credentials and calibration. Reverting restores the known pre-fix limitations, so avoid relying on the old Ctrl+C pose sequence. No lockfile, dependency, model or driver rollback is required.
