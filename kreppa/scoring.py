from __future__ import annotations

from datetime import UTC, date, datetime
from statistics import mean
from typing import Any

from kreppa.freshness import is_stale
from kreppa.models import ComponentScore, IndicatorScore, ScoreOutput


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def percentile_stress(value: float, history: list[float], direction: str) -> float:
    if not history:
        return 50.0
    ordered = sorted(history)
    low_i = max(0, int(len(ordered) * 0.01))
    high_i = min(len(ordered) - 1, int(len(ordered) * 0.99))
    low = ordered[low_i]
    high = ordered[high_i]
    winsorized = [clamp(item, low, high) for item in history]
    current = clamp(value, low, high)
    below_or_equal = sum(1 for item in winsorized if item <= current)
    rank = below_or_equal / len(winsorized) * 100.0
    return 100.0 - rank if direction == "lower_is_worse" else rank


def threshold_stress(value: float, threshold: dict[str, float], direction: str) -> float:
    good = float(threshold["good"])
    bad = float(threshold["bad"])
    if direction == "lower_is_worse":
        return clamp((good - value) / (good - bad) * 100.0)
    return clamp((value - good) / (bad - good) * 100.0)


def indicator_stress(value: float, history: list[float], config: dict[str, Any]) -> float:
    percentile = percentile_stress(value, history, config["direction"])
    threshold = config.get("threshold")
    if not threshold:
        return percentile
    return (0.70 * percentile) + (0.30 * threshold_stress(value, threshold, config["direction"]))


def confidence_label(confidence: float) -> str:
    if confidence >= 0.85:
        return "High"
    if confidence >= 0.60:
        return "Medium"
    return "Low"


def score_level(score: float, levels: list[dict[str, Any]]) -> dict[str, Any]:
    for level in levels:
        if float(level["min"]) <= score < float(level["max"]) + 1:
            return level
    return levels[-1]


def compute_score(
    observations: list[dict[str, Any]],
    indicator_config: dict[str, Any],
    source_config: dict[str, Any],
    as_of: date | None = None,
    warnings: list[str] | None = None,
) -> ScoreOutput:
    as_of = as_of or date.today()
    warnings = list(warnings or [])
    sources = {source["id"]: source for source in source_config.get("sources", [])}
    by_indicator: dict[str, list[dict[str, Any]]] = {}
    for observation in observations:
        by_indicator.setdefault(observation["indicator_id"], []).append(observation)

    components: list[ComponentScore] = []
    all_indicator_scores: list[IndicatorScore] = []

    for component_id, component_cfg in indicator_config["components"].items():
        configured = [item for item in indicator_config["indicators"] if item["component"] == component_id]
        available_scores = []
        indicators = []
        missing_or_stale = []
        configured_weight = sum(float(item["weight_within_component"]) for item in configured)
        available_weight = 0.0

        for indicator in configured:
            series = sorted(by_indicator.get(indicator["id"], []), key=lambda item: item["period"])
            usable = [item for item in series if item.get("value") is not None]
            latest = usable[-1] if usable else None
            if not latest:
                missing_or_stale.append(indicator["id"])
                continue
            stale = is_stale(latest["period"], as_of, int(indicator["stale_after_days"]))
            if stale:
                missing_or_stale.append(indicator["id"])
                warnings.append(f"{indicator['label_en']} is stale at period {latest['period']}.")
                continue

            history = [float(item["value"]) for item in usable]
            stress = indicator_stress(float(latest["value"]), history, indicator)
            weight = float(indicator["weight_within_component"])
            available_weight += weight
            available_scores.append((stress, weight))
            source = sources[indicator["source_id"]]
            contribution = float(component_cfg["weight"]) * weight * (stress - 50.0)
            scored = IndicatorScore(
                id=indicator["id"],
                label_is=indicator["label_is"],
                label_en=indicator["label_en"],
                value=round(float(latest["value"]), 2),
                unit=indicator["unit"],
                period=latest["period"],
                stress_score=round(stress, 2),
                direction=indicator["direction"],
                source_id=indicator["source_id"],
                source_name=source["attribution"],
                source_url=source["page_url"],
                retrieved_at=datetime.fromisoformat(latest["retrieved_at"].replace("Z", "+00:00")),
                stale=False,
                contribution=round(contribution, 3),
            )
            indicators.append(scored)
            all_indicator_scores.append(scored)

        component_score = weighted_average(available_scores)
        confidence = available_weight / configured_weight if configured_weight else 0.0
        components.append(
            ComponentScore(
                id=component_id,
                label_is=component_cfg["label_is"],
                label_en=component_cfg["label_en"],
                score=round(component_score, 2) if component_score is not None else None,
                weight=float(component_cfg["weight"]),
                confidence=round(confidence, 3),
                indicators=indicators,
                missing_or_stale=missing_or_stale,
            )
        )

    weighted_components = [(component.score, component.weight) for component in components if component.score is not None]
    raw_score = weighted_average(weighted_components) or 0.0
    available_component_weight = sum(component.weight for component in components if component.score is not None)
    total_component_weight = sum(float(item["weight"]) for item in indicator_config["components"].values())
    confidence = available_component_weight / total_component_weight if total_component_weight else 0.0

    if not any(component.id == "credit_banking" and component.score is not None for component in components):
        warnings.append("Credit and banking component is pending because a stable public machine-readable endpoint is not yet verified.")

    up = sorted([item for item in all_indicator_scores if item.contribution > 0], key=lambda item: item.contribution, reverse=True)[:3]
    down = sorted([item for item in all_indicator_scores if item.contribution < 0], key=lambda item: item.contribution)[:3]
    generated_at = datetime.now(UTC)
    level = score_level(raw_score, indicator_config["levels"])

    return ScoreOutput(
        score_version=indicator_config["score_version"],
        generated_at=generated_at,
        as_of=as_of,
        overall={
            "score": round(raw_score),
            "raw_score": round(raw_score, 2),
            "confidence": round(confidence, 3),
            "confidence_label": confidence_label(confidence),
            "level": level,
        },
        components=components,
        drivers={
            "up": [_driver(item, True) for item in up],
            "down": [_driver(item, False) for item in down],
        },
        warnings=sorted(set(warnings)),
        attribution=sorted({source["attribution"] for source in source_config.get("sources", [])}),
    )


def weighted_average(values: list[tuple[float | None, float]]) -> float | None:
    clean = [(float(value), float(weight)) for value, weight in values if value is not None and weight > 0]
    if not clean:
        return None
    denominator = sum(weight for _value, weight in clean)
    return sum(value * weight for value, weight in clean) / denominator


def _driver(item: IndicatorScore, up: bool) -> dict[str, Any]:
    reason = (
        f"{item.label_is} ýtir mælinum upp miðað við sögu og þröskulda."
        if up
        else f"{item.label_is} heldur aftur af kreppu-stemmingunni."
    )
    return {
        "indicator_id": item.id,
        "label_is": item.label_is,
        "label_en": item.label_en,
        "reason_is": reason,
        "contribution": item.contribution,
    }
