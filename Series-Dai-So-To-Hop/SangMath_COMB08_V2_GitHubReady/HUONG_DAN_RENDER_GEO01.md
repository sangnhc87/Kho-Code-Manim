# HƯỚNG DẪN GITHUB ACTIONS — VIDEO RIÊNG GEO01

**Video GEO01 độc lập, không thay thế COMB01 hoặc COMB02.** Gói ZIP chứa cả COMB01, COMB02 để có thể chép toàn bộ vào một GitHub repository chung.

## Đưa code lên GitHub

1. Tải ZIP, giải nén trên máy tính.
2. Chép **toàn bộ nội dung bên trong thư mục** vào gốc repository Series trên GitHub, kể cả thư mục ẩn `.github`.
3. Commit và push lên nhánh mặc định (`main` hoặc `master`). Nếu chưa có repo, tạo repo mới và tải toàn bộ nội dung giải nén vào gốc.
4. Mở tab **Actions** → chọn `Render GEO01 - Point Inside Triangle - Manim Typst` → **Run workflow**.
5. Chọn `preview` để kiểm tra trước. Khi xong, mở lần chạy ở Actions → **Artifacts** → tải `GEO01-preview-MP4-and-QA.zip`.
6. Trong Artifacts có `GEO01.mp4`, tám ảnh PNG và `contact_sheet.png` để duyệt bố cục.
7. Khi preview đạt, chạy lại, chọn `fullhd` (1920×1080, 30 fps).

## Chạy tại máy có Manim + Typst

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/build_geo_formulas.py
manim -ql --fps 24 episodes/geo01_point_inside_triangle.py GEO01
manim -qh -r 1920,1080 --fps 30 episodes/geo01_point_inside_triangle.py GEO01
```

> **Lưu ý:** workflow không tự tạo giọng đọc. Video là hình động + đề/lập luận/công thức; lời dẫn tiếng Việt ở `narration_GEO01.md` để ghép audio trong giai đoạn sau. Render Full HD dài hơn preview.

## Nếu Actions báo lỗi

Gửi toàn bộ phần log bước thất bại; quan trọng nhất là bước `Compile Typst formulas` hoặc `Preview render`. Gửi thêm `contact_sheet.png` để tôi sửa cỡ chữ, bố cục, hình học. Code đã qua kiểm tra cú pháp và toán, nhưng nếu chưa chạy thực tế thì không coi là đã nghiệm thu hình.
