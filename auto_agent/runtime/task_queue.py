"""Basic task queue layer for Master Agent runtime."""

from collections import deque


class TaskQueue:
    def __init__(self):
        self._queue = deque()

    def add(self, task):
        self._queue.append(task)

    def next(self):
        if self._queue:
            return self._queue.popleft()
        return None

    def size(self):
        return len(self._queue)
