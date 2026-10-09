# Hướng dẫn render STAT01 trên GitHub Actions

1. Tải `SangMath_ThongKe_STAT01_GitHubReady.zip` và giải nén.
2. Dùng GitHub Desktop hoặc Git push để đưa *nội dung* thư mục vào repository mới `sangmath-thong-ke`. Phải có file `.github/workflows/render-stat01.yml` nằm đúng gốc.
3. Trên GitHub: **Actions > Render STAT01 - Du lieu biet noi - Manim Typst > Run workflow**.
4. Chạy `preview` và `voice=off`. Kiểm tra tệp MP4, 8 ảnh chương, QA JSON và phụ đề SRT trong Artifacts.
5. Nếu ổn, chạy `voice=on` ở Preview. Edge TTS sẽ dùng Internet GitHub Actions để tổng hợp giọng nữ tiếng Việt `vi-VN-HoaiMyNeural`.
6. Cuối cùng render `quality=fullhd`, `voice=on` để xuất 1920 × 1080, 30 FPS.
7. **Chưa đăng dạy ngay:** kiểm tra chữ không tràn khung, số liệu và biểu đồ, nghe lời giảng có vấp hoặc cắt câu không, đặc biệt là cảnh các thẻ sắp xếp, công thức Typst và dấu tiếng Việt.

Khi một job màu đỏ, mở job `render`, gửi log bước bị lỗi. Không cần sửa cả series hoặc tạo repository khác.

**Lưu ý:** Đây là series thống kê riêng; không cần ghi đè repository tổ hợp 25 tập.
