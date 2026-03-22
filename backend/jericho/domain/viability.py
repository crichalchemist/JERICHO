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


# ── Load ratio ────────────────────────────────────────────────────────────────

def compute_load_ratio(daily_load: float, capacity: float) -> float:
    """Ratio of scheduled load to available capacity for a given day.

    Capacity of 0 is treated as effectively zero-capacity (returns inf-equivalent
    1e9) so downstream checks always land in the "overloaded" branch.
    """
    if capacity <= 0:
        return float("inf")
    return daily_load / capacity


# ── Viability classification ──────────────────────────────────────────────────

ViabilityLabel = Literal["viable", "overloaded", "infeasible"]


def check_viability(load_ratio: float) -> ViabilityLabel:
    """Classify a load ratio into a viability label.

    Boundaries (from constants, matching PRD §3.2):
      0.0 – 0.75  → viable
      0.75 – 1.0  → overloaded   (degraded but schedulable)
      > 1.0       → infeasible
    """
    if load_ratio > OVERLOADED_THRESHOLD:
        return "infeasible"
    if load_ratio >= VIABLE_THRESHOLD:
        return "overloaded"
    return "viable"


# ── Viability Pause triggers ──────────────────────────────────────────────────

UrgencyLevel = Literal["low", "high"]


def should_trigger_viability_pause(
    task: Task,
    deadline_within_days: int | None,
) -> tuple[bool, UrgencyLevel] | tuple[Literal[False], None]:
    """Determine whether a Viability Pause should be triggered for a task.

    Returns (True, urgency) when a pause is warranted, (False, None) otherwise.

    Rules (PRD §3.2):
      - ≥ VIABILITY_PAUSE_DEFERRAL_HIGH deferrals                 → high urgency + decompose offer
      - ≥ VIABILITY_PAUSE_DEADLINE_DEFERRAL deferrals
        + deadline within VIABILITY_PAUSE_DEADLINE_DAYS           → high urgency
      - ≥ VIABILITY_PAUSE_DEFERRAL_LOW deferrals + no deadline    → low urgency
    """
    d = task.deferral_count

    # Highest-priority check first so it takes precedence over the deadline rule
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
