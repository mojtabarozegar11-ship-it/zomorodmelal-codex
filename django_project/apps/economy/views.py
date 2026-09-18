from django.http import JsonResponse
from django.shortcuts import render
from .agents import EconomicMasterAgent
from .models import Asset, OrderIntent, Portfolio, MarketDataSnapshot


def dashboard(request):
    context = {
        "assets": Asset.objects.filter(active=True).count(),
        "portfolios": Portfolio.objects.filter(active=True).count(),
        "orders": OrderIntent.objects.count(),
        "market_points": MarketDataSnapshot.objects.count(),
        "agents": EconomicMasterAgent().capabilities(),
    }
    return render(request, "economy/dashboard.html", context)


def health(request):
    return JsonResponse({"economic_agent": "ready", "paper_trading": True, "real_execution": False, "owner_approval_required": True})
