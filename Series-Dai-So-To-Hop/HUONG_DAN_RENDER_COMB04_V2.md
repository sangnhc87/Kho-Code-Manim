# COMB04 V2 — KHI NÀO THỨ TỰ QUAN TRỌNG?

**Mã nguồn mới:** `episodes/comb04_order_matters.py` — Scene Manim `COMB04`.

## Render ngay trên GitHub Actions

1. Giải nén ZIP và chép **toàn bộ nội dung bên trong** thư mục lên gốc repository đã chứa các tập COMB01–03. Phải giữ thư mục ẩn `.github/workflows`.
2. Commit/push thay đổi.
3. Mở **Actions → Render COMB04 V2 - Bai giang day du Manim Typst** → **Run workflow**.
4. Lần đầu: `quality=preview`, `voice=on`. Nếu lỗi kết nối Edge TTS, thử lại `voice=off` để kiểm tra hình.
5. Tải artifact `COMB04-V2-preview-voice-on` chứa MP4, SRT, báo cáo JSON và tám ảnh chụp một ảnh mỗi chương.
6. Duyệt hình và lời giảng trước khi dùng `quality=fullhd` (1920×1080/30fps).

## Đặc tả và thời lượng

- 8 chương × 6 nhịp = **48 nhịp**; lời dẫn tiếng Việt **2.497 từ**.
- Thời lượng nền **850 giây (14 phút 10 giây)** tính cả kết thúc; với TTS tự điều chỉnh lên nếu âm thanh chậm hơn.
- Mỗi nhịp đọc trọn một đoạn, phụ đề SRT tạo đồng bộ từ cùng một nguồn dữ liệu.
- Chủ đề: 12 phân công và 6 nhóm trong bốn người; AB và BA; sáu thứ tự của bộ ba ABC; 60 dãy có thứ tự và 10 nhóm; 30 phân công và 15 nhóm của sáu người; 168 đội ba người có đội trưởng.
- Chưa giới thiệu ký hiệu chỉnh hợp/tổ hợp trong bài 04, vì 05–07 mới là các bài hình thành công thức. Khi dùng ký hiệu, thống nhất **n ở trên, k ở dưới**: `A^(n)_(k)` và `C^(n)_(k)` theo cấu hình `series_config.py`.

## Các bước chạy cục bộ (nếu có Manim và Typst)

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/prepare_comb04_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb04_order_matters.py COMB04
# Hoặc render với giọng đọc:
python scripts/prepare_comb04_v2.py --voice on
manim -qh -r 1920,1080 --fps 30 episodes/comb04_order_matters.py COMB04
```

## QA và các lỗi cần kiểm tra sau render đầu tiên

- Nhãn vai trò **TRƯỞNG/PHÓ** phải cố định trong khi thẻ A/B hoán đổi.
- Bảng 12 cặp có thứ tự, sáu cặp nhóm tương đương, sáu hoán vị ABC và danh sách 15 nhóm không được bị cắt.
- Cột bên phải không tràn chữ; công thức Typst ở dưới ba ý giải thích.
- Video phải có âm thanh khi `voice=on`, không có đoạn giọng đọc bị cắt.
- QA kiểm tra thời lượng (>= 810 giây), file âm thanh nếu cần, độ phân giải, tạo 8 ảnh chụp và contact sheet.

**Trạng thái:** Đã kiểm tra cú pháp, phép đếm và mã chuẩn bị; chưa render MP4 Manim thật tại môi trường đóng gói vì chưa cài Manim/Typst. Video đầu tiên trên GitHub Actions là bản cần nghiệm thu thực tế. Không xem các ảnh storyboard là ảnh chụp từ Manim.
