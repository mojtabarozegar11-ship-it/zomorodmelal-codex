"""Django integration for the configured AI provider."""

import os

from django.conf import settings

from ai_engine.deepseek_provider import DeepSeekProvider

from .models import AIConfiguration


def get_deepseek_provider():
    if not getattr(settings, "AI_PROVIDER_ENABLED", False):
        return None

    try:
        config = AIConfiguration.objects.get(provider="deepseek", enabled=True)
    except AIConfiguration.DoesNotExist:
        config = None

    api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    base_url = os.environ.get("DEEPSEEK_BASE_URL", "").strip()
    model = os.environ.get("DEEPSEEK_MODEL", "").strip()

    if config:
        api_key = api_key or config.api_key
        base_url = base_url or config.base_url
        model = model or config.model

    if not api_key:
        return None

    return DeepSeekProvider(
        api_key=api_key,
        base_url=base_url or "https://api.deepseek.com",
        model=model or "deepseek-chat",
    )
