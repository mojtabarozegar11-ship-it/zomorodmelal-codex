class RuntimeHealth:
    """Runtime status checker."""

    def __init__(self):
        self.status = "ready"

    def check(self):
        return {
            "runtime": self.status
        }
