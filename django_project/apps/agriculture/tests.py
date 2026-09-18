from django.test import TestCase
from django.urls import reverse

from .models import Farm, ProductionChain, ProductionProduct


class AgriculturePageTests(TestCase):
    def test_dashboard(self):
        Farm.objects.create(name="Farm")
        ProductionProduct.objects.create(name="Almond", category="orchard")
        ProductionChain.objects.create(name="Almond Chain")
        response = self.client.get(reverse("agriculture-dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Almond Chain")
