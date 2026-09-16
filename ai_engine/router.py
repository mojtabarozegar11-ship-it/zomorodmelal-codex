class AIRouter:
    def __init__(self, providers):
        self.providers = providers

    def choose(self, task_type="general"):
        priority = {
            "coding": ["deepseek", "openai"],
            "research": ["gemini", "deepseek", "openai"],
            "reasoning": ["openai", "claude", "deepseek"],
            "documents": ["claude", "gemini", "openai"],
            "content": ["openai", "claude", "deepseek"],
            "general": ["openai", "deepseek", "gemini", "claude"],
        }

        for name in priority.get(task_type, priority["general"]):
            provider = self.providers.get(name)
            if provider and provider.available():
                return provider

        return None
