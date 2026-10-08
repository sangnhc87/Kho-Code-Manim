# SANG MATH · COMB11 V2 — HOÁN VỊ VÒNG TRÒN

Tập 11 của Series **Đại số tổ hợp Manim–Typst**. Dự án chứa toàn bộ COMB01–COMB10 V2 và GEO01 cùng các workflow cũ; tập 11 được bổ sung độc lập.

## Mục tiêu học tập

- Phân biệt hoán vị vòng tròn với hoán vị theo hàng; mỗi cấu hình vòng chỉ tính một lần dưới phép quay.
- Chứng minh công thức `(n-1)!` khi có n người phân biệt ngồi quanh bàn **không có ghế đánh số**.
- Không tự chia 2 cho ảnh gương trừ khi đề cho phép lật; phân biệt mô hình ghế được đánh số.
- Áp dụng gộp khối, phần bù, đếm vị trí, nam nữ xen kẽ và bao hàm–loại trừ.

## Nội dung

- 48 nhịp bài giảng thuộc 8 chương, mục tiêu thời lượng nền khoảng 17 phút 53 giây.
- Lời giảng tiếng Việt theo nhịp, phụ đề SRT và TTS tùy chọn.
- Ví dụ trọng tâm: 6 người có 120 vòng, A-B ngồi cạnh 48, không cạnh 72, 3 nam/3 nữ xen kẽ 12, ba cặp vợ chồng không đôi nào cạnh nhau 32.
- Hình bên trái, lý giải và công thức Typst bên phải; cảnh quay vòng và biến đổi nhóm được minh họa bằng Manim.

## Tệp chính

- `episodes/comb11_circular_permutations.py` — Scene `COMB11`.
- `comb11_lesson_data.py`, `comb11_beats.json` — toán và kịch bản 48 nhịp.
- `scripts/prepare_comb11_v2.py` — biên dịch công thức Typst, chuẩn bị TTS và SRT.
- `scripts/qa_comb11_v2.py` — xác minh MP4 và tạo 8 ảnh QA.
- `.github/workflows/render-comb11-v2.yml` — workflow render có preview/FullHD và voice on/off.
- `narration_COMB11_v2.md`, `storyboard_COMB11_v2.md`, `HUONG_DAN_RENDER_COMB11_V2.md`.

## Lệnh kiểm thử và render

```bash
python -m unittest discover -s tests -v
python scripts/prepare_comb11_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb11_circular_permutations.py COMB11
```

**Lưu ý:** đã kiểm tra logic toán và Python; chưa xác nhận render Manim/Typst tại môi trường soạn. Bản MP4 đầu tiên từ GitHub Actions phải được duyệt hình, tiếng và công thức trước khi công bố.


---

## COMB12 V2 — Phương pháp gộp khối (Video 12)

- Manim scene: `episodes/comb12_block_method.py` → `COMB12`
- Data & math model: `comb12_lesson_data.py`, `comb12_beats.json`, `comb12_formulas.json`
- Typst + TTS + SRT: `scripts/prepare_comb12_v2.py`
- Quality-control report & 8 captures: `scripts/qa_comb12_v2.py`
- GitHub workflow: `.github/workflows/render-comb12-v2.yml`
- Full storyboard: `storyboard_COMB12_v2.md`
- Vietnamese voice: `narration_COMB12_v2.md`
- GitHub guide: `HUONG_DAN_RENDER_COMB12_V2.md`

**Vui lòng render preview và duyệt thực tế trước khi dùng giảng dạy; Python tests chưa xác nhận Manim/TTS chạy thành công.**
