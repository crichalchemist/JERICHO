"""Stub port of src/core/narrative-compiler.js. Phase 1: LLM-generated."""
from typing import Any


def compile_narrative(state: dict[str, Any], pipeline_result: dict[str, Any]) -> dict[str, Any]:
    goal = pipeline_result.get("goal")
    integrity = (pipeline_result.get("integrity") or {}).get("score", 0)
    return {
        "headline": f"Working toward: {goal.get('outcome', 'your goal') if goal else 'your goal'}",
        "integrityNote": f"Integrity score: {integrity}/100",
        "tasks": pipeline_result.get("tasks") or [],
    }
