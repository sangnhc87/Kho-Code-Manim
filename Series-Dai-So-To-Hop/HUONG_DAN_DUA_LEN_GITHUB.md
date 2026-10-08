# CÀI COMB01 V2 LÊN GITHUB (KHÔNG CẦN CODEX CLOUD)

**Đây là bản Video 01 đã viết lại để xử lý lỗi video quá ngắn.** Không dùng workflow COMB01 cũ khi render.

1. Giải nén file `SangMath_COMB01_V2_GitHubReady.zip`.
2. Chép **toàn bộ nội dung đã giải nén**, kể cả thư mục ẩn `.github`, vào gốc repository GitHub đang lưu COMB01, COMB02, GEO01. Giữ nguyên vị trí thư mục `episodes`, `scripts`, `tests`.
3. Khi hệ thống hỏi, chọn **ghi đè** các file COMB01 trùng tên. Các mã COMB02 và GEO01 vẫn được giữ.
4. Commit và push thay đổi.
5. Vào **Actions → Render COMB01 V2 - Bai giang day du Manim Typst → Run workflow**.
6. Chạy trước với `quality=preview`, `voice=on`. Nếu dịch vụ tạo giọng đọc lỗi mạng, chọn `voice=off` để duyệt riêng hình.
7. Ở cuối tác vụ, vào Artifacts, tải `COMB01-V2-preview-voice-on`. Trong đó có MP4, 8 ảnh chụp từng chương, ảnh tổng hợp và báo cáo kiểm tra thời lượng.
8. Sau khi xem preview thực tế, chạy lại workflow chọn `quality=fullhd` để xuất 1920×1080, 30 FPS.

**Định lượng bắt buộc:** bài có 42 nhịp, 8 phần, video tối thiểu 11 phút. File đã bật tiếng phải có audio stream. Workflow dùng `ffprobe` kiểm tra hai điều kiện này.

**Lưu ý kỹ thuật:** bộ code đã được kiểm tra toán, cú pháp Python, cấu trúc YAML. Môi trường đóng gói thiếu Manim/Typst nên chưa thể xác nhận render thực tế. Khi GH báo lỗi Manim/Typst/TTS, gửi log để sửa đúng lỗi. Không khẳng định video hoàn thiện khi chưa xem MP4.
