from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

from approval.approval_gateway import ApprovalGateway
from approval.telegram_approval import TelegramApproval
from autonomous_core.change_package import ChangePackage
from controller.change_package_executor import ChangePackageExecutor
from deployment.host_adapter import HostDeploymentAdapter


class DeploymentGate:
    """Final boundary between verified promotion and optional real host deployment."""

    def __init__(self, root: Optional[Union[str, Path]] = None) -> None:
        self.root = Path(root or Path(__file__).resolve().parents[1]).resolve()
        self.approval = ApprovalGateway(self.root)
        self.telegram = TelegramApproval(self.root)
        self.packages = ChangePackage(self.root / "data" / "change_packages")
        self.executor = ChangePackageExecutor(self.root)
        self.adapter = HostDeploymentAdapter()

    def prepare(self, package_id: str, reason: str) -> Dict[str, Any]:
        package = self.packages.get(package_id)
        if not self.packages.verify_integrity(package):
            raise ValueError("change package integrity check failed")
        request = self.approval.request(
            "production_deployment", reason,
            {"package_id": package_id, "package_sha256": package.get("package_sha256"),
             "target": os.environ.get("MASTER_AGENT_DEPLOY_TARGET", "production")},
        )
        notification = self.telegram.notify(request)
        return {"status": request.get("status"), "request_id": request.get("id"),
                "package_id": package_id, "package_sha256": package.get("package_sha256"),
                "owner_approval_required": True, "telegram": notification,
                "external_deployment": self.adapter.enabled}

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

        promotion = self.executor.execute(package_id, request_id)
        if not promotion.get("success"):
            return promotion
        if not self.adapter.enabled:
            return dict(promotion, external_deployment=False, status="promoted_host_adapter_disabled")
        remote = self.adapter.deploy()
        return dict(promotion, external_deployment=True, external_result=remote.__dict__,
                    status="deployed" if remote.success else "external_deployment_failed")

    def status(self) -> Dict[str, Any]:
        return {"enabled": True, "owner_approval_required": True, "package_hash_binding": True,
                "telegram_enabled": self.telegram.enabled,
                "external_deployment": self.adapter.enabled,
                "external_target_configured": bool(os.environ.get("MASTER_AGENT_DEPLOY_TARGET")),
                "adapter_configured": bool(self.adapter.command),
                "message": "External deployment requires explicit host configuration and owner approval."}
