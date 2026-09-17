from dataclasses import dataclass

@dataclass
class AgentRequestSerializer:
    goal: str

    def validate(self):
        return bool(self.goal and self.goal.strip())

@dataclass
class AgentResponseSerializer:
    status: str
    result: str
