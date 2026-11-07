# describe-csv

A Claude Code skill that describes the structure of any CSV file. It prints each column's data type, its non-null count and, for numeric columns, the min, max and mean.

The skill is **read-only**. It does not clean or change the CSV and writes nothing to disk.

## Example

```
Column      Type   Count  Min    Max    Mean
----------  -----  -----  -----  -----  ---------
trial_id    int64  2073   1      2073   1,037
user_id     int64  2073   27046  31165  29,075.58
started_at  str    2073   -      -      -
outcome     str    1655   -      -      -
```

Min, max and mean show `-` for non-numeric columns.

## Setup

Requirements: Python 3.11+ and [Poetry](https://python-poetry.org/).

```
poetry install
```

## Usage

In Claude Code, from the project root:

```
/describe-csv path/to/file.csv
```

If no file is given, the skill replies with an error saying that no file was provided.

You can also run the script directly:

```
poetry run python .claude/skills/describe-csv/scripts/describe_csv.py path/to/file.csv
```

## How it works

1. The skill takes the CSV path from the request, and stops with an error if there is none.
2. It runs `scripts/describe_csv.py` with `poetry run python`.
3. The script reads the file with pandas, detecting the delimiter, and prints the table.
4. Errors (missing, empty or unreadable file) are shown as clear messages.

## Project structure

```
.claude/skills/describe-csv/
├── SKILL.md              # skill definition and rules
└── scripts/describe_csv.py   # the tool the skill runs
AGENTS.md                 # project conventions for agents
```
