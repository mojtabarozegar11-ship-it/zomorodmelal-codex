class MasterCoreConnector:
    """Connect runtime components to Master Core safely."""

    def __init__(self, runtime, cycle):
        self.runtime = runtime
        self.cycle = cycle

    def health(self):
        return {
            "runtime": True,
            "cycle": self.cycle is not None,
        }

    def dispatch(self, goal):
        return self.cycle.run(goal)
