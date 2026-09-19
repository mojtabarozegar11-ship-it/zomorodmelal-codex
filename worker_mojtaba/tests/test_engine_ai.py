from worker_mojtaba.ai.adapter import AIProviderAdapter
from worker_mojtaba.ai.registry import AIProviderRegistry
from worker_mojtaba.core.engine import ExecutionEngine
from worker_mojtaba.core.memory import MemoryStore
from worker_mojtaba.tools.registry import ToolRegistry


class FakeTextProvider(AIProviderAdapter):
    name = "fake-text"

    def generate(self, request: str, *, capability: str) -> dict:
        return {"status": "completed", "text": f"handled: {request}", "capability": capability}


def test_engine_calls_registered_ai_provider():
    registry = AIProviderRegistry()
    registry.register(FakeTextProvider(), ["text_model"], priority=1)
    engine = ExecutionEngine(MemoryStore(), ToolRegistry(), registry)

    result = engine.run("سلام")
    assert result["status"] == "completed"
    assert result["ai"]["text"] == "handled: سلام"
