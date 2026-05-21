from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field


class Observation(BaseModel):
    indicator_id: str
    source_id: str
    period: str
    period_start: date | None = None
    period_end: date | None = None
    value: float | None
    unit: str
    raw_value: Any | None = None
    source_url: str
    retrieved_at: datetime
    published_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class SourceFailure(BaseModel):
    source_id: str
    code: str
    message: str


class IndicatorScore(BaseModel):
    id: str
    label_is: str
    label_en: str
    value: float
    unit: str
    period: str
    stress_score: float
    direction: str
    source_id: str
    source_name: str
    source_url: str
    retrieved_at: datetime
    stale: bool
    contribution: float


class ComponentScore(BaseModel):
    id: str
    label_is: str
    label_en: str
    score: float | None
    weight: float
    confidence: float
    indicators: list[IndicatorScore] = Field(default_factory=list)
    missing_or_stale: list[str] = Field(default_factory=list)


class ScoreOutput(BaseModel):
    schema_version: str = "1.0.0"
    score_version: str
    generated_at: datetime
    as_of: date
    overall: dict[str, Any]
    components: list[ComponentScore]
    drivers: dict[str, list[dict[str, Any]]]
    warnings: list[str]
    attribution: list[str]
