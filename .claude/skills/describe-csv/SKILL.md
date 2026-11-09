---
name: describe-csv
description: Print the column data types, per-column non-null counts, and basic stats (min, max, mean for numeric columns) of a CSV file. Use when the user asks to describe, inspect, or show the structure, columns, or dtypes of a CSV. Read-only; does no cleaning.
user-invocable: true
allowed-tools: Bash(poetry run python .claude/skills/describe-csv/scripts/describe_csv.py:*)
argument-hint: "<path to a CSV>"
---

# describe-csv

Prints each column's data type, non-null count and, for numeric columns, min, max and mean for a CSV file by running a bundled script.

## Steps

1. Get the CSV path from the user's request. **If no file was given, reply with an error saying that no file was provided and stop.** Do not guess a file or search for one.
2. Run the script from the project root:

   ```
   poetry run python .claude/skills/describe-csv/scripts/describe_csv.py "<path/to/file.csv>"
   ```

3. Show the script's output to the user as-is. If it prints an error (file not found, empty, unreadable), relay that error.

## Rules
- Read-only: never modify the CSV, never write anything to disk (no output files, no temp copies).

### Must do:
- Always use `poetry run python`, never bare `python`.
- Make sure the CSV path is quoted to handle spaces and special characters.

### Must not do:
- No cleaning, no interpretation, no analysis beyond the basic stats the script prints.
- Do not create any additional file, all information should be printed in the console/terminal.