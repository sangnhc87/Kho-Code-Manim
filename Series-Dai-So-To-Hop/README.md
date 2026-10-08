# SANG MATH · ĐẠI SỐ TỔ HỢP MANIM–TYPST

Dự án Series COMB01–COMB14 (V2) + GEO01. **Tập mới nhất: COMB14 – Phương pháp đếm phần bù.** Các tập cũ kế thừa từ gói COMB13, không thay đổi.

## Video COMB14

- 8 chương, 48 nhịp, 3.831 từ lời giảng; thời lượng nền thiết kế 18:34 (thời lượng có giọng đọc có thể dài hơn).
- Manim scene: `episodes/comb14_complement.py` → `COMB14`.
- Kịch bản nội dung: `comb14_beats.json`; chương: `comb14_chapters.json`; công thức Typst: `comb14_formulas.json`.
- Chương trình chuẩn bị: `scripts/prepare_comb14_v2.py`.
- Kiểm thử và hậu kiểm: `tests/test_comb14_v2.py`, `scripts/qa_comb14_v2.py`.
- Workflow GitHub: `.github/workflows/render-comb14-v2.yml`.
- Bản tham khảo thiết kế: `preview/comb14_v2/storyboard_8_chapters.png` (không phải ảnh Manim đã render).
- Đọc `HUONG_DAN_RENDER_COMB14_V2.md` trước khi chạy.

## Triết lý và quy ước

Công thức tổng quát **đếm thỏa = đếm tất cả − đếm không thỏa** chỉ đúng sau khi làm rõ tập kết quả và hai miền đối lập. Các trường hợp có nhiều điều kiện cấm phải xem xét phần giao; không mặc nhiên trừ các nhóm vi phạm độc lập.

Manim dựng hình và chuyển động; Typst dựng các công thức. Nền tối, màn hình hai cột, không để chữ đè hình; đề bài hiện trước lời giải. Chỉnh hợp/tổ hợp trình bày theo yêu cầu của Series: chỉ số trên `n`, chỉ số dưới `k`, như `A^(n)_(k)` và `C^(n)_(k)`.

## Lệnh để kiểm tra/chuẩn bị

```bash
python -m unittest discover -s tests -v
python scripts/prepare_comb14_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb14_complement.py COMB14
```

## Trạng thái chất lượng

Kiểm thử toán, toàn bộ unit tests và cú pháp Python được thực hiện trong môi trường xây dựng mã. **Chưa thể xác nhận video Manim xuất thực tế** nếu chưa chạy workflow GitHub; điều này không được xem là nghiệm thu hình ảnh hoặc tiếng đọc.


## COMB15 V2 — Lập số tự nhiên thỏa điều kiện về chữ số

- Tệp Scene: `episodes/comb15_number_formation.py` — class `COMB15`.
- Bộ dữ liệu: `comb15_lesson_data.py`, `comb15_beats.json`, `comb15_formulas.json`.
- Build/TTS: `scripts/prepare_comb15_v2.py`.
- QA: `scripts/qa_comb15_v2.py`, `tests/test_comb15_v2.py`.
- Workflow: `.github/workflows/render-comb15-v2.yml`.
- 48 nhịp giảng; 8 chương; trên 19 phút nền, 1080p/30 fps khi chọn fullhd.
- Bài cuối: chữ số 0..5, 4 chữ số khác nhau, lớn hơn 3000, chia hết 15: 24 số.
- Thời lượng thực tế/độ hoàn thiện thị giác vẫn phải kiểm chứng sau khi render trên GitHub Actions.
