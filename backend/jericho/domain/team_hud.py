"""Stub port of src/core/team-hud.js."""
from typing import Any


def build_team_hud(session: dict[str, Any]) -> dict[str, Any]:
    return {"hud": [], "summary": None}


def build_team_export(session: dict[str, Any]) -> dict[str, Any]:
    return {"export": session, "format": "jericho-v1"}
