# HƯỚNG DẪN GITHUB ACTIONS – STAT04

## Cập nhật repository cũ
Nếu đã có STAT01–03, dùng ZIP patch STAT04. Giải nén và chép nội dung vào gốc repository `sangmath-thong-ke`, giữ nguyên cấu trúc `stat01/`, `stat02/`, `stat03/`, `stat04/` và `.github/workflows/`.

Nếu chưa có các tập trước, dùng ZIP trọn bộ STAT01–STAT04. Commit và push lên nhánh chính.

## Chạy render
1. Mở **Actions** → **Render STAT04 - Tu phan vi Q1 Q2 Q3 - Manim Typst** → **Run workflow**.
2. Chọn `quality=preview`, `voice=off` để kiểm tra hình, công thức và mốc thời gian.
3. Tải artifact. Xem 8 ảnh chụp chương và MP4; sửa nếu thấy chữ đè, hiển thị sai dấu, chuyển động quá nhanh/chậm.
4. Chạy lại `voice=on` để có giọng đọc tiếng Việt (cần mạng, edge-tts có thể từ chối hoặc đổi chính sách). Khi lỗi TTS, workflow báo lỗi, **không tự tạo video giả có tiếng**.
5. Sau khi duyệt, chạy `quality=fullhd` xuất 1920×1080, 30 fps.

## Chạy trong máy Linux đã cài Manim / Typst
```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/build_stat04_typst.py
python scripts/prepare_stat04.py --voice off
manim -ql -r 854,480 --fps 24 stat04/scene.py STAT04
VIDEO=$(find media/videos -type f -name STAT04.mp4 | head -n 1)
python scripts/qa_stat04.py --video "$VIDEO" --quality preview --voice off
```

## Kiểm tra kỹ thuật
- `scripts/prepare_stat04.py` tạo `stat04/runtime_plan.json` và `STAT04_vi.srt` khớp 32 nhịp.
- Thời lượng thiết kế **832 giây (13 phút 52 giây)** khi `voice=off`; với TTS có thể kéo dài.
- `scripts/qa_stat04.py` dùng FFprobe kiểm tra độ phân giải, thời lượng, luồng âm thanh nếu bật TTS, sau đó trích 8 ảnh vào `artifacts/stat04_qa/`.
- Kiểm tra kỹ thuật KHÔNG đồng nghĩa video đã đạt chất lượng trình bày và sư phạm.

## Quy ước tứ phân vị
- n chẵn: Q1 và Q3 là trung vị hai nửa có n/2 giá trị.
- n lẻ: loại Q2 trước khi lấy trung vị hai nửa còn lại.
- Trường hợp bộ điểm giả lập: Q1=6, Q2=7, Q3=8. Vị trí tương ứng: 10–11, 20–21, 30–31.
- Khi nhiều quan sát trùng nhau, tránh khẳng định cứng rằng chính xác 25% số quan sát nhỏ hơn Q1.
