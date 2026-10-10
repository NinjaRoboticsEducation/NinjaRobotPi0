from .base import ProviderError
from .cloud import CloudProvider


class AnthropicProvider(CloudProvider):
    provider = "anthropic"
    origin = "https://api.anthropic.com"
    catalog = "/v1/models"
    endpoint = "/v1/messages"

    def payload(self, model, content, system, temperature):
        return {
            "model": model,
            "system": system,
            "messages": [{"role": "user", "content": content}],
            "max_tokens": 2048,
        }

    def extract(self, data):
        if data.get("stop_reason") not in ("end_turn", "stop_sequence"):
            raise ProviderError(
                "Anthropic response refused, incomplete or requires unsupported tools"
            )
        return "\n".join(
            block.get("text", "")
            for block in data.get("content", [])
            if block.get("type") == "text"
        )
