from core.runner import Runner


class DemoMasterAgent:
    def run(self, goal):
        return {
            "goal": goal,
            "status": "completed"
        }


def start():
    master_agent = DemoMasterAgent()
    runner = Runner(master_agent)
    return runner.start("system health check")


if __name__ == "__main__":
    print(start())
