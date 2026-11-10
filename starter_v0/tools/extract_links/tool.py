from __future__ import annotations

import re
from typing import Any

_MD_LINK = re.compile(r"\[([^\]]*)\]\((https?://[^\s)]+)\)")
_BARE_URL = re.compile(r"https?://[^\s)\]>\"',;]+")


def extract_links(text: str = "", items: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Trích danh sách URL (kèm tiêu đề nếu có) từ văn bản hoặc danh sách item đã có."""
    # Normalize inputs at trust boundary (model may send wrong types)
    if not isinstance(text, str):
        return {"tool": "extract_links", "error": "TypeError", "message": "text must be a string"}
    if items is not None and not isinstance(items, list):
        return {"tool": "extract_links", "error": "TypeError", "message": "items must be a list"}

    links: list[dict[str, str]] = []
    seen: set[str] = set()

    if text.strip():
        # Markdown link trước để giữ được title
        for title, url in _MD_LINK.findall(text):
            if url not in seen:
                seen.add(url)
                links.append({"url": url, "title": title})
        for url in _BARE_URL.findall(text):
            if url not in seen:
                seen.add(url)
                links.append({"url": url})

    for item in items or []:
        if not isinstance(item, dict):
            continue
        url = item.get("url")
        if url and url not in seen:
            seen.add(url)
            links.append({"url": url, "title": item.get("title") or item.get("source") or ""})

    if not links:
        return {"tool": "extract_links", "error": "ValueError", "message": "no links found in text or items"}
    return {"tool": "extract_links", "links": links, "link_count": len(links)}
