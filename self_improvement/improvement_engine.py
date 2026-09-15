import os
import json
from datetime import datetime


class ImprovementEngine:
    def __init__(self):
        self.project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )

        self.data_dir = os.path.join(
            self.project_root, "data"
        )

        self.file = os.path.join(
            self.data_dir, "improvement_proposals.json"
        )

        os.makedirs(self.data_dir, exist_ok=True)

        if not os.path.exists(self.file):
            self._save([])

    def _load(self):
        try:
            with open(
                self.file,
                "r",
                encoding="utf-8"
            ) as f:
                return json.load(f)

        except (
            FileNotFoundError,
            json.JSONDecodeError
        ):
            return []

    def _save(self, proposals):
        with open(
            self.file,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                proposals,
                f,
                ensure_ascii=False,
                indent=2
            )

    def analyze(self, audit_result):
        proposals = self._load()

        missing = audit_result.get(
            "missing",
            []
        )

        created = []

        for capability in missing:

            proposal = {
                "id": len(proposals) + 1,
                "capability": capability,
                "type": "self_improvement",
                "status": "proposal_only",
                "owner_approval_required": True,
                "created_at": datetime.now().isoformat()
            }

            proposals.append(proposal)
            created.append(proposal)

        self._save(proposals)

        return created

    def get_all(self):
        return self._load()

    def status(self):
        proposals = self._load()

        return {
            "improvement_engine": True,
            "proposals": len(proposals),
            "owner_approval_required": True,
            "automatic_changes": False
        }


if __name__ == "__main__":

    engine = ImprovementEngine()

    sample_audit = {
        "missing": [
            "advanced_web_research",
            "agent_generation",
            "automated_testing",
            "safe_code_evolution"
        ]
    }

    proposals = engine.analyze(
        sample_audit
    )

    print("🧬 Improvement Engine فعال شد.")

    print("\n📋 پیشنهادهای خودسازی:")

    for proposal in proposals:
        print(
            f"[{proposal['id']}] "
            f"{proposal['capability']} | "
            f"{proposal['status']} | "
            f"تأیید مالک: "
            f"{proposal['owner_approval_required']}"
        )

    print("\n📊 وضعیت:")
    print(engine.status())
