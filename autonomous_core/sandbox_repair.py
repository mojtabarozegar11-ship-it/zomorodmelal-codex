from __future__ import annotations

import hashlib
import json
import py_compile
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class SandboxRepairEngine:
    """Apply bounded repair plans only inside the isolated sandbox, then verify or rollback."""

    MAX_FILES = 20
    MAX_BYTES_PER_FILE = 512 * 1024
    MAX_TEST_SECONDS = 20

    def __init__(self, root: Union[str, Path]) -> None:
        self.root = Path(root).resolve()
        self.sandbox = (self.root / "sandbox").resolve()
        self.snapshots = (self.root / "data" / "sandbox_repair_snapshots").resolve()
        self.snapshots.mkdir(parents=True, exist_ok=True)
        self.sandbox.mkdir(parents=True, exist_ok=True)

    def _safe_path(self, relative: str) -> Path:
        path = (self.sandbox / str(relative)).resolve()
        if path != self.sandbox and self.sandbox not in path.parents:
            raise ValueError("repair path escapes sandbox")
        return path

    def _snapshot(self, paths: List[str]) -> str:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        directory = self.snapshots / stamp
        directory.mkdir(parents=True, exist_ok=False)
        manifest: List[Dict[str, Any]] = []
        for relative in paths:
            target = self._safe_path(relative)
            if target.exists() and target.is_file():
                data = target.read_bytes()
                backup = directory / relative
                backup.parent.mkdir(parents=True, exist_ok=True)
                backup.write_bytes(data)
                manifest.append({"path": relative, "exists": True, "sha256": hashlib.sha256(data).hexdigest()})
            else:
                manifest.append({"path": relative, "exists": False})
        (directory / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        return stamp

    def _rollback(self, snapshot_id: str, paths: List[str]) -> None:
        directory = self.snapshots / snapshot_id
        for relative in paths:
            target = self._safe_path(relative)
            backup = directory / relative
            if backup.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(backup.read_bytes())
            elif target.exists():
                target.unlink()

    def _validate_plan(self, changes: List[Dict[str, Any]]) -> None:
        if not changes or len(changes) > self.MAX_FILES:
            raise ValueError("repair plan must contain 1..20 files")
        for change in changes:
            relative = str(change.get("path", ""))
            if not relative or relative.startswith("/"):
                raise ValueError("repair paths must be relative")
            if not isinstance(change.get("content"), str):
                raise ValueError("repair content must be text")
            if len(change["content"].encode("utf-8")) > self.MAX_BYTES_PER_FILE:
                raise ValueError("repair file exceeds size limit")
            self._safe_path(relative)

    def _verify(self, paths: List[str], test_command: Optional[List[str]]) -> Dict[str, Any]:
        compile_errors: List[Dict[str, str]] = []
        for relative in paths:
            target = self._safe_path(relative)
            if target.suffix == ".py":
                try:
                    py_compile.compile(str(target), doraise=True)
                except py_compile.PyCompileError as exc:
                    compile_errors.append({"file": relative, "error": str(exc)})
        if compile_errors:
            return {"passed": False, "kind": "compile", "errors": compile_errors}
        if not test_command:
            return {"passed": True, "kind": "compile_only", "returncode": 0}
        if not isinstance(test_command, list) or not test_command:
            return {"passed": False, "kind": "invalid_test_command"}
        try:
            command = [str(item) for item in test_command]
            completed = subprocess.run(command, cwd=self.sandbox, capture_output=True, text=True,
                                       timeout=self.MAX_TEST_SECONDS, shell=False)
            return {"passed": completed.returncode == 0, "kind": "command", "returncode": completed.returncode,
                    "stdout": completed.stdout[-4000:], "stderr": completed.stderr[-4000:]}
        except subprocess.TimeoutExpired as exc:
            return {"passed": False, "kind": "timeout", "error": str(exc)}
        except OSError as exc:
            return {"passed": False, "kind": "execution_error", "error": str(exc)}

    def repair(self, changes: List[Dict[str, Any]], test_command: Optional[List[str]] = None) -> Dict[str, Any]:
        self._validate_plan(changes)
        paths = [str(change["path"]) for change in changes]
        snapshot_id = self._snapshot(paths)
        started = time.monotonic()
        try:
            for change in changes:
                target = self._safe_path(str(change["path"]))
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(str(change["content"]), encoding="utf-8")
            verification = self._verify(paths, test_command)
            if verification.get("passed"):
                status = "verified"
                rolled_back = False
            else:
                self._rollback(snapshot_id, paths)
                status = "rolled_back"
                rolled_back = True
            return {"status": status, "snapshot": snapshot_id, "files": paths,
                    "verification": verification, "rolled_back": rolled_back,
                    "elapsed_seconds": round(time.monotonic() - started, 3),
                    "sandbox_only": True, "real_world_changes": False,
                    "owner_approval_required": True}
        except Exception as exc:
            self._rollback(snapshot_id, paths)
            return {"status": "rolled_back", "snapshot": snapshot_id, "files": paths,
                    "verification": {"passed": False, "kind": "repair_error", "error": str(exc)},
                    "rolled_back": True, "elapsed_seconds": round(time.monotonic() - started, 3),
                    "sandbox_only": True, "real_world_changes": False,
                    "owner_approval_required": True}
