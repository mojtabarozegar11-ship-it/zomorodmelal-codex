from .openai_provider import OpenAIProvider
from .deepseek_provider import DeepSeekProvider
from .gemini_provider import GeminiProvider
from .claude_provider import ClaudeProvider


def get_providers():
    providers = [
        OpenAIProvider(),
        DeepSeekProvider(),
        GeminiProvider(),
        ClaudeProvider(),
    ]
    return {p.name: p for p in providers}
