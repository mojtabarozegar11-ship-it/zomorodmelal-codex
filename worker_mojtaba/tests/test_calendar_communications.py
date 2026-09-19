from worker_mojtaba.calendar import CalendarEvent, CalendarManager
from worker_mojtaba.communications import Contact, MessagingManager

def test_three_calendars_are_supported():
    manager = CalendarManager()
    for name in ("gregorian", "persian", "hijri"):
        manager.add(CalendarEvent("test", name, "2026-01-01"))
    assert len(manager.list()) == 3

def test_recurring_tasks_are_unlimited_by_policy():
    event = CalendarEvent("repeat", "persian", "1405-01-01", recurrence="RRULE:FREQ=DAILY")
    assert event.recurrence.startswith("RRULE:")

def test_contact_has_phone_email_whatsapp():
    contact = Contact("Owner", "+98...", "owner@example.com", "+98...")
    assert contact.phone and contact.email and contact.whatsapp

def test_messaging_requires_real_provider_connection():
    result = MessagingManager().send("whatsapp", "+98...", "سلام")
    assert result["status"] == "provider_connection_required"
