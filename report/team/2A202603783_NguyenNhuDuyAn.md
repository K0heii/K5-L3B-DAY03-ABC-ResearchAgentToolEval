# Báo cáo cá nhân — HoVaTen-MSSV

Đổi tên file theo quy tắc `MSSV_HoTen.md`.

Ví dụ: `20241234_NguyenVanAn.md`.

## 1. Thông tin thành viên

- Họ tên: Nguyễn Như Duy An
- MSSV: 2A202603783
- Email: 26ai.annnd@vinuni.edu.vn

## 2. Phần việc phụ trách

CP3 — Lập trình tool mới, `TOOL.md` và unit test.

## 3. Đóng góp cụ thể

Thiết kế và lập trình **4 tool mới** cho research agent:

**1. Tool `summarize`** — tóm tắt extractive một đoạn văn bản dài:
- Chấm điểm từng câu theo tần số từ khóa, bỏ stopword tiếng Anh và tiếng Việt, chọn ra các câu quan trọng nhất rồi giữ nguyên thứ tự gốc. 
- Tool chạy hoàn toàn local, không cần API key. Trả về error dict thay vì raise khi gặp input xấu (text không phải string, text rỗng, `max_sentences < 1`).

**2. Tool `keywords`** — trích từ khóa xuất hiện nhiều nhất trong văn bản:
- Đếm tần số từ, bỏ stopword (VN+EN), trả top N từ khóa kèm số lần xuất hiện.
- Hữu ích để tag nội dung từ fetch/paper_text trước khi lưu hoặc format.

**3. Tool `extract_links`** — trích danh sách URL từ văn bản hoặc items:
- Nhận diện markdown link `[title](url)` giữ được title, bare URL, và URL trong danh sách items từ lookup/timeline/papers.
- Khử trùng lặp, sửa bug regex URL đang bắt luôn dấu phẩy cuối (test suite phát hiện).

**4. Tool `merge_sources`** — gộp items từ nhiều nguồn, khử trùng lặp:
- Nhận `dedupe_key` (mặc định "url") để nhận item trùng, giữ bản có score cao hơn.
- Có thể sắp xếp theo score giảm dần. Hữu ích khi gọi song song lookup + social_search + papers rồi gộp lại trước khi format.

Mỗi tool có:
- `TOOL.md`
- Khai báo trong `artifacts/tools.yaml`
- 3 unit test: happy path, input xấu từ model (None/sai kiểu/rỗng), nhánh lỗi → error dict không raise.
- Đăng ký trong `tools/__init__.py` (`TOOL_FUNCTIONS`).

## 4. Bằng chứng

- File/commit/PR:

  **4 tool mới:**
  - [tools/summarize/tool.py](../../starter_v0/tools/summarize/tool.py) và [TOOL.md](../../starter_v0/tools/summarize/TOOL.md)
  - [tools/keywords/tool.py](../../starter_v0/tools/keywords/tool.py) và [TOOL.md](../../starter_v0/tools/keywords/TOOL.md)
  - [tools/extract_links/tool.py](../../starter_v0/tools/extract_links/tool.py) và [TOOL.md](../../starter_v0/tools/extract_links/TOOL.md)
  - [tools/merge_sources/tool.py](../../starter_v0/tools/merge_sources/tool.py) và [TOOL.md](../../starter_v0/tools/merge_sources/TOOL.md)

  Đăng ký và khai báo: [tools/__init__.py](../../starter_v0/tools/__init__.py) và [tools.yaml](../../starter_v0/artifacts/tools.yaml).

  Unit test: [test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py) (12 test cho 4 tool: `test_summarize_*`, `test_merge_sources_*`, `test_keywords_*`, `test_extract_links_*`).

  Kết quả tự kiểm tra: `pytest tests/ -v` báo **94 passed, 0 failed** (12 test của 4 tool mới đều passed; 14 test còn skip là stub của phần việc khác). `pytest tests/test_tool_contract.py` báo **75 passed** — bao gồm contract test cho 4 tool mới (có implementation, tham số khai báo khớp signature, mô tả không rỗng, TOOL.md có frontmatter đúng tên).

- AI/công cụ đã dùng và cách tự kiểm tra kết quả: Claude Code. Tôi nhờ AI đọc contract test (`test_tool_contract.py`) và các tool mẫu (`format`, `lookup`) để nắm pattern trả error dict, sau đó sinh bản đầu của 4 tool.py và unit test. Kết quả AI đề xuất được tự kiểm tra lại bằng cách: chạy `pytest` trên venv của project để xác nhận 0 failed. Test suite còn bắt được 1 bug thật trong `extract_links` (regex URL bắt luôn dấu phẩy cuối `https://b.com/2,`) mà AI không phát hiện, tôi tự sửa regex loại trừ dấu phẩy. Kiểm tra khai báo trong `tools.yaml` khớp signature hàm bằng chính contract test của lab (chạy xanh là bằng chứng). Tự rà soát và bổ sung mô tả "không dùng khi..." cho 4 tool theo rubric C2.

## 5. Tự đánh giá

Qua phần việc này tôi hiểu rõ sự khác nhau giữa unit test và eval: unit test đo code của tool chạy đúng (logic, input xấu, nhánh lỗi), còn eval đo lựa chọn của model (route đúng tool, truyền đúng tham số). Tôi cũng hiểu vì sao tool nên trả error dict thay vì raise: agent loop có thể tự bắt lỗi và cho model thấy nguyên nhân, để model chỉnh tham số và thử lại thay vì làm hỏng cả lượt chạy. Cách làm này tôi sẽ áp dụng lại khi viết tool cho các dự án sau.
