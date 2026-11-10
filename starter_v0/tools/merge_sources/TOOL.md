---
name: merge_sources
track: bonus
kind: local_formatter
requires_env: []
inputs: [items, dedupe_key, sort_by]
outputs: [items, item_count, duplicates_removed, skipped]
side_effect: false
---
# merge_sources

Gộp danh sách item từ nhiều tool (lookup, timeline, social_search, papers) và loại bỏ item trùng nhau theo một khóa (mặc định url). Không tìm dữ liệu mới.
