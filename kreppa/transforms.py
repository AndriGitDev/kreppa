from __future__ import annotations

from datetime import date
from typing import Any

from kreppa.freshness import period_end
from kreppa.models import Observation


def sort_periods(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(rows, key=lambda row: row["period"])


def matches(row: dict[str, Any], match: dict[str, Any]) -> bool:
    dimensions = row.get("dimensions", {})
    return all(str(dimensions.get(key)) == str(value) for key, value in match.items())


def latest_value(rows: list[dict[str, Any]], indicator: dict[str, Any], source: dict[str, Any], retrieved_at) -> list[Observation]:
    out = []
    for row in sort_periods([r for r in rows if matches(r, indicator.get("match", {}))]):
        value = row.get("value")
        if value is None:
            continue
        end = period_end(row["period"])
        out.append(
            Observation(
                indicator_id=indicator["id"],
                source_id=source["id"],
                period=row["period"],
                period_end=end,
                value=float(value),
                unit=indicator["unit"],
                raw_value=value,
                source_url=source["page_url"],
                retrieved_at=retrieved_at,
                metadata={"dimensions": row.get("dimensions", {})},
            )
        )
    return out


def yoy_percent_change(rows: list[dict[str, Any]], indicator: dict[str, Any], source: dict[str, Any], retrieved_at) -> list[Observation]:
    selected = sort_periods([r for r in rows if matches(r, indicator.get("match", {})) and r.get("value") is not None])
    by_period = {row["period"]: float(row["value"]) for row in selected}
    out = []
    for row in selected:
        period = row["period"]
        previous_period = _previous_year_period(period)
        previous = by_period.get(previous_period)
        current = float(row["value"])
        if previous in (None, 0):
            continue
        value = ((current / previous) - 1.0) * 100.0
        end = period_end(period)
        out.append(
            Observation(
                indicator_id=indicator["id"],
                source_id=source["id"],
                period=period,
                period_end=end,
                value=value,
                unit=indicator["unit"],
                raw_value=current,
                source_url=source["page_url"],
                retrieved_at=retrieved_at,
                metadata={"previous_period": previous_period, "dimensions": row.get("dimensions", {})},
            )
        )
    return out


def rolling_12m_sum_yoy(rows: list[dict[str, Any]], indicator: dict[str, Any], source: dict[str, Any], retrieved_at) -> list[Observation]:
    selected = sort_periods([r for r in rows if matches(r, indicator.get("match", {})) and r.get("value") is not None])
    out = []
    for index in range(23, len(selected)):
        current_window = selected[index - 11 : index + 1]
        previous_window = selected[index - 23 : index - 11]
        current_sum = sum(float(row["value"]) for row in current_window)
        previous_sum = sum(float(row["value"]) for row in previous_window)
        if previous_sum == 0:
            continue
        period = selected[index]["period"]
        value = ((current_sum / previous_sum) - 1.0) * 100.0
        end = period_end(period)
        out.append(
            Observation(
                indicator_id=indicator["id"],
                source_id=source["id"],
                period=period,
                period_end=end,
                value=value,
                unit=indicator["unit"],
                raw_value=current_sum,
                source_url=source["page_url"],
                retrieved_at=retrieved_at,
                metadata={
                    "rolling_12m_sum": current_sum,
                    "previous_12m_sum": previous_sum,
                    "dimensions": selected[index].get("dimensions", {}),
                },
            )
        )
    return out


def _previous_year_period(period: str) -> str:
    if "M" in period:
        year_s, month_s = period.split("M", 1)
        return f"{int(year_s) - 1}M{month_s}"
    if "Q" in period:
        year_s, quarter_s = period.split("Q", 1)
        return f"{int(year_s) - 1}Q{quarter_s}"
    if period.isdigit():
        return str(int(period) - 1)
    raise ValueError(f"Unsupported period format: {period}")


TRANSFORMS = {
    "latest_value": latest_value,
    "yoy_percent_change": yoy_percent_change,
    "rolling_12m_sum_yoy": rolling_12m_sum_yoy,
}
