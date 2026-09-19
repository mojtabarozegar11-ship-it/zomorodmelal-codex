"""Unified calendar/event model for Gregorian, Persian and Hijri dates."""
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class CalendarEvent:
    title: str
    calendar: str
    date: str
    time: str = ""
    recurrence: str = ""
    occasion: str = ""
    action: dict[str, Any] = field(default_factory=dict)

class CalendarManager:
    calendars = ("gregorian", "persian", "hijri")
    def __init__(self) -> None:
        self.events: list[CalendarEvent] = []
    def add(self, event: CalendarEvent) -> CalendarEvent:
        if event.calendar not in self.calendars:
            raise ValueError("Unsupported calendar")
        self.events.append(event)
        return event
    def list(self) -> list[CalendarEvent]:
        return list(self.events)
