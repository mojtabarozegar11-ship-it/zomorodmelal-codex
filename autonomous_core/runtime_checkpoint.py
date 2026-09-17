class RuntimeCheckpoint:
    def __init__(self):
        self.state = {}

    def save(self, key, value):
        self.state[key] = value

    def load(self, key, default=None):
        return self.state.get(key, default)
