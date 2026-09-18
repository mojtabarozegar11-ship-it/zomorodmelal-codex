from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone

from apps.common.platform import record_audit, require_owner_approval
from .models import AuditLog, CompanyDelegation, Journal, JournalLine


def user_has_company_role(user, company, roles=()):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    qs = CompanyDelegation.objects.filter(
        user=user, company=company, active=True, owner_approved=True
    )
    return not roles or qs.filter(role__in=roles).exists()


def audit(actor, action, obj, company=None, metadata=None):
    return AuditLog.objects.create(
        actor=actor,
        company=company,
        action=action,
        object_type=obj.__class__.__name__,
        object_id=str(obj.pk),
        metadata=metadata or {},
    )


def accessible_companies(user):
    from .models import Company
    if user.is_superuser:
        return Company.objects.filter(active=True)
    return Company.objects.filter(
        active=True,
        delegations__user=user,
        delegations__active=True,
        delegations__owner_approved=True,
    ).distinct()


@transaction.atomic
def post_journal(*, company, journal_no, entry_date, lines, actor=None, description="", owner_approved=False):
    """Create and post a balanced double-entry journal as one atomic operation."""
    if not user_has_company_role(actor, company, roles=("manager", "accountant")):
        raise PermissionDenied("User is not authorized for this company accounting operation.")
    require_owner_approval(owner_approved)
    if not lines or len(lines) < 2:
        raise ValidationError("A journal requires at least two lines.")
    journal = Journal.objects.create(
        company=company,
        journal_no=journal_no,
        entry_date=entry_date,
        description=description,
        created_by=actor if getattr(actor, "is_authenticated", False) else None,
        owner_approved=True,
    )
    total_debit = total_credit = 0
    for index, item in enumerate(lines, start=1):
        account = item["account"]
        if account.company_id != company.id or not account.active:
            raise ValidationError("Every account must be active and belong to the journal company.")
        debit = item.get("debit", 0)
        credit = item.get("credit", 0)
        if debit <= 0 and credit <= 0:
            raise ValidationError("Each journal line must have a positive debit or credit.")
        if debit > 0 and credit > 0:
            raise ValidationError("A journal line cannot contain both debit and credit.")
        total_debit += debit
        total_credit += credit
        JournalLine.objects.create(
            journal=journal,
            line_no=index,
            account=account,
            description=item.get("description", ""),
            debit=debit,
            credit=credit,
        )
    if total_debit != total_credit:
        raise ValidationError("Total debit and credit must be equal.")
    journal.status = "posted"
    journal.posted_at = timezone.now()
    journal.save(update_fields=["status", "posted_at"])
    record_audit(
        actor=actor,
        action="journal_posted",
        scope="office.accounting",
        obj=journal,
        metadata={"debit": str(total_debit), "credit": str(total_credit), "line_count": len(lines)},
    )
    return journal
