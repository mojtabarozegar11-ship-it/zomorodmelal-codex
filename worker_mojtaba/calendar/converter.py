"""Calendar conversion abstraction.

The project keeps calendar math behind this interface so an authoritative
Persian/Hijri provider can be plugged in without changing scheduling logic.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class CalendarDate:
    calendar: str
    year: int
    month: int
    day: int


class CalendarConverter:
    SUPPORTED = ("gregorian", "persian", "hijri")

    def __init__(self, provider=None):
        self.provider = provider

    def convert(self, value: CalendarDate, target: str) -> CalendarDate:
        if value.calendar not in self.SUPPORTED or target not in self.SUPPORTED:
            raise ValueError("Unsupported calendar")
        if value.calendar == target:
            return value
        if self.provider is None:
            raise RuntimeError("authoritative_calendar_provider_required")
        result = self.provider.convert(value, target)
        if not isinstance(result, CalendarDate):
            raise TypeError("calendar provider returned invalid result")
        return result

    def resolve(self, value: CalendarDate) -> CalendarDate:
        """Validate and normalize a date through the configured provider."""
        if value.calendar not in self.SUPPORTED:
            raise ValueError("Unsupported calendar")
        if self.provider is None:
            raise RuntimeError("authoritative_calendar_provider_required")
        result = self.provider.resolve(value)
        if not isinstance(result, CalendarDate):
            raise TypeError("calendar provider returned invalid result")
        return result
