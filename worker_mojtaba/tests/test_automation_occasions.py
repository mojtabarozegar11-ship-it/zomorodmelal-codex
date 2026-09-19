from worker_mojtaba.tools.automation_adapter import AutomationToolAdapter


def test_occasion_catalog_is_exposed_by_automation_tool():
    tool = AutomationToolAdapter()
    result = tool.execute("list_occasions", {})
    assert result["status"] == "completed"
    keys = {item["key"] for item in result["occasions"]}
    assert "nowruz" in keys
    assert "eid_al_ghadir" in keys
    assert "world_environment_day" in keys


def test_occasion_category_filter():
    tool = AutomationToolAdapter()
    result = tool.execute("list_occasions", {"category": "religious"})
    assert result["occasions"]
    assert all(item["category"] == "religious" for item in result["occasions"])
