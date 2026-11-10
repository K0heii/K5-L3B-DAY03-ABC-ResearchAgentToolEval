---
name: extract_links
track: bonus
kind: local_formatter
requires_env: []
inputs: [text, items]
outputs: [links, link_count]
side_effect: false
---
# extract_links

Trích danh sách URL (kèm tiêu đề nếu có) từ một đoạn văn bản hoặc danh sách item đã có trong hội thoại. Không truy cập các URL đó.
