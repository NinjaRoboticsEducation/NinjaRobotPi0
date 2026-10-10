"""Offline transport, transactional setup and robot-plan regression tests."""

import asyncio
import json
from pathlib import Path
from unittest.mock import AsyncMock, Mock

import httpx
import pytest
from click.testing import CliRunner

from ninja_core.config import AIConfig, AIProfile, NinjaConfig
from ninja_core.provider_credentials import read_credential
from ninja_core.provider_setup import (
    commit_profile,
    configure_ai_model,
    read_configuration,
)
from ninja_core.providers.base import (
    Auth,
    ModelOption,
    ProviderError,
    MAX_RESPONSE_BYTES,
)
from ninja_core.providers.openai import OpenAIProvider
from ninja_core.providers.anthropic import AnthropicProvider
from ninja_core.providers.ollama import OllamaProvider
from ninja_core.providers.http import request_json
from ninja_core.agent_response import parse_plan, InvalidPlan


@pytest.fixture(autouse=True)
def private_home(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "user-config"))


@pytest.mark.parametrize(
    "adapter,body",
    [
        (
            OpenAIProvider,
            {
                "status": "completed",
                "output": [
                    {"type": "reasoning"},
                    {
                        "type": "message",
                        "content": [{"type": "output_text", "text": "hello"}],
                    },
                ],
            },
        ),
        (
            AnthropicProvider,
            {"stop_reason": "end_turn", "content": [{"type": "text", "text": "hello"}]},
        ),
        (
            OllamaProvider,
            {"done": True, "done_reason": "stop", "message": {"content": "hello"}},
        ),
    ],
)
def test_auth_catalog_and_inference(adapter, body):
    seen = []

    def handler(request):
        seen.append(request)
        assert request.headers["authorization"] == "Bearer inert-key"
        if request.method == "GET":
            if adapter is OllamaProvider:
                return httpx.Response(
                    200, json={"models": [{"name": "exact:cloud-id"}]}
                )
            return httpx.Response(200, json={"data": [{"id": "text-model"}]})
        payload = json.loads(request.content)
        assert "format" not in payload
        return httpx.Response(200, json=body)

    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            provider = adapter(Auth("inert-key", "wrkspc_test"), client=client)
            models = await provider.list_models()
            assert len(models) == 1
            assert not provider.supports_audio(models[0].model_id)
            assert (
                await provider.generate(models[0].model_id, "hi", system="prompt")
                == "hello"
            )

    asyncio.run(run())
    if adapter is AnthropicProvider:
        assert seen[0].headers["anthropic-workspace-id"] == "wrkspc_test"
        assert seen[0].headers["anthropic-version"] == "2023-06-01"


@pytest.mark.parametrize("status", [301, 400, 401, 403, 404, 429, 500])
def test_safe_transport_errors_and_no_redirect(status):
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(
            status,
            headers={"location": "https://evil.invalid"},
            text="secret-key provider raw error",
        )

    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            with pytest.raises(ProviderError) as exc:
                await request_json(
                    "POST",
                    "https://api.openai.com/v1/responses",
                    headers={"Authorization": "Bearer secret-key"},
                    body={},
                    client=client,
                )
            assert "secret-key" not in str(exc.value)
            assert "raw error" not in str(exc.value)

    asyncio.run(run())
    assert len(seen) == 1


@pytest.mark.parametrize("data", [[], "bad", {"too_big": "x" * MAX_RESPONSE_BYTES}])
def test_invalid_bounded_response(data):
    async def run():
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(lambda r: httpx.Response(200, json=data))
        ) as client:
            with pytest.raises(ProviderError):
                await request_json(
                    "GET", "https://ollama.com/api/tags", headers={}, client=client
                )

    asyncio.run(run())


def test_anthropic_pagination_rejects_repeat():
    async def run():
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(
                lambda r: httpx.Response(
                    200, json={"data": [], "has_more": True, "last_id": "same"}
                )
            )
        ) as client:
            with pytest.raises(ProviderError, match="pagination"):
                await AnthropicProvider(Auth("inert"), client=client).list_models()

    asyncio.run(run())


