"""Stub port of src/core/ai-interpreter.js."""
from typing import Any


def interpret_command(
    command: dict[str, Any],
    state: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Interpret a command against state. Returns (next_state, effects)."""
    cmd = command.get("command", "")
    if cmd == "reset":
        return {**state, "tasks": [], "history": []}, [{"type": "reset", "applied": True}]
    raise ValueError(f"Unknown command: {cmd!r}")
