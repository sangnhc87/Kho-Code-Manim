# HƯỚNG DẪN RENDER COMB10 V2 BẰNG GITHUB ACTIONS

## Đưa vào repository đang dùng

1. Giải nén `SangMath_COMB10_V2_GitHubReady.zip` và **chép nội dung bên trong** vào gốc repository cũ (không chỉ chép ZIP).
2. Đảm bảo `.github/workflows/render-comb10-v2.yml` nằm chính xác trong thư mục `.github/workflows/` tại gốc repository.
3. Commit và push lên nhánh mặc định. Workflow COMB01–COMB09 vẫn được giữ nguyên.

## Chạy render

1. Mở **Actions** → **Render COMB10 V2 - Hoan vi cac phan tu giong nhau** → **Run workflow**.
2. Chọn `quality: preview`, `voice: off` để kiểm tra hình 854×480, 24fps.
3. Khi đạt, chạy `quality: preview`, `voice: on` để thử giọng tiếng Việt. Chế độ on cần kết nối mạng đến dịch vụ TTS.
4. Chạy `quality: fullhd`, `voice: on` để xuất 1920×1080, 30fps khi bản thử đã được duyệt.
5. Tải **Artifacts**: MP4, 8 ảnh QA, bảng liên hệ, báo cáo, phụ đề SRT và kịch bản.

## Nếu workflow thất bại

- `typst compile ...`: lỗi công thức hoặc phông; gửi toàn bộ log ở bước **Prepare PNG formula sheets**.
- `ModuleNotFoundError`: xem bước cài Python packages.
- `Render ...`: gửi tên Scene, traceback của Manim và 1–2 khung hình nếu có.
- `Voice`: nếu mạng chặn Edge TTS, hãy chạy `voice: off` để xét hình trước.
- `QA Export too short` hoặc `Time mismatch`: không bỏ kiểm tra; gửi MP4 và log để điều chỉnh đúng nhịp.

**Quan trọng:** phụ đề `.srt` là file rời, không phải phụ đề đã cháy vào video. `voice=on` tổng hợp tiếng đọc tự động; cần giáo viên nghe và duyệt phát âm.
