class AgentRuntimeStatus:
    def __init__(self):
        self.status = 'idle'

    def set_status(self, value):
        self.status = value

    def get_status(self):
        return self.status
