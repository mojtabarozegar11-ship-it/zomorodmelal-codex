from .agent_bridge import AgentBridge


class AgentService:
    """Application service for Django to communicate with Master Agent."""

    def __init__(self, runner=None):
        self.bridge = AgentBridge(runner)

    def run(self, goal):
        return self.bridge.execute_goal(goal)
