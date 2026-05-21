#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kreppa.sources import repo_root


ROOT = repo_root()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", action="store_true", help="Validate checked-in static fixture outputs.")
    args = parser.parse_args()
    base = ROOT / "apps/web/public/data" if args.fixtures else ROOT / "data/snapshots"
    latest = load(base / "latest.json")
    history = load(base / "history.json")
    sources = load(base / "sources.json")
    methodology = load(base / "methodology.json")

    required_latest = ["schema_version", "score_version", "generated_at", "overall", "components", "drivers", "warnings"]
    for key in required_latest:
        assert key in latest, f"latest.json missing {key}"
    assert 0 <= latest["overall"]["score"] <= 100
    assert latest["overall"]["confidence"] >= 0.55, "confidence below publish minimum"
    populated = [component for component in latest["components"] if component["score"] is not None]
    available_indicators = sum(len(component["indicators"]) for component in latest["components"])
    assert len(populated) >= 4, "fewer than 4 populated components"
    assert available_indicators >= 5, "fewer than 5 available indicators"
    assert history["score_version"] == latest["score_version"]
    assert len(sources["sources"]) >= 6
    assert methodology["score_version"] == latest["score_version"]
    print(f"Validated outputs in {base}")
    return 0


def load(path: Path) -> dict:
    assert path.exists(), f"Missing {path}"
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
