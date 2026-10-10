# Nguyên Hàm – Tích Phân – Ứng Dụng Chuyên Sâu (36 tập)

**Thầy Nguyễn Văn Sang** · Manim Community 0.19 + Typst + Edge TTS · GitHub Actions → YouTube

- 📋 Kế hoạch toàn series: [KE_HOACH_SERIES_36_TAP.md](KE_HOACH_SERIES_36_TAP.md) (dữ liệu máy đọc: [series_plan.json](series_plan.json))
- 🎬 Đã dựng: **INT01 – Đi ngược đạo hàm: bản chất nguyên hàm** ([lời giảng](LOI_GIANG_INT01.md))

## Cấu trúc

```text
common/            engine dùng chung cho cả 36 tập
  theme.py         màu, font, kích thước
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
