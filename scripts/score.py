#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kreppa.scoring import compute_score
from kreppa.sources import load_yaml, repo_root


ROOT = repo_root()
OBSERVATIONS_PATH = ROOT / "data/snapshots/observations.json"
LATEST_PATH = ROOT / "data/snapshots/latest.json"
HISTORY_PATH = ROOT / "data/snapshots/history.json"
SOURCES_OUT = ROOT / "data/snapshots/sources.json"
METHODOLOGY_OUT = ROOT / "data/snapshots/methodology.json"
WEB_DATA = ROOT / "apps/web/public/data"


def main() -> int:
    indicator_catalog = load_yaml(ROOT / "data/catalog/indicators.yaml")
    source_catalog = load_yaml(ROOT / "data/catalog/sources.yaml")
    observations_payload = json.loads(OBSERVATIONS_PATH.read_text(encoding="utf-8"))
    failures = observations_payload.get("failures", [])
    warnings = [f"{item['code']}: {item['message']}" for item in failures]
    score = compute_score(
        observations_payload.get("observations", []),
        indicator_catalog,
        source_catalog,
        warnings=warnings,
    )

    latest_json = score.model_dump(mode="json")
    write_json(LATEST_PATH, latest_json)
    write_json(HISTORY_PATH, build_history(latest_json))
    write_json(SOURCES_OUT, build_sources(source_catalog))
    write_json(METHODOLOGY_OUT, build_methodology(indicator_catalog, source_catalog))

    WEB_DATA.mkdir(parents=True, exist_ok=True)
    for path in [LATEST_PATH, HISTORY_PATH, SOURCES_OUT, METHODOLOGY_OUT]:
        shutil.copy2(path, WEB_DATA / path.name)

    print(f"Wrote score {latest_json['overall']['score']}/100 to {LATEST_PATH}")
    return 0


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def build_history(latest: dict) -> dict:
    return {
        "schema_version": "1.0.0",
        "score_version": latest["score_version"],
        "generated_at": latest["generated_at"],
        "history": [
            {
                "date": latest["as_of"],
                "score": latest["overall"]["score"],
                "raw_score": latest["overall"]["raw_score"],
                "confidence": latest["overall"]["confidence"],
            }
        ],
        "note": "History begins with generated snapshots in the MVP. Backfill is implemented as a future calibration step.",
    }


def build_sources(source_catalog: dict) -> dict:
    return {
        "schema_version": "1.0.0",
        "sources": source_catalog.get("sources", []),
        "pending_sources": source_catalog.get("pending_sources", []),
    }


def build_methodology(indicator_catalog: dict, source_catalog: dict) -> dict:
    return {
        "schema_version": "1.0.0",
        "score_version": indicator_catalog["score_version"],
        "components": indicator_catalog["components"],
        "indicators": indicator_catalog["indicators"],
        "normalization": {
            "percentile": "Winsorized 1st/99th percentile rank; inverted when lower values are worse.",
            "threshold": "Linear 0-100 scale between configured good and bad thresholds.",
            "combined": "0.70 percentile stress + 0.30 threshold stress when thresholds exist.",
        },
        "missing_data": "Missing or stale indicators are excluded from scoring and reduce confidence.",
        "disclaimer": "Kreppumælirinn er ekki fjármálaráðgjöf. Hann er opið gagnamælaborð með kvíða.",
        "source_count": len(source_catalog.get("sources", [])),
    }


if __name__ == "__main__":
    raise SystemExit(main())
