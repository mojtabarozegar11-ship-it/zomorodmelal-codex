"""Append-only audit event abstraction."""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
from pathlib import Path

@dataclass
class AuditEvent:
    action: str
    status: str
    metadata: dict
    timestamp: str

class AuditLog:
    def __init__(self, path: str = "worker_mojtaba/data/audit.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, action: str, status: str, metadata: dict | None = None) -> None:
        event = AuditEvent(action, status, metadata or {}, datetime.now(timezone.utc).isoformat())
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(event), ensure_ascii=False) + "\n")
