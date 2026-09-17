class TaskManager:
    def __init__(self):
        self.tasks = []

    def create(self, title, payload=None):
        task = {
            "title": title,
            "payload": payload,
            "status": "PENDING"
        }
        self.tasks.append(task)
        return task

    def update_status(self, task, status):
        task["status"] = status
        return task

    def all(self):
        return self.tasks
