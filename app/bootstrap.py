from agents.registry import AgentRegistry
from agents.knowledge import KnowledgeAgent
from agents.finance import FinanceAgent
from agents.agriculture import AgricultureAgent
from agents.security import SecurityAgent
from agents.game import GameAgent


def load_agents():
    registry = AgentRegistry()
    registry.register("knowledge", KnowledgeAgent())
    registry.register("finance", FinanceAgent())
    registry.register("agriculture", AgricultureAgent())
    registry.register("security", SecurityAgent())
    registry.register("game", GameAgent())
    return registry
