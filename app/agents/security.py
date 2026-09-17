from .base import BaseAgent

class SecurityAgent(BaseAgent):
    name = "Security Agent"
    version = "1.0"

    def match(self, goal):
        return any(x in goal.lower() for x in ["security", "امنیت", "سایبری"])

    def run(self, task):
        return {"agent": self.name, "status": "completed", "result": "security task processed"}
