"""Command-line interface for the chess opening notebook."""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from .models import ENTRY_TYPES, Entry
from .storage import Storage


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chess-notebook",
        description="Log chess opening lines, traps, and refutations with PGN snippets and review dates.",
    )
    parser.add_argument(
        "--db",
        default=Storage.default_path(),
        help="Path to the local JSON notebook file (default: ./chess_notebook.json)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new opening line, trap, or refutation")
    p_add.add_argument("--title", required=True, help="Short title for the entry")
    p_add.add_argument(
        "--type",
        required=True,
        choices=list(ENTRY_TYPES),
        help="Type of entry",
    )
    p_add.add_argument("--pgn", required=True, help="PGN snippet text")
    p_add.add_argument(
        "--review-date",
        required=True,
        help="Review date in YYYY-MM-DD format",
    )
    p_add.add_argument("--notes", default="", help="Free-form notes")
    p_add.add_argument("--tags", default="", help="Comma-separated tags")
    p_add.add_argument("--fen", default="", help="Optional FEN position")
    p_add.set_defaults(func=_cmd_add)

    p_list = sub.add_parser("list", help="List logged entries")
    p_list.add_argument("--type", choices=list(ENTRY_TYPES), help="Filter by entry type")
    p_list.add_argument(
        "--due",
        action="store_true",
        help="Show only entries due for review on or before today",
    )
    p_list.set_defaults(func=_cmd_list)

    p_show = sub.add_parser("show", help="Show details of one entry")
    p_show.add_argument("--id", required=True, help="Entry id")
    p_show.set_defaults(func=_cmd_show)

    p_export = sub.add_parser("export", help="Export entries to JSON or CSV")
    p_export.add_argument(
        "--format",
        required=True,
        choices=["json", "csv"],
        help="Export format",
    )
    p_export.add_argument("--out", required=True, help="Output file path")
    p_export.set_defaults(func=_cmd_export)

    p_review = sub.add_parser("review", help="List entries due for review")
    p_review.add_argument(
        "--as-of",
        default=None,
        help="Review cutoff date YYYY-MM-DD (default: today)",
    )
    p_review.set_defaults(func=_cmd_review)

    return parser


def _cmd_add(args: argparse.Namespace, storage: Storage) -> int:
    entry = Entry(
        title=args.title,
        entry_type=args.type,
        pgn=args.pgn,
        review_date=args.review_date,
        notes=args.notes,
        tags=args.tags,
        fen=args.fen,
    )
    storage.add(entry)
    print(f"added {entry.id}  {entry.title} ({entry.entry_type})")
    return 0


def _cmd_list(args: argparse.Namespace, storage: Storage) -> int:
    entries = storage.list(entry_type=args.type, due_only=args.due)
    if not entries:
        print("(no entries)")
        return 0
    for e in entries:
        due = "DUE" if _is_due(e.review_date) else ""
        print(f"{e.id}  {e.review_date}  {e.entry_type:14s}  {e.title}  {due}")
    return 0


def _cmd_show(args: argparse.Namespace, storage: Storage) -> int:
    entry = storage.get(args.id)
    if entry is None:
        print(f"entry not found: {args.id}", file=sys.stderr)
        return 1
    print(f"id:        {entry.id}")
    print(f"title:     {entry.title}")
    print(f"type:      {entry.entry_type}")
    print(f"review:    {entry.review_date}")
    print(f"tags:      {entry.tags}")
    print(f"fen:       {entry.fen}")
    print(f"created:   {entry.created_at}")
    if entry.notes:
        print(f"notes:     {entry.notes}")
    print("pgn:")
    print(entry.pgn)
    return 0


def _cmd_export(args: argparse.Namespace, storage: Storage) -> int:
    if args.format == "json":
        storage.export_json(args.out)
    else:
        storage.export_csv(args.out)
    print(f"exported to {args.out}")
    return 0


def _cmd_review(args: argparse.Namespace, storage: Storage) -> int:
    entries = storage.list(due_only=True, as_of=args.as_of)
    if not entries:
        print("(nothing due for review)")
        return 0
    for e in entries:
        print(f"{e.review_date}  {e.id}  {e.entry_type:14s}  {e.title}")
    return 0


def _is_due(review_date: str) -> bool:
    from datetime import date

    return date.fromisoformat(review_date) <= date.today()


def main(argv: Optional[List[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    storage = Storage(args.db)
    return args.func(args, storage)


if __name__ == "__main__":
    raise SystemExit(main())
