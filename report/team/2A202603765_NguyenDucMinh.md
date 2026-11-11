# Báo cáo cá nhân — Nguyen Duc Minh-2A202603765

## 1. Thông tin thành viên

- Họ tên: Nguyễn Đức Minh   
- MSSV: 2A202603765
- Email: 26ai.minhnd5@vinuni.edu.vn

## 2. Phần việc phụ trách

- CP1–CP2: chạy baseline, phân tích lỗi và cải tiến system prompt, mô tả tool qua các phiên bản v1–v5.
- Chạy eval để so sánh trước và sau khi sửa; xuất bảng CSV và cập nhật version log bằng kết quả thực tế.
- Chạy lại bộ group do nhóm xây dựng để kiểm tra hồi quy, đối chiếu từng ca và bổ sung kết quả v5 vào bảng B3 của báo cáo nhóm.
- Bổ sung xử lý ngày tháng theo giờ Việt Nam, sửa lỗi lấy nhầm ngày khi hỏi kết quả xổ số và hạn chế trả lời khi chưa có nguồn xác minh.
- Hỗ trợ kiểm tra kết nối API, sửa lỗi Unicode trên Windows và kiểm tra lại giao diện sau khi cập nhật.

## 3. Đóng góp cụ thể
Chạy baseline v0, đọc các ca lỗi trong run JSON rồi chia thành từng nhóm để sửa prompt và mô tả tool.

V1: Sửa prompt để agent hỏi lại khi thiếu tài khoản hoặc URL, không tự đoán thông tin và yêu cầu xác nhận trước khi gửi tin. Kết quả tăng từ 65% lên 85%.

V2: Bổ sung quy định truyền đầy đủ tham số khi hỏi lại, giới hạn phạm vi nghiên cứu và phân biệt trả lời trong chat với gửi tin ra ngoài. Kết quả đạt 90%.

V3: Hoàn thiện quy trình xác nhận, giúp agent nhớ đúng nguồn tìm kiếm khi người dùng đổi ý, đồng thời làm rõ mô tả và tham số của các tool. Kết quả đạt 100% trên 20 ca kiểm thử base.

V4: Chỉ thêm một câu vào bước 1 của quy trình xác nhận để yêu cầu đăng/gửi sau lượt tìm kiếm vẫn phải hỏi xác nhận bằng `clarify(yes_no)` trước. Chạy cả base và group: base đạt 20/20, group đạt 10/10; G06 đã chọn đúng tool xác nhận. Không sửa nội dung case hay code chấm.

V5: Bổ sung tool `calendar` để lấy ngày giờ thật theo giờ Việt Nam và tính đúng hôm nay, hôm qua, hôm kia, ngày mai, ngày kia. Thêm tham số `target_date` cho `lookup` để tìm theo ngày cụ thể; bổ sung kiểm tra trong vòng xử lý để chặn truy vấn xổ số lệch ngày hoặc tìm kết quả của kỳ chưa diễn ra. Sửa prompt để không lấy kết quả ngày cũ thay thế và không tự điền số khi nguồn không xác minh được. Nếu chưa đến giờ mở thưởng, chỉ thông báo điều đó khi đã kiểm tra lịch; nếu chưa đủ bằng chứng thì nói rõ chưa xác minh được kết quả.

Sau khi v5 ban đầu đạt 19/20, phân tích R01 hỏi thừa số lượng tweet và thêm quy tắc dùng giá trị mặc định cho tham số tùy chọn. Lần kiểm tra tiếp theo phát hiện M03 sai handle, nên bổ sung ánh xạ tên sang tài khoản thật trong mô tả `timeline`. Bản sửa đạt [base 20/20](../../starter_v0/runs/v5_B_base_openrouter_20261111T114616307841.json) và [group 10/10](../../starter_v0/runs/v5_B_group_openrouter_20261111T114714485359.json); giữ nguyên các run 19/20 làm bằng chứng trước sửa.

Viết thêm kiểm tra ngày tháng, gồm đổi tháng/năm, năm nhuận, hôm qua trừ một ngày, hôm kia trừ hai ngày và chặn tìm sai ngày. Thử model với nguồn giả lập rỗng để kiểm tra cách trả lời khi không có dữ liệu. Đồng thời sửa lỗi `UnicodeEncodeError` do dòng log có emoji trên Windows, giữ nguyên tiếng Việt trong câu trả lời và transcript. Sau các bổ sung, bộ test có 121 passed, 14 skipped.

## 4. Bằng chứng

- File/commit/PR:

  File analysis: [v0](../../starter_v0/analysis/base_runs.csv), [v1](../../starter_v0/analysis/base_runs_v1.csv), [v2](../../starter_v0/analysis/base_runs_v2.csv) và [v3](../../starter_v0/analysis/base_runs_v3.csv).

  Các thay đổi nằm trong [system_prompt.md](../../starter_v0/artifacts/system_prompt.md) và [tools.yaml](../../starter_v0/artifacts/tools.yaml). File theo dõi các phiên bản là [version_log.csv](../../starter_v0/artifacts/version_log.csv).

  Kết quả chạy chi tiết được lưu trong các file JSON: [v0 đạt 65%](../../starter_v0/runs/v0_B_base_openrouter_20261110T175810757222.json), [v1 đạt 85%](../../starter_v0/runs/v1_B_base_openrouter_20261110T182116426151.json), [v2 đạt 90%](../../starter_v0/runs/v2_B_base_openrouter_20261110T182901299092.json) và [v3 đạt 100%](../../starter_v0/runs/v3_B_base_openrouter_20261110T184535773441.json).

  Bằng chứng v4: [run base 20/20](../../starter_v0/runs/v4_B_base_openrouter_20261111T090622307950.json), [run group 10/10](../../starter_v0/runs/v4_B_group_openrouter_20261111T090726767829.json) và [phân tích thay đổi, lỗi kết nối, giới hạn so sánh](../../starter_v0/analysis/v4_summary.md).

  Bằng chứng v5 trước sửa: [run ban đầu 19/20, lỗi R01](../../starter_v0/runs/v5_B_base_openrouter_20261111T112032802355.json) và [run trung gian 19/20, lỗi M03](../../starter_v0/runs/v5_B_base_openrouter_20261111T114251450323.json).

  Bằng chứng v5 sau sửa: [run base 20/20](../../starter_v0/runs/v5_B_base_openrouter_20261111T114616307841.json), [run group 10/10](../../starter_v0/runs/v5_B_group_openrouter_20261111T114714485359.json), [CSV base](../../starter_v0/analysis/base_runs_v5.csv) và [CSV group](../../starter_v0/analysis/group_runs_v5.csv). Bảng B3 trong [báo cáo nhóm](group_report.md#b3-team-eval-cases) có kết quả từng ca.

## 5. Tự đánh giá
Đây là một phần quan trọng của bài lab cách tạo prompt và cách kiểm soát cho AI của mình sẽ áp dụng được rất nhiều vào phần build và quá trình sau này.
