from dataclasses import dataclass

@dataclass
class ExecutionResult:
    success: bool
    message: str
    data: dict | None = None
