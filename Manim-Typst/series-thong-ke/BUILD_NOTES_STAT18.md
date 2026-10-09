# STAT18 – kiểm tra và giới hạn xác nhận

- Mã/kiểm thử Python: kiểm tra cú pháp và unittest, dự phòng mock 32 hình và 32 khung giải thích.
- Typst: 8 nguồn công thức, script buộc phải biên dịch ra SVG thật và thất bại nếu thiếu CLI.
- Manim: dùng `STAT18_SMOKE` để render thử thật 32 hình, sau đó render `STAT18`.
- Phụ đề SRT: tạo từ cùng nguồn lời giảng với kế hoạch thời lượng; chế độ voice=on dùng tệp audio do Edge TTS sinh.
- Nếu thiếu dịch vụ TTS, chế độ voice=on phải báo lỗi; không xuất bản file câm được gắn nhãn có tiếng.
- Mô phỏng cố định seed, thống kê rút không hoàn lại; công thức sd có hệ số hiệu chỉnh hữu hạn.
- Công thức khoảng dạng chuẩn là minh họa gần đúng, không phải bảo đảm xác suất cho tham số đã cố định.
- Các ảnh preview do Pillow sinh chỉ nhằm duyệt storyboard, không phải khung hình thực tế.
- Chỉ báo **đã nghiệm thu** sau khi kiểm tra MP4 Full HD, phụ đề, tiếng nam, màu sắc, tỷ lệ và không tràn chữ.
