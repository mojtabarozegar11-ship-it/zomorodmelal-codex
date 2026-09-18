"""Canonical orchestration path for the Zomorod Melal Master Agent."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ActionPolicy:
    requires_owner_approval: bool = True


class MasterOrchestrator:
    def __init__(self, policy=None, planner=None, runtime=None, registry=None, tools=None,
                 audit=None, approval=None):
        self.policy = policy or ActionPolicy()
        self.planner = planner or self._default_plan
        self.runtime = runtime
        self.registry = registry
        self.tools = tools
        self.audit = audit
        self.approval = approval
        self.audit_log = []

    @staticmethod
    def _default_plan(goal):
        return {'goal': goal, 'steps': ['analyze', 'execute', 'validate', 'report']}

    def plan(self, goal):
        if not isinstance(goal, str) or not goal.strip():
            raise ValueError('goal must be a non-empty string')
        return self.planner(goal.strip())

    def _log(self, event, **data):
        item = {'event': event, **data}
        self.audit_log.append(item)
        if self.audit and hasattr(self.audit, 'log'):
            self.audit.log(event, data or None)

    def execute(self, goal, approved=False, action=None, validate=None):
        plan = self.plan(goal)
        self._log('PLAN', goal=plan['goal'])
        if self.policy.requires_owner_approval and not approved:
            approval_payload = self.approval.require_owner_approval(plan['goal']) if self.approval else None
            self._log('DENIED', reason='OWNER_APPROVAL_REQUIRED')
            return {'status': 'approval_required', 'plan': plan, 'approval': approval_payload}

        if action is not None:
            result = action(plan)
        elif self.runtime is not None and hasattr(self.runtime, 'execute'):
            result = self.runtime.execute(plan)
        elif self.tools is not None and hasattr(self.tools, 'execute'):
            result = self.tools.execute(plan)
        else:
            result = {'status': 'planned', 'plan': plan}

        valid = validate(result) if validate else True
        self._log('VALIDATED', valid=bool(valid))
        if not valid:
            self._log('FAILED_VALIDATION')
            return {'status': 'validation_failed', 'plan': plan, 'result': result}
        self._log('COMPLETED')
        return {'status': 'completed', 'plan': plan, 'result': result}

    def report(self):
        return {'events': list(self.audit_log), 'event_count': len(self.audit_log)}
