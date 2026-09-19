"""Persistent-memory interface for Worker Mojtaba."""
from dataclasses import dataclass, asdict
import json
from pathlib import Path

@dataclass
class MemoryItem:
    key: str
    value: str
    category: str = "general"

class PersistentMemory:
    def __init__(self, path: str = "worker_mojtaba/data/memory.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def save(self, item: MemoryItem) -> None:
        items = json.loads(self.path.read_text(encoding="utf-8"))
        items.append(asdict(item))
        self.path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    def search(self, term: str) -> list[dict]:
        items = json.loads(self.path.read_text(encoding="utf-8"))
        return [x for x in items if term.lower() in str(x).lower()]
