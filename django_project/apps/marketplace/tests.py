from django.test import TestCase
from django.urls import reverse

from .models import Product


class MarketplacePageTests(TestCase):
    def test_catalog_and_detail(self):
        product = Product.objects.create(
            name="Product", slug="product", price=100, stock=5
        )
        response = self.client.get(reverse("marketplace"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Product")
        response = self.client.get(reverse("marketplace-product", args=[product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Product")
