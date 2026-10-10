# Pi0 Cloud Provider Adapter — Phased Implementation Plan

**Date:** 2026-10-10 (Asia/Tokyo)

**Status:** Draft for owner review; implementation is not authorized by this document.

**Repository baseline:** NinjaRobotPi0 `d0f451d`; clean worktree before this plan.

**Deliverable scope:** Research and this plan only. No runtime changes, installations, account access, paid inference, or hardware operations were performed.

## 1. Outcome and confirmed scope

Add a provider boundary to NinjaRobot Agent so users can configure **Google (Gemini), OpenAI, Anthropic (Claude), or Ollama Cloud**, discover suitable models, validate their selection, and run the agent using that provider.

The owner confirmed these decisions during planning:

1. **Pi0 uses cloud inference only.** Install the Ollama CLI automatically, but do not download model weights, run local inference, or add a remote self-hosted Ollama endpoint.
2. **Release 1 uses API keys for all four providers.** Officially supported account login belongs in a later phase.
3. **Release 1 is text-first.** Preserve voice for models with verified audio support; clearly report voice as unavailable elsewhere. Do not silently send audio to another provider or introduce a transcription account.

Required setup flows:

- `ninja_core init-tool`: rename option 1 to **“Select AI model”**.
- `./onboard.sh`: replace the current seventh step with **“Select model provider”** while retaining its position, skip/retry/resume behavior, and other steps.
- Both invoke the same sequence: **provider → authentication → live model discovery → model selection → safe validation → atomic save**.
- `./install.sh`: automatically install/reuse a compatible Ollama CLI as part of software installation. Installation must not start an Ollama daemon, robot service, hardware tool, or login flow.

Non-goals: Pi5 support, Education web-platform changes, local models, arbitrary API gateways, browser-based provider administration, new speech transcription/TTS services, new agent tools, automatic cross-provider fallback, or changes to GPIO, calibration, movement APIs, and BLE command envelopes.

Overall implementation risk is **medium-high**: the inference boundary affects robot plans, credentials, startup, and deployment. Provider selection must never bypass existing execution checks. The current planning task is read-only except for this file.

## 2. Evidence and current implementation

### 2.1 Wiki retrieval and trust

Used the Pi0 `robot-wiki-query` workflow against **`ninjarobot_pi0_Wiki/`**, the canonical embedded wiki named in Pi0 policy. The similarly named Librarian copy is not substituted for it.

Executed `python3 scripts/wiki.py search 'Gemini'`, `source status`, `check`, `lint --strict`, `link check`, `index check`, and `stats` from the Pi0 root. Results: knowledge check passed; strict lint reported **0 errors, 0 warnings, 0 suggestions**; link check exited successfully; indexes were current. Stats reported 27 draft/unverified pages with 27 passing sourced semantic reviews, 67 ingested sources and 4 pending sources. A passing agent review does not establish human verification or Raspberry Pi acceptance.

Primary retrieved pages:

| Page under `ninjarobot_pi0_Wiki/wiki/` | Evidence used | Qualification |
| --- | --- | --- |
| `concepts/action-library-and-ai-agent.md` | Model discovery/probe, Gemini runtime split, action validation and interruption | Draft/unverified; recorded semantic review passed on 2026-10-09; checked against code |
| `concepts/guided-onboarding.md` | Step ordering, private workers, skip/resume, explicit hardware readiness | Draft/unverified; recorded semantic review passed on 2026-10-08; checked against `scripts/onboard.py` |
| `entities/ninja-core.md` | Core configuration and agent component discovery | Retrieved as supporting navigation; code remains decisive |
| `references/api-and-cli-reference.md` | Existing CLI compatibility surface | Retrieved as supporting navigation; exact CLI inspected |

`project-knowledge.json` resolves the current manuals to:

- Installation: `raw/articles/ninjarobotpi0/2026-10-10-cli-repair/InstallationGuide.md`, source `src-20261010-installationguide-2`.
- Development: `raw/articles/ninjarobotpi0/2026-10-10-cli-repair/DevelopmentGuide.md`, source `src-20261010-developmentguide-2`.
- Log: `raw/notes/ninjarobotpi0/2026-10-10-cli-repair/DevelopmentLog.md`, source `src-20261010-developmentlog-2`.

Their registered fingerprints passed the knowledge check. Relevant agent-page provenance includes `src-20260822-developmentguide`, `src-20260822-readme-3`, and `src-20261009-2026-10-09-builtin-movements`. Historical citations are not treated as proof of new provider capabilities.

### 2.2 Verified code map

Paths below are relative to NinjaRobotPi0. Existing symbols are named exactly; proposed files are explicitly marked new.

