"""Bounded async HTTPS; never follows authenticated redirects or replays inference."""

import asyncio
import json

import httpx

from .base import MAX_RESPONSE_BYTES, ProviderError

ORIGINS = {
    "https://generativelanguage.googleapis.com",
    "https://api.openai.com",
    "https://api.anthropic.com",
    "https://ollama.com",
}


async def request_json(method, url, *, headers, body=None, params=None, client=None):
    parsed = httpx.URL(url)
    if f"{parsed.scheme}://{parsed.host}" not in ORIGINS or parsed.port not in (
        None,
        443,
    ):
        raise ProviderError("Unapproved provider endpoint")

    async def fetch(session):
        async with session.stream(
            method,
            url,
            headers=headers,
            json=body,
            params=params,
            follow_redirects=False,
        ) as response:
            if response.status_code != 200:
                status = response.status_code
                category = {
                    400: "unsupported request",
                    401: "authentication",
                    403: "permission/workspace",
                    404: "model unavailable",
                    429: "quota/rate limit",
                }.get(status, "service/transport")
                raise ProviderError(f"Provider {category} error (HTTP {status})")
            raw = bytearray()
            async for chunk in response.aiter_bytes():
                raw.extend(chunk)
                if len(raw) > MAX_RESPONSE_BYTES:
                    raise ProviderError("Provider response exceeded size limit")
            try:
                data = json.loads(raw)
            except (ValueError, UnicodeError):
                raise ProviderError("Provider returned malformed JSON") from None
            if not isinstance(data, dict):
                raise ProviderError("Provider returned an invalid response")
            return data

    async def run():
        if client is not None:
            return await fetch(client)
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(60, connect=10), trust_env=False
        ) as session:
            return await fetch(session)

    try:
        return await asyncio.wait_for(run(), timeout=30 if method == "GET" else 60)
    except (httpx.HTTPError, TimeoutError):
        raise ProviderError(
            "Provider request timed out or network unavailable"
        ) from None
