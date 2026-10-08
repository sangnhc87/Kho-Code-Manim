# COMB20 V2 — CÁC TỔNG HỆ SỐ NHỊ THỨC

## 1. Đưa vào GitHub

Giải nén **toàn bộ** ZIP tại thư mục gốc repository đang dùng (không chép nguyên ZIP và không làm mất thư mục `.github/`). Commit và push. Gói chứa đủ các mã COMB01–COMB19 cũ và bổ sung COMB20.

## 2. Render trong GitHub Actions

1. Vào Actions → **Render COMB20 V2 - Cac tong he so nhi thuc - dao ham tich phan**.
2. Chọn **Run workflow**, `quality=preview`, `voice=off` để kiểm tra hình lần đầu.
3. Khi preview đạt, chạy `voice=on` để có giọng đọc tiếng Việt đồng bộ từng nhịp. Cần kết nối dịch vụ TTS; nếu thất bại có thể render `off`.
4. Chạy `quality=fullhd` để xuất 1920×1080, 30 fps.
5. Tải MP4, ảnh theo chương, báo cáo kiểm tra và phụ đề tại Artifacts.

## 3. Cấu trúc gói

- `episodes/comb20_binomial_sums.py`: Scene `COMB20`.
- `comb20_lesson_data.py`: các hàm toán học không phụ thuộc Manim.
- `comb20_beats.json`, `comb20_chapters.json`, `comb20_formulas.json`: 48 nhịp, 8 chương, công thức Typst.
- `scripts/prepare_comb20_v2.py`: biên dịch công thức `.typ → .png`, chuẩn bị giọng đọc, thời gian, phụ đề.
- `scripts/qa_comb20_v2.py`: kiểm tra thời lượng, độ phân giải, tiếng và ảnh.
- `tests/test_comb20_binomial_sums.py`: kiểm tra toán và gói kỹ thuật.
- `LO_TRINH_COMB21_25_OLYMPIAD.md`: đề cương năm tập cao siêu tiếp theo.

## 4. Chạy thủ công (nếu có Manim, Typst và FFmpeg)

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/prepare_comb20_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb20_binomial_sums.py COMB20
```

Để render final: `manim -qh -r 1920,1080 --fps 30 episodes/comb20_binomial_sums.py COMB20`.

## 5. Nghiệm thu

Thời lượng nền dự kiến **20 phút 53 giây** (48 × 26s + đoạn kết 5.2s), giọng đọc có thể kéo dài từng nhịp. Đây là thời lượng *theo mã*, chưa phải MP4 đã render. Việc kiểm thử Python **không thể thay thế** biên dịch Typst và kiểm tra Manim thật. Tránh công bố video khi chưa duyệt ảnh, nhịp chuyển cảnh và tiếng đọc.
