from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union


class AutonomousDecisionEngine:
    """Choose the safest useful next mission from local evidence."""

    CACHE_SECONDS = 15.0

    def __init__(self, root: Union[str, Path]) -> None:
        self.root = Path(root).resolve()
        self.path = self.root / "data" / "autonomous_decisions.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._cache: Optional[Dict[str, Any]] = None
        self._cache_key: Optional[Tuple[Tuple[str, int, int], ...]] = None
        self._cache_at = 0.0

    def _load_json(self, name: str, default: Any) -> Any:
        try:
            return json.loads((self.root / "data" / name).read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError):
            return default

    def _evidence_key(self) -> Tuple[Tuple[str, int, int], ...]:
        names = (
            "project_discovery.json",
            "autonomous_goal_engine.json",
            "autonomous_mission_queue.json",
            "test_results.json",
            "self_repair_mission.json",
            "agent_registry.json",
        )
        key = []
        for name in names:
            path = self.root / "data" / name
            try:
                stat = path.stat()
                key.append((name, stat.st_mtime_ns, stat.st_size))
            except OSError:
                key.append((name, 0, 0))
        return tuple(key)

    def assess(self) -> Dict[str, Any]:
        now = time.monotonic()
        evidence_key = self._evidence_key()
        if (
            self._cache is not None
            and self._cache_key == evidence_key
            and now - self._cache_at < self.CACHE_SECONDS
        ):
            result = dict(self._cache)
            result["fast_path"] = True
            return result

        discovery = self._load_json("project_discovery.json", {})
        goal_state = self._load_json("autonomous_goal_engine.json", {})
        mission_state = self._load_json("autonomous_mission_queue.json", {})
        tests = self._load_json("test_results.json", [])
        repair = self._load_json("self_repair_mission.json", {})
        agents = self._load_json("agent_registry.json", [])

        files = discovery.get("files", []) if isinstance(discovery, dict) else []
        py = [x for x in files if str(x.get("path", "")).endswith(".py")]
        html = [x for x in files if str(x.get("path", "")).endswith(".html")]
        django = bool(discovery.get("django_detected"))
        syntax_errors = [x for x in py if x.get("syntax_ok") is False]

        history = goal_state.get("history", []) if isinstance(goal_state, dict) else []
        recent_repair = any(x.get("status") == "needs_repair" for x in history[-10:])
        repair_ready = isinstance(repair, dict) and repair.get("status") == "queued_for_sandbox_repair"
        queue = mission_state.get("missions", mission_state.get("queue", [])) if isinstance(mission_state, dict) else []
        pending_missions = sum(1 for x in queue if isinstance(x, dict) and str(x.get("status", "pending")) in {"pending", "queued", "ready"}) if isinstance(queue, list) else 0

        if syntax_errors:
            decision, reason = "quality.syntax_repair", "Python syntax errors were detected"
        elif repair_ready or recent_repair:
            decision, reason = "quality.repair_and_retest", "an autonomous repair mission is waiting"
        elif django and not html:
            decision, reason = "site.django_templates", "Django is detected but no HTML templates were discovered"
        elif django:
            decision, reason = "site.django_integration", "Django is present; continue safe integration work"
        elif pending_missions:
            decision, reason = "mission.queue_progress", "the persistent mission queue contains ready work"
        elif not agents:
            decision, reason = "agent.ecosystem_bootstrap", "no subordinate-agent registry exists yet"
        elif not discovery:
            decision, reason = "site.foundation", "no discovery snapshot exists yet"
        else:
            decision, reason = "quality.tests", "continue trusted quality checks"

        result = {
            "decision_engine": True,
            "decision": decision,
            "reason": reason,
            "signals": {
                "django_detected": django,
                "python_files": len(py),
                "html_files": len(html),
                "syntax_errors": len(syntax_errors),
                "recent_repair_signal": recent_repair,
                "repair_mission_ready": repair_ready,
                "pending_missions": pending_missions,
                "agent_count": len(agents) if isinstance(agents, list) else 0,
                "tests_snapshot_present": bool(tests),
            },
            "owner_approval_required": True,
            "real_changes_allowed": False,
            "sandbox_only": True,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.path)
        self._cache = dict(result)
        self._cache_key = evidence_key
        self._cache_at = now
        return result
