"""Personal administration, accounting and automated payments policy.

The worker can plan, record and execute authorized personal administrative tasks.
Financial execution requires a real connected account/provider and explicit
operation-level authorization. No payment credentials or secrets are stored
in source code or ordinary memory.
"""
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any


@dataclass
class AdministrativeTask:
    title: str
    due: str = ""
    recurrence: str = ""
    action: dict[str, Any] = field(default_factory=dict)
    enabled: bool = True


@dataclass
class LedgerEntry:
    description: str
    amount: Decimal
    currency: str
    kind: str  # income | expense | transfer
    category: str = ""


class PersonalAdminManager:
    def __init__(self) -> None:
        self.tasks: list[AdministrativeTask] = []
        self.ledger: list[LedgerEntry] = []

    def plan(self, task: AdministrativeTask) -> AdministrativeTask:
        self.tasks.append(task)
        return task

    def record(self, entry: LedgerEntry) -> LedgerEntry:
        if entry.amount < 0:
            raise ValueError("amount_must_be_non_negative")
        self.ledger.append(entry)
        return entry

    def balance(self, currency: str) -> Decimal:
        total = Decimal("0")
        for entry in self.ledger:
            if entry.currency != currency:
                continue
            if entry.kind == "income":
                total += entry.amount
            elif entry.kind == "expense":
                total -= entry.amount
        return total

    def payment_requires_provider(self, provider: str, operation: str) -> dict[str, str]:
        return {
            "status": "provider_connection_required",
            "provider": provider,
            "operation": operation,
        }
