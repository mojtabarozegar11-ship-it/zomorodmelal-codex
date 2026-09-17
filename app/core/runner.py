class Runner:
    def __init__(self, master_agent):
        self.master_agent = master_agent

    def start(self, goal):
        return self.master_agent.run(goal)
