# COMB22 V2 – QUY HOẠCH ĐỘNG TRONG TỔ HỢP

## 1. Trạng thái bàn giao

Gói này **đã có code Manim–Typst và GitHub Actions**, nhưng chưa có MP4 Manim được render và nghiệm thu thực tế trong môi trường biên soạn. Các phép đếm đã được kiểm tra bằng thuật toán độc lập. Không nhầm storyboard PNG với khung hình từ video thật.

Video gồm 8 chương × 6 nhịp = **48 nhịp giảng**. Thời lượng thiết kế khi tắt giọng đọc khoảng **22 phút 29 giây**; khi bật thuyết minh, thời lượng sẽ tự căn theo âm thanh thực tế của từng nhịp. Phụ đề `.srt` và lời giảng được sinh cùng một nguồn dữ liệu.

## 2. Các tệp chính

- `episodes/comb22_dynamic_programming.py`: Scene `COMB22`, tám mô hình DP có trạng thái chuyển động.
- `comb22_lesson_data.py`: 48 nhịp giảng và các thuật toán đếm chính xác.
- `comb22_beats.json`, `comb22_formulas.json`, `comb22_chapters.json`: dữ liệu nội dung, công thức Typst và chương.
- `scripts/prepare_comb22_v2.py`: tạo PNG Typst, giọng đọc, lời thuyết minh và phụ đề.
- `scripts/qa_comb22_v2.py`: kiểm tra thời lượng/độ phân giải/tiếng và trích 8 khung hình.
- `tests/test_comb22_dynamic_programming.py`: kiểm thử độc lập và trường hợp biên.
- `.github/workflows/render-comb22-v2.yml`: workflow GitHub Actions riêng cho tập 22.
- `preview/comb22_v2/storyboard_8_chapters.png`: storyboard, **không phải** MP4 được render.

## 3. Render trên GitHub Actions

1. Giải nén `SangMath_COMB22_V2_GitHubReady.zip` vào thư mục repository đang sử dụng. Chép **nội dung** bên trong thư mục, không đẩy nguyên tệp ZIP lên GitHub.
2. Commit, push và mở tab **Actions**.
3. Chọn **Render COMB22 V2 - Quy hoach dong - Dynamic Programming** rồi bấm **Run workflow**.
4. Lượt thứ nhất: `quality = preview`, `voice = off`. Chờ Actions hoàn tất, mở **Artifacts** để tải MP4 và ảnh QA.
5. Duyệt tính đúng toán học, cách mở dần lời giải, chữ tiếng Việt, công thức và hình trước khi bật TTS.
6. Lượt thứ hai: `voice = on`; cần kết nối dịch vụ Edge TTS. Nghe và kiểm tra tiếng Việt, nhất là tên thuật ngữ DP, bitmask, ma trận.
7. Khi đã đạt yêu cầu, chọn `quality = fullhd` để xuất **1920×1080, 30 FPS**.

**Chú ý:** Workflow chỉ có thể tải được MP4 khi render hoàn thành. Nếu Manim/Typst lỗi, mở phần log của bước bị lỗi rồi gửi đoạn lỗi để sửa; các bài kiểm thử Python thành công không đảm bảo mọi công thức Typst hay hiệu ứng Manim đã render thành công.

## 4. Lệnh kiểm tra cục bộ hoặc trên Codespaces

```bash
python -m unittest discover -s tests -v
python scripts/prepare_comb22_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb22_dynamic_programming.py COMB22
```

Nếu bật tiếng, thay `--voice off` thành `--voice on` trước khi gọi Manim. Sau khi có MP4:

```bash
python scripts/qa_comb22_v2.py --video media/videos/comb22_dynamic_programming/480p24/COMB22.mp4 --voice off
```

Đường dẫn thật trong `media/videos` phụ thuộc cấu hình Manim; trên GitHub Actions workflow tự tìm tệp chính xác.

## 5. Những kiểm chứng toán học quan trọng

| Nội dung | Đáp số |
|---|---:|
| Đường đi (4 phải, 3 lên) | 35 |
| Không đi qua đỉnh (2,1) | 17 |
| Lát sáu ô bằng viên 1 hoặc 2 | 13 |
| Dãy 6 bit không có 11 | 21 |
| Dãy 6 bit không chứa 101 | 37 |
| Phân công 4 việc, không ai trùng chỉ số | 9 |
| Vòng 8 vị trí đánh số, không có hai số 1 kề nhau | 47 |
| Dãy 10 bit, đúng 4 số 1, tránh 101, kết thúc 0 | 48 |

**Giữ nguyên quy ước:** khi xuất hiện tổ hợp, ký hiệu `C_k^n` thể hiện **n ở trên, k ở dưới**; không đổi sang ký hiệu khác tùy ý.

## 6. Kiểm tra sư phạm sau render

- Đề bài phải xuất hiện trước khi đáp số lộ ra; hình bên trái, suy luận bên phải không chồng lấn.
- Với lưới, học sinh phân biệt được vật cản và con đường hợp lệ.
- Với máy tránh mẫu, cung chuyển bị cấm phải có màu đỏ và không được đưa vào phép đếm.
- Với bài toán vòng tròn, **các vị trí được đánh số**, không được chia kết quả cho số phép quay.
- Trong capstone, ba điều kiện được kiểm tra đồng thời; đáp án 48 phải tương ứng đúng ba điều kiện.
- Chỉ phát hành video chính thức sau khi duyệt cả hình ảnh, thời lượng và tiếng đọc.