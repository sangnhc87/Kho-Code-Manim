# HƯỚNG DẪN RENDER COMB07 V2 (TỔ HỢP)

## Đưa mã lên GitHub

1. Tải `SangMath_COMB07_V2_GitHubReady.zip` và giải nén.
2. Sao chép **toàn bộ nội dung bên trong** thư mục vừa giải nén vào **gốc repository đang có COMB01–COMB06**. Chấp nhận ghi đè những file trùng tên nếu chúng là từ phiên bản V2 trước.
3. Giữ cả thư mục ẩn `.github/workflows/`, `assets`, `episodes`, `scripts`, `tests`, `voice`.
4. Commit và push. Không đặt file ZIP nguyên trong repo; không đặt các tệp vào thư mục con thừa.
5. Trên GitHub chọn **Actions → Render COMB07 V2 - Bai giang To Hop Manim Typst → Run workflow**.
6. Lần đầu chọn **quality=preview, voice=off** để kiểm tra nhanh hình/công thức. Sau đó dùng `voice=on` để thử giọng đọc tiếng Việt; nếu TTS lỗi mạng có thể chạy `voice=off` trước.
7. Tại cuối workflow mở **Artifacts**, tải `COMB07-V2-preview-voice-off` (hoặc tương ứng). MP4 có tên `COMB07.mp4`. Bên cạnh có `qa_comb07_v2/contact_sheet.jpg`, 8 ảnh chương, `report.json`, file SRT, lời dẫn và manifest.
8. Nếu preview đạt, chạy **quality=fullhd, voice=on** để xuất Full HD 1080p/30fps.

## Các tệp chính

- **Mã Manim:** `episodes/comb07_combinations.py`, Scene `COMB07`.
- **Dữ liệu toán và thời lượng:** `comb07_lesson_data.py`, `comb07_beats.json`.
- **Biên dịch Typst / tạo giọng đọc / phụ đề:** `scripts/prepare_comb07_v2.py`.
- **Kiểm tra MP4 và trích ảnh:** `scripts/qa_comb07_v2.py`.
- **Workflow:** `.github/workflows/render-comb07-v2.yml`.
- **Thuyết minh:** `narration_COMB07_v2.md`.
- **Ký hiệu:** `series_config.py`, mặc định kiểu người dùng `C^(n)_(k)`, `A^(n)_(k)`.

## Tự chạy thử bằng máy Linux đã có Manim, Typst

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/prepare_comb07_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb07_combinations.py COMB07
VIDEO=$(find media/videos -type f -name COMB07.mp4 | head -n 1)
python scripts/qa_comb07_v2.py --video "$VIDEO" --voice off
```

## Những giới hạn phải kiểm tra

- 48 nhịp × 19,25 giây + đoạn cuối = **929,2 giây (15 phút 29 giây)** ở chế độ không có tiếng. Có giọng TTS, thời lượng có thể dài hơn.
- `voice=on` dùng giọng TTS trực tuyến `vi-VN-NamMinhNeural`; không phải file giọng thu thủ công. Nếu dịch vụ mạng không khả dụng, workflow báo lỗi đúng nguyên nhân.
- Chỉ báo hoàn thành **render thực tế** sau khi GitHub Actions tạo MP4 và QA thông qua. Các phép kiểm thử Python không thay thế xem video bằng mắt.
