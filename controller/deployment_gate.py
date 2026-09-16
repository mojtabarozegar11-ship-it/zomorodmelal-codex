from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

from approval.approval_gateway import ApprovalGateway
from autonomous_core.change_package import ChangePackage
from controller.change_package_executor import ChangePackageExecutor


class DeploymentGate:
    """Final boundary between verified project promotion and real deployment."""

    def __init__(self, root: Optional[Union[str, Path]] = None) -> None:
        self.root = Path(root or Path(__file__).resolve().parents[1]).resolve()
        self.approval = ApprovalGateway(self.root)
        self.packages = ChangePackage(self.root / "data" / "change_packages")
        self.executor = ChangePackageExecutor(self.root)

    def prepare(self, package_id: str, reason: str) -> Dict[str, Any]:
        package = self.packages.get(package_id)
        if not self.packages.verify_integrity(package):
            raise ValueError("change package integrity check failed")
        request = self.approval.request(
            "production_deployment",
            reason,
            {
                "package_id": package_id,
                "package_sha256": package.get("package_sha256"),
                "target": os.environ.get("MASTER_AGENT_DEPLOY_TARGET", "production"),
            },
        )
        return {
            "status": request.get("status"),
            "request_id": request.get("id"),
            "package_id": package_id,
            "package_sha256": package.get("package_sha256"),
            "owner_approval_required": True,
            "external_deployment": False,
        }

    def deploy(self, package_id: str, request_id: int) -> Dict[str, Any]:
        request = self.approval.get(request_id)
        if not request or not self.approval.is_approved(request_id):
            return {"success": False, "status": "approval_required", "request_id": request_id}
        package = self.packages.get(package_id)
        if not self.packages.verify_integrity(package):
            return {"success": False, "status": "package_integrity_failed", "request_id": request_id}
        metadata = request.get("metadata") or {}
        if metadata.get("package_id") != package_id or metadata.get("package_sha256") != package.get("package_sha256"):
            return {"success": False, "status": "approval_binding_mismatch", "request_id": request_id}

        # Project promotion is deliberately the only action this component can perform.
        # External hosting deployment requires a separately configured adapter/secret.
        return self.executor.execute(package_id, request_id)

    def status(self) -> Dict[str, Any]:
        return {
            "enabled": True,
            "owner_approval_required": True,
            "package_hash_binding": True,
            "external_deployment": False,
            "external_target_configured": bool(os.environ.get("MASTER_AGENT_DEPLOY_TARGET")),
            "message": "Production deployment remains disabled until an explicit host adapter is configured.",
        }
