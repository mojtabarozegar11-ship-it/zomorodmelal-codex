import json
import os
import time
from datetime import datetime
from pathlib import Path


class ApprovalGateway:
    """Persistent approval boundary with a bounded read cache."""

    CACHE_SECONDS = 3.0

    def __init__(self, root=None):
        self.root = Path(root or Path(__file__).resolve().parents[1]).resolve()
        self.data_dir = self.root / "data"
        self.file = self.data_dir / "approval_requests.json"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._cache = None
        self._cache_mtime_ns = None
        self._cache_size = None
        self._cache_at = 0.0
        if not self.file.exists():
            self._save([])

    def _load(self, force=False):
        try:
            stat = self.file.stat()
            now = time.monotonic()
            if (not force and self._cache is not None
                    and self._cache_mtime_ns == stat.st_mtime_ns
                    and self._cache_size == stat.st_size
                    and now - self._cache_at < self.CACHE_SECONDS):
                return self._cache
            with self.file.open("r", encoding="utf-8") as f:
                data = json.load(f)
            value = data if isinstance(data, list) else []
            self._cache = value
            self._cache_mtime_ns = stat.st_mtime_ns
            self._cache_size = stat.st_size
            self._cache_at = now
            return value
        except Exception:
            return self._cache or []

    def _save(self, requests):
        tmp = self.file.with_name(self.file.name + ".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(requests, f, ensure_ascii=False, indent=2)
        os.replace(tmp, self.file)
        try:
            stat = self.file.stat()
            self._cache = requests
            self._cache_mtime_ns = stat.st_mtime_ns
            self._cache_size = stat.st_size
            self._cache_at = time.monotonic()
        except OSError:
            self._cache = requests
            self._cache_mtime_ns = None
            self._cache_size = None
            self._cache_at = time.monotonic()

    def request(self, action, reason, metadata=None):
        metadata = metadata or {}
        requests = list(self._load())
        for existing in requests:
            if existing.get("action") != action:
                continue
            if existing.get("status") not in {"waiting_approval", "approved"}:
                continue
            if (existing.get("metadata") or {}) == metadata:
                return existing
        next_id = max((int(r.get("id", 0)) for r in requests), default=0) + 1
        request = {
            "id": next_id, "action": action, "reason": reason, "metadata": metadata,
            "status": "waiting_approval", "approved": False,
            "created_at": datetime.now().isoformat(), "approved_at": None,
        }
        requests.append(request)
        self._save(requests)
        return request

    def get(self, request_id):
        for request in self._load():
            if request.get("id") == request_id:
                return request
        return None

    def approve(self, request_id):
        requests = list(self._load(force=True))
        for request in requests:
            if request.get("id") != request_id:
                continue
            if request.get("status") != "waiting_approval":
                return request
            request["status"] = "approved"
            request["approved"] = True
            request["approved_at"] = datetime.now().isoformat()
            self._save(requests)
            return request
        return None

    def reject(self, request_id):
        requests = list(self._load(force=True))
        for request in requests:
            if request.get("id") != request_id:
                continue
            if request.get("status") != "waiting_approval":
                return request
            request["status"] = "rejected"
            request["approved"] = False
            self._save(requests)
            return request
        return None

    def is_approved(self, request_id):
        request = self.get(request_id)
        return bool(request and request.get("status") == "approved" and request.get("approved") is True)

    def get_all(self):
        return list(self._load())

    def get_waiting(self):
        return [r for r in self._load() if r.get("status") == "waiting_approval"]

    def status(self):
        requests = self._load()
        return {
            "approval_gateway": True,
            "total_requests": len(requests),
            "waiting": sum(r.get("status") == "waiting_approval" for r in requests),
            "approved": sum(r.get("status") == "approved" for r in requests),
            "rejected": sum(r.get("status") == "rejected" for r in requests),
            "owner_approval_required": True,
        }
