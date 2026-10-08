# SANG MATH · Manim–Typst · Đại số tổ hợp (mùa 1)

## COMB01 v2.0 — QUY TẮC CỘNG (nâng cấp bài giảng dài)

**Thay thế hẳn code COMB01 ngắn trước đây.** Scene giữ tên `COMB01`, tệp giữ đường dẫn `episodes/comb01_rule_of_sum.py`, workflow giữ đường dẫn `.github/workflows/render-comb01.yml`, nên chỉ cần chép đè code vào repository cũ. COMB02 và GEO01 **giữ nguyên**, không bị xóa.

- 8 chương, 42 nhịp nội dung; **~12 phút 52 giây khi không bật tiếng**. Khi bật TTS, thời lượng phụ thuộc tốc độ đọc thực tế, đồng bộ theo từng clip, không cắt câu đọc.
- Bài toán 2 xe buýt / 3 tàu; phân nhóm X, Y; quy tắc cộng; bài chọn 4 sách Toán hoặc 3 sách Vật lí; phần giao trong tập các số 1–12; ví dụ 10 số lẻ + 5 bội của 4 trong 1–20; so sánh hoặc / và; hai bài củng cố.
- Hình động ở cột trái, đề bài và lập luận ở cột phải. Các kết luận xuất hiện **sau** thao tác quan sát, không hiển thị toàn bộ ngay từ đầu.
- Công thức được biên dịch bằng Typst, hình học/di chuyển bằng Manim; font Noto hiển thị tiếng Việt.
- Tùy chọn đọc tiếng Việt bằng Microsoft Edge TTS (`vi-VN-NamMinhNeural`), do GitHub Actions tự tạo 42 clip và ghép đồng bộ vào video. Cần runner có quyền truy cập dịch vụ TTS; đây là dịch vụ bên ngoài, có thể gặp giới hạn/kết nối thất bại.
- Hệ thống kiểm tra MP4 dài ít nhất 660 giây và **phải có luồng audio nếu bật TTS**, trích 8 ảnh đại diện của 8 chương.
- Ở nơi đóng gói, chưa có Manim/Typst và không truy cập Internet để cài; code đã qua kiểm tra cú pháp và các phép đếm, **chưa được khẳng định đã render/kiểm tra khung hình Manim thật**. Hãy kiểm tra preview trên GitHub trước khi xuất bản.

### Hướng dẫn nhanh để đưa lên GitHub

1. Giải nén toàn bộ ZIP. Đưa **nội dung bên trong thư mục**, kể cả thư mục ẩn `.github`, vào gốc repository có COMB01/COMB02/GEO01.
2. Commit, push, vào **Actions → Render COMB01 V2 - Bai giang day du Manim Typst**.
3. Chọn `quality = preview`, `voice = on` (có thuyết minh tiếng Việt) rồi chạy.
4. Trong `Artifacts` tải `COMB01-V2-preview-voice-on` gồm video MP4, bộ ảnh 8 chương, contact sheet và báo cáo thời lượng. Nếu ưng ý, chọn `quality=fullhd` để xuất 1920×1080/30 fps.
5. Khi TTS Edge gặp lỗi mạng, chạy `voice=off` để kiểm tra hình. Bản này vẫn dài khoảng 12m52s nhưng **không có tiếng đọc**.

### Chạy thủ công trên Linux/macOS có Manim, Typst và FFmpeg

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/prepare_comb01_v2.py --voice on
manim -ql -r 854,480 --fps 24 episodes/comb01_rule_of_sum.py COMB01
# hoặc
manim -qh -r 1920,1080 --fps 30 episodes/comb01_rule_of_sum.py COMB01
```

Nếu không dùng TTS: `python scripts/prepare_comb01_v2.py --voice off`.

### Các tệp quan trọng

| Tệp | Nội dung |
|---|---|
| `episodes/comb01_rule_of_sum.py` | Scene Manim COMB01 **mới** |
| `comb01_lesson_data.py` | 42 nhịp: đề bài, lý giải, lời giảng, thời lượng |
| `scripts/prepare_comb01_v2.py` | Biên dịch 10 công thức Typst, dựng 42 clip TTS và file manifest |
| `scripts/qa_comb01_v2.py` | Kiểm tra MP4, âm thanh, trích 8 ảnh, contact sheet |
| `narration_COMB01_v2.md` | Bản lời đọc rút gọn thực tế, căn mốc theo thời lượng dự kiến |
| `storyboard_COMB01_v2.md` | Đề cương và quy tắc nghiệm thu từng chương |
| `.github/workflows/render-comb01.yml` | Workflow mới thay thế workflow COMB01 cũ |
| `episodes/comb02_rule_of_product.py` | Code COMB02 cũ giữ nguyên |
| `episodes/geo01_point_inside_triangle.py` | Code GEO01 cũ giữ nguyên |

### Quy ước ký hiệu tổ hợp/chỉnh hợp cho các tập sau

Thực hiện đúng ký hiệu thầy đã chốt: `C^(n)_(k)` và `A^(n)_(k)` (n phía trên, k phía dưới). Đây là chế độ `COMB_NOTATION=user` được khai báo trong `series_config.py`. SGK Việt Nam thường in chỉ số ngược lại; lựa chọn này đã được ghi chú rõ. COMB01 chưa cần dùng ký hiệu A/C.

### Tinh thần thiết kế

Chú trọng **bản chất phép đếm**, không kéo dài bằng animation trang trí. Công thức chỉ xuất hiện sau lập luận, màu đỏ dùng để cảnh báo kết quả bị tính hai lần (không phải kết quả không hợp lệ); phân biệt rõ trường hợp không giao nhau và có giao nhau.
