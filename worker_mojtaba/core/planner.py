"""Task planner."""
class Planner:
    def make_plan(self, request:str)->list[str]:
        if not request.strip(): return []
        return ["understand_request","select_capability","execute","verify","deliver"]
