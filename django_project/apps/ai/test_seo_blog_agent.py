from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from .seo_blog_agent import DEFAULT_LANGUAGES, RUN_TIME, SeoBlogOperationsAgent, should_run_at
from .content_agent_models import BlogPlatform


class SeoBlogAgentTests(TestCase):
    def setUp(self):
        for i, language in enumerate(DEFAULT_LANGUAGES):
            BlogPlatform.objects.create(
                name=f"Blog {i}",
                platform=f"platform-{i}",
                base_url=f"https://example.com/{i}",
                language=language,
                legal_terms_reviewed=True,
                account_ready=True,
                credentials_configured=True,
            )

    def test_run_time_is_exactly_three_am(self):
        self.assertTrue(should_run_at(timezone.make_aware(datetime(2026, 9, 20, 3, 0))))
        self.assertFalse(should_run_at(timezone.make_aware(datetime(2026, 9, 20, 3, 1))))
        self.assertFalse(should_run_at(timezone.make_aware(datetime(2026, 9, 20, 4, 0))))

    def test_daily_run_builds_five_text_only_items(self):
        run = SeoBlogOperationsAgent().run(now=timezone.make_aware(datetime(2026, 9, 20, 3, 0)))
        self.assertEqual(run.target_count, 5)
        self.assertEqual(run.target_languages, list(DEFAULT_LANGUAGES))
        self.assertEqual(run.items.count(), 5)
        self.assertTrue(all(item.seo_metadata["text_only"] for item in run.items.all()))
        self.assertEqual(run.published_count, 0)
        self.assertEqual(run.pending_count, 5)
        self.assertEqual(run.status, "partial")

