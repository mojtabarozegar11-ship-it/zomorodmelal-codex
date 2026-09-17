import time

class RuntimeEventLogger:
    def __init__(self):
        self.events = []

    def record(self, event, data=None):
        self.events.append({"time": time.time(), "event": event, "data": data})

    def all(self):
        return self.events
