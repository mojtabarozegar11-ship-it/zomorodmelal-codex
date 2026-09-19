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
