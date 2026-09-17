class CycleAdapter:
    def __init__(self, runtime, cycle):
        self.runtime = runtime
        self.cycle = cycle

    def execute(self, goal):
        return self.runtime.run(goal)
