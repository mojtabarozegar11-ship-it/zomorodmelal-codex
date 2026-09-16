from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from autonomous_core.agent_factory import AgentFactory


class AgentOrchestrator:
    """Plans bounded multi-agent work without performing external actions."""

    ROUTE_CACHE_SECONDS = 15.0

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()
        self.factory = AgentFactory(self.root)
        self.path = self.root / "data" / "agent_orchestration.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._route_cache: Dict[str, Any] | None = None
        self._route_cache_key: str | None = None
        self._route_cache_at = 0.0

    def route(self, goal: str | None) -> Dict[str, Any]:
        cache_key = str(goal or "").strip().lower() or "general autonomous improvement"
        now = time.monotonic()
        if (self._route_cache is not None and self._route_cache_key == cache_key
                and now - self._route_cache_at < self.ROUTE_CACHE_SECONDS):
            return dict(self._route_cache)

        text = cache_key
        roles = []
        mapping = {
            "research": ("research",),
            "site": ("website", "engineering", "testing", "security"),
            "website": ("website", "engineering", "testing", "security"),
            "django": ("website", "engineering", "testing", "security"),
            "test": ("testing", "engineering"),
            "repair": ("testing", "engineering", "security"),
            "security": ("security", "testing"),
            "agri": ("agriculture", "research", "knowledge"),
            "کشاور": ("agriculture", "research", "knowledge"),
            "content": ("content", "knowledge", "security"),
            "knowledge": ("knowledge", "research"),
            "business": ("business", "research", "knowledge"),
        }
        for needle, candidates in mapping.items():
            if needle in text:
                roles.extend(candidates)
        if not roles:
            roles = ["research", "engineering", "testing", "security"]
        roles = list(dict.fromkeys(roles))
        agents = [self.factory.ensure_agent(role, goal or "autonomous mission") for role in roles]
        plan = {
            "goal": goal,
            "agents": [a["agent_id"] for a in agents],
            "sequence": roles,
            "status": "sandbox_planned",
            "owner_approval_required": True,
            "real_world_actions": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.path)
        self._route_cache = dict(plan)
        self._route_cache_key = cache_key
        self._route_cache_at = now
        return plan
