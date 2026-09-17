"""
Recovery Manager for Auto Agent Runtime.

Responsible for runtime error handling, retry policy,
and recovery state management.
"""

class RecoveryManager:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries

    def should_retry(self, attempts):
        return attempts < self.max_retries

    def record_failure(self, task_id, error):
        return {
            "task_id": task_id,
            "status": "failed",
            "error": str(error),
        }
