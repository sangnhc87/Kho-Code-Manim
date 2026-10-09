# Kiểm tra kỹ thuật STAT07

Đã kiểm tra bằng Python trên nguồn STAT01–07: 347 test (bao gồm test STAT07), 32 trạng thái Scene và phần lời giải kiểm tra qua API mock Manim, biên dịch cú pháp Python, có runtime plan 32 nhịp (928 giây) và 162 đoạn phụ đề. Đây là **kiểm thử trước render**, không phải bằng chứng video thực xuất đạt yêu cầu.

GitHub Actions chạy những bước bắt buộc tiếp theo: (1) cài Typst và Manim; (2) tạo 8 SVG từ Typst; (3) thực sự dựng 32 trạng thái bằng Scene `STAT07_SMOKE`; (4) render cả bài; (5) ffprobe kiểm tra thời lượng, 854×480 hoặc 1920×1080, âm thanh khi bật TTS; (6) trích 8 ảnh theo chương.

Nếu workflow báo lỗi, gửi log có tên bước lỗi và ảnh Artifacts để sửa đúng điểm, không đánh đồng test Python với render thật.

**Số liệu chuẩn**: 40 điểm giả lập; bốn lớp nửa kín [4;6), [6;8), [8;10), [10;12), tần số (6,18,14,2), tích lũy (6,24,38,40), tỷ lệ 15%–45%–35%–5%; các lớp không đều [4;6), [6;7), [7;9), [9;11) có mật độ (3,8,9,4), tổng diện tích 40. Ước lượng trung bình ghép nhóm = 7,6, trung bình dữ liệu gốc = 7,1.
