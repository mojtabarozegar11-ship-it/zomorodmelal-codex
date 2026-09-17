from datetime import datetime


class ExecutionLogger:
    def __init__(self):
        self.events = []

    def log(self, stage, message):
        self.events.append({
            "time": datetime.utcnow().isoformat(),
            "stage": stage,
            "message": message
        })

    def report(self):
        return self.events
