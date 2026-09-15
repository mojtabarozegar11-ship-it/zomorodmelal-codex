from pathlib import Path
import json
from datetime import datetime


class SandboxManager:
    def __init__(self, sandbox_path="sandbox/workspace"):
        self.sandbox_path = Path(sandbox_path)
        self.sandbox_path.mkdir(parents=True, exist_ok=True)

        self.log_file = Path("data/sandbox_tests.json")

        if not self.log_file.exists():
            self.log_file.write_text("[]", encoding="utf-8")

    def create_test(self, name, description):
        tests = json.loads(
            self.log_file.read_text(encoding="utf-8")
        )

        test = {
            "id": len(tests) + 1,
            "name": name,
            "description": description,
            "status": "created",
            "created_at": datetime.now().isoformat()
        }

        tests.append(test)

        self.log_file.write_text(
            json.dumps(tests, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        return test

    def list_tests(self):
        return json.loads(
            self.log_file.read_text(encoding="utf-8")
        )


if __name__ == "__main__":
    sandbox = SandboxManager()

    test = sandbox.create_test(
        "Self Improvement Test",
        "آزمایش تغییرات جدید قبل از ورود به سیستم اصلی"
    )

    print("🧪 Sandbox Manager فعال شد.")
    print("📁 محیط آزمایشی:", sandbox.sandbox_path)
    print("🆔 Test ID:", test["id"])
    print("📌 وضعیت:", test["status"])
    print("🔐 سیستم اصلی هنوز محافظت شده است.")
