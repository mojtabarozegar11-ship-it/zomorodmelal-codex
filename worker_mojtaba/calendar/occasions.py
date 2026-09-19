"""Configurable occasion provider boundary."""
class OccasionProvider:
    def list(self, calendar: str, date: str) -> list[dict]:
        return [{"calendar": calendar, "date": date, "status": "occasion_provider_required", "occasions": []}]
