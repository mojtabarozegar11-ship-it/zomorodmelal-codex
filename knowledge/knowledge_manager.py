import json
from pathlib import Path


class KnowledgeManager:
    def __init__(self, file_path="data/knowledge_base.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def add(self, topic, knowledge, source=None, confidence=0.5):
        data = json.loads(
            self.file_path.read_text(encoding="utf-8")
        )

        item = {
            "id": len(data) + 1,
            "topic": topic,
            "knowledge": knowledge,
            "source": source,
            "confidence": confidence
        }

        data.append(item)

        self.file_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        return item

    def search(self, keyword):
        data = json.loads(
            self.file_path.read_text(encoding="utf-8")
        )

        keyword = keyword.lower()

        return [
            item for item in data
            if keyword in item["topic"].lower()
            or keyword in item["knowledge"].lower()
        ]

    def get_all(self):
        return json.loads(
            self.file_path.read_text(encoding="utf-8")
        )


if __name__ == "__main__":
    km = KnowledgeManager()

    km.add(
        "اقتصاد",
        "نمونه دانش برای آزمایش Knowledge Manager.",
        source="test",
        confidence=0.9
    )

    print("🧠 Knowledge Manager فعال شد.")
    print("📚 تعداد دانش‌ها:", len(km.get_all()))

    results = km.search("اقتصاد")

    print("🔎 نتایج جست‌وجو:", len(results))

    for item in results:
        print(
            f"• [{item['id']}] "
            f"{item['topic']} | "
            f"اعتماد: {item['confidence']}"
        )
