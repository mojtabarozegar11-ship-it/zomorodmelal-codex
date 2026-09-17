class FinalExecution:
    def __init__(self, runner):
        self.runner = runner

    def run(self, goal):
        return self.runner.execute(goal)
