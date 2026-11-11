from __future__ import annotations

from datetime import datetime, timedelta, timezone
import re
import unicodedata
from typing import Any


VIETNAM = timezone(timedelta(hours=7), name="Asia/Ho_Chi_Minh")


def get_calendar_context() -> dict[str, Any]:
    """Read the machine clock, returning calendar offsets in Vietnam time."""
    now = datetime.now(VIETNAM)
    offsets = {"today": 0, "yesterday": -1, "day_before_yesterday": -2,
               "tomorrow": 1, "day_after_tomorrow": 2}
    dates = {}
    for name, offset in offsets.items():
        day = now.date() + timedelta(days=offset)
        dates[name] = {"iso": day.isoformat(), "display": day.strftime("%d/%m/%Y")}
    return {"tool": "calendar", "timezone": "Asia/Ho_Chi_Minh",
            "now": now.isoformat(timespec="seconds"), "dates": dates,
            "note": "Calendar only; this does not establish a draw schedule or result."}


def lottery_turn_context(messages: list[dict[str, str]]) -> dict[str, Any] | None:
    """Bind Vietnamese relative dates to this turn, independent of model memory."""
    users = [unicodedata.normalize("NFC", m.get("content", "")).casefold()
             for m in messages if m.get("role") == "user"]
    if not users:
        return None
    latest = users[-1]

    def mentions_lottery(text: str) -> bool:
        return bool(re.search(r"\b(xổ số|xsmb|xsmt|xsmn|kqxs)\b", text)) or (
            "kết quả" in text and any(region in text for region in ("miền bắc", "miền trung", "miền nam"))
        )

    followup = bool(re.match(r"\s*(còn|thế|vậy|hôm nay|hôm qua|hôm kia|ngày mai|ngày kia)\b", latest))
    if not mentions_lottery(latest) and not (followup and any(mentions_lottery(s) for s in users[:-1])):
        return None
    phrases = {"hôm nay": "today", "hôm qua": "yesterday", "hôm kia": "day_before_yesterday",
               "ngày mai": "tomorrow", "ngày kia": "day_after_tomorrow"}
    matches = [(phrase, key) for phrase, key in phrases.items()
               if re.search(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", latest)]
    # Don't impose a single date on requests for a range or an explicit date.
    if len(matches) != 1 or re.search(r"\d{1,4}[-/]\d{1,2}[-/]\d{1,4}", latest):
        return None
    context = get_calendar_context()
    context["requested_phrase"] = matches[0][0]
    context["target_date"] = context["dates"][matches[0][1]]["iso"]
    context["is_future"] = context["target_date"] > context["dates"]["today"]["iso"]
    return context
