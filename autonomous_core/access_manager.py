from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


class AccessManager:
    """Track capability access requests without acquiring or using credentials."""

    CATALOG = {
        "web_research": {"level": "read", "risk": "low", "resource": "internet_research"},
        "github_repo": {"level": "read_write", "risk": "high", "resource": "github_repository"},
        "telegram_bot": {"level": "send", "risk": "high", "resource": "telegram_bot"},
        "hosting": {"level": "deploy", "risk": "critical", "resource": "hosting_environment"},
        "payments": {"level": "transact", "risk": "critical", "resource": "payment_account"},
        "email": {"level": "send", "risk": "high", "resource": "email_account"},
        "calendar": {"level": "write", "risk": "high", "resource": "calendar"},
        "secrets": {"level": "read", "risk": "critical", "resource": "secret_store"},
        "browser_automation": {"level": "restricted", "risk": "high", "resource": "browser_runtime"},
    }

    def __init__(self, root: str | Path | None = None) -> None:
        self.root = Path(root or Path(__file__).resolve().parents[1]).resolve()
        self.data_dir = self.root / "data"
        self.file = self.data_dir / "access_requests.json"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.file.exists():
            self._save([])

    def _load(self) -> List[Dict[str, Any]]:
        try:
            data = json.loads(self.file.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def _save(self, items: List[Dict[str, Any]]) -> None:
        tmp = self.file.with_name(self.file.name + ".tmp")
        tmp.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, self.file)

    def discover(self, capabilities: List[str]) -> List[Dict[str, Any]]:
        result = []
        for capability in sorted(set(capabilities)):
            spec = self.CATALOG.get(capability)
            if not spec:
                continue
            result.append({
                "capability": capability,
                **spec,
                "status": "identified",
                "owner_approval_required": True,
                "credentials_acquired": False,
                "activated": False,
            })
        return result

    def request(self, capability: str, goal: str, scope: str = "minimum_required") -> Dict[str, Any]:
        if capability not in self.CATALOG:
            raise ValueError(f"unknown capability: {capability}")
        spec = self.CATALOG[capability]
        items = self._load()
        for item in items:
            if item.get("capability") == capability and item.get("goal") == goal and item.get("scope") == scope and item.get("status") in {"waiting_owner_approval", "approved_pending_activation"}:
                return item
        material = f"{capability}|{goal}|{scope}|{datetime.now(timezone.utc).isoformat()}"
        request_id = hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]
        item = {
            "request_id": request_id,
            "capability": capability,
            "resource": spec["resource"],
            "level": spec["level"],
            "access_level": spec["level"],
            "risk": spec["risk"],
            "risk_level": spec["risk"],
            "goal": goal,
            "scope": scope,
            "status": "waiting_owner_approval",
            "owner_approval_required": True,
            "credentials_acquired": False,
            "activated": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        items.append(item)
        self._save(items)
        return item

    def approve(self, request_id: str) -> Dict[str, Any] | None:
        items = self._load()
        for item in items:
            if item.get("request_id") == request_id:
                if item.get("status") == "waiting_owner_approval":
                    item["status"] = "approved_pending_activation"
                    item["approved_at"] = datetime.now(timezone.utc).isoformat()
                self._save(items)
                return item
        return None

    def revoke(self, request_id: str) -> Dict[str, Any] | None:
        items = self._load()
        for item in items:
            if item.get("request_id") == request_id:
                item["status"] = "revoked"
                item["activated"] = False
                item["revoked_at"] = datetime.now(timezone.utc).isoformat()
                self._save(items)
                return item
        return None

    def status(self) -> Dict[str, Any]:
        items = self._load()
        return {
            "access_manager": True,
            "total": len(items),
            "requests": items,
            "waiting_owner_approval": sum(x.get("status") == "waiting_owner_approval" for x in items),
            "approved_pending_activation": sum(x.get("status") == "approved_pending_activation" for x in items),
            "revoked": sum(x.get("status") == "revoked" for x in items),
            "credentials_acquired": sum(bool(x.get("credentials_acquired")) for x in items),
            "activated": sum(bool(x.get("activated")) for x in items),
            "owner_approval_required": True,
        }
