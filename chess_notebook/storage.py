"""Local-first JSON/CSV storage for notebook entries."""

from __future__ import annotations

import csv
import json
import os
from typing import Iterable, List, Optional

from .models import ENTRY_TYPES, Entry


class Storage:
    """Persists entries to a local JSON file; exports to JSON or CSV."""

    def __init__(self, path: str) -> None:
        self.path = path

    @classmethod
    def default_path(cls) -> str:
        return os.path.join(os.getcwd(), "chess_notebook.json")

    def load(self) -> List[Entry]:
        if not os.path.exists(self.path):
            return []
        with open(self.path, "r", encoding="utf-8") as fh:
            raw = fh.read().strip()
        if not raw:
            return []
        data = json.loads(raw)
        if not isinstance(data, list):
            raise ValueError(f"Storage file {self.path} does not contain a list")
        return [Entry.from_dict(item) for item in data]

    def save(self, entries: Iterable[Entry]) -> None:
        entries = list(entries)
        payload = [e.to_dict() for e in entries]
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, sort_keys=True)
            fh.write("\n")
        os.replace(tmp, self.path)

    def add(self, entry: Entry) -> Entry:
        entries = self.load()
        entries.append(entry)
        self.save(entries)
        return entry

    def get(self, entry_id: str) -> Optional[Entry]:
        for entry in self.load():
            if entry.id == entry_id:
                return entry
        return None

    def list(
        self,
        entry_type: Optional[str] = None,
        due_only: bool = False,
        as_of: Optional[str] = None,
    ) -> List[Entry]:
        from datetime import date

        entries = self.load()
        if entry_type is not None:
            if entry_type not in ENTRY_TYPES:
                raise ValueError(f"unknown entry type: {entry_type!r}")
            entries = [e for e in entries if e.entry_type == entry_type]
        if due_only:
            today = date.fromisoformat(as_of) if as_of else date.today()
            entries = [e for e in entries if date.fromisoformat(e.review_date) <= today]
        entries.sort(key=lambda e: (e.review_date, e.title))
        return entries

    def export_json(self, out_path: str) -> None:
        entries = self.load()
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump([e.to_dict() for e in entries], fh, indent=2, sort_keys=True)
            fh.write("\n")

    def export_csv(self, out_path: str) -> None:
        entries = self.load()
        fields = [
            "id",
            "title",
            "entry_type",
            "pgn",
            "fen",
            "review_date",
            "notes",
            "tags",
            "created_at",
        ]
        with open(out_path, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields)
            writer.writeheader()
            for entry in entries:
                row = entry.to_dict()
                writer.writerow({k: row.get(k, "") for k in fields})
