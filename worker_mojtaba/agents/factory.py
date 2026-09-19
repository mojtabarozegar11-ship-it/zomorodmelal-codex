"""Agent factory for creating specialist specifications."""
from dataclasses import dataclass

@dataclass
class AgentBlueprint:
    name: str
    purpose: str
    required_tools: list[str]

class AgentFactory:
    def design(self, purpose: str, required_tools: list[str]) -> AgentBlueprint:
        slug = purpose.strip().lower().replace(" ", "-") or "specialist"
        return AgentBlueprint(name=slug, purpose=purpose, required_tools=required_tools)
