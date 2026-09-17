import os

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class DeepSeekProvider:
    """DeepSeek API provider compatible with OpenAI SDK."""

    name = "deepseek"

    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        self.base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        self.client = None
        if self.api_key and OpenAI:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def is_available(self):
        return self.client is not None

    def chat(self, messages, **kwargs):
        if not self.client:
            raise RuntimeError("DEEPSEEK_API_KEY is not configured")
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
