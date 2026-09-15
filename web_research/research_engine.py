import json
import os
from datetime import datetime


class WebResearchEngine:
    def __init__(self):
        self.project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )

        self.data_dir = os.path.join(self.project_root, "data")
        self.research_file = os.path.join(
            self.data_dir, "web_research.json"
        )

        os.makedirs(self.data_dir, exist_ok=True)

        if not os.path.exists(self.research_file):
            self._save([])

    def _load(self):
        try:
            with open(self.research_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save(self, records):
        with open(self.research_file, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)

    def create_research_request(self, topic):
        records = self._load()

        request = {
            "id": len(records) + 1,
            "topic": topic,
            "status": "research_required",
            "sources_found": [],
            "approval_required": True,
            "created_at": datetime.now().isoformat()
        }

        records.append(request)
        self._save(records)

        return request

    def add_source(self, research_id, title, url, summary):
        records = self._load()

        for record in records:
            if record["id"] == research_id:
                record["sources_found"].append({
                    "title": title,
                    "url": url,
                    "summary": summary,
                    "added_at": datetime.now().isoformat()
                })

                record["status"] = "sources_collected"
                self._save(records)
                return record

        return None

    def get_all(self):
        return self._load()

    def status(self):
        records = self._load()

        return {
            "web_research_engine": True,
            "research_requests": len(records),
            "owner_approval_required": True,
            "autonomous_web_actions": False
        }


if __name__ == "__main__":
    engine = WebResearchEngine()

    request = engine.create_research_request(
        "هوش مصنوعی و اقتصاد"
    )

    print("🌐 Web Research Engine فعال شد.")
    print("\n📋 درخواست تحقیق:")
    print(request)

    print("\n📊 وضعیت:")
    print(engine.status())
