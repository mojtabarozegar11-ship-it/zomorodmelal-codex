"""Append-only audit event abstraction with deterministic JSON serialization."""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


@dataclass
class AuditEvent:
    action: str
    status: str
    metadata: dict[str, Any]
    timestamp: str


class AuditLog:
    def __init__(self, path: str = "worker_mojtaba/data/audit.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(
        self,
        action: str,
        status: str,
        metadata: dict[str, Any] | None = None,
    ) -> AuditEvent:
        event = AuditEvent(
            action=action,
            status=status,
            metadata=metadata or {},
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    asdict(event),
                    ensure_ascii=False,
                    sort_keys=True,
                )
                + "\n"
            )
        return event

    def tail(self, limit: int = 20) -> list[dict[str, Any]]:
        if limit < 1:
            raise ValueError("limit must be positive")
        if not self.path.exists():
            return []
        lines = self.path.read_text(encoding="utf-8").splitlines()
        return [json.loads(line) for line in lines[-limit:] if line.strip()]
