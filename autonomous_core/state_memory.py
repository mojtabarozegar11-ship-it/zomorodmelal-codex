class StateMemory:
    """Simple runtime state storage for agent execution."""

    def __init__(self):
        self.state = {}

    def set(self, key, value):
        self.state[key] = value

    def get(self, key, default=None):
        return self.state.get(key, default)
