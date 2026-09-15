from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


@dataclass(frozen=True)
class ChangeItem:
    path: str
    sha256: str
    size: int


class ChangePackage:
    """Creates an auditable, immutable description of a sandbox change set."""

    def __init__(self, root: str | Path = "data/change_packages") -> None:
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def create(self, files: List[Dict[str, object]], reason: str) -> Dict[str, object]:
        items = [
            ChangeItem(
                path=str(item["path"]),
                sha256=str(item["sha256"]),
                size=int(item["size"]),
            )
            for item in files
        ]
        payload = {
            "reason": reason,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "awaiting_owner_approval",
            "owner_approval_required": True,
            "real_changes_allowed": False,
            "files": [asdict(item) for item in items],
        }
        canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
        payload["package_sha256"] = hashlib.sha256(canonical).hexdigest()
        package_id = payload["package_sha256"][:16]
        payload["package_id"] = package_id
        (self.root / f"{package_id}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return payload

    def get(self, package_id: str) -> Dict[str, object]:
        path = self.root / f"{package_id}.json"
        if not path.exists():
            raise FileNotFoundError(package_id)
        return json.loads(path.read_text(encoding="utf-8"))
