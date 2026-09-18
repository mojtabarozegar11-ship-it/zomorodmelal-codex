from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from .models import CompanyDelegation, Employee, Invoice, OfficeTask, CashTransaction, InventoryItem
from .services import accessible_companies

@login_required
def summary(request):
    companies = accessible_companies(request.user)
    return JsonResponse({
        "companies": companies.count(),
        "delegations": CompanyDelegation.objects.filter(company__in=companies, active=True, owner_approved=True).count(),
        "employees": Employee.objects.filter(company__in=companies, active=True).count(),
        "open_tasks": OfficeTask.objects.filter(company__in=companies).exclude(status="done").count(),
        "invoices": Invoice.objects.filter(company__in=companies).exclude(status="cancelled").count(),
        "inventory_items": InventoryItem.objects.filter(company__in=companies).count(),
        "cash_in": str(CashTransaction.objects.filter(company__in=companies, kind="in").aggregate(x=Sum("amount"))["x"] or 0),
        "cash_out": str(CashTransaction.objects.filter(company__in=companies, kind="out").aggregate(x=Sum("amount"))["x"] or 0),
    })
