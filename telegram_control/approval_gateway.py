class ApprovalGateway:
    """Owner approval gate for sensitive Master Agent actions."""

    def __init__(self):
        self.pending = {}

    def request(self, action_id, action):
        self.pending[action_id] = action
        return {
            "status": "waiting_for_owner_approval",
            "action_id": action_id,
            "action": action,
        }

    def approve(self, action_id):
        if action_id in self.pending:
            return {"status": "approved", "action": self.pending.pop(action_id)}
        return {"status": "not_found"}

    def reject(self, action_id):
        self.pending.pop(action_id, None)
        return {"status": "rejected", "action_id": action_id}
