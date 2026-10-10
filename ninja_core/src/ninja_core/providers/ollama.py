from .base import ProviderError
from .cloud import CloudProvider


class OllamaProvider(CloudProvider):
    provider = "ollama"
    origin = "https://ollama.com"
    catalog = "/api/tags"
    endpoint = "/api/chat"

    def payload(self, model, content, system, temperature):
        return {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": content},
            ],
            "stream": False,
            "options": {"num_predict": 2048, "temperature": temperature},
        }

    def extract(self, data):
        if (
            data.get("error")
            or data.get("done") is not True
            or data.get("done_reason") not in (None, "stop")
        ):
            raise ProviderError("Ollama response failed or incomplete")
        message = data.get("message", {})
        if message.get("tool_calls"):
            raise ProviderError("Ollama returned unsupported tool calls")
        return message.get("content", "")
