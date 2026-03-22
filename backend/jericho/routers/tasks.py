from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from jericho.db.json_adapter import safe_read_state, write_state

router = APIRouter(tags=["tasks"])

_VALID_STATUSES_FULL = {"completed", "missed", "pending"}
_VALID_STATUSES_TERMINAL = {"completed", "missed"}


def _apply_task_status_to_state(state: dict[str, Any], task_id: str, status: str) -> dict[str, Any]:
    """Immutably update task status in the state dict."""
    tasks: list[dict[str, Any]] = state.get("tasks") or []
    updated = [
        {**t, "status": status} if t.get("id") == task_id else t
        for t in tasks
    ]
    return {**state, "tasks": updated}


class TaskStatusUpdatePayload(BaseModel):
    id: str
    status: str


class TaskStatusPayload(BaseModel):
    taskId: str
    status: str


@router.post("/tasks")
async def update_task(payload: TaskStatusUpdatePayload) -> JSONResponse:
    if payload.status not in _VALID_STATUSES_FULL:
        raise HTTPException(
            status_code=400,
            detail={"error": "INVALID_TASK_STATUS", "message": "Invalid status."},
        )

    result = await safe_read_state()
    if not result["ok"]:
        raise HTTPException(status_code=500, detail={"error": result["errorCode"]})

    updated = _apply_task_status_to_state(result["state"], payload.id, payload.status)
    await write_state(updated)
    return JSONResponse({"status": "ok"})


@router.post("/task-status")
async def update_task_status(payload: TaskStatusPayload) -> JSONResponse:
    if payload.status not in _VALID_STATUSES_TERMINAL:
        raise HTTPException(
            status_code=400,
            detail={"error": "INVALID_TASK_STATUS", "message": "Invalid status."},
        )

    result = await safe_read_state()
    if not result["ok"]:
        raise HTTPException(status_code=500, detail={"error": result["errorCode"]})

    updated = _apply_task_status_to_state(result["state"], payload.taskId, payload.status)
    written = await write_state(updated)
    return JSONResponse({"state": written})
