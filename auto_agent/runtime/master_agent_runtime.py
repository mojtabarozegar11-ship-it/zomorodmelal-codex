"""
Master Agent Runtime Bridge
Connects task queue, worker and execution flow.
Security rule: owner approval is required before execution.
"""

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class TaskResult:
    status: str
    data: Dict[str, Any]


class MasterAgentRuntime:
    def __init__(self, queue, worker):
        self.queue = queue
        self.worker = worker

    def submit_task(self, task: Dict[str, Any]):
        if not task.get("owner_approved", False):
            return TaskResult("blocked", {"reason": "OWNER_APPROVAL_REQUIRED"})
        self.queue.push(task)
        return TaskResult("queued", task)

    def run_once(self):
        task = self.queue.pop()
        if task is None:
            return TaskResult("idle", {})
        result = self.worker.execute(task)
        return TaskResult("completed", {"result": result})
