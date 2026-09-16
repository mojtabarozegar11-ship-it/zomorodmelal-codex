from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable


class AgentFactory:
    """Safely designs and materializes subordinate-agent definitions.

    The factory creates only local Python modules/manifests in the sandbox. It
    never executes generated code and never grants external access.
    """

    SAFE_ROLES = {
        "research": "Research and summarize evidence for assigned missions.",
        "engineering": "Design and implement isolated software changes.",
        "testing": "Run and interpret trusted project tests.",
        "security": "Review changes for safety and policy constraints.",
        "content": "Draft structured content and metadata.",
        "website": "Develop website features inside the sandbox.",
        "agriculture": "Analyze agricultural-domain tasks and data.",
        "business": "Analyze business and market tasks without external action.",
        "knowledge": "Organize reusable knowledge and research findings.",
        "general": "Perform bounded general-purpose planning and execution.",
    }

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()
        self.registry = self.root / "data" / "agent_registry.json"
        self.registry.parent.mkdir(parents=True, exist_ok=True)
        if not self.registry.exists():
            self._write([])

    def _read(self) -> list[dict[str, Any]]:
        try:
            value = json.loads(self.registry.read_text(encoding="utf-8"))
            return value if isinstance(value, list) else []
        except (OSError, ValueError, TypeError):
            return []

    def _write(self, value: list[dict[str, Any]]) -> None:
        tmp = self.registry.with_suffix(".tmp")
        tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.registry)

    @staticmethod
    def _slug(value: str) -> str:
        value = re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip().lower()).strip("_")
        return value[:64] or "general_agent"

    def ensure_agent(self, role: str, mission: str = "") -> Dict[str, Any]:
        role = self._slug(role)
        description = self.SAFE_ROLES.get(role, "Bounded specialist agent created for an identified capability gap.")
        agents = self._read()
        for agent in agents:
            if agent.get("role") == role:
                return agent
        agent_id = f"agent_{len(agents) + 1:04d}"
        agent = {
            "agent_id": agent_id,
            "name": f"{role}_agent",
            "role": role,
            "mission": mission,
            "description": description,
            "generation": 1,
            "status": "sandbox_ready",
            "permissions": {"sandbox_write": True, "real_world_write": False, "external_action": False},
            "owner_approval_required": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        agents.append(agent)
        self._write(agents)
        return agent

    def ensure_for_capabilities(self, capabilities: Iterable[str]) -> list[Dict[str, Any]]:
        created = []
        for capability in capabilities:
            text = str(capability).lower()
            role = "general"
            for candidate in self.SAFE_ROLES:
                if candidate in text:
                    role = candidate
                    break
            created.append(self.ensure_agent(role, str(capability)))
        return created

    def list_agents(self) -> list[dict[str, Any]]:
        return self._read()
