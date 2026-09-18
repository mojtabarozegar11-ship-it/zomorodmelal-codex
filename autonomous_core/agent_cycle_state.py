class AgentCycleState:
    def __init__(self):
        self.status = "initialized"

    def set_status(self, status):
        self.status = status
        return self.status
