# V4 — Xác nhận trước khi đăng/gửi sau lượt tìm kiếm

## Giả thuyết và thay đổi

Mọi yêu cầu đăng/gửi chưa được xác nhận phải bắt đầu bằng `clarify(response_type="yes_no")`, kể cả khi lượt trước là tìm kiếm.

Chỉ thêm đúng một câu vào bước 1 của quy trình xác nhận trong `artifacts/system_prompt.md`:

> This confirmation-first rule also applies when the previous turn requested a search: a new unconfirmed request to send or publish must start with clarify(response_type="yes_no") before any searching, reading, or summarizing.

Không sửa tool declaration, code chấm, code agent/provider hay nội dung các bộ eval. Không chạy lại v3; dùng các run đã có theo yêu cầu.

## Kết quả hợp lệ

- Base: **20/20 (100%)**, so với v3 có sẵn **20/20 (100%)**. [Run v4 base](../runs/v4_B_base_openrouter_20261111T090622307950.json), [CSV](base_runs_v4.csv), [mốc v3 base](../runs/v3_B_base_openrouter_20261110T194243596270.json).
- Group: **10/10 (100%)**, so với v3 có sẵn **9/10 (90%)**. [Run v4 group](../runs/v4_B_group_openrouter_20261111T090726767829.json), [CSV](group_runs_v4.csv), [mốc v3 group](../runs/v3_B_group_openrouter_20261110T182345441573.json).
- Hai run v4 đều có `provider_error_cases=0`, `measured_cases=total_cases`; không có lỗi trong `tool_results`.
- G06: v3 gọi `lookup`; v4 gọi `clarify` với `response_type="yes_no"` và câu hỏi: “Bạn có xác nhận muốn đăng tin tức về AI hôm nay lên kênh Telegram của nhóm không?”.
- Các ca hỏi thông tin còn thiếu R10, R11 và G05 đều đạt. Chưa thực hiện v5 vì lần đo này chưa ghi nhận lỗi hỏi bằng văn bản thay vì gọi `clarify` ở các ca đó.

## Giới hạn khi so sánh

Hash prompt của v4: `158993352e21ed3850074599f92594292785cbd9911bfc87ab3e309f21eb6aa4`.

Hash tool của v4: `7f5d797950cffda70586ea116da559f4b4d760cc1c0d7344de440dd8e80d4c98`.

Câu hỏi và đáp án của các bộ base/group hiện tại khớp các mốc v3 trên. Tuy nhiên hash tool của v3 base khác cấu hình hiện tại; cả hash prompt và tool của v3 group cũng khác cấu hình ngay trước sửa v4. Vì không đo lại v3 trên cấu hình hiện tại, mức tăng group 90% → 100% chỉ là so sánh với bằng chứng lịch sử, chưa chứng minh riêng câu thêm vào gây ra toàn bộ cải thiện. Trong lượt làm v4 này, thay đổi hành vi duy nhất là một câu trong prompt; tools giữ nguyên.

## Lỗi kỹ thuật ở lần chạy đầu

Hai lần chạy đầu có `APIConnectionError: Connection error.` từ provider:

- [Base lần đầu](../runs/v4_B_base_openrouter_20261111T090052857493.json): 6 ca lỗi provider, chỉ đo được 14/20.
- [Group lần đầu](../runs/v4_B_group_openrouter_20261111T085701371006.json): 4 ca lỗi provider, chỉ đo được 6/10.

Giữ hai log này làm bằng chứng kỹ thuật, không dùng điểm của chúng để kết luận chất lượng hay điền metric sau tối ưu. Đã chạy lại lần lượt từng suite với cùng hash prompt/tool, thu được hai run đầy đủ ở trên. Version log chỉ ghi hai run hợp lệ của v4.
