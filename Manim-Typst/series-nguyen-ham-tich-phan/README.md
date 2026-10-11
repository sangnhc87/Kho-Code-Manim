# Nguyên Hàm – Tích Phân – Ứng Dụng Chuyên Sâu (36 tập)

**Thầy Nguyễn Văn Sang** · Manim Community 0.19 + Typst + Edge TTS · GitHub Actions → YouTube

- 📋 Kế hoạch toàn series: [KE_HOACH_SERIES_36_TAP.md](KE_HOACH_SERIES_36_TAP.md) (dữ liệu máy đọc: [series_plan.json](series_plan.json))
- 🎬 Đã dựng: **INT01 – Đi ngược đạo hàm** ([lời giảng](LOI_GIANG_INT01.md)) · **INT02 – Tính chất nguyên hàm & hàm lũy thừa** ([lời giảng](LOI_GIANG_INT02.md)) · **INT03 – Nguyên hàm của 1/x và hàm mũ** ([lời giảng](LOI_GIANG_INT03.md)) · **INT04 – Nguyên hàm lượng giác** ([lời giảng](LOI_GIANG_INT04.md)) · **INT05 – Nguyên hàm của f(ax + b)** ([lời giảng](LOI_GIANG_INT05.md)) · **INT06 – Nguyên hàm có điều kiện & hàm từng khúc** ([lời giảng](LOI_GIANG_INT06.md)) · **INT07 – Nguyên hàm phân thức hữu tỉ** ([lời giảng](LOI_GIANG_INT07.md)) · **INT08 – Phương pháp đổi biến số** ([lời giảng](LOI_GIANG_INT08.md)) · **INT09 – Nguyên hàm từng phần** ([lời giảng](LOI_GIANG_INT09.md)) · **INT10 – Từ tốc độ thay đổi đến đại lượng** ([lời giảng](LOI_GIANG_INT10.md)) · **INT11 – Diện tích dưới đường cong & tổng Riemann** ([lời giảng](LOI_GIANG_INT11.md)) · **INT12 – Định nghĩa tích phân** ([lời giảng](LOI_GIANG_INT12.md)) · **INT13 – Tính chất của tích phân** ([lời giảng](LOI_GIANG_INT13.md)) · **INT14 – Tích phân chứa trị tuyệt đối & hàm từng khúc** ([lời giảng](LOI_GIANG_INT14.md)) · **INT15 – Độ dời và quãng đường** ([lời giảng](LOI_GIANG_INT15.md)) · **INT16 – Tích phân đổi biến số** ([lời giảng](LOI_GIANG_INT16.md)) · **INT17 – Tích phân từng phần** ([lời giảng](LOI_GIANG_INT17.md)) · **INT18 – Hàm ẩn & tính đối xứng** ([lời giảng](LOI_GIANG_INT18.md)) · **INT19 – Hàm ẩn từ phương trình vi phân** ([lời giảng](LOI_GIANG_INT19.md)) · **INT20 – Tổng ôn tích phân (mini-đề 10 câu)** ([lời giảng](LOI_GIANG_INT20.md)) · **INT21 – Diện tích hình phẳng với trục Ox** ([lời giảng](LOI_GIANG_INT21.md)) · **INT22 – Diện tích giữa hai đường cong** ([lời giảng](LOI_GIANG_INT22.md)) · **INT23 – Diện tích có tham số** ([lời giảng](LOI_GIANG_INT23.md)) · **INT24 – Đọc diện tích từ đồ thị f'** ([lời giảng](LOI_GIANG_INT24.md)) · **INT25 – Thể tích theo thiết diện** ([lời giảng](LOI_GIANG_INT25.md)) · **INT26 – Khối tròn xoay quanh Ox** ([lời giảng](LOI_GIANG_INT26.md)) · **INT27 – Khối tròn xoay giữa hai đường** ([lời giảng](LOI_GIANG_INT27.md)) · **INT28 – Dựng lại công thức thể tích** ([lời giảng](LOI_GIANG_INT28.md)) · **INT29 – Bài toán chuyển động thực tế** ([lời giảng](LOI_GIANG_INT29.md)) · **INT30 – Tích phân trong thiết kế** ([lời giảng](LOI_GIANG_INT30.md)) · **INT31 – Bồn chứa và lưu lượng** ([lời giảng](LOI_GIANG_INT31.md)) · **INT32 – Tích phân trong kinh tế & sinh học** ([lời giảng](LOI_GIANG_INT32.md))

## Cấu trúc

```text
common/            engine dùng chung cho cả 36 tập
  theme.py         màu, font, kích thước
  blocks.py        màn hình chuẩn: tiêu đề, mục tiêu, Đúng/Sai, trả lời ngắn, tổng kết, bài tập, tập sau
  kit.py           đồ thị cắt theo khung, trường hướng, tiếp tuyến, xe, đồng hồ, thẻ, badge…
  lesson_scene.py  khung cố định + thanh tiến độ 5 phần + đồng bộ từng nhịp với MP3
  voice.py         Edge TTS (thử lại khi lỗi mạng), mốc câu → phụ đề, chapter YouTube
  typst_build.py   biên dịch công thức Typst → SVG (lỗi là dừng)
int01/
  lesson.py        lời giảng 36 nhịp + 49 công thức + kiểm chứng SymPy (nguồn duy nhất)
  scene.py         một hàm beat_<id> cho mỗi nhịp
scripts/           build_typst · prepare_voice · finalize · qa_video · build_docs
tests/             kiểm tra kế hoạch, nội dung, công thức, phụ đề/chapter
```

## Chạy trên GitHub Actions

**Actions → “Render INT - Nguyen ham Tich phan (36 tap)” → Run workflow**

| Bước | episode | quality | voice | upload | Mục đích |
| :-: | :-: | :-: | :-: | :-: | :-- |
| 1 | int01 | preview | off | ☐ | duyệt bố cục, màu, công thức |
| 2 | int01 | preview | on | ☐ | duyệt giọng đọc, độ khớp hình – lời |
| 3 | int01 | fullhd | on | ☑ | xuất bản YouTube (mô tả có mốc chương) |

Artifacts của mỗi lần chạy: MP4, `INT01_vi.srt`, mô tả YouTube, `qa_report.json` và ảnh chụp từng nhịp (`artifacts/int01_qa/`).

## Chạy trên máy (macOS/Linux có cairo, pango, ffmpeg, typst)

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/build_typst.py --ep int01
python scripts/prepare_voice.py --ep int01 --voice on
manim --disable_caching -ql -r 854,480 --fps 24 int01/scene.py INT01
python scripts/finalize.py --ep int01
```

`--disable_caching` là bắt buộc: các cảnh có trường hướng nhiều đối tượng khiến bộ băm cache của Manim chậm hàng chục lần.

## Thêm một tập mới (INT02 …)

1. Tạo `int02/lesson.py` theo mẫu `int01/lesson.py` (EPISODE, PARTS, BEATS, FORMULAS, EXERCISES, `validate()`).
2. Tạo `int02/scene.py`: `class INT02(LessonScene)` với `EP = 'int02'` và một `beat_<id>(self, T)` cho mỗi nhịp; dùng `self.rt(phần_trăm)` để tính thời lượng animation.
3. Đổi `status` trong `series_plan.json`, thêm test, chạy workflow với `episode=int02`.
