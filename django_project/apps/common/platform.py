from django.core.exceptions import PermissionDenied
from django.db import IntegrityError, transaction

from .models import IdempotencyRecord, PlatformAuditEvent

OWNER_APPROVAL_MESSAGE = "OWNER APPROVAL REQUIRED BEFORE ANY SENSITIVE ACTION"


def require_owner_approval(approved):
    if not approved:
        raise PermissionDenied(OWNER_APPROVAL_MESSAGE)


@transaction.atomic
def record_audit(*, actor=None, action, scope, obj=None, request_id="", metadata=None):
    return PlatformAuditEvent.objects.create(
        actor=actor,
        action=action,
        scope=scope,
        object_type=obj.__class__.__name__ if obj is not None else "",
        object_id=str(obj.pk) if obj is not None and getattr(obj, "pk", None) else "",
        request_id=request_id,
        metadata=metadata or {},
    )


def get_idempotent_response(*, key, scope, actor):
    return IdempotencyRecord.objects.filter(
        key=key, scope=scope, actor=actor
    ).first()


@transaction.atomic
def save_idempotent_response(
    *, key, scope, actor, response_code, response_payload
):
    try:
        return IdempotencyRecord.objects.create(
            key=key,
            scope=scope,
            actor=actor,
            response_code=response_code,
            response_payload=response_payload,
        )
    except IntegrityError:
        return IdempotencyRecord.objects.get(
            key=key, scope=scope, actor=actor
        )


def require_owner_actor(actor):
    """Require an authenticated Django superuser for owner-level approval."""
    if not getattr(actor, "is_authenticated", False) or not getattr(
        actor, "is_superuser", False
    ):
        raise PermissionDenied("OWNER APPROVAL REQUIRED")
    return actor


def approve_owner_action(*, actor, action, scope, obj=None, request_id="", metadata=None):
    """Record explicit owner approval and return the audit event."""
    require_owner_actor(actor)
    return record_audit(
        actor=actor,
        action=action,
        scope=scope,
        obj=obj,
        request_id=request_id,
        metadata={**(metadata or {}), "owner_approved": True},
    )
