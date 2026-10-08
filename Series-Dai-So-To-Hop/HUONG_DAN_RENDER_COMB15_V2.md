# HƯỚNG DẪN RENDER COMB15 V2 — SANG MATH

## Cập nhật repository

1. Tải gói `SangMath_COMB15_V2_GitHubReady.zip`, giải nén.
2. Chép **nội dung bên trong thư mục giải nén** vào gốc repository GitHub hiện tại.
3. Giữ nguyên thư mục ẩn `.github/workflows`. Commit và push toàn bộ các tệp.
4. Không đưa file ZIP nguyên vẹn lên repository để mong GitHub tự giải nén.

## Render

- Vào **Actions → Render COMB15 V2 - Lap so tu nhien theo dieu kien → Run workflow**.
- Lần đầu chọn `quality=preview`, `voice=off`; khi chạy xong lấy MP4 + 8 ảnh QA trong Artifacts.
- Sau khi duyệt, chọn `voice=on` (cần Edge TTS truy cập mạng) để có giọng đọc tiếng Việt và SRT.
- Khi đã ổn, chọn `quality=fullhd` để xuất MP4 1920×1080, 30 FPS.
- Nếu pipeline báo lỗi, gửi tôi log từ bước đầu tiên thất bại và các ảnh QA để sửa.

## Render thủ công

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/prepare_comb15_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb15_number_formation.py COMB15
```

Cần `typst`, `ffmpeg`, Manim Community v0.19 và font Noto Sans/Serif trong PATH.
Nếu dùng TTS: `python scripts/prepare_comb15_v2.py --voice on`.

## Trạng thái kiểm thử trước khi chạy Actions

- Dữ liệu, kiểm thử toán học và nội dung mã Python: kiểm tra tự động.
- Typst PNG và MP4 Manim thực tế: **chưa render trong môi trường tạo gói**.
- Lịch không tiếng: tối thiểu 1157,2 giây, khoảng 19:17; có tiếng dựa trên thời lượng từng MP3.
- Nếu xuất video ngắn bất thường hoặc không có âm thanh khi `voice=on`, QA phải thất bại.
