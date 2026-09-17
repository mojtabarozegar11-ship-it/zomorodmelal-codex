class PermissionGuard:
    """Enforces owner approval before critical actions."""

    def __init__(self, approval_gateway):
        self.approval_gateway = approval_gateway

    def can_execute(self, action):
        request = self.approval_gateway.request(
            action=action,
            reason="Critical action requires owner approval"
        )
        return request
