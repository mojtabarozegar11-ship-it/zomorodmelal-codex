class Planner:
    def create_plan(self, goal):
        return {
            "goal": goal,
            "steps": ["analyze", "execute", "report"],
            "status": "planned"
        }
