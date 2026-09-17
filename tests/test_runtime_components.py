from autonomous_core.task_queue import TaskQueue
from autonomous_core.state_memory import StateMemory
from autonomous_core.runtime_health import RuntimeHealth


def test_runtime_components():
    queue = TaskQueue()
    queue.add("test")
    assert queue.next() == "test"

    memory = StateMemory()
    memory.set("mode", "test")
    assert memory.get("mode") == "test"

    assert RuntimeHealth().check()["runtime"] == "ready"