| Existing file/symbol | Current behavior and required impact |
| --- | --- |
| `ninja_core/src/ninja_core/config.py`: `NinjaConfig`, `GeminiConfig`, `set_gemini_configuration`, `save_config` | Stores `api_keys["gemini"]` and `gemini.model`; legacy default is `gemini-3-flash-preview`. Generic save is a direct JSON write. Add provider profiles, explicit migration, and a shared private transactional writer. |
| `ninja_core/src/ninja_core/gemini_models.py`: `list_available_gemini_models`, `_fetch_model_pages` | Existing REST discovery, pagination and safe errors. Reuse its behavior behind the Google adapter. |
| `ninja_core/src/ninja_core/gemini_runtime.py`: `generate_content_text`, `validate_gemini_model`, `requires_thinking_compatibility` | Bounded REST path for Gemini 3 compatibility; preserve initially. |
| `ninja_core/src/ninja_core/init_tool.py`: `configure_gemini_api_key`, `run_init_tool` | Option 1 discovers, selects, probes, then persists Gemini settings. Replace with shared provider setup and keep a compatibility wrapper. |
| `ninja_core/src/ninja_core/__main__.py`: `set_key`, `chat` | Gemini-specific setup and startup messages. Preserve existing commands while adding safe provider selection. |
| `ninja_core/src/ninja_core/ninja_agent.py`: `NinjaAgent` | Direct Google SDK imports/configuration; text, recorded audio and all four code-assistance methods use Gemini. Extract provider transport, retaining public method contracts. |
| `scripts/onboard.py`: `STEPS`, `_worker`, `wizard`, progress helpers | `gemini` is step 7. Worker masks input and protects config permissions; progress must remain secret-free. |
| `ninja_core/src/ninja_core/web_server.py`: `agent_status`, `set_key_endpoint`, agent initialization and audio route | Status only returns `active`; legacy key endpoint writes Gemini then rebuilds the agent. Add safe compatibility behavior and capability reporting. Server startup can center servos: never use it as a harmless model probe. |
| `ninja_core/src/ninja_core/dispatcher.py`, `runtime_pipeline.py`, `safe_executor.py` | Consumers of agent results and execution/cancellation controls. Preserve behavior and verify with regression tests. |
| `ninja_webapp/src/pages/Agent/index.jsx`, `src/locales/{en,ja,zh-tw,zh-cn}.json` | Existing voice control needs an unavailable state and provider-neutral errors; no provider-settings screen is proposed. |
| `install.sh`, `scripts/install-rpi.sh`, `install_check.py`, `install_record.py`, `install-versions.env`, `install_system.py` | Root script delegates actual installation. Add Ollama there, including preview/check/version-record behavior. |
| Root and `ninja_core/pyproject.toml`, `uv.lock` | Both declare legacy `google-generativeai`; inspect and lock any new HTTP/auth dependency in both owning manifests as appropriate. |
| `docs/validation/core_baseline.json`, `scripts/verify_core.py` | Several affected files are fingerprint-protected. Review intended changes before refreshing their baseline; never refresh merely to hide failures. |

Important limitations/drift found:

- Runtime preflight requires Python 3.10+, although package metadata and older manual sections still say 3.9+. Resolve that inconsistency within the approved packaging/documentation phase; do not claim Python 3.9 support.
- The agent constructs a search tool, but `_create_model` does not attach it. Comments about automatic search are not evidence of working cross-provider web search. Release 1 adds no search-parity promise.
- Agent parsing currently extracts JSON from text, and `_validate_native_plan` enforces native movement names, robot type, at most 32 chain entries and integer repetitions 1–20. Provider output still requires local validation.
- Existing plain-text fallback can produce speaking face/sound. Setup probes must bypass the entire agent/dispatcher, even for an innocuous prompt.
- The Education Code IDE's BYO credentials are a separate contract; this task must not import those browser credentials into robot configuration.
- The final read-only `scripts/verify_core.py` check reported **nine pre-existing fingerprint mismatches**, despite a clean tracked worktree: `ninja_core/pyproject.toml`, `ninja_core/src/ninja_core/{config,movement_cli,movement_controller,ninja_agent,runtime_pipeline,web_server}.py`, root `pyproject.toml`, and `uv.lock`. The knowledge-map check passes, so the protected-source baseline and knowledge map disagree. Phase 0 must reconcile their provenance against committed changes before implementation; no hashes were refreshed during planning.

The Education root worktree contained extensive unrelated changes before planning. Those files, Pi5, and the Librarian wikis are outside this task.

## 3. Official API research and feasibility

Research date: 2026-10-10. These are documented capabilities, not live-account test results. Model catalogs, access, and previews must be checked again during implementation. “OpenAI” identifies the API provider; a ChatGPT subscription and an API key are distinct authentication/billing routes.

### 3.1 Release 1 authentication and discovery

