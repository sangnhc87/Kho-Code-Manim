# HƯỚNG DẪN RENDER COMB03 V2 – SƠ ĐỒ CÂY VÀ KHÔNG GIAN MẪU

## 1. Đưa dự án lên GitHub

Gói ZIP đã chứa cả COMB01 V2, COMB02 V2, GEO01 và COMB03 V2. Giải nén, chép **toàn bộ nội dung bên trong thư mục** vào gốc repository GitHub cũ, kể cả thư mục ẩn `.github`, rồi commit và push. Không tải nguyên ZIP vào một vị trí trong repo và kỳ vọng Actions tự giải nén.

## 2. Chạy COMB03 trên GitHub Actions

1. Mở **Actions → Render COMB03 V2 - Bai giang day du Manim Typst**.
2. Chọn **Run workflow**.
3. `quality=preview` tạo 854×480 / 24 fps; `quality=fullhd` tạo 1920×1080 / 30 fps.
4. `voice=on` tạo các tệp giọng đọc tiếng Việt tự động qua dịch vụ TTS trực tuyến; `voice=off` dựng bản không thuyết minh để kiểm tra kỹ thuật (không cần dịch vụ TTS).
5. Đợi job kết thúc, mở mục **Artifacts** để tải MP4, phụ đề `.srt`, báo cáo kiểm tra và ảnh của 8 chương.

**Lưu ý:** Giai đoạn TTS với `voice=on` cần GitHub runner kết nối được dịch vụ Edge TTS. Khi TTS gặp lỗi mạng, có thể chạy `voice=off` để kiểm tra hình trước; không được coi bản này là bài học hoàn chỉnh có thuyết minh.

## 3. Những file quan trọng

- `episodes/comb03_tree_sample_space.py`: Scene Manim tên `COMB03`.
- `comb03_lesson_data.py` và `comb03_beats.json`: 48 nhịp giảng, nội dung toán và lời giảng tiếng Việt.
- `scripts/prepare_comb03_v2.py`: biên dịch công thức Typst, tạo TTS/SRT và nhịp thời gian.
- `scripts/qa_comb03_v2.py`: kiểm tra MP4, âm thanh, độ phân giải, thời lượng và trích tám ảnh.
- `.github/workflows/render-comb03-v2.yml`: workflow GitHub Actions cho COMB03.
- `preview/comb03_v2/storyboard_8_chapters.png`: bản phác thảo 8 chương, **không phải** ảnh render Manim.

## 4. Lệnh chạy khi có Manim, Typst và FFmpeg

```bash
python -m unittest discover -s tests -v
python scripts/prepare_comb03_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb03_tree_sample_space.py COMB03
VIDEO=$(find media/videos -type f -name 'COMB03.mp4' | head -n 1)
python scripts/qa_comb03_v2.py --video "$VIDEO" --voice off
```

## 5. Tiêu chí duyệt video

- Đủ 8 chương, 48 nhịp; thời lượng tối thiểu 13 phút.
- Hình bên trái không đè lên lời giải bên phải.
- Đủ 8 lá NNN, NNS, NSN, NSS, SNN, SNS, SSN, SSS.
- Biến cố có đúng hai lần ngửa gồm NNS, NSN, SNN, tổng 3.
- Cấm hai lần ngửa liên tiếp: loại NNN, NNS, SNN và giữ đúng 5 dãy.
- Bốn lần tung không có NN: 8 dãy; giải bằng 5 + 3.
- Không suy xác suất 3/8 hoặc 5/8 nếu chưa giả thiết các kết quả đồng khả năng.
- Giọng đọc và phụ đề không được cắt câu, đọc sai ký hiệu hoặc trễ so với hình.

## 6. Trạng thái nghiệm thu

Mã Python và dữ liệu toán đã được kiểm thử tĩnh. **Chưa render Manim thực tế trong môi trường tạo gói** vì thiếu Manim/Typst. Sau lần render đầu, cần gửi MP4 và ảnh QA để rà bố cục, nhịp giảng và âm thanh trước khi xem là bản đã nghiệm thu.