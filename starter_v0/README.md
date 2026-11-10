# Source code

Toàn bộ source code của lab nằm trong folder này. Chạy mọi lệnh từ `starter_v0/`.

- File bắt đầu chạy: `run_eval.py` (chạy eval), `chat.py` (chat live), `scripts/preflight_provider.py` (kiểm tra provider).
- Cách chạy: `python run_eval.py --provider openrouter --version v0 --suite base --eval-cases data/eval_base.json`; `python chat.py --provider openrouter --version v3`; `pytest`.
- Input: `artifacts/system_prompt.md`, `artifacts/tools.yaml`, bộ case `data/*.json`, API key trong `.env` (mẫu ở `.env.example`).
- Output: `runs/*.json` (kết quả eval), `transcripts/*.transcript.json` (chat live), `analysis/*.csv` (nếu chạy `scripts/parse_runs.py`).
- File học viên được sửa: `artifacts/system_prompt.md`, `artifacts/tools.yaml`, `artifacts/version_log.csv`, `data/eval_group.json`, `tools/` (thêm tool mới và đăng ký trong `tools/__init__.py`), `tests/test_tools_todo.py`, code UI và `requirements.txt`. Không sửa nội dung case trong `data/eval_base.json`.

Chi tiết từng bước xem [README.md](../README.md) ở root; cấu hình API key xem [docs/TOOL-SETUP.md](../docs/TOOL-SETUP.md).

## Giao diện Streamlit

Chạy từ `starter_v0/`, sau khi kích hoạt môi trường Python:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Mở địa chỉ in trong terminal (mặc định `http://localhost:8501`).
Giao diện mặc định dùng **Agent thật**, provider OpenRouter. Điền API key trong
`.env` như hướng dẫn setup; các tool cần key riêng theo `docs/TOOL-SETUP.md`.
Sidebar cho chọn provider, model (để trống dùng mặc định), nhãn phiên bản
prompt/tool, số lượt giữ trong ngữ cảnh và giới hạn vòng tool.

Phiên đầu tiên sẽ đọc prompt và khai báo tool hiện tại, dùng chung
`chat.run_model_tool_loop()` với CLI. Cấu hình và nội dung prompt/tool được giữ
trong suốt phiên; tạo “Cuộc trò chuyện mới” để đổi cấu hình hoặc lấy prompt/tool
mới sau khi nhóm cập nhật. UI tự sử dụng tool được khai báo và đăng ký theo
contract của starter, không cần thêm nút riêng cho từng tool.

Agent hỏi bổ sung hoặc xin xác nhận thì trả lời tiếp trong ô chat. Kết quả tool
và lịch sử hỏi lại được giữ trong ngữ cảnh của các lượt sau. Mở “Hoạt động tool”
để xem arguments/kết quả thật, hoặc “Chi tiết các vòng xử lý” để đọc đầy đủ log.
Lỗi provider và lỗi tool được hiển thị; UI không tự chạy lại một lượt đã lỗi.

Transcript tự lưu sau mỗi lượt trong `transcripts/live_<mã>.transcript.json`.
Nút “Tải transcript JSON” tải bản hiện tại về máy. JSON có provider/model,
nhãn phiên bản, hash prompt/tool, thời gian GMT+7, các lượt hỏi/đáp, trạng thái,
vòng xử lý và tool events. Nếu provider lỗi sau khi tool đã chạy, các kết quả
tool đã có vẫn được lưu. Lỗi khởi tạo được ghi `configuration_error` cùng cấu
hình yêu cầu; lỗi gọi model được ghi `provider_error`.

Mỗi phiên có file riêng; tạo phiên mới giữ các file cũ. Tải lại trang có thể
bắt đầu phiên mới; UI hiện chưa mở lại transcript cũ. Nếu ghi file lỗi,
sidebar báo lỗi và có “Thử lưu lại”; bạn vẫn có thể tải JSON.

Chọn **Demo giao diện** trước khi gửi câu hỏi để thử UI không gọi API.
Transcript demo ghi `mode: "demo"`, trạng thái `demo_answered`, provider/model
để `null` và các trường tool rỗng. Transcript demo không phải bằng chứng chạy
Agent thật. Hội thoại demo đã mở ở bản UI trước vẫn được giữ khi hot reload.
