class AgentMetrics:
    def __init__(self):
        self.executions = 0
        self.successes = 0

    def record(self, success):
        self.executions += 1
        if success:
            self.successes += 1

    def summary(self):
        return {
            "executions": self.executions,
            "successes": self.successes,
        }
