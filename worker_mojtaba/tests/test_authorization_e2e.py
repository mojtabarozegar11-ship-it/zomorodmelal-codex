from worker_mojtaba.api.service import WorkerService


def test_unauthorized_capability_is_blocked_before_adapter_execution():
    service = WorkerService()
    service.policy.allowed = {"calendar_event"}
    result = service.handle("کیف پول")
    assert result["execution"]["result_state"] == "blocked"
    assert result["execution"]["reason"] == "capability_not_authorized_by_policy"
    assert result["authorization"]["allowed"] is False


def test_authorized_calendar_capability_reaches_adapter():
    service = WorkerService()
    service.policy.allowed = {"calendar_event"}
    result = service.handle(
        "تقویم شمسی",
        context={
            "title": "آزمون امنیت",
            "calendar": "persian",
            "date": "1405-07-01",
            "time": "08:00",
        },
    )
    assert result["authorization"]["allowed"] is True
    assert result["execution"]["status"] == "scheduled"