@pytest.mark.parametrize(
    "adapter,data",
    [
        (OpenAIProvider, {"status": "incomplete"}),
        (AnthropicProvider, {"stop_reason": "max_tokens"}),
        (OllamaProvider, {"done": True, "done_reason": "length"}),
    ],
)
def test_truncation_never_becomes_text(adapter, data):
    with pytest.raises(ProviderError):
        adapter(Auth("inert")).extract(data)


def test_profile_commit_permissions_preserves_legacy(tmp_path):
    path = tmp_path / "config.json"
    prior = NinjaConfig(
        api_keys={"gemini": "legacy-key"},
        gemini={"model": "gemini-old"},
        movements={"wave": []},
    )
    path.write_text(prior.model_dump_json())
    commit_profile("openai", "exact-model", Auth("new-secret"), path)
    saved = read_configuration(path)
    assert saved.movements == prior.movements
    assert saved.api_keys == prior.api_keys
    assert saved.ai.active_provider == "openai"
    assert "new-secret" not in path.read_text()
    assert path.stat().st_mode & 0o777 == 0o600
    profile = saved.ai.profiles["openai"]
    assert read_credential("openai", profile).key == "new-secret"
    assert (tmp_path / "config.pre-provider.json").stat().st_mode & 0o777 == 0o600
    assert (
        commit_profile("google", "gemini-new", Auth("google-new"), path, activate=False)
        == "gemini-new"
    )
    assert read_configuration(path).ai.active_provider == "openai"


def test_cancel_and_probe_failure_never_write(tmp_path, monkeypatch):
    path = tmp_path / "config.json"
    adapter = Mock()
    adapter.list_models = AsyncMock(return_value=[ModelOption("model", "Model")])
    adapter.validate_model = AsyncMock(side_effect=ProviderError("probe failed"))
    monkeypatch.setattr("ninja_core.provider_setup.create_provider", lambda *a: adapter)
    runner = CliRunner()
    import click

    @click.command()
    def command():
        configure_ai_model("openai", path=path)

    result = runner.invoke(command, input="secret\n\n")
    assert result.exit_code == 0
    assert not path.exists()
    result = runner.invoke(command, input="secret\n1\n")
    assert result.exit_code != 0
    assert not path.exists()
    assert "secret" not in result.output
    assert not (tmp_path / "user-config").exists()


def test_symlink_configuration_rejected(tmp_path):
    target = tmp_path / "target"
    target.write_text("{}")
    link = tmp_path / "config.json"
    link.symlink_to(target)
    with pytest.raises(ValueError):
        commit_profile("openai", "model", Auth("key"), link)
    assert target.read_text() == "{}"


def test_schema_corruption_no_fallback():
    with pytest.raises(ValueError):
        NinjaConfig(ai={"version": 2, "active_provider": "openai", "profiles": {}})
    with pytest.raises(ValueError):
        AIConfig(active_provider="openai", profiles={})


CAPS = {
    "movements": ["home"],
    "actions": ["dance"],
    "faces": ["happy", "speaking"],
    "sounds": ["happy", "speaking"],
}


@pytest.mark.parametrize(
    "plan",
    [
        {"chain": [{"name": "home", "repetitions": True}]},
        {"chain": [{"name": "home", "repetitions": 21}]},
        {"chain": [{"name": "home"}] * 33},
        {"action_chain": [{"name": "unknown"}]},
        {"face_chain": [{"name": "happy", "duration": float("nan")}]},
        {"sound_chain": ["unknown"]},
        {"movement": "unknown"},
        {"code": "robot.move()"},
    ],
)
def test_whole_plan_validation(plan):
    with pytest.raises(InvalidPlan):
        parse_plan(json.dumps(plan), CAPS)


