from .base import BaseAgent

class AgricultureAgent(BaseAgent):
    name = "Agriculture Agent"
    version = "1.0"

    def match(self, goal):
        return any(x in goal for x in ["کشاورزی", "زراعت", "agriculture"])

    def run(self, task):
        return {"agent": self.name, "status": "completed", "result": "agriculture task processed"}
