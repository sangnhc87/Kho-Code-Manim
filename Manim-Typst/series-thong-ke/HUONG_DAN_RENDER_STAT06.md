# STAT06 – Phương sai và độ lệch chuẩn: Hướng dẫn GitHub Actions

## Cập nhật mã nguồn

- Nếu GitHub đã có STAT01–STAT05: giải nén `SangMath_ThongKe_STAT06_Patch_GitHubReady.zip` rồi chép **cả thư mục .github ẩn** và những thư mục/tệp đi kèm vào gốc repository; giữ cấu trúc đường dẫn.
- Nếu chưa có dự án Thống kê: dùng ZIP trọn bộ STAT01–STAT06.
- Commit và push. Vào GitHub → **Actions → Render STAT06 - Phuong sai - Do lech chuan**.

## Quy trình chạy an toàn (nên theo thứ tự)

1. `quality=preview`, `voice=off` để chạy test, biên dịch SVG, smoke-render và bản 854×480.
2. Xem MP4 và 8 ảnh QA trong Artifacts. Nếu công thức/đối tượng lệch hoặc chữ quá nhỏ, sửa trước khi xuất bản.
3. Khi hình đạt, chọn `voice=on` kiểm tra toàn bộ giọng đọc tiếng Việt, phụ đề SRT và âm lượng.
4. Cuối cùng chọn `quality=fullhd`, `voice=on` để xuất 1920×1080 30 FPS.

## Các chốt kiểm tra mới nhằm giảm lỗi build

- Chạy `python -m unittest discover -s tests -v` để kiểm tra toán và tính tương thích STAT01–06.
- Chạy `python scripts/check_stat06_states.py` để dựng mô phỏng **đủ 32 trạng thái** bằng API Manim tối thiểu, phát hiện tham chiếu biến chưa import và lỗi Python thường gặp.
- `python scripts/build_stat06_typst.py` biên dịch **8 SVG Typst thật**; bất kỳ lỗi font/cú pháp/SVG trống đều khiến job thất bại.
- `python scripts/prepare_stat06.py --voice off` tạo runtime plan + SRT. Với `voice on`, nếu Edge TTS không truy cập được, job **báo lỗi**, không xuất video câm giả thành công.
- `manim -ql -r 426,240 --fps 8 stat06/scene.py STAT06_SMOKE` kiểm tra render thật 32 nhịp ở chất lượng thấp; KHÔNG chỉ thử 10 giây đầu.
- Render chính thức xong, `qa_stat06.py` bắt buộc kiểm tra độ phân giải, chênh lệch thời lượng, có audio khi bật voice và trích 8 ảnh kiểm tra.

## Tự chạy preview trong Codespaces hoặc máy riêng

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/check_stat06_states.py
python scripts/build_stat06_typst.py
python scripts/prepare_stat06.py --voice off
manim -ql -r 426,240 --fps 8 stat06/scene.py STAT06_SMOKE
manim -ql -r 854,480 --fps 24 stat06/scene.py STAT06
```

Cần cài thêm Typst CLI, FFmpeg, Cairo/Pango và font Noto Sans. Lệnh `python scripts/build_stat06_typst.py` thất bại trước khi render nếu thiếu Typst.

## Về công thức toán

Với **40 điểm giả lập** đã dùng suốt Series: trung bình `7,1`, phương sai `2,29`, độ lệch chuẩn `√2,29 ≈ 1,513`. Công thức thống kê mô tả ở phổ thông dùng mẫu số `n`. Giá trị `n-1` thuộc ước lượng không chệch của phương sai tổng thể trong thống kê suy luận; không hoán đổi hai công thức.

Thí nghiệm thay một điểm 10 bằng 30 là **dữ liệu giả lập mở rộng**, không phải điểm kiểm tra hợp lệ trên thang 10. Trung bình thành `7,6`, phương sai thành `14,94`, độ lệch chuẩn `≈3,865`.

## Lỗi thường gặp và cách nhận biết

- **Thiếu công thức SVG**: xác nhận bước `Compile all STAT06 Typst formula SVGs` xanh; không copy SVG từ bản preview làm kết quả chính thức.
- **TTS không tạo được MP3**: kiểm tra Internet và log `Prepare 32 beats`; không đánh dấu hoàn tất khi `voice=on` bị lỗi.
- **Frame bị lỗi ở chương cuối**: xem step `STAT06_SMOKE`, chạy nó trước Full HD.
- **QA báo MP4 quá ngắn**: không chỉnh bỏ ngưỡng kiểm tra; xem `stat06/runtime_plan.json` và `ffprobe` của MP4.
- **Thiếu workflow**: `.github/workflows/render-stat06.yml` là thư mục ẩn; nhớ upload lên repository.

**Trạng thái nghiệm thu:** Kiểm thử mã/toán tại môi trường soạn có thể chạy, còn Typst + Manim cần GitHub Actions xác nhận. Cần duyệt hình ảnh và âm thanh sư phạm trước khi dùng dạy học.
