from .base import normalize_provider


def create_provider(provider, auth):
    provider = normalize_provider(provider)
    if provider == "google":
        from .google import GoogleProvider

        return GoogleProvider(auth)
    if provider == "openai":
        from .openai import OpenAIProvider

        return OpenAIProvider(auth)
    if provider == "anthropic":
        from .anthropic import AnthropicProvider

        return AnthropicProvider(auth)
    from .ollama import OllamaProvider

    return OllamaProvider(auth)
