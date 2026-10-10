"""Native async Google setup with the existing Gemini generation controls."""

import asyncio

from ..gemini_runtime import generate_content_text
from .base import ModelOption, ProviderError, safe_label
from .http import request_json


class GoogleProvider:
    def __init__(self, auth, *, client=None):
        self.auth = auth
        self.client = client

    async def list_models(self):
        async def collect():
            token = None
            seen = set()
            result = {}
            for _ in range(20):
                params = {"pageSize": 100}
                if token:
                    params["pageToken"] = token
                data = await request_json(
                    "GET",
                    "https://generativelanguage.googleapis.com/v1beta/models",
                    headers={"x-goog-api-key": self.auth.key},
                    params=params,
                    client=self.client,
                )
                entries = data.get("models", [])
                if not isinstance(entries, list):
                    raise ProviderError("Invalid Google model catalog")
                for item in entries:
                    if not isinstance(item, dict):
                        raise ProviderError("Invalid Google model entry")
                    resource = item.get("name", "")
                    methods = item.get("supportedGenerationMethods", [])
                    if (
                        not isinstance(methods, list)
                        or not isinstance(resource, str)
                        or not resource.startswith("models/gemini-")
                        or "generateContent" not in methods
                    ):
                        continue
                    model = item.get("baseModelId") or resource.removeprefix("models/")
                    if (
                        not isinstance(model, str)
                        or len(model) > 200
                        or any(ord(c) < 32 for c in model)
                    ):
                        continue
                    result[model] = ModelOption(
                        model,
                        safe_label(item.get("displayName", model)),
                        safe_label(item.get("description", "")),
                        self.supports_audio(model),
                    )
                    if len(result) > 2000:
                        raise ProviderError("Google model catalog exceeded limit")
                token = data.get("nextPageToken")
                if not token:
                    break
                if not isinstance(token, str) or token in seen:
                    raise ProviderError("Invalid Google pagination")
                seen.add(token)
            else:
                raise ProviderError("Google pagination exceeded limit")
            if not result:
                raise ProviderError("No suitable Gemini models available")
            return sorted(
                result.values(), key=lambda item: item.display_name.casefold()
            )

        try:
            return await asyncio.wait_for(collect(), 30)
        except TimeoutError:
            raise ProviderError("Google model discovery timed out") from None

    async def validate_model(self, model):
        await generate_content_text(
            self.auth.key,
            model,
            [{"text": "Reply with exactly: OK"}],
            temperature=0.0,
            max_output_tokens=128,
            timeout=60,
        )

    def supports_audio(self, model):
        # Known existing native-audio paths; new/unknown model IDs stay text-only.
        return model in {
            "gemini-2.0-flash",
            "gemini-2.0-flash-001",
            "gemini-2.5-flash",
            "gemini-2.5-pro",
            "gemini-3-flash-preview",
        }

    async def generate(self, model, content, *, system="", temperature=0.7):
        if not isinstance(content, str):
            raise ProviderError("Use the qualified agent audio path for recorded audio")
        return await generate_content_text(
            self.auth.key,
            model,
            [{"text": content}],
            system_instruction=system,
            temperature=temperature,
        )
