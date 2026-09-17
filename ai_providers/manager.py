from .deepseek_provider import DeepSeekProvider
from .openai_provider import OpenAIProvider


class AIProviderManager:

    def __init__(self):
        self.providers = {
            "deepseek": DeepSeekProvider(),
            "openai": OpenAIProvider()
        }
        self.active_provider = "deepseek"

    def use(self, name):
        if name in self.providers:
            self.active_provider = name
            return True
        return False

    def generate(self, prompt):
        provider = self.providers[self.active_provider]
        return provider.generate(prompt)

    def status(self):
        return {
            "active": self.active_provider,
            "providers": {
                name: provider.status()
                for name, provider in self.providers.items()
            }
        }
