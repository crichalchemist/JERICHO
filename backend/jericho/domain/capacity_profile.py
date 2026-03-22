"""
Capacity profile engine — PRD §3.6.

Handles:
  - Cold-start multipliers for new users (weeks 1–3)
  - Exponential weighted average smoothing of observed capacity
  - Deriving updated CapacityVector from weekly completion signals
"""
from __future__ import annotations

from jericho.constants import (
    COLD_START_MULTIPLIERS,
    COLD_START_WEEK_COUNT,
    EWA_ALPHA,
)
from jericho.domain.types import CapacityVector, MomentumSignal


# ── Cold start ────────────────────────────────────────────────────────────────

def apply_cold_start(declared: float, week_number: int) -> float:
    """Scale declared capacity by the cold-start multiplier for the given week.

    Week numbers are 1-indexed.  Weeks beyond COLD_START_WEEK_COUNT are
    returned unmodified (multiplier = 1.0).
    """
    if week_number < 1 or week_number > COLD_START_WEEK_COUNT:
        return declared
    return declared * COLD_START_MULTIPLIERS[week_number - 1]


# ── EWA smoothing ─────────────────────────────────────────────────────────────

def compute_ewa(current: float, new_observation: float, alpha: float = EWA_ALPHA) -> float:
    """Exponential weighted average of a capacity value.

    alpha controls how quickly the estimate adapts to new observations.
    Higher alpha → faster adaptation, more volatility.
    """
    return alpha * new_observation + (1.0 - alpha) * current


# ── Derive updated capacity ───────────────────────────────────────────────────

# Momentum signal multipliers applied to the observed completion ratios
# before feeding into EWA.  Heavy week → user was overloaded; Light week
# → user had spare capacity.
_SIGNAL_SCALE: dict[MomentumSignal, float] = {
    MomentumSignal.HEAVY: 0.85,
    MomentumSignal.NEUTRAL: 1.0,
    MomentumSignal.LIGHT: 1.10,
}

_CAPACITY_MATCH_BONUS: float = 0.05


def derive_capacity_from_signal(
    current_vector: CapacityVector,
    completion_ratios: tuple[float, ...],
    momentum_signal: MomentumSignal,
    capacity_match: bool,
) -> CapacityVector:
    """Produce an updated CapacityVector from a week's observed completion data.

    Args:
        current_vector:    The stored CapacityVector before this update.
        completion_ratios: Observed completion ratio per day (length 7, 0.0–1.0).
        momentum_signal:   User's self-reported workload signal for the week.
        capacity_match:    True when the user confirmed the predicted capacity
                           matched their actual experience (adds small bonus).

    Returns:
        A new CapacityVector with each day updated via EWA.
    """
    if len(completion_ratios) != 7:
        raise ValueError(
            f"completion_ratios must have length 7, got {len(completion_ratios)}"
        )

    scale = _SIGNAL_SCALE[momentum_signal]
    bonus = _CAPACITY_MATCH_BONUS if capacity_match else 0.0

    new_values = tuple(
        compute_ewa(current, (observed * scale) + bonus)
        for current, observed in zip(current_vector.values, completion_ratios)
    )
    return CapacityVector(values=new_values)
