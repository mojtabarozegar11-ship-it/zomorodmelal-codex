class PermissionManager:
    def __init__(self):
        self.owner_approval_required = True
        self.approved_actions = set()

    def request_approval(self, action_id):
        return {
            "action_id": action_id,
            "approved": False,
            "message": "Owner approval required before any action."
        }

    def approve(self, action_id):
        self.approved_actions.add(action_id)
        return True

    def is_approved(self, action_id):
        return action_id in self.approved_actions

    def revoke(self, action_id):
        self.approved_actions.discard(action_id)
        return True


if __name__ == "__main__":
    security = PermissionManager()

    request = security.request_approval("TEST-001")

    print("🔐 Permission Manager فعال شد.")
    print("🆔 Action:", request["action_id"])
    print("🔒 Approved:", request["approved"])
    print("⚠️", request["message"])

    security.approve("TEST-001")

    print("✅ بعد از تأیید مالک:", security.is_approved("TEST-001"))
