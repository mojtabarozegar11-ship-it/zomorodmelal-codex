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
        self.model = model or "deepseek-chat"
        self.client = None
        if self.api_key and OpenAI:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    @property
    def name(self):
        return "deepseek"

    def available(self):
        return self.client is not None

    def chat(self, messages, **kwargs):
        if not self.client:
            raise RuntimeError("DeepSeek provider is not configured")
        return self.client.chat.completions.create(
            model=kwargs.get("model", self.model),
            messages=messages,
        )


    def generate_json(self, *, system, user):
        import json

        response = self.chat(
            [
                {"role": "system", "content": system},
                {"role": "user", "content": json.dumps(user, ensure_ascii=False)},
            ],
            temperature=0.7,
        )
        text = response.choices[0].message.content
        if not text:
            raise RuntimeError("DeepSeek returned empty content")
        return json.loads(text)
