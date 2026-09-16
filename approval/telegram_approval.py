from __future__ import annotations

import hashlib
import hmac
import json
import os
from typing import Any, Dict
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from approval.approval_gateway import ApprovalGateway


class TelegramApproval:
    """Optional Telegram approval bridge; disabled until credentials are configured."""

    API_ROOT = "https://api.telegram.org/bot"

    def __init__(self, root=None, token=None, owner_chat_id=None, timeout=15):
        self.gateway = ApprovalGateway(root)
        self.token = token or os.environ.get("MASTER_AGENT_TELEGRAM_BOT_TOKEN", "")
        self.owner_chat_id = str(owner_chat_id or os.environ.get("MASTER_AGENT_TELEGRAM_OWNER_CHAT_ID", ""))
        self.timeout = max(1, min(int(timeout), 60))

    @property
    def enabled(self):
        return bool(self.token and self.owner_chat_id)

    def _call(self, method: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.enabled:
            return {"ok": False, "status": "disabled"}
        body = urlencode({key: str(value) for key, value in payload.items()}).encode("utf-8")
        request = Request(self.API_ROOT + self.token + "/" + method, data=body, method="POST")
        with urlopen(request, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))

    def _callback_token(self, request_id: int, action: str) -> str:
        secret = hashlib.sha256(self.token.encode("utf-8")).hexdigest() if self.token else "disabled"
        raw = "%s:%s:%s" % (request_id, action, secret)
        return hmac.new(secret.encode("utf-8"), raw.encode("utf-8"), hashlib.sha256).hexdigest()[:24]

    def build_callback(self, request_id: int, action: str) -> str:
        if action not in {"approve", "reject"}:
            raise ValueError("unsupported approval action")
        return "ma:%s:%s:%s" % (request_id, action, self._callback_token(request_id, action))

    def notify(self, request: Dict[str, Any]) -> Dict[str, Any]:
        if not self.enabled:
            return {"ok": False, "status": "disabled", "request_id": request.get("id")}
        request_id = int(request["id"])
        text = (
            "Master Agent approval request\n"
            "ID: %s\n"
            "Action: %s\n"
            "Reason: %s\n\n"
            "Approve or reject this request."
        ) % (request_id, request.get("action", ""), request.get("reason", ""))
        keyboard = json.dumps({"inline_keyboard": [[
            {"text": "Approve", "callback_data": self.build_callback(request_id, "approve")},
            {"text": "Reject", "callback_data": self.build_callback(request_id, "reject")},
        ]]})
        result = self._call("sendMessage", {"chat_id": self.owner_chat_id, "text": text, "reply_markup": keyboard})
        return {"ok": bool(result.get("ok")), "status": "sent" if result.get("ok") else "send_failed", "request_id": request_id}

    def handle_callback(self, callback: Dict[str, Any]) -> Dict[str, Any]:
        """Validate owner callback and apply exactly one pending decision."""
        if not self.enabled:
            return {"success": False, "status": "disabled"}
        message = callback.get("message") or {}
        chat = message.get("chat") or {}
        if str(chat.get("id")) != self.owner_chat_id:
            return {"success": False, "status": "unauthorized"}
        data = str(callback.get("data", ""))
        parts = data.split(":")
        if len(parts) != 4 or parts[0] != "ma" or parts[2] not in {"approve", "reject"}:
            return {"success": False, "status": "invalid_callback"}
        try:
            request_id = int(parts[1])
        except ValueError:
            return {"success": False, "status": "invalid_request_id"}
        if not hmac.compare_digest(parts[3], self._callback_token(request_id, parts[2])):
            return {"success": False, "status": "invalid_token", "request_id": request_id}
        request = self.gateway.approve(request_id) if parts[2] == "approve" else self.gateway.reject(request_id)
        if request is None:
            return {"success": False, "status": "request_not_found", "request_id": request_id}
        return {"success": True, "status": request.get("status"), "request_id": request_id}
