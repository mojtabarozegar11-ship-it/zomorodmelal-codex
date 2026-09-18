from django.contrib.auth import get_user_model
from django.test import TestCase
from unittest.mock import patch

from .content_agent import ContentAgent
from .content_agent_models import ContentAsset, ContentChannel


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


    @patch("apps.ai.content_agent.get_deepseek_provider")
    def test_configured_provider_generates_structured_assets(self, mock_provider):
        provider = mock_provider.return_value
        provider.generate_json.return_value = {
            "title": "عنوان",
            "script": "اسکریپت",
            "caption": "کپشن",
            "description": "توضیح",
            "hashtags": "#کشاورزی",
            "thumbnail_prompt": "تصویر بندانگشتی",
            "image_prompt": "تصویر اصلی",
        }
        brief = ContentAgent().generate_brief(
            channel=self.channel, topic="آبیاری هوشمند", user=self.staff
        )
        assets = ContentAgent().create_draft_assets(brief, actor=self.staff)
        self.assertEqual(len(assets), 7)
        self.assertTrue(
            ContentAsset.objects.filter(
                brief=brief, metadata__source="deepseek"
            ).exists()
        )
