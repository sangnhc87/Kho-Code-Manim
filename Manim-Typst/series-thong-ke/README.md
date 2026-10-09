# SangMath – Series Thống kê THPT 18 tập

**Hoàn thành mã nguồn 18/18 tập.** Mỗi tập có kịch bản, bài giảng tiếng Việt, mã Manim, công thức Typst, workflow GitHub Actions và hướng dẫn kiểm tra. **Chưa có chứng nhận đã nghiệm thu MP4 thật:** cần render trên runner có Manim, Typst, FFmpeg và kiểm tra hình/tiếng trước khi dạy.

## Tập cuối: STAT18 – Lấy mẫu, thiên lệch và mô phỏng

- 8 chương, 32 phân cảnh, thời lượng nền 20 phút 16 giây.
- Quần thể 1000 học sinh giả lập; 400 chọn phương án A. Lấy mẫu ngẫu nhiên đơn không hoàn lại, mẫu thuận tiện, phản hồi tự nguyện; 300 lần mô phỏng ở từng cỡ mẫu 20 và 80.
- Sai số chuẩn với hiệu chỉnh quần thể hữu hạn và minh họa khoảng tin cậy xấp xỉ. Phân biệt dao động ngẫu nhiên và thiên lệch chọn mẫu.
- Giọng nam tiếng Việt `vi-VN-NamMinhNeural`, footer **Thầy Nguyễn Văn Sang**; không hiện số phân cảnh hoặc tên công nghệ trên video.
- Tài liệu tập cuối: `HUONG_DAN_RENDER_STAT18.md`, `LOI_GIANG_STAT18.md`, `STORYBOARD_STAT18.md`, `STAT18_MANIFEST.json`.

## Khởi chạy

Chạy trong repository đầy đủ chứa `.github/workflows/` và `stat01` tới `stat18`. Vào **Actions → Render STAT18 - Lay mau, Thien lech va Mo phong → Run workflow**. Chạy preview/off trước, sau đó preview/on để nghe giọng nam, cuối cùng fullhd/on để xuất 1920×1080, 30 FPS. Mỗi tập cũ có workflow riêng.

```bash
python -m unittest discover -s tests -v
python scripts/build_stat18_typst.py
python scripts/prepare_stat18.py --voice off
python scripts/check_stat18_states.py
manim -ql -r 854,480 --fps 24 stat18/scene.py STAT18
```

## Cấu trúc tập

| Phần | Vị trí |
|---|---|
| Nội dung, lời giảng | `statXX/lesson.py` |
| Hình và chuyển động | `statXX/scene.py` |
| Công thức | `typst/statXX/*.typ` |
| Biên dịch, thuyết minh, QA | `scripts/*statXX*.py` |
| Workflow | `.github/workflows/render-statXX.yml` |
| Kiểm thử | `tests/test_statXX.py` |
| Storyboard, hướng dẫn | `STORYBOARD_STATXX.md`, `HUONG_DAN_RENDER_STATXX.md` |

**Chú ý:** ảnh trong `preview/` chỉ là thiết kế tham khảo, không thay cho ảnh QA được trích từ MP4 thật. Mọi số liệu mô phỏng chỉ có giá trị minh họa phương pháp.
