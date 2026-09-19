"""Security policy primitives."""

class Policy:
    def __init__(self) -> None:
        self.enabled = True

    def check_capability(self, capability: str) -> bool:
        return bool(self.enabled and capability.strip())

    def disable(self) -> None:
        self.enabled = False
