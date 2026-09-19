"""Built-in occasion catalog with explicit source categories.

Official Iranian dates should be synchronized from the current official calendar;
international observances are based on UN-designated observances.
"""
from dataclasses import dataclass
from typing import Optional, Iterable


@dataclass(frozen=True)
class Occasion:
    key: str
    title: str
    category: str
    calendar: str
    month: Optional[int] = None
    day: Optional[int] = None
    recurring: bool = True
    source: str = ""


class OccasionProvider:
    """Provides important Iranian, religious, and global occasion metadata."""

    CATEGORIES = ("iranian", "religious", "international")

    def list(self, category: Optional[str] = None):
        if category and category not in self.CATEGORIES:
            raise ValueError(f"unsupported category: {category}")
        items = [
            Occasion("nowruz", "نوروز", "iranian", "persian", 1, 1,
                     source="official_iranian_calendar"),
            Occasion("nature_day", "روز طبیعت", "iranian", "persian", 1, 13,
                     source="official_iranian_calendar"),
            Occasion("international_womens_day", "روز جهانی زن", "international",
                     "gregorian", 3, 8, source="un"),
            Occasion("world_water_day", "روز جهانی آب", "international",
                     "gregorian", 3, 22, source="un"),
            Occasion("world_environment_day", "روز جهانی محیط زیست", "international",
                     "gregorian", 6, 5, source="un"),
            Occasion("world_food_day", "روز جهانی غذا", "international",
                     "gregorian", 10, 16, source="un"),
            Occasion("international_day_of_peace", "روز جهانی صلح", "international",
                     "gregorian", 9, 21, source="un"),
            Occasion("world_tourism_day", "روز جهانی گردشگری", "international",
                     "gregorian", 9, 27, source="un"),
            Occasion("human_rights_day", "روز جهانی حقوق بشر", "international",
                     "gregorian", 12, 10, source="un"),
        ]
        # Religious lunar occasions are represented by keys and resolved against
        # an authoritative lunar calendar at runtime; fixed Gregorian/Persian
        # dates must not be substituted for them.
        religious = [
            ("eid_al_fitr", "عید فطر"),
            ("eid_al_adha", "عید قربان"),
            ("eid_al_ghadir", "عید غدیر"),
            ("eid_al_mabath", "مبعث"),
            ("ramadan", "ماه رمضان"),
            ("ashura", "عاشورا"),
            ("arbaeen", "اربعین"),
            ("eid_al_milad", "میلاد پیامبر(ص) و امام صادق(ع)"),
            ("imam_ali_birth", "ولادت امام علی(ع)"),
            ("imam_hossein_birth", "ولادت امام حسین(ع)"),
            ("imam_reza_birth", "ولادت امام رضا(ع)"),
            ("fatimah_birth", "ولادت حضرت فاطمه(س)"),
            ("imam_mahdi_birth", "ولادت امام مهدی(عج)"),
        ]
        items.extend(
            Occasion(key, title, "religious", "hijri", recurring=True,
                     source="lunar_calendar_provider")
            for key, title in religious
        )
        return [x for x in items if category is None or x.category == category]

    def by_keys(self, keys: Iterable[str]):
        wanted = set(keys)
        return [item for item in self.list() if item.key in wanted]

    def categories(self) -> tuple[str, ...]:
        return self.CATEGORIES
