from worker_mojtaba.tools.automation_adapter import AutomationToolAdapter


def test_schedule_recurring_action_for_occasion():
    tool = AutomationToolAdapter()
    result = tool.execute("schedule_for_occasion", {
        "occasion_key": "nowruz",
        "name": "Nowruz content",
        "expression": "annual",
        "calendar": "persian",
        "action": {"type": "publish_status", "text": "نوروز مبارک"},
    })
    assert result["status"] == "scheduled"
    assert result["occasion_key"] == "nowruz"
    assert result["run_count"] is None
    assert result["action"]["type"] == "publish_status"
