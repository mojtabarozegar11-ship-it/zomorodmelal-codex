from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


class AutonomousDecisionEngine:
    """Choose safe next work from local evidence only.

    This component never deploys, sends, purchases, or edits the real project.
    It only reads local discovery/history snapshots and records a recommendation.
    """

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()
        self.path = self.root / "data" / "autonomous_decisions.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _load_json(self, name: str, default: Any) -> Any:
        try:
            return json.loads((self.root / "data" / name).read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError):
            return default

    def assess(self) -> Dict[str, Any]:
        discovery = self._load_json("project_discovery.json", {})
        goal_state = self._load_json("autonomous_goal_engine.json", {})
        mission_state = self._load_json("autonomous_mission_queue.json", {})
        tests = self._load_json("test_results.json", {})

        files = discovery.get("files", []) if isinstance(discovery, dict) else []
        py = [x for x in files if str(x.get("path", "")).endswith(".py")]
        html = [x for x in files if str(x.get("path", "")).endswith(".html")]
        django = bool(discovery.get("django_detected"))
        syntax_errors = [x for x in py if x.get("syntax_ok") is False]

        history = goal_state.get("history", []) if isinstance(goal_state, dict) else []
        recent_repair = any(x.get("status") == "needs_repair" for x in history[-10:])

        queue = mission_state.get("missions", mission_state.get("queue", [])) if isinstance(mission_state, dict) else []
        pending_missions = sum(
            1 for x in queue
            if isinstance(x, dict) and str(x.get("status", "pending")) in {"pending", "queued", "ready"}
        ) if isinstance(queue, list) else 0

        if syntax_errors:
            decision, reason = "quality.syntax_repair", "Python syntax errors were detected by discovery"
        elif recent_repair:
            decision, reason = "quality.repair_and_retest", "recent autonomous work needs repair and retest"
        elif django and not html:
            decision, reason = "site.django_templates", "Django is detected but no HTML templates were discovered"
        elif django:
            decision, reason = "site.django_integration", "Django is present; continue safe integration work"
        elif pending_missions:
            decision, reason = "mission.queue_progress", "the persistent mission queue contains ready work"
        elif not discovery:
            decision, reason = "site.foundation", "no discovery snapshot exists yet"
        else:
            decision, reason = "quality.tests", "no higher-confidence repair or integration signal was found"

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
                "pending_missions": pending_missions,
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
        return result
