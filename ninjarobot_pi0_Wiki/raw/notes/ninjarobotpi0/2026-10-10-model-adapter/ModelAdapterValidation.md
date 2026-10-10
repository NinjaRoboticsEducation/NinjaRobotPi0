# Cloud model adapter validation

Date: 2026-10-10 (Asia/Tokyo). Host-only implementation evidence; owner manual Raspberry Pi validation and wiki ingestion/review are pending.

## 1. Scope

API-key selection for Google, OpenAI, Anthropic and Ollama Cloud; profiles/private storage; setup cancellation and atomic publication; agent text/audio parsing; provider errors, truncation and cancellation; stale response rejection; CLI installer; voice capability UI. OAuth/account login belongs to the later milestone.

## 2. Environment and prerequisites

Host: macOS. Existing isolated test environments: `/private/tmp/ninjapi0-robot-env` (Python 3.13.14), `/private/tmp/ninjapi0-py311-env` (Python 3.11.15). Added approved HTTP dependency to these environments; no production Pi environment was installed. `UV_CACHE_DIR` was set to a writable temporary cache; bytecode writes disabled. Frontend uses the committed npm lockfile.

## 3. Safety

Tests use inert SDK, HTTP and hardware fixtures. Browser tests serve static frontend output and intercept every API request/socket; no robot backend was started. No GPIO, servo, buzzer, display, ngrok, live provider account or hardware operation was performed. JEV key presence was checked without exposing credentials; it remained unavailable to this session.

## 4. Completed safe smoke and contract tests

| Check | Actual result |
| --- | --- |
| Pre-change focused Google/config/initializer suite | 39 passed |
| Complete `tests/` suite, Python 3.13 | 377 passed; 8 existing dbus-next Python deprecation warnings |
| Complete `tests/` suite, Python 3.11 | 377 passed |
| Final credential/setup/config focused tests after final refinements | 58 passed on Python 3.13 and Python 3.11 |
| Ruff: `ninja_core/src/ninja_core scripts tests` | Passed |
| npm frontend lint | Passed |
| npm production build (temporary output directory) | Passed |
| Mocked Chromium UI regression | 72 responsive, locale, navigation and API assertions passed, including enabled/disabled voice capability states |
| Shell syntax: installer/onboarding wrappers | Passed |
| Installer/onboarding dry-run | Passed; no account, network, service or hardware action |
| `uv lock --check --offline` | Passed |
| `scripts/verify_core.py` | Passed after explicit baseline reconciliation and approved implementation fingerprint updates |
| Git whitespace check | Passed |

Meaningful failure/robustness coverage includes private permissions, traversing/symlink paths, failed config publication preserving the previous credential reference, concurrent provider writers preserving profiles, canceled/failed discovery and validation producing no config/credential writes, malformed and oversized transport payloads, redirect rejection, provider status errors, repeated pagination, native Google API headers/filtering, truncation, stream cancellation/closure, unsafe action-chain bounds and identifiers, superseded inference and plans waiting on the execution lock, and unsupported voice rejected before file reads or first-interaction hardware logic.

The first broad run exposed the pre-existing uv cache sandbox restriction and stale fingerprints, plus a new installer import issue; these were resolved. The browser test exposed an existing activity-panel/header stacking overlap; a one-line stacking fix restored navigation, and the full browser fixture passed. No test assertions were bypassed with forced clicks or disabled checks. A legacy initializer fixture was adapted to the approved provider-selection prompt and private-key storage.

The regression command explicitly targets `python -m pytest tests -q`. An unscoped repository-root collection also enters independent hardware packages and the embedded wiki; it fails collection because those packages reuse the `tests` module name and the isolated robot environment does not contain `llmwiki`. This does not constitute validation of those separate suites. No wiki ingestion or semantic review workflow was run.

## 5. Communication and provider acceptance — pending on Pi

For each provider, enter test credentials privately using `uv run ninja_core config select-model`, verify a live catalog and one harmless response, then confirm the saved provider/model on deliberate agent startup. Confirm revoked/expired keys, permissions/workspace errors, quota/rate limits and offline behavior are understandable and do not change the active profile or switch providers.

Protect recordings and test code; cloud calls may incur charges. No provider credential or successful live inference is claimed by the host fixtures.

## 6. Voice, sensor and display checks — pending

Test a supported Google recording in the owner's language and verify the response. For OpenAI/Anthropic/Ollama selections, verify the disabled voice label and direct backend voice rejection. Confirm there is no upload to another provider. Sensor/display behavior is unchanged; regression acceptance can use the normal configured device checks.

## 7. Actuator-moving checks — pending and operator-controlled

Server startup can initialize hardware and center servos. Only after confirming wiring, safe servo travel, stable power and clear workspace, execute one existing small known movement through a validated plan. Confirm Stop/new-input interruption and no late movement from a superseded request. Host tests cannot prove physical timing or driver behavior.

## 8. Installer and resource acceptance — pending

On actual Zero 2 W/aarch64/Python 3.10+ Raspberry Pi OS, run `./install.sh --dry-run` first, then the owner-approved installer. Confirm at least 2 GB temporary free space for the approximately 1.56 GB official ARM64 archive. Verify checksum rejection/repair behavior, CLI version and its availability in a new login session, with no model cache, inference libraries or Ollama daemon/service introduced. Confirm direct cloud inference works independently of the CLI. Record binary/dependency disk size, idle/peak RSS, request latency and sensor/event-loop responsiveness under inference.

The checksum was obtained from official release metadata; the ARM64 binary was not downloaded or executed on this macOS host.

## 9. Documentation execution status

Created new complete English InstallationGuide, DevelopmentGuide, DevelopmentLog and README evidence versions plus the detailed implementation and validation notes. Registered originals, canonical wiki pages, indexes, semantic review records and `project-knowledge.json` are unchanged. New sources are intentionally unregistered, and implementation knowledge-map fingerprints are intentionally pending owner ingestion. Consequently no current-wiki release/ingestion gate is claimed.

## 10. Acceptance checklist

- [x] Host implementation tests, lint, build and mocked UI tests pass.
- [x] Four API-key adapters and shared setup are implemented.
- [x] Whole-plan validation, private credentials and no automatic provider fallback are covered by tests.
- [x] Installer implementation is checksum-pinned and daemon/model-free.
- [ ] Live provider accounts accepted on the Pi.
- [ ] Pinned ARM64 CLI executed and resource footprint accepted.
- [ ] Voice and movement/stop acceptance performed with operator readiness.
- [ ] Owner ingested and reviewed English wiki sources and updated canonical mappings/pages.

Until pending target-device and hardware checks pass, this is an evaluation build rather than a hardware-qualified robot release.

## 11. Rollback

Stop the agent in a controlled maintenance session. Restore the prior code/lockfile and private `config.pre-provider.json` when migrating from legacy configuration, preserve calibration and credential records, and deliberately restart with the previous Google profile. For new installs without a legacy snapshot, retain an explicitly working provider profile before changing settings. Remove only recorded installer-owned Ollama files and matching launcher when rolling back installation; do not remove existing user-managed software or provider-side credentials.
