from dataclasses import dataclass
from typing import Dict

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils import timezone

from apps.common.platform import record_audit, require_owner_approval
from .content_intelligence import ContentIntelligenceEngine\nfrom .content_agent_models import (
    ContentBrief,
    ContentChannel,
    ContentCompetitor,
    ContentPublication,
    ContentAsset,
)


@dataclass
class StrategyInput:
    topic: str
    objective: str = "grow_audience"


class ContentAgent:
    """Domain service for research -> strategy -> production -> approval -> publication."""

    def build_content_plan(self, channel: ContentChannel, topic: str) -> Dict[str, object]:
        strategy = getattr(channel, "strategy", None)
        algorithm_notes = (strategy.algorithm_notes if strategy else {}) or {}
        competitors = list(
            ContentCompetitor.objects.filter(channel=channel, active=True)
            .values("name", "platform", "url", "notes")
        )
        pillars = (strategy.pillars if strategy else []) or [channel.topic]
        formats = (strategy.formats if strategy else []) or ["short_video", "carousel", "post"]
        return {
            "channel": channel.name,
            "platform": channel.platform,
            "topic": topic,
            "pillars": pillars,
            "formats": formats,
            "competitors": competitors,
            "algorithm_notes": algorithm_notes,\n            "platform_variants": self.intelligence.generate_platform_variants(topic=topic, platforms=formats),\n            "baseline_score": score,\n            "research_tasks": [
                "collect_current_topic_signals",
                "collect_competitor_patterns",
                "identify_audience_questions",
                "draft_multiple_angles",
                "score_for_relevance_and_originality",
            ],
        }

    @transaction.atomic
    def generate_brief(self, *, channel: ContentChannel, topic: str, user=None) -> ContentBrief:
        if not topic.strip():
            raise ValueError("Topic is required.")
        plan = self.build_content_plan(channel, topic)
        brief = ContentBrief.objects.create(
            channel=channel,
            topic=topic.strip(),
            objective="grow_audience",
            format=(plan["formats"] or ["short_video"])[0],
            angle=f"Original angle for: {topic.strip()}",
            audience_pain="Identify and answer one concrete audience need.",
            hook=f"چرا {topic.strip()} مهم است؟",
            call_to_action="برای ادامه این موضوع همراه ما باشید.",
            keywords=[topic.strip()],
            status="briefed",
            scorecard={"research": 0, "originality": 0, "clarity": 0, "platform_fit": 0},
            owner_approved=False,
            created_by=user if getattr(user, "is_authenticated", False) else None,
        )
        record_audit(
            actor=user if getattr(user, "is_authenticated", False) else None,
            action="content_brief_created",
            scope="ai.content",
            obj=brief,
            metadata={"channel": channel.name, "topic": topic.strip()},
        )
        return brief

    @transaction.atomic
    def approve_brief(self, brief: ContentBrief, *, actor=None):
        require_owner_approval(True)
        brief.owner_approved = True
        brief.status = "approved"
        brief.save(update_fields=["owner_approved", "status", "updated_at"])
        record_audit(actor=actor, action="content_brief_approved", scope="ai.content", obj=brief)
        return brief

    @transaction.atomic
    def create_draft_assets(self, brief: ContentBrief, *, actor=None):
        """Create platform-ready first drafts. AI providers can replace these drafts."""
        outputs = {
            "title": f"{brief.topic} | راهنمای کاربردی",
            "script": (
                f"شروع: یک سؤال مهم درباره «{brief.topic}».\n"
                "ارزش: سه نکته روشن و کاربردی ارائه کن.\n"
                "پایان: یک اقدام مشخص برای مخاطب پیشنهاد بده."
            ),
            "caption": f"{brief.hook}\n\n{brief.angle}\n\n{brief.call_to_action}",
            "description": f"محتوای آموزشی درباره {brief.topic}.",
            "hashtags": f"#{brief.topic.replace(' ', '_')}",
            "thumbnail_prompt": f"تصویر حرفه‌ای و جذاب برای موضوع {brief.topic} بدون ادعای گمراه‌کننده",
            "image_prompt": f"تصویر اصلی متناسب با موضوع {brief.topic}",
        }
        created = []
        for asset_type, body in outputs.items():
            latest = brief.assets.filter(asset_type=asset_type).order_by("-version").first()
            version = (latest.version + 1) if latest else 1
            created.append(ContentAsset.objects.create(
                brief=brief,
                asset_type=asset_type,
                version=version,
                body=body,
                metadata={"source": "content-agent-template", "platform": brief.channel.platform},
            ))
        brief.status = "review"
        brief.save(update_fields=["status", "updated_at"])
        record_audit(
            actor=actor,
            action="content_assets_generated",
            scope="ai.content",
            obj=brief,
            metadata={"asset_count": len(created)},
        )
        return created


    def approve_publication(self, publication: ContentPublication, *, approved: bool, actor=None):
        if approved:
            require_owner_approval(approved)
            publication.owner_approved = True
            publication.save(update_fields=["owner_approved"])
            record_audit(actor=actor, action="content_publication_approved", scope="ai.content", obj=publication)
        else:
            publication.owner_approved = False
            publication.status = "cancelled"
            publication.save(update_fields=["owner_approved", "status"])
            record_audit(actor=actor, action="content_publication_cancelled", scope="ai.content", obj=publication)
        return publication

    @transaction.atomic
    def queue_publication(self, *, brief: ContentBrief, channel: ContentChannel, actor=None):
        if not brief.owner_approved and channel.auto_publish:
            raise PermissionDenied("OWNER APPROVAL REQUIRED BEFORE ANY SENSITIVE ACTION")
        key = f"content:{brief.pk}:{channel.pk}"
        publication, _ = ContentPublication.objects.get_or_create(
            idempotency_key=key,
            defaults={"brief": brief, "channel": channel, "provider": "manual", "status": "queued"},
        )
        record_audit(
            actor=actor, action="content_publication_queued", scope="ai.content",
            obj=publication, metadata={"channel": channel.name, "platform": channel.platform},
        )
        return publication

    def publish(self, publication: ContentPublication, *, actor=None):
        if publication.status in {"published", "cancelled"}:
            return publication
        if not publication.owner_approved:
            raise PermissionDenied("OWNER APPROVAL REQUIRED BEFORE ANY SENSITIVE ACTION")
        if not publication.brief.assets.filter(approved=True).exists():
            raise PermissionDenied("At least one approved content asset is required before publication.")
        publication.status = "published"
        publication.published_at = timezone.now()
        publication.external_id = f"SIM-{publication.pk}"
        publication.save(update_fields=["status", "published_at", "external_id"])
        record_audit(
            actor=actor, action="content_published", scope="ai.content", obj=publication,
            metadata={"provider": publication.provider, "external_id": publication.external_id},
        )
        return publication


class SocialPlatformAdapter:
    platform = "manual"

    def publish(self, *, publication: ContentPublication, payload: Dict[str, object]) -> Dict[str, object]:
        return {"ok": True, "sandbox": True, "publication_id": publication.pk}


def get_social_adapter(platform: str) -> SocialPlatformAdapter:
    # Real provider adapters can be added without changing the content pipeline.
    return SocialPlatformAdapter()
