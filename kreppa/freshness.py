from __future__ import annotations

from datetime import date


def period_end(period: str) -> date | None:
    if "M" in period:
        year_s, month_s = period.split("M", 1)
        year = int(year_s)
        month = int(month_s)
        if month == 12:
            return date(year, 12, 31)
        return date(year, month + 1, 1).replace(day=1).fromordinal(
            date(year, month + 1, 1).toordinal() - 1
        )
    if "Q" in period:
        year_s, quarter_s = period.split("Q", 1)
        month = int(quarter_s) * 3
        if month == 12:
            return date(int(year_s), 12, 31)
        return date(int(year_s), month + 1, 1).fromordinal(
            date(int(year_s), month + 1, 1).toordinal() - 1
        )
    if period.isdigit() and len(period) == 4:
        return date(int(period), 12, 31)
    return None


def is_stale(period: str, as_of: date, stale_after_days: int) -> bool:
    end = period_end(period)
    if end is None:
        return True
    return (as_of - end).days > stale_after_days
