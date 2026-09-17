"""Master Agent runtime runner.
Connects scheduler, queue, worker and execution engine.
"""

from .scheduler import Scheduler
from .worker import Worker
from .task_queue import TaskQueue
from .execution_engine import ExecutionEngine
from .master_agent_runtime import MasterAgentRuntime


class RuntimeRunner:
    def __init__(self):
        self.queue = TaskQueue()
        self.engine = ExecutionEngine()
        self.worker = Worker(self.queue, self.engine)
        self.scheduler = Scheduler(self.queue)
        self.agent = MasterAgentRuntime()

    def run_once(self):
        task = self.scheduler.next_task()
        if task:
            self.worker.execute(task)
            return True
        return False

    def start(self):
        while True:
            self.run_once()


if __name__ == "__main__":
    RuntimeRunner().start()
