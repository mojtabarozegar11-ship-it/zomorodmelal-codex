"""Compatibility manager backed by the canonical ai_engine provider registry."""
from ai_engine.provider_registry import ProviderRegistry


class AIProviderManager:
    def __init__(self):
        self.registry = ProviderRegistry()
        self.active_provider = "deepseek"

    @property
    def providers(self):
        return self.registry.get_all()

    def use(self, name):
        if name not in self.providers:
            return False
        self.active_provider = name
        return True

    def generate(self, prompt):
        provider = self.providers[self.active_provider]
        return provider.chat([{"role": "user", "content": prompt}])

    def status(self):
        return {
            "active": self.active_provider,
            "providers": {
                name: {
                    "available": bool(p.available() if hasattr(p, "available") else p.is_available())
                }
                for name, p in self.providers.items()
            },
        }
