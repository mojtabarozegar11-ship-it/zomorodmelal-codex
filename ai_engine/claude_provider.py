import os
from .base import AIProvider


class ClaudeProvider(AIProvider):
    name = "claude"

    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")

    def available(self):
        return bool(self.api_key)

    def is_available(self):
        return self.available()

    def chat(self, messages, **kwargs):
        if not self.available():
            raise RuntimeError("ANTHROPIC_API_KEY missing")
        return {"provider": self.name, "status": "configured", "messages": messages}
