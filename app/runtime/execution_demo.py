class ExecutionDemo:
    def run(self, goal):
        return {
            "goal": goal,
            "flow": ["plan", "task", "agent", "result", "report"],
            "status": "completed"
        }
