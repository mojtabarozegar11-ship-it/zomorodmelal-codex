"""Track task execution states."""

class TaskExecutionTracker:
    def __init__(self):
        self.tasks = {}

    def update(self, task_id, state):
        self.tasks[task_id] = state
        return self.tasks[task_id]
