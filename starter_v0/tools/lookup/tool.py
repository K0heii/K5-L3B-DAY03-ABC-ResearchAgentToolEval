from __future__ import annotations

import os
from datetime import date
from typing import Any

import requests

from tools._shared import TIMEOUT, domain, err


def web_search(query: str = "", topic: str = "general", timeframe: str | None = "week", max_results: int = 5, target_date: str | None = None) -> dict[str, Any]:
    try:
        if target_date is not None:
            day = date.fromisoformat(target_date)
            if day.isoformat() != target_date:
                raise ValueError("target_date must be YYYY-MM-DD")
            query = f"{query} ngày {day.strftime('%d/%m/%Y')}"
            # Search recency is a publication filter, not the requested event date.
            timeframe = None
        key = os.getenv("TAVILY_API_KEY")
        if not key:
            raise RuntimeError("Missing TAVILY_API_KEY env var")
        body: dict[str, Any] = {"query": query, "topic": topic, "max_results": int(max_results or 5), "search_depth": "basic"}
        if timeframe:
            body["time_range"] = timeframe
        response = requests.post(
            "https://api.tavily.com/search",
            json=body,
            headers={"Authorization": f"Bearer {key}"},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        items = [{
            "title": item.get("title"),
            "url": item.get("url"),
            "source": domain(item.get("url", "")),
            "summary": item.get("content"),
            "score": item.get("score"),
        } for item in data.get("results", [])]
        result = {"tool": "web_search", "query": query, "topic": topic, "timeframe": timeframe, "items": items}
        if target_date is not None:
            result["target_date"] = target_date
            result["verification_note"] = "Search matches are unverified; check the event date and region in source content before reporting numbers."
        return result
    except Exception as exc:
        return err("web_search", exc)

