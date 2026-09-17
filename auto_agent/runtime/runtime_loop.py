"""
Runtime Loop
Connects Scheduler, Queue, Worker and Persistence layers.
"""

import time


class RuntimeLoop:
    def __init__(self, scheduler, queue, worker, persistence):
        self.scheduler = scheduler
        self.queue = queue
        self.worker = worker
        self.persistence = persistence
        self.running = False

    def start(self):
        self.running = True
        while self.running:
            task = self.scheduler.next_task()
            if task:
                self.persistence.save(task, "queued")
                result = self.worker.execute(task)
                self.persistence.save(task, "completed", result)
            time.sleep(1)

    def stop(self):
        self.running = False
