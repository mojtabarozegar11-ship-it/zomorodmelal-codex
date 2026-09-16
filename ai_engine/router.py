class AIRouter:
    def __init__(self, providers):
        self.providers = providers

    def choose(self, task_type="general"):
        priority = {
            "coding": ["deepseek", "openai"],
            "research": ["deepseek", "openai"],
            "reasoning": ["openai", "deepseek"],
            "general": ["openai", "deepseek"],
        }

        for name in priority.get(task_type, priority["general"]):
            provider = self.providers.get(name)
            if provider and provider.available():
                return provider

        return None
