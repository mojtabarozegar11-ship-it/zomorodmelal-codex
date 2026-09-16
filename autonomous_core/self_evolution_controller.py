from __future__ import annotations

import json
import py_compile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class SelfEvolutionController:
    """Controls safe generations of the agent system in local sandbox state."""

    CACHE_SECONDS = 3.0

    def __init__(self, root: Union[str, Path]) -> None:
        self.root = Path(root).resolve()
        self.path = self.root / "data" / "evolution_state.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._cache: Optional[Dict[str, Any]] = None
        self._cache_mtime_ns: Optional[int] = None
        self._cache_size: Optional[int] = None
        self._cache_at = 0.0

    def _read(self, force: bool = False) -> Dict[str, Any]:
        try:
            stat = self.path.stat()
            now = time.monotonic()
            if (not force and self._cache is not None
                    and self._cache_mtime_ns == stat.st_mtime_ns
                    and self._cache_size == stat.st_size
                    and now - self._cache_at < self.CACHE_SECONDS):
                return self._cache
            value = json.loads(self.path.read_text(encoding="utf-8"))
            result = value if isinstance(value, dict) else {}
            self._cache = result
            self._cache_mtime_ns = stat.st_mtime_ns
            self._cache_size = stat.st_size
            self._cache_at = now
            return result
        except (OSError, ValueError, TypeError):
            return self._cache or {}

    def _write(self, value: Dict[str, Any]) -> None:
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.path)
        try:
            stat = self.path.stat()
            self._cache = value
            self._cache_mtime_ns = stat.st_mtime_ns
            self._cache_size = stat.st_size
            self._cache_at = time.monotonic()
        except OSError:
            self._cache = value
            self._cache_mtime_ns = None
            self._cache_size = None
            self._cache_at = time.monotonic()

    def evaluate(self, test_result: Optional[Dict[str, Any]], agent_count: int) -> Dict[str, Any]:
        state = self._read(force=True)
        previous = int(state.get("generation", 1))
        passed = bool((test_result or {}).get("passed"))
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tests_passed": passed,
            "agent_count": agent_count,
            "generation": previous,
        }
        history = state.get("history", []) if isinstance(state.get("history"), list) else []
        history = (history + [event])[-50:]
        generation = previous + 1 if passed and agent_count > 0 else previous
        result = {
            "generation": generation,
            "previous_generation": previous,
            "agent_count": agent_count,
            "tests_passed": passed,
            "status": "sandbox_evolved" if passed else "awaiting_repair",
            "owner_approval_required": True,
            "real_world_changes": False,
            "history": history,
            "timestamp": event["timestamp"],
        }
        self._write(result)
        return result

    def validate_python(self, files: List[str]) -> Dict[str, Any]:
        errors = []
        for file_name in files:
            path = Path(file_name)
            try:
                py_compile.compile(str(path), doraise=True)
            except (OSError, py_compile.PyCompileError) as exc:
                errors.append({"file": str(path), "error": str(exc)})
        return {"passed": not errors, "errors": errors}
