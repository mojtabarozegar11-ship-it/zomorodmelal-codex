from django.contrib import admin
from .models import Asset, EconomicAuditLog, EconomicPublication, EconomicReport, EconomicWorkItem, MarketDataSnapshot, OrderIntent, Portfolio, Position, RiskPolicy, Signal, SignalCoupon, SignalPerformance, SignalProduct, SignalPurchase, SignalSubscription, Strategy, Trade, VirtualAssetProject

for model in (Asset, MarketDataSnapshot, Strategy, RiskPolicy, Portfolio, Position, OrderIntent, Trade, EconomicReport, EconomicAuditLog, SignalProduct, SignalPurchase, SignalSubscription, SignalCoupon, SignalPerformance, Signal, VirtualAssetProject, EconomicWorkItem, EconomicPublication, GoldOrder):
    admin.site.register(model)
