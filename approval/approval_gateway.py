import os
import json
from datetime import datetime


class ApprovalGateway:
    """Persistent approval boundary; supports isolated project roots for tests."""
    def __init__(self, root=None):
        self.root = os.path.abspath(root or os.path.join(os.path.dirname(__file__), ".."))
        self.data_dir = os.path.join(self.root, "data")
        self.file = os.path.join(self.data_dir, "approval_requests.json")
        os.makedirs(self.data_dir, exist_ok=True)
        if not os.path.exists(self.file): self._save([])

    def _load(self):
        try:
            with open(self.file, "r", encoding="utf-8") as f: return json.load(f)
        except Exception: return []

    def _save(self, requests):
        tmp = self.file + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f: json.dump(requests, f, ensure_ascii=False, indent=2)
        os.replace(tmp, self.file)

    def request(self, action, reason, metadata=None):
        requests = self._load()
        next_id = max((int(r.get("id", 0)) for r in requests), default=0) + 1
        request = {"id": next_id, "action": action, "reason": reason, "metadata": metadata or {},
                   "status": "waiting_approval", "approved": False,
                   "created_at": datetime.now().isoformat(), "approved_at": None}
        requests.append(request); self._save(requests); return request

    def get(self, request_id):
        for request in self._load():
            if request.get("id") == request_id: return request
        return None

    def approve(self, request_id):
        requests = self._load()
        for request in requests:
            if request.get("id") != request_id: continue
            if request.get("status") != "waiting_approval": return request
            request["status"] = "approved"; request["approved"] = True
            request["approved_at"] = datetime.now().isoformat(); self._save(requests); return request
        return None

    def reject(self, request_id):
        requests = self._load()
        for request in requests:
            if request.get("id") != request_id: continue
            if request.get("status") != "waiting_approval": return request
            request["status"] = "rejected"; request["approved"] = False
            self._save(requests); return request
        return None

    def is_approved(self, request_id):
        request = self.get(request_id)
        return bool(request and request.get("status") == "approved" and request.get("approved") is True)

    def get_all(self): return self._load()
    def get_waiting(self): return [r for r in self._load() if r.get("status") == "waiting_approval"]

    def status(self):
        requests = self._load()
        return {"approval_gateway": True, "total_requests": len(requests),
                "waiting": sum(r.get("status") == "waiting_approval" for r in requests),
                "approved": sum(r.get("status") == "approved" for r in requests),
                "rejected": sum(r.get("status") == "rejected" for r in requests),
                "owner_approval_required": True}
