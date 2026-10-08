# HƯỚNG DẪN RENDER COMB17 V2 – NHỊ THỨC NEWTON

## 1. Cập nhật vào repository cũ

Giải nén `SangMath_COMB17_V2_GitHubReady.zip`. Sao chép **các thư mục và tệp bên trong** vào thư mục gốc của repository hiện dùng, không tải ZIP nguyên khối. Giữ nguyên `.github/workflows/` (thư mục bắt đầu bằng dấu chấm). Commit và push lên nhánh mặc định.

Gói này **giữ lại mã nguồn và workflow của COMB01–COMB16 cùng GEO01**. Các tệp mới chính là `comb17_beats.json`, `comb17_lesson_data.py`, `comb17_formulas.json`, `comb17_chapters.json`, `episodes/comb17_binomial_theorem.py`, các script và workflow riêng cho COMB17.

## 2. Chạy trên GitHub Actions

Vào **Actions → Render COMB17 V2 - Nhi thuc Newton tu phep chon → Run workflow**.

- **Lần thử thứ nhất:** `quality=preview`, `voice=off`. Tải MP4 và bộ ảnh QA trong **Artifacts** để duyệt bố cục, đồ họa, công thức, tiến trình lập luận.
- **Lần thử thứ hai:** `quality=preview`, `voice=on`. Kiểm tra toàn bộ giọng đọc tiếng Việt, dấu câu, nhịp hoạt hình và âm thanh.
- **Sau khi duyệt:** `quality=fullhd`, `voice=on` để xuất bản 1920×1080/30fps.

Khi `voice=on`, GitHub Actions phải kết nối được dịch vụ Edge TTS. Nếu bị chặn hoặc giới hạn mạng, hãy chạy `voice=off` để kiểm tra hình trước. Workflow có kiểm tra MP4 về thời lượng, độ phân giải, luồng âm thanh khi có giọng đọc, và trích tám khung hình thuộc tám chương.

## 3. Chạy thủ công

Từ thư mục gốc repository:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -q
python scripts/prepare_comb17_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb17_binomial_theorem.py COMB17
```

Xuất 1080p:

```bash
manim -qh -r 1920,1080 --fps 30 episodes/comb17_binomial_theorem.py COMB17
```

Cần cài Manim Community, Typst, FFmpeg, font Noto Sans/Serif và các thư viện nền của Manim trước khi chạy. Các công thức được xuất từ Typst thành ảnh PNG trong `assets/comb17v2/`.

## 4. Tiêu chuẩn nghiệm thu

1. 48 nhịp và 8 chương; không xuất nhầm video quá ngắn.
2. Không có chữ tràn khung hoặc công thức bị che khuất; đề bài phải xuất hiện trước đáp số.
3. Hệ số xuất phát từ phép đếm vị trí, không chỉ từ biến đổi thuộc lòng.
4. Dùng thống nhất ký hiệu tổ hợp **n ở trên, k ở dưới**, dạng Typst `C^(n)_(k)`.
5. Hệ số `x³` của `(2x−1)^6` là `−160`; bài cuối của `(1+x)^4(1+2x)^3` là `96`.
6. Khi bật thuyết minh, lời giảng không bị cắt hoặc trễ so với cảnh.

**Trạng thái:** Mã mới đã chạy kiểm thử Python, nhưng chưa được render và nghiệm thu MP4 trên môi trường hiện tại. Thời lượng im lặng theo lịch khoảng 20 phút 53 giây; TTS có thể kéo dài thêm tùy tốc độ giọng đọc.
