from .base import BaseAgent

class FinanceAgent(BaseAgent):
    name = "Finance Agent"
    version = "1.0"

    def match(self, goal):
        return any(x in goal for x in ["مالی", "حسابداری", "finance"])

    def run(self, task):
        return {"agent": self.name, "status": "completed", "result": "finance task processed"}
