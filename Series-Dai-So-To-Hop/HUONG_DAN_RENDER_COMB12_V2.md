# HƯỚNG DẪN RENDER COMB12 V2 — GITHUB ACTIONS

## A. Cập nhật repository cũ

1. Tải và giải nén **SangMath_COMB12_V2_GitHubReady.zip**.
2. Sao chép **toàn bộ các tệp và thư mục bên trong** vào thư mục gốc repository cũ (nơi đã chứa `episodes/` và `.github/`). Không upload nguyên ZIP và không tạo thêm một thư mục lồng ở gốc repository.
3. Commit và push. Các tập COMB01–COMB11, GEO01 vẫn có trong gói này.

## B. Chạy tự động

- GitHub → repository → Actions → **Render COMB12 V2 - Gop khoi - phan tu dung canh** → Run workflow.
- Lần đầu chọn **quality=preview** và **voice=off** để kiểm tra hình, công thức, thời lượng.
- Tải file MP4, bảng ảnh tám chương, báo cáo `qa_comb12_v2/report.json` trong Artifacts.
- Nếu preview ổn mới chạy **voice=on** để lấy tiếng Việt; TTS cần kết nối Internet đến nhà cung cấp giọng đọc.
- Cuối cùng chọn **quality=fullhd** (1920×1080, 30 fps).

## C. Chạy lệnh tương đương khi dùng Linux có Manim, Typst

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/prepare_comb12_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb12_block_method.py COMB12
VIDEO=$(find media/videos -type f -name 'COMB12.mp4' | head -n 1)
python scripts/qa_comb12_v2.py --video "$VIDEO" --voice off
```

**Chú ý:** `--skip-typst` chỉ tạo mã công thức `.typ` mà chưa tạo PNG; không được dùng khi render Manim thật.

## D. Checklist nghiệm thu

- [ ] 8 chương, 48 nhịp; MP4 dài tối thiểu khoảng 18 phút (nếu không bật giọng đọc).
- [ ] Không còn chữ tràn hai cột hoặc công thức ảnh PNG trắng.
- [ ] Các khối AB, ABC, AB/CD hiện đúng; không dùng cùng một người trong hai khối độc lập.
- [ ] Phần giao hai biến cố được trừ đúng và sơ đồ không gây hiểu nhầm tỉ lệ diện tích.
- [ ] Bàn tròn chỉ đồng nhất phép quay, không tự ý đồng nhất phép gương.
- [ ] Lời đọc nếu bật phải có tiếng, không bị cắt mất câu; phụ đề đúng ngữ cảnh.
- [ ] Bài nâng cao bảy người ra 1968, kiểm chứng bằng Python.

Nếu GitHub Actions báo lỗi, gửi thầy cô **log bước lỗi** và MP4 / ảnh contact sheet (nếu có); những tệp này giúp sửa nhanh hơn chỉ dựa vào ảnh chụp toàn bộ trang GitHub.
