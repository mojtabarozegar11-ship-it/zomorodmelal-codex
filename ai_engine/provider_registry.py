from .deepseek_provider import DeepSeekProvider
from .openai_provider import OpenAIProvider
from .gemini_provider import GeminiProvider
from .claude_provider import ClaudeProvider


class ProviderRegistry:
    def __init__(self):
        self.providers = {
            "openai": OpenAIProvider(),
            "deepseek": DeepSeekProvider(),
            "gemini": GeminiProvider(),
            "claude": ClaudeProvider(),
        }

    def get_all(self):
        return self.providers

    def get_available(self):
        return {
            name: provider
            for name, provider in self.providers.items()
            if provider.available()
        }
