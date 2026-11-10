---
name: summarize
track: bonus
kind: local_formatter
requires_env: []
inputs: [text, max_sentences]
outputs: [summary, sentences_used, sentence_count]
side_effect: false
---
# summarize

Tóm tắt extractive một đoạn văn bản đã có trong hội thoại (ví dụ từ fetch hoặc paper_text). Không tìm kiếm hoặc gọi API nào.