def test_non_google_agent_stale_result_and_voice(tmp_path, monkeypatch):
    from ninja_core.ninja_agent import NinjaAgent

    path = tmp_path / "config.json"
    commit_profile("ollama", "cloud-model", Auth("inert"), path)
    monkeypatch.setattr(NinjaAgent, "_load_robot_capabilities", lambda *a: CAPS)
    agent = NinjaAgent(read_configuration(path), Mock())
    assert agent.provider_name == "ollama" and agent.model is None
    assert not agent.supports_audio

    async def run():
        started = asyncio.Event()
        release = asyncio.Event()

        async def generate(*args, **kwargs):
            started.set()
            await release.wait()
            return '{"movement":"home","response":"ok"}'

        agent.provider.generate = generate
        task = asyncio.create_task(agent.process_command("move"))
        await started.wait()
        agent.cancel_pending()
        release.set()
        assert (await task)["action_plan"] == {}
        assert (await agent.process_audio_command("nonexistent"))["action_plan"] == {}

    asyncio.run(run())


def test_atomic_publish_failure_preserves_active_configuration(tmp_path, monkeypatch):
    import ninja_core.provider_setup as setup

    path = tmp_path / "config.json"
    commit_profile("openai", "working", Auth("working-key"), path)
    prior = path.read_bytes()
    original = setup.atomic_json

    def fail_config(target, value):
        if Path(target) == path:
            raise OSError("disk failure")
        return original(target, value)

    monkeypatch.setattr(setup, "atomic_json", fail_config)
    with pytest.raises(OSError):
        commit_profile("ollama", "new-model", Auth("new-key"), path)
    assert path.read_bytes() == prior
    assert (
        read_credential("openai", read_configuration(path).ai.profiles["openai"]).key
        == "working-key"
    )


def test_private_credential_bad_permissions_and_reference(tmp_path):
    from ninja_core.provider_credentials import credential_directory

    path = tmp_path / "config.json"
    commit_profile("openai", "model", Auth("key"), path)
    profile = read_configuration(path).ai.profiles["openai"]
    record = credential_directory() / f"{profile.credential_ref}.json"
    record.chmod(0o644)
    with pytest.raises(ProviderError):
        read_credential("openai", profile)
    with pytest.raises(ProviderError):
        read_credential("openai", AIProfile(model="model", credential_ref="../escape"))


def test_discovery_failure_no_configuration(tmp_path, monkeypatch):
    adapter = Mock(list_models=AsyncMock(side_effect=ProviderError("unauthorized")))
    monkeypatch.setattr("ninja_core.provider_setup.create_provider", lambda *a: adapter)
    import click

    @click.command()
    def command():
        configure_ai_model("openai", path=tmp_path / "config.json")

    result = CliRunner().invoke(command, input="secret\n")
    assert result.exit_code != 0
    assert "secret" not in result.output
    assert not (tmp_path / "config.json").exists()


