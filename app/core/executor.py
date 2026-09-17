class Executor:
    def execute(self, agent, task):
        if agent:
            return agent.run(task)
        return {
            "status": "failed",
            "message": "agent not found"
        }
