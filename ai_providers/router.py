import os

from .deepseek_provider import DeepSeekProvider


class AIRouter:
    def __init__(self):
        self.providers = {
            "deepseek": DeepSeekProvider(),
        }

    def get_provider(self, task_type=None):
        preferred = os.getenv("AI_PROVIDER", "deepseek")
        provider = self.providers.get(preferred)
        if provider and provider.is_available():
            return provider
        for item in self.providers.values():
            if item.is_available():
                return item
        return None

    def chat(self, messages, task_type=None, **kwargs):
        provider = self.get_provider(task_type)
        if not provider:
            raise RuntimeError("No AI provider configured")
        return provider.chat(messages, **kwargs)
