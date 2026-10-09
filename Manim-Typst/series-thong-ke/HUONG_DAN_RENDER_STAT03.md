# Render THONG-KE-03 — Số trung bình, trung vị và mốt

## Cập nhật GitHub

- Nếu repository đã có STAT01–STAT02: giải nén `SangMath_ThongKe_STAT03_Patch_GitHubReady.zip` và chép đè các tệp đúng vị trí gốc. **Không** tải ZIP nguyên khối vào repository.
- Nếu muốn dự án trọn bộ: dùng `SangMath_ThongKe_STAT01_STAT02_STAT03_GitHubReady.zip`.
- Cấu trúc `.github/workflows/render-stat03.yml` phải nằm ngay trong gốc repository, kể cả dấu chấm trước `github`.
- Commit và push lên nhánh mặc định.

## Thực hiện

1. GitHub → **Actions** → **Render STAT03 - So trung binh - Trung vi - Mot - Manim Typst** → **Run workflow**.
2. Chọn `quality=preview`, `voice=off`. Chờ hoàn tất rồi tải Artifact MP4 + 8 ảnh QA.
3. Xem thật kỹ các điểm: dữ liệu trung bình 7,1; cột trái và chữ ở cột phải không đè nhau; trung vị là vị trí 20–21; cảnh thay 9 phút bằng 27 phút có dấu dịch chuyển trung bình.
4. Tiếp tục `voice=on` để thử giọng tiếng Việt. Chế độ này sử dụng dịch vụ Edge TTS qua Internet; nếu không có tiếng hoặc tải giọng thất bại, workflow sẽ lỗi thay vì phát hành MP4 giả có tiếng.
5. Duyệt đạt mới chạy `quality=fullhd` để xuất 1920×1080/30fps.

## Lệnh chạy trực tiếp (Linux có Manim, Typst, FFmpeg)

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/build_stat03_typst.py
python scripts/prepare_stat03.py --voice off
manim -ql -r 854,480 --fps 24 stat03/scene.py STAT03
VIDEO=$(find media/videos -type f -name 'STAT03.mp4' | head -n 1)
python scripts/qa_stat03.py --video "$VIDEO" --quality preview --voice off
```

Để có tiếng: `python scripts/prepare_stat03.py --voice on`, sau đó render lại.

## Các điểm cần nghiệm thu

- **Chính xác toán:** 40 điểm có tổng 284, trung bình 7,1, trung vị 7, mốt 7.
- **Ví dụ ngoài điểm số:** chín thời lượng luyện tập ban đầu trung bình = trung vị = mốt = 7 phút; thay 9 bằng 27 phút khiến trung bình = 9, trung vị và mốt vẫn 7. Đây là dữ liệu minh họa **độc lập**, không lấy 27 làm điểm kiểm tra.
- **Thời lượng nền:** 800 giây (13:20) cho 32 nhịp. Có giọng đọc, thời lượng tự tăng nếu âm thanh dài hơn thời gian nền mỗi nhịp.
- **SRT:** lời đọc khớp mốc thời gian theo từng nhịp, phụ đề có thể hiệu chỉnh sau kiểm tra MP4.
- **Quan trọng:** các bài test thuần Python **không** chứng minh Manim/Typst sẽ render thành công. GitHub Actions mới là bước kiểm tra biên dịch thực tế.
