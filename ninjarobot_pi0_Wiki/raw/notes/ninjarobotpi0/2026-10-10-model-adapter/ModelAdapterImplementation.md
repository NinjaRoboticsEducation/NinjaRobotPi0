# Pi0 Cloud Model Provider Adapter

Date: 2026-10-10 (Asia/Tokyo). Implementation baseline: `ae58a22`.

Status: implementation source prepared for owner manual validation, ingestion and semantic review. This document is English-only. No ingestion, normalization, registration, semantic review, wiki plan application, or knowledge-map refresh was performed. Canonical wiki pages still describe the previously ingested Google-only implementation until the owner processes these sources.

## User setup

Run one of these from the installed Pi0 checkout:

```bash
uv run ninja_core config select-model
uv run ninja_core init-tool
./onboard.sh --step ai_model
```

Init-tool option 1 is **Select AI model**. Onboarding step 7 is **Select model provider**. The provider order is Google (Gemini), OpenAI, Anthropic (Claude), Ollama Cloud. Select a provider, enter a hidden API key or reuse the stored key, retrieve the current catalog, select a model, and validate it using a small generation request. Model input accepts `R` to refresh, `B` to return to provider selection, or blank to cancel. No hardware or robot server is initialized by discovery/validation. The validation call may incur provider charges.

After a CLI configuration change, deliberately restart any already-running agent/server to apply it. Server startup initializes robot hardware and can center servos; perform it only under the normal operator readiness procedure. The installer and model-selection tools do not start that server.

The first release uses API keys. It does not implement ChatGPT, Google, Claude or Ollama account login. Consumer subscription credentials/passwords are not API keys. Supported official login routes remain a separate milestone in the approved plan.

## Provider behavior

| Provider | Discovery | Inference | Authentication/context | Voice |
| --- | --- | --- | --- | --- |
| Google | Async paginated Gemini REST catalog, `generateContent` models | Existing SDK for older models; cancellation-aware REST for Gemini 3 models | `x-goog-api-key` in REST; configured SDK key for the older path | Enabled for an explicit known-model allowlist; unknown/new IDs are text-only; real-model/audio acceptance remains manual |
| OpenAI | `/v1/models`, `data[]`; filters known embedding, image, audio and other incompatible families | `/v1/responses`; complete visible text items only; `store:false`, non-streamed API-key requests | Bearer API key | Disabled in this adapter |
| Anthropic | `/v1/models`, bounded `has_more`/`last_id` pagination | `/v1/messages`; text blocks; only successful final stop reasons accepted | Bearer API key, `anthropic-version:2023-06-01`; workspace ID where required | Disabled in this adapter |
| Ollama Cloud | `https://ollama.com/api/tags`, exact returned names | Hosted `/api/chat`, non-streamed `message.content` | Bearer API key | Disabled in this adapter |

The same origin is used for credential validation and inference. A catalog entry is a candidate, not a promise of account entitlement, billing availability or feature parity. Selection is saved only after the chosen model responds to the production adapter's bounded test request. Current Google compatibility selection remains available through `config set-key gemini`; the preferred new flow is `config select-model`. Generic non-provider `set-key` behavior is retained. Provider-specific compatibility commands can expose keys through shell history/argv, so documentation recommends hidden entry instead.

Ollama Cloud does not provide enforced structured output according to the researched official documentation. Its adapter requests ordinary text and relies on the local parser/validator; it does not send local-only schema-enforcement parameters. There is no silent cloud-provider fallback or separate audio-transcription service.

## Code organization

New provider code lives in `ninja_core/src/ninja_core/providers/`: `base.py`, `registry.py`, `http.py`, `cloud.py`, and one module per provider. `provider_setup.py` is shared by CLI and onboarding; `provider_credentials.py` handles opaque private credential records; `private_files.py` provides atomic private writes and cooperative config locks. `agent_response.py` validates model-produced action objects.

