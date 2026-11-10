# Báo cáo cá nhân — TruongThiThuHa-2A202603780

## 1. Thông tin thành viên

- Họ tên: Trương Thị Thu Hà
- MSSV: 2A202603780
- Email: 26ai.hattt@vinuni.edu.vn

## 2. Phần việc phụ trách

Người 4 — phụ trách CP4 (10 eval case nhóm, chạy `--suite group`) và tổng hợp báo cáo nhóm (Phần A, bảng B1, B2, B3, B5a).

## 3. Đóng góp cụ thể

- Setup môi trường cá nhân: `.venv`, `.env` với key riêng (OpenRouter, Gemini, Tavily, Firecrawl, RapidAPI); `pytest` 62 passed / 17 skipped; preflight OpenRouter và Gemini pass.
- Phát hiện model mặc định `gemini-3.8-flash` bị lỗi 503 (quá tải) → đổi default sang `gemini-3.1-flash-lite` trong `providers/gemini_provider.py`.
- Phân tích 7 case FAIL của run v0 → bảng B2 (loại lỗi, tool call thực tế, nguyên nhân, cách sửa).
- Viết eval case nhóm trong `starter_v0/data/eval_group.json` (G02–G10, case G01 cho tool mới).
- Soạn Phần A (A1–A3) và khung bảng B1, B3 trong `report/team/group_report.md`.

## 4. Bằng chứng

- File/commit/PR: `starter_v0/data/eval_group.json`, `report/team/group_report.md`, `starter_v0/providers/gemini_provider.py` _(điền link commit sau khi push)_
- AI/công cụ đã dùng và cách tự kiểm tra kết quả: Dùng Claude để giải thích đề, hướng dẫn setup, gợi ý và soạn nháp eval case, phân tích run JSON. Tự kiểm tra bằng: chạy `pytest tests/test_tool_contract.py` (xanh), chạy thử `--suite group` để xác nhận file eval không lỗi schema, đối chiếu bảng B2 với `results[*].result.failures` trong run v0.

## 5. Tự đánh giá

_(Hà tự viết: mình học được gì, chỗ nào còn yếu, nếu làm lại sẽ làm khác gì.)_
