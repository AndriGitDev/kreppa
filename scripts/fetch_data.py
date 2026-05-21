#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kreppa.clients.pxweb import PxWebClient, PxWebError
from kreppa.clients.xlsx import CentralBankNewCreditClient, XlsxError
from kreppa.sources import load_yaml, repo_root
from kreppa.transforms import TRANSFORMS


ROOT = repo_root()
SOURCES_PATH = ROOT / "data/catalog/sources.yaml"
INDICATORS_PATH = ROOT / "data/catalog/indicators.yaml"
OBSERVATIONS_PATH = ROOT / "data/snapshots/observations.json"


def main() -> int:
    source_catalog = load_yaml(SOURCES_PATH)
    indicator_catalog = load_yaml(INDICATORS_PATH)
    client = PxWebClient()
    xlsx_client = CentralBankNewCreditClient()
    retrieved_at = datetime.now(UTC)
    observations = []
    failures = []
    rows_by_source = {}

    for source in source_catalog.get("sources", []):
        try:
            if source["kind"] == "pxweb":
                metadata = client.metadata(source["api_url"])
                data = client.query(source["api_url"], metadata, source.get("query", {}), source["time_code"])
                rows_by_source[source["id"]] = client.rows(data, source["time_code"])
            elif source["kind"] == "central_bank_new_credit_xlsx":
                rows_by_source[source["id"]] = xlsx_client.rows(source["download_url"])
            else:
                raise ValueError(f"Unsupported source kind: {source['kind']}")
        except (PxWebError, XlsxError, KeyError, ValueError) as exc:
            failures.append({"source_id": source["id"], "code": "SOURCE_UNREACHABLE", "message": str(exc)})

    sources = {source["id"]: source for source in source_catalog.get("sources", [])}
    for indicator in indicator_catalog.get("indicators", []):
        source = sources.get(indicator["source_id"])
        rows = rows_by_source.get(indicator["source_id"])
        if not source or rows is None:
            failures.append(
                {
                    "source_id": indicator["source_id"],
                    "code": "SOURCE_VALUE_MISSING",
                    "message": f"No rows available for {indicator['id']}",
                }
            )
            continue
        transform = TRANSFORMS[indicator["transform"]]
        transformed = transform(rows, indicator, source, retrieved_at)
        observations.extend(item.model_dump(mode="json") for item in transformed)
        if not transformed:
            failures.append(
                {
                    "source_id": indicator["source_id"],
                    "code": "TRANSFORM_FAILED",
                    "message": f"Transform produced no observations for {indicator['id']}",
                }
            )

    payload = {
        "schema_version": "1.0.0",
        "generated_at": retrieved_at.isoformat().replace("+00:00", "Z"),
        "observations": observations,
        "failures": failures,
    }
    OBSERVATIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    OBSERVATIONS_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(observations)} observations to {OBSERVATIONS_PATH}")
    if failures:
        print(f"Recorded {len(failures)} non-fatal source/indicator failures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
