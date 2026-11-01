# Chess Opening Notebook CLI

A friendly, local-first command-line tool for chess players to log opening lines, traps, and refutations — complete with PGN snippets and review dates. Export your notebook to JSON or CSV whenever you like.

No accounts, no API keys, no network connection required. Everything lives on your machine in a single JSON file.

Built by [Asdale Dynamics, LLC](https://dylanasdale.github.io) — beginner-friendly AI education, books, and practical tools. Credit: Asdale Dynamics, LLC.

## Who this is for

This is one of the "fun extras" from Asdale Dynamics, LLC, the company founded by Dylan Asdale — a registered nurse turned AI author in Indiana. Dylan writes *The Massive AI Manual* and runs the hub site dylanasdale.github.io, explaining technology "like a friend would": plain English, step by step, never condescending.

If you're a chess player who wants a simple, private place to keep track of the openings you're studying, the traps you've spotted, and the refutations that shut them down, this tool is for you. It's designed to be approachable whether you're new to the command line or a longtime player.

## Install

You'll need Python 3.9 or newer.

```bash
# Get the code
git clone <this-repo>
cd chess-opening-notebook-cli

# Install the chess-notebook command
pip install -e .
```

This installs a `chess-notebook` command you can run from anywhere.

## Use it step by step

### 1. Add an opening line

```bash
chess-notebook add \
  --title "Ruy Lopez: Morphy Defense" \
  --type opening_line \
  --pgn "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7" \
  --review-date 2027-02-01 \
  --tags "open,spanish" \
  --notes "Study the main line variations"
```

### 2. Add a trap

```bash
chess-notebook add \
  --title "Legal Trap" \
  --type trap \
  --pgn "1. e4 e5 2. Nf3 Nc6 3. Bc4 Nf6 4. Ng5 d5 5. exd5 Nxd5 6. Nxf7" \
  --review-date 2027-03-01 \
  --notes "Queen and knight fork trap"
```

### 3. Add a refutation

```bash
chess-notebook add \
  --title "Refutation of the Trap" \
  --type refutation \
  --pgn "1. e4 e5 2. Nf3 Nc6 3. Bc4 Nf6 4. Ng5 d5 5. exd5 Nxd5 6. Nxf7?? Qh4+" \
  --review-date 2027-03-01 \
  --notes "...Qh4+ refutes the sacrifice"
```

Each entry gets a short id (like `a1b2c3d4e5f6`) that you can use to look it up later.

### 4. List your entries

```bash
# See everything
chess-notebook list

# Only traps
chess-notebook list --type trap

# Only entries due for review today or earlier
chess-notebook list --due
```

### 5. Show one entry in full

```bash
chess-notebook show --id a1b2c3d4e5f6
```

### 6. Review what's due

```bash
# Due on or before today
chess-notebook review

# Due on or before a specific date
chess-notebook review --as-of 2027-03-01
```

### 7. Export your notebook

```bash
chess-notebook export --format json --out notebook.json
chess-notebook export --format csv --out notebook.csv
```

Use `--db <path>` with any command if you'd rather store the notebook somewhere besides `./chess_notebook.json`.

## What's in an entry

| Field | What it means |
|-------|---------------|
| id | Short unique id (generated for you) |
| title | A name you give the entry |
| type | `opening_line`, `trap`, or `refutation` |
| pgn | The PGN move snippet |
| fen | Optional starting position |
| review_date | When you'd like to review this (YYYY-MM-DD) |
| notes | Free-form notes |
| tags | Comma-separated tags |
| created_at | When the entry was added |

PGN snippets are checked with [python-chess](https://pypi.org/project/chess/) when you add them, so typos are caught right away.

## Storage

Your notebook is a single local JSON file (default: `./chess_notebook.json`). Nothing is sent anywhere. Export to JSON or CSV whenever you want a backup or to open your data in a spreadsheet.

## Tests

```bash
pip install pytest
pytest
```

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC.

## About

Dylan Asdale is a registered nurse turned AI author and founder of Asdale Dynamics, LLC (Indiana, formed Oct 2026). His book *The Massive AI Manual* and hub site dylanasdale.github.io explain AI "like a friend would": plain English, step by step, never condescending. This chess tool is one of the LLC's fun extras — practical, local-first, beginner-friendly software.
