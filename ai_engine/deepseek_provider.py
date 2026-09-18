import os
from .base import AIProvider

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


class DeepSeekProvider(AIProvider):
    def __init__(self, api_key=None, base_url=None, model=None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.base_url = base_url or os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        self.model = model or os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url) if self.api_key and OpenAI else None

    @property
    def name(self):
        return "deepseek"

    def available(self):
        return self.client is not None

    def is_available(self):
        return self.available()

    def chat(self, messages, **kwargs):
        if not self.client:
            raise RuntimeError("DeepSeek provider is not configured")
        return self.client.chat.completions.create(
            model=kwargs.get("model", self.model),
            messages=messages,
            **{k:v for k,v in kwargs.items() if k != "model"},
        )
