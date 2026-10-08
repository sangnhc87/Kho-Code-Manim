# Hướng dẫn render COMB24 V2 · Catalan, Dyck, phản xạ

## Cập nhật GitHub

1. Giải nén `SangMath_COMB24_V2_GitHubReady.zip`.
2. Chép **toàn bộ nội dung bên trong** (bao gồm thư mục ẩn `.github`) vào thư mục gốc repository SangMath hiện có.
3. Commit và push. Trên GitHub mở **Actions → Render COMB24 V2 - Catalan - Dyck - Nguyen ly phan xa → Run workflow**.
4. Chạy `quality=preview`, `voice=off` để xem bố cục ở 854×480, 24 fps; trong Artifacts có MP4, SRT và 8 ảnh kiểm tra.
5. Nếu đạt, chạy tiếp `quality=preview`, `voice=on` để xem tiếng Việt (cần mạng truy cập dịch vụ Edge TTS).
6. Cuối cùng chọn `quality=fullhd`, độ phân giải 1920×1080, 30 fps.

## Bước kiểm tra trước khi render

```bash
python -m unittest discover -s tests -v
python scripts/prepare_comb24_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb24_catalan_reflection.py COMB24
```

## Ghi chú kỹ thuật

- Bố cục 2 cột: hình động trái, lời giải và công thức Typst phải.
- Ký hiệu kiểu đã chốt với người dùng: `C_k^n` (n ở **trên**, k ở **dưới**).
- Thuyết minh được tạo từng nhịp và ghép đúng thời lượng nhạc/giọng; `voice=off` vẫn dành đủ thời gian cho lời giảng.
- Preview/storyboard PNG là ảnh mô phỏng để xem trước, **không phải ảnh trích từ render Manim**.
- Chưa có MP4 được nghiệm thu trong môi trường soạn; cần duyệt cả hình và tiếng trên GitHub Actions.
