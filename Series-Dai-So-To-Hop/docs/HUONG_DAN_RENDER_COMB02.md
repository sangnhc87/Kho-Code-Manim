# ĐƯA VIDEO 02 LÊN GITHUB ACTIONS

## Đây là gói *cập nhật chung*, không phải repo khác

Trong thư mục này đã có cả `COMB01` và `COMB02`.

- **Video 01**: `episodes/comb01_rule_of_sum.py`, Scene: `COMB01`.
- **Video 02**: `episodes/comb02_rule_of_product.py`, Scene: `COMB02`.
- **Workflow 02**: `.github/workflows/render-comb02.yml`.

### Nếu đang có repository chứa COMB01

1. Giải nén tệp ZIP mới.
2. Sao chép các thư mục và file bên trong ZIP **vào gốc repository hiện có**, cho phép gộp thư mục `episodes`, `scripts`, `tests`, `.github` (không lồng thêm một thư mục vào repository).
3. Commit rồi push lên nhánh mặc định (`main`).
4. Vào GitHub → repository → **Actions** → **Render COMB02 - Manim + Typst** → **Run workflow**.
5. Chọn `quality: preview`; `notation: user` (mặc định ký hiệu C^n_k, A^n_k).
6. Chờ build hoàn thành, chọn run → **Artifacts** → tải tệp `COMB02-preview-user`. Bên trong có video `COMB02.mp4`.
7. Khi đã duyệt preview, chạy lại `quality: fullhd` để có 1920×1080, 30 fps.

### Nếu chưa có repo

Tạo repository GitHub trống, đưa **toàn bộ nội dung đã giải nén** vào gốc repo (đặc biệt giữ nguyên thư mục ẩn `.github/workflows`). Commit, push, rồi chạy tương tự từ bước 4.

### Lưu ý

- Đừng upload ZIP như một tệp duy nhất vào GitHub.
- Không chọn Scene `COMB01` khi muốn render tập 02.
- GitHub Actions chạy bằng runner Linux, không cần mở Manim trên Mac.
- MP4 hiện **chưa có lời đọc/giọng TTS**; kịch bản nằm trong `narration_COMB02.md`. Render preview trước khi đưa vào lớp.
- Khi workflow thất bại, xem bước đỏ đầu tiên trong Actions → log và gửi thông báo lỗi để hiệu chỉnh.
