from dataclasses import dataclass
from typing import Dict

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils import timezone

from apps.common.platform import record_audit, require_owner_approval
from .content_intelligence import (
    CompetitorPattern,
    ContentIntelligenceEngine,
    ResearchSignal,
)
from .content_agent_models import (
    ContentAsset,
    ContentBrief,
    ContentChannel,
    ContentCompetitor,
    ContentPublication,
)


@dataclass
class StrategyInput:
    topic: str
    objective: str = "grow_audience"


class ContentAgent:
    """Research -> strategy -> production -> approval -> publication."""

    def __init__(self):
        self.intelligence = ContentIntelligenceEngine()

    def build_content_plan(self, channel: ContentChannel, topic: str) -> Dict[str, object]:
        strategy = getattr(channel, "strategy", None)
        algorithm_notes = (strategy.algorithm_notes if strategy else {}) or {}
        competitors = list(
            ContentCompetitor.objects.filter(channel=channel, active=True)
            .values("name", "platform", "url", "notes")
        )
        pillars = (strategy.pillars if strategy else []) or [channel.topic]
        formats = (strategy.formats if strategy else []) or ["short_video", "carousel", "post"]
        score = self.intelligence.score_content(
            relevance=70, originality=70, clarity=80, platform_fit=80
        )
        return {
            "channel": channel.name,
            "platform": channel.platform,
            "topic": topic,
            "pillars": pillars,
            "formats": formats,
            "competitors": competitors,
            "algorithm_notes": algorithm_notes,
            "platform_variants": self.intelligence.generate_platform_variants(
                topic=topic, platforms=formats
            ),
            "baseline_score": score,
            "research_tasks": [
                "collect_current_topic_signals",
                "collect_competitor_patterns",
                "identify_audience_questions",
                "draft_multiple_angles",
                "score_for_relevance_and_originality",
            ],
        }

    def research_snapshot(self, channel: ContentChannel, topic: str):
        signals = list(
            channel.research_snapshots.filter(query__icontains=topic)
            .values("source", "title", "summary", "metrics")[:20]
        )
        return self.intelligence.summarize_research(
            [
                ResearchSignal(
                    source=item["source"],
                    title=item["title"] or topic,
                    summary=item["summary"],
                    metrics=item["metrics"] or {},
                )
                for item in signals
            ]
        )

    def competitor_snapshot(self, channel: ContentChannel):
        patterns = list(
            channel.competitors.filter(active=True)
            .values("name", "platform", "notes")[:50]
        )
        return self.intelligence.compare_competitors(
            [
                CompetitorPattern(
                    name=item["name"],
                    platform=item["platform"],
                    pattern=item["notes"] or "observed competitor pattern",
                    evidence=item["notes"] or "",
                )
                for item in patterns
            ]
        )

    @transaction.atomic
    def generate_brief(self, *, channel: ContentChannel, topic: str, user=None) -> ContentBrief:
        if not topic.strip():
            raise ValueError("Topic is required.")
        plan = self.build_content_plan(channel, topic)
        research = self.research_snapshot(channel, topic)
        competitors = self.competitor_snapshot(channel)
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
            scorecard={
                "research": min(100, research.get("signal_count", 0) * 10),
                "originality": 70,
                "clarity": 80,
                "platform_fit": 80,
                "competitors": competitors.get("competitor_count", 0),
            },
            owner_approved=False,
            created_by=user if getattr(user, "is_authenticated", False) else None,
        )
        record_audit(
            actor=user if getattr(user, "is_authenticated", False) else None,
            action="content_brief_created",
            scope="ai.content",
            obj=brief,
            metadata={
                "channel": channel.name,
                "topic": topic.strip(),
                "research": research,
                "competitors": competitors,
            },
        )
        return brief

    @transaction.atomic
    def approve_brief(self, brief: ContentBrief, *, actor=None):
        if not getattr(actor, "is_authenticated", False) or not getattr(
            actor, "is_superuser", False
        ):
            raise PermissionDenied("Only the owner can approve content.")
        require_owner_approval(True)
        brief.owner_approved = True
        brief.status = "approved"
        brief.save(update_fields=["owner_approved", "status", "updated_at"])
        record_audit(
            actor=actor, action="content_brief_approved",
            scope="ai.content", obj=brief
        )
        return brief

    @transaction.atomic
    def create_draft_assets(self, brief: ContentBrief, *, actor=None):
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
            "thumbnail_prompt": (
                f"تصویر حرفه‌ای و جذاب برای موضوع {brief.topic} "
                "بدون ادعای گمراه‌کننده"
            ),
            "image_prompt": f"تصویر اصلی متناسب با موضوع {brief.topic}",
        }
        created = []
        for asset_type, body in outputs.items():
            latest = (
                brief.assets.filter(asset_type=asset_type)
                .order_by("-version")
                .first()
            )
            version = (latest.version + 1) if latest else 1
            created.append(
                ContentAsset.objects.create(
                    brief=brief,
                    asset_type=asset_type,
                    version=version,
                    body=body,
                    metadata={
                        "source": "content-agent-template",
                        "platform": brief.channel.platform,
                    },
                )
            )
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

    @transaction.atomic
    def approve_publication(self, publication: ContentPublication, *, approved: bool, actor=None):
        if approved:
            if not getattr(actor, "is_authenticated", False) or not getattr(
                actor, "is_superuser", False
            ):
                raise PermissionDenied("Only the owner can approve publication.")
            require_owner_approval(True)
            publication.owner_approved = True
            publication.save(update_fields=["owner_approved"])
            record_audit(
                actor=actor,
                action="content_publication_approved",
                scope="ai.content",
                obj=publication,
            )
        else:
            publication.owner_approved = False
            publication.status = "cancelled"
            publication.save(update_fields=["owner_approved", "status"])
            record_audit(
                actor=actor,
                action="content_publication_cancelled",
                scope="ai.content",
                obj=publication,
            )
        return publication

    @transaction.atomic
    def queue_publication(self, *, brief: ContentBrief, channel: ContentChannel, actor=None):
        if not brief.owner_approved and channel.auto_publish:
            raise PermissionDenied("OWNER APPROVAL REQUIRED BEFORE ANY SENSITIVE ACTION")
        key = f"content:{brief.pk}:{channel.pk}"
        publication, _ = ContentPublication.objects.get_or_create(
            idempotency_key=key,
            defaults={
                "brief": brief,
                "channel": channel,
                "provider": "manual",
                "status": "queued",
            },
        )
        record_audit(
            actor=actor,
            action="content_publication_queued",
            scope="ai.content",
            obj=publication,
            metadata={"channel": channel.name, "platform": channel.platform},
        )
        return publication

    @transaction.atomic
    def publish(self, publication: ContentPublication, *, actor=None):
        if publication.status in {"published", "cancelled"}:
            return publication
        if not publication.owner_approved:
            raise PermissionDenied("OWNER APPROVAL REQUIRED BEFORE ANY SENSITIVE ACTION")
        if not publication.brief.assets.filter(approved=True).exists():
            raise PermissionDenied(
                "At least one approved content asset is required before publication."
            )
        adapter = get_social_adapter(publication.channel.platform)
        publication.status = "publishing"
        publication.save(update_fields=["status"])
        result = adapter.publish(
            publication=publication, payload=publication.payload or {}
        )
        if not result.get("ok"):
            publication.status = "failed"
            publication.response_metadata = result
            publication.save(update_fields=["status", "response_metadata"])
            return publication
        publication.status = "published"
        publication.published_at = timezone.now()
        publication.external_id = str(
            result.get("external_id") or f"SIM-{publication.pk}"
        )
        publication.response_metadata = result
        publication.save(
            update_fields=[
                "status",
                "published_at",
                "external_id",
                "response_metadata",
            ]
        )
        record_audit(
            actor=actor,
            action="content_published",
            scope="ai.content",
            obj=publication,
            metadata={
                "provider": publication.provider,
                "external_id": publication.external_id,
                "sandbox": result.get("sandbox", True),
            },
        )
        return publication


class SocialPlatformAdapter:
    platform = "manual"

    def publish(self, *, publication: ContentPublication, payload: Dict[str, object]):
        return {
            "ok": True,
            "sandbox": True,
            "provider": self.platform,
            "publication_id": publication.pk,
            "external_id": f"SIM-{self.platform}-{publication.pk}",
        }


class PlatformAdapterRegistry:
    _adapters = {}

    @classmethod
    def register(cls, platform, adapter):
        cls._adapters[platform] = adapter

    @classmethod
    def resolve(cls, platform):
        adapter = cls._adapters.get(platform)
        return adapter() if adapter else SocialPlatformAdapter()


def get_social_adapter(platform: str) -> SocialPlatformAdapter:
    return PlatformAdapterRegistry.resolve(platform)
