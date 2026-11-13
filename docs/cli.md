# Command line usage

```
python -m maintenance_scheduler EQUIPMENT_FILE [--today YYYY-MM-DD] [--warn-days N] [--json]
```

| Option | Default | Effect |
|---|---|---|
| `--today` | the current date | Reference date for the computation; useful for tests and reports |
| `--warn-days` | `7` | Items due within this many days are reported as `DUE` |
| `--json` | off | Print a JSON array instead of the table |

Exit codes: `0` when nothing is overdue, `1` when at least one item is overdue,
`2` on invalid input. This makes the tool usable in a cron job or a CI check.

## JSON output

```json
[
  {"tag": "P-101", "name": "Coolant pump", "status": "OVERDUE",
   "due": "2026-11-02", "days": -11, "interval": "every 400 h"}
]
```

`days` is the number of days until the due date (negative when overdue).
