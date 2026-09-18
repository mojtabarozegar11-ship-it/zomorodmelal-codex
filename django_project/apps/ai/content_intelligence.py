"""Pluggable content-intelligence engine.

The engine deliberately separates collection, analysis, generation and publication.
Network providers can be attached later; without them the system remains deterministic
and auditable instead of pretending to have live platform data.
"""
from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass(frozen=True)
class ResearchSignal:
    source: str
    title: str
    summary: str = ""
    metrics: Dict[str, float] | None = None


@dataclass(frozen=True)
class CompetitorPattern:
    name: str
    platform: str
    pattern: str
    evidence: str = ""


class ContentIntelligenceEngine:
    def summarize_research(self, signals: Iterable[ResearchSignal]) -> Dict[str, object]:
        items = list(signals)
        return {
            "signal_count": len(items),
            "sources": sorted({item.source for item in items}),
            "topics": [item.title for item in items[:20]],
        }

    def compare_competitors(self, patterns: Iterable[CompetitorPattern]) -> Dict[str, object]:
        items = list(patterns)
        return {
            "competitor_count": len(items),
            "platforms": sorted({item.platform for item in items}),
            "patterns": [item.__dict__ for item in items[:50]],
        }

    def score_content(self, *, relevance: float, originality: float, clarity: float, platform_fit: float) -> Dict[str, float]:
        values = {
            "relevance": max(0.0, min(100.0, relevance)),
            "originality": max(0.0, min(100.0, originality)),
            "clarity": max(0.0, min(100.0, clarity)),
            "platform_fit": max(0.0, min(100.0, platform_fit)),
        }
        values["overall"] = round(sum(values.values()) / 4.0, 2)
        return values

    def generate_platform_variants(self, *, topic: str, platforms: Iterable[str]) -> List[Dict[str, str]]:
        variants = []
        for platform in platforms:
            if platform == "youtube":
                fmt, cta = "video", "برای ادامه موضوع کانال را دنبال کنید."
            elif platform == "instagram":
                fmt, cta = "reel", "نظر خودتان را در کامنت بنویسید."
            elif platform == "tiktok":
                fmt, cta = "short_video", "این موضوع را ذخیره کنید و ادامه را ببینید."
            elif platform == "linkedin":
                fmt, cta = "professional_post", "دیدگاه حرفه‌ای خود را مطرح کنید."
            else:
                fmt, cta = "post", "برای دریافت ادامه محتوا همراه ما باشید."
            variants.append({"platform": platform, "format": fmt, "cta": cta, "topic": topic})
        return variants
