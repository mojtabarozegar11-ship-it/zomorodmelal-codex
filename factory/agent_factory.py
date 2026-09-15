import json
import os
from datetime import datetime


class AgentFactory:
    def __init__(self):
        self.project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )

        self.data_dir = os.path.join(self.project_root, "data")
        self.registry_file = os.path.join(
            self.data_dir, "agent_factory.json"
        )

        os.makedirs(self.data_dir, exist_ok=True)

        if not os.path.exists(self.registry_file):
            self._save([])

    def _load(self):
        try:
            with open(self.registry_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save(self, agents):
        with open(self.registry_file, "w", encoding="utf-8") as f:
            json.dump(
                agents,
                f,
                ensure_ascii=False,
                indent=2
            )

    def design_agent(self, name, role, purpose):
        agents = self._load()

        agent = {
            "id": len(agents) + 1,
            "name": name,
            "role": role,
            "purpose": purpose,
            "status": "designed",
            "approval_required": True,
            "created_at": datetime.now().isoformat()
        }

        agents.append(agent)
        self._save(agents)

        return agent

    def get_agents(self):
        return self._load()

    def status(self):
        agents = self._load()

        return {
            "agent_factory": True,
            "agents_designed": len(agents),
            "agents": agents,
            "auto_creation": False,
            "owner_approval_required": True
        }


if __name__ == "__main__":
    factory = AgentFactory()

    factory.design_agent(
        "Economist Agent",
        "اقتصاددان",
        "تحلیل اقتصادی، بازار، هزینه، درآمد و فرصت‌های کسب‌وکار"
    )

    factory.design_agent(
        "Research Scientist Agent",
        "پژوهشگر",
        "تحقیق، یادگیری، ارزیابی منابع و تولید دانش"
    )

    factory.design_agent(
        "Office Automation Agent",
        "اتوماسیون اداری",
        "طراحی و تحلیل فرایندهای اداری و اتوماسیون سازمانی"
    )

    print("🏭 Agent Factory فعال شد.")
    print("\n📋 وضعیت:")
    print(factory.status())