| Provider | API-key route | Model discovery | Inference adapter |
| --- | --- | --- | --- |
| Google | AI Studio key in `x-goog-api-key`; handle restrictions and key rejection without exposing the key | `GET https://generativelanguage.googleapis.com/v1beta/models`; follow `nextPageToken`, require `generateContent` support | Preserve the current supported `generateContent` path and Gemini compatibility behavior initially |
| OpenAI | API key in `Authorization: Bearer` | `GET https://api.openai.com/v1/models`; API-key catalog uses `data[]` model IDs, not an agent-compatibility guarantee | Responses API (`POST /v1/responses`) for the new adapter; parse text output items, refusals and incomplete/error states |
| Anthropic | Console API key using the documented bearer header; legacy `x-api-key` remains supported. Include `anthropic-version`; supply `anthropic-workspace-id` when a multi-workspace key requires it | `GET https://api.anthropic.com/v1/models`; use `has_more`/`last_id` pagination; retain capability/lifecycle metadata when present | Messages API (`POST /v1/messages`); extract text blocks and distinguish refusal, tool-use and truncation states |
| Ollama Cloud | Ollama API key in `Authorization: Bearer` | `GET https://ollama.com/api/tags`; use returned names exactly | Native `POST https://ollama.com/api/chat`; extract `message.content`; explicitly choose streaming behavior |

