import json
from pathlib import Path
from datetime import datetime


class EvolutionEngine:
    def __init__(self, proposal_file="data/evolution_proposals.json"):
        self.proposal_file = Path(proposal_file)
        self.proposal_file.parent.mkdir(parents=True, exist_ok=True)

        if not self.proposal_file.exists():
            self.proposal_file.write_text("[]", encoding="utf-8")

    def analyze(self, missing_capabilities):
        proposals = json.loads(
            self.proposal_file.read_text(encoding="utf-8")
        )

        new_proposals = []

        for capability in missing_capabilities:
            proposal = {
                "id": len(proposals) + len(new_proposals) + 1,
                "capability": capability,
                "type": "self_improvement",
                "status": "proposal_only",
                "owner_approval_required": True,
                "created_at": datetime.now().isoformat()
            }

            new_proposals.append(proposal)

        proposals.extend(new_proposals)

        self.proposal_file.write_text(
            json.dumps(proposals, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        return new_proposals

    def get_proposals(self):
        return json.loads(
            self.proposal_file.read_text(encoding="utf-8")
        )


if __name__ == "__main__":
    engine = EvolutionEngine()

    missing = [
        "real_web_research",
        "agent_factory",
        "version_control"
    ]

    proposals = engine.analyze(missing)

    print("🧬 Evolution Engine فعال شد.")
    print("📋 پیشنهادهای ارتقا:", len(proposals))

    for proposal in proposals:
        print(
            f"• [{proposal['id']}] "
            f"{proposal['capability']} | "
            f"وضعیت: {proposal['status']} | "
            f"تأیید مالک: {proposal['owner_approval_required']}"
        )
