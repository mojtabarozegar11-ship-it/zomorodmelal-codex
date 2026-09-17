from .provider_registry import ProviderRegistry


def ai_provider_status():
    registry = ProviderRegistry()
    result = {}

    for name, provider in registry.get_all().items():
        try:
            result[name] = "active" if provider.available() else "inactive"
        except Exception:
            result[name] = "error"

    return result


def format_ai_status():
    status = ai_provider_status()
    return "\n".join([f"{name}: {state}" for name, state in status.items()])
