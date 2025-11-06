# NHL Goal Drought Checker

This Python script evaluates NHL players for goal droughts by analyzing the most recent games of the top goal scorers in a given season. It generates JSON and CSV outputs containing players who are currently "due" for goals.

---

## Features

- Fetches NHL player stats via the NHL API.
- Sorts players by goals scored in a season.
- Checks for goal droughts over the last N games.
- Outputs:
  - `players_due.json` → Players currently in a goal drought.
  - `players_sanity_check.json` → Full stats for the top players evaluated.
  - `name_output.csv` → Names of players currently in a goal drought.

---

## Requirements

- Python 3.7+
- Modules:
  - `requests`
  - `csv`
  - `json`
  - `argparse`
  - `os`
  - `datetime`

Install dependencies (if needed):

```bash
pip install requests
```

---

## Usage

Run the script from the command line:

```bash
python nhl_goal_drought.py --season <SEASON_ID> --dt <DROUGHT_THRESHOLD> --playerLimit <TOP_PLAYERS>
```

### Arguments

| Argument         | Type  | Default | Description |
|-----------------|-------|---------|-------------|
| `--season`       | int   | 20252026| NHL season to evaluate (e.g., `20252026`) |
| `--dt`           | int   | 2       | Number of consecutive games without a goal to count as a drought |
| `--playerLimit`  | int   | 50      | Maximum number of top scorers to check |

### Example

```bash
python nhl_goal_drought.py --season 20252026 --dt 3 --playerLimit 100
```

This checks the top 100 goal scorers for a 3-game goal drought in the 2025-2026 season.

---

## Output

All outputs are stored in:

```
results/season/<season>/<YYYY-MM-DD>/
```

- `players_due.json` → JSON list of players currently in a goal drought.
- `players_sanity_check.json` → JSON with full stats for sanity checking.
- `name_output.csv` → CSV list of player names in a goal drought.

---

## Notes

- The script uses NHL’s official API endpoints.
- Make sure your internet connection is active as it fetches live data.
- JSON files include detailed stats for further analysis.
- Customize the `playerLimit` and `drought_threshold` to adjust evaluation scope.

---

## License

This project is provided as-is for educational or personal use.

