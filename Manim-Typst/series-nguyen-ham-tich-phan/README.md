# SANG MATH – NGUYÊN HÀM / TÍCH PHÂN / ỨNG DỤNG CHUYÊN SÂU

**INT01 – Đi ngược đạo hàm: Bản chất của nguyên hàm**

Phần đầu tiên trong dự kiến 36 tập. Gói này là repository bắt đầu mới; không trộn với repository `sangmath-thong-ke` gồm 18 tập Thống kê.

## Khả năng

- 8 chương, 32 phân đoạn giảng dạy (trên video không có bộ đếm, số nhịp hoặc nhãn debug).
- Đồ thị có tọa độ thực; 3 parabol x² + C, các tiếp tuyến song song tại cùng x, khoảng cách 3 giữa hai nguyên hàm, điểm (1;3), bài ứng dụng vận tốc–tọa độ, bài luyện x³+4.
- 22 công thức toán được biên dịch từ Typst thành SVG; cảnh dựng bằng **Manim Community**.
- Voice nam tiếng Việt (`vi-VN-NamMinhNeural`) và phụ đề `.srt`, có kiểm tra MP4/âm thanh.
- Footer chính xác: **Thầy Nguyễn Văn Sang**.
- Full HD 1920x1080/30fps; preview 854x480/24fps.

## GitHub Actions

Push toàn bộ *nội dung bên trong* ZIP vào gốc repo mới; phải bao gồm `.github/workflows/render-int01.yml`. Vào **Actions → Render INT01 - Ban chat nguyen ham → Run workflow**.

1. `quality=preview`, `voice=off`: kiểm tra bố cục, màu và công thức.
2. `quality=preview`, `voice=on`: kiểm tra giọng nam và phụ đề.
3. Nếu đạt, `quality=fullhd`, `voice=on` để xuất bản.

Tải **Artifacts** của workflow gồm MP4, phụ đề, 8 ảnh chụp từ MP4 và báo cáo QA.

**Voice-on phải thất bại khi không tạo được MP3:** không xuất bản video câm giả có giọng. Đánh giá đủ chất lượng còn cần xem/nghe video thật.

## Chạy từ Linux cài Manim/Typst

```bash
python -m pip install -r requirements.txt
python scripts/prepare_int01.py --voice off
python -m unittest discover -s tests -v
python scripts/build_int01_typst.py
manim -ql -r 426,240 --fps 8 int01/scene.py INT01_SMOKE
manim -ql -r 854,480 --fps 24 int01/scene.py INT01
```

Dùng `python scripts/prepare_int01.py --voice on` để tạo audio TTS cần mạng, rồi render lại scene `INT01`.

## Cảnh báo môi trường phát triển

Ở môi trường soạn gói ban đầu, **không có Manim hoặc Typst và không thể cài từ mạng**. Do đó đã chạy kiểm thử dữ liệu và sinh storyboard bằng Pillow, **chưa có SVG Typst hoặc MP4 render thật**. Cảnh `INT01_SMOKE` trên GitHub mới là render kỹ thuật đầu tiên; sau đó phải duyệt MP4 thực tế.

Các ảnh `preview/int01` là **bản dựng phác thảo để duyệt** (không phải ảnh trích từ MP4 thật).