def test_provider_setup_has_no_hardware_imports():
    import subprocess
    import sys

    script = "import sys; import ninja_core.provider_setup; assert not any(n in sys.modules for n in ('ninja_core.hal','ninja_core.web_server','ninja_core.dispatcher','pi0servo'))"
    env = dict(__import__("os").environ)
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "ninja_core/src")
    result = subprocess.run(
        [sys.executable, "-B", "-c", script], env=env, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr


def test_google_native_discovery_headers_and_filtering():
    from ninja_core.providers.google import GoogleProvider

    seen = []

    def handler(request):
        seen.append(request)
        assert request.headers["x-goog-api-key"] == "inert"
        assert "inert" not in str(request.url)
        return httpx.Response(
            200,
            json={
                "models": [
                    {
                        "name": "models/gemini-3.7-flash",
                        "displayName": "Flash",
                        "supportedGenerationMethods": ["generateContent"],
                    },
                    {
                        "name": "models/embedding",
                        "supportedGenerationMethods": ["embedContent"],
                    },
                ]
            },
        )

    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            models = await GoogleProvider(Auth("inert"), client=client).list_models()
            assert [(m.model_id, m.audio) for m in models] == [
                ("gemini-3.7-flash", False)
            ]

    asyncio.run(run())
    assert len(seen) == 1


def test_async_google_generation_and_truncation(monkeypatch):
    from ninja_core.gemini_runtime import generate_content_text, GeminiRuntimeError

    seen = []

    async def request(method, url, **kwargs):
        seen.append(kwargs)
        return {
            "candidates": [
                {"finishReason": "STOP", "content": {"parts": [{"text": "OK"}]}}
            ]
        }

    monkeypatch.setattr("ninja_core.providers.http.request_json", request)
    assert (
        asyncio.run(
            generate_content_text("inert", "gemini-3.7-flash", [{"text": "hi"}])
        )
        == "OK"
    )
    assert seen[0]["body"]["generationConfig"]["thinkingConfig"] == {
        "thinkingLevel": "low"
    }

    async def incomplete(*args, **kwargs):
        return {
            "candidates": [
                {
                    "finishReason": "MAX_TOKENS",
                    "content": {"parts": [{"text": '{"movement":"home"}'}]},
                }
            ]
        }

    monkeypatch.setattr("ninja_core.providers.http.request_json", incomplete)
    with pytest.raises(GeminiRuntimeError, match="MAX_TOKENS"):
        asyncio.run(
            generate_content_text("inert", "gemini-3.7-flash", [{"text": "hi"}])
        )


def test_cancellation_closes_http_stream():
    closed = []

    class SlowStream(httpx.AsyncByteStream):
        async def __aiter__(self):
            await asyncio.sleep(10)
            yield b"{}"

        async def aclose(self):
            closed.append(True)

    async def run():
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(
                lambda r: httpx.Response(200, stream=SlowStream())
            )
        ) as client:
            with pytest.raises(TimeoutError):
                await asyncio.wait_for(
                    request_json(
                        "POST",
                        "https://ollama.com/api/chat",
                        headers={},
                        body={},
                        client=client,
                    ),
                    0.02,
                )

    asyncio.run(run())
    assert closed == [True]


def test_concurrent_profile_writers_preserve_both(tmp_path):
    from concurrent.futures import ThreadPoolExecutor

    path = tmp_path / "config.json"
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [
            pool.submit(commit_profile, p, "model", Auth("inert"), path)
            for p in ("openai", "ollama")
        ]
        for future in futures:
            assert future.result() == "model"
    assert set(read_configuration(path).ai.profiles) == {"openai", "ollama"}


def test_stale_plan_waiting_for_execution_lock_is_discarded(monkeypatch):
    from types import SimpleNamespace
    from ninja_core import web_server

    execute = AsyncMock()
    monkeypatch.setattr(web_server, "session_active", lambda state: True)
    monkeypatch.setattr(web_server, "_execute_action_plan_unlocked", execute)

    async def run():
        agent = SimpleNamespace(_generation=1)
        state = SimpleNamespace(agent=agent, action_plan_lock=asyncio.Lock())
        await state.action_plan_lock.acquire()
        task = asyncio.create_task(
            web_server.execute_action_plan(
                state, {"movement": "home"}, agent=agent, generation=1
            )
        )
        await asyncio.sleep(0)
        agent._generation = 2
        state.action_plan_lock.release()
        await task

    asyncio.run(run())
    execute.assert_not_awaited()


def test_unsupported_voice_rejected_before_hardware_or_file_read(monkeypatch):
    from types import SimpleNamespace
    from fastapi import HTTPException
    from ninja_core import web_server

    interaction = AsyncMock()
    monkeypatch.setattr(web_server, "handle_first_interaction", interaction)
    state = SimpleNamespace(agent=SimpleNamespace(supports_audio=False))
    request = SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(ninja=state)))
    file = Mock()
    with pytest.raises(HTTPException, match="Voice unavailable"):
        asyncio.run(web_server.agent_voice(request, file))
    interaction.assert_not_awaited()
    file.read.assert_not_called()
