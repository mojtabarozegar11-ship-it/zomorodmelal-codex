"""
Persistence layer for Auto Agent Runtime.
Stores task states and execution history.
"""

from datetime import datetime


class TaskStore:
    def __init__(self):
        self.tasks = {}

    def create(self, task_id, payload):
        self.tasks[task_id] = {
            "id": task_id,
            "payload": payload,
            "status": "queued",
            "created_at": datetime.utcnow().isoformat(),
        }
        return self.tasks[task_id]

    def update_status(self, task_id, status):
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = status
        return self.tasks.get(task_id)

    def get(self, task_id):
        return self.tasks.get(task_id)

    def all(self):
        return list(self.tasks.values())
