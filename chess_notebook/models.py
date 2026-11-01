"""Data models for the chess opening notebook."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import date, datetime, timezone
from typing import Optional


ENTRY_TYPES = ("opening_line", "trap", "refutation")


@dataclass
class Entry:
    """A single logged opening line, trap, or refutation."""

    title: str
    entry_type: str
    pgn: str
    review_date: str
    notes: str = ""
    tags: str = ""
    fen: str = ""
    id: Optional[str] = None
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    )

    def __post_init__(self) -> None:
        if self.entry_type not in ENTRY_TYPES:
            raise ValueError(
                f"entry_type must be one of {ENTRY_TYPES}, got {self.entry_type!r}"
            )
        # Validate the review date is a real ISO date.
        date.fromisoformat(self.review_date)
        # Validate PGN parses and contains at least one move.
        if self.pgn.strip():
            import chess.pgn

            import io

            game = chess.pgn.read_game(io.StringIO(self.pgn))
            if game is None or list(game.mainline_moves()) == []:
                raise ValueError(f"PGN snippet did not parse: {self.pgn!r}")
        if self.id is None:
            self.id = self._generate_id()

    def _generate_id(self) -> str:
        import hashlib

        payload = f"{self.created_at}|{self.title}|{self.pgn}".encode("utf-8")
        return hashlib.sha1(payload).hexdigest()[:12]

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Entry":
        return cls(**data)


__all__ = ["Entry", "ENTRY_TYPES"]
