from __future__ import annotations

import re
from collections import Counter
from typing import Any

_WORD = re.compile(r"[a-zA-ZàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđA-Z0-9]+")

_STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "is", "are", "was", "were",
    "for", "on", "with", "that", "this", "it", "as", "at", "by", "be", "from",
    "và", "của", "các", "là", "cho", "trong", "với", "theo", "một", "những",
    "khi", "đã", "không", "này",
}


def extract_keywords(text: str = "", top_n: int = 5) -> dict[str, Any]:
    """Trích các từ khóa xuất hiện nhiều nhất trong văn bản đã có."""
    # Normalize inputs at trust boundary (model may send wrong types)
    if not isinstance(text, str):
        return {"tool": "keywords", "error": "TypeError", "message": "text must be a string"}
    text = text.strip()
    if not text:
        return {"tool": "keywords", "error": "ValueError", "message": "text is empty"}
    try:
        top_n = int(top_n)
    except (TypeError, ValueError) as exc:
        return {"tool": "keywords", "error": "ValueError", "message": f"top_n must be an integer: {exc}"}
    if top_n < 1:
        return {"tool": "keywords", "error": "ValueError", "message": "top_n must be >= 1"}

    words = [w.lower() for w in _WORD.findall(text) if len(w) > 2 and w.lower() not in _STOPWORDS]
    freq = Counter(words)
    top = freq.most_common(top_n)
    return {
        "tool": "keywords",
        "keywords": [{"word": word, "count": count} for word, count in top],
        "keyword_count": len(top),
        "word_count": len(words),
    }
