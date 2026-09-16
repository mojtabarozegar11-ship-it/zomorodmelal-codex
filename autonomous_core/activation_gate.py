from __future__ import annotations

from typing import Any, Dict

from .access_manager import AccessManager


class ActivationGate:
    """Final authorization boundary before any external capability activation.

    This class never acquires credentials and never activates an external resource.
    It only issues a short-lived, in-memory authorization decision after re-checking
    the AccessManager state and requested scope.
    """

    def __init__(self, root=None, access_manager: AccessManager | None = None) -> None:
        self.access_manager = access_manager or AccessManager(root)

    def authorize(self, request_id: str, capability: str, scope: str = "minimum_required") -> Dict[str, Any]:
        request = next(
            (item for item in self.access_manager.status()["requests"] if item.get("request_id") == request_id),
            None,
        )
        if not request:
            raise PermissionError("access request not found")
        if request.get("status") != "approved_pending_activation":
            raise PermissionError("access request is not approved for activation")
        if request.get("capability") != capability:
            raise PermissionError("capability does not match approved request")
        if request.get("scope") != scope:
            raise PermissionError("scope does not match approved request")
        if request.get("credentials_acquired") or request.get("activated"):
            raise PermissionError("activation state is invalid")

        return {
            "authorized": True,
            "request_id": request_id,
            "capability": capability,
            "scope": scope,
            "credentials_acquired": False,
            "activated": False,
            "owner_approval_required": True,
            "external_action_allowed": False,
        }
