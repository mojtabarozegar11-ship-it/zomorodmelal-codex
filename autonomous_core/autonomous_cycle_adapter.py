"""Small adapter to expose the existing AutonomousCycle through a stable interface."""
from autonomous_core.autonomous_cycle import AutonomousCycle

class AutonomousCycleAdapter:
    def __init__(self, cycle=None):
        self.cycle = cycle or AutonomousCycle()

    def run(self, goal=None):
        return self.cycle.run(goal)
