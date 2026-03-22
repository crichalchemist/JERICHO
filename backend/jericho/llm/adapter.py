"""
LLM adapter — wraps Instructor + Ollama.

All external LLM calls go through call_llm(). Stub mode activates when
inference_backend == "stub" or LLM_API_KEY is absent — returns a deterministic
stub without touching the network. Same pattern as the JS callLLM() stub.
"""
from __future__ import annotations

import asyncio
import os
from typing import Any, TypeVar

from jericho.llm.registry import ModelProfile
from jericho.llm.schemas import DecomposedGoal

T = TypeVar("T")

_STUB_DECOMPOSED_GOAL = DecomposedGoal(
    goal_title="Stub goal",
    tasks=[],
    dependency_rationale="Stub mode — no LLM call made.",
)


def _is_stub_mode(model_profile: ModelProfile) -> bool:
    return model_profile.inference_backend == "stub" or not os.getenv("LLM_API_KEY")


def _build_stub(schema: type[T]) -> T:
    """Return a deterministic stub instance for the given schema type."""
    if schema is DecomposedGoal:
        return _STUB_DECOMPOSED_GOAL  # type: ignore[return-value]
    # Attempt minimal no-validation construction for other schemas
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
    """
    Single LLM call returning structured output via Instructor.
    Falls back to stub when offline or in test mode.
    """
    if _is_stub_mode(model_profile):
        return _build_stub(schema)

    # Heavy imports deferred — Ollama not required during tests
    import instructor
    import ollama as _ollama

    client = instructor.from_ollama(_ollama.Client())

    if otel_span is not None:
        otel_span.set_attribute("llm.model_id", model_profile.model_id)
        otel_span.set_attribute("llm.backend", model_profile.inference_backend)

    return client.chat.completions.create(  # type: ignore[no-any-return]
        model=model_profile.model_id,
        messages=[{"role": "user", "content": prompt}],
        response_model=schema,
    )


def subagent_spawn(
    prompt: str,
    schema: type[T],
    model_profile: ModelProfile,
    pass_number: int = 1,
    otel_span: Any = None,
) -> T:
    """
    Fresh LLM context per call — no conversation history bleeds across passes.
    pass_number is recorded for observability only.
    """
    if otel_span is not None:
        otel_span.set_attribute("llm.pass_number", pass_number)
    return call_llm(prompt, schema, model_profile, otel_span=otel_span)


async def with_fallback(
    primary_fn: Any,
    fallback_fn: Any,
    timeout_seconds: float,
) -> Any:
    """
    Run primary_fn under a deadline; on timeout or any exception use fallback_fn.
    Accepts both sync and async callables for both branches.
    """
    loop = asyncio.get_event_loop()

    async def _run(fn: Any) -> Any:
        if asyncio.iscoroutinefunction(fn):
            return await fn()
        return await loop.run_in_executor(None, fn)

    try:
        return await asyncio.wait_for(_run(primary_fn), timeout=timeout_seconds)
    except Exception:
        return await _run(fallback_fn)
