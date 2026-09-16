from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class TestingEngine:
    def __init__(self, file_path="data/test_results.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def record_test(self, name, passed, details="", diagnostics: dict[str, Any] | None = None):
        try:
            results = json.loads(self.file_path.read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError):
            results = []
        if not isinstance(results, list):
            results = []
        diagnostics = diagnostics or {}
        result = {
            "id": len(results) + 1,
            "name": name,
            "passed": bool(passed),
            "details": details,
            "diagnostics": {
                "returncode": diagnostics.get("returncode"),
                "stdout": str(diagnostics.get("stdout", ""))[-8000:],
                "stderr": str(diagnostics.get("stderr", ""))[-8000:],
                "failure_kind": diagnostics.get("failure_kind", "unknown"),
            },
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        results.append(result)
        tmp = self.file_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.file_path)
        return result

    def get_results(self):
        try:
            value = json.loads(self.file_path.read_text(encoding="utf-8"))
            return value if isinstance(value, list) else []
        except (OSError, ValueError, TypeError):
            return []

    def latest_failure(self):
        for result in reversed(self.get_results()):
            if not result.get("passed"):
                return result
        return None
