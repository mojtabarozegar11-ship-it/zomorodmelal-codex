from ai_engine.router import AIRouter
from ai_engine.provider_registry import ProviderRegistry


class MasterCore:
    def __init__(self):
        self.name = "Master Agent Core"
        self.version = "0.3.0"
        self.owner_approval_required = True
        self.auto_execution = False
        self.self_evolution = False

        self.ai_registry = ProviderRegistry()
        self.ai_router = AIRouter(self.ai_registry.providers)

    def status(self):
        return {
            "name": self.name,
            "version": self.version,
            "owner_approval_required": self.owner_approval_required,
            "auto_execution": self.auto_execution,
            "self_evolution": self.self_evolution,
            "ai_providers": list(self.ai_registry.providers.keys()),
        }

    def think(self, task, task_type="general"):
        provider = self.ai_router.choose(task_type)

        if not provider:
            return {
                "status": "no_provider",
                "task": task
            }

        return provider.chat(task)

    def plan(self, goal):
        return {
            "goal": goal,
            "status": "planned",
            "approval_required": True,
            "actions": [
                "analyze_goal",
                "select_ai_provider",
                "create_plan",
                "request_owner_approval",
                "execute_only_after_approval"
            ]
        }


if __name__ == "__main__":
    core = MasterCore()

    print("🧠 Master Agent Core")
    print("Version:", core.version)
    print("🔐 Owner approval:", core.owner_approval_required)
    print("🤖 AI Providers:", core.status()["ai_providers"])
