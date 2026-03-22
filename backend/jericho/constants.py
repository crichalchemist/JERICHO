"""
Named constants for the Jericho domain.
No magic numbers anywhere in the codebase — everything lives here.
"""

# ── Viability thresholds (PRD §3.2) ─────────────────────────────────────────
VIABLE_THRESHOLD: float = 0.75
OVERLOADED_THRESHOLD: float = 1.0

# ── Capacity profile (PRD §3.6) ─────────────────────────────────────────────
# Cold-start multipliers for weeks 1–3 (index 0 = week 1)
COLD_START_MULTIPLIERS: tuple[float, ...] = (0.60, 0.75, 1.0)
COLD_START_WEEK_COUNT: int = len(COLD_START_MULTIPLIERS)

# Exponential weighted average smoothing factor
EWA_ALPHA: float = 0.3

# ── Look-ahead engine (PRD §3.4) ─────────────────────────────────────────────
LOOK_AHEAD_DEFAULT_DAYS: int = 7
LOOK_AHEAD_MAX_EXTENSION_DAYS: int = 14
ANCHOR_EVENT_CAPACITY_BUFFER: float = 0.20

# ── Cognitive load (PRD §3.3) ────────────────────────────────────────────────
USER_OVERRIDE_LOAD_BONUS: float = 0.2

# Duration buckets → multipliers
DURATION_MULTIPLIERS: dict[str, float] = {
    "lte_30": 1.0,
    "31_to_60": 1.2,
    "61_to_90": 1.5,
    "gt_90": 1.8,
}

# Dependency position → multipliers
DEPENDENCY_POSITION_WEIGHTS: dict[str, float] = {
    "no_dependents": 1.0,
    "one_to_two": 1.25,
    "three_plus": 1.5,
}

# ── Viability pause triggers (PRD §3.2) ──────────────────────────────────────
VIABILITY_PAUSE_DEFERRAL_LOW: int = 3     # + no deadline → low urgency
VIABILITY_PAUSE_DEFERRAL_HIGH: int = 5    # regardless → high urgency + decompose offer
VIABILITY_PAUSE_DEADLINE_DAYS: int = 7    # ≥2 deferrals + deadline ≤7d → high urgency
VIABILITY_PAUSE_DEADLINE_DEFERRAL: int = 2

# ── Scoring (v1 integrity engine, preserved for migration bridge) ─────────────
DIFFICULTY_WEIGHTS: dict[int, float] = {1: 0.8, 2: 1.0, 3: 1.2}
LATE_COMPLETION_PENALTY: float = 0.7

# ── Weekly rhythms (PRD §3.7) ────────────────────────────────────────────────
TONE_BRANCH_MOMENTUM_THRESHOLD: float = 0.70
TONE_BRANCH_RECALIBRATION_THRESHOLD: float = 0.40

# ── Accountability tokens ────────────────────────────────────────────────────
ACCOUNTABILITY_TOKEN_BYTES: int = 48   # produces 64-char URL-safe string
ACCOUNTABILITY_EVENT_RETENTION_DAYS: int = 30  # viewer-side soft-delete TTL

# ── Model registry drift detection (OQ-08) ──────────────────────────────────
REGISTRY_DRIFT_LATENCY_THRESHOLD: float = 0.20  # 20% divergence
REGISTRY_DRIFT_MIN_SAMPLES: int = 50

# ── API / server ─────────────────────────────────────────────────────────────
DEFAULT_PORT: int = 8000
CORS_ALLOW_ORIGINS: tuple[str, ...] = ("http://localhost:5173",)
