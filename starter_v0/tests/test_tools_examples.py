"""Worked examples - read these first, then copy the patterns into test_tools_todo.py.

Patterns shown:
1. Pure local tool: call it, assert on the output dict.
2. Guardrail: a side-effect tool must NOT act without confirmation.
3. Live API tool: mock HTTP, assert on the request we send AND on how we map the response.
4. Failure path: missing key / HTTP error returns an error dict instead of raising.
5. Agent loop without a real model: a fake provider returns tool calls.
"""
from __future__ import annotations

import io

import pytest
import requests

from agent import ResearchAgent
from conftest import FakeResponse
from providers.base import ModelResponse, ToolCall
from tools import TOOL_FUNCTIONS
from ui_agent import AgentSession, run_live_turn

format_tool = TOOL_FUNCTIONS["format"]
lookup_tool = TOOL_FUNCTIONS["lookup"]
send_tool = TOOL_FUNCTIONS["send"]


# 1. Pure local tool -------------------------------------------------------

def test_format_brief_keeps_at_most_5_items_and_links_source() -> None:
    items = [{"title": f"Tin {i}", "url": f"https://example.com/{i}"} for i in range(8)]
    result = format_tool(items=items, template="brief", headline="AI hôm nay")

    assert result["item_count"] == 8
    assert result["markdown"].startswith("**AI hôm nay**")
    assert result["markdown"].count("\n- ") == 5
    assert "[example.com](https://example.com/0)" in result["markdown"]


def test_format_truncates_long_summary() -> None:
    result = format_tool(items=[{"summary": "x" * 500}], template="bullets")
    assert "x" * 277 + "..." in result["markdown"]
    assert "x" * 278 not in result["markdown"]


# 2. Guardrail ---------------------------------------------------------------

@pytest.mark.parametrize("confirmed", [False, "false"])
def test_send_without_confirmation_does_not_call_network(fake_http, confirmed) -> None:
    calls = fake_http(FakeResponse({"ok": True}))
    result = send_tool(text="Bản tin", confirmed=confirmed)

    assert result["status"] == "needs_confirmation"
    assert calls == []


# 3. Live API tool with mocked HTTP -----------------------------------------

def test_lookup_sends_expected_request_and_maps_results(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"results": [
        {"title": "GPT news", "url": "https://www.openai.com/blog/x", "content": "summary", "score": 0.9},
    ]}))

    result = lookup_tool(query="OpenAI news", topic="news", timeframe="day", max_results=3)

    assert calls[0]["url"] == "https://api.tavily.com/search"
    assert calls[0]["json"]["topic"] == "news"
    assert calls[0]["json"]["time_range"] == "day"
    assert calls[0]["json"]["max_results"] == 3
    assert calls[0]["headers"]["Authorization"] == "Bearer test-key"
    assert result["items"][0] == {
        "title": "GPT news", "url": "https://www.openai.com/blog/x",
        "source": "openai.com", "summary": "summary", "score": 0.9,
    }


# 4. Failure path -----------------------------------------------------------

def test_lookup_without_key_returns_error_dict() -> None:
    result = lookup_tool(query="anything")
    assert result["error"] == "RuntimeError"
    assert "TAVILY_API_KEY" in result["message"]


def test_lookup_http_error_returns_error_dict(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
    fake_http(FakeResponse(status_code=429))
    assert lookup_tool(query="x")["error"] == "HTTPError"


def test_send_hides_bot_token_in_http_error(monkeypatch, fake_http) -> None:
    token = "test-telegram-token"
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", token)
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-1234")
    fake_http(requests.HTTPError(f"Request failed at https://api.telegram.org/bot{token}/sendMessage"))

    result = send_tool(text="Bản tin", confirmed=True)

    assert result["error"] == "HTTPError"
    assert token not in result["message"]


# 5. Agent loop with a fake provider (no model, no API) ---------------------

class FakeProvider:
    def __init__(self, calls: list[ToolCall]) -> None:
        self.calls = calls

    def complete(self, messages, tools=None, *, model=None, temperature=0.0, tool_choice=None) -> ModelResponse:
        return ModelResponse(text=None, tool_calls=self.calls)


def test_live_chat_tool_logging_works_with_legacy_windows_stdout(monkeypatch) -> None:
    buffer = io.BytesIO()
    console = io.TextIOWrapper(buffer, encoding="cp1252", errors="strict")
    question = "Bạn muốn xem kết quả ngày nào? 🔧"
    session = AgentSession(
        FakeProvider([ToolCall("clarify", {"question": question, "response_type": "text"})]),
        "test", [], {"history_window": 5, "model": "fake", "max_tool_rounds": 1},
    )

    with monkeypatch.context() as patch:
        patch.setattr("sys.stdout", console)
        result = run_live_turn(session, [], "test")
        console.flush()

    assert result["status"] == "waiting_for_user"
    assert result["assistant_text"] == question
    assert result["tool_events"][0]["args"]["question"] == question
    assert "[tool]" in buffer.getvalue().decode("ascii")


def test_agent_executes_tool_and_survives_unknown_or_bad_calls() -> None:
    provider = FakeProvider([
        ToolCall("clarify", {"question": "Bạn muốn xem tài khoản nào?"}),
        ToolCall("made_up_tool", {}),
        ToolCall("format", {"_invalid_json_arguments": "{bad json"}),
    ])
    run = ResearchAgent(provider, system_prompt="test").run([{"role": "user", "content": "tweet mới nhất?"}])

    assert run.tool_results[0]["result"]["awaiting_user"] is True
    assert run.tool_results[1]["error"] == "unknown_tool"
    assert run.tool_results[2]["result"]["error"] == "TypeError"


@pytest.fixture
def telegram_chat(monkeypatch, fake_http):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-telegram-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-1234")
    calls = fake_http(FakeResponse({"ok": True}))
    text = "**Bản tin**\n\nNội dung vừa soạn."
    session = AgentSession(
        FakeProvider([ToolCall("send", {"text": text, "confirmed": True})]),
        "test", [], {"history_window": 5, "model": "fake", "max_tool_rounds": 4},
    )
    return session, text, calls


def test_chat_sends_the_displayed_draft_only_after_new_approval(telegram_chat) -> None:
    session, text, calls = telegram_chat

    preview = run_live_turn(session, [], "yes")

    assert preview["status"] == "waiting_for_user"
    assert text in preview["assistant_text"]
    assert "-1234" in preview["assistant_text"]
    assert calls == []

    turn = {"user": "yes", **preview}
    sent = run_live_turn(session, [turn], "Gửi")

    assert sent["tool_events"][0]["result"]["status"] == "sent"
    assert len(calls) == 1
    assert calls[0]["json"]["text"] == text
    assert calls[0]["json"]["chat_id"] == "-1234"

    run_live_turn(session, [turn], "Gửi")
    assert len(calls) == 1


def test_chat_canceling_a_telegram_draft_does_not_send(telegram_chat) -> None:
    session, _, calls = telegram_chat
    turn = {"user": "yes", **run_live_turn(session, [], "yes")}

    canceled = run_live_turn(session, [turn], "Hủy")

    assert "Đã hủy" in canceled["assistant_text"]
    assert calls == []


def test_chat_blocks_telegram_send_if_the_destination_changed(monkeypatch, telegram_chat) -> None:
    session, _, calls = telegram_chat
    turn = {"user": "yes", **run_live_turn(session, [], "yes")}
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-5678")

    failed = run_live_turn(session, [turn], "Gửi")

    assert "Đích Telegram đã đổi" in failed["tool_events"][0]["result"]["message"]
    assert calls == []