`NinjaAgent` retains its public text, audio and code-assistance methods and stateless prompt behavior. Google SDK operations are invoked only when Google is selected; other providers use their native adapters. New Google setup and Gemini 3 REST requests use the shared async transport so canceled setup does not wait for a background urllib worker. Synchronous legacy helpers remain compatibility APIs. Existing robot capabilities, prompts, saved actions and native movement limits remain in force. The new HTTP dependency is `httpx` 0.28.x. Root/core manifests now require Python 3.10+, matching the pre-existing platform check. The lockfile's older Python-3.9 resolution branches are removed as a consequence; this is not an unrelated library upgrade.

Native-audio allowlist: `gemini-2.0-flash`, `gemini-2.0-flash-001`, `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-3-flash-preview`. New IDs must be explicitly qualified before this list is extended. A listed retired model still cannot pass the required setup probe.

## Profiles, storage and migration

`config.json` adds an `ai` object with version 1, `active_provider`, and a `profiles` map. Each provider profile stores its exact model, `auth_method:"api_key"`, an opaque credential reference, and optional Anthropic workspace ID. New API keys are stored separately under `$XDG_CONFIG_HOME/ninjarobot_pi0/credentials/`, defaulting to `~/.config/ninjarobot_pi0/credentials/`. Directory permissions are owner-only; records and config files are mode `0600`.

API keys are never used as model prompts or URL parameters. Raw transport errors and SDK exception messages are not returned to browsers or terminal users. Public robot profiles and `/api/agent/status` omit credentials and their records. Environment variables containing unrelated provider keys do not silently override a selected profile. Filesystem permissions do not encrypt an SD card against root or physical access.

When no `ai` section exists, the runtime resolves legacy `api_keys.gemini` and `gemini.model` in memory, retaining the historical default only for legacy files that omitted a model. New selection writes a private `config.pre-provider.json` snapshot once before migration. Preserve that snapshot for rollback. Legacy Google fields are retained during transition; a new non-Google key is never inserted into those legacy fields. Unknown unrelated root fields and hardware/movement settings survive profile changes.

Credential publication occurs before the atomic config reference update, under a cooperative config writer lock. If config publication fails, the old profile stays active and an unused private credential record may remain. It is not automatically deleted because active/rollback credentials must be preserved. Failed discovery/probe or canceled selection performs no profile/credential publication. Symlink redirects and traversing credential references are rejected. Do not publish migration backups, credential records or config files.

Old onboarding `gemini` progress and `--step gemini` map to `ai_model`; hardware progress and account-unverified status are preserved. Resume/status do not revalidate accounts or infer physical acceptance.

The legacy web key endpoint remains Google-specific: it validates the saved Google model with the new key. If another provider is active, only the inactive Google profile changes. It does not silently switch the running agent. `/api/agent/status` preserves `active` and adds provider, model and audio-capability metadata. Browser voice controls are disabled for unsupported models; backend voice requests are rejected before provider upload or first-interaction hardware behavior. A one-line activity-panel stacking correction keeps the existing header/menu accessible during the browser regression.

## Safety and bounded execution

All model action objects are untrusted. The shared parser checks the complete object: allowed fields, string response, available native/saved action/face/sound identifiers, list shape and maximum 32 entries, repetitions as strict integers 1–20, and finite positive face durations up to 60 seconds (or the existing null/until-replaced behavior). Malformed or invalid objects return no executable actions; a safe string response may be retained. Plain conversational text retains existing speaking behavior. Provider refusals and incomplete responses are rejected before parsing.

The agent serializes command/audio inference. A new interaction invalidates in-flight/queued requests using a generation counter, and web action dispatch rechecks the producing agent/generation after acquiring the execution lock. Changing the active agent invalidates old responses. HTTP cancellation closes the request; inference is not automatically retried. SDK/blocking Google calls remain deadline-bounded, and any late result is discarded.

Hosted HTTP uses approved TLS origins, does not follow redirects with credentials, and limits decoded responses to 2 MiB. Catalog discovery has a 30-second total bound, at most 20 pages/2000 candidates for new cloud adapters, repeated-page protection and sanitized display labels. Generation has a 60-second deadline, a 10-second connection bound and finite provider output limits. Google REST response reads are bounded, and generation finish reasons are checked. Audio uploads and local reads are capped at 8 MiB. No partial streamed plan is executed.

