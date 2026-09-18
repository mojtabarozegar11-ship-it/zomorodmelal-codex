from .models import AuditLog, CompanyDelegation

def user_has_company_role(user, company, roles=()):
    if not user.is_authenticated: return False
    if user.is_superuser: return True
    qs=CompanyDelegation.objects.filter(user=user, company=company, active=True, owner_approved=True)
    return not roles or qs.filter(role__in=roles).exists()

def audit(actor, action, obj, company=None, metadata=None):
    return AuditLog.objects.create(actor=actor, company=company, action=action, object_type=obj.__class__.__name__, object_id=str(obj.pk), metadata=metadata or {})

def accessible_companies(user):
    """Return only companies explicitly delegated to the user, unless superuser."""
    from .models import Company
    if user.is_superuser:
        return Company.objects.filter(active=True)
    return Company.objects.filter(
        active=True,
        delegations__user=user,
        delegations__active=True,
        delegations__owner_approved=True,
    ).distinct()
