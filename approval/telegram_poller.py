from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional

from approval.telegram_approval import TelegramApproval


class TelegramApprovalPoller:
    """Long-poll Telegram for owner callbacks and persist the update offset."""

    def __init__(self, root: Optional[str] = None, poll_seconds: int = 25) -> None:
        self.root = Path(root or Path(__file__).resolve().parents[1]).resolve()
        self.telegram = TelegramApproval(self.root)
        self.offset_path = self.root / "data" / "telegram_update_offset.json"
        self.offset_path.parent.mkdir(parents=True, exist_ok=True)
        self.poll_seconds = max(1, min(int(poll_seconds), 50))

    def _offset(self) -> int:
        try:
            data = json.loads(self.offset_path.read_text(encoding="utf-8"))
            return int(data.get("offset", 0))
        except (OSError, ValueError, TypeError):
            return 0

    def _save_offset(self, offset: int) -> None:
        tmp = self.offset_path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"offset": int(offset)}, indent=2), encoding="utf-8")
        tmp.replace(self.offset_path)

    def poll_once(self) -> Dict[str, Any]:
        if not self.telegram.enabled:
            return {"status": "disabled", "processed": 0}
        result = self.telegram._call("getUpdates", {
            "offset": self._offset(),
            "timeout": self.poll_seconds,
            "allowed_updates": json.dumps(["callback_query"]),
        })
        if not result.get("ok"):
            return {"status": "telegram_error", "processed": 0, "response": result}
        processed = 0
        last_update = None
        for update in result.get("result", []) or []:
            last_update = int(update.get("update_id", 0))
            callback = update.get("callback_query")
            if not callback:
                continue
            outcome = self.telegram.handle_callback(callback)
            self.telegram.answer_callback(callback.get("id"), outcome.get("status", "processed"))
            processed += 1
        if last_update is not None:
            self._save_offset(last_update + 1)
        return {"status": "ok", "processed": processed, "next_offset": self._offset()}

    def run_forever(self) -> None:
        if not self.telegram.enabled:
            raise RuntimeError("Telegram approval credentials are not configured")
        while True:
            try:
                self.poll_once()
            except Exception:
                time.sleep(2)


if __name__ == "__main__":
    TelegramApprovalPoller().run_forever()
