import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core import MasterCore
from planner.planner import Planner
from research.research_engine import ResearchEngine
from knowledge.knowledge_manager import KnowledgeManager
from evaluation.evaluation_engine import EvaluationEngine
from self_audit.self_audit_engine import SelfAuditEngine
from evolution.evolution_engine import EvolutionEngine
from factory.agent_factory import AgentFactory
from access.access_manager import AccessManager
from versioning.version_control import VersionControl


class MasterOrchestrator:

    def __init__(self):
        self.core = MasterCore()
        self.planner = Planner()
        self.research = ResearchEngine()
        self.knowledge = KnowledgeManager()
        self.evaluation = EvaluationEngine()
        self.audit = SelfAuditEngine()
        self.evolution = EvolutionEngine()
        self.factory = AgentFactory()
        self.access = AccessManager()
        self.versioning = VersionControl()

    def status(self):

        return {
            "master_core": self.core.status(),

            "knowledge_items": len(
                self.knowledge.get_all()
            ),

            "self_audit": self.audit.audit(),

            "agent_factory": self.factory.status(),

            "access": self.access.status(),

            "version_control": self.versioning.status(),

            "security": {
                "owner_approval_required": True,
                "automatic_execution": False
            }
        }

    def analyze_goal(self, goal):

        plan = self.planner.create_plan(goal)

        research_request = self.research.research(goal)

        return {
            "goal": goal,
            "plan": plan,
            "research": research_request,
            "approval_required": True,
            "execution": "blocked_until_owner_approval"
        }


if __name__ == "__main__":

    orchestrator = MasterOrchestrator()

    print("🧠 Master Orchestrator فعال شد.")
    print("🔐 قانون تأیید مالک: فعال")
    print("⛔ اجرای خودکار: غیرفعال")

    print("\n🎯 تحلیل هدف:")

    result = orchestrator.analyze_goal(
        "خودسازی و توسعه Master Agent"
    )

    print(result)

    print("\n📊 وضعیت کلی سیستم:")

    print(orchestrator.status())
