from __future__ import annotations

from pathlib import Path

import pytest

from kreppa.clients.xlsx import CentralBankNewCreditClient


@pytest.mark.skipif(not Path("/tmp/newcredit.xlsx").exists(), reason="live Excel inspection fixture not present")
def test_new_credit_client_parses_downloaded_excel() -> None:
    rows = CentralBankNewCreditClient().parse(Path("/tmp/newcredit.xlsx").read_bytes())
    household = [row for row in rows if row["dimensions"]["sector_en"] == "Households"]
    assert household
    assert household[-1]["period"].startswith("2026M")
