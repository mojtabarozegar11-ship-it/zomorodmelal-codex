class ApprovalFlow:
    def __init__(self, gateway):
        self.gateway = gateway

    def check(self, action):
        return self.gateway.request(action)
