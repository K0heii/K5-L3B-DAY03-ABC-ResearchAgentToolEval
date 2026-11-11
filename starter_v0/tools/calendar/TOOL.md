---
name: calendar
track: bonus
kind: control
requires_env: []
inputs: []
outputs: [timezone, now, dates, note]
side_effect: false
---
# calendar

Đọc đồng hồ hệ thống theo giờ Việt Nam (UTC+7), trả ngày ISO và DD/MM/YYYY
cho hôm nay, hôm qua, hôm kia, ngày mai và ngày kia. Không gọi mạng.
Phụ thuộc đồng hồ máy được đặt đúng; không xác nhận lịch hay kết quả xổ số.
