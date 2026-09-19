import logging
import time
import uuid


class _DefaultPlanner:
    def create_plan(self, goal):
        return {"actions": [goal]}


class _DefaultExecutor:
    def execute(self, action):
        return {"status": "approval_required", "action": action}


class _DefaultApprovalGateway:
    def request(self, action, reason):
        return {
            "id": str(uuid.uuid4()),
            "action": action,
            "reason": reason,
            "approved": False,
        }


class SafeAgentLoop:
    """Safe autonomous loop: plan, request owner approval, never execute unapproved actions."""

    def __init__(self, planner=None, executor=None, approval_gateway=None):
        self.planner = planner or _DefaultPlanner()
        self.executor = executor or _DefaultExecutor()
        self.approval_gateway = approval_gateway or _DefaultApprovalGateway()
        self.running = False
        self.logger = logging.getLogger(__name__)

    def create_plan(self, goal):
        return self.planner.create_plan(goal)

    def request_approval(self, action, reason):
        return self.approval_gateway.request(action=action, reason=reason)

    def execute_cycle(self, goal):
        return self.run_cycle(goal)

    def run_cycle(self, goal):
        plan = self.create_plan(goal)
        steps = list(plan.get("actions", []))
        result = {
            "goal": goal,
            "status": "approval_required" if steps else "ready",
            "steps": steps,
            "waiting_for_approval": [],
            "executed": [],
        }
        for step in steps:
            approval = self.request_approval("agent_execution", step)
            approved = bool(approval.get("approved"))
            item = {
                "step": step,
                "approval_id": approval.get("id"),
                "approved": approved,
            }
            result["waiting_for_approval"].append(item)
            if approved:
                execution = self.executor.execute(step)
                item["execution"] = execution
                result["executed"].append(execution)
        result["waiting"] = result["waiting_for_approval"]
        return result

    def heartbeat(self, interval=60):
        self.running = True
        while self.running:
            self.logger.info("Master Agent heartbeat")
            time.sleep(interval)

    def stop(self):
        self.running = False
