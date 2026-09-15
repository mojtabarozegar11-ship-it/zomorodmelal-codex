from __future__ import annotations

import ast
import hashlib
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping


DEFAULT_ALLOWED_EXTENSIONS = {
    ".py", ".json", ".md", ".txt", ".html", ".css", ".js"
}


@dataclass(frozen=True)
class BuildResult:
    path: str
    sha256: str
    size: int
    syntax_ok: bool


class SafeBuilder:
    """Build files only inside an isolated sandbox directory.

    This component never writes to the repository root and never executes
    generated code. It validates paths, file size, allowed extensions, and
    Python syntax before returning a deterministic change manifest.
    """

    def __init__(
        self,
        sandbox_root: str | Path,
        max_file_size: int = 512_000,
        allowed_extensions: Iterable[str] | None = None,
    ) -> None:
        self.sandbox_root = Path(sandbox_root).resolve()
        self.max_file_size = int(max_file_size)
        self.allowed_extensions = {
            ext.lower() if ext.startswith(".") else f".{ext.lower()}"
            for ext in (allowed_extensions or DEFAULT_ALLOWED_EXTENSIONS)
        }
        self.sandbox_root.mkdir(parents=True, exist_ok=True)

    def _safe_path(self, relative_path: str) -> Path:
        raw = Path(relative_path)
        if raw.is_absolute() or ".." in raw.parts:
            raise ValueError("path must be relative and cannot contain '..'")
        if not raw.name:
            raise ValueError("file path is required")
        if raw.suffix.lower() not in self.allowed_extensions:
            raise ValueError(f"extension not allowed: {raw.suffix or '<none>'}")

        target = (self.sandbox_root / raw).resolve()
        if target != self.sandbox_root and self.sandbox_root not in target.parents:
            raise ValueError("path escapes sandbox")
        return target

    def build(self, files: Mapping[str, str]) -> List[Dict[str, object]]:
        results: List[Dict[str, object]] = []
        for relative_path, content in files.items():
            if not isinstance(content, str):
                raise TypeError("file content must be text")
            target = self._safe_path(relative_path)
            encoded = content.encode("utf-8")
            if len(encoded) > self.max_file_size:
                raise ValueError(f"file too large: {relative_path}")

            syntax_ok = True
            if target.suffix.lower() == ".py":
                try:
                    ast.parse(content, filename=relative_path)
                except SyntaxError as exc:
                    raise ValueError(f"invalid Python syntax in {relative_path}: {exc}") from exc

            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(encoded)
            digest = hashlib.sha256(encoded).hexdigest()
            results.append(
                asdict(
                    BuildResult(
                        path=relative_path,
                        sha256=digest,
                        size=len(encoded),
                        syntax_ok=syntax_ok,
                    )
                )
            )
        return results
