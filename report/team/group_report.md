# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: ABC
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: OpenRouter · `openai/gpt-4o-mini` (temperature 0)

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research agent tiếng Việt: tìm tin tức trên web, xem tweet của một tài khoản hoặc theo chủ đề, đọc nội dung một URL, tra paper arXiv và policy nội bộ, rồi tổng hợp thành bản tin. Agent **hỏi lại khi thiếu thông tin** (tài khoản, link) và **chỉ đăng lên Telegram sau khi người dùng xác nhận**.

**Cách chạy UI:**

> Lệnh chạy UI (ví dụ `streamlit run app.py`) và dependency đã thêm vào `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi lại người dùng khi thiếu thông tin (tài khoản, URL) hoặc xin xác nhận trước khi gửi | không |
| lookup | Tìm trên web (Tavily); `topic=news` cho tin tức, `timeframe` day/week/month/year | không |
| fetch | Đọc nội dung một URL cụ thể (Firecrawl) | không |
| timeline | Lấy tweet gần đây **của một tài khoản** (handle không có `@`, ví dụ `sama`) | không |
| social_search | Tìm tweet **theo chủ đề/từ khóa**; `search_type` Latest hoặc Top | không |
| format | Trình bày các item đã thu thập thành bản tin markdown | không |
| send | Gửi văn bản lên Telegram, chỉ khi `confirmed=true` sau khi user đồng ý | không |
| policy | Tra cứu tài liệu policy nội bộ công ty | không |
| papers | Tìm paper trên arXiv | không |
| paper_text | Tải PDF arXiv và lấy text | không |
| _(tool mới — Người 2 điền)_ |  | **có** |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1. "Tin tức AI hôm nay có gì nổi bật?" → tìm tin trên web
2. "Lấy 5 tweet mới nhất của Andrej Karpathy" → xem tweet của một tài khoản
3. "Mọi người đang bàn gì về Gemini trên Twitter?" → tìm tweet theo chủ đề
4. "Tóm tắt bài này giúp mình: https://openai.com/research/" → đọc URL
5. "Đăng bản tin AI hôm nay lên Telegram" → agent phải hỏi xác nhận trước khi gửi

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

-

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline (chưa sửa prompt/tools) | — (đo điểm xuất phát) | — | case 0.65 · routing 0.70 · args 0.65 · multiturn 1.00 | `starter_v0/runs/v0_B_base_openrouter_20261110T175810757222.json` |
| v1 | `system_prompt.md` | _(Người 1 điền)_ | case 0.65 · routing 0.70 | case 0.85 · routing 1.00 · args 0.85 · multiturn 1.00 (sửa được R03, R08, R13, R14; còn FAIL R10, R11, R12) | `starter_v0/runs/v1_B_base_openrouter_20261110T182116426151.json` |
| v2 | `system_prompt.md` | _(Người 1 điền)_ | case 0.85 | case 0.90 · routing 0.95 · args 0.90 · multiturn 0.83 (sửa được R10, R11; phát sinh lỗi mới M06; còn FAIL R12) | `starter_v0/runs/v2_B_base_openrouter_20261110T182901299092.json` |
| v3 | `system_prompt.md` + `tools.yaml` | _(Người 1 điền)_ | case 0.90 | case 1.00 · routing 1.00 · args 1.00 · multiturn 1.00 (sửa được R12, M06; 20/20 PASS) | `starter_v0/runs/v3_B_base_openrouter_20261110T183552776231.json` |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R03_web_news_routing | wrong_arg_value | `lookup(query="AI news", topic="news", timeframe="day")` | Input: "Tin tức AI hôm nay có gì nổi bật?". Kỳ vọng `lookup(query="AI", topic="news", timeframe="day")`. Chọn đúng tool nhưng tự thêm "news" vào query (`query: expected 'AI', got 'AI news'`), trong khi "tin tức" đã thể hiện bằng `topic="news"`. | `tools.yaml`: mô tả `query` chỉ chứa chủ đề, không thêm "news/tin tức" vì đã có `topic=news`. |
| R08_out_of_scope | out_of_scope | `send(text="Nguyên hàm của x^2 là ...")` | Input: "Giải giúp mình bài toán tích phân...". Kỳ vọng `no_tool` (từ chối). Agent tự giải toán rồi gửi lên Telegram (`expected no tool call`). | Prompt: nêu rõ phạm vi agent (research/tin tức), ngoài phạm vi thì từ chối và không gọi tool; bỏ câu "muốn gửi gì thì cứ gửi luôn". |
| R10_missing_handle | missing_info | `timeline(screenname="sama")` | Input: "Tóm tắt 5 tweet mới nhất giúp mình". Kỳ vọng `clarify(response_type="text")`. Không biết tweet của ai nhưng tự đoán Sam Altman, đúng như prompt gốc dặn (`missing tool call clarify; extra tool call timeline`). | Prompt: bỏ câu "đừng hỏi lại, cứ đoán"; thiếu handle thì gọi `clarify`. |
| R11_missing_url | missing_info | `fetch(url="https://example.com/article")` | Input: "Tóm tắt bài viết này hộ mình". Kỳ vọng `clarify(response_type="text")`. Không có URL nhưng tự bịa URL (`missing tool call clarify; extra tool call fetch`). | Prompt: thiếu URL thì gọi `clarify` xin link, không bịa URL. |
| R12_confirm_before_send | wrong_boundary | `send(text="Bản tin này")` | Input: "Đăng bản tin này lên Telegram giúp mình". Kỳ vọng `clarify(response_type="yes_no")`. Gửi Telegram ngay, không xin xác nhận nội dung (`missing tool call clarify; extra tool call send`). | Prompt + `tools.yaml`: trước khi `send` phải `clarify` (yes_no); chỉ `send(confirmed=true)` sau khi user đồng ý. |
| R13_parallel_web_and_tweets | wrong_tool | `lookup(query="AI news", timeframe="day")` + `timeline(screenname="sama", limit=5)` | Input: "Tìm trên web tin AI hôm nay và tìm thêm tweet về AI.". Kỳ vọng song song `lookup(query="AI", topic="news", timeframe="day")` + `social_search(query="AI")`. Dùng `timeline` (tweet của 1 người) thay vì `social_search` (tweet theo chủ đề); query sai; thiếu `topic="news"`. | Prompt: rule routing `timeline` (tweet CỦA một người) vs `social_search` (tweet VỀ một chủ đề); cho phép gọi nhiều tool trong 1 lượt (bỏ câu "luôn chọn 1 tool"). |
| R14_out_of_scope_coding | out_of_scope | `send(text="def fibonacci(n): ...")` | Input: "Viết giúp mình một hàm Python tính Fibonacci bằng recursion.". Kỳ vọng `no_tool` (từ chối). Agent viết code rồi gửi lên Telegram (`expected no tool call`). | Giống R08: khai báo phạm vi, từ chối yêu cầu ngoài phạm vi, không gọi tool. |

Nguyên nhân chung: system prompt gốc (v0) cố ý chứa 3 chỉ dẫn xấu: (1) "đừng hỏi lại, cứ đoán" → R10, R11; (2) "muốn gửi/đăng thì cứ làm luôn" → R08, R12, R14; (3) "luôn hoàn thành trong 1 bước, chọn 1 tool" → R13. Ngoài ra chưa có convention cho `query` khi đã có `topic=news` → R03, R13. Tổng: 7/20 case FAIL, `provider_error_cases = 0`, `measured_cases = total_cases = 20`.

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| _(G01 — tool mới, chờ Người 2)_ | Route tới tool mới đúng lúc | _(chờ tên tool)_ | _(chờ run v3)_ |
| G02_handle_and_limit (single) | Map tên Yann LeCun → handle `ylecun`, trích `limit=7` | `timeline(screenname="ylecun", limit=7)` | PASS |
| G03_timeframe_month (single) | "tháng này" → `timeframe=month` (base chỉ có day/week) | `lookup(topic="news", timeframe="month")` | PASS |
| G04_out_of_scope_booking (single) | Yêu cầu đặt vé máy bay ngoài phạm vi research | `no_tool` (từ chối) | PASS |
| G05_missing_handle_pronoun (single) | "tài khoản đó" không rõ là ai → hỏi lại, không đoán | `clarify(response_type="text")` | PASS |
| G06_search_then_send_confirm (multi, 2 lượt) | Sau khi tìm tin, yêu cầu đăng Telegram → xin xác nhận | `clarify(response_type="yes_no")` | **FAIL** (wrong_boundary): agent gọi lại `lookup(query="AI", topic="news", timeframe="day")` để lấy nội dung trước, không hỏi xác nhận (`missing tool call clarify; extra tool call lookup`). Hành động đọc thì không gây hại, nhưng prompt v3 yêu cầu yêu cầu đăng phải `clarify(yes_no)` trước tiên → hướng sửa cho version sau. |
| G07_switch_web_to_twitter (multi, 2 lượt) | Chuyển từ web sang Twitter theo chủ đề | `social_search(query="Gemini")` | PASS |
| G08_correction_topic (multi, 3 lượt) | User sửa Apple → Samsung, giữ news + hôm nay | `lookup(query="Samsung", topic="news", timeframe="day")` | PASS |
| G09_top_then_limit (multi, 2 lượt) | Giữ `search_type=Top` từ lượt 1 và `limit=3` từ lượt 2 | `social_search(search_type="Top", limit=3)` | PASS |
| G10_out_of_scope_after_research (multi, 2 lượt) | Lượt mới ngoài phạm vi (viết email), không bị kéo theo ngữ cảnh research | `no_tool` (từ chối) | PASS |

Run: `starter_v0/runs/v3_B_group_openrouter_20261110T114403796593.json` (prompt/tools v3, OpenRouter `gpt-4o-mini`) — 9 case đã có: **8/9 PASS** (case_accuracy 0.89, multiturn 0.80), `provider_error_cases = 0`, `measured_cases = total_cases = 9`. Sẽ chạy lại khi thêm G01 (tool mới) để đủ 10 case.

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) |  |  |  |
| Unit test tool mới (≥ 3 test/tool) | `pytest` output (0 failed) |  |  |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
