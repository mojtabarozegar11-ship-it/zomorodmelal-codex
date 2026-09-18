from uuid import uuid4
from django.utils import timezone
from .models import SignalPurchase


class PaymentGateway:
    name = "sandbox"

    def create_checkout(self, purchase):
        """Create a sandbox checkout reference. No real money is charged."""
        authority = "SANDBOX-" + uuid4().hex
        purchase.gateway = self.name
        purchase.authority = authority
        purchase.save(update_fields=["gateway", "authority"])
        return {"authority": authority, "checkout_url": "/economy/signals/checkout/{}/".format(purchase.pk), "sandbox": True}

    def verify(self, purchase, success=False):
        if not success:
            purchase.status = "failed"
            purchase.save(update_fields=["status"])
            return False
        purchase.status = "paid"
        purchase.paid_at = timezone.now()
        purchase.save(update_fields=["status", "paid_at"])
        return True


def get_payment_gateway():
    return PaymentGateway()
