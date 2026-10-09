# STAT07 – Hướng dẫn GitHub Actions & nghiệm thu

## Các lựa chọn
- `quality = preview` tạo 854×480, 24 fps.
- `quality = fullhd` tạo 1920×1080, 30 fps.
- `voice = off`: không đọc nhưng vẫn có video có thời lượng nền.
- `voice = on`: cần Internet để tổng hợp giọng đọc tiếng Việt; nếu lỗi TTS, job phải báo lỗi thay vì xuất video câm.

## Các bước
1. Giải nén ZIP và sao chép **nội dung** (không đặt thêm một thư mục cha) vào repository `sangmath-thong-ke`.
2. Commit và push; `.github/workflows/render-stat07.yml` phải nằm đúng vị trí.
3. Vào **Actions → Render STAT07 - Mau so lieu ghep nhom - Histogram → Run workflow**.
4. Chọn `preview`, `off`. Workflow lần lượt: cài môi trường, chạy kiểm thử, kiểm tra 32 trạng thái qua mock, biên dịch **8 công thức Typst thành SVG**, tạo kế hoạch 32 nhịp, **smoke-render thực tế 32 trạng thái**, render cả bài, kiểm tra MP4 và xuất 8 ảnh theo chương.
5. Tải Artifacts. Kiểm tra ảnh `chapter_01` đến `chapter_08`, nhãn tiếng Việt, các ranh giới lớp, chiều rộng cột histogram, lời giải và độ dài.
6. Sau khi duyệt hình, chạy `voice=on`, rồi Full HD.

## Các phép kiểm soát toán học
- Các lớp nửa kín: `[4;6)`, `[6;8)`, `[8;10)`, `[10;12)` với tần số `6,18,14,2`.
- Tần số tích lũy `6,24,38,40`; tỷ lệ `15%,45%,35%,5%`.
- Ghép nhóm khác: `[4;6),[6;7),[7;9),[9;11)` cho `6,8,18,8`. Histogram với độ rộng khác nhau dùng mật độ `3,8,9,4`: **tổng diện tích = 40**.
- Trung bình dữ liệu gốc `7,1` và **ước lượng từ trung điểm nhóm** `7,6` không phải cùng một đại lượng chính xác.
- Bài tập 20 quan sát có bảng `5,7,6,2` và tích lũy `5,12,18,20`.

## Nếu build lỗi
- `ModuleNotFoundError`: kiểm tra vị trí folder `stat07/` và `stat01/`; cần chạy lệnh ở root repository.
- `Missing Typst SVG`: xem bước `build_stat07_typst.py`, kiểm tra phiên bản Typst.
- Lỗi `SVG parse`: kiểm tra tệp SVG của công thức tương ứng trong `assets/stat07_formulas/`.
- Lỗi Manim ở nhịp muộn: xem bước `STAT07_SMOKE`, vì smoke-render thực tế đi qua toàn bộ 32 cảnh trước khi xuất Full HD.
- Sai thời lượng/không có tiếng: xem `qa_stat07.py`, `stat07/runtime_plan.json` và TTS log.

**Chưa có MP4 thực tế nào được xác nhận trong môi trường soạn.** Kiểm thử mô phỏng không thay thế render Manim thật. Luôn xem thử MP4 trước khi phát cho học sinh.
