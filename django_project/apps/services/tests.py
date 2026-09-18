from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import ServiceCategory, ServiceOffering, ServiceRequest

class ServicesTests(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(name="آموزش", slug="education", description="آموزش کاربردی")
        self.service = ServiceOffering.objects.create(
            category=self.category, name="مشاوره آموزشی", slug="education-consulting",
            summary="مشاوره ساده", description="توضیحات", request_enabled=True
        )

    def test_public_services_page(self):
        response = self.client.get(reverse("services"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "خدمات زمرد ملل")

    def test_search(self):
        response = self.client.get(reverse("services") + "?q=آموزشی")
        self.assertContains(response, "مشاوره آموزشی")

    def test_request_requires_login(self):
        response = self.client.get(reverse("service-request", args=[self.service.slug]))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_request_gets_tracking_code(self):
        user = get_user_model().objects.create_user(username="public", password="pass")
        self.client.force_login(user)
        response = self.client.post(reverse("service-request", args=[self.service.slug]), {"details": "نیاز به مشاوره دارم"})
        self.assertEqual(response.status_code, 302)
        item = ServiceRequest.objects.get(user=user)
        self.assertTrue(item.tracking_code.startswith("ZM-"))

    def test_user_cannot_see_other_request(self):
        user = get_user_model().objects.create_user(username="other", password="pass")
        item_user = get_user_model().objects.create_user(username="owner", password="pass")
        item = ServiceRequest.objects.create(user=item_user, service=self.service, details="private")
        self.client.force_login(user)
        response = self.client.get(reverse("service-request-detail", args=[item.tracking_code]))
        self.assertEqual(response.status_code, 403)
