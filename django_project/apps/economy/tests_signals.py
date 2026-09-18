from django.contrib.auth import get_user_model
from django.test import TestCase
from .gateway import get_payment_gateway
from .models import SignalProduct, SignalPurchase

class SignalSalesTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="buyer", password="pass")
        self.product = SignalProduct.objects.create(name="Demo Signal", description="Demo", price="1000", currency="IRR")
    def test_sandbox_checkout(self):
        purchase = SignalPurchase.objects.create(product=self.product, user=self.user, amount=self.product.price)
        result = get_payment_gateway().create_checkout(purchase)
        self.assertTrue(result["sandbox"])
        self.assertTrue(result["authority"].startswith("SANDBOX-"))
        self.assertEqual(SignalPurchase.objects.get(pk=purchase.pk).status, "pending")


    def test_coupon_model_can_be_created(self):
        from .models import SignalCoupon
        coupon = SignalCoupon.objects.create(code="WELCOME", percent=10)
        self.assertEqual(coupon.percent, 10)
