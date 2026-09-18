import os
from .base import AIProvider

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


class OpenAIProvider(AIProvider):
    name = "openai"

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=self.api_key) if self.api_key and OpenAI else None

    def available(self):
        return self.client is not None

    def is_available(self):
        return self.available()

    def chat(self, messages, **kwargs):
        if not self.client:
            raise RuntimeError("OPENAI_API_KEY missing")
        return self.client.chat.completions.create(
            model=kwargs.get("model", self.model),
            messages=messages,
            **{k:v for k,v in kwargs.items() if k != "model"},
        )
