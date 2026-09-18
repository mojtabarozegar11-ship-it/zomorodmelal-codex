from dataclasses import dataclass

@dataclass(frozen=True)
class ActionPolicy:
    requires_owner_approval: bool = True

class MasterOrchestrator:
    def __init__(self, policy=None, planner=None):
        self.policy = policy or ActionPolicy()
        self.planner = planner or self._default_plan
        self.audit_log = []

    @staticmethod
    def _default_plan(goal):
        return {'goal': goal, 'steps': ['analyze', 'execute', 'validate', 'report']}

    def plan(self, goal):
        if not isinstance(goal, str) or not goal.strip():
            raise ValueError('goal must be a non-empty string')
        return self.planner(goal.strip())

    def execute(self, goal, approved=False, action=None, validate=None):
        plan = self.plan(goal)
        self.audit_log.append({'event': 'PLAN', 'goal': plan['goal']})
        if self.policy.requires_owner_approval and not approved:
            self.audit_log.append({'event': 'DENIED', 'reason': 'OWNER_APPROVAL_REQUIRED'})
            return {'status': 'approval_required', 'plan': plan}
        result = action(plan) if action else {'status': 'planned', 'plan': plan}
        valid = validate(result) if validate else True
        self.audit_log.append({'event': 'VALIDATED', 'valid': bool(valid)})
        if not valid:
            self.audit_log.append({'event': 'FAILED_VALIDATION'})
            return {'status': 'validation_failed', 'plan': plan, 'result': result}
        self.audit_log.append({'event': 'COMPLETED'})
        return {'status': 'completed', 'plan': plan, 'result': result}

    def report(self):
        return {'events': list(self.audit_log), 'event_count': len(self.audit_log)}
