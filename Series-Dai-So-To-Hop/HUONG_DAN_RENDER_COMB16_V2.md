# COMB16 V2 · CHIA NHÓM VÀ PHÂN CÔNG VAI TRÒ

**SANG MATH – Series Đại số tổ hợp, Video 16.**

- Manim Community + Typst; hai cột cố định, nền tối, font Noto Sans.
- 8 chương, 48 nhịp, mỗi nhịp tối thiểu 24,5 giây.
- Bài giảng chính: chia nhóm có nhãn và không có nhãn, nhóm cùng cỡ hoặc khác cỡ, ghép cặp, chọn trưởng, điều kiện A–B và tổng hợp HSG.
- Ký hiệu theo Series: `C_(k)^(n)` (n ở trên và k ở dưới).
- Chưa có MP4 Manim đã nghiệm thu. Hãy render `preview` trên GitHub Actions và duyệt hình trước khi xuất Full HD.

## Bài toán tổng hợp

Chia 9 học sinh thành 3 nhóm 3 người không có tên, A và B ở hai nhóm khác nhau, sau đó chọn một trưởng nhóm trong mỗi nhóm.

Cách 1: `(280 - 70) × 3³ = 5670`.

Cách 2: `C_2^7 × C_2^5 × 3³ = 5670` (theo quy ước thầy sử dụng: 7 và 5 đặt ở trên, 2 ở dưới).

## Cấu trúc

- `episodes/comb16_group_division.py`: mã Scene `COMB16`.
- `comb16_beats.json`, `comb16_chapters.json`, `comb16_formulas.json`: nội dung từng nhịp và công thức.
- `comb16_lesson_data.py`: mô hình và hàm kiểm chứng toán học độc lập.
- `scripts/prepare_comb16_v2.py`: biên dịch PNG Typst, giọng TTS tùy chọn, tạo phụ đề và manifest thời gian.
- `scripts/qa_comb16_v2.py`: nghiệm thu MP4 và trích 8 khung hình.
- `tests/test_comb16_v2.py`: bài kiểm thử mới.
- `.github/workflows/render-comb16-v2.yml`: render cloud (preview / Full HD; voice on/off).
- `preview/comb16_v2/`: storyboard *thiết kế* (không phải kết quả render Manim).

## Render trong repository

1. Giải nén ZIP. Chép **nội dung** vào gốc repository hiện có; bảo đảm có thư mục ẩn `.github/workflows/`.
2. Commit & push.
3. Vào `Actions → Render COMB16 V2 - Chia nhom va phan cong vai tro → Run workflow`.
4. Trước tiên chọn `quality=preview`, `voice=off`. Tải MP4 và ảnh QA ở Artifacts.
5. Duyệt xong mới chạy `quality=fullhd`, tùy chọn `voice=on` nếu TTS có kết nối.

Lệnh local tương ứng:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/prepare_comb16_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb16_group_division.py COMB16
```

**Lưu ý:** `voice=on` tổng hợp giọng Việt nhờ `edge-tts`, cần kết nối Internet trong GitHub Actions. Độ dài MP4 được căn theo clip âm thanh chứ không theo số chữ ước tính. Artifact có thời hạn lưu trữ; hãy tải về sau khi job thành công.
