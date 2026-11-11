# Rà soát trước khi push — 11/11/2026 (GMT+7)

Đối chiếu `README.md`, `starter_v0/README.md`, `RULES.md` và `SUBMISSION.md`. Đây là kết quả kiểm tra trong repo, không xác nhận việc nộp LMS hoặc thời hạn gia hạn.

## Các mục đã kiểm tra

- Repo đúng mẫu `K5-L3B-DAY03-ABC-ResearchAgentToolEval`, nhánh `main`.
- [TEAM.md](../../TEAM.md) có đủ 4 thành viên và phân công. Có đủ 4 báo cáo cá nhân đúng tên MSSV; lịch sử Git có commit kỹ thuật của các thành viên.
- [Báo cáo nhóm](group_report.md) có Phần A, kết quả v0–v3, phân tích lỗi, 10 case nhóm, transcript, UI, tool mới và phần hạn chế. Đã bổ sung kết quả v4 và giữ nhận xét v3 làm lịch sử.
- Prompt/tool declaration đồng bộ với implementation và contract test. V4 chỉ thêm một câu ở bước 1 của prompt; không sửa tool hoặc code chấm.
- [Version log](../../starter_v0/artifacts/version_log.csv) có 7 dòng dữ liệu: v0, v1, v2, hai lần v3 và hai suite v4. Mọi dòng khớp version/hash/điểm/đường dẫn JSON; chỉ dẫn tới run đủ case và không có lỗi provider.
- V4 base **20/20**, group **10/10**, G06 gọi `clarify(response_type="yes_no")`. Hai run hợp lệ không có lỗi `tool_results`. [Phân tích và giới hạn so sánh](../../starter_v0/analysis/v4_summary.md).
- [Eval nhóm](../../starter_v0/data/eval_group.json) đúng **10 ca: 5 single turn + 5 multi turn**, có G01 kiểm tra tool mới `summarize` và 5 nhóm lỗi.
- Cả `data/eval_base.json` và `data/eval_research_extension.json` khớp nội dung bản đề gốc ở commit `fbab62d` sau chuẩn hóa xuống dòng.
- Bốn tool mới `summarize`, `keywords`, `extract_links`, `merge_sources` có `tool.py`, `TOOL.md`, đăng ký và schema; mỗi tool có **3 test** trong `tests/test_tools_todo.py`.
- Chạy `..\.venv\Scripts\python.exe -m pytest -q` trong `starter_v0`: **94 passed, 14 skipped, 0 failed**. Các test skip là stub TODO của tool có sẵn, không phải 12 test của tool mới.
- UI có `app.py`, `ui_agent.py`, `ui_transcripts.py`, cấu hình Streamlit và dependency trong `requirements.txt`; báo cáo có lệnh chạy. Đã cài dependency vào `.venv` của máy và kiểm tra khởi động bằng `streamlit.testing.v1.AppTest`: **0 exception, 1 ô chat**. Đây là kiểm tra khởi động, không phải một phiên live chat mới hoặc kiểm tra deploy.
- Có 3 transcript JSON live với lần lượt **3, 5 và 1 lượt**. Báo cáo dẫn bằng chứng yêu cầu thường, thiếu thông tin rồi bổ sung, yêu cầu gửi Telegram và người dùng hủy gửi.
- Đã rà các file tracked và file mới không bị ignore: không thấy key đang cấu hình trong `.env`, token phổ biến hoặc private key. `.env`, `.venv`, cache và `arxiv_papers/` được loại khỏi commit.
- Đã kiểm tra metadata run, cấu trúc CSV, dấu tiếng Việt UTF-8, đường dẫn bằng chứng v4 và `git diff --check`.

## Những điểm chưa xác nhận hoặc chưa đạt bonus

- Mục link demo public trong A1 chưa điền. UI đã kiểm tra chạy trong môi trường máy, chưa triển khai public trong lượt rà soát này.
- Cần nhóm tự xác nhận người chấm truy cập được repo, từng thành viên đã nộp LMS đúng hạn và thông báo gia hạn của coach.
- Còn **14 test skipped**: chưa đạt bonus toàn suite 0 skipped; không phải lỗi ở yêu cầu 0 failed và 3 test/tool mới.
- Chưa có bằng chứng chạy hai model local hoặc gửi Telegram thành công sau xác nhận; không ghi nhận các bonus đó là đã hoàn thành.
- Bộ group chỉ có `summarize` đại diện cho tool mới. Ba tool mới còn lại có unit test nhưng chưa có ca routing riêng trong bộ group; cần lưu ý nếu yêu cầu bonus có điều kiện bổ sung.
- Lỗi live chat hỏi bằng chữ thay vì gọi `clarify` trong transcript B2 vẫn được ghi là hạn chế; các ca eval hỏi lại đạt không chứng minh lỗi live chat này đã được sửa.
- Hai run v4 đầu có lỗi kết nối provider được giữ làm log kỹ thuật; không dùng làm số liệu tối ưu trong version log. Chỉ dùng hai run v4 đầy đủ sau khi chạy lại.
- Hash cấu hình của các mốc v3 và v4 có khác biệt, nên so sánh lịch sử không tách riêng hoàn toàn tác động của câu thêm vào v4. Không chạy lại v3 theo yêu cầu của thành viên.

Không đánh dấu các mục chưa xác nhận là đã hoàn thành và không thay nội dung hướng dẫn/chấm điểm để làm checklist đạt.
