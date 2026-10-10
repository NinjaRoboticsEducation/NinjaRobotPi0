from .base import ProviderError
from .cloud import CloudProvider


class OpenAIProvider(CloudProvider):
    provider = "openai"
    origin = "https://api.openai.com"
    catalog = "/v1/models"
    endpoint = "/v1/responses"

    def payload(self, model, content, system, temperature):
        return {
            "model": model,
            "instructions": system,
            "input": content,
            "store": False,
            "stream": False,
            "max_output_tokens": 2048,
        }

    def extract(self, data):
        if data.get("status") != "completed" or data.get("error"):
            raise ProviderError("OpenAI response refused, incomplete or failed")
        texts = []
        for item in data.get("output", []):
            if item.get("type") == "message":
                for block in item.get("content", []):
                    if block.get("type") == "refusal":
                        raise ProviderError("OpenAI refused the request")
                    if block.get("type") == "output_text":
                        texts.append(block.get("text", ""))
        return "\n".join(texts)
