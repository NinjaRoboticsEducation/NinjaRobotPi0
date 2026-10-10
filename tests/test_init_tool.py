from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner
from ninja_core.provider_credentials import resolve_profile

from ninja_core.__main__ import main
from ninja_core.config import load_config, save_config
from ninja_core.gemini_models import (
    GeminiModelDiscoveryError,
    GeminiModelOption,
)
from ninja_core.gemini_runtime import GeminiRuntimeError


@pytest.fixture(autouse=True)
def private_credentials(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "credentials-home"))


def _model_options():
    return [
        GeminiModelOption(
            model_id="gemini-alpha",
            display_name="Gemini Alpha",
            description="Fast model",
        ),
        GeminiModelOption(
            model_id="gemini-beta",
            display_name="Gemini Beta",
            description="Capable model",
        ),
    ]


def test_init_tool_exits_cleanly():
    runner = CliRunner()

    result = runner.invoke(main, ["init-tool"], input="8\n")

    assert result.exit_code == 0
    assert "Initialization Tool" in result.output
    assert "Exiting NinjaRobotV5 initialization tool." in result.output


def test_init_tool_selects_robot_type():
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(main, ["init-tool"], input="4\n2\n8\n")

        assert result.exit_code == 0
        assert load_config().robot_type == "humanoid"


def test_init_tool_shows_sanitized_hardware_configuration(monkeypatch, tmp_path):
    from unittest.mock import AsyncMock, Mock
    from ninja_core.providers.base import ModelOption

    adapter = Mock()
    adapter.list_models = AsyncMock(
        return_value=[
            ModelOption("gemini-alpha", "Alpha"),
            ModelOption("gemini-beta", "Beta"),
        ]
    )
    adapter.validate_model = AsyncMock()
    monkeypatch.setattr(
        "ninja_core.provider_setup.create_provider", lambda *args: adapter
    )
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    runner = CliRunner()
    monkeypatch.setattr(
        "ninja_core.init_tool.list_available_gemini_models",
        lambda key: _model_options(),
    )
    monkeypatch.setattr(
        "ninja_core.init_tool.validate_gemini_model",
        lambda key, model: None,
    )

    with runner.isolated_filesystem():
        result = runner.invoke(
            main,
            ["init-tool"],
            input="1\n1\nsuper-secret-key\n2\n6\n8\n",
        )

        assert result.exit_code == 0
        assert "hardware_configuration" in result.output
        assert "super-secret-key" not in result.output
        assert "api_keys" not in result.output


def test_config_set_key_gemini_selects_and_persists_model(monkeypatch):
    runner = CliRunner()
    validated = []
    monkeypatch.setattr(
        "ninja_core.init_tool.list_available_gemini_models",
        lambda key: _model_options(),
    )
    monkeypatch.setattr(
        "ninja_core.init_tool.validate_gemini_model",
        lambda key, model: validated.append(model),
    )

    with runner.isolated_filesystem():
        result = runner.invoke(
            main,
            ["config", "set-key", "gemini", "super-secret-key"],
            input="2\n",
        )

        assert result.exit_code == 0
        config = load_config()
        provider, profile, auth = resolve_profile(config)
        assert provider == "google"
        assert auth.key == "super-secret-key"
        assert profile.model == "gemini-beta"
        assert "super-secret-key" not in Path("config.json").read_text()
        assert validated == ["gemini-beta"]
        assert "super-secret-key" not in result.output
        assert "Gemini Beta" in result.output


def test_config_set_key_gemini_validation_failure_preserves_existing_config(
    monkeypatch,
):
    runner = CliRunner()
    monkeypatch.setattr(
        "ninja_core.init_tool.list_available_gemini_models",
        lambda key: _model_options(),
    )

    def fail_validation(key, model):
        raise GeminiRuntimeError("selected model did not respond")

    monkeypatch.setattr(
        "ninja_core.init_tool.validate_gemini_model",
        fail_validation,
    )

    with runner.isolated_filesystem():
        config = load_config()
        config.api_keys["gemini"] = "working-key"
        config.gemini.model = "gemini-working"
        save_config(config)
        config_path = Path("config.json")
        before = config_path.read_bytes()

        result = runner.invoke(
            main,
            ["config", "set-key", "gemini", "replacement-key"],
            input="2\n",
        )

        assert result.exit_code != 0
        assert "selected model did not respond" in result.output
        assert config_path.read_bytes() == before
        assert "replacement-key" not in result.output


def test_config_set_key_gemini_failure_preserves_existing_config(monkeypatch):
    runner = CliRunner()

    def fail_lookup(key):
        raise GeminiModelDiscoveryError("lookup failed")

    monkeypatch.setattr(
        "ninja_core.init_tool.list_available_gemini_models",
        fail_lookup,
    )

    with runner.isolated_filesystem():
        config = load_config()
        config.api_keys["gemini"] = "working-key"
        config.gemini.model = "gemini-working"
        save_config(config)
        config_path = Path("config.json")
        before = config_path.read_bytes()

        result = runner.invoke(
            main,
            ["config", "set-key", "gemini", "replacement-key"],
        )

        assert result.exit_code != 0
        assert "lookup failed" in result.output
        assert config_path.read_bytes() == before
        assert "replacement-key" not in result.output


def test_config_set_key_gemini_cancel_does_not_create_config(monkeypatch):
    runner = CliRunner()
    monkeypatch.setattr(
        "ninja_core.init_tool.list_available_gemini_models",
        lambda key: _model_options(),
    )

    with runner.isolated_filesystem():
        result = runner.invoke(
            main,
            ["config", "set-key", "gemini", "super-secret-key"],
            input="",
        )

        assert result.exit_code != 0
        assert Path("config.json").exists() is False
        assert "super-secret-key" not in result.output


def test_config_set_key_non_gemini_keeps_generic_behavior():
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(
            main,
            ["config", "set-key", "another-service", "service-key"],
        )

        assert result.exit_code == 0
        assert load_config().api_keys["another-service"] == "service-key"
