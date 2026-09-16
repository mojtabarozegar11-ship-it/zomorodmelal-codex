from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict
from urllib.request import Request, urlopen


class ReadOnlySiteDiscovery:
    """Inspect the public site without modifying it or executing site code."""

    def __init__(self, project_root: str | Path | None = None) -> None:
        self.project_root = Path(project_root or Path(__file__).resolve().parent.parent).resolve()
        self.config_path = self.project_root / "config" / "site_target.json"

    def target_url(self) -> str:
        data = json.loads(self.config_path.read_text(encoding="utf-8"))
        if data.get("real_changes_allowed") is not False:
            raise RuntimeError("site target must keep real_changes_allowed=false")
        return str(data["base_url"])

    def inspect(self, timeout: int = 15) -> Dict[str, Any]:
        url = self.target_url()
        request = Request(url, headers={"User-Agent": "ZomorodMelal-MasterAgent-Discovery/1.0"})
        with urlopen(request, timeout=timeout) as response:
            raw = response.read(200_000)
            html = raw.decode("utf-8", errors="replace")
            return {
                "url": url,
                "status": getattr(response, "status", None),
                "content_type": response.headers.get("Content-Type"),
                "server": response.headers.get("Server"),
                "title": self._title(html),
                "html_size": len(raw),
                "django_hint": bool(re.search(r"csrfmiddlewaretoken|__django|Django", html, re.I)),
                "read_only": True,
                "real_changes_allowed": False,
                "owner_approval_required": True,
            }

    @staticmethod
    def _title(html: str) -> str | None:
        match = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
        return re.sub(r"\s+", " ", match.group(1)).strip() if match else None
