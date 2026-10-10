"""Provider-neutral contracts. Capabilities are deliberately conservative."""

from dataclasses import dataclass, field
from typing import Literal

ProviderID = Literal["google", "openai", "anthropic", "ollama"]
PROVIDERS = {
    "google": "Google (Gemini)",
    "openai": "OpenAI",
    "anthropic": "Anthropic (Claude)",
    "ollama": "Ollama Cloud",
}
MAX_AUDIO_BYTES = 8 * 1024 * 1024
MAX_RESPONSE_BYTES = 2 * 1024 * 1024


class ProviderError(ValueError):
    """Only safe messages may leave the transport boundary."""


def normalize_provider(value):
    value = "google" if value == "gemini" else value
    if value not in PROVIDERS:
        raise ProviderError("Unknown AI provider")
    return value


@dataclass(frozen=True)
class Auth:
    key: str = field(repr=False)
    workspace_id: str | None = None

    def __post_init__(self):
        if (
            not isinstance(self.key, str)
            or not self.key.strip()
            or len(self.key) > 16384
            or any(ord(c) < 32 or ord(c) > 126 for c in self.key)
        ):
            raise ProviderError("Invalid API key input")
        if self.workspace_id is not None:
            import re

            if not re.fullmatch(r"wrkspc_[A-Za-z0-9]+", self.workspace_id):
                raise ProviderError("Invalid Anthropic workspace ID")


@dataclass(frozen=True)
class ModelOption:
    model_id: str
    display_name: str
    description: str = ""
    audio: bool = False


def safe_label(value):
    import unicodedata

    printable = "".join(
        c for c in str(value) if not unicodedata.category(c).startswith("C")
    )
    return " ".join(printable.split())[:200]
