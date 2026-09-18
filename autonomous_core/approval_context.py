"""Minimal approval context shared by execution paths."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ApprovalContext:
    approved: bool = False
    request_id: int = 0

    def allows(self):
        return self.approved
