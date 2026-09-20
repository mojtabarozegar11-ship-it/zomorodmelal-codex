"""Scheduled SEO blog operations for Content Agent supervision.

This module is intentionally isolated from ordinary website request handling.
It prepares five language-specific, text-only blog items and records the
publication state for legally configured external blog platforms.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import time
from typing import Dict, Iterable, List, Sequence

from django.db import transaction
from django.utils import timezone

from .content_agent import ContentAgent
from .content_agent_models import BlogPlatform, SeoBlogItem, SeoBlogRun


RUN_TIME = time(hour=3, minute=0)
DEFAULT_LANGUAGES = ("fa", "en", "ar", "tr", "ru")


@dataclass(frozen=True)
class BlogPlan:
    languages: Sequence[str] = DEFAULT_LANGUAGES
    target_count: int = 5


class SeoBlogOperationsAgent:
    """Runs the daily text-only SEO/blog workflow under ContentAgent supervision."""

    agent_name = "SEO Blog Operations Agent"

    def eligible_blogs(self) -> List[BlogPlatform]:
        return list(
            BlogPlatform.objects.filter(
                active=True,
                legal_terms_reviewed=True,
                account_ready=True,
                credentials_configured=True,
            ).order_by("name")[:5]
        )

    @staticmethod
    def seo_metadata(*, title: str, language: str, keywords: Iterable[str]) -> Dict[str, object]:
        unique_keywords = list(dict.fromkeys(str(item).strip() for item in keywords if str(item).strip()))
        return {
            "title": title,
            "meta_description": f"اطلاعات ارزشمند درباره {title}"[:160],
            "keywords": unique_keywords[:12],
            "language": language,
            "content_type": "article",
            "text_only": True,
        }

    @staticmethod
    def build_body(topic: str, language: str) -> str:
        templates = {
            "fa": f"این مطلب به معرفی ظرفیت‌ها، خدمات و فعالیت‌های شرکت کشت و صنعت زمرد ملل در حوزه «{topic}» می‌پردازد و اطلاعات کاربردی و قابل استناد ارائه می‌کند.",
            "en": f"This article introduces Zomorod Melal Agricultural and Industrial Company in the area of “{topic}” and provides useful, factual information.",
            "ar": f"يقدم هذا المقال تعريفاً بشركة زمرد ملل الزراعية والصناعية في مجال «{topic}» مع معلومات عملية وموثوقة.",
            "tr": f"Bu yazı, Zomorod Melal Tarım ve Sanayi Şirketi'nin “{topic}” alanındaki faaliyetlerini tanıtır ve faydalı, doğrulanabilir bilgiler sunar.",
            "ru": f"В этой статье представлена компания Zomorod Melal Agricultural and Industrial Company в области «{topic}» и приведена полезная, проверяемая информация.",
        }
        return templates.get(language, templates["en"])

    @transaction.atomic
    def create_daily_run(self, *, now=None, topic: str = "معرفی ارزشمند شرکت و سایت") -> SeoBlogRun:
        now = timezone.localtime(now or timezone.now())
        run, _ = SeoBlogRun.objects.get_or_create(
            run_date=now.date(),
            scheduled_time=RUN_TIME,
            defaults={
                "target_languages": list(DEFAULT_LANGUAGES),
                "target_count": 5,
                "status": "planned",
            },
        )
        return run

    @transaction.atomic
    def run(self, *, topic: str = "معرفی ارزشمند شرکت و سایت", now=None) -> SeoBlogRun:
        """Prepare the daily five-item run; publish only through configured legal adapters."""
        now = timezone.localtime(now or timezone.now())
        run = self.create_daily_run(now=now, topic=topic)
        run.status = "running"
        run.started_at = timezone.now()
        run.target_languages = list(DEFAULT_LANGUAGES)
        run.target_count = 5
        run.save(update_fields=["status", "started_at", "target_languages", "target_count"])

        blogs = self.eligible_blogs()
        if len(blogs) < 5:
            run.status = "partial"
            run.pending_count = max(0, 5 - len(blogs))
            run.report = {
                "reason": "fewer_than_five_legal_ready_blog_accounts",
                "required": 5,
                "available": len(blogs),
                "next_action": "acquire_legal_access_for_additional_platforms",
            }
            run.finished_at = timezone.now()
            run.save(update_fields=["status", "pending_count", "report", "finished_at"])
            return run

        ContentAgent()  # explicit supervision boundary
        published = 0
        pending = 0
        failed = 0
        for language, blog in zip(DEFAULT_LANGUAGES, blogs):
            title = f"{topic} | Zomorod Melal"
            item, _ = SeoBlogItem.objects.get_or_create(
                run=run,
                blog=blog,
                defaults={
                    "language": language,
                    "topic": topic,
                    "title": title,
                    "body": self.build_body(topic, language),
                    "seo_metadata": self.seo_metadata(
                        title=title,
                        language=language,
                        keywords=[topic, "Zomorod Melal"],
                    ),
                    "status": "ready",
                },
            )
            # No external publisher adapter is wired into this agent yet.
            # Never report a generated draft as published.
            item.status = "pending_access"
            pending += 1
            item.save(update_fields=["status"])
        run.published_count = published
        run.pending_count = pending
        run.failed_count = failed
        run.status = "partial" if pending else ("failed" if failed else "completed")
        run.report = {
            "supervised_by": ContentAgent.__name__,
            "text_only": True,
            "languages": list(DEFAULT_LANGUAGES),
            "blog_count": len(blogs),
            "published_count": published,
            "pending_count": pending,
            "failed_count": failed,
        }
        run.finished_at = timezone.now()
        run.save(
            update_fields=[
                "published_count",
                "pending_count",
                "failed_count",
                "status",
                "report",
                "finished_at",
            ]
        )
        return run


def should_run_at(now=None) -> bool:
    now = timezone.localtime(now or timezone.now())
    return now.hour == RUN_TIME.hour and now.minute == RUN_TIME.minute
