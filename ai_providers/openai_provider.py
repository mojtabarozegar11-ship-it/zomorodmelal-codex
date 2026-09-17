from .base_provider import BaseAIProvider

class OpenAIProvider(BaseAIProvider):

    def __init__(self):
        self.name = "OpenAI"

    def generate(self, prompt: str) -> str:
        return "OpenAI provider ready"

    def status(self):
        return {
            "provider": self.name,
            "status": "ready"
        }
