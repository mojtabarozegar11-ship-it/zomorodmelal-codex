"""Django integration for provider configuration.

Secrets are read from the database only at runtime and are never returned
by the management API or included in logs.
"""
from django.conf import settings

from ai_engine.deepseek_provider import DeepSeekProvider
from .models import AIConfiguration


def get_deepseek_provider():
    if not getattr(settings, "AI_PROVIDER_ENABLED", False):
        return None

    try:
        config = AIConfiguration.objects.get(provider="deepseek", enabled=True)
    except AIConfiguration.DoesNotExist:
        return None

    if not config.api_key:
        return None

    return DeepSeekProvider(
        api_key=config.api_key,
        base_url=config.base_url,
        model=config.model,
    )
