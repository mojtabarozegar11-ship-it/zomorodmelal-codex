class AgentBridge:
    """Bridge between Django services and Master Agent Core."""

    def __init__(self, agent_runner=None):
        self.agent_runner = agent_runner

    def execute_goal(self, goal):
        if not self.agent_runner:
            return {"status": "pending", "message": "Runner not connected"}

        return self.agent_runner.start(goal)
