from django.contrib import admin
from .models import Asset, EconomicAuditLog, EconomicReport, MarketDataSnapshot, OrderIntent, Portfolio, Position, RiskPolicy, Signal, SignalProduct, SignalPurchase, Strategy, Trade

for model in (Asset, MarketDataSnapshot, Strategy, RiskPolicy, Portfolio, Position, OrderIntent, Trade, EconomicReport, EconomicAuditLog, SignalProduct, SignalPurchase, Signal):
    admin.site.register(model)
