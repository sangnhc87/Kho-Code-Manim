# SERIE TRẢI PHẲNG — VIDEO 18, 19, 20

Ba video này dùng cùng cơ sở Manim–Typst và quy trình GitHub Actions như Video 17.

## Cách nộp lên GitHub
1. Giải nén ZIP tại THƯ MỤC GỐC của repository (giữ nguyên cây thư mục).
2. Kiểm tra 3 mã Python nằm trong `Manim-Typst/`.
3. Kiểm tra 3 workflow `.yml` nằm trong `.github/workflows/`.
4. Commit và push cả hai thư mục.
5. Mở GitHub → Actions → chọn `Render Trai Phang 18 MASTER`, `19 MASTER`, `20 MASTER`.
6. Nhấn **Run workflow**. Mỗi video xuất file MP4 1920x1080/30fps có tiếng vào Artifacts.

Video 18: một mặt bị cấm, hộp 8×5×4.
Video 19: hộp 4×6×t, đổi phương án tại t=6.
Video 20: Capstone, quy trình liệt kê, mở dải, lọc, chọn đường tốt nhất.

## Lưu ý
- Đây là mã nguồn .py + workflow .yml, không phải file .typ riêng.
- Máy tạo gói không cài Manim/Typst/Edge TTS nên chưa kiểm chứng render thực tế; pipeline có preflight + smoke render trước full video.
- Trong quá trình tải Artifact, kiểm tra MP4 và giọng đọc.
