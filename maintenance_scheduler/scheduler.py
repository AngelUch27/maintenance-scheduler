from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
import json
from pathlib import Path


class EquipmentError(ValueError):
    pass


@dataclass(frozen=True)
class Equipment:
    tag: str
    name: str
    last_service: date
    interval: float
    unit: str  # "days" | "hours"
    hours_per_day: float | None = None

    def interval_days(self) -> int:
        if self.unit == "days":
            return max(1, round(self.interval))
        if not self.hours_per_day or self.hours_per_day <= 0:
            raise EquipmentError(f"{self.tag}: hours_per_day is required for hour intervals")
        return max(1, round(self.interval / self.hours_per_day))

    def interval_label(self) -> str:
        return f"every {self.interval:g} h" if self.unit == "hours" else f"every {self.interval:g} days"


@dataclass(frozen=True)
class PlanItem:
    tag: str
    name: str
    status: str
    due: date
    days: int
    interval: str

    def to_dict(self) -> dict:
        return {"tag": self.tag, "name": self.name, "status": self.status, "due": self.due.isoformat(), "days": self.days, "interval": self.interval}


def _parse_item(raw: dict) -> Equipment:
    tag = str(raw.get("tag") or "?")
    for field in ("tag", "name", "last_service", "interval", "unit"):
        if field not in raw:
            raise EquipmentError(f"{tag}: missing field '{field}'")
    if raw["unit"] not in ("days", "hours"):
        raise EquipmentError(f"{tag}: unit must be 'days' or 'hours'")
    try:
        last = date.fromisoformat(str(raw["last_service"]))
    except ValueError as exc:
        raise EquipmentError(f"{tag}: last_service must be YYYY-MM-DD") from exc
    try:
        interval = float(raw["interval"])
    except (TypeError, ValueError) as exc:
        raise EquipmentError(f"{tag}: interval must be a number") from exc
    if interval <= 0:
        raise EquipmentError(f"{tag}: interval must be positive")
    hpd = raw.get("hours_per_day")
    return Equipment(tag, str(raw["name"]), last, interval, raw["unit"], float(hpd) if hpd is not None else None)


def load_equipment(path: str | Path) -> list[Equipment]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise EquipmentError("the equipment file must contain a JSON array")
    return [_parse_item(item) for item in data]


def build_plan(equipment: list[Equipment], today: date, warn_days: int = 7) -> list[PlanItem]:
    items = []
    for eq in equipment:
        due = eq.last_service + timedelta(days=eq.interval_days())
        days = (due - today).days
        status = "OVERDUE" if days < 0 else "DUE" if days <= warn_days else "OK"
        items.append(PlanItem(eq.tag, eq.name, status, due, days, eq.interval_label()))
    order = {"OVERDUE": 0, "DUE": 1, "OK": 2}
    return sorted(items, key=lambda i: (order[i.status], i.days))


def format_table(plan: list[PlanItem]) -> str:
    lines = []
    for item in plan:
        when = "(today)" if item.days == 0 else f"({-item.days} days late)" if item.days < 0 else f"(in {item.days} days)"
        lines.append(f"{item.status:8s} {item.tag:6s} {item.name:22s} due {item.due}  {when:16s} {item.interval}")
    return "\n".join(lines)
