"""Compatibility adapter: ai_providers now delegates to canonical ai_engine providers."""
from .registry import get_providers


def get_canonical_provider(name):
    return get_providers().get(name)


def provider_status(name):
    provider = get_canonical_provider(name)
    if provider is None:
        return {"provider": name, "status": "unknown"}
    available = provider.available() if hasattr(provider, "available") else provider.is_available()
    return {"provider": name, "available": bool(available)}
