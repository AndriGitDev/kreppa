from __future__ import annotations

from kreppa.clients.pxweb import PxWebClient


def test_jsonstat2_rows() -> None:
    dataset = {
        "id": ["Month", "Index"],
        "size": [2, 1],
        "dimension": {
            "Month": {"category": {"index": {"2026M03": 0, "2026M04": 1}, "label": {"2026M03": "2026M03", "2026M04": "2026M04"}}},
            "Index": {"category": {"index": {"CPI": 0}, "label": {"CPI": "Consumer price index"}}},
        },
        "value": [100, 102],
    }
    rows = PxWebClient().rows(dataset, "Month")
    assert rows[1]["period"] == "2026M04"
    assert rows[1]["value"] == 102
    assert rows[1]["dimensions"]["Index"] == "CPI"
