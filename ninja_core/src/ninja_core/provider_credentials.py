"""Opaque immutable credential records outside the checkout."""

import json
import os
import re
import uuid
from pathlib import Path

from .private_files import atomic_json, checked_path
from .providers.base import Auth, ProviderError


def credential_directory():
    root = Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config")))
    if not root.is_absolute():
        raise ProviderError("XDG_CONFIG_HOME must be an absolute path")
    return checked_path(root / "ninjarobot_pi0" / "credentials")


def write_credential(provider, auth):
    directory = credential_directory()
    directory.mkdir(parents=True, mode=0o700, exist_ok=True)
    directory.chmod(0o700)
    directory.parent.chmod(0o700)
    reference = uuid.uuid4().hex
    atomic_json(
        directory / f"{reference}.json", {"provider": provider, "key": auth.key}
    )
    return reference


def read_credential(provider, profile):
    reference = profile.credential_ref
    if not re.fullmatch(r"[a-f0-9]{32}", reference):
        raise ProviderError("Invalid credential reference")
    path = checked_path(credential_directory() / f"{reference}.json")
    try:
        if path.stat().st_mode & 0o077 or path.stat().st_size > 16384:
            raise ProviderError("Credential record must be private and bounded")
        data = json.loads(path.read_text())
        if (
            data.get("provider") != provider
            or not isinstance(data.get("key"), str)
            or not data["key"].strip()
        ):
            raise ProviderError("Invalid credential record")
        return Auth(data["key"], profile.workspace_id)
    except (OSError, ValueError, TypeError, AttributeError):
        raise ProviderError(
            "AI credential unavailable; run config select-model"
        ) from None


def resolve_profile(config):
    from .config import AIProfile

    if config.ai is None:
        key = config.api_keys.get("gemini")
        if not key:
            raise ProviderError("AI key missing; run ninja_core config select-model")
        return (
            "google",
            AIProfile(model=config.gemini.model, credential_ref="legacy"),
            Auth(key),
        )
    provider = config.ai.active_provider
    profile = config.ai.profiles[provider]
    return provider, profile, read_credential(provider, profile)
