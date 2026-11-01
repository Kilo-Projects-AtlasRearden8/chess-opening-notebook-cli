"""Tests for the chess opening notebook."""

from __future__ import annotations

import csv
import json
import os
import tempfile

import pytest

from chess_notebook.cli import main
from chess_notebook.models import ENTRY_TYPES, Entry
from chess_notebook.storage import Storage

SAMPLE_PGN = """1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 O-O 8. c3 d5 9. exd5 Nxd5 10. Nxe5 Nxe5 11. Rxe5 c6 12. d4 Bd6 13. Re1 Qh4 14. g3 Qh3 15. gxh3 Nf4 16. Rf1 Nxh3 17. Kf2 Ng5+ 18. Kg2 Qf6 19. Rxf6 gxf6 20. h4"""


@pytest.fixture
def tmp_storage():
    with tempfile.TemporaryDirectory() as td:
        yield Storage(os.path.join(td, "notebook.json"))


def test_entry_creation_and_id(tmp_storage):
    entry = Entry(
        title="Ruy Lopez",
        entry_type="opening_line",
        pgn=SAMPLE_PGN,
        review_date="2027-01-15",
        notes="classic",
        tags="open,king's pawn",
    )
    assert entry.id is not None
    assert len(entry.id) == 12
    assert entry.created_at.endswith("Z")
    tmp_storage.add(entry)
    got = tmp_storage.get(entry.id)
    assert got is not None
    assert got.title == "Ruy Lopez"
    assert got.entry_type == "opening_line"


def test_entry_type_validation():
    with pytest.raises(ValueError):
        Entry(title="t", entry_type="blunder", pgn=SAMPLE_PGN, review_date="2027-01-01")


def test_entry_pgn_validation():
    with pytest.raises(ValueError):
        Entry(title="t", entry_type="trap", pgn="not valid pgn", review_date="2027-01-01")


def test_entry_review_date_validation():
    with pytest.raises(ValueError):
        Entry(title="t", entry_type="refutation", pgn=SAMPLE_PGN, review_date="not-a-date")


def test_storage_list_and_filter(tmp_storage):
    tmp_storage.add(Entry(title="A", entry_type="opening_line", pgn=SAMPLE_PGN, review_date="2027-01-01"))
    tmp_storage.add(Entry(title="B", entry_type="trap", pgn=SAMPLE_PGN, review_date="2027-02-01"))
    tmp_storage.add(Entry(title="C", entry_type="refutation", pgn=SAMPLE_PGN, review_date="2027-03-01"))

    assert len(tmp_storage.list()) == 3
    assert len(tmp_storage.list(entry_type="trap")) == 1
    assert tmp_storage.list(entry_type="trap")[0].title == "B"


def test_storage_export_json_and_csv(tmp_storage):
    tmp_storage.add(Entry(title="X", entry_type="opening_line", pgn=SAMPLE_PGN, review_date="2027-01-01"))
    jpath = os.path.join(tempfile.gettempdir(), "chess_notebook_test_export.json")
    cpath = os.path.join(tempfile.gettempdir(), "chess_notebook_test_export.csv")
    tmp_storage.export_json(jpath)
    tmp_storage.export_csv(cpath)

    with open(jpath) as fh:
        data = json.load(fh)
    assert len(data) == 1
    assert data[0]["title"] == "X"

    with open(cpath, newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 1
    assert rows[0]["title"] == "X"
    assert rows[0]["entry_type"] == "opening_line"


def test_cli_add_list_show(tmp_storage):
    db = tmp_storage.path
    assert main(["--db", db, "add", "--title", "Sicilian", "--type", "opening_line",
                 "--pgn", SAMPLE_PGN, "--review-date", "2027-05-01", "--tags", "sicily"]) == 0
    assert main(["--db", db, "list"]) == 0
    # Capture show output indirectly via get
    entries = tmp_storage.list()
    assert len(entries) == 1
    assert main(["--db", db, "show", "--id", entries[0].id]) == 0


def test_cli_export_csv(tmp_storage):
    db = tmp_storage.path
    tmp_storage.add(Entry(title="Y", entry_type="trap", pgn=SAMPLE_PGN, review_date="2027-06-01"))
    out = os.path.join(tempfile.gettempdir(), "chess_notebook_cli_export.csv")
    assert main(["--db", db, "export", "--format", "csv", "--out", out]) == 0
    with open(out, newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert rows[0]["title"] == "Y"


def test_entry_types_constant():
    assert "opening_line" in ENTRY_TYPES
    assert "trap" in ENTRY_TYPES
    assert "refutation" in ENTRY_TYPES
