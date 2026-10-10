"""Shared terminal setup; inference probes cannot reach robot execution."""

import asyncio
import json
from pathlib import Path

import click

from .config import AIConfig, AIProfile, CONFIG_FILE_PATH, NinjaConfig
from .private_files import atomic_json, checked_path, config_lock
from .provider_credentials import read_credential, write_credential
from .providers.base import (
    Auth,
    PROVIDERS,
    ProviderError,
    normalize_provider,
    safe_label,
)
from .providers.registry import create_provider


def read_configuration(path):
    path = checked_path(path)
    if not path.exists():
        return NinjaConfig()
    try:
        return NinjaConfig.model_validate_json(path.read_text())
    except (ValueError, OSError):
        raise ProviderError(
            "Invalid saved configuration; retain it and repair before setup"
        ) from None


def commit_profile(provider, model, auth, path=CONFIG_FILE_PATH, *, activate=True):
    """Call only after a successful probe. Credential publication precedes config commit."""
    provider = normalize_provider(provider)
    path = Path(path)
    with config_lock(path):
        config = read_configuration(path)
        if path.exists() and config.ai is None:
            backup = path.with_name("config.pre-provider.json")
            if not backup.exists():
                atomic_json(backup, json.loads(path.read_text()))
        # Never save a key-shaped empty candidate or unchecked model identifier.
        if not auth.key.strip():
            raise ProviderError("API key cannot be empty")
        AIProfile(
            model=model, credential_ref="candidate", workspace_id=auth.workspace_id
        )
        reference = write_credential(provider, auth)
        profile = AIProfile(
            model=model, credential_ref=reference, workspace_id=auth.workspace_id
        )
        profiles = dict(config.ai.profiles) if config.ai else {}
        # Preserve the legacy active Google profile when updating an inactive Google key.
        active = (
            provider if activate or config.ai is None else config.ai.active_provider
        )
        profiles[provider] = profile
        config.ai = AIConfig(active_provider=active, profiles=profiles)
        atomic_json(path, config.model_dump())
    return model


async def validate_and_save(
    provider, model, auth, path=CONFIG_FILE_PATH, *, activate=True
):
    adapter = create_provider(provider, auth)
    await adapter.validate_model(model)
    return commit_profile(provider, model, auth, path, activate=activate)


def configure_ai_model(provider=None, *, api_key=None, path=CONFIG_FILE_PATH):
    config = read_configuration(path)
    if provider is None:
        click.echo("Select AI model provider:")
        for number, label in enumerate(PROVIDERS.values(), 1):
            click.echo(f"{number}. {label}")
        selected = click.prompt(
            "Provider (blank to cancel)", default="", show_default=False
        )
        if not selected:
            return None
        if selected not in ("1", "2", "3", "4"):
            raise ProviderError("Select provider 1–4")
        provider = list(PROVIDERS)[int(selected) - 1]
    provider = normalize_provider(provider)
    profile = config.ai.profiles.get(provider) if config.ai else None
    workspace = profile.workspace_id if profile else None
    if (
        api_key is None
        and profile
        and click.confirm("Reuse saved API key?", default=True)
    ):
        auth = read_credential(provider, profile)
    else:
        key = api_key or click.prompt(
            "API key (blank to cancel)", hide_input=True, default="", show_default=False
        )
        if not key.strip():
            return None
        if provider == "anthropic":
            workspace = (
                click.prompt(
                    "Workspace ID (blank for a single-workspace key)",
                    default=workspace or "",
                    show_default=False,
                )
                or None
            )
        auth = Auth(key.strip(), workspace)
    adapter = create_provider(provider, auth)
    click.echo(f"Retrieving models from {PROVIDERS[provider]}...")
    while True:
        models = asyncio.run(adapter.list_models())
        for index, item in enumerate(models, 1):
            marker = " [current]" if profile and profile.model == item.model_id else ""
            click.echo(
                f"{index}. {safe_label(item.display_name)} ({safe_label(item.model_id)}){marker} — {'voice supported' if item.audio else 'text; voice unavailable'}"
            )
        selected = click.prompt(
            "Select model (R refresh, B provider, blank cancel)",
            default="",
            show_default=False,
        ).lower()
        if selected == "r":
            continue
        if selected == "b":
            return configure_ai_model(path=path)
        if not selected:
            return None
        if not selected.isdigit() or not 1 <= int(selected) <= len(models):
            click.echo("Invalid model selection; refresh or choose a listed model.")
            continue
        model = models[int(selected) - 1].model_id
        break
    click.echo(
        "Validating with a small cloud request (may incur provider charges; up to 60 seconds)..."
    )
    asyncio.run(adapter.validate_model(model))
    commit_profile(provider, model, auth, path)
    click.echo(
        f"Saved {PROVIDERS[provider]} / {safe_label(model)}. Restart the agent/server deliberately to apply."
    )
    return model
