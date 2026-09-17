import logging
import time


class SafeAgentLoop:
    """
    Safe autonomous execution loop for Master Agent.

    Critical actions must pass through owner approval.
    """

    def __init__(self, planner, executor, approval_gateway):
        self.planner = planner
        self.executor = executor
        self.approval_gateway = approval_gateway
        self.running = False
        self.logger = logging.getLogger(__name__)

    def create_plan(self, goal):
        return self.planner.create_plan(goal)

    def request_approval(self, action, reason):
        return self.approval_gateway.request(
            action=action,
            reason=reason,
        )

    def run_cycle(self, goal):
        plan = self.create_plan(goal)

        result = {
            "goal": goal,
            "steps": plan.get("actions", []),
            "waiting_for_approval": [],
        }

        for step in result["steps"]:
            approval = self.request_approval(
                "agent_execution",
                step,
            )

            result["waiting_for_approval"].append({
                "step": step,
                "approval_id": approval.get("id"),
            })

        return result

    def heartbeat(self, interval=60):
        self.running = True
        while self.running:
            self.logger.info("Master Agent heartbeat")
            time.sleep(interval)

    def stop(self):
        self.running = False
