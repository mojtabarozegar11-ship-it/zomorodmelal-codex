"""Stable contract for autonomous runtime results."""
from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass
class RuntimeResult:
    status: str
    message: str = ""
    executed: List[str] = field(default_factory=list)
    pending_approval: List[str] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)

    @property
    def ok(self):
        return self.status == "ok"
