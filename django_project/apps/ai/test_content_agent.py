from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.ai.content_agent import ContentAgent
from apps.ai.content_agent_models import ContentChannel


class ContentAgentTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="content-admin", password="test-pass")
        self.channel = ContentChannel.objects.create(
            name="کانال کشاورزی",
            platform="youtube",
            topic="کشاورزی هوشمند",
        )

    def test_plan_contains_platform_variants(self):
        plan = ContentAgent().build_content_plan(self.channel, "آبیاری هوشمند")
        self.assertEqual(plan["channel"], "کانال کشاورزی")
        self.assertTrue(plan["platform_variants"])
        self.assertIn("baseline_score", plan)

    def test_generate_brief_and_assets(self):
        agent = ContentAgent()
        brief = agent.generate_brief(channel=self.channel, topic="آبیاری", user=self.user)
        assets = agent.create_draft_assets(brief, actor=self.user)
        self.assertEqual(brief.status, "review")
        self.assertGreaterEqual(len(assets), 5)

    def test_publication_needs_owner_approval(self):
        brief = ContentAgent().generate_brief(channel=self.channel, topic="آبیاری", user=self.user)
        publication = ContentAgent().queue_publication(brief=brief, channel=self.channel, actor=self.user)
        with self.assertRaises(Exception):
            ContentAgent().publish(publication, actor=self.user)
