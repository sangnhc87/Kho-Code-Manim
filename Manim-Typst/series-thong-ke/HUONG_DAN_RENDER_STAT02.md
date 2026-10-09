# Render SangMath Thống kê 02 trên GitHub Actions

## Chọn gói cập nhật phù hợp

- Đã có repository của **STAT01**: tải `SangMath_ThongKe_STAT02_Patch_GitHubReady.zip`, giải nén rồi chép nội dung **vào gốc repository**. File `.github/workflows/render-stat02.yml` phải được Git quản lý.
- Chưa có repository hoặc muốn đồng bộ từ đầu: dùng `SangMath_ThongKe_STAT01_STAT02_GitHubReady.zip`, giải nén và đưa toàn bộ nội dung thư mục vào gốc repository. Gói này có cả 01, 02.
- KHÔNG upload nguyên tệp ZIP lên GitHub (Actions không giải nén tự động).

## Workflow

1. Commit và push dữ liệu mới lên GitHub.
2. Vào **Actions → Render STAT02 - Bieu do thong ke - Manim Typst → Run workflow**.
3. Chọn `quality=preview`, `voice=off` cho lượt đầu. Hình 854×480, 24 FPS.
4. Tải tệp `STAT02.mp4`, phụ đề `.srt`, ảnh phác thảo và 8 ảnh QA được trích **trực tiếp từ MP4** tại **Artifacts**. Xem kỹ độ rõ chữ, nhịp xuất hiện, trục đồ thị và tỉ lệ.
5. Chạy `quality=preview`, `voice=on` để thử giọng đọc nữ `vi-VN-HoaiMyNeural` (Edge TTS cần mạng). Khi không tạo được giọng nói, job sẽ **báo lỗi**, không giả vờ đã có tiếng.
6. Khi đã duyệt bản thử, chạy `quality=fullhd`, `voice=on` để xuất **1920×1080, 30 FPS**.

## Các tính chất đã kiểm tra bằng Python

- Mẫu A: **40 quan sát**, điểm 7 có 10 học sinh; bảng tần số: 2, 4, 8, 10, 8, 6, 2.
- Tổng tỉ lệ: **100%**; tổng góc hình tròn: **360°**, riêng điểm 7 là **90°**.
- Ghép điểm theo khoảng `[4,6), [6,8), [8,10), [10,12)` được **6, 18, 14, 2**.
- Mẫu B **giả lập và tách biệt** có 50 học sinh, trong đó 25 đạt từ 8 điểm (50%).
- Histogram khi khoảng không đều dùng chiều cao là **tần số / độ rộng lớp**; diện tích mới tỉ lệ với tần số.
- Bộ điểm trung bình theo sáu tháng là **một ví dụ khác**, không suy từ dữ liệu 40 điểm.

## Chạy trên Linux có Manim, Typst, FFmpeg

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/build_stat02_typst.py
python scripts/prepare_stat02.py --voice off
manim -ql -r 854,480 --fps 24 stat02/scene.py STAT02
VIDEO=$(find media/videos -type f -name 'STAT02.mp4' | head -n 1)
python scripts/qa_stat02.py --video "$VIDEO" --quality preview --voice off
```

Bản có giọng đọc: thay `--voice off` bằng `--voice on` trong bước prepare, rồi render lại; qa cũng thay thành `--voice on`.

**Giới hạn hiện tại:** Bộ mã đã kiểm thử dữ liệu/cấu trúc Python và đã xuất được bản phác thảo bố cục. Không được hiểu là đã kiểm tra MP4 Manim hay SVG Typst trong môi trường soạn. Giáo viên cần duyệt bản render thử trên GitHub.
