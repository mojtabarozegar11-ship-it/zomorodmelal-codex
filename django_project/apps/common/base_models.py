from datetime import datetime, timezone


class BaseEntity:
    """Common base structure placeholder for shared Django entities."""

    @staticmethod
    def created_at() -> datetime:
        """Return the current UTC timestamp when requested."""
        return datetime.now(timezone.utc)
