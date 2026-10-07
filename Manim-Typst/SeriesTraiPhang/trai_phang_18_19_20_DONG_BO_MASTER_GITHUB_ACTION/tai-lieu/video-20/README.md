# TRẢI PHẲNG 20 MASTER — CAPSTONE THUẬT TOÁN

## Upload GitHub

Đặt `.py` tại `Manim-Typst/` và `.yml` tại `.github/workflows/`.

Vào GitHub → Actions → **Render Trai Phang 20 MASTER** → **Run workflow**.

Workflow sẽ cài `manim==0.21.0`, `typst>=0.14`, `edge-tts==7.2.8` và ffmpeg. Các bước gồm kiểm tra Python, lời thoại, Typst, hình học, layout, smoke render 480p, render full 1080p rồi ghép giọng đọc. Video cuối nằm trong **Artifacts**.

## Nội dung chính

Hộp 8×5×4; P trên mặt trước, Q trên mặt sau. Không cấm mặt: đường qua nắp dài `sqrt(65)`. Cấm nắp: đường hợp lệ qua đáy dài `sqrt(137)`. Thuật toán liệt kê các dải mặt liền nhau, mở thật quanh bản lề, kiểm tra giao cạnh nội phần và chọn nhỏ nhất.

## Ghi chú

- Manim gọi `MathTypst` để hiển thị công thức; **không bắt buộc có tệp `.typ` riêng**.
- Tệp `.py` tự gọi `edge-tts` và `ffmpeg` trong giai đoạn render.
- Cần mạng cho Edge TTS và cần GitHub Actions được bật.
- Kiểm tra tĩnh và số học đã chạy; **chưa xác nhận full MP4 được render trong phiên tạo gói này**.
