from django.core.management.base import BaseCommand
from apps.economy.models import Asset, SignalProduct

class Command(BaseCommand):
    help = "Create a safe demo signal product."
    def handle(self, *args, **kwargs):
        asset, _ = Asset.objects.get_or_create(symbol="DEMO", defaults={"name":"Demo Asset", "asset_type":"stock"})
        product, created = SignalProduct.objects.get_or_create(name="Demo Signals", defaults={"description":"Demo informational signals", "price":"100000", "currency":"IRR"})
        self.stdout.write(self.style.SUCCESS("Demo signal product ready: %s" % product.name))
