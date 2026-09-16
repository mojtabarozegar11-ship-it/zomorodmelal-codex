import os
from .base import AIProvider

class ClaudeProvider(AIProvider):
    name = "claude"

    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")

    def is_available(self):
        return bool(self.api_key)

    def chat(self, messages, **kwargs):
        if not self.is_available():
            raise RuntimeError("ANTHROPIC_API_KEY missing")
        return {"provider": self.name, "status": "ready"}
