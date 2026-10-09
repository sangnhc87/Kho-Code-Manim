# SangMath Thống kê – GitHub Ready (STAT01–STAT07)

Mã nguồn Manim + công thức Typst + lời giảng tiếng Việt + workflow GitHub Actions cho 7 tập đầu. Không xóa các tập cũ khi thêm STAT07.

**Chạy nhanh:** chọn `Actions → Render STAT07 - Mau so lieu ghep nhom - Histogram → Run workflow` với `quality=preview` và `voice=off`.

**Thử local nếu có Manim/Typst:**
```bash
python -m unittest discover -s tests -q
python scripts/check_stat07_states.py
python scripts/build_stat07_typst.py
python scripts/prepare_stat07.py --voice off
manim -ql -r 426,240 --fps 8 stat07/scene.py STAT07_SMOKE
manim -ql -r 854,480 --fps 24 stat07/scene.py STAT07
```

Xem `STORYBOARD_STAT07.md`, `LOI_GIANG_STAT07.md`, `HUONG_DAN_RENDER_STAT07.md`.

Quy ước: nhóm `[a;b)` gồm a và không gồm b; tần số tích lũy luôn tính theo thứ tự lớp; histogram độ rộng khác nhau dùng mật độ tần số để diện tích thể hiện tần số.

**Cần duyệt MP4 thật** trước khi sử dụng giảng dạy. Smoke-render trên GitHub phát hiện nhiều lỗi, nhưng không thay thế kiểm tra sư phạm bằng mắt.


## STAT08 – Số trung bình và mốt của mẫu số liệu ghép nhóm

- 8 chương / 32 nhịp / 16:00 thời lượng nền.
- Code: `stat08/scene.py`; toán: `stat08/lesson.py`; workflow: `.github/workflows/render-stat08.yml`.
- Render hướng dẫn: `HUONG_DAN_RENDER_STAT08.md`; kiểm thử đặc biệt xem `BUILD_NOTES_STAT08.md`.
