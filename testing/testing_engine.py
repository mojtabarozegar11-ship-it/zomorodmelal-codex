from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


class TestingEngine:
    """Persistent test history with a small in-process read cache."""

    def __init__(self, file_path="data/test_results.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")
        self._results_cache: Optional[List[Dict[str, Any]]] = None
        self._results_mtime_ns: Optional[int] = None

    def _read_results(self) -> List[Dict[str, Any]]:
        try:
            mtime_ns = self.file_path.stat().st_mtime_ns
        except OSError:
            mtime_ns = None
        if self._results_cache is not None and mtime_ns == self._results_mtime_ns:
            return list(self._results_cache)
        try:
            value = json.loads(self.file_path.read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError):
            value = []
        results = value if isinstance(value, list) else []
        self._results_cache = list(results)
        self._results_mtime_ns = mtime_ns
        return list(results)

    def record_test(self, name, passed, details="", diagnostics=None):
        results = self._read_results()
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
        try:
            self._results_mtime_ns = self.file_path.stat().st_mtime_ns
        except OSError:
            self._results_mtime_ns = None
        self._results_cache = list(results)
        return result

    def get_results(self):
        return self._read_results()

    def latest_failure(self):
        for result in reversed(self._read_results()):
            if not result.get("passed"):
                return result
        return None
