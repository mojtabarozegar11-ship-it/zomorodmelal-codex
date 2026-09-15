import json
from pathlib import Path
from datetime import datetime


class TestingEngine:
    def __init__(self, file_path="data/test_results.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def record_test(self, name, passed, details=""):
        results = json.loads(
            self.file_path.read_text(encoding="utf-8")
        )

        result = {
            "id": len(results) + 1,
            "name": name,
            "passed": bool(passed),
            "details": details,
            "created_at": datetime.now().isoformat()
        }

        results.append(result)

        self.file_path.write_text(
            json.dumps(results, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        return result

    def get_results(self):
        return json.loads(
            self.file_path.read_text(encoding="utf-8")
        )


if __name__ == "__main__":
    tester = TestingEngine()

    result = tester.record_test(
        "Core Security Test",
        True,
        "Owner approval remains required."
    )

    print("🧪 Testing Engine فعال شد.")
    print("🆔 Test ID:", result["id"])
    print("✅ Passed:", result["passed"])
    print("📋 Details:", result["details"])
    print("📊 کل تست‌ها:", len(tester.get_results()))
