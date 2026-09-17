"""Security rules for Django <-> Master Agent bridge."""


class ConnectorSecurity:
    def __init__(self, require_owner_approval=True):
        self.require_owner_approval = require_owner_approval

    def can_execute(self, approved=False):
        if self.require_owner_approval:
            return approved
        return True
