from __future__ import annotations

from datetime import date

from kreppa.freshness import is_stale, period_end


def test_period_end_month() -> None:
    assert period_end("2026M02") == date(2026, 2, 28)


def test_period_end_quarter() -> None:
    assert period_end("2026Q1") == date(2026, 3, 31)


def test_stale() -> None:
    assert is_stale("2025M01", date(2026, 5, 21), 75)
    assert not is_stale("2026M04", date(2026, 5, 21), 75)
