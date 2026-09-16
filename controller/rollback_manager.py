from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class RollbackManager:
    """Creates and restores controlled backups with an auditable trail."""

    def __init__(self, root: Optional[Union[str, Path]] = None) -> None:
        self.root = Path(root or Path(__file__).resolve().parents[1]).resolve()
        self.backup_root = self.root / "data" / "execution_backups"
        self.audit_file = self.root / "data" / "rollback_audit.json"
        self.backup_root.mkdir(parents=True, exist_ok=True)
        self.audit_file.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> List[Dict[str, Any]]:
        if not self.audit_file.exists():
            return []
        try:
            value = json.loads(self.audit_file.read_text(encoding="utf-8"))
            return value if isinstance(value, list) else []
        except (OSError, ValueError, TypeError):
            return []

    def _audit(self, event: str, details: Dict[str, Any]) -> None:
        rows = self._load()
        rows.append({
            "event": event,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "details": details,
        })
        self.audit_file.write_text(
            json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def create_backup(self, paths: List[str]) -> str:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        destination = self.backup_root / "rollback_{}".format(stamp)
        destination.mkdir(parents=True, exist_ok=False)
        copied = []
        for relative in paths:
            source = (self.root / str(relative)).resolve()
            if self.root not in source.parents or not source.is_file():
                continue
            target = destination / str(relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            copied.append(str(relative))
        self._audit("backup_created", {"backup": str(destination), "files": copied})
        return str(destination)

    def rollback(self, backup_path: str, paths: List[str]) -> Dict[str, Any]:
        backup = Path(backup_path).resolve()
        if self.backup_root not in backup.parents or not backup.is_dir():
            raise ValueError("backup path is not an approved rollback location")

        restored = []
        for relative in paths:
            source = (backup / str(relative)).resolve()
            target = (self.root / str(relative)).resolve()
            if backup not in source.parents or self.root not in target.parents:
                raise ValueError("rollback path escapes its controlled root")
            if not source.is_file():
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            restored.append(str(relative))

        self._audit("rollback_completed", {"backup": str(backup), "files": restored})
        return {
            "success": True,
            "status": "rollback_completed",
            "backup": str(backup),
            "restored_files": restored,
        }

    def audit(self) -> List[Dict[str, Any]]:
        return self._load()