## Ollama installation

`install.sh` delegates to `scripts/install-rpi.sh`, which installs a compatible CLI automatically or reuses an existing compatible CLI. `scripts/install_ollama.py` downloads the pinned official Linux ARM64 release archive, verifies its SHA-256, extracts only `bin/ollama` to a regular staging file, checks its ELF architecture and client version, and publishes it atomically to the app-owned tools directory. A non-overwriting `/usr/local/bin/ollama` launcher makes the private CLI available to later sessions. Incompatible existing installations are preserved and reported for repair.

Pin: v0.40.2. Archive SHA-256: `92b3ef3d5e10f5849273bfa1345000f2a8ce8bc834e95061ff5b9df5d08e3c3f`, retrieved from official GitHub release metadata. The ARM64 archive is approximately 1.56 GB; installation requires at least 2 GB temporary free space plus the retained binary. `zstd` is added to the explicit OS prerequisites. No inference libraries, model weights, GPU drivers, Ollama daemon, service, account login or cloud inference are installed/executed by this helper. Direct hosted Ollama inference does not depend on the CLI or local API.

Dry-run has no network/writes. Check inspects the existing CLI only. The final installer record identifies the pinned artifact inputs. Target-Pi download/extraction/runtime acceptance is still manual; a host metadata check is not proof that this ARM64 binary ran.

## Validation and manual release gate

See `ModelAdapterValidation.md` beside this source for exact completed checks and pending operator checks. Host tests use inert HTTP/SDK/hardware fixtures. Live provider credentials, real OAuth flows, target-Pi installation and physical movements were not exercised. JEV was rechecked twice, but `JEV_API_KEY` was absent from the execution environment; no external JEV request or simulated result was used.

The protected core fingerprint baseline predated committed movement, lifecycle and packaging changes. Its nine pre-existing discrepancies were inspected against committed history and existing tests. Updated fingerprints cover those reviewed committed changes plus the approved model adapter changes; no GPIO/driver/runtime-pipeline behavior was modified by this task. The knowledge-map fingerprints remain pending owner ingestion rather than being refreshed to hide drift.

Before accepting a robot release, manually verify at least one harmless inference per provider, a supported recording, unsupported-audio rejection, network/key failure behavior, and the pinned CLI on actual Zero 2 W hardware. Physical movement/stop checks require operator readiness. An unqualified host build is evaluation-only until those checks pass.

## Rollback

Under a controlled maintenance session, stop the running agent, restore the previous code/lockfile and private pre-migration config snapshot, and deliberately restart. Old code can run the retained Google profile; it cannot run a new non-Google profile. Preserve private credential records for current/rollback references. To remove the CLI, remove only the installer-owned binary directory and its matching launcher after checking ownership; retain pre-existing installations. No automated credential deletion, provider-side revocation or hardware recovery is performed.

## Sources and owner ingestion targets

Official documentation: [OpenAI Responses](https://developers.openai.com/api/docs/guides/text), [OpenAI model list](https://developers.openai.com/api/reference/resources/models/methods/list), [Google OAuth/API keys](https://ai.google.dev/gemini-api/docs/api-key), [Google models](https://ai.google.dev/api/models), [Anthropic API](https://platform.claude.com/docs/en/api/overview), [Anthropic models](https://platform.claude.com/docs/en/api/models/list), [Ollama Cloud](https://docs.ollama.com/cloud), [Ollama structured outputs](https://docs.ollama.com/capabilities/structured-outputs), [Ollama release](https://github.com/ollama/ollama/releases/tag/v0.40.2).

After manual validation, register/normalize the new complete English manual versions and this evidence. Update the approved concept/entity/reference/overview pages listed in `DevelopmentPlanDoc/Pi0ModelAdapterImplementation.md`, update current-manual pointers and reviewed implementation mappings, apply a reviewed wiki plan, then run knowledge checks/lint/links/indexes. This task intentionally leaves that workflow to the owner.
