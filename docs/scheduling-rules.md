# How due dates are computed

1. The interval is converted to days. A `days` interval is used as-is; an
   `hours` interval is divided by `hours_per_day` and rounded to the nearest
   whole day (minimum one day).
2. `due = last_service + interval_days`.
3. `days = due - today`.
4. Status:
   - `OVERDUE` when `days < 0`
   - `DUE` when `0 <= days <= warn_days`
   - `OK` otherwise

The report is sorted so that `OVERDUE` items come first (most overdue at the
top), then `DUE`, then `OK` by due date.
