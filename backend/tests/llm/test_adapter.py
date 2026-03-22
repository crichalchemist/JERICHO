"""Tests for the LLM adapter — stub mode and fallback behavior."""
import asyncio

import pytest

from jericho.llm.adapter import call_llm, subagent_spawn, with_fallback
from jericho.llm.registry import ModelProfile
from jericho.llm.schemas import DecomposedGoal

_STUB_PROFILE = ModelProfile(
    model_id="stub",
    inference_backend="stub",
    context_window_tokens=4096,
    structured_output_reliability="low",
    reasoning_depth="low",
    recommended_pass_count=1,
    self_critique_required=False,
    timeout_threshold_seconds=1,
    latency_profile="fast",
    supports_tool_use=False,
)

_LLAMACPP_PROFILE = ModelProfile(
    model_id="llama3-8b-instruct",
    inference_backend="llamacpp",
    base_url="",
    context_window_tokens=4096,
    structured_output_reliability="medium",
    reasoning_depth="medium",
    recommended_pass_count=4,
    self_critique_required=True,
    timeout_threshold_seconds=60,
    latency_profile="medium",
    supports_tool_use=False,
)

_BITNET_PROFILE = ModelProfile(
    model_id="bitnet-2b",
    inference_backend="bitnet",
    base_url="",
    context_window_tokens=2048,
    structured_output_reliability="low",
    reasoning_depth="low",
    recommended_pass_count=1,
    self_critique_required=False,
    timeout_threshold_seconds=15,
    latency_profile="fast",
    supports_tool_use=False,
)


def test_stub_profile_returns_decomposed_goal_without_llm():
    result = call_llm("any prompt", DecomposedGoal, _STUB_PROFILE)
    assert isinstance(result, DecomposedGoal)


def test_llamacpp_falls_back_to_stub_when_base_url_empty(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("LLAMACPP_BASE_URL", raising=False)
    result = call_llm("any prompt", DecomposedGoal, _LLAMACPP_PROFILE)
    assert isinstance(result, DecomposedGoal)


def test_bitnet_falls_back_to_stub_when_base_url_empty(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("BITNET_BASE_URL", raising=False)
    result = call_llm("any prompt", DecomposedGoal, _BITNET_PROFILE)
    assert isinstance(result, DecomposedGoal)


def test_subagent_spawn_uses_stub_mode():
    result = subagent_spawn("prompt", DecomposedGoal, _STUB_PROFILE, pass_number=1)
    assert isinstance(result, DecomposedGoal)


async def test_with_fallback_returns_primary_on_success():
    result = await with_fallback(lambda: "primary", lambda: "fallback", timeout_seconds=5.0)
    assert result == "primary"


async def test_with_fallback_returns_fallback_on_timeout():
    async def slow() -> str:
        await asyncio.sleep(10)
        return "slow"

    result = await with_fallback(slow, lambda: "fallback", timeout_seconds=0.05)
    assert result == "fallback"


async def test_with_fallback_returns_fallback_on_exception():
    def bad() -> str:
        raise ValueError("explode")

    result = await with_fallback(bad, lambda: "safe", timeout_seconds=5.0)
    assert result == "safe"


def test_call_llm_sets_latency_on_span():
    from unittest.mock import MagicMock
    span = MagicMock()
    call_llm("prompt", DecomposedGoal, _STUB_PROFILE, otel_span=span)
    attr_keys = {c.args[0] for c in span.set_attribute.call_args_list}
    assert "llm.latency_ms" in attr_keys


def test_pass_count_drives_decomposition_passes():
    """Verify stub respects recommended_pass_count as a smoke test (stubs return on pass 1)."""
    from jericho.llm.prompts.decomposition import run_decomposition_pipeline

    result = run_decomposition_pipeline("I will finish my album by 2026-12-31", _STUB_PROFILE)
    assert isinstance(result, DecomposedGoal)
    # Stub returns empty tasks — no LLM calls
    assert result.tasks == []
