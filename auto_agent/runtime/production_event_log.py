"""Production event logging layer."""

class ProductionEventLog:
    def __init__(self):
        self.events = []

    def add(self, event):
        self.events.append(event)
        return event
