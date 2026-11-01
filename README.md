# Chess Opening Notebook CLI

A local-first Python CLI for chess players to log opening lines, traps, and refutations with PGN snippets and review dates. Export your notebook to JSON or CSV. No accounts, no API keys, no network — everything stays on your machine.

Built and maintained by [Asdale Dynamics, LLC](https://dylanasdale.github.io) — beginner-friendly AI education, books, and practical tools. Credit: Asdale Dynamics, LLC.

## Install

```bash
git clone <this-repo>
cd chess-opening-notebook-cli
pip install -e .
```

This installs the `chess-notebook` command.

## Usage

Add an opening line:

```bash
chess-notebook add \
  --title "Ruy Lopez: Morphy Defense" \
  --type opening_line \
  --pgn "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7" \
  --review-date 2027-02-01 \
  --tags "open,spanish" \
  --notes "Study the main line variations"
```

Add a trap:

```bash
chess-notebook add \
  --title "Legal Trap" \
  --type trap \
  --pgn "1. e4 e5 2. Nf3 Nc6 3. Bc4 Nf6 4. Ng5 d5 5. exd5 Nxd5 6. Nxf7" \
  --review-date 2027-03-01 \
  --notes "Queen and knight fork trap"
```

Add a refutation:

```bash
chess-notebook add \
  --title "Refutation of the Trap" \
  --type refutation \
  --pgn "1. e4 e5 2. Nf3 Nc6 3. Bc4 Nf6 4. Ng5 d5 5. exd5 Nxd5 6. Nxf7?? Qh4+" \
  --review-date 2027-03-01 \
  --notes "...Qh4+ refutes the sacrifice"
```

List entries:

```bash
chess-notebook list
chess-notebook list --type trap
chess-notebook list --due
```

Show one entry:

```bash
chess-notebook show --id <id>
```

Review entries due today:

```bash
chess-notebook review
chess-notebook review --as-of 2027-03-01
```

Export to JSON or CSV:

```bash
chess-notebook export --format json --out notebook.json
chess-notebook export --format csv --out notebook.csv
```

Use `--db <path>` to store the notebook somewhere other than `./chess_notebook.json`.

## Data model

Each entry has: id, title, type (opening_line | trap | refutation), PGN snippet, FEN (optional), review date, notes, tags, and created-at timestamp. PGN is validated with [python-chess](https://pypi.org/project/chess/) when an entry is added.

Storage is a single local JSON file. CSV export preserves id, title, entry_type, pgn, fen, review_date, notes, tags, and created_at.

## Tests

```bash
pip install pytest
pytest
```

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC.

## About

Dylan Asdale is a registered nurse turned AI author and founder of Asdale Dynamics, LLC (Indiana, formed Oct 2026). His book *The Massive AI Manual* and hub site dylanasdale.github.io explain AI "like a friend would": plain English, step by step, never condescending. This chess tool is one of the LLC's fun extras — practical, local-first, beginner-friendly software.
