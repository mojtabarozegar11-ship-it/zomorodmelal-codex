from worker_mojtaba.automation.engine import AutomationEngine

def test_unlimited_schedule_and_calendar():
    task = AutomationEngine().schedule(
        "daily report", "0 8 * * *", calendar="persian", run_count=None,
        action={"type":"send_whatsapp", "recipient":"+98...", "message":"گزارش"}
    )
    assert task.calendar == "persian"
    assert task.run_count is None
    assert task.action["type"] == "send_whatsapp"

def test_limited_schedule_is_supported():
    task = AutomationEngine().schedule("once", "2026-09-20T08:00", run_count=3)
    assert task.run_count == 3
