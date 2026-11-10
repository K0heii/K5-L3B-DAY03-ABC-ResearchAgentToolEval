from __future__ import annotations

from typing import Any


def merge_sources(items: list[dict[str, Any]] | None = None, dedupe_key: str = "url", sort_by: str = "none") -> dict[str, Any]:
    """Gộp item từ nhiều nguồn (lookup, timeline, papers...), khử trùng lặp theo một khóa."""
    # Normalize inputs at trust boundary (model may send wrong types)
    if not isinstance(items, list):
        return {"tool": "merge_sources", "error": "TypeError", "message": "items must be a list"}
    if not isinstance(dedupe_key, str) or not dedupe_key:
        return {"tool": "merge_sources", "error": "ValueError", "message": "dedupe_key must be a non-empty string"}
    if sort_by not in ("none", "score"):
        return {"tool": "merge_sources", "error": "ValueError", "message": "sort_by must be 'none' or 'score'"}

    merged: list[dict[str, Any]] = []
    seen: dict[Any, int] = {}  # dedupe_key value -> index in merged
    duplicates = 0
    skipped = 0
    for item in items:
        if not isinstance(item, dict):
            skipped += 1
            continue
        key = item.get(dedupe_key)
        if key is not None and key in seen:
            duplicates += 1
            old = merged[seen[key]]
            # Giữ bản có điểm cao hơn nếu cả hai đều có score
            if isinstance(item.get("score"), (int, float)) and (
                not isinstance(old.get("score"), (int, float)) or item["score"] > old["score"]
            ):
                merged[seen[key]] = item
            continue
        if key is not None:
            seen[key] = len(merged)
        merged.append(item)

    if sort_by == "score":
        merged.sort(key=lambda it: it["score"] if isinstance(it.get("score"), (int, float)) else float("-inf"), reverse=True)

    return {
        "tool": "merge_sources",
        "items": merged,
        "item_count": len(merged),
        "duplicates_removed": duplicates,
        "skipped": skipped,
    }
