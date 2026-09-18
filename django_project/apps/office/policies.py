"""Central policy guards for sensitive office/economic actions."""

from django.core.exceptions import PermissionDenied


def require_owner_approval(*, approved: bool) -> None:
    if not approved:
        raise PermissionDenied("OWNER APPROVAL REQUIRED BEFORE ANY SENSITIVE ACTION")


def real_execution_allowed(*, requested: bool, owner_approved: bool, system_enabled: bool) -> None:
    if not requested:
        return
    if not owner_approved:
        raise PermissionDenied("OWNER APPROVAL REQUIRED BEFORE REAL EXECUTION")
    if not system_enabled:
        raise PermissionDenied("REAL EXECUTION IS DISABLED")
