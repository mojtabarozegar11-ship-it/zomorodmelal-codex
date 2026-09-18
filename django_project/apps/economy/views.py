from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .agents import EconomicMasterAgent
from .gateway import get_payment_gateway
from .models import Asset, EconomicWorkItem, MarketDataSnapshot, OrderIntent, Portfolio, SignalProduct, SignalPurchase, VirtualAssetProject

def dashboard(request):
    return render(request, "economy/dashboard.html", {"assets": Asset.objects.filter(active=True).count(), "portfolios": Portfolio.objects.filter(active=True).count(), "orders": OrderIntent.objects.count(), "market_points": MarketDataSnapshot.objects.count(), "signals": SignalProduct.objects.filter(active=True).count(), "virtual_assets": VirtualAssetProject.objects.filter(active=True).count(), "work_items": EconomicWorkItem.objects.exclude(status="done").count(), "agents": EconomicMasterAgent().capabilities()})

def health(request):
    return JsonResponse({"economic_agent": "ready", "specialized_agents": EconomicMasterAgent().capabilities(), "paper_trading": True, "real_execution": False, "owner_approval_required": True, "virtual_asset_issuance": "gated", "legal_review_required": True, "signal_sales": True, "payment_gateway": "sandbox"})

def signal_store(request):
    return render(request, "economy/signals.html", {"products": SignalProduct.objects.filter(active=True).order_by("-created_at")})

@require_POST
def signal_checkout(request, product_id):
    product = get_object_or_404(SignalProduct, pk=product_id, active=True)
    if not request.user.is_authenticated: return redirect("/admin/login/?next=/economy/signals/")
    purchase = SignalPurchase.objects.create(product=product, user=request.user, amount=product.price, currency=product.currency)
    checkout = get_payment_gateway().create_checkout(purchase)
    return render(request, "economy/checkout.html", {"purchase": purchase, "checkout": checkout})

def signal_checkout_page(request, purchase_id):
    purchase = get_object_or_404(SignalPurchase, pk=purchase_id)
    if request.user.is_authenticated and purchase.user_id != request.user.id and not request.user.is_staff: return JsonResponse({"detail": "forbidden"}, status=403)
    return render(request, "economy/checkout.html", {"purchase": purchase, "checkout": {"authority": purchase.authority, "sandbox": True}})
