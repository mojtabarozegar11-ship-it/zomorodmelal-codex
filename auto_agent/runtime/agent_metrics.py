"""Runtime metrics foundation."""

class AgentMetrics:
    def __init__(self):
        self.values = {}

    def set(self, key, value):
        self.values[key] = value
