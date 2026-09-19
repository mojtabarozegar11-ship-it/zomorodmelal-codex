"""Subscription and budget tracking abstraction."""
from dataclasses import dataclass

@dataclass
class Subscription:
    provider: str
    plan: str
    monthly_limit: float | None = None
    enabled: bool = True

class SubscriptionManager:
    def __init__(self) -> None:
        self.items: list[Subscription] = []

    def add(self, provider: str, plan: str, monthly_limit: float | None = None) -> None:
        self.items.append(Subscription(provider, plan, monthly_limit))

    def active(self) -> list[Subscription]:
        return [x for x in self.items if x.enabled]
