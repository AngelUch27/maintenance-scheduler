import argparse
from datetime import date
import json
import sys

from .scheduler import EquipmentError, build_plan, format_table, load_equipment


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="maintenance_scheduler", description="Dated maintenance plan from an equipment list.")
    parser.add_argument("equipment_file")
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    parser.add_argument("--warn-days", type=int, default=7)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        plan = build_plan(load_equipment(args.equipment_file), args.today, args.warn_days)
    except (EquipmentError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps([i.to_dict() for i in plan], indent=2) if args.json else format_table(plan))
    return 1 if any(i.status == "OVERDUE" for i in plan) else 0


if __name__ == "__main__":
    sys.exit(main())
