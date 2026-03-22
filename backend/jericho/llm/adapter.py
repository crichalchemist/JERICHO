"""
LLM adapter — Instructor + openai-compatible client (llama.cpp / BitNet.cpp).

Stub mode: inference_backend == "stub" OR resolved base_url is empty.
  llamacpp → LLAMACPP_BASE_URL  (default http://localhost:8080/v1)
  bitnet   → BITNET_BASE_URL    (default http://localhost:8081/v1)
  mlx      → MLX_BASE_URL       (iOS on-device; stubs on server when unset)

No network call is ever made during testing (env vars absent → stub).
"""
from __future__ import annotations

import asyncio
import os
from typing import Any, TypeVar

from jericho.llm.registry import ModelProfile
from jericho.llm.schemas import DecomposedGoal, NarrativeText

T = TypeVar("T")

_STUB_DECOMPOSED_GOAL = DecomposedGoal(
    goal_title="Stub goal",
    tasks=[],
    dependency_rationale="Stub mode — no LLM call made.",
)
_STUB_NARRATIVE = NarrativeText(text="Stub narrative — no LLM call made.")

_BACKEND_ENV: dict[str, str] = {
    "llamacpp": "LLAMACPP_BASE_URL",
    "bitnet": "BITNET_BASE_URL",
    "mlx": "MLX_BASE_URL",
}


def _resolve_base_url(profile: ModelProfile) -> str:
    """Return the base_url for this profile, or '' to trigger stub mode.

    Resolution order: profile.base_url → env var → '' (stub).
    The env var must be explicitly set; no hardcoded defaults so that
    the test suite (no env vars set) always stays offline.
    """
    if profile.inference_backend == "stub":
        return ""
    if profile.base_url:
        return profile.base_url
    env_key = _BACKEND_ENV.get(profile.inference_backend, "")
    return os.getenv(env_key, "") if env_key else ""


def _is_stub(profile: ModelProfile) -> bool:
    return not _resolve_base_url(profile)


def _build_stub(schema: type[T]) -> T:
    """Return a deterministic stub instance for the given schema type."""
    if schema is DecomposedGoal:
        return _STUB_DECOMPOSED_GOAL  # type: ignore[return-value]
    if schema is NarrativeText:
        return _STUB_NARRATIVE  # type: ignore[return-value]
    try:
        return schema.model_construct()  # type: ignore[return-value, union-attr]
    except Exception:
        return None  # type: ignore[return-value]


def call_llm(
    prompt: str,
    schema: type[T],
    model_profile: ModelProfile,
    otel_span: Any = None,
) -> T:
    """Single LLM call returning structured output via Instructor + openai client."""
    if _is_stub(model_profile):
        return _build_stub(schema)

    # Heavy imports deferred — openai/instructor not required during offline tests
    import instructor
    from openai import OpenAI

    base_url = _resolve_base_url(model_profile)
    client = instructor.from_openai(
        OpenAI(base_url=base_url, api_key="no-key"),
        mode=instructor.Mode.JSON,
    )

    if otel_span is not None:
        otel_span.set_attribute("llm.model_id", model_profile.model_id)
        otel_span.set_attribute("llm.backend", model_profile.inference_backend)

    return client.chat.completions.create(  # type: ignore[no-any-return]
        model=model_profile.model_id,
        messages=[{"role": "user", "content": prompt}],
        response_model=schema,
        max_retries=2,
    )


def subagent_spawn(
    prompt: str,
    schema: type[T],
    model_profile: ModelProfile,
    pass_number: int = 1,
    otel_span: Any = None,
) -> T:
    """Fresh LLM context per call — no conversation history bleeds across passes."""
    if otel_span is not None:
        otel_span.set_attribute("llm.pass_number", pass_number)
    return call_llm(prompt, schema, model_profile, otel_span=otel_span)


async def with_fallback(
    primary_fn: Any,
    fallback_fn: Any,
    timeout_seconds: float,
) -> Any:
    """Run primary_fn under a deadline; on timeout or exception use fallback_fn."""
    loop = asyncio.get_event_loop()

    async def _run(fn: Any) -> Any:
        if asyncio.iscoroutinefunction(fn):
            return await fn()
        return await loop.run_in_executor(None, fn)

    try:
        return await asyncio.wait_for(_run(primary_fn), timeout=timeout_seconds)
    except Exception:
        return await _run(fallback_fn)
