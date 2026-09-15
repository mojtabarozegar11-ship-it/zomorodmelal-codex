import json
from datetime import datetime
from pathlib import Path


class ResearchEngine:
    def __init__(self, knowledge_file="data/knowledge.json"):
        self.knowledge_file = Path(knowledge_file)
        self.knowledge_file.parent.mkdir(parents=True, exist_ok=True)

        if not self.knowledge_file.exists():
            self.knowledge_file.write_text(
                "[]",
                encoding="utf-8"
            )

    def research(self, topic):
        return {
            "topic": topic,
            "status": "research_required",
            "questions": [
                f"دانش فعلی درباره «{topic}» چیست؟",
                f"چه چیزهایی درباره «{topic}» ناشناخته است؟",
                f"چه منابع معتبری باید بررسی شوند؟",
                f"چگونه می‌توان این دانش را آزمایش کرد؟"
            ],
            "created_at": datetime.now().isoformat()
        }

    def learn(self, topic, knowledge, sources=None):
        if sources is None:
            sources = []

        data = json.loads(
            self.knowledge_file.read_text(encoding="utf-8")
        )

        record = {
            "topic": topic,
            "knowledge": knowledge,
            "sources": sources,
            "learned_at": datetime.now().isoformat()
        }

        data.append(record)

        self.knowledge_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        return record

    def get_knowledge(self):
        return json.loads(
            self.knowledge_file.read_text(encoding="utf-8")
        )


if __name__ == "__main__":
    engine = ResearchEngine()

    result = engine.research("اقتصاد")

    print("🔬 Research & Learning Engine فعال شد.")
    print("🎯 موضوع:", result["topic"])
    print("📚 وضعیت:", result["status"])
    print("❓ پرسش‌های تحقیق:")

    for question in result["questions"]:
        print("•", question)

    engine.learn(
        "اقتصاد",
        "نمونه دانش ثبت‌شده برای آزمایش موتور یادگیری.",
        ["test-source"]
    )

    print("🧠 دانش با موفقیت ذخیره شد.")
    print("📚 تعداد دانش‌های ذخیره‌شده:",
          len(engine.get_knowledge()))
