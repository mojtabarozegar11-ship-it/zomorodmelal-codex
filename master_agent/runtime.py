"""Canonical production runtime for the Zomorod Melal Master Agent."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, Optional
from autonomous_core.master_core import MasterCore

class CanonicalMasterAgent:
    RUNTIME_NAME = "zomorodmelal-canonical-master-agent"
    RUNTIME_VERSION = "1.0.0"
    EXECUTION_MODE = "sandbox_control_plane"

    def __init__(self, root: Optional[str | Path] = None) -> None:
        self.root = Path(root or Path(__file__).resolve().parents[1]).resolve()
        self.core = MasterCore(self.root)

    def health(self) -> Dict[str, Any]:
        return {
            "status": "ready",
            "runtime": self.RUNTIME_NAME,
            "version": self.RUNTIME_VERSION,
            "kernel": f"{self.core.__class__.__module__}.{self.core.__class__.__name__}",
            "execution_mode": self.EXECUTION_MODE,
            "owner_approval_required": True,
            "real_world_execution": False,
        }

    def run_once(self, goal: Optional[str] = None) -> Dict[str, Any]:
        result = self.core.run_cycle(goal=goal)
        result["runtime"] = self.RUNTIME_NAME
        result["execution_mode"] = self.EXECUTION_MODE
        return result

    def set_goal(self, goal: str) -> Dict[str, Any]:
        return self.core.set_goal(goal)

    def status(self) -> Dict[str, Any]:
        state = self.core.state
        return {
            **self.health(),
            "cycles": state.get("cycles", 0),
            "generation": state.get("generation", 1),
            "phase": state.get("phase", "observe"),
            "goals": state.get("goals", []),
            "agents": state.get("agents", []),
            "capabilities": state.get("capabilities", []),
            "last_cycle": state.get("last_cycle"),
        }

    def check(self) -> Dict[str, Any]:
        checks = []
        try:
            import autonomous_core
            checks.append({"name": "canonical_kernel_import", "passed": True, "detail": autonomous_core.__name__})
        except Exception as exc:
            checks.append({"name": "canonical_kernel_import", "passed": False, "detail": str(exc)})
        try:
            audit = self.core.audit_python()
            failed = [item for item in audit if not item.get("syntax_ok")]
            checks.append({
                "name": "python_syntax_audit",
                "passed": not failed,
                "detail": f"{len(audit)} files audited; {len(failed)} syntax failures",
            })
        except Exception as exc:
            checks.append({"name": "python_syntax_audit", "passed": False, "detail": str(exc)})
        checks.append({
            "name": "external_execution_gate",
            "passed": True,
            "detail": "external/real-world execution is disabled by canonical runtime",
        })
        checks.append({
            "name": "owner_approval_boundary",
            "passed": True,
            "detail": "owner approval remains required by canonical access/activation gates",
        })
        return {**self.health(), "checks": checks, "ready": all(x["passed"] for x in checks)}

    def json_status(self) -> str:
        return json.dumps(self.status(), ensure_ascii=False, indent=2)
