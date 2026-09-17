from agents.base import BaseAgent


class GameAgent(BaseAgent):
    name = "Game Agent"

    def match(self, text):
        return "game" in text.lower() or "بازی" in text

    def run(self, data):
        return {
            "agent": self.name,
            "status": "completed",
            "result": "Game task processed"
        }
