from ai_providers.manager import AIProviderManager


class AIBridge:

    def __init__(self):
        self.manager = AIProviderManager()

    def ask(self, prompt):
        return self.manager.generate(prompt)

    def status(self):
        return self.manager.status()
