# STATUS

## What was built
A local-first Python CLI, `chess-notebook`, for chess players to log opening lines, traps, and refutations with PGN snippets and review dates.

Package `chess_notebook/`:
- `models.py` — `Entry` dataclass (id, title, entry_type, pgn, fen, review_date, notes, tags, created_at). PGN validated with python-chess (must contain at least one move); entry_type restricted to opening_line/trap/refutation; review_date validated as ISO date.
- `storage.py` — `Storage` backed by a single local JSON file. `add`, `get`, `list` (filter by type, due-for-review), `export_json`, `export_csv`. Atomic writes via tmp + os.replace.
- `cli.py` — argparse subcommands: `add`, `list`, `show`, `export` (json/csv), `review`. Global `--db` option (default `./chess_notebook.json`).
- `pyproject.toml` — setuptools build, console script `chess-notebook = chess_notebook.cli:main`, pytest config.
- `tests/test_notebook.py` — 9 tests covering models validation, storage add/list/export, and CLI add/list/export.

Supporting files:
- `README.md` — install, usage examples for all subcommands, data model, tests, license, about Asdale Dynamics, LLC.
- `LICENSE` — MIT, copyright line exactly `Copyright (c) 2026 Asdale Dynamics, LLC`.

## How to run it
```bash
cd /workspace/kilo-lab/chess-opening-notebook-cli
pip install -e .          # installs the chess-notebook command
chess-notebook add --title "Ruy Lopez" --type opening_line \
  --pgn "1. e4 e5 2. Nf3 Nc6 3. Bb5" --review-date 2027-02-01
chess-notebook list
chess-notebook list --due
chess-notebook show --id <id>
chess-notebook review --as-of 2027-02-01
chess-notebook export --format json --out notebook.json
chess-notebook export --format csv --out notebook.csv
pytest                    # run the test suite
```

## Verification results
- `pip install -e .` — success.
- `pytest` — 9 passed.
- CLI smoke test — add/list/review/export (json) all succeed; PGN validation rejects invalid snippets; invalid entry_type and review_date raise ValueError.
- `LICENSE` line 3: `Copyright (c) 2026 Asdale Dynamics, LLC` (exact).
- `README.md` credits Asdale Dynamics, LLC (lines 5, 98, 102).

## Known gaps
- No GUI/web interface; CLI only.
- Storage is a single JSON file (no concurrent-write locking beyond atomic replace).
- Review due-check uses the system local date.
- No search/filter by tags or notes text (tags are stored but not queryable).
- Not published to PyPI (per instructions, never publish).
