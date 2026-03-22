"""
Task lifecycle state machine — PRD §3.2.

Transitions are represented as a frozenset of (from, to) pairs so membership
tests are O(1).  The `transition()` function is pure: it returns a new Task
and calls an injected `ledger_writer` side-effect only on success.
"""
from __future__ import annotations

from dataclasses import replace
from typing import Callable

from jericho.domain.types import Task, TaskStatus

S = TaskStatus


class InvalidTransitionError(ValueError):
    """Raised when a requested state transition is not permitted."""

    def __init__(self, from_status: TaskStatus, to_status: TaskStatus) -> None:
        super().__init__(
            f"Invalid transition: {from_status.value!r} → {to_status.value!r}"
        )
        self.from_status = from_status
        self.to_status = to_status


# ── Allowed transitions ───────────────────────────────────────────────────────

VALID_TRANSITIONS: frozenset[tuple[TaskStatus, TaskStatus]] = frozenset(
    {
        # Normal forward flow
        (S.CREATED, S.SCHEDULED),
        (S.SCHEDULED, S.IN_WINDOW),
        (S.IN_WINDOW, S.COMPLETED),
        (S.IN_WINDOW, S.MISSED),
        # Rescheduling
        (S.MISSED, S.RESCHEDULED),
        (S.SCHEDULED, S.RESCHEDULED),
        (S.RESCHEDULED, S.SCHEDULED),
        (S.RESCHEDULED, S.IN_WINDOW),
        # Viability pause
        (S.SCHEDULED, S.VIABILITY_PAUSE),
        (S.IN_WINDOW, S.VIABILITY_PAUSE),
        (S.RESCHEDULED, S.VIABILITY_PAUSE),
        (S.VIABILITY_PAUSE, S.SCHEDULED),
        (S.VIABILITY_PAUSE, S.DECOMPOSED),
        (S.VIABILITY_PAUSE, S.DATE_EXTENDED),
        (S.VIABILITY_PAUSE, S.ARCHIVED),
        # Date extension
        (S.SCHEDULED, S.DATE_EXTENDED),
        (S.DATE_EXTENDED, S.SCHEDULED),
        # Decomposition
        (S.SCHEDULED, S.DECOMPOSED),
        # Terminal: only ARCHIVED is truly terminal — completed/missed can still be read
        (S.COMPLETED, S.ARCHIVED),
        (S.MISSED, S.ARCHIVED),
        (S.DECOMPOSED, S.ARCHIVED),
    }
)


# ── Pure transition function ──────────────────────────────────────────────────

def transition(
    task: Task,
    to_status: TaskStatus,
    ledger_writer: Callable[[Task, TaskStatus], None],
) -> Task:
    """Apply a status transition, returning the updated Task.

    Args:
        task:           The current immutable Task snapshot.
        to_status:      The desired new status.
        ledger_writer:  Side-effect called with (task, to_status) *after* the
                        transition is validated.  Typically writes a Decision
                        Ledger row; use a no-op lambda in tests.

    Raises:
        InvalidTransitionError: When the (from, to) pair is not in
                                VALID_TRANSITIONS.
    """
    if (task.status, to_status) not in VALID_TRANSITIONS:
        raise InvalidTransitionError(task.status, to_status)

    updated = replace(task, status=to_status)
    ledger_writer(task, to_status)
    return updated
