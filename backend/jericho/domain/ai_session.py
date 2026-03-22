"""Stub port of src/core/ai-session.js."""
import uuid
from typing import Any


def build_session_snapshot(**kwargs: Any) -> dict[str, Any]:
    return {
        "id": str(uuid.uuid4()),
        "goal": (kwargs.get("pipeline_output") or {}).get("goal"),
        "integrity": ((kwargs.get("pipeline_output") or {}).get("integrity") or {}).get("score", 0),
        "tasks": (kwargs.get("pipeline_output") or {}).get("tasks") or [],
        "narrative": kwargs.get("narrative"),
        "directives": kwargs.get("directives"),
        "teamRoles": {},
    }
