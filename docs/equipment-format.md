# Equipment file format

The scheduler reads a JSON array. Each item describes one piece of equipment:

| Field | Type | Required | Meaning |
|---|---|---|---|
| `tag` | string | yes | Unique equipment tag, e.g. `P-101` |
| `name` | string | yes | Human-readable name |
| `last_service` | `YYYY-MM-DD` | yes | Date of the last completed service |
| `interval` | number | yes | Service interval |
| `unit` | `"days"` or `"hours"` | yes | Unit of `interval` |
| `hours_per_day` | number | only for `hours` | Average operating hours per day, used to convert hours to days |

Example:

```json
[
  {"tag": "P-101", "name": "Coolant pump", "last_service": "2026-10-16",
   "interval": 400, "unit": "hours", "hours_per_day": 24},
  {"tag": "C-220", "name": "Air compressor", "last_service": "2026-08-15",
   "interval": 90, "unit": "days"}
]
```

Validation errors (missing field, unknown unit, bad date) stop the run with a
message that names the offending tag.
