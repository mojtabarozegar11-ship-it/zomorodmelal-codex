from django.urls import path

from .views import (
    dashboard,
    gold_market,
    gold_order_create,
    health,
    signal_checkout,
    signal_checkout_page,
    signal_store,
)

urlpatterns = [
    path("", dashboard, name="economy-dashboard"),
    path("signals/", signal_store, name="signal-store"),
    path(
        "signals/buy/<int:product_id>/",
        signal_checkout,
        name="signal-checkout",
    ),
    path(
        "signals/checkout/<int:purchase_id>/",
        signal_checkout_page,
        name="signal-checkout-page",
    ),
    path("api/health/", health, name="economy-health"),
    path("api/gold/", gold_market, name="gold-market"),
    path(
        "api/gold/orders/",
        gold_order_create,
        name="gold-order-create",
    ),
]
