"""Stub port of src/core/scene-compiler.js. Phase 1: full port."""
from typing import Any


def compile_scene_graph(pipeline_result: dict[str, Any]) -> dict[str, Any]:
    """Build a scene graph from pipeline output. Stub for Phase 0."""
    return {
        "nodes": [],
        "edges": [],
        "goal": pipeline_result.get("goal"),
        "integrityScore": (pipeline_result.get("integrity") or {}).get("score", 0),
        "taskCount": len(pipeline_result.get("tasks") or []),
    }
