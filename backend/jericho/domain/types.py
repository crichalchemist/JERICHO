"""
Core domain types for Jericho 2.0.

All dataclasses are frozen (immutable) — state transitions produce new
instances rather than mutating in place.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Literal


# ── Enumerations ──────────────────────────────────────────────────────────────

class TaskStatus(str, Enum):
    """Lifecycle states for a Task.  See state_machine.py for valid transitions."""
    CREATED = "created"
    SCHEDULED = "scheduled"
    IN_WINDOW = "in_window"
    COMPLETED = "completed"
    MISSED = "missed"
    RESCHEDULED = "rescheduled"
    VIABILITY_PAUSE = "viability_pause"
    DECOMPOSED = "decomposed"
    DATE_EXTENDED = "date_extended"
    ARCHIVED = "archived"


class DependencyType(str, Enum):
    BLOCKING = "blocking"
    PREFERRED_ORDER = "preferred_order"
    PARALLEL_OK = "parallel_ok"


class MomentumSignal(str, Enum):
    HEAVY = "heavy"
    NEUTRAL = "neutral"
    LIGHT = "light"


# ── Value objects ─────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class CapacityVector:
    """Daily declared capacity, indexed Monday(0)–Sunday(6).

    Why length-7 tuple rather than dict: positional indexing allows direct
    arithmetic with day-of-week integers from Python's date.weekday().
    """
    values: tuple[float, ...]

    def __post_init__(self) -> None:
        if len(self.values) != 7:
            raise ValueError(
                f"CapacityVector must have exactly 7 values, got {len(self.values)}"
            )


@dataclass(frozen=True)
class Task:
    """Immutable snapshot of a task at a point in time."""
    id: str
    goal_id: str
    title: str
    status: TaskStatus
    task_type: Literal["decision", "research", "creative", "execution", "administrative"]
    importance_tier: Literal["hard_deadline", "routine", "flexible"]
    estimated_duration_minutes: int
    cognitive_load: float
    deferral_count: int
    dependencies: tuple[str, ...]   # IDs of tasks this one depends on
    scheduled_date: date | None = None
    deadline: date | None = None


@dataclass(frozen=True)
class Goal:
    """Immutable snapshot of a goal."""
    id: str
    instance_id: str
    title: str
    created_at: datetime


@dataclass(frozen=True)
class PlacementResult:
    """Output of the look-ahead feathering algorithm for a single task."""
    task_id: str
    scheduled_date: date | None
    load_ratio: float
    was_deferred: bool
