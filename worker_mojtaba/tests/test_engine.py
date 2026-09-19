from worker_mojtaba.core.engine import ExecutionEngine
from worker_mojtaba.core.memory import MemoryStore
from worker_mojtaba.tools.registry import ToolRegistry


def test_engine_detects_wallet_intent():
    engine = ExecutionEngine(MemoryStore(), ToolRegistry())
    result = engine.run("موجودی کیف پول را بررسی کن")
    assert result["intent"] == "wallet"
    assert result["route"] == "text_model"


def test_engine_detects_media_intent():
    engine = ExecutionEngine(MemoryStore(), ToolRegistry())
    result = engine.run("یک ویدئو بساز")
    assert result["intent"] == "media_generation"


def test_engine_executes_registered_safe_tool_for_general_request():
    engine = ExecutionEngine(MemoryStore(), ToolRegistry())
    from worker_mojtaba.api.service import WorkerService
    result = WorkerService().handle("سلام")
    assert result["execution"]["status"] == "completed"
    assert result["execution"]["tool"] == "echo"
