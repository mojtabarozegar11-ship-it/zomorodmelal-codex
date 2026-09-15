import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from autonomous_core import MasterCore
from evolution.evolution_engine import EvolutionEngine
from versioning.version_control import VersionControl


class SelfImprovementLoop:

    def __init__(self):
        self.master = MasterCore()
        self.evolution = EvolutionEngine()
        self.versioning = VersionControl()

    def run_cycle(self):

        print("🔄 شروع چرخه یکپارچه Master Agent...")

        # هسته مرکزی خودش پروژه را بررسی می‌کند
        result = self.master.run_cycle()

        # پیشنهادهای Evolution موجود
        evolution_proposals = (
            self.evolution.get_proposals()
        )

        # وضعیت نسخه و امکان بازگشت
        version_status = (
            self.versioning.status()
        )

        result["evolution_proposals"] = len(
            evolution_proposals
        )

        result["backup_available"] = (
            version_status.get(
                "rollback_available",
                False
            )
        )

        # مرز امنیتی دائمی
        result["owner_approval_required"] = True
        result["real_changes_allowed"] = False
        result["automatic_changes"] = False
        result["next_step"] = "owner_approval"

        return result


if __name__ == "__main__":

    loop = SelfImprovementLoop()

    result = loop.run_cycle()

    print("\n✅ چرخه یکپارچه تکمیل شد.")

    print("\n📊 نتیجه:")
    print(result)
