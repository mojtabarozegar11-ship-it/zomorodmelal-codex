from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ExecutionResult:
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
