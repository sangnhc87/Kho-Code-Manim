# HƯỚNG DẪN RENDER COMB25 V2 BẰNG GITHUB ACTIONS

## 1. Cập nhật repository
Giải nén ZIP trọn bộ rồi **chép nội dung bên trong** vào gốc repository của thầy (không commit file ZIP như một tệp thay cho nguồn). Duy trì thư mục ẩn `.github/workflows/`. Commit và push.

Nếu đã có đầy đủ COMB01–COMB24, có thể dùng gói `SangMath_COMB25_Patch_GitHubReady.zip` để chỉ chép phần mới cho COMB25, đồng thời cập nhật README.

## 2. Chạy workflow
Vào **Actions → Render COMB25 V2 - Olympiad Finale - Burnside - Polya → Run workflow**.

**Lần 1:** `quality=preview`, `voice=off`. Workflow cài FFmpeg/Manim/Typst/font Noto, chạy các tests, biên dịch 48 công thức `.typ` ra PNG, render MP4 854×480/24 fps và trích 8 ảnh QA.

**Lần 2:** `quality=preview`, `voice=on`. Cần mạng ra dịch vụ TTS Edge. Thời lượng tự theo âm thanh thực tế. Nếu TTS lỗi, xem log; không nên bỏ qua lỗi để xuất video mất tiếng.

**Lần 3:** `quality=fullhd`, `voice=on`, xuất 1920×1080/30fps.

Tại trang tác vụ đã chạy xong, mở mục **Artifacts** tải MP4, phụ đề SRT, bản lời giảng, ảnh QA và JSON báo cáo.

## 3. Kiểm tra chất lượng

- Xác nhận MP4 dài ít nhất 23 phút; script QA kiểm tra đúng manifest và định dạng video.
- Kiểm tra ảnh từng chương, tránh chữ đè lên khung hình.
- Soát các phép quay/phản chiếu: nhóm quay khác nhóm dihedral.
- Bài lập phương: 24 phép quay, đúng 5 loại; đáp số 57.
- TTS có thể dài hơn thời lượng nền 24:53.

## 4. Tình trạng kiểm thử
Các kiểm thử đại số, Burnside/Pólya và liệt kê độc lập đã chạy; code Manim chưa render thật trong môi trường soạn. Hãy xem đây là bản sẵn sàng chạy thử trên Actions, không phải video đã được duyệt hình/tiếng.
