"""Agent manager skeleton."""
from dataclasses import dataclass

@dataclass
class AgentSpec:
    name: str
    purpose: str
    enabled: bool = True

class AgentManager:
    def __init__(self) -> None:
        self.agents: dict[str, AgentSpec] = {}

    def register(self, name: str, purpose: str) -> AgentSpec:
        spec = AgentSpec(name=name, purpose=purpose)
        self.agents[name] = spec
        return spec

    def list(self) -> list[AgentSpec]:
        return list(self.agents.values())
