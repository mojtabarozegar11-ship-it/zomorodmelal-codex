"""Execution state storage foundation for Master Agent runtime."""

class ExecutionStateStore:
    def __init__(self):
        self.states = {}

    def save(self, task_id, state):
        self.states[task_id] = state

    def get(self, task_id):
        return self.states.get(task_id)
