# STAT18 – Lấy mẫu, thiên lệch và mô phỏng (TẬP CUỐI)

## Bài học

- **Chủ đề:** quần thể và mẫu; rút mẫu ngẫu nhiên đơn; mẫu thuận tiện, tự nguyện, không phản hồi; dao động lấy mẫu; mô phỏng 300 lần; cỡ mẫu; khoảng ước lượng; tổng kết series.
- **Đối tượng:** học sinh THPT (nội dung lấy mẫu và khoảng tin cậy là *mở rộng vận dụng*, không thay yêu cầu chương trình cơ bản).
- **Cấu trúc:** 8 chương × 4 phân cảnh, **32 phân cảnh**, thời lượng nền **1216 giây (20 phút 16 giây)**. Nếu giọng đọc dài hơn, video tự điều chỉnh nhịp chờ theo file âm thanh.
- **Dữ liệu:** mô phỏng 1000 học sinh (400 chọn A), không phải dữ liệu khảo sát thật.
- **Giọng mặc định:** nam Việt `vi-VN-NamMinhNeural`. **Footer đúng:** `Thầy Nguyễn Văn Sang`.
- **Không có:** số nhịp, mốc kỹ thuật, tên công nghệ dựng, gắn nhãn debug trong hình.

## Cách đưa lên repository

Đã có STAT01–17: giải nén `SangMath_ThongKe_STAT18_Patch_GitHubReady.zip` và chép **nội dung bên trong** vào gốc repository; đảm bảo thấy `.github/workflows/render-stat18.yml`, `stat18/`, `scripts/`, `typst/` và `tests/`.

Muốn repository từ đầu: dùng **duy nhất** `SangMath_ThongKe_STAT01_STAT18_GitHubReady.zip`, giải nén và push tất cả tệp. **Không** chép cả hai gói chồng lên nhau, và không commit tệp zip mà không giải nén.

## Dựng bằng GitHub Actions

Mở **Actions → Render STAT18 - Lay mau, Thien lech va Mo phong → Run workflow**.

1. Chạy `quality=preview`, `voice=off`. Workflow thực hiện unit test → kiểm tra mô phỏng 32 phân cảnh → biên dịch 8 SVG Typst → tạo timeline và phụ đề → **smoke-render Manim thật** → render MP4.
2. Tải Artifacts xem MP4 854×480, báo cáo QA, 8 ảnh trích từ video và hình phác thảo. Kiểm tra font Việt, nhãn tỉ lệ, trục đồ thị, thanh 40%–70%, dải khoảng, chuyển động con trỏ và lúc đáp án bài cuối xuất hiện.
3. Chạy `quality=preview`, `voice=on`, **nghe thực tế giọng nam** và rà việc chữ/công thức xuất hiện phù hợp. TTS dùng Edge TTS qua mạng. Lỗi TTS phải làm job thất bại, không giả tạo tệp video có tiếng.
4. Chỉ khi đạt yêu cầu, chạy `quality=fullhd`, `voice=on` để xuất **1920×1080, 30 FPS**.

### Lệnh Linux cục bộ (đã cài Manim, Typst, FFmpeg)

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/check_stat18_states.py
python scripts/build_stat18_typst.py
python scripts/prepare_stat18.py --voice off
manim -ql -r 426,240 --fps 8 stat18/scene.py STAT18_SMOKE
manim -ql -r 854,480 --fps 24 stat18/scene.py STAT18
VIDEO=$(find media/videos -type f -name 'STAT18.mp4' | head -n 1)
python scripts/qa_stat18.py --video "$VIDEO" --quality preview --voice off
```

### Rà các phép tính

| Kiểm tra | Kết quả đúng |
|---|---|
| Quần thể tổng | 1000 học sinh |
| Số học sinh chọn A | 400 = 40% |
| Mẫu ngẫu nhiên n=20 | 7/20 = 35% |
| Mẫu ngẫu nhiên n=80 | 37/80 = 46,25% |
| Mô phỏng lặp | 300 lần riêng cho mỗi cỡ mẫu; lấy mẫu không hoàn lại trong từng lần |
| Độ lệch chuẩn tỉ lệ mẫu n=20 (hữu hạn) | ≈ 10,85 điểm % |
| Độ lệch chuẩn tỉ lệ mẫu n=80 (hữu hạn) | ≈ 5,26 điểm % |
| Khảo sát tự nguyện | 70/100 = 70%, **ví dụ có thiên lệch cố ý** |
| Bài tập mẫu ngẫu nhiên | 88/200 = 44% |
| Bài tập mẫu thuận tiện | 150/200 = 75% |
| Khoảng minh họa dạng chuẩn (không hiệu chỉnh) | 44% ± 1,96√(0,44×0,56/200) ≈ [37,1%; 50,9%] |

**Lưu ý sư phạm:** khoảng tin cậy dạng chuẩn ở đây chỉ mang tính minh họa xấp xỉ, không phải khẳng định xác suất cho tham số cố định, không dùng để hợp thức hóa mẫu tự nguyện. Biểu thức sai số chuẩn lý thuyết ở chương 5 *có hiệu chỉnh hữu hạn*, còn khoảng đơn giản ở chương 6 cố ý là *xấp xỉ chưa hiệu chỉnh*; phải giải thích rõ hai mức độ này nếu mở rộng bài giảng.

**Tình trạng nghiệm thu:** Bộ mã và file thiết kế chưa thay thế được việc kiểm tra render Manim/Typst và xem MP4 thực tế. Mọi file `preview/stat18/*.png` là hình thiết kế, không phải ảnh chụp video.
