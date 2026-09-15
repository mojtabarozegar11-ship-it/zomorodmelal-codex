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
    """Creates an immutable, auditable description of sandbox changes."""

    def __init__(self, root: str | Path = "data/change_packages") -> None:
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def create(
        self,
        files: List[Dict[str, object]],
        reason: str,
        sandbox_rel: str | None = None,
    ) -> Dict[str, object]:
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
            "sandbox_rel": sandbox_rel,
            "files": [asdict(item) for item in items],
        }
        canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
        payload["package_sha256"] = hashlib.sha256(canonical).hexdigest()
        payload["package_id"] = payload["package_sha256"][:16]
        (self.root / f"{payload['package_id']}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return payload

    def get(self, package_id: str) -> Dict[str, object]:
        path = self.root / f"{package_id}.json"
        if not path.exists():
            raise FileNotFoundError(package_id)
        return json.loads(path.read_text(encoding="utf-8"))

    def verify_integrity(self, package: Dict[str, object]) -> bool:
        stored = str(package.get("package_sha256", ""))
        if not stored:
            return False
        canonical_payload = {
            key: package[key]
            for key in (
                "reason",
                "created_at",
                "status",
                "owner_approval_required",
                "real_changes_allowed",
                "sandbox_rel",
                "files",
            )
            if key in package
        }
        digest = hashlib.sha256(
            json.dumps(canonical_payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()
        return digest == stored and str(package.get("package_id", "")) == stored[:16]
