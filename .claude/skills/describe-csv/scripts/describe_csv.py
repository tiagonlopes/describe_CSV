"""Print column data types, non-null counts and basic stats of a CSV file.

Basic stats (min, max, mean) are shown only for numeric columns, where they
make sense. Read-only: the file is opened for reading only. Nothing is
written to disk, and no cleaning is performed.

Usage:
    poetry run python describe_csv.py <path/to/file.csv>
"""

import sys
from pathlib import Path

import pandas as pd
from pandas.api.types import is_bool_dtype, is_numeric_dtype

NA = "-"


def _fmt(value: float) -> str:
    """Format a number compactly."""
    return f"{value:,.2f}".rstrip("0").rstrip(".") if isinstance(value, float) else str(value)


def column_stats(series: pd.Series) -> tuple[str, str, str]:
    """Return (min, max, mean) as text; '-' when not meaningful."""
    if is_numeric_dtype(series) and not is_bool_dtype(series) and series.count():
        return _fmt(series.min()), _fmt(series.max()), _fmt(float(series.mean()))
    return NA, NA, NA


def describe_csv(path: str) -> str:
    """Return a text table with dtype, non-null count and stats per column."""
    df = pd.read_csv(path, sep=None, engine="python")  # sniff delimiter
    header = ("Column", "Type", "Count", "Min", "Max", "Mean")
    rows = [
        (str(col), str(df[col].dtype), str(int(df[col].count())),
         *column_stats(df[col]))
        for col in df.columns
    ]
    widths = [max(len(r[i]) for r in [header, *rows]) for i in range(len(header))]

    def line(cells: tuple[str, ...]) -> str:
        return "  ".join(c.ljust(w) for c, w in zip(cells, widths)).rstrip()

    out = [
        f"File: {path}",
        f"Rows: {len(df)}  Columns: {len(df.columns)}",
        "",
        line(header),
        line(tuple("-" * w for w in widths)),
        *[line(r) for r in rows],
        "",
        "Count = non-null values. Min/Max/Mean shown for numeric columns only.",
    ]
    return "\n".join(out)


def main(argv: list[str]) -> int:
    if len(argv) < 2 or not argv[1].strip():
        print("Error: no file was provided. Usage: describe_csv.py <file.csv>",
              file=sys.stderr)
        return 1
    path = argv[1]
    if not Path(path).is_file():
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 1
    try:
        print(describe_csv(path))
    except pd.errors.EmptyDataError:
        print(f"Error: file is empty: {path}", file=sys.stderr)
        return 1
    except Exception as exc:  # unreadable / malformed CSV
        print(f"Error: could not read CSV ({exc})", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
