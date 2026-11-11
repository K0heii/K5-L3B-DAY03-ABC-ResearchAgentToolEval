# Team

## Thông tin nhóm

- Tên nhóm: ABC
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-ABC-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo và nhánh nộp: https://github.com/K0heii/K5-L3B-DAY03-ABC-ResearchAgentToolEval — `main`.
- Commit chốt duy nhất — **v5 đã sửa**: [commit mới nhất trên main](https://github.com/K0heii/K5-L3B-DAY03-ABC-ResearchAgentToolEval/commit/main). Liên kết dùng ref `main` để luôn trỏ tới commit cuối cùng đã push, kể cả commit cập nhật tài liệu; mã SHA cụ thể được ghi trong lịch sử GitHub. Bản chốt có base 20/20 và group 10/10; các run v5 ban đầu 19/20 vẫn được giữ làm lịch sử.

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Như Duy An | 2A202603783| 26ai.annnd@vinuni.edu.vn | K0heii | Nhóm trưởng · CP3: 4 tool mới + unit test |
|   2 | Nguyễn Đức Minh | 2A202603765 | 26ai.minhnd5@vinuni.edu.vn | miao1114 | Thành viên · CP1–CP2: baseline, tối ưu prompt/tools v1–v5 và kiểm thử hồi quy |
|   3 | Phạm Thế Hùng | 2A202603778 | 26ai.hungpt5@vinuni.edu.vn | thehung1406 | CP5: UI Streamlit, tích hợp agent, transcript |
|   4 | Trương Thị Thu Hà | 2A202603780 | 26ai.hattt@vinuni.edu.vn | TruongThuHa | Người 4: eval nhóm (CP4) + tổng hợp báo cáo nhóm |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## NguyenNhuDuyAn-2A202603783

### Phần việc phụ trách

- Nhóm trưởng; CP3 — lập trình tool mới, `TOOL.md` và unit test.

### Đóng góp cụ thể

- Viết 4 tool mới chạy cục bộ: `summarize`, `keywords`, `extract_links`, `merge_sources`; mỗi tool có `TOOL.md`, đăng ký trong `tools/__init__.py` và `artifacts/tools.yaml` (có mô tả "khi nào không dùng").
- Viết 12 unit test (3 test/tool: happy path, input xấu, nhánh lỗi trả error dict); test bắt được bug regex URL dính dấu phẩy trong `extract_links` và đã sửa.

### Bằng chứng

- `starter_v0/tools/{summarize,keywords,extract_links,merge_sources}/`, `starter_v0/tests/test_tools_todo.py`; `pytest`: 94 passed, 0 failed.
- Báo cáo cá nhân: `report/team/2A202603783_NguyenNhuDuyAn.md`.

## NguyenDucMinh-2A202603765

### Phần việc phụ trách

- CP1–CP2 — chạy baseline v0, phân tích lỗi và tối ưu prompt/tool declaration v1–v5.
- Chạy lại base và bộ group của nhóm để kiểm tra hồi quy; cập nhật run JSON, CSV, version log và bằng chứng trong báo cáo.
- Bổ sung xử lý ngày giờ Việt Nam, kiểm tra ngày đích khi tìm xổ số và sửa lỗi log Unicode trên Windows.

### Đóng góp cụ thể

- Chạy v0 (0.65), phân tích case lỗi và sửa prompt/tools qua v1 (0.85), v2 (0.90), v3 (1.00 trên 20 case base).
- Chạy lại v3 sau khi thêm `summarize` (20/20) và bộ kiểm tra riêng fetch/summarize (2/2); ghi `version_log.csv`.
- Thực hiện v4 với một giả thuyết: thêm đúng một câu vào bước 1 để xin xác nhận trước khi đăng/gửi sau lượt tìm kiếm; base 20/20, group 10/10 và G06 PASS. Bằng chứng và lỗi kết nối ban đầu: [v4_summary.md](starter_v0/analysis/v4_summary.md).
- Bổ sung v5 xử lý ngày tháng: tool `calendar`, `target_date` cho `lookup`, kiểm tra ngày đích trong chat và sửa log Unicode. Viết test đổi tháng/năm, năm nhuận, hôm qua/hôm kia và chặn truy vấn sai ngày; toàn suite đạt 121 passed, 14 skipped. [Lần chạy v5 ban đầu](starter_v0/runs/v5_B_base_openrouter_20261111T112032802355.json) đạt 19/20, phát hiện hồi quy R01.
- Sửa tiếp v5: không hỏi tham số tùy chọn có mặc định và làm rõ ánh xạ tên sang handle. Bản mới đạt [base 20/20](starter_v0/runs/v5_B_base_openrouter_20261111T114616307841.json) và [group 10/10](starter_v0/runs/v5_B_group_openrouter_20261111T114714485359.json); CSV v5 hiện dẫn tới các run mới, giữ run 19/20 làm lịch sử.
- Đối chiếu kết quả group v5 với version log và bổ sung cột v5 trong B3 của báo cáo nhóm; phân biệt kết quả v4 làm mốc với các lần thử và sửa hồi quy của v5.

### Bằng chứng

- Prompt, tool và lịch sử thử nghiệm: [system_prompt.md](starter_v0/artifacts/system_prompt.md), [tools.yaml](starter_v0/artifacts/tools.yaml), [version_log.csv](starter_v0/artifacts/version_log.csv).
- Xử lý ngày tháng và kiểm tra: [calendar](starter_v0/tools/calendar/tool.py), [lookup](starter_v0/tools/lookup/tool.py), [chat.py](starter_v0/chat.py), [test ngày tháng](starter_v0/tests/test_calendar_dates.py), [test log Unicode](starter_v0/tests/test_tools_examples.py).
- Kết quả v5 mới nhất: [CSV base](starter_v0/analysis/base_runs_v5.csv), [CSV group](starter_v0/analysis/group_runs_v5.csv); liên kết run chi tiết ở trên.
- Báo cáo cá nhân: [Nguyễn Đức Minh](report/team/2A202603765_NguyenDucMinh.md).

## PhamTheHung-2A202603778

### Phần việc phụ trách

- CP5 — giao diện Streamlit, tích hợp agent, lưu transcript.

### Đóng góp cụ thể

- Xây dựng UI chat Streamlit (lịch sử hội thoại, cấu hình provider/model, hiển thị tool call và lỗi), nối với vòng lặp agent của `chat.py`.
- Tự động lưu transcript JSON mỗi lượt (provider/model, version, hash prompt/tool, tool events); chạy phiên chat 5 lượt gồm yêu cầu thường, thiếu thông tin rồi bổ sung, yêu cầu gửi Telegram có xác nhận.

### Bằng chứng

- `starter_v0/app.py`, `ui_agent.py`, `ui_transcripts.py`, `.streamlit/config.toml`, `starter_v0/transcripts/*.transcript.json`; chạy bằng `python -m streamlit run app.py`.
- Báo cáo cá nhân: `report/team/2A202603778_PhamTheHung.md`.

## TruongThiThuHa-2A202603780

### Phần việc phụ trách

- CP4 — 10 eval case nhóm và chạy `--suite group`; tổng hợp báo cáo nhóm.

### Đóng góp cụ thể

- Viết 10 eval case (5 single + 5 multi turn, phủ 5 loại lỗi, G01 route tới tool mới `summarize`); chạy trên v3 được 9/10, case G06 phát hiện lỗi xác nhận trước khi đăng mà bộ base không bắt được.
- Phân tích 7 case FAIL của v0 (bảng B2); tổng hợp `group_report.md` (Phần A, B1–B5a, Giải pháp, Khó khăn, Reflection); đổi model mặc định Gemini do lỗi 503.

### Bằng chứng

- `starter_v0/data/eval_group.json`, `starter_v0/runs/v3_B_group_openrouter_20261110T182345441573.json`, `report/team/group_report.md`.
- Báo cáo cá nhân: `report/team/2A202603780_TruongThiThuHa.md`.
