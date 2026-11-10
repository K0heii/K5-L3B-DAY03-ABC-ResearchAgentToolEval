---
name: keywords
track: bonus
kind: local_formatter
requires_env: []
inputs: [text, top_n]
outputs: [keywords, keyword_count, word_count]
side_effect: false
---
# keywords

Trích các từ khóa xuất hiện nhiều nhất trong một đoạn văn bản đã có trong hội thoại (ví dụ từ fetch hoặc paper_text). Không tìm kiếm, không gọi API.
