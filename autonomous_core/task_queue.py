from collections import deque


class TaskQueue:
    """Minimal internal queue for Master Agent tasks."""

    def __init__(self):
        self._queue = deque()

    def add(self, task):
        self._queue.append(task)

    def next(self):
        return self._queue.popleft() if self._queue else None

    def size(self):
        return len(self._queue)
