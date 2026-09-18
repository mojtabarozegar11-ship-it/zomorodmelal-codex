from django.test import TestCase
from django.urls import reverse

from .models import ResearchProject


class ResearchPageTests(TestCase):
    def test_project_pages(self):
        project = ResearchProject.objects.create(title="Research", summary="Summary")
        response = self.client.get(reverse("research-home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Research")
        response = self.client.get(reverse("research-project", args=[project.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Summary")
