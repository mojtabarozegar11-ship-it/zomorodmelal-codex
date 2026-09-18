from autonomous_core.autonomous_cycle_adapter import AutonomousCycleAdapter

class FakeCycle:
    def run(self, goal=None):
        return {"goal": goal, "ok": True}

def test_adapter_delegates_to_existing_cycle():
    result = AutonomousCycleAdapter(FakeCycle()).run("test goal")
    assert result == {"goal": "test goal", "ok": True}
