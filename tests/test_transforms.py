from __future__ import annotations

from datetime import UTC, datetime

from kreppa.transforms import yoy_percent_change


def test_yoy_percent_change_monthly() -> None:
    rows = [
        {"period": "2025M04", "value": 100, "dimensions": {"Index": "CPI"}},
        {"period": "2026M04", "value": 110, "dimensions": {"Index": "CPI"}},
    ]
    indicator = {
        "id": "headline_inflation_yoy",
        "unit": "% YoY",
        "match": {"Index": "CPI"},
    }
    source = {"id": "statice_cpi", "page_url": "https://example.test"}
    obs = yoy_percent_change(rows, indicator, source, datetime.now(UTC))
    assert len(obs) == 1
    assert round(obs[0].value or 0, 2) == 10.0
    assert obs[0].period == "2026M04"
