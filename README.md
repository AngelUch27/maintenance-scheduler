# maintenance-scheduler

A small Python CLI that turns an equipment list into a dated maintenance plan.
Give it the equipment, the last service date and the interval, and it tells you
what is due, what is overdue and when the next service falls.

```bash
python -m maintenance_scheduler examples/equipment.json --today 2026-11-13
```

```
OVERDUE  P-101  Coolant pump          due 2026-11-02  (11 days late)   every 400 h
DUE      C-220  Air compressor        due 2026-11-13  (today)          every 90 days
OK       T-305  Cooling tower fan     due 2026-12-20  (in 37 days)     every 180 days
```

## Features

- Intervals in **days** or **operating hours** (hours are converted with the
  equipment's daily usage).
- Three states: `OK`, `DUE` (within the warning window, default 7 days) and
  `OVERDUE`.
- `--json` output for other tools, `--warn-days` to change the window.
- No dependencies beyond the Python standard library (3.10+).

## Install and test

```bash
git clone https://github.com/AngelUch27/maintenance-scheduler.git
cd maintenance-scheduler
python -m pytest -q
```

## Documentation

- [Equipment file format](docs/equipment-format.md)
- [Command line usage](docs/cli.md)
- [How due dates are computed](docs/scheduling-rules.md)

## License

MIT
