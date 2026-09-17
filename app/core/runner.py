from system.execution_logger import ExecutionLogger


class Runner:
    def __init__(self, master_agent, logger=None):
        self.master_agent = master_agent
        self.logger = logger or ExecutionLogger()

    def start(self, goal):
        self.logger.log("START", "Goal execution started")
        self.logger.log("MASTER", "Sending goal to master agent")

        result = self.master_agent.run(goal)

        self.logger.log("RESULT", "Goal execution completed")
        return {
            "result": result,
            "report": self.logger.report()
        }
