from worker_mojtaba.api.service import WorkerService


def test_personal_calendar_request_executes_through_engine():
    result = WorkerService().handle(
        "تقویم شمسی",
        context={
            "title": "جلسه شخصی",
            "calendar": "persian",
            "date": "1405-07-01",
            "time": "08:00",
            "recurrence": "RRULE:FREQ=WEEKLY",
        },
    )
    assert result["intent"] == "calendar"
    assert result["route"] == "automation"\n    assert result["intent"] == "calendar"
    assert result["execution"]["status"] == "scheduled"
    assert result["execution"]["event"]["calendar"] == "persian"


def test_calendar_events_can_be_listed():
    service = WorkerService()
    service.handle(
        "تقویم میلادی",
        context={"title": "کار", "calendar": "gregorian", "date": "2026-09-20"},
    )
    result = service.handle("فهرست رویدادهای تقویم")
    assert result["route"] == "automation"
    assert result["execution"]["status"] == "completed"
