from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class MissionQueue:
    """Persistent, bounded queue for safe autonomous follow-up missions."""

    MAX_ITEMS = 50

    def __init__(self, root: Union[str, Path]) -> None:
        self.root = Path(root).resolve()
        self.path = self.root / "data" / "mission_queue.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> List[Dict[str, Any]]:
        try:
            value = json.loads(self.path.read_text(encoding="utf-8"))
            return value if isinstance(value, list) else []
        except (OSError, ValueError, TypeError):
            return []

    def _save(self, items: List[Dict[str, Any]]) -> None:
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(items[-self.MAX_ITEMS:], ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.path)

    def enqueue(self, mission: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not isinstance(mission, dict):
            return None
        item = dict(mission)
        item.setdefault("id", "continuous.improvement")
        item.setdefault("status", "ready")
        item["queued_at"] = datetime.now(timezone.utc).isoformat()
        items = self._load()
        mission_id = str(item.get("id"))
        items = [x for x in items if str(x.get("id")) != mission_id]
        items.append(item)
        self._save(items)
        return item

    def pending(self) -> List[Dict[str, Any]]:
        return [x for x in self._load() if x.get("status") not in {"completed", "cancelled"}]

    def peek(self) -> Optional[Dict[str, Any]]:
        items = self.pending()
        if not items:
            return None
        items.sort(key=lambda x: (-int(x.get("priority", 0) or 0), str(x.get("queued_at", ""))))
        return dict(items[0])

    def complete(self, mission_id: str) -> bool:
        items = self._load()
        changed = False
        for item in items:
            if str(item.get("id")) == str(mission_id):
                item["status"] = "completed"
                item["completed_at"] = datetime.now(timezone.utc).isoformat()
                changed = True
        if changed:
            self._save(items)
        return changed
