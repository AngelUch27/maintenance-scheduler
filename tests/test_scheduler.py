from datetime import date

import pytest

from maintenance_scheduler import build_plan, load_equipment
from maintenance_scheduler.scheduler import Equipment, EquipmentError

TODAY = date(2026, 11, 13)


def test_example_plan_orders_overdue_first():
    plan = build_plan(load_equipment("examples/equipment.json"), TODAY)
    assert [(i.tag, i.status, i.days) for i in plan] == [("P-101", "OVERDUE", -11), ("C-220", "DUE", 0), ("T-305", "OK", 37)]


def test_hours_are_converted_with_daily_usage():
    eq = Equipment("X", "x", date(2026, 1, 1), 100, "hours", hours_per_day=8)
    assert eq.interval_days() == 12  # 100 h / 8 h per day = 12.5 -> 12


def test_warn_window_controls_due_status():
    eq = Equipment("X", "x", date(2026, 11, 1), 20, "days")  # due 2026-11-21, in 8 days
    assert build_plan([eq], TODAY, warn_days=7)[0].status == "OK"
    assert build_plan([eq], TODAY, warn_days=10)[0].status == "DUE"


@pytest.mark.parametrize("bad", [
    {"tag": "A", "name": "a", "last_service": "2026-01-01", "interval": 10},             # no unit
    {"tag": "A", "name": "a", "last_service": "2026-13-01", "interval": 10, "unit": "days"},
    {"tag": "A", "name": "a", "last_service": "2026-01-01", "interval": -5, "unit": "days"},
    {"tag": "A", "name": "a", "last_service": "2026-01-01", "interval": 10, "unit": "hours"},  # no hours_per_day
])
def test_invalid_items_are_rejected_with_the_tag(bad, tmp_path):
    f = tmp_path / "e.json"
    f.write_text(__import__("json").dumps([bad]), encoding="utf-8")
    with pytest.raises(EquipmentError) as info:
        build_plan(load_equipment(f), TODAY)
    assert "A:" in str(info.value)
