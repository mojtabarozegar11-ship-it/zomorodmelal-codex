class ExecutionPolicy:
    def __init__(self, owner_approval_required=True):
        self.owner_approval_required = owner_approval_required

    def can_execute(self, approved=False):
        if self.owner_approval_required:
            return approved
        return True
