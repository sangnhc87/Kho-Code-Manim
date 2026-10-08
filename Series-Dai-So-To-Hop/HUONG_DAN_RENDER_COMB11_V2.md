# Hướng dẫn render COMB11 V2 – HOÁN VỊ VÒNG TRÒN

## Chuẩn bị

Giải nén gói ZIP. **Chép nội dung bên trong thư mục dự án vào gốc repository hiện có**; giữ thư mục `.github/` và các thư mục `episodes/`, `scripts/`, `tests/`, `assets/`, `voice/` đúng cấu trúc. Không cần tạo repository mới.

## GitHub Actions

1. Commit và push code lên nhánh mặc định của repository.
2. Truy cập **Actions → Render COMB11 V2 - Hoan vi vong tron → Run workflow**.
3. Trước tiên chọn `quality=preview`, `voice=off` để xem hình động và công thức, tốc độ 854×480 / 24 fps.
4. Tải artifact `COMB11-V2-preview-voice-off`; trong đó có MP4 và các ảnh QA tám chương.
5. Kiểm tra xong mới chạy `voice=on`; lưu ý `edge-tts` đòi hỏi dịch vụ giọng nói ngoài còn truy cập được và có thể lỗi mạng.
6. Chạy `quality=fullhd`, `voice=on` để xuất MP4 1920×1080 / 30 fps khi đã nghiệm thu.

## Mã lệnh tương đương

```bash
python -m unittest discover -s tests -v
python scripts/prepare_comb11_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb11_circular_permutations.py COMB11
python scripts/qa_comb11_v2.py --video media/videos/comb11_circular_permutations/480p24/COMB11.mp4 --voice off
```

Đường dẫn MP4 thực tế thay đổi theo cấu hình Manim; workflow tự tìm bằng `find media/videos`.

## Kiểm tra cần thực hiện

- Bàn tròn đang xét **không đánh số ghế**, nên chỉ bỏ phép quay: `(n - 1)!`.
- Hai cấu hình ảnh gương là khác nhau trong bài xếp người thông thường; ví dụ `120/2=60` chỉ khi **đề cho phép lật gương**.
- Cặp AB cạnh nhau bao gồm ghế cuối gần ghế đầu vòng tròn.
- Bài ba cặp không cạnh nhau phải cho **32** theo bao hàm–loại trừ.
- Ký hiệu tổ hợp/chỉnh hợp ở những tập liên quan tiếp tục giữ định dạng đã thống nhất `C^(n)_(k)` và `A^(n)_(k)`.
- `voice=off` chỉ là video hình; `voice=on` mới có giọng đọc AI tiếng Việt.

**Giới hạn bàn giao:** kiểm thử Python và xác minh nội dung toán không thay thế được một lần render Manim/Typst thật. Nếu workflow lỗi, gửi lại log và bộ ảnh QA để sửa tiếp.
