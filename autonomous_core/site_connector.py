from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from typing import Any, Dict


class SiteConnector:
    """Read-only HTTP discovery for the public company site.

    This connector never logs in, submits forms, uploads files, writes to the
    remote site, deploys code, or executes downloaded content.
    """

    def __init__(self, root: str | Path, url: str = "https://zomorodmelal.ir/", timeout: int = 15) -> None:
        self.root = Path(root).resolve()
        self.url = url
        self.timeout = max(3, int(timeout))
        self.path = self.root / "data" / "site_discovery.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _title(body: str) -> str | None:
        match = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
        if not match:
            return None
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", match.group(1))).strip() or None

    def discover(self) -> Dict[str, Any]:
        request = Request(self.url, headers={"User-Agent": "ZomorodMelal-MasterAgent/1.0"}, method="GET")
        result: Dict[str, Any] = {
            "url": self.url,
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "reachable": False,
            "status_code": None,
            "content_type": None,
            "server": None,
            "title": None,
            "django_signals": [],
            "error": None,
            "remote_write_performed": False,
            "owner_approval_required_for_changes": True,
        }
        try:
            with urlopen(request, timeout=self.timeout) as response:
                raw = response.read(512 * 1024)
                body = raw.decode("utf-8", errors="replace")
                headers = response.headers
                result.update({
                    "reachable": True,
                    "status_code": getattr(response, "status", None),
                    "content_type": headers.get("Content-Type"),
                    "server": headers.get("Server"),
                    "title": self._title(body),
                })
                signals = []
                cookies = headers.get("Set-Cookie", "")
                if "csrftoken" in cookies.lower():
                    signals.append("csrftoken_cookie")
                if "django" in body.lower() or "django" in str(headers).lower():
                    signals.append("django_marker")
                if "csrfmiddlewaretoken" in body.lower():
                    signals.append("django_csrf_form")
                result["django_signals"] = signals
        except HTTPError as exc:
            result.update({"status_code": exc.code, "error": f"HTTPError: {exc.code}"})
        except (URLError, TimeoutError, OSError) as exc:
            result["error"] = f"{type(exc).__name__}: {exc}"

        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.path)
        return result
