"""Retry policy foundation."""

class RetryPolicy:
    def __init__(self, max_retry=3):
        self.max_retry = max_retry

    def allowed(self, count):
        return count < self.max_retry
