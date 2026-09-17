class AuditLogger:
    def __init__(self):
        self.events = []

    def log(self, action, result=None):
        self.events.append({
            "action": action,
            "result": result
        })

    def history(self):
        return self.events
