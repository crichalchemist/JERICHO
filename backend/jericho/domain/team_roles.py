"""Stub port of src/core/team-roles.js."""
from typing import Any


def filter_session_for_viewer(
    session: dict[str, Any],
    viewer_id: str | None,
    team_roles: Any,
    context: str,
) -> dict[str, Any]:
    return session
