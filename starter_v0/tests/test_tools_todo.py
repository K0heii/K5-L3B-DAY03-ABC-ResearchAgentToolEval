"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    # Call clarify with response_type="choice" and 2 options.
    # Assert: options are returned unchanged, awaiting_user is True.
    pytest.skip(TODO)


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    # Items with section "A", "B", "A" -> markdown has exactly one "## A" and one "## B".
    pytest.skip(TODO)


def test_format_thread_numbers_items() -> None:
    # template="thread" -> lines start with "1/", "2/", ...
    pytest.skip(TODO)


def test_format_empty_items_does_not_crash() -> None:
    # items=None and items=[] -> item_count == 0, no exception.
    pytest.skip(TODO)


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    # Set TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, mock HTTP.
    # Assert: exactly one POST, URL contains the token, json has chat_id + text, status == "sent".
    pytest.skip(TODO)


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    pytest.skip(TODO)


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    # timeframe=None -> request body has no "time_range" key.
    pytest.skip(TODO)


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    # Mock {"data": {"markdown": "...", "metadata": {"title": "T", "sourceURL": "https://..."}}}
    # Assert title/url/source/summary in result["items"][0].
    pytest.skip(TODO)


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    pytest.skip(TODO)


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    # Mock {"timeline": [...]} with 1 item missing tweet_id and 6 valid items, limit=3.
    # Assert 3 items, and each url looks like https://x.com/<handle>/status/<id>.
    pytest.skip(TODO)


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    # Assert the request params carry the query and search_type ("Top" / "Latest").
    pytest.skip(TODO)


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    pytest.skip(TODO)


def test_policy_area_filter_only_returns_that_area() -> None:
    # policy_area="data_privacy" -> every result has policy_area == "data_privacy".
    pytest.skip(TODO)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    # One policy file contains a quoted line that tries to give the assistant orders.
    # Query that section (source_citation) and assert: that line is in untrusted_text, NOT in facts.
    pytest.skip(TODO)


# ---------------- YOUR NEW TOOL(S) ----------------
# Write at least 3 tests per tool your team adds:
#   1. happy path (mocked if it calls an API)
#   2. bad / missing input from the model (empty string, wrong type, out-of-enum value)
#   3. failure path (missing key, HTTP error, timeout) -> returns error dict, does not raise

summarize_tool = TOOL_FUNCTIONS["summarize"]


def test_summarize_picks_top_sentences_in_original_order() -> None:
    # Craft text where top-scoring sentences are not the first ones
    text = (
        "The weather is nice today. "
        "Artificial intelligence transforming research workflows dramatically. "
        "I like coffee. "
        "Machine learning models require extensive computational resources. "
        "The sky is blue."
    )
    result = summarize_tool(text=text, max_sentences=2)

    assert result["tool"] == "summarize"
    assert result["sentences_used"] == 2
    assert result["sentence_count"] == 5
    # Top sentences should contain key terms (intelligence, machine, learning, etc.)
    assert "intelligence" in result["summary"].lower() or "machine" in result["summary"].lower()


def test_summarize_bad_input_returns_error_dict() -> None:
    # Model sends wrong type
    result = summarize_tool(text=None)
    assert result["error"] == "TypeError"
    assert "string" in result["message"]

    # Empty text
    result = summarize_tool(text="")
    assert result["error"] == "ValueError"
    assert "empty" in result["message"]

    # text as integer (wrong type)
    result = summarize_tool(text=123)
    assert result["error"] == "TypeError"


def test_summarize_invalid_max_sentences_returns_error_dict() -> None:
    # max_sentences too small
    result = summarize_tool(text="Hello. World.", max_sentences=0)
    assert result["error"] == "ValueError"
    assert "must be >= 1" in result["message"]

    # max_sentences negative
    result = summarize_tool(text="Hello. World.", max_sentences=-5)
    assert result["error"] == "ValueError"


# ---------------- merge_sources (new tool, CP3 bonus) ----------------

merge_tool = TOOL_FUNCTIONS["merge_sources"]


def test_merge_sources_dedupes_by_url_and_keeps_highest_score() -> None:
    items = [
        {"title": "A", "url": "https://x.com/a", "score": 1},
        {"title": "B", "url": "https://x.com/b", "score": 2},
        {"title": "A (dup)", "url": "https://x.com/a", "score": 5},
        "not a dict",
        {"title": "C"},  # no url -> always kept
    ]
    result = merge_tool(items=items)

    assert result["item_count"] == 3
    assert result["duplicates_removed"] == 1
    assert result["skipped"] == 1
    a = next(i for i in result["items"] if i.get("url") == "https://x.com/a")
    assert a["score"] == 5  # bản điểm cao hơn thay bản điểm thấp


def test_merge_sources_sort_by_score_puts_top_first() -> None:
    items = [{"url": "u1", "score": 1}, {"url": "u2", "score": 3}, {"url": "u3", "score": 2}, {"url": "u4"}]
    result = merge_tool(items=items, sort_by="score")
    assert [i.get("score") for i in result["items"]] == [3, 2, 1, None]  # không có score xuống cuối


def test_merge_sources_bad_input_returns_error_dict() -> None:
    assert merge_tool(items=None)["error"] == "TypeError"
    assert merge_tool(items="oops")["error"] == "TypeError"
    assert merge_tool(items=[], dedupe_key="")["error"] == "ValueError"
    assert merge_tool(items=[], sort_by="date")["error"] == "ValueError"


# ---------------- keywords (new tool, CP3 bonus) ----------------

keywords_tool = TOOL_FUNCTIONS["keywords"]


def test_keywords_returns_most_frequent_words_first() -> None:
    text = "AI agents help research. Research teams build agents. Agents use research tools."
    result = keywords_tool(text=text, top_n=2)

    assert result["keywords"][0] == {"word": "agents", "count": 3}
    assert result["keywords"][1] == {"word": "research", "count": 3}
    assert result["word_count"] == 11


def test_keywords_bad_input_returns_error_dict() -> None:
    assert keywords_tool(text=None)["error"] == "TypeError"
    assert keywords_tool(text=123)["error"] == "TypeError"
    assert keywords_tool(text="   ")["error"] == "ValueError"


def test_keywords_invalid_top_n_returns_error_dict() -> None:
    assert keywords_tool(text="hello world", top_n=0)["error"] == "ValueError"
    assert keywords_tool(text="hello world", top_n="abc")["error"] == "ValueError"


# ---------------- extract_links (new tool, CP3 bonus) ----------------

links_tool = TOOL_FUNCTIONS["extract_links"]


def test_extract_links_pulls_markdown_bare_and_item_urls_without_duplicates() -> None:
    text = "Xem [bài viết](https://a.com/1) và https://b.com/2, trùng: https://a.com/1"
    result = links_tool(text=text)

    assert result["link_count"] == 2
    assert result["links"][0] == {"url": "https://a.com/1", "title": "bài viết"}
    assert result["links"][1] == {"url": "https://b.com/2"}

    # items cũng là nguồn link
    result = links_tool(text="", items=[{"url": "https://c.com/3", "title": "C"}])
    assert result["links"] == [{"url": "https://c.com/3", "title": "C"}]


def test_extract_links_bad_input_returns_error_dict() -> None:
    assert links_tool(text=123)["error"] == "TypeError"
    assert links_tool(text="", items="oops")["error"] == "TypeError"


def test_extract_links_text_without_links_returns_error_dict() -> None:
    result = links_tool(text="không có link nào ở đây")
    assert result["error"] == "ValueError"
    assert "no links" in result["message"]
