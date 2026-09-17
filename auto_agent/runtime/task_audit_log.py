"""Task audit log foundation."""

class TaskAuditLog:
    def __init__(self):
        self.logs = []

    def add(self, event):
        self.logs.append(event)
