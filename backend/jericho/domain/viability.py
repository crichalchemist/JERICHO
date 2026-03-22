"""
Viability engine — PRD §3.2.

Determines whether a task's scheduled load is sustainable and whether
a Viability Pause should be triggered.
"""
from __future__ import annotations

from typing import Literal

from jericho.constants import (
    OVERLOADED_THRESHOLD,
    VIABLE_THRESHOLD,
    VIABILITY_PAUSE_DEADLINE_DAYS,
    VIABILITY_PAUSE_DEADLINE_DEFERRAL,
    VIABILITY_PAUSE_DEFERRAL_HIGH,
    VIABILITY_PAUSE_DEFERRAL_LOW,
)
from jericho.domain.types import Task


def compute_load_ratio(daily_load: float, capacity: float) -> float:
    if capacity <= 0:
        return float("inf")
    return daily_load / capacity


ViabilityLabel = Literal["viable", "overloaded", "infeasible"]


def check_viability(load_ratio: float) -> ViabilityLabel:
    """Classify a load ratio per PRD §3.2 thresholds."""
    if load_ratio > OVERLOADED_THRESHOLD:
        return "infeasible"
    if load_ratio >= VIABLE_THRESHOLD:
        return "overloaded"
    return "viable"


UrgencyLevel = Literal["low", "high"]


def should_trigger_viability_pause(
    task: Task,
    deadline_within_days: int | None,
) -> tuple[bool, UrgencyLevel] | tuple[Literal[False], None]:
    """Return (True, urgency) when a pause is warranted, (False, None) otherwise.

    Rule priority (PRD §3.2):
      1. ≥ DEFERRAL_HIGH deferrals           → high (beats all other rules)
      2. ≥ DEADLINE_DEFERRAL + deadline ≤ 7d → high
      3. ≥ DEFERRAL_LOW + no deadline        → low
    """
    d = task.deferral_count

    if d >= VIABILITY_PAUSE_DEFERRAL_HIGH:
        return (True, "high")

    if (
        d >= VIABILITY_PAUSE_DEADLINE_DEFERRAL
        and deadline_within_days is not None
        and deadline_within_days <= VIABILITY_PAUSE_DEADLINE_DAYS
    ):
        return (True, "high")

    if d >= VIABILITY_PAUSE_DEFERRAL_LOW and task.deadline is None:
        return (True, "low")

    return (False, None)
