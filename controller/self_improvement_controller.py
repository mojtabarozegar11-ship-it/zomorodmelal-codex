import os
import sys
from datetime import datetime

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from self_audit.self_audit_engine import SelfAuditEngine
from self_improvement.improvement_engine import ImprovementEngine
from evolution.evolution_engine import EvolutionEngine
from versioning.version_control import VersionControl
from approval.approval_gateway import ApprovalGateway


class SelfImprovementController:

    def __init__(self):
        self.audit = SelfAuditEngine()
        self.improvement = ImprovementEngine()
        self.evolution = EvolutionEngine()
        self.versioning = VersionControl()
        self.approval = ApprovalGateway()

    def run_cycle(self):

        print("🧠 Self-Improvement Controller فعال شد.")
        print("🔐 تأیید مالک: فعال")
        print("⛔ تغییر خودکار: غیرفعال")

        # 1. Audit
        audit_result = self.audit.audit()

        print("\n🔍 ممیزی سیستم:")
        print(audit_result)

        # 2. Improvement proposals
        proposals = self.improvement.analyze(
            audit_result
        )

        print("\n🛠️ پیشنهادهای ارتقا:")

        for proposal in proposals:
            print(
                f"[{proposal['id']}] "
                f"{proposal['capability']} | "
                f"{proposal['status']}"
            )

        # 3. Evolution proposals
        evolution_proposals = (
            self.evolution.get_proposals()
        )

        print("\n🧬 پیشنهادهای تکامل:")
        print(evolution_proposals)

        # 4. Backup
        backup = self.versioning.create_backup()

        print("\n💾 Backup:")
        print(backup)

        # 5. Create approval request
        approval_request = self.approval.request(
            action="self_improvement_cycle",
            reason="اجرای تغییرات پیشنهادی پس از ممیزی سیستم"
        )

        print("\n👑 درخواست تأیید مالک:")
        print(approval_request)

        return {
            "cycle": "completed",
            "audit_completed": True,
            "improvement_proposals": len(proposals),
            "evolution_proposals": len(evolution_proposals),
            "backup_created": True,
            "approval_request_id": approval_request["id"],
            "owner_approval_required": True,
            "automatic_changes": False,
            "next_step": "owner_approval"
        }

    def status(self):

        return {
            "controller": True,
            "owner_approval_required": True,
            "automatic_changes": False,
            "timestamp": datetime.now().isoformat()
        }


if __name__ == "__main__":

    controller = SelfImprovementController()

    result = controller.run_cycle()

    print("\n✅ چرخه کنترل خودسازی کامل شد.")

    print("\n📊 نتیجه نهایی:")
    print(result)
