import json
import os
from datetime import datetime


class AccessManager:
    def __init__(self):
        self.project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )

        self.data_dir = os.path.join(self.project_root, "data")
        self.access_file = os.path.join(
            self.data_dir, "access_control.json"
        )

        os.makedirs(self.data_dir, exist_ok=True)

        if not os.path.exists(self.access_file):
            self._save({
                "permissions": {},
                "owner_approval_required": True
            })

    def _load(self):
        try:
            with open(self.access_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "permissions": {},
                "owner_approval_required": True
            }

    def _save(self, data):
        with open(self.access_file, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=2
            )

    def request_access(self, resource, level="read"):
        data = self._load()

        data["permissions"][resource] = {
            "level": level,
            "status": "waiting_approval",
            "approved": False,
            "requested_at": datetime.now().isoformat()
        }

        self._save(data)

        return data["permissions"][resource]

    def approve_access(self, resource):
        data = self._load()

        if resource not in data["permissions"]:
            return False

        data["permissions"][resource]["approved"] = True
        data["permissions"][resource]["status"] = "approved"
        data["permissions"][resource]["approved_at"] = (
            datetime.now().isoformat()
        )

        self._save(data)

        return True

    def revoke_access(self, resource):
        data = self._load()

        if resource not in data["permissions"]:
            return False

        data["permissions"][resource]["approved"] = False
        data["permissions"][resource]["status"] = "revoked"

        self._save(data)

        return True

    def is_allowed(self, resource):
        data = self._load()

        permission = data["permissions"].get(resource)

        if not permission:
            return False

        return (
            permission.get("approved", False)
            and permission.get("status") == "approved"
        )

    def get_all(self):
        return self._load()

    def status(self):
        data = self._load()

        return {
            "access_manager": True,
            "resources": len(data["permissions"]),
            "owner_approval_required": True
        }


if __name__ == "__main__":
    manager = AccessManager()

    request = manager.request_access(
        "web_research",
        "read"
    )

    print("🔐 Access Manager فعال شد.")
    print("\n📋 درخواست دسترسی:")
    print(request)

    print("\n📊 قبل از تأیید:")
    print("Allowed:", manager.is_allowed("web_research"))

    manager.approve_access("web_research")

    print("\n👑 بعد از تأیید مالک:")
    print("Allowed:", manager.is_allowed("web_research"))

    print("\n📊 وضعیت:")
    print(manager.status())
