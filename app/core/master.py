class MasterAgent:
    def __init__(self):
        self.name = "Zomorod Melal Master Agent"

    def run(self, goal):
        return {
            "status": "received",
            "goal": goal,
            "message": "Task submitted to Master Agent"
        }
