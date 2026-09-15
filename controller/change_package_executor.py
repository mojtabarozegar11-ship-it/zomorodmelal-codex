from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path
from typing import Dict, Any

from approval.approval_gateway import ApprovalGateway
from execution.execution_controller import ExecutionController
from autonomous_core.change_package import ChangePackage


class ChangePackageExecutor:
    """Promotes only an approved, hash-verified package into the project.

    Real deployment remains opt-in through ``execute``; credentials and
    external services are deliberately outside this component.
    """

    def __init__(self) -> None:
        self.root = Path(__file__).resolve().parents[1]
        self.approval = ApprovalGateway()
        self.execution = ExecutionController()
        self.packages = ChangePackage(self.root / "data" / "change_packages")

    def _verify_package(self, package_id: str) -> Dict[str, Any]:
        package = self.packages.get(package_id)
        if package.get("status") != "approved":
            raise PermissionError("change package is not approved")
        return package

    def execute(self, package_id: str, request_id: int) -> Dict[str, Any]:
        request = self.approval.get(request_id)
        if not request or not self.approval.is_approved(request_id):
            return {"success": False, "status": "approval_required", "request_id": request_id}

        package = self._verify_package(package_id)
        backup = self.execution.backup()
        staged = []

        for item in package.get("files", []):
            relative = str(item["path"])
            source = (self.root / "sandbox" / relative).resolve()
            target = (self.root / relative).resolve()
            if self.root not in source.parents or self.root not in target.parents:
                raise ValueError("package path escapes project")
            if not source.is_file():
                raise FileNotFoundError(relative)
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            if digest != item["sha256"]:
                raise ValueError(f"hash mismatch: {relative}")
            staged.append(relative)

        return {
            "success": True,
            "status": "verified_ready_for_promotion",
            "request_id": request_id,
            "package_id": package_id,
            "backup_path": backup,
            "verified_files": staged,
            "real_deployment": False,
            "message": "بسته تأییدشده اعتبارسنجی شد؛ انتقال به محیط اصلی همچنان مرحله‌ای جداگانه است."
        }
