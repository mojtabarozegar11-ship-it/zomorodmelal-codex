from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Dict, Iterable


class SelfAuditEngine:
    """Audit capability availability from the repository instead of static flags."""

    DEFAULT_CAPABILITIES = {
        "core": ("autonomous_core",),
        "memory": ("memory", "autonomous_core"),
        "agents": ("agents", "app/agents", "worker_mojtaba/agents"),
        "tasks": ("tasks",),
        "security": ("security", "app/security", "worker_mojtaba/security"),
        "planner": ("planner",),
        "research": ("research",),
        "knowledge": ("knowledge", "website/encyclopedia"),
        "evaluation": ("testing", "tests"),
        "real_web_research": ("web_research", "research"),
        "tool_manager": ("tools",),
        "agent_factory": ("agent_factory", "factory", "autonomous_core/agent_factory.py"),
        "sandbox": ("sandbox",),
        "testing": ("testing", "tests"),
        "evolution": ("evolution", "self_improvement"),
        "version_control": ("versioning",),
    }

    def __init__(self, root: str | Path | None = None, capabilities: Dict[str, bool] | None = None):
        self.root = Path(root or Path(__file__).resolve().parents[1]).resolve()
        self.capabilities = dict(capabilities or {})

    def _path_exists(self, candidate: str) -> bool:
        return (self.root / candidate).exists()

    def _module_available(self, module_name: str) -> bool:
        try:
            return importlib.util.find_spec(module_name) is not None
        except (ImportError, ModuleNotFoundError, ValueError):
            return False

    def _detect(self, candidates: Iterable[str]) -> bool:
        for candidate in candidates:
            candidate = str(candidate)
            if "/" in candidate or candidate.endswith(".py"):
                if self._path_exists(candidate):
                    return True
            elif self._path_exists(candidate) or self._module_available(candidate):
                return True
        return False

    def audit(self):
        detected = {}
        for name, candidates in self.DEFAULT_CAPABILITIES.items():
            detected[name] = self.capabilities.get(name, self._detect(candidates))

        available = sorted(name for name, enabled in detected.items() if enabled)
        missing = sorted(name for name, enabled in detected.items() if not enabled)

        return {
            "available": available,
            "missing": missing,
            "capabilities": detected,
            "total": len(detected),
            "available_count": len(available),
            "missing_count": len(missing),
            "root": str(self.root),
            "detection": "repository",
        }


if __name__ == "__main__":
    auditor = SelfAuditEngine()
    report = auditor.audit()

    print("🔍 Self-Audit Engine فعال شد.")
    print("📊 کل قابلیت‌ها:", report["total"])
    print("✅ قابلیت‌های موجود:", report["available_count"])
    print("❌ قابلیت‌های ناقص:", report["missing_count"])

    print("\n🚧 مواردی که باید ساخته شوند:")
    for item in report["missing"]:
        print("•", item)
