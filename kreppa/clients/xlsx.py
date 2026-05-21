from __future__ import annotations

import re
from datetime import datetime, timedelta
from io import BytesIO
from typing import Any
from zipfile import ZipFile

import requests
from xml.etree import ElementTree as ET


NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


class XlsxError(RuntimeError):
    pass


class CentralBankNewCreditClient:
    def __init__(self, timeout: int = 30) -> None:
        self.timeout = timeout

    def rows(self, url: str) -> list[dict[str, Any]]:
        response = requests.get(url, timeout=self.timeout)
        if response.status_code != 200:
            raise XlsxError(f"Excel download failed {response.status_code}: {url}")
        return self.parse(response.content)

    def parse(self, content: bytes) -> list[dict[str, Any]]:
        with ZipFile(BytesIO(content)) as archive:
            strings = self._shared_strings(archive)
            sheet_xml = archive.read("xl/worksheets/sheet2.xml")

        root = ET.fromstring(sheet_xml)
        rows = root.findall(".//m:sheetData/m:row", NS)
        header = self._row_cells(rows[9], strings)
        date_columns = {
            col: self._excel_serial_to_period(value)
            for col, value in header.items()
            if col != "A" and value not in (None, "")
        }

        out: list[dict[str, Any]] = []
        block = ""
        for row in rows[10:]:
            cells = self._row_cells(row, strings)
            label = cells.get("A")
            if not label:
                continue
            label = str(label).strip()
            if label.startswith("Ný ") or label.startswith("New "):
                block = label
                continue
            for col, period in date_columns.items():
                value = self._float_or_none(cells.get(col))
                out.append(
                    {
                        "period": period,
                        "value": value,
                        "dimensions": {
                            "sector": label,
                            "sector_en": self._english_name(label),
                            "sector_is": self._icelandic_name(label),
                            "block": block,
                        },
                    }
                )
        return out

    def _shared_strings(self, archive: ZipFile) -> list[str]:
        try:
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
        except KeyError:
            return []
        strings = []
        for item in root.findall("m:si", NS):
            strings.append("".join(node.text or "" for node in item.findall(".//m:t", NS)))
        return strings

    def _row_cells(self, row: ET.Element, strings: list[str]) -> dict[str, Any]:
        cells: dict[str, Any] = {}
        for cell in row.findall("m:c", NS):
            ref = cell.attrib["r"]
            col = re.match(r"([A-Z]+)", ref)
            if not col:
                continue
            cells[col.group(1)] = self._cell_value(cell, strings)
        return cells

    def _cell_value(self, cell: ET.Element, strings: list[str]) -> Any:
        value = cell.find("m:v", NS)
        if value is None:
            return None
        raw = value.text
        if raw is None:
            return None
        if cell.attrib.get("t") == "s":
            return strings[int(raw)]
        return raw

    def _excel_serial_to_period(self, serial: Any) -> str:
        dt = datetime(1899, 12, 30) + timedelta(days=float(serial))
        return f"{dt.year}M{dt.month:02d}"

    def _float_or_none(self, value: Any) -> float | None:
        if value in (None, ""):
            return None
        return float(value)

    def _english_name(self, label: str) -> str:
        return label.split(" / ", 1)[1] if " / " in label else label

    def _icelandic_name(self, label: str) -> str:
        return label.split(" / ", 1)[0] if " / " in label else label
