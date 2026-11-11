from datetime import datetime, timezone
from importlib import import_module

import pytest

from conftest import FakeResponse
from tools.lookup.tool import web_search
from chat import run_model_tool_loop
from providers.base import ModelResponse, ToolCall
from tools import TOOL_FUNCTIONS


calendar = import_module("tools.calendar.tool")


@pytest.mark.parametrize(
    "utc_time,today,yesterday,day_before,tomorrow,day_after",
    [
        ("2026-11-10T18:00:00+00:00", "2026-11-11", "2026-11-10", "2026-11-09", "2026-11-12", "2026-11-13"),
        ("2026-12-31T18:00:00+00:00", "2027-01-01", "2026-12-31", "2026-12-30", "2027-01-02", "2027-01-03"),
        ("2024-02-29T18:00:00+00:00", "2024-03-01", "2024-02-29", "2024-02-28", "2024-03-02", "2024-03-03"),
    ],
)
def test_calendar_offsets_use_vietnam_calendar_days(
    monkeypatch, utc_time, today, yesterday, day_before, tomorrow, day_after,
):
    frozen = datetime.fromisoformat(utc_time)

    class FrozenDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return frozen.astimezone(tz or timezone.utc)

    monkeypatch.setattr(calendar, "datetime", FrozenDatetime)
    result = calendar.get_calendar_context()

    assert result["timezone"] == "Asia/Ho_Chi_Minh"
    assert result["now"].endswith("+07:00")
    dates = result["dates"]
    assert [dates[k]["iso"] for k in (
        "today", "yesterday", "day_before_yesterday", "tomorrow", "day_after_tomorrow",
    )] == [today, yesterday, day_before, tomorrow, day_after]
    for value in dates.values():
        assert value["display"] == datetime.fromisoformat(value["iso"]).strftime("%d/%m/%Y")


def test_lookup_exact_draw_date_adds_date_and_disables_recency(monkeypatch, fake_http):
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"results": []}))

    result = web_search(query="xổ số miền Bắc", timeframe="day", target_date="2026-11-11")

    body = calls[0]["json"]
    assert body["query"] == "xổ số miền Bắc ngày 11/11/2026"
    assert "time_range" not in body
    assert result["target_date"] == "2026-11-11"
    assert result["timeframe"] is None
    assert result["items"] == []
    assert "unverified" in result["verification_note"]


@pytest.mark.parametrize("bad_date", ["2026-02-30", "11/11/2026", "20261111", "hôm qua"])
def test_lookup_invalid_date_returns_error_without_network(bad_date, fake_http):
    calls = fake_http(FakeResponse())
    result = web_search(query="lottery", target_date=bad_date)
    assert result["error"] == "ValueError"
    assert calls == []


@pytest.mark.parametrize("phrase,key", [
    ("hôm nay", "today"), ("hôm qua", "yesterday"),
    ("hôm kia", "day_before_yesterday"), ("ngày kia", "day_after_tomorrow"),
])
def test_latest_relative_date_does_not_chain_from_previous_draw(monkeypatch, phrase, key):
    snapshot = calendar.get_calendar_context()
    monkeypatch.setattr(calendar, "get_calendar_context", lambda: snapshot.copy())
    result = calendar.lottery_turn_context([
        {"role": "user", "content": "Xổ số miền Bắc hôm kia"},
        {"role": "assistant", "content": "Kết quả cũ của một ngày khác"},
        {"role": "user", "content": f"Còn {phrase}?"},
    ])
    assert result["target_date"] == snapshot["dates"][key]["iso"]


@pytest.mark.parametrize("future,expected_error", [
    (False, "draw_date_mismatch"), (True, "unpublished_future_draw"),
])
def test_lottery_lookup_wrong_date_or_future_is_blocked(monkeypatch, future, expected_error):
    context = {"target_date": "2026-11-11", "is_future": future}
    monkeypatch.setattr("chat.lottery_turn_context", lambda messages: context)
    called = []
    monkeypatch.setitem(TOOL_FUNCTIONS, "lookup", lambda **kwargs: called.append(kwargs))
    responses = iter([
        ModelResponse(text=None, tool_calls=[ToolCall("lookup", {
            "query": "lottery", "target_date": "2026-11-09",
        })]),
        ModelResponse(text="No verified results.", tool_calls=[]),
    ])

    class Provider:
        def complete(self, *args, **kwargs):
            return next(responses)

    result = run_model_tool_loop(
        provider=Provider(), messages=[{"role": "user", "content": "test"}],
        tools=[], model=None, max_tool_rounds=2,
    )
    assert called == []
    assert result["tool_events"][0]["result"]["error"] == expected_error


def test_calendar_recognizes_regional_result_request_without_word_lottery():
    context = calendar.lottery_turn_context([
        {"role": "user", "content": "Kết quả miền Bắc hôm nay"},
    ])
    assert context["target_date"] == context["dates"]["today"]["iso"]


def test_switch_to_ordinary_news_does_not_inherit_lottery_date_guard():
    assert calendar.lottery_turn_context([
        {"role": "user", "content": "Xổ số miền Bắc hôm qua"},
        {"role": "user", "content": "Tìm tin tức AI hôm nay"},
    ]) is None
