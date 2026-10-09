# SangMath – THỐNG KÊ TRỰC QUAN – STAT01

## Dữ liệu biết nói: Từ 40 điểm kiểm tra đến bức tranh của cả lớp

**Đây là repository độc lập cho Series Thống kê 10–11–12**, không cần tải toàn bộ code 25 tập Đại số tổ hợp để chạy. Đây là code **sẵn sàng thử render**, chưa phải MP4 Manim đã nghiệm thu.

- `STAT01`: Scene Manim Community, 16:9, nền tối, font Noto Sans, bố cục hai cột; 8 chương, 32 nhịp, 704 giây (**11:44**) trước khi giọng đọc làm kéo dài.
- 40 điểm kiểm tra **giả lập**; dữ liệu, bảng tần số, tần số tương đối và biểu đồ dùng chung `stat01/lesson.py`.
- Animation minh họa: các thẻ điểm tự sắp xếp thật, bảng tần số, biểu đồ cột có gốc 0, biểu đồ điểm, biểu đồ tỉ lệ, bài học về biểu đồ gây hiểu nhầm, bài tự kiểm tra.
- Typst tạo công thức toán **SVG vector**; Manim đưa SVG vào hình động; không cài LaTeX.
- Có lời dẫn tiếng Việt hoàn chỉnh theo từng nhịp và phụ đề `.srt`. Bật `voice=on` dùng Edge TTS qua Internet trong GitHub Actions, không tự động xuất bản im lặng nếu TTS lỗi.
- Workflow kiểm tra **thời lượng, độ phân giải và audio**, trích 8 khung hình theo chương; bản cuối cần giáo viên xem duyệt.

## Tải về và đưa lên GitHub

Tạo repository mới (gợi ý: `sangmath-thong-ke`), giải nén ZIP, đưa toàn bộ **nội dung bên trong** thư mục vào gốc repository (kể cả thư mục ẩn `.github`). Commit/push. Không upload nguyên ZIP.

Vào **Actions → Render STAT01 - Du lieu biet noi - Manim Typst → Run workflow**, chọn:

- `quality=preview`, `voice=off`: kiểm tra hình nhanh ở 854×480, 24 FPS.
- `quality=preview`, `voice=on`: kiểm tra lời đọc tiếng Việt và phụ đề.
- `quality=fullhd`, `voice=on`: xuất 1920×1080, 30 FPS.

Trong **Artifacts**, tải MP4, phụ đề SRT và các ảnh QA. Nếu GitHub Actions lỗi, gửi phần cuối log để sửa chính xác.

## Chạy cục bộ (Linux có Manim/Typst)

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/build_typst.py
python scripts/prepare.py --voice off
manim -ql -r 854,480 --fps 24 stat01/scene.py STAT01
VIDEO=$(find media/videos -type f -name 'STAT01.mp4' | head -n 1)
python scripts/qa_video.py --video "$VIDEO" --quality preview --voice off
```

Với giọng đọc Việt:

```bash
python scripts/prepare.py --voice on
manim -qh -r 1920,1080 --fps 30 stat01/scene.py STAT01
```

Lưu ý: Edge TTS phụ thuộc dịch vụ bên ngoài, có thể gián đoạn; bản `voice=off` không phụ thuộc TTS.

## Cấu trúc dự án

| Đường dẫn | Mục đích |
|---|---|
| `stat01/lesson.py` | Bộ số liệu cố định, tần số, 32 lời giảng và 8 chương; không phụ thuộc Manim |
| `stat01/scene.py` | Hình động Manim và thiết kế 16:9 |
| `typst/*.typ`, `scripts/build_typst.py` | Công thức Typst; biên dịch SVG trước khi render |
| `scripts/prepare.py` | Tạo audio tùy chọn, lịch nhịp, phụ đề |
| `scripts/qa_video.py` | QA video render thật, xuất 8 ảnh kiểm tra |
| `tests/test_statistics.py` | Kiểm thử tính nhất quán toán học và kịch bản |
| `STORYBOARD_STAT01.md`, `LOI_GIANG_STAT01.md` | 32 nhịp, lời dẫn đầy đủ |
| `preview/STAT01_storyboard_8_chapters.png` | Phác thảo bố cục **không phải ảnh render Manim** |
| `.github/workflows/render-stat01.yml` | Workflow render và xuất video |

## Quy ước cho các tập kế tiếp

Lấy cùng bộ `SCORES` để dạy biểu đồ, trung bình, trung vị, mốt, tứ phân vị, phương sai… theo thứ tự hợp lý. Không gán dữ liệu giả lập cho lớp thật. Thay đổi số liệu phải cập nhật từ **một nguồn duy nhất**, sau đó chạy test lại.

**Trạng thái:** Kiểm thử dữ liệu/cấu trúc Python tại thời điểm bàn giao; chưa có MP4 Manim và Typst được nghiệm thu thực tế ở môi trường soạn.
