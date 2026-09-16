"""Bridge between Telegram approval and Master Agent execution."""

from core import MasterCore


class ExecutionBridge:
    def __init__(self, master_agent=None, notifier=None):
        self.master_agent = master_agent or MasterCore()
        self.notifier = notifier

    def execute_approved_action(self, action):
        result = self.master_agent.execute(action)

        if self.notifier:
            self.notifier.send_message(result)

        return result
