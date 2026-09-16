from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path
from typing import Any, Dict, Optional, Union

from approval.approval_gateway import ApprovalGateway
from autonomous_core.change_package import ChangePackage
from execution.execution_controller import ExecutionController


class ChangePackageExecutor:
    """Promote only an owner-approved, hash-verified sandbox package once."""
    PROTECTED = {".git", "data", "sandbox", ".venv", "venv"}

    def __init__(self, root: Optional[Union[str, Path]] = None) -> None:
        self.root = Path(root or Path(__file__).resolve().parents[1]).resolve()
        self.approval = ApprovalGateway(self.root)
        self.execution = ExecutionController() if root is None else ExecutionControllerForRoot(self.root)
        self.packages = ChangePackage(self.root / "data" / "change_packages")
        self.execution_records = self.root / "data" / "execution_records.json"
        self._ensure_execution_records()

    def _ensure_execution_records(self) -> None:
        self.execution_records.parent.mkdir(parents=True, exist_ok=True)
        if not self.execution_records.exists():
            self._save_execution_records({})

    def _load_execution_records(self) -> Dict[str, Any]:
        try:
            with self.execution_records.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    def _save_execution_records(self, records: Dict[str, Any]) -> None:
        tmp = self.execution_records.with_name(self.execution_records.name + ".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        os.replace(tmp, self.execution_records)

    def _execution_key(self, request_id: int, package_id: str, package_sha256: str) -> str:
        return f"{request_id}:{package_id}:{package_sha256}"

    def _safe_relative(self, relative: str) -> Path:
        raw = Path(relative)
        if raw.is_absolute() or ".." in raw.parts or not raw.name:
            raise ValueError("package path must be relative and contained")
        if raw.parts[0] in self.PROTECTED:
            raise ValueError("protected project path cannot be promoted")
        target = (self.root / raw).resolve()
        if self.root not in target.parents:
            raise ValueError("package path escapes project")
        return target

    def _verify_package(self, package_id: str) -> Dict[str, Any]:
        package = self.packages.get(package_id)
        if not self.packages.verify_integrity(package):
            raise ValueError("change package integrity check failed")
        if package.get("status") != "awaiting_owner_approval":
            raise PermissionError("change package is not awaiting owner approval")
        if not package.get("owner_approval_required", True):
            raise PermissionError("owner approval boundary is missing")
        return package

    def execute(self, package_id: str, request_id: int) -> Dict[str, Any]:
        request = self.approval.get(request_id)
        if not request or not self.approval.is_approved(request_id):
            return {"success": False, "status": "approval_required", "request_id": request_id}
        package = self._verify_package(package_id)
        metadata = request.get("metadata") or {}
        if metadata.get("package_id") != package_id:
            return {"success": False, "status": "package_binding_mismatch", "request_id": request_id}
        if metadata.get("package_sha256") != package.get("package_sha256"):
            return {"success": False, "status": "package_hash_binding_mismatch", "request_id": request_id}
        execution_key = self._execution_key(request_id, package_id, str(package.get("package_sha256")))
        if execution_key in self._load_execution_records():
            return {"success": False, "status": "already_executed", "request_id": request_id, "package_id": package_id}

        sandbox_rel = str(package.get("sandbox_rel") or "")
        if not sandbox_rel:
            return {"success": False, "status": "sandbox_source_missing", "request_id": request_id}
        sandbox = (self.root / sandbox_rel).resolve()
        if self.root not in sandbox.parents or not sandbox.is_dir():
            return {"success": False, "status": "sandbox_source_invalid", "request_id": request_id}
        verified = []
        for item in package.get("files", []):
            relative = str(item["path"])
            self._safe_relative(relative)
            source = (sandbox / relative).resolve()
            if sandbox not in source.parents or not source.is_file():
                raise FileNotFoundError(relative)
            content = source.read_bytes()
            if len(content) != int(item["size"]):
                raise ValueError(f"size mismatch: {relative}")
            if hashlib.sha256(content).hexdigest() != str(item["sha256"]):
                raise ValueError(f"hash mismatch: {relative}")
            verified.append(relative)
        existed_before = {relative: self._safe_relative(relative).is_file() for relative in verified}
        backup = self.execution.backup(verified)
        promoted = []
        try:
            for relative in verified:
                source = (sandbox / relative).resolve()
                target = self._safe_relative(relative)
                target.parent.mkdir(parents=True, exist_ok=True)
                temp = target.with_name(target.name + ".master-agent.tmp")
                try:
                    shutil.copy2(source, temp)
                    os.replace(temp, target)
                finally:
                    if temp.exists():
                        temp.unlink()
                promoted.append(relative)
            records = self._load_execution_records()
            records[execution_key] = {"request_id": request_id, "package_id": package_id, "package_sha256": package.get("package_sha256"), "files": promoted}
            self._save_execution_records(records)
            self.execution._log("package_promote", "completed", {"request_id": request_id, "package_id": package_id, "package_sha256": package.get("package_sha256"), "files": promoted, "backup": backup})
        except Exception:
            for relative in reversed(promoted):
                target = self._safe_relative(relative)
                backup_file = Path(backup) / relative
                if existed_before.get(relative) and backup_file.is_file():
                    shutil.copy2(backup_file, target)
                elif target.exists():
                    target.unlink()
            self.execution._log("package_promote", "rolled_back_after_failure", {"request_id": request_id, "package_id": package_id, "backup": backup})
            raise
        return {"success": True, "status": "promoted", "request_id": request_id, "package_id": package_id, "backup_path": backup, "promoted_files": promoted, "project_promotion": True, "external_deployment": False, "generated_code_executed": False}


class ExecutionControllerForRoot(ExecutionController):
    def __init__(self, root: Path) -> None:
        self.root = str(root)
        self.data_dir = str(root / "data")
        self.sandbox_dir = str(root / "sandbox" / "execution_workspace")
        self.log_file = str(root / "data" / "execution_log.json")
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.sandbox_dir, exist_ok=True)
        if not os.path.exists(self.log_file):
            self._save_logs([])
