from django.contrib.auth import get_user_model
from django.test import TestCase

from .content_agent import ContentAgent
from .content_agent_models import ContentChannel


class ContentAgentPipelineTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com"
        )
        self.staff = User.objects.create_user(
            username="staff", password="test-password", is_staff=True
        )
        self.channel = ContentChannel.objects.create(
            name="کشاورزی هوشمند",
            platform="youtube",
            topic="کشاورزی",
        )

    def test_research_and_competitor_signals_are_recorded_in_brief(self):
        brief = ContentAgent().generate_brief(
            channel=self.channel, topic="آبیاری هوشمند", user=self.staff
        )
        self.assertEqual(brief.status, "briefed")
        self.assertIn("competitors", brief.scorecard)

    def test_non_owner_cannot_approve_brief(self):
        brief = ContentAgent().generate_brief(
            channel=self.channel, topic="آبیاری هوشمند", user=self.staff
        )
        with self.assertRaises(Exception):
            ContentAgent().approve_brief(brief, actor=self.staff)

    def test_owner_can_approve_brief(self):
        brief = ContentAgent().generate_brief(
            channel=self.channel, topic="آبیاری هوشمند", user=self.staff
        )
        ContentAgent().approve_brief(brief, actor=self.owner)
        self.assertTrue(brief.owner_approved)
        self.assertEqual(brief.status, "approved")
