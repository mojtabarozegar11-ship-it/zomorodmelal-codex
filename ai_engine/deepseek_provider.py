import os
from .base import AIProvider

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


class DeepSeekProvider(AIProvider):
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.client = None
        if self.api_key and OpenAI:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
            )

    @property
    def name(self):
        return "deepseek"

    def available(self):
        return self.client is not None

    def chat(self, messages, **kwargs):
        return self.client.chat.completions.create(
            model=kwargs.get("model", "deepseek-chat"),
            messages=messages
        )
