# Báo cáo cá nhân — HoVaTen-MSSV

Đổi tên file theo quy tắc `MSSV_HoTen.md`.

Ví dụ: `20241234_NguyenVanAn.md`.

## 1. Thông tin thành viên

- Họ tên: Nguyễn Đức Minh   
- MSSV: 2A202603765
- Email: 26ai.minhnd5@vinuni.edu.vn

## 2. Phần việc phụ trách
CP1+CP2
...

## 3. Đóng góp cụ thể
Chạy v0 và tìm ra nhưng case bị lỗi sau đó thiết kế prompt:
V1: Sửa prompt để agent hỏi lại khi thiếu tài khoản hoặc URL, không tự đoán thông tin và yêu cầu xác nhận trước khi gửi tin. Kết quả tăng từ 65% lên 85%.
V2: Bổ sung quy định truyền đầy đủ tham số khi hỏi lại, giới hạn phạm vi nghiên cứu và phân biệt trả lời trong chat với gửi tin ra ngoài. Kết quả đạt 90%.
V3: Hoàn thiện quy trình xác nhận, giúp agent nhớ đúng nguồn tìm kiếm khi người dùng đổi ý, đồng thời làm rõ mô tả và tham số của các tool. Kết quả đạt 100% trên 20 ca kiểm thử base.
...

## 4. Bằng chứng

- File/commit/PR:

  File analysis: [v0](../../starter_v0/analysis/base_runs.csv), [v1](../../starter_v0/analysis/base_runs_v1.csv), [v2](../../starter_v0/analysis/base_runs_v2.csv) và [v3](../../starter_v0/analysis/base_runs_v3.csv).

  Các thay đổi nằm trong [system_prompt.md](../../starter_v0/artifacts/system_prompt.md) và [tools.yaml](../../starter_v0/artifacts/tools.yaml). File theo dõi các phiên bản là [version_log.csv](../../starter_v0/artifacts/version_log.csv).

  Kết quả chạy chi tiết được lưu trong các file JSON: [v0 đạt 65%](../../starter_v0/runs/v0_B_base_openrouter_20261110T175810757222.json), [v1 đạt 85%](../../starter_v0/runs/v1_B_base_openrouter_20261110T182116426151.json), [v2 đạt 90%](../../starter_v0/runs/v2_B_base_openrouter_20261110T182901299092.json) và [v3 đạt 100%](../../starter_v0/runs/v3_B_base_openrouter_20261110T184535773441.json).

- AI/công cụ đã dùng và cách tự kiểm tra kết quả: ChatGPT, Gemini/ Tôi nhờ AI đọc hộ tôi base_run của từng file sau đó phân tích xem điều gì đang mắc phải. Sau đó chọn ra từng nhóm và chia nhỏ ra để xử lý. Dựa vào gợi ý prompt sau đó sửa lại một số ý rồi viết vào phi prompt để kiểm tra kết qua của từng version sau.

## 5. Tự đánh giá
Đây là một phần quan trọng của bài lab cách tạo prompt và cách kiểm soát cho AI của mình sẽ áp dụng được rất nhiều vào phần build và quá trình sau này.

...
