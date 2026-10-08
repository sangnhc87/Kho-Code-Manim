# HƯỚNG DẪN GITHUB ACTIONS — COMB13 V2

**Tập 13: Các phần tử không được đứng cạnh nhau.**

1. Tải và giải nén ZIP, chép **nội dung bên trong** vào gốc repository GitHub hiện có. Đừng tải cả ZIP lên mà không giải nén. Phải giữ thư mục ẩn `.github/workflows/`.
2. Commit và push. Trong tab **Actions**, chọn **Render COMB13 V2 - Khong dung canh nhau**.
3. Chạy thử với `quality=preview`, `voice=off`. Sau khi hoàn thành, tải `COMB13-V2-preview-voice-off` ở Artifacts và kiểm tra bảng ảnh `qa_comb13_v2/contact_sheet.jpg`.
4. Chạy `quality=preview`, `voice=on` để tổng hợp giọng đọc tiếng Việt (Edge TTS cần mạng). Khi TTS thất bại, workflow báo lỗi thay vì lặng lẽ tạo video không lời.
5. Sau khi hình và tiếng đạt yêu cầu, chạy `quality=fullhd`, `voice=on` để xuất 1920×1080 30 fps.

Workflow sẽ kiểm thử toán, biên dịch 48 biểu thức Typst, tổng hợp lời giảng, render Scene `COMB13`, dùng ffprobe xác nhận MP4 đủ độ dài/âm thanh/độ phân giải rồi trích 8 khung hình kiểm tra.

**Không nhầm lẫn:** thời lượng nền là thời lượng của các nhịp trong code, không phải bằng chứng MP4 đã render. Nếu phiên bản có lời đọc dài hơn thì mỗi nhịp tự đợi cho đủ thời lượng âm thanh.

**Tự kiểm thử toán và chuẩn bị trước khi render:**

```bash
python -m unittest discover -s tests -v
python scripts/prepare_comb13_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb13_not_adjacent.py COMB13
```

Bài toán cuối tập: 8 học sinh, AB/CD/EF đều không kề. Kết quả được kiểm tra bằng liệt kê độc lập là **17.760**.
