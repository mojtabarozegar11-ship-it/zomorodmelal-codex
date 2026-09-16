from __future__ import annotations

import json
import py_compile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


class SelfEvolutionController:
    """Controls safe generations of the agent system in local sandbox state."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()
        self.path = self.root / "data" / "evolution_state.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _read(self) -> Dict[str, Any]:
        try:
            value = json.loads(self.path.read_text(encoding="utf-8"))
            return value if isinstance(value, dict) else {}
        except (OSError, ValueError, TypeError):
            return {}

    def _write(self, value: Dict[str, Any]) -> None:
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.path)

    def evaluate(self, test_result: Dict[str, Any] | None, agent_count: int) -> Dict[str, Any]:
        state = self._read()
        generation = int(state.get("generation", 1))
        passed = bool((test_result or {}).get("passed"))
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tests_passed": passed,
            "agent_count": agent_count,
            "generation": generation,
        }
        history = state.get("history", []) if isinstance(state.get("history"), list) else []
        history.append(event)
        history = history[-50:]
        # A generation advances only after a successful trusted test cycle.
        if passed and agent_count > 0:
            generation += 1
        result = {
            "generation": generation,
            "previous_generation": int(state.get("generation", 1)),
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

    def validate_python(self, files: list[str]) -> Dict[str, Any]:
        errors = []
        for file_name in files:
            path = Path(file_name)
            try:
                py_compile.compile(str(path), doraise=True)
            except (OSError, py_compile.PyCompileError) as exc:
                errors.append({"file": str(path), "error": str(exc)})
        return {"passed": not errors, "errors": errors}
