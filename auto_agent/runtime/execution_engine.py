"""Execution engine connecting queued tasks to workers."""


class ExecutionEngine:
    def __init__(self, worker, queue):
        self.worker = worker
        self.queue = queue

    def run_once(self):
        task = self.queue.next()
        if task is None:
            return None
        return self.worker.execute(task)
