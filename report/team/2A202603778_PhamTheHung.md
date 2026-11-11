# Báo cáo cá nhân — Pham The Hung — 2A202603778

## 1. Thông tin thành viên

- Họ tên: Pham The Hung
- MSSV: 2A202603778
- Email: 26ai.hungpt5@vinuni.edu.vn

## 2. Phần việc phụ trách

CP5 — Xây dựng giao diện Streamlit, tích hợp Research Agent và lưu transcript hội thoại.

## 3. Đóng góp cụ thể

Xây dựng giao diện chat bằng Streamlit, gồm ô nhập câu hỏi, hiển thị lịch sử hội thoại, sidebar cấu hình provider/model và nút tạo cuộc trò chuyện mới.

Tích hợp giao diện với vòng lặp Agent có sẵn trong `chat.py`, nạp prompt và danh sách tool của nhóm. Hiển thị tiến trình, arguments, kết quả gọi tool và các lỗi để người dùng kiểm tra.

Bổ sung chức năng tự động lưu transcript JSON sau mỗi lượt chat và tải transcript từ giao diện. Mỗi phiên có file riêng, ghi provider/model, phiên bản và hash prompt/tool, thời gian, câu hỏi, câu trả lời cùng kết quả tool.

Kiểm tra tích hợp tool mới `summarize` qua giao diện: nhận đoạn văn 5 câu và tóm tắt còn 2 câu. Thử hội thoại 5 lượt gồm tóm tắt, yêu cầu thiếu thông tin rồi bổ sung tài liệu, yêu cầu gửi lên Telegram và từ chối gửi sau khi Agent hỏi xác nhận.

## 4. Bằng chứng

- File/commit/PR:

  Code giao diện và tích hợp: [app.py](../../starter_v0/app.py), [ui_agent.py](../../starter_v0/ui_agent.py), [ui_transcripts.py](../../starter_v0/ui_transcripts.py) và phần bổ sung callback trong [chat.py](../../starter_v0/chat.py).

  Cấu hình, dependency và hướng dẫn chạy: [config.toml](../../starter_v0/.streamlit/config.toml), [requirements.txt](../../starter_v0/requirements.txt) và [README.md](../../starter_v0/README.md).

  Bằng chứng chính: [transcript hội thoại 5 lượt](../../starter_v0/transcripts/live_8b2a2d7549464c58988584b9c4cb419b.transcript.json). Lượt 2 Agent hỏi bổ sung bằng văn bản, chưa gọi `clarify`; lượt 4 gọi `clarify` với `response_type="yes_no"` và chờ xác nhận; lượt 5 người dùng từ chối nên không gọi `send`.

  Kiểm tra riêng tool mới: [transcript summarize](../../starter_v0/transcripts/live_bb95accc24b545d288ec6624823bfa65.transcript.json), ghi nhận `max_sentences=2`, `sentence_count=5` và `sentences_used=2`.

  Lệnh chạy từ `starter_v0/`: `python -m streamlit run app.py`. Địa chỉ local: <http://127.0.0.1:8501/>. Commit kỹ thuật của phần UI được ghi trong lịch sử Git cùng các file trên.

- AI/công cụ đã dùng và cách tự kiểm tra kết quả:

  Sử dụng Codex hỗ trợ đọc đề, xây dựng code và kiểm tra ứng dụng. Việc kiểm chứng được thực hiện bằng pytest, Streamlit AppTest, chạy hội thoại thật qua OpenRouter, xem hoạt động tool và đối chiếu file JSON đã lưu. Sau khi bỏ hai file test UI bổ sung và đồng bộ code mới của nhóm, kết quả suite còn lại là 70 passed, 14 skipped, 0 failed; các test skip là TODO có sẵn của starter.

### Triển khai giao diện dùng thử

Tôi chạy Streamlit trên máy Windows và dùng Cloudflare Quick Tunnel để chia sẻ giao diện với nhóm và người chấm. Sau khi Streamlit chạy ở cổng `8501`, tôi mở PowerShell thứ hai và chạy:

```powershell
& "C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://localhost:8501
```

Endpoint `/_stcore/health` qua URL công khai trả về HTTP 200 (`ok`). Link dùng thử đã được điền vào A1 và B5a trong [báo cáo nhóm](group_report.md). Link hoạt động khi cả Streamlit và `cloudflared` đang chạy. [Mở Research Desk](https://impact-prohibited-emerald-overcome.trycloudflare.com)

## 5. Tự đánh giá

Phần việc đã có giao diện chạy local, kết nối Agent thật, hiển thị hoạt động tool và lưu/tải transcript làm bằng chứng. Phiên 5 lượt thể hiện được các tình huống yêu cầu thường, bổ sung thông tin và hỏi xác nhận trước khi gửi.

Cần phối hợp với thành viên phụ trách prompt để xem lại trường hợp hỏi thiếu thông tin nhưng chưa gọi `clarify`. Khi trình bày, cần nắm được luồng giao diện → Agent → tool và cách kiểm tra kết quả từ transcript.