Sources: [Google keys](https://ai.google.dev/gemini-api/docs/api-key), [Google models](https://ai.google.dev/api/models), [Google generation](https://ai.google.dev/api/generate-content), [OpenAI API authentication](https://developers.openai.com/api/reference/overview), [OpenAI models](https://developers.openai.com/api/reference/resources/models/methods/list), [OpenAI text generation](https://developers.openai.com/api/docs/guides/text), [Anthropic API overview](https://platform.claude.com/docs/en/api/overview), [Anthropic models](https://platform.claude.com/docs/en/api/models/list), [Messages](https://platform.claude.com/docs/en/api/messages/create), [Ollama Cloud](https://docs.ollama.com/cloud), [Ollama authentication](https://docs.ollama.com/api/authentication), [Ollama chat](https://docs.ollama.com/api/chat).

Discovery is not authentication proof for every endpoint: Ollama documents a public cloud catalog. For every provider, use the candidate credential and selected model in a bounded, non-executing generation probe before saving. Listing also does not guarantee billing eligibility or ongoing availability.

### 3.2 Account login: later-phase feasibility

| Provider | Official evidence | Plan decision and release gate |
| --- | --- | --- |
| Google | Gemini documents OAuth, a Cloud project, consent-screen/client configuration, token refresh and authenticated model listing | Feasible as an advanced Google API login. Requires owner-managed client/project, appropriate scopes/quota project, distribution/verification review and a headless flow test. Do not describe it as access through a consumer Gemini subscription. |
| OpenAI | Current Sign in with ChatGPT docs explicitly support eligible open-source clients using ChatGPT plan usage | Feasible, conditional on project/account eligibility and preview restrictions. Implement the documented public-client registration/PKCE flow; do not reuse Codex credentials or private ChatGPT endpoints. |
| Anthropic | Official `ant auth login` supports Claude Console OAuth; scripting docs explicitly permit obtaining a refreshed token for HTTP requests | Feasible for a separate Console-login integration, subject to ARM64 tooling and runtime suitability tests. It is documented for local development/personal scripting; unattended server use needs separate assessment. Consumer Claude subscription login for this arbitrary agent is not established by these sources. |
| Ollama | `ollama signin` supports cloud use through the CLI/local API; direct hosted API access is documented with API keys | Retain direct cloud API keys for this plan. A later CLI-login integration would introduce a local proxy/daemon dependency and needs its own resource and lifecycle decision. Do not present CLI credentials as a documented general OAuth bearer token for direct cloud HTTP. |

Sources: [Google OAuth](https://ai.google.dev/gemini-api/docs/oauth), [Sign in with ChatGPT quickstart](https://developers.openai.com/siwc/quickstart), [OpenAI registration/sign-in](https://developers.openai.com/siwc/token-sharing-open-source/sign-in), [Anthropic CLI authentication](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/authentication), [Anthropic scripting](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/scripting), [Ollama authentication](https://docs.ollama.com/api/authentication).

OpenAI's later adapter must handle an authentication-specific catalog: OAuth listing returns `models[]` with `slug`, `display_name` and `visibility`, unlike the API-key catalog. The documented flow requires streaming Responses requests with `store: false`. Its preview rejects several ordinary parameters, including `max_output_tokens` and `temperature`, and does not support audio/transcription. Thus authentication mode is part of capability negotiation, not simply a different string in the same header. [Catalog and inference](https://developers.openai.com/siwc/token-sharing-open-source/models-and-inference), [preview restrictions](https://developers.openai.com/siwc/token-sharing-open-source/preview-limitations).

A headless Pi cannot receive a laptop browser's loopback callback without a deliberate local tunnel or another officially supported flow. Do not open a public callback, use ngrok automatically, collect account passwords, scrape cookies, or invent an unsupported device-code grant.

### 3.3 Ollama-specific constraints

Direct cloud requests need no Ollama installation or local server. Installing the CLI is an explicit owner requirement, not an inference prerequisite. The official Linux guide provides ARM64 artifacts; actual CLI compatibility and footprint on Zero 2 W still need testing. Use a reviewed, pinned artifact rather than executing an unpinned network script during installation. [Cloud](https://docs.ollama.com/cloud), [Linux installation](https://docs.ollama.com/linux).

Ollama Cloud currently **does not support structured outputs**. Do not send local-only JSON-schema options and assume enforcement. Prompt for the existing action schema, parse defensively, and apply the same local safety validator as every other provider. Malformed action output must produce no executable actions. [Structured outputs](https://docs.ollama.com/capabilities/structured-outputs).

## 4. Proposed architecture

### 4.1 Small native adapters

Add a `ninja_core.providers` package rather than a full agent framework or multi-provider proxy. Proposed new modules:

- `providers/base.py`: typed request/result, model descriptor, capabilities, normalized errors and provider protocol.
- `providers/registry.py`: fixed provider IDs `google`, `openai`, `anthropic`, `ollama`; `gemini` accepted only as a compatibility alias for Google.
- `providers/google.py`, `openai.py`, `anthropic.py`, `ollama.py`: authentication-specific discovery and generation mapping.
- `providers/http.py`: shared bounded async HTTP transport; proposed dependency `httpx`, pinned and verified for the supported Python/ARM64 environment during implementation.
- `provider_setup.py`: shared setup orchestration independent of menus and hardware.
- `provider_credentials.py`: private credential records and explicit credential resolution.
- `agent_response.py`: shared parsing and validation for text/audio action output.

Keep existing Google helpers as delegating compatibility surfaces while migrating consumers. Retain the legacy Google SDK behind the Google adapter initially; replacing it with `google-genai` or a complete REST implementation is a separate follow-up, not a prerequisite for adding providers.

Proposed interface responsibilities:

| Operation/type | Contract |
| --- | --- |
| `list_models(auth, deadline)` | Return bounded, deduplicated `ModelOption` objects; no hardware imports or writes |
| `capabilities(model, auth_mode)` | Text, recorded-audio, JSON-schema enforcement, tools and supported generation controls; each unknown remains unknown/disabled |
| `validate_model(model, auth)` | One tiny text/JSON probe through the production transport, no robot prompt, tools, dispatcher or execution |
| `generate(request, cancellation)` | Return normalized text, finish state, safe diagnostics and optional usage; never execute tools/actions |
| `ProviderError` | Safe category: authentication, permission, billing/quota, rate limit, unavailable model, unsupported capability, timeout/network, refusal or malformed response |

The `NinjaAgent` continues to own prompts and existing methods: `process_command`, `process_audio_command`, `explain_code`, `generate_code`, `analyze_error`, `analyze_code`, and `refresh_capabilities`. Return shapes such as `{action_plan, response, log}` remain compatible. Preserve current stateless request behavior; adding conversational memory is outside scope.

### 4.2 Model eligibility and validation

1. Fetch a live catalog after credential entry, including documented provider pagination. Bound total pages, items, bytes and elapsed time; detect repeated page tokens.
2. Normalize display metadata but preserve the exact provider model ID. Escape control characters in catalog text before printing it to the terminal.
3. Exclude explicitly non-text endpoints/models, retired entries and models incompatible with the implemented generation route. Do not use a name prefix alone as proof of compatibility.
4. Use provider metadata plus a small reviewed capability registry where metadata is incomplete. Unknown text candidates may be offered as “unverified—requires validation”; known incompatible models cannot be selected. Do not probe the entire catalog.
5. Show text/voice availability and the current selection. A saved model absent from the catalog is shown as unavailable, never silently replaced.
6. Explain that the selected-model probe may incur a small provider charge, then run it only as part of the user's explicit setup action. A successful probe is point-in-time evidence, not a guarantee.
7. Persist only after a successful probe. Cancellation, empty catalogs, invalid keys, quota failures, timeouts and invalid output leave the active configuration unchanged. Cached catalogs may aid display but cannot authorize a new selection without validation.

### 4.3 Configuration and credential transaction

Proposed non-secret shape in `config.json` (illustrative placeholders, not default model choices):

```json
{
  "ai": {
    "version": 1,
    "active_provider": "openai",
    "profiles": {
      "openai": {
        "model": "<selected-live-model-id>",
        "auth_method": "api_key",
        "credential_ref": "<opaque-record-id>"
      }
    }
  }
}
```

Optional provider context belongs in each profile (for example Anthropic workspace ID, or a later Google quota project); do not add freely configurable base URLs. Configure one remembered profile per provider in Release 1. Multiple accounts per provider are a later extension.

Store new credentials outside the repository, under an app-owned user directory such as `~/.config/ninjarobot_pi0/credentials/`, with directory mode `0700` and records `0600`. Reject symlink/path traversal targets; never serialize raw secrets into a public Pydantic dump. The directory is private filesystem storage, not encryption against root or an SD-card reader; document that limitation.

Transaction design: keep candidate credentials in memory while discovering/probing; write a new immutable credential record atomically; then atomically replace the non-secret config referencing it. Lock concurrent writers, flush/fsync writes, and preserve the previous config/reference until commit. A crash before config commit can leave an unused private record, but cannot switch the active provider. Cleanup must not remove referenced records or rollback credentials. Apply private-write guarantees to all config-writing callers so hardware imports cannot undo permissions.

Read-only status, preview and compatibility resolution must not create/migrate files. Keep credentials out of onboarding progress, exports, browser status, BLE profiles, screenshots, logs and exception text. If environment credentials are supported, a profile explicitly selects that source; an unrelated environment variable must not silently override a saved account.

### 4.4 Legacy migration and rollback

- With no `ai` block, resolve legacy `api_keys.gemini` plus `gemini.model` as the Google profile in memory. Preserve the existing default only for legacy files missing a model; do not recommend that preview ID for new installs.
- Explicit setup writes the new profile only after validation. Preserve unrelated calibration/movements/ngrok settings and a private pre-migration snapshot. Keep old Google fields during the transition for rollback; do not insert new non-Google secrets there.
- New `ai` state takes precedence. Corrupt/unsupported versions fail visibly; never silently fall back to another provider and disclose the prompt there.
- Keep `configure_gemini_api_key` and `config set-key gemini` as compatibility routes to Google setup. Add `config select-model` as the preferred shared entry point. Preserve generic non-provider `set-key` behavior. New examples use hidden input, not literal keys in argv.
- CLI selections apply on next agent/server start; do not automatically restart a server that can energize hardware. Report this clearly. Existing explicit web key updates must retain their documented runtime behavior safely.
- Legacy `/api/agent/set_api_key` continues to mean Google only. Validate and update the Google profile transactionally; if another provider is active, do not switch/rebuild it. Return a safe message explaining that the active provider is unchanged. If Google is active, replace its agent only after validation succeeds.
- Map old onboarding `gemini` progress/`--step gemini`/worker aliases to the new `ai_model` step. Prior saved completion means “configured; not revalidated online,” not current account validity. Preserve all hardware progress and schema-version compatibility.
- Rollback: stop the agent under existing maintenance procedures, restore the previous code/lockfile and private configuration snapshot, then deliberately restart. Old code cannot run a non-Google profile. Keep the previously working Google setup available where one existed; never fabricate rollback credentials.

## 5. Safety, security and platform constraints

**Robot output is untrusted.** Keep the existing native-chain limits, robot-type filtering, action-library resolution, SafeExecutor and dispatcher cancellation. Centralize parsing so text and audio use identical rules. Validate the complete action object before dispatch, including face/sound/action identifiers and types. On malformed JSON, refusal, truncation or timeout, return an empty executable plan; do not convert an invalid plan into partial movement. Plain conversational fallback may retain existing speaking behavior only after being explicitly classified as valid prose.

**Setup cannot activate hardware.** Importing provider/setup modules must not import HAL/drivers, initialize the web server or instantiate the dispatcher. Probe directly through the provider adapter with a synthetic prompt and no executable actions. Unit tests must assert this isolation.

**Network and cancellation are bounded.** Proposed defaults: 10-second connect timeout, 30-second total catalog deadline, 60-second generation/probe deadline, one outstanding inference per agent. Bound response bytes and audio upload size, with limits documented/tested before release. Use cancellation-aware async requests; discard late responses using request/session generation IDs. Retry idempotent catalog GETs at most twice with bounded backoff. Do not automatically replay generation or hardware actions after ambiguous failures.

**Controls vary by provider.** Map output/reasoning controls only where documented. For the later OpenAI OAuth route, local stream byte/time limits must replace unsupported request limits; local cancellation does not guarantee server-side billing stops. Never execute partial streamed plans. Provider errors should name provider/model and a safe category, not raw response bodies, request headers or URLs containing credentials.

**Credential scope and transport.** Use TLS verification and fixed official origins. Reject cross-origin redirects carrying authorization. Keep API keys in headers. No provider credentials in browser bundles, BLE messages, URLs, shell history, model prompts or logs. Redact legacy keys as well as new records. Invalidate caches after provider/account/workspace changes. Local deletion does not revoke a provider key; document provider-side revocation separately.

**Cloud privacy/cost.** Setup explains that prompts, code and supported recordings go to the selected provider and may incur charges. Do not silently route to a second provider. Discovery failure must distinguish unauthorized credentials from unavailable networking/quota. No model names, pricing or account entitlement are hardcoded as permanent guarantees.

**Pi0 resources.** Target the current Zero 2 W/aarch64/Debian-family/Python 3.10+ preflight. Measure installed dependency/CLI disk size, runtime peak RSS, request latency and event-loop responsiveness on the real Pi. No GPU drivers, model weights or background inference service. No claim of ARM64 feasibility is complete until the pinned artifact executes successfully on the target.

**Voice.** Release 1 enables recorded audio only for a tested provider/model/auth combination. Preserve Gemini's supported path. Disable voice otherwise and reject audio server-side before upload to a provider; an older browser cannot bypass this check. No automatic transcription fallback. Keep browser speech output behavior unchanged.

## 6. Detailed implementation phases

Each phase ends with a reviewed diff and its tests. Phase 0 is the approval checkpoint; phases 1–6 form Release 1. Phase 7 is a separately accepted account-login milestone.

### Phase 0 — Approve contracts and capture baseline

**Work:** Approve this plan and confirmed scope. Recheck worktrees, relevant wiki fingerprints and source revisions. Record fixtures for Google text/audio/code paths, CLI cancel/failure behavior, onboarding v1 progress and legacy config. Verify official endpoint documentation again. Select the async HTTP version and Ollama release/artifact after ARM64 compatibility review; do not invent checksum/version values in advance.

**Gate:** Existing focused tests pass or failures are documented as pre-existing. Review all nine protected-baseline mismatches against the committed history and record why each is legitimate or needs correction; establish a reviewed baseline before subsequent changes. Provider request/result schemas, error categories, migration precedence and safety limits are reviewed. The pinned Ollama artifact/license/integrity source is identified.

**Rollback:** No runtime changes yet. Stop if a new external service, hardware behavior or unsupported installation requirement appears.

### Phase 1 — Configuration and credential foundation

**Work:** Add provider-independent types, registry, private credential store, profile schema and shared transaction writer. Add read-only legacy resolution and explicit migration. Update secret exclusion/ignore rules and hardware import preservation. Keep Google as the only executable adapter until parity is verified.

**Files:** New `providers/base.py`, `registry.py`, `provider_credentials.py`; existing `config.py`, config/import callers and `.gitignore`; new `tests/test_provider_config.py`, `test_provider_credentials.py` plus `test_config.py`.

**Validation:** Missing/legacy/new/corrupt configs; preserved unrelated fields; missing credentials; permissions from first write; symlink/traversal rejection; concurrent writes; interrupted writes at each transaction boundary; orphan records; environment precedence; public serialization redaction; cancel makes zero writes. Verify no driver imports.

**Gate/rollback:** All schema/transaction cases pass. Restore the previous config/reference without changing hardware configuration if migration fails.

### Phase 2 — Extract Google and integrate the agent boundary

**Work:** Wrap current Google discovery/runtime; replace direct Google dependencies in `NinjaAgent` with the provider interface. Route text, voice and every code-assistance method through it. Move shared parsing to `agent_response.py`; preserve prompts, response envelopes, capability refresh and downstream execution checks. Make logs/errors provider-neutral and redact before exposure.

**Files:** New `providers/google.py`, `agent_response.py`; existing `ninja_agent.py`, Google helper shims and relevant tests.

**Validation:** `test_gemini_models.py`, `test_gemini_runtime.py`, `test_ninja_agent_model.py`, `test_builtin_movements.py`, `test_dispatcher.py`, `test_runtime_pipeline.py`, `test_safe_executor.py`; new shared parser/adversarial fixtures. Verify invalid types, unknown names, 33-entry chains, zero/negative/bool/21 repetitions, malformed/truncated JSON and cancellation produce no unsafe dispatch.

**Gate/rollback:** Google parity on fixtures before enabling another provider. Revert extraction while retaining backward-readable config if parity fails. No live hardware needed.

### Phase 3 — Add OpenAI, Anthropic and Ollama Cloud adapters

**Work:** Add bounded HTTP transport and the three native adapters; implement endpoint-specific authentication, catalog parsers, eligible-model selection and tiny probes. Make capabilities explicit; do not require schema enforcement from Ollama Cloud. Handle Anthropic workspace context and OpenAI mixed output items. Keep optional SDKs out of non-selected provider imports.

**Files:** New `providers/http.py`, `openai.py`, `anthropic.py`, `ollama.py`, provider test modules; owning `pyproject.toml` files and `uv.lock`. Correct the verified Python minimum metadata inconsistency in the same reviewed packaging change.

**Validation:** Mock HTTP contract tests for successful discovery/generation, pagination, empty/duplicate catalogs, malformed payloads, model removal, 401/403/404/429/5xx, quota, timeouts, cancellation, overlarge responses, redirect rejection, refusals and truncated output. Assert keys never appear in captured logs or exception strings. Confirm provider modules import without Google credentials or hardware packages initialized.

**Gate/rollback:** All four adapters pass the same provider contract tests and their endpoint-specific fixtures. Disable/revert an individual new adapter on failure; never automatically reroute a user's request.

### Phase 4 — Shared setup, onboarding and compatibility surfaces

**Work:** Implement `provider_setup.py`, option 1 **“Select AI model”**, `config select-model`, and step 7 **“Select model provider”**. Provider order is Google, OpenAI, Anthropic, Ollama Cloud. Release 1 offers hidden API-key entry, retained-key reuse, back/cancel and model refresh; account-login choices remain unavailable until Phase 7 passes. Prompt for Anthropic workspace ID only when required, with an actionable error on missing context.

Add secret-free provider/model/capability fields to `/api/agent/status` while preserving `active`. Preserve the legacy Google setter with the semantics in §4.4. Gate voice in the Pi0 web UI and backend; update all existing UI locale files for the small new states. No new provider-admin web form.

**Files:** `init_tool.py`, `__main__.py`, `scripts/onboard.py`, `web_server.py`, Agent page/locales, `tests/test_init_tool.py`, `test_cli_entrypoints.py`, `test_upgrade_workflows.py`, `test_lifecycle_refinements.py`, `test_contracts.py`, and new setup/HTTP-handler fixtures.

**Validation:** Both entry points yield identical saved profiles; no hardware import during setup; cancel/EOF/Ctrl-C/failure preserve byte-for-byte active config; stored credentials are never printed. Test old onboarding progress and aliases, skip/resume without a network request, inactive-Google web updates, safe failed hot replacement, unsupported audio and old status clients. Browser fixtures check voice labeling, focus and disabled state using mocked APIs, not a live robot server.

**Gate/rollback:** The exact requested labels and order work for all four providers; previous users can keep Google unchanged. Roll back UI/setup independently, preserving old progress and private snapshots.

### Phase 5 — Automatically install Ollama CLI without local inference

**Work:** Integrate a reviewed, version-pinned ARM64 artifact into `scripts/install-rpi.sh`. Reuse a compatible existing CLI; otherwise stage and verify the download, safely extract only installer-owned files, and publish atomically to an app-owned tools directory. Make the binary discoverable in subsequent normal-user sessions through a controlled launcher/symlink strategy. Record version, origin and integrity hash with existing installation records.

Do not execute the upstream install script unchanged: its service behavior must not violate Pi0's inactive-service rule. Do not run `ollama serve`, `run`, `pull`, `signin`, install GPU support, create model caches, or change an existing user-managed Ollama service. Artifact integrity must come from a reviewed release/checksum/signature source; fail closed if verification is unavailable. Treat CLI installation failure as an incomplete required install stage with a retry path, not a false success.

**Files:** `install.sh` preview/help, `scripts/install-rpi.sh`, `install_check.py`, `install_record.py`, `install-versions.env`, and `install_system.py` only if extraction requires an explicitly listed prerequisite; `tests/test_installer_bootstrap.py` and installer fixtures.

**Validation:** `bash -n`; dry-run has no network/writes; check has no downloads, login or daemon startup; compatible reuse and absent/incompatible CLI; checksum mismatch; bad architecture; low disk; malicious archive paths; interrupted download; retry/idempotency; PATH resolution after a new login. Assert no model download or service activation commands. Real ARM64 acceptance follows in Phase 6.

**Gate/rollback:** Automatic installation works on the target without a local inference daemon or weights. Remove only recorded installer-owned files to roll back; preserve pre-existing Ollama installations and all user data. Direct cloud inference remains independent of the CLI.

### Phase 6 — Release qualification and canonical documentation

**Host checks:** Run focused tests, then the complete Pi0 suite once integration changes settle. Run Ruff on touched Python files, shell syntax checks, and the frontend lint/build/browser fixtures for the capability changes. Use the existing locked environment; do not install dependencies merely to run a planning check.

Planned implementation commands (not executed for this plan):

```bash
uv run --locked pytest tests/test_config.py tests/test_init_tool.py tests/test_gemini_models.py tests/test_gemini_runtime.py tests/test_ninja_agent_model.py -q
uv run --locked pytest tests -q
uv run --locked ruff check ninja_core/src/ninja_core scripts tests
bash -n install.sh onboard.sh scripts/install-rpi.sh
./install.sh --dry-run
python3 scripts/verify_core.py
```

Add new provider-specific tests to the focused command. If repository-wide Ruff already fails, distinguish baseline findings and require touched-code checks to pass. Review protected-source diffs explicitly, then update only approved fingerprints before the final `verify_core.py`; retain the review evidence.

**Owner-controlled Pi acceptance:** On a Zero 2 W/aarch64 installation, record OS/Python/CLI versions, available RAM/disk, dependency footprint and idle/peak RSS. First test installation/check/setup and one harmless text inference per provider using real accounts, with no HAL/server startup. Check expired/revoked key behavior and loss of network. Test supported Google voice separately with an explicitly supplied recording. Confirm incompatible voice is rejected without provider upload. Live probes incur provider usage and require the owner's test credentials through local secret entry, never chat.

**Hardware acceptance:** Only after explicit operator readiness, test a small known movement using the existing safety procedure, then stop/interruption and stale-response rejection. These checks can move servos or activate sound/display; host tests cannot stand in for them. No changes to travel limits or wiring are included.

**Documentation:** Create new complete dated English versions of InstallationGuide, DevelopmentGuide and DevelopmentLog, a new immutable implementation/test evidence note, and updated package README snapshots. Keep root README in its required four-language order; its raw snapshot includes English only. Resolve current versions through `project-knowledge.json`, preserving registered originals. Update the following canonical pages to describe only verified behavior:

- `wiki/concepts/action-library-and-ai-agent.md`
- `wiki/concepts/guided-onboarding.md`
- `wiki/concepts/architecture-and-hal.md`
- `wiki/entities/ninja-core.md`
- `wiki/entities/ninja-webapp.md`
- `wiki/references/api-and-cli-reference.md`
- `wiki/references/installation-guide.md`
- `wiki/references/installation-and-wiring.md`
- `wiki/references/hardware-calibration-and-tools.md`
- `wiki/references/development-guide.md`
- `wiki/analyses/development-history-and-evolution.md`
- `wiki/overview.md`

Use `robot-wiki-maintain`: register/normalize immutable evidence, prepare a schema-v2 plan with current hashes, show its semantic diff, apply the approved in-scope changes and record source-grounded reviews. Regenerate indexes/log through the wiki workflow. Run `check`, `lint --strict`, `link check`, `index check`, `stats`, and search for the newly implemented provider behavior. Education PlatformWiki and Pi5 wiki updates are not required for this Pi0-only scope.

**Release gate:** All criteria in §7 pass, with host/live-account/Pi/hardware results separately recorded. Required target-Pi and controlled hardware checks must pass before calling Release 1 accepted. A build with those checks pending is **evaluation-only, not hardware-qualified**, and is not an accepted robot release. Roll back using §4.4 and the installer-owned file record.

### Phase 7 — Official account-login milestone (later release)

Re-research provider eligibility and exact protocol support before coding. Shared auth work includes expiration, serialized refresh, atomic rotating-token replacement, account binding, logout/revocation guidance, canceled/denied/expired flows, and no browser/credential leakage. API keys remain available.

- **Google:** Implement an installed-app flow using supported Google auth libraries, a maintained client/project and approved scopes. Verify generation as well as listing; document quota-project and verification requirements. Validate a supported SSH/headless procedure without exposing callbacks publicly. Do not auto-install the full Cloud SDK just for login.
- **OpenAI:** Implement the documented ChatGPT open-source registration with PKCE/state/nonce, loopback callback, validated ID-token identity, stable host identity and issued client ID. Scope inference separately from identity. Keep auth-specific model parsing and request parameters; stream into a bounded buffer and validate the completed result. Test SSH loopback forwarding, refresh rotation, denied scopes, workspace/account mismatch and preview restrictions. Do not depend on Codex app-server to execute robot tools.
- **Anthropic:** First qualify the official `ant` CLI for Pi ARM64 and personal interactive use. If suitable, integrate a selected Console profile and the documented credential helper via a bounded subprocess whose token output is captured privately and never logged. Test refresh/profile precedence; keep account/workspace selection stable. Do not read undocumented Claude Code stores or promise consumer subscription access. If unattended deployment is not supported for this route, retain API keys for that mode and document the limit.
- **Ollama:** No account-login implementation is required by the approved Release 1 scope. Reconsider CLI-mediated login only with an explicit decision about its local proxy/service footprint; otherwise keep hosted API-key mode.

**Gate:** Each login route has current official support, target-platform evidence, secure token lifecycle tests and a working authenticated discovery/probe. Ship eligible routes individually; a missing login option must not block the four API-key adapters.

## 7. Acceptance checklist

- [ ] Option 1 and onboarding step 7 show the exact requested labels and the same provider/model flow.
- [ ] All four providers discover live models and save only a successfully probed selection.
- [ ] Anthropic workspace context and provider-specific response/catalog formats are handled correctly.
- [ ] Existing Google configurations, CLI aliases, hardware settings and onboarding progress remain usable.
- [ ] Text and code-assistance operations use the selected provider; no hidden Google dependency or cross-provider fallback.
- [ ] Voice is preserved only where verified; unsupported voice is clearly disabled and blocked server-side.
- [ ] Malformed, refused, truncated, canceled and stale results cannot dispatch unsafe actions.
- [ ] Secrets remain private across input, storage, exports, progress, logs, errors and browser/BLE surfaces.
- [ ] Ollama CLI installs automatically, is available after a fresh login, and no daemon/model download is introduced.
- [ ] Host regression/security/installer checks and required real-provider/Pi/hardware acceptance pass, with separate evidence for each environment.
- [ ] Protected-source baseline changes are reviewed, and canonical wiki updates are applied, lint-clean and retrievable.

## 8. Planning validation and remaining decisions

The three material scope ambiguities (Ollama cloud-only, API keys first, and text-first capability handling) were explicitly confirmed by the owner. Exact HTTP-library/Ollama versions, artifact hashes, model eligibility fixtures and live provider accounts are implementation-stage verification items, not assumed working facts.

JEV was checked without revealing credentials and was **UNCONFIGURED** (`JEV_API_KEY` missing). No JEV request or simulated judgment was used. Repository policy permits continuing with direct evidence; the plan uses official documentation, wiki retrieval, Serena symbol inspection and exact source reads.

Planning checks actually executed: clean Pi0 status baseline; wiki retrieval/source status; knowledge check; strict lint; links; indexes; stats; Git whitespace check; protected-source fingerprint check. The fingerprint check reports the nine pre-existing mismatches listed in §2.2; it did not pass. The new plan is the only worktree change. A fresh-reader review checked scope, rollout, authentication, rollback and safety, and its release-gate ambiguity was corrected. Production inference, OAuth, installation, application regression tests and Raspberry Pi/hardware validation were **not run** for this documentation-only task.

This file is a proposed implementation plan, not a claim that the feature exists. It deliberately does not alter canonical wiki implementation knowledge before code is approved and verified.
