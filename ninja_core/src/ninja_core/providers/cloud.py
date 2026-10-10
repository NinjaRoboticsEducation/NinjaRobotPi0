"""Native hosted API adapters. Model access is confirmed by a selected-model probe."""

import asyncio

from .base import ModelOption, ProviderError, safe_label
from .http import request_json


class CloudProvider:
    provider = ""
    origin = ""
    catalog = ""
    endpoint = ""

    def __init__(self, auth, *, client=None):
        self.auth = auth
        self.client = client

    def headers(self):
        headers = {
            "Authorization": f"Bearer {self.auth.key}",
            "Content-Type": "application/json",
        }
        if self.provider == "anthropic":
            headers["anthropic-version"] = "2023-06-01"
            if self.auth.workspace_id:
                headers["anthropic-workspace-id"] = self.auth.workspace_id
        return headers

    async def call(self, method, path, *, body=None, params=None):
        return await request_json(
            method,
            self.origin + path,
            headers=self.headers(),
            body=body,
            params=params,
            client=self.client,
        )

    async def list_models(self):
        async def collect():
            result = {}
            token = None
            seen = set()
            for _ in range(20):
                params = {"after_id": token, "limit": 100} if token else None
                data = await self.call("GET", self.catalog, params=params)
                entries = data.get("models" if self.provider == "ollama" else "data")
                if not isinstance(entries, list):
                    raise ProviderError("Provider returned an invalid model catalog")
                for item in entries:
                    if not isinstance(item, dict):
                        raise ProviderError("Provider returned an invalid model entry")
                    model = item.get("name" if self.provider == "ollama" else "id")
                    if (
                        not isinstance(model, str)
                        or not model
                        or len(model) > 200
                        or any(ord(c) < 32 for c in model)
                    ):
                        continue
                    if item.get("lifecycle") in ("retired", "deprecated"):
                        continue
                    # Catalogs include embeddings, speech and image endpoints; these cannot plan actions.
                    if self.provider == "openai" and any(
                        term in model.lower()
                        for term in (
                            "embedding",
                            "tts",
                            "whisper",
                            "transcribe",
                            "realtime",
                            "audio",
                            "image",
                            "dall-e",
                            "moderation",
                            "sora",
                            "search",
                        )
                    ):
                        continue
                    result[model] = ModelOption(
                        model, safe_label(item.get("display_name", model))
                    )
                    if len(result) > 2000:
                        raise ProviderError("Provider catalog exceeded model limit")
                if not data.get("has_more"):
                    break
                token = data.get("last_id")
                if (
                    self.provider != "anthropic"
                    or not isinstance(token, str)
                    or token in seen
                ):
                    raise ProviderError("Invalid provider pagination")
                seen.add(token)
            else:
                raise ProviderError("Provider pagination exceeded limit")
            if not result:
                raise ProviderError("No suitable text models available")
            return sorted(
                result.values(), key=lambda item: item.display_name.casefold()
            )

        try:
            return await asyncio.wait_for(collect(), 30)
        except TimeoutError:
            raise ProviderError("Model discovery timed out") from None

    async def generate(self, model, content, *, system="", temperature=0.7):
        if not isinstance(content, str):
            raise ProviderError("Voice unavailable for this provider/model")
        body = self.payload(model, content, system, temperature)
        data = await self.call("POST", self.endpoint, body=body)
        try:
            text = self.extract(data)
        except (TypeError, AttributeError, KeyError):
            raise ProviderError(
                "Provider returned an invalid inference response"
            ) from None
        if not isinstance(text, str) or not text.strip():
            raise ProviderError("Provider returned no visible text")
        return text

    async def validate_model(self, model):
        await self.generate(
            model,
            'Reply with exactly {"response":"OK"}.',
            system="No tools or actions. Only reply to this test.",
            temperature=0.1,
        )

    def supports_audio(self, model):
        return False
