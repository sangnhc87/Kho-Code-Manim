# SANGMATH – Series Thống kê trực quan – STAT01/02/03

Bộ mã nguồn tạo video cho giáo viên THPT với **Manim + Typst**, tách dữ liệu–sư phạm, cảnh hình động, kiểm thử và GitHub Actions.

## Video mới – STAT03: Số trung bình, trung vị và mốt

- 8 chương × 4 nhịp = **32 nhịp**; 800 giây nền (13 phút 20 giây).
- 40 điểm giả lập kế thừa STAT01: tổng 284; số trung bình 7,1; trung vị 7; mốt 7.
- Cảnh trực quan: sắp xếp 40 thẻ, hai vị trí 20–21, các cột tần số, điểm cân bằng, kéo một quan sát ngoại lệ và biến đổi thống kê trực tiếp, phép tịnh tiến phân bố, bài toán tìm số còn thiếu.
- Bộ dữ liệu ngoại lệ **riêng về phút luyện tập**, ban đầu [5,6,6,7,7,7,8,8,9], sau thay 9 thành 27. Không được hiểu 27 là điểm kiểm tra.

### Cấu trúc

- `stat01/`, `stat02/`, `stat03/`: từng tập độc lập.
- `stat03/lesson.py`: dữ liệu và lời giảng thuần Python (không phụ thuộc Manim).
- `stat03/scene.py`: lớp Manim `STAT03`.
- `scripts/build_stat03_typst.py`: biên dịch 8 công thức Typst thành SVG.
- `scripts/prepare_stat03.py`: tạo runtime, SRT, tùy chọn giọng Edge TTS.
- `scripts/qa_stat03.py`: kiểm tra MP4 thật, tiếng khi bật, độ phân giải, thời lượng và 8 ảnh chụp từng chương.
- `.github/workflows/render-stat03.yml`: workflow GitHub Actions có lựa chọn preview/Full HD và voice off/on.
- `LOI_GIANG_STAT03.md`, `STORYBOARD_STAT03.md`: tài liệu sư phạm.
- `preview/stat03/`: bản thiết kế để xem trước, **không phải khung hình từ video render**.

### Chạy thử

```bash
python -m unittest discover -s tests -v
python scripts/build_stat03_typst.py
python scripts/prepare_stat03.py --voice off
manim -ql -r 854,480 --fps 24 stat03/scene.py STAT03
```

Xem `HUONG_DAN_RENDER_STAT03.md` để chạy GitHub Actions và nghiệm thu.

**Trạng thái:** kiểm thử Python đã thực hiện; chưa biên dịch Typst hoặc render video Manim thực tế trong môi trường soạn mã. Cần kiểm tra MP4 từ GitHub Actions.
