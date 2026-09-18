"""Economic execution and publication policy boundary."""

from django.conf import settings
from django.core.exceptions import PermissionDenied


def guard_real_execution(*, owner_approved: bool) -> None:
    if not owner_approved:
        raise PermissionDenied("OWNER APPROVAL REQUIRED BEFORE REAL EXECUTION")
    if not getattr(settings, "ECONOMIC_REAL_EXECUTION_ENABLED", False):
        raise PermissionDenied("ECONOMIC REAL EXECUTION IS DISABLED")


def guard_publication(*, compliance_checked: bool, owner_approved: bool) -> None:
    if not compliance_checked:
        raise PermissionDenied("COMPLIANCE CHECK REQUIRED BEFORE PUBLICATION")
    if not owner_approved:
        raise PermissionDenied("OWNER APPROVAL REQUIRED BEFORE PUBLICATION")
