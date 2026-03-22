from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from jericho.db.json_adapter import safe_read_state, write_state

router = APIRouter(tags=["goals"])


class GoalPayload(BaseModel):
    text: str | None = None
    goal: str | None = None
    goalText: str | None = None


@router.post("/goals")
async def add_goal(payload: GoalPayload) -> JSONResponse:
    text = payload.text or payload.goal or payload.goalText
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail={"error": "INVALID_GOAL", "message": "Goal text is required."})

    text = text.strip()

    # Phase 1: replace with LLM-based goal validation
    if len(text) < 5:
        raise HTTPException(
            status_code=400,
            detail={"error": "INVALID_DEFINITE_GOAL", "message": "Goal must be specific, measurable, and time-bound."},
        )

    result = await safe_read_state()
    if not result["ok"]:
        raise HTTPException(status_code=500, detail={"error": result["errorCode"]})

    current = result["state"]
    existing: list[str] = current.get("goals") or []

    # Deduplicate while preserving order (latest wins)
    with_new = [*existing, text]
    seen: set[str] = set()
    deduped: list[str] = []
    for g in reversed(with_new):
        if g not in seen:
            seen.add(g)
            deduped.insert(0, g)

    next_state = {**current, "goals": deduped}
    await write_state(next_state)
    return JSONResponse({"goals": deduped})
