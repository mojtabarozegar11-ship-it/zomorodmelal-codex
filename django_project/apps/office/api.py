from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from .models import Company, CompanyDelegation, Employee, Invoice, OfficeTask, CashTransaction, InventoryItem

@login_required
def summary(request):
    companies=Company.objects.filter(active=True)
    return JsonResponse({"companies":companies.count(),"delegations":CompanyDelegation.objects.filter(active=True,owner_approved=True).count(),"employees":Employee.objects.filter(active=True).count(),"open_tasks":OfficeTask.objects.exclude(status="done").count(),"invoices":Invoice.objects.exclude(status="cancelled").count(),"inventory_items":InventoryItem.objects.count(),"cash_in":str(CashTransaction.objects.filter(kind="in").aggregate(x=Sum("amount"))["x"] or 0),"cash_out":str(CashTransaction.objects.filter(kind="out").aggregate(x=Sum("amount"))["x"] or 0)})
