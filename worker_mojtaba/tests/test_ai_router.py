from worker_mojtaba.ai.router import AIRouter


def test_router_prefers_lower_priority_value():
    router = AIRouter()
    router.register("slow", ["text"], priority=50)
    router.register("fast", ["text"], priority=10)
    assert router.choose("text").name == "fast"


def test_disabled_provider_is_not_selected():
    router = AIRouter()
    router.register("provider", ["text"])
    router.set_enabled("provider", False)
    assert router.choose("text") is None
