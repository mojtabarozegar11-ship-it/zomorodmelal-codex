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
    path("economy/", dashboard, name="economy-dashboard"),
    path("economy/signals/", signal_store, name="signal-store"),
    path(
        "economy/signals/buy/<int:product_id>/",
        signal_checkout,
        name="signal-checkout",
    ),
    path(
        "economy/signals/checkout/<int:purchase_id>/",
        signal_checkout_page,
        name="signal-checkout-page",
    ),
    path("api/economy/health/", health, name="economy-health"),
    path("api/economy/gold/", gold_market, name="gold-market"),
    path(
        "api/economy/gold/orders/",
        gold_order_create,
        name="gold-order-create",
    ),
]
