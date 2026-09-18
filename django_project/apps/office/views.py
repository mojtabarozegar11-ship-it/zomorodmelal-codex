from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from .models import AccountingEntry, Company, CompanyDelegation, Invoice, OfficeTask


@login_required
def dashboard(request):
    companies = Company.objects.filter(active=True)
    context = {
        "companies": companies[:12],
        "delegations": CompanyDelegation.objects.filter(active=True, owner_approved=True).select_related("company", "user")[:12],
        "tasks": OfficeTask.objects.exclude(status="done")[:12],
        "invoices": Invoice.objects.exclude(status="cancelled")[:12],
        "income": AccountingEntry.objects.aggregate(total=Sum("credit"))["total"] or 0,
        "expense": AccountingEntry.objects.aggregate(total=Sum("debit"))["total"] or 0,
    }
    return render(request, "office/dashboard.html", context)
