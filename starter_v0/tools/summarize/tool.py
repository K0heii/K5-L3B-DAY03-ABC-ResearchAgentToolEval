from __future__ import annotations

import re
from collections import Counter
from typing import Any

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
_WORD = re.compile(r"[a-zA-ZàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđA-Z0-9]+")


def summarize_text(text: str = "", max_sentences: int = 3) -> dict[str, Any]:
    """Extractive summarization: pick top-scoring sentences by word frequency."""
    # Normalize inputs at trust boundary (model may send wrong types)
    try:
        if not isinstance(text, str):
            return {"tool": "summarize", "error": "TypeError", "message": "text must be a string"}
        text = text.strip()
        max_sentences = int(max_sentences)
    except (TypeError, ValueError) as exc:
        return {"tool": "summarize", "error": type(exc).__name__, "message": str(exc)}

    if not text:
        return {"tool": "summarize", "error": "ValueError", "message": "text is empty"}
    if max_sentences < 1:
        return {"tool": "summarize", "error": "ValueError", "message": "max_sentences must be >= 1"}

    sentences = [s.strip() for s in _SENTENCE_SPLIT.split(text) if s.strip()]
    sentence_count = len(sentences)

    if sentence_count <= max_sentences:
        summary_sentences = sentences
    else:
        # Frequency-based scoring: skip common stopwords
        stop = {"the", "a", "an", "and", "or", "of", "to", "in", "is", "are", "was", "were",
                "for", "on", "with", "that", "this", "it", "as", "at", "by", "be", "from",
                "và", "của", "các", "là", "cho", "trong", "với", "theo", "một", "những",
                "khi", "đã", "không", "này"}
        freq: Counter[str] = Counter()
        for s in sentences:
            for w in _WORD.findall(s.lower()):
                if w not in stop and len(w) > 2:
                    freq[w] += 1

        # Score each sentence by word frequency, normalized by length
        scores = [sum(freq[w] for w in _WORD.findall(s.lower())) / max(len(s.split()), 1) for s in sentences]
        top_indices = sorted(range(sentence_count), key=lambda i: scores[i], reverse=True)[:max_sentences]
        # Keep original order
        summary_sentences = [sentences[i] for i in sorted(top_indices)]

    return {
        "tool": "summarize",
        "summary": " ".join(summary_sentences),
        "sentences_used": len(summary_sentences),
        "sentence_count": sentence_count,
    }
