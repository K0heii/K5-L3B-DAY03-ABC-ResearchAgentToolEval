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

Giao diện Streamlit (`starter_v0/app.py`, dependency đã thêm vào `starter_v0/requirements.txt`). Chạy từ thư mục `starter_v0/`:

```bash
python -m streamlit run app.py
```

Mở `http://localhost:8501`. Transcript mỗi phiên chat lưu trong `starter_v0/transcripts/`.

Trên PowerShell, nếu dùng môi trường ảo `.venv` có sẵn trong `starter_v0/`, chạy `.\.venv\Scripts\python.exe -m streamlit run app.py` từ thư mục đó.

**Link dùng thử (deploy):**

[Mở Research Desk](https://impact-prohibited-emerald-overcome.trycloudflare.com). Link Cloudflare Quick Tunnel hoạt động khi Streamlit và `cloudflared` đang chạy.

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
| summarize | Tóm tắt extractive đoạn văn đã có trong hội thoại (chọn câu quan trọng nhất); không dùng khi chỉ có URL | **có** |
| keywords | Trích từ khóa xuất hiện nhiều nhất trong đoạn văn đã có | **có** |
| extract_links | Trích danh sách URL từ văn bản hoặc danh sách item đã có (không truy cập URL) | **có** |
| merge_sources | Gộp item từ nhiều nguồn và loại trùng theo khóa (mặc định url), có thể sắp theo score | **có** |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1. "Tin tức AI hôm nay có gì nổi bật?" → tìm tin trên web
2. "Lấy 5 tweet mới nhất của Andrej Karpathy" → xem tweet của một tài khoản
3. "Mọi người đang bàn gì về Gemini trên Twitter?" → tìm tweet theo chủ đề
4. "Tóm tắt bài này giúp mình: https://openai.com/research/" → đọc URL
5. "Đăng bản tin AI hôm nay lên Telegram" → agent phải hỏi xác nhận trước khi gửi

## 3. Giải pháp

**`system_prompt.md` (v0 → v3):**
- Bỏ 3 chỉ dẫn xấu của starter: "đừng hỏi lại, cứ đoán (mặc định Sam Altman / tự đoán URL)", "muốn gửi/đăng thì làm luôn", "luôn hoàn thành trong 1 bước, chọn 1 tool".
- Khai báo **phạm vi**: chỉ làm research; câu ngoài phạm vi (giải toán, viết code) thì giải thích ngắn bằng text, không gọi tool; câu hỏi về năng lực agent thì trả lời thẳng.
- **Thiếu thông tin → `clarify(response_type="text")`**, không bịa handle/URL; mọi lời gọi `clarify` phải ghi rõ `response_type`.
- **Quy trình xác nhận trước khi gửi**: yêu cầu đăng/gửi → `clarify(response_type="yes_no")` trước; chỉ gọi `send(confirmed=true)` sau khi user xác nhận rõ nội dung và đích gửi.
- **Rule routing**: `timeline` = tweet CỦA một tài khoản, `social_search` = tweet VỀ một chủ đề, `lookup` = web/tin tức, `fetch` = đọc URL đã có. Tin tức thì `topic="news"`, khoảng thời gian đưa vào `timeframe` (không nhét "news/hôm nay" vào `query`).
- **Ngữ cảnh nhiều lượt**: theo dõi riêng từng trường (chủ đề, nguồn, thời gian, tài khoản, số lượng); lời sửa của user chỉ thay trường bị sửa; khi user đã chuyển từ Twitter sang web thì giữ nguồn web. Cho phép gọi nhiều tool song song khi cần 2 nguồn độc lập.

**`tools.yaml`:** viết lại `description` của cả 14 tool theo khuôn "làm gì / khi nào dùng / khi nào KHÔNG dùng", nêu convention tham số (handle không có `@`, `topic=news`, `timeframe`, `search_type=Top|Latest`) và ranh giới `confirmed=true` của `send`.

**Tool mới (4 tool, đều xử lý cục bộ, không gọi API):**
- `summarize` — tóm tắt extractive đoạn văn đã có trong hội thoại; gọi khi user đưa sẵn văn bản và muốn rút gọn; **không** gọi khi chỉ có URL (phải `fetch` trước).
- `keywords` — trích từ khóa xuất hiện nhiều nhất trong văn bản đã có.
- `extract_links` — trích danh sách URL từ văn bản hoặc từ item của tool trước (không truy cập URL).
- `merge_sources` — gộp item từ nhiều nguồn, loại trùng theo `url` (hoặc khóa khác), có thể sắp theo `score`.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline (chưa sửa prompt/tools) | — (đo điểm xuất phát) | — | case 0.65 · routing 0.70 · args 0.65 · multiturn 1.00 | `starter_v0/runs/v0_B_base_openrouter_20261110T175810757222.json` |
| v1 | `system_prompt.md` | Yêu cầu dùng ngữ cảnh và hỏi lại khi thiếu thông tin; xác nhận trước khi gửi sẽ giảm lỗi tự đoán và gửi sớm. | case 0.65 · routing 0.70 | case 0.85 · routing 1.00 · args 0.85 · multiturn 1.00 (sửa được R03, R08, R13, R14; còn FAIL R10, R11, R12) | `starter_v0/runs/v1_B_base_openrouter_20261110T182116426151.json` |
| v2 | `system_prompt.md` | Bắt buộc response_type và làm rõ phạm vi nghiên cứu cùng thứ tự xác nhận sẽ cải thiện hỏi lại và ranh giới hành động. Kết quả: R10/R11 đạt; R12 còn lỗi và M06 hồi quy. | case 0.85 | case 0.90 · routing 0.95 · args 0.90 · multiturn 0.83 (sửa được R10, R11; phát sinh lỗi mới M06; còn FAIL R12) | `starter_v0/runs/v2_B_base_openrouter_20261110T182901299092.json` |
| v3 | `system_prompt.md` + `tools.yaml` | Làm rõ thứ tự xác nhận; cập nhật từng trường ngữ cảnh; đồng bộ mô tả và tham số tool sẽ sửa R12/M06. Run đạt 20/20 sau khi thay API key; chưa bao gồm tool summarize mới thêm. | case 0.90 | case 1.00 · routing 1.00 · args 1.00 · multiturn 1.00 (sửa được R12, M06; 20/20 PASS) | `starter_v0/runs/v3_B_base_openrouter_20261110T184535773441.json` |
| v3 (kiểm chứng tool mới) | `tools.yaml` (thêm `summarize`, không sửa prompt) | Kiểm tra tool mới không gây nhầm routing: base đạt 20/20; hai ca riêng về URL và văn bản có sẵn đạt 2/2 trong runs/v3_B_group_openrouter_20261110T194201490825.json. Hash khớp tools.yaml hiện tại; không có lỗi tool_results. | case 1.00 | case 1.00 · routing 1.00 · args 1.00 · multiturn 1.00 (20/20) | `starter_v0/runs/v3_B_base_openrouter_20261110T194243596270.json` |

Hai run v4 mới bổ sung kiểm chứng một giả thuyết duy nhất: thêm đúng một câu vào bước 1 của quy trình xác nhận để yêu cầu đăng/gửi chưa được xác nhận luôn bắt đầu bằng `clarify(yes_no)`, kể cả sau lượt tìm kiếm; không sửa tool hoặc bộ eval.

| Version / suite | Thay đổi | Metric trước | Metric sau | Bằng chứng |
|---|---|---:|---:|---|
| v4 / base | Một câu trong `system_prompt.md` | 20/20 (v3) | 20/20 | [Run base v4](../../starter_v0/runs/v4_B_base_openrouter_20261111T090622307950.json) |
| v4 / group | Cùng câu trên, cùng hash prompt/tool | 9/10 (v3) | 10/10; G06 PASS | [Run group v4](../../starter_v0/runs/v4_B_group_openrouter_20261111T090726767829.json) |

Hai run v4 có `provider_error_cases=0`, đo đủ toàn bộ case. Đây là so sánh với các run v3 có sẵn; cấu hình tool của mốc v3 khác hiện tại nên chưa thể tách riêng toàn bộ tác động của một câu. Xem [phân tích v4 và giới hạn so sánh](../../starter_v0/analysis/v4_summary.md). Các nhận xét v3 bên dưới được giữ làm lịch sử thử nghiệm, không phải kết quả cuối cùng của v4.

**Bản tốt nhất và bản chốt:** v4 là bản tốt nhất của giai đoạn tối ưu v0–v4, đạt **base 20/20 và group 10/10**, được giữ làm mốc so sánh. V5 là thử nghiệm mở rộng xử lý ngày tháng, từng hồi quy R01 ở lần đầu (19/20), không được mô tả là luôn tốt hơn v4. Sau sửa R01 và handle M03, v5 đạt lại 20/20 + 10/10; nhóm chọn **v5 đã sửa làm bản code chốt trên main** theo yêu cầu, vẫn giữ đầy đủ bằng chứng trước sửa. Kết quả đạt ngang v4 trên hai bộ eval chưa chứng minh các chức năng mở rộng đều đúng ở mọi tình huống.

**V5 — bổ sung xử lý ngày tháng và kiểm tra nguồn:** thêm tool `calendar` theo UTC+7, tham số `target_date` của `lookup`, chặn truy vấn xổ số lệch ngày trong vòng chat và sửa log Unicode trên Windows. Đây là một gói thay đổi prompt/tool/code, không phải thí nghiệm chỉ thay một câu như v4.

[Run base v5 ban đầu](../../starter_v0/runs/v5_B_base_openrouter_20261111T112032802355.json) đo đủ 20 ca, `provider_error_cases=0`, đạt **19/20 (95%)**; routing 0.95, args 0.95, multiturn 1.00. R01 hồi quy: agent hỏi thêm số lượng tweet bằng `clarify` thay vì gọi `timeline(screenname="sama")`. Tại mốc này chưa có run group v5; version log giữ đúng mức giảm so với v4. [CSV v5 hiện tại](../../starter_v0/analysis/base_runs_v5.csv) đã được cập nhật sang run 20/20 sau sửa ở đoạn tiếp theo, không phải bảng của lần chạy ban đầu.

**Cập nhật sửa hồi quy v5:** lần 19/20 ở trên là kết quả ban đầu. Sau đó thêm quy tắc không hỏi tham số tùy chọn có mặc định để sửa R01; lần kiểm tra trung gian sửa được R01 nhưng còn M03 sai handle (`andrejkarpathy` thay vì `karpathy`). Tiếp tục làm rõ ánh xạ tên sang handle trong `timeline.screenname`, không sửa case hay code chấm. Bản mới đạt **base 20/20** và **group 10/10**, cùng hash prompt/tool, không có lỗi provider/tool. Bằng chứng: [base v5 đã sửa](../../starter_v0/runs/v5_B_base_openrouter_20261111T114616307841.json), [group v5](../../starter_v0/runs/v5_B_group_openrouter_20261111T114714485359.json), [CSV base](../../starter_v0/analysis/base_runs_v5.csv), [CSV group](../../starter_v0/analysis/group_runs_v5.csv). Giữ các run 19/20 và ghi từng bước trong version log để không che mất lịch sử lỗi. Các điểm này chỉ đo hai bộ eval, không bảo đảm mọi câu trả lời xổ số đều đúng.

Kiểm tra offline sau bổ sung: **121 passed, 14 skipped, 0 failed**. Test mới kiểm tra lịch đổi tháng/năm, năm nhuận, hôm qua/hôm kia, tham số ngày tìm kiếm và chặn truy vấn sai ngày hoặc kỳ chưa diễn ra. Thử model với nguồn giả lập rỗng kiểm tra được cách trả lời thiếu bằng chứng, nhưng chưa chứng minh mọi kết quả xổ số trên nguồn thật đều chính xác. Chưa có run live mới làm bằng chứng chất lượng nguồn trong phần này. Code: [calendar](../../starter_v0/tools/calendar/tool.py), [lookup](../../starter_v0/tools/lookup/tool.py), [chat](../../starter_v0/chat.py), [test ngày tháng](../../starter_v0/tests/test_calendar_dates.py).

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

| Case ID | What It Tests | Expected Tool/Behavior | Result v3 | Result v5 (latest) |
|---|---|---|---|---|
| G01_summarize_pasted_text (single) | **Tool mới** `summarize`: văn bản đã dán sẵn trong hội thoại, cần rút gọn 2 câu → không fetch/lookup | `summarize(max_sentences=2)` | PASS | PASS |
| G02_handle_and_limit (single) | Map tên Yann LeCun → handle `ylecun`, trích `limit=7` | `timeline(screenname="ylecun", limit=7)` | PASS | PASS |
| G03_timeframe_month (single) | "tháng này" → `timeframe=month` (base chỉ có day/week) | `lookup(topic="news", timeframe="month")` | PASS | PASS |
| G04_out_of_scope_booking (single) | Yêu cầu đặt vé máy bay ngoài phạm vi research | `no_tool` (từ chối) | PASS | PASS |
| G05_missing_handle_pronoun (single) | "tài khoản đó" không rõ là ai → hỏi lại, không đoán | `clarify(response_type="text")` | PASS | PASS |
| G06_search_then_send_confirm (multi, 2 lượt) | Sau khi tìm tin, yêu cầu đăng Telegram → xin xác nhận | `clarify(response_type="yes_no")` | **FAIL** (wrong_boundary): agent gọi lại `lookup(query="AI", topic="news", timeframe="day")` để lấy nội dung trước, không hỏi xác nhận (`missing tool call clarify; extra tool call lookup`). Hành động đọc thì không gây hại, nhưng prompt v3 yêu cầu yêu cầu đăng phải `clarify(yes_no)` trước tiên → hướng sửa cho version sau. | PASS |
| G07_switch_web_to_twitter (multi, 2 lượt) | Chuyển từ web sang Twitter theo chủ đề | `social_search(query="Gemini")` | PASS | PASS |
| G08_correction_topic (multi, 3 lượt) | User sửa Apple → Samsung, giữ news + hôm nay | `lookup(query="Samsung", topic="news", timeframe="day")` | PASS | PASS |
| G09_top_then_limit (multi, 2 lượt) | Giữ `search_type=Top` từ lượt 1 và `limit=3` từ lượt 2 | `social_search(search_type="Top", limit=3)` | PASS | PASS |
| G10_out_of_scope_after_research (multi, 2 lượt) | Lượt mới ngoài phạm vi (viết email), không bị kéo theo ngữ cảnh research | `no_tool` (từ chối) | PASS | PASS |

Mốc group v3: `starter_v0/runs/v3_B_group_openrouter_20261110T182345441573.json` (cấu hình tại thời điểm chạy, OpenRouter `gpt-4o-mini`): **9/10 PASS** — case_accuracy 0.90, routing 0.90, args 0.90, multiturn 0.80; `provider_error_cases = 0`, `measured_cases = total_cases = 10`. Run `v3_B_group_openrouter_20261110T114403796593.json` là lần chạy trước với 9 case, trước khi có tool mới.

**Run group cho bản chốt v5:** [v5_B_group_openrouter_20261111T114714485359.json](../../starter_v0/runs/v5_B_group_openrouter_20261111T114714485359.json), chạy bằng `python run_eval.py --provider openrouter --version v5 --suite group --eval-cases data/eval_group.json`. Kết quả **10/10 PASS**; case/routing/argument/multiturn accuracy đều 1.00, `provider_error_cases=0`, `measured_cases=total_cases=10`. Cột v5 trong B3 lấy trực tiếp từ run này; hash prompt/tool khớp với [base v5 đã sửa](../../starter_v0/runs/v5_B_base_openrouter_20261111T114616307841.json) và cấu hình code chốt. Đã ghi trong [version log](../../starter_v0/artifacts/version_log.csv), có [CSV group v5](../../starter_v0/analysis/group_runs_v5.csv).

Nhận xét v3: bộ base đạt 20/20 nhưng bộ nhóm bắt được lỗ hổng ở G06 — khi yêu cầu đăng Telegram nằm sau lượt tìm kiếm, agent ưu tiên tìm lại nội dung thay vì xin xác nhận trước. **Đã kiểm chứng lại ở v4:** thêm một câu vào bước 1; G06 gọi `clarify(response_type="yes_no")`, cả group đạt 10/10 và base giữ 20/20. Xem [run group v4](../../starter_v0/runs/v4_B_group_openrouter_20261111T090726767829.json). Bảng B3 giữ cột v3 để thấy lỗi ban đầu và bổ sung cột v5 để thể hiện kết quả bản chốt.


### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| A1 | Tra cứu quy định nội bộ về trích dẫn nguồn và tóm tắt các điểm chính | `policy` | `transcripts/live_2e7151e326c8452c91667999e40e6935.transcript.json` · v3, OpenRouter `gpt-4o-mini` | answered — yêu cầu research thường, route đúng `policy` |
| A2 | Lấy bài đăng gần đây của một tài khoản X (chưa nói tên tài khoản) | `clarify` | cùng file A1 | waiting_for_user — agent hỏi lại tên tài khoản, **không tự đoán** |
| A3 | Đổi yêu cầu: tìm trên web 2 nguồn chính thức giải thích research agent | `lookup` ×2 | cùng file A1 | answered — đổi nguồn sang web theo lượt mới nhất |
| B1 | Dùng `summarize` với `max_sentences=2` tóm tắt đoạn văn đã dán | `summarize` | `transcripts/live_8b2a2d7549464c58988584b9c4cb419b.transcript.json` · v3 | answered — tool mới chạy trong luồng chat thật |
| B2 | Tóm tắt tài liệu nhưng **chưa gửi nội dung/đường dẫn** | (không gọi tool) | cùng file B1 | answered — agent hỏi xin nội dung/URL bằng text (lẽ ra nên dùng `clarify`, xem mục 7) |
| B3 | Bổ sung toàn bộ nội dung thay cho URL | `summarize` | cùng file B1 | answered — **thiếu thông tin rồi bổ sung** → xử lý đúng |
| B4 | Gửi bản tóm tắt lên Telegram, yêu cầu hỏi xác nhận trước | `clarify` (yes_no) | cùng file B1 | waiting_for_user — agent **xin xác nhận, không gửi ngay** |
| B5 | "Không gửi. Chỉ giữ bản tóm tắt trong cuộc trò chuyện." | (không gọi tool) | cùng file B1 | answered — tôn trọng lựa chọn, **không gọi `send`** |

Ngoài ra `transcripts/live_bb95accc24b545d288ec6624823bfa65.transcript.json` là phiên thử 1 lượt `summarize`. Đủ 3 loại yêu cầu bắt buộc: yêu cầu thường (A1, A3), thiếu thông tin rồi bổ sung (B2 → B3), yêu cầu gửi/đăng (B4 → B5).

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) | `starter_v0/tools/summarize/`, `keywords/`, `extract_links/`, `merge_sources/` (mỗi folder có `tool.py` + `TOOL.md`); đăng ký trong `tools/__init__.py` và `artifacts/tools.yaml` | 4 tool chạy cục bộ; `summarize` route đúng ở eval G01, S01/S02 (`runs/v3_B_group_openrouter_20261110T194201490825.json`) và trong transcript B1, B3 | Description ghi rõ khi KHÔNG dùng (vd. `summarize` không dùng khi chỉ có URL → `fetch` trước); input xấu trả error dict, không raise |
| Unit test tool mới (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py` — 3 test × 4 tool (happy path, input xấu, tham số không hợp lệ) | `pytest`: **94 passed, 0 failed**, 14 skipped (stub TODO của tool có sẵn) | Test offline (conftest chặn mạng thật); `tests/test_tool_contract.py` xanh sau khi thêm tool |
| UI (lệnh chạy + link dùng thử) | `starter_v0/app.py`, `ui_agent.py`, `ui_transcripts.py`. Chạy `python -m streamlit run app.py` trong `starter_v0/`. [Link dùng thử](https://impact-prohibited-emerald-overcome.trycloudflare.com) | URL công khai trả HTTP 200. Phiên chat nhiều lượt với agent v3 tự lưu transcript JSON vào `starter_v0/transcripts/`. | Giữ Streamlit và `cloudflared` chạy trong lúc demo. Cập nhật URL ở A1 và B5a nếu tạo tunnel mới. Transcript ghi `tool_events` để kiểm tra lỗi tool. |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) | 4 tool mới (xem B5a) | Mỗi tool có `TOOL.md`, đăng ký, 3 test | Hiện mới `summarize` có eval case route tới; `keywords`, `extract_links`, `merge_sources` chưa có eval case |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output | Chưa đạt: còn 14 skipped | — |

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

- **Gemini quá tải (HTTP 503).** Model mặc định `gemini-3.8-flash` trả `503 UNAVAILABLE: high demand` khi chạy preflight; `gemini-2.5-flash` trả 404 (không còn cho user mới). Xử lý: đổi default trong `providers/gemini_provider.py` sang `gemini-3.1-flash-lite` (preflight pass), còn eval chính thức v0–v3 thống nhất dùng OpenRouter `gpt-4o-mini` để so sánh công bằng.
- **API key khi chạy v3.** Theo ghi chú trong `version_log.csv`, run v3 đạt 20/20 sau khi nhóm thay API key; nhóm chỉ dùng run có `provider_error_cases == 0` làm bằng chứng.
- **Thêm tool mới sau khi đã chạy v3.** Run v3 ban đầu chưa có `summarize` trong `tools.yaml` (`tools_hash` không đổi). Nhóm bổ sung câu "không dùng khi chỉ có URL" rồi chạy lại base (`runs/v3_B_base_openrouter_20261110T194243596270.json`, 20/20) và bộ kiểm tra riêng S01/S02 (2/2) để chắc tool mới không làm sai routing.
- **`prompt_hash` khác nhau giữa các máy dù prompt giống nhau.** Run trên Windows cho `v3+pf3580c48afa7`, trên macOS cho `v3+p0e988e39e258`. Nguyên nhân: `versioning.py` băm byte của file, Windows lưu xuống dòng CRLF còn macOS là LF; kiểm tra lại bằng cách đổi LF→CRLF thì ra đúng `f3580c48afa7`. Nội dung prompt không đổi.
- **Git.** Một thành viên bị kẹt ở màn hình vim khi `git pull` (merge message) và có xung đột ở `TEAM.md` khi nhiều người cùng điền bảng thành viên; xử lý bằng hoàn tất merge và giữ đủ 4 dòng thành viên. Hệ quả là một phần bài được push sau 23h59, trong thời gian gia hạn của coach.
- **Kết nối provider khi chạy v4.** Lần chạy base đầu có 6 ca `APIConnectionError`, group đầu có 4 ca; giữ nguyên log và không dùng điểm của hai run thiếu dữ liệu làm kết quả tối ưu. Chạy lại lần lượt từng suite với cùng prompt/tool: base 20/20 và group 10/10, không còn lỗi provider/tool. Đường dẫn các log và giải thích nằm trong [v4_summary.md](../../starter_v0/analysis/v4_summary.md).

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix nào thuộc `system_prompt.md`?** Hành vi và quy trình: phạm vi agent (R08, R14), hỏi lại khi thiếu thông tin (R10, R11), thứ tự xác nhận trước khi gửi (R12), theo dõi ngữ cảnh nhiều lượt và đổi nguồn (M06), cho phép gọi song song (R13).
- **Fix nào thuộc `tools.yaml`?** Lựa chọn giữa các tool và giá trị tham số: phân biệt `timeline`/`social_search`/`lookup`/`fetch`, convention `topic=news` + `timeframe` thay vì nhét vào `query` (R03, R13), `confirmed=true` của `send`, và ranh giới `summarize` vs `fetch` khi chỉ có URL.
- **Failure nào cần review thủ công?** (1) Câu ngoài phạm vi: eval chỉ kiểm "không gọi tool", không kiểm agent từ chối có lịch sự/đúng không. (2) G06: agent tìm lại tin trước khi hỏi xác nhận — đọc thêm thì vô hại, nhưng có thể lệch quy trình; cần người xem để quyết định đó là lỗi hay hành vi chấp nhận được. (3) Transcript B2: agent hỏi lại bằng text thay vì `clarify` — đúng ý nhưng sai cơ chế, chấm tự động trên chat thật không bắt được. (4) Chất lượng nội dung tóm tắt/bản tin không được chấm.
- **Lưu ý về phương pháp:** v1–v3 mỗi version sửa nhiều điểm cùng lúc (v3 sửa cả prompt lẫn tools), nên khó tách thay đổi nào tạo ra mức tăng. Ví dụ v1 giả thuyết về "hỏi lại" nhưng R10/R11 vẫn FAIL đến v2 (do thiếu `response_type`), còn phần tăng điểm của v1 thực tế đến từ phạm vi và routing (R03, R08, R13, R14).
- **Vòng bổ sung đã thực hiện:** v4 kiểm chứng một giả thuyết cho G06 bằng đúng một câu thêm vào bước 1; base đạt 20/20 và group 10/10. Chưa thực hiện v5. Lỗi hỏi bằng chữ thay vì `clarify` trong transcript B2 vẫn là giới hạn cần kiểm tra riêng bằng chat nhiều lượt; việc các ca eval hỏi lại đều đạt không chứng minh lỗi live chat này đã được sửa. Bước sau có thể kiểm chứng giả thuyết đó, rồi thêm eval case cho `keywords`, `extract_links`, `merge_sources`.

## 8. Tài liệu tham khảo

- Đề bài: `README.md`, `RULES.md`, `CHECKPOINTS.md`, `RUBRIC.md`, `SUBMISSION.md`, `docs/TOOL-SETUP.md`, `starter_v0/tools/README.md`
- Tavily API: https://docs.tavily.com · Firecrawl: https://docs.firecrawl.dev · RapidAPI Twitter API45: https://rapidapi.com/alexanderxbx/api/twitter-api45
- Streamlit: https://docs.streamlit.io · OpenRouter: https://openrouter.ai/docs
- Công cụ AI hỗ trợ (giải thích đề, soạn nháp, phân tích log) được ghi trong báo cáo cá nhân của từng thành viên.
