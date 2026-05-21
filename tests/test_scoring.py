from __future__ import annotations

from datetime import date

from kreppa.scoring import indicator_stress, percentile_stress, score_level, threshold_stress


def test_threshold_higher_is_worse() -> None:
    assert threshold_stress(2.5, {"good": 2.5, "bad": 10.0}, "higher_is_worse") == 0
    assert threshold_stress(10.0, {"good": 2.5, "bad": 10.0}, "higher_is_worse") == 100


def test_threshold_lower_is_worse() -> None:
    assert threshold_stress(3.0, {"good": 3.0, "bad": -4.0}, "lower_is_worse") == 0
    assert threshold_stress(-4.0, {"good": 3.0, "bad": -4.0}, "lower_is_worse") == 100


def test_percentile_lower_is_worse_inverts_rank() -> None:
    stress = percentile_stress(1.0, [1, 2, 3, 4], "lower_is_worse")
    assert stress < 80


def test_combined_stress_uses_threshold() -> None:
    config = {"direction": "higher_is_worse", "threshold": {"good": 0, "bad": 10}}
    assert indicator_stress(10, [0, 5, 10], config) > 80


def test_score_level_uses_integer_bands() -> None:
    levels = [
        {"min": 40, "max": 59, "label": "middle"},
        {"min": 60, "max": 79, "label": "high"},
    ]
    assert score_level(59.09, levels)["label"] == "middle"
