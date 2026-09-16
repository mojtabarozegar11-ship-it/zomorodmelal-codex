"""Bridge between Telegram approval and Master Agent execution."""


class ExecutionBridge:
    def __init__(self, master_agent=None, notifier=None):
        self.master_agent = master_agent
        self.notifier = notifier

    def execute_approved_action(self, action):
        if self.master_agent is None:
            result = {
                "status": "queued",
                "message": "No runtime executor connected yet",
                "action": action,
            }
        else:
            result = self.master_agent.execute(action)

        if self.notifier:
            self.notifier.send_message(result)

        return result
