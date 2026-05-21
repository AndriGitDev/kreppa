from __future__ import annotations

import itertools
from typing import Any

import requests


class PxWebError(RuntimeError):
    pass


class PxWebClient:
    def __init__(self, timeout: int = 30) -> None:
        self.timeout = timeout

    def metadata(self, api_url: str) -> dict[str, Any]:
        response = requests.get(api_url, timeout=self.timeout)
        if response.status_code != 200:
            raise PxWebError(f"Metadata request failed {response.status_code}: {api_url}")
        return response.json()

    def query(self, api_url: str, metadata: dict[str, Any], selections: dict[str, list[str]], time_code: str) -> dict[str, Any]:
        query = []
        for variable in metadata["variables"]:
            code = variable["code"]
            values = selections.get(code)
            if values is None:
                if time_code == "composite_year_month" and code in {"Ár", "Mánuður"}:
                    values = variable["values"]
                elif code == time_code:
                    values = variable["values"]
                else:
                    values = variable["values"]
            query.append({"code": code, "selection": {"filter": "item", "values": values}})
        payload = {"query": query, "response": {"format": "JSON-stat2"}}
        response = requests.post(api_url, json=payload, timeout=self.timeout)
        if response.status_code != 200:
            raise PxWebError(f"Data request failed {response.status_code}: {api_url}: {response.text[:200]}")
        return response.json()

    def rows(self, dataset: dict[str, Any], time_code: str) -> list[dict[str, Any]]:
        ids = dataset["id"]
        sizes = dataset["size"]
        dimensions = dataset["dimension"]
        value = dataset.get("value", [])
        categories = []
        for dim_id in ids:
            dim = dimensions[dim_id]["category"]
            ordered = sorted(dim["index"].items(), key=lambda item: item[1])
            categories.append([(code, dim.get("label", {}).get(code, code)) for code, _ in ordered])

        rows = []
        for index, combo in enumerate(itertools.product(*categories)):
            row_value = value[index] if index < len(value) else None
            dims = {dim_id: code for dim_id, (code, _label) in zip(ids, combo, strict=True)}
            dim_labels = {dim_id: label for dim_id, (_code, label) in zip(ids, combo, strict=True)}
            if time_code == "composite_year_month":
                period = f"{dims['Ár']}M{int(dims['Mánuður']):02d}"
            else:
                period = dims[time_code]
            rows.append(
                {
                    "period": period,
                    "value": row_value,
                    "dimensions": dims,
                    "dimension_labels": dim_labels,
                }
            )
        return rows
