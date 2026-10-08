# SERIES SANG MATH · ĐẠI SỐ TỔ HỢP — TẬP MỚI NHẤT COMB21

**COMB21 V2: Hàm sinh (Generating Functions)** đã có mã nguồn để thử render: 48 nhịp, 8 chương, 3.271 từ lời giảng; thời lượng thiết kế 21 phút 41 giây trước TTS. `episodes/comb21_generating_functions.py` — Scene `COMB21`. Workflow: `.github/workflows/render-comb21-v2.yml`. Xem `HUONG_DAN_RENDER_COMB21_V2.md`.

Cấu trúc giữ các tập COMB01–20 + GEO01. Các tệp mới dùng tiền tố COMB21/comb21. Ký hiệu tổ hợp luôn là `C^(n)_(k)` với n trên, k dưới.

**Trạng thái QA:** Chưa render MP4 thực tế tại môi trường soạn. Đã kiểm tra mã Python, số học, thời lượng theo kịch bản và cấu trúc workflow. GitHub Actions phải chạy để biên dịch Typst, render Manim và kiểm tra ảnh/âm thanh.

---

# COMB18 V2 - TAM GIAC PASCAL VA CAC TINH CHAT

Video 18 duoc bo sung vao du an COMB01-COMB17 ma khong thay the ma Scene cu.

- **48 nhip giang / 8 chuong**; thoi luong nen thiet ke 19 phut 17 giay (co TTS co the dai hon).
- **Manim:** `episodes/comb18_pascal_triangle.py` -> class `COMB18`.
- **Typst:** 48 cong thuc voi ky hieu `C^(n)_(k)` (n o tren).
- **Loi giang:** `narration_COMB18_v2.md`, phu de `subtitles_COMB18_v2.srt`.
- **Actions:** `.github/workflows/render-comb18-v2.yml`; xem `HUONG_DAN_RENDER_COMB18_V2.md`.
- **QA:** `tests/test_comb18_pascal.py`, `scripts/qa_comb18_v2.py`, 8 anh storyboard.
- Khong tu nhan MP4 da render/duyet: ma da duoc kiem tra, render thuc te can GitHub Actions.

---

# COMB17 V2 - Newton qua phep chon

Tiep noi COMB01-COMB16; video COMB17 hoan chinh nguon de render tren GitHub Actions.
- 48 nhip, 8 chuong, ~20 phut 53 giay khong TTS.
- Manim: `episodes/comb17_binomial_theorem.py`, scene `COMB17`.
- GitHub Actions: `.github/workflows/render-comb17-v2.yml`.
- Tai lieu: `HUONG_DAN_RENDER_COMB17_V2.md`.
- Giong doc tieng Viet: `--voice on`; tuy chon `off` de thu hinh.
- Trang thai: da kiem thu Python, chua render Manim that.

---

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


## Video 16 · Chia nhóm và phân công vai trò (COMB16 V2)

Đã bổ sung mã Manim–Typst cho 8 chương/48 nhịp với đầy đủ lời giảng, công thức, phụ đề, kiểm thử và workflow `render-comb16-v2.yml`. Xem `HUONG_DAN_RENDER_COMB16_V2.md` để chạy.

Video 16: 9 học sinh, 3 nhóm 3 vô danh, A và B phải khác nhóm, mỗi nhóm chọn 1 trưởng: **5670 cách**. Bản code cần được render và nghiệm thu MP4 trên GitHub Actions.


## COMB19 V2 – Tập con và công thức 2^n

- 8 chương; 48 nhịp giảng; công thức Typst đúng ký hiệu `C^(n)_(k)` (n ở trên).
- Các mô hình: liệt kê tập con, 0/1, phân lớp theo kích thước, điều kiện A/B, chẵn–lẻ, mạng tập con, không kề nhau, bài nâng cao tám vị trí.
- **Hai cách đếm bài cuối**: 55−21=34 và 13+13+8=34.
- Mã Scene: `episodes/comb19_subsets.py` · Dữ liệu: `comb19_lesson_data.py`, `comb19_beats.json`.
- GitHub workflow: `.github/workflows/render-comb19-v2.yml`.
- Hướng dẫn riêng: `HUONG_DAN_RENDER_COMB19_V2.md`.
- Bản xem trước: `preview/comb19_v2/storyboard_8_chapters.png`.
- Video thực tế chưa được nghiệm thu: chạy workflow với preview, voice off trước khi phát hành.


## COMB19 V2 – Tập con và công thức 2^n

- 8 chương; 48 nhịp giảng; công thức Typst đúng ký hiệu `C^(n)_(k)` (n ở trên).
- Các mô hình: liệt kê tập con, 0/1, phân lớp theo kích thước, điều kiện A/B, chẵn–lẻ, mạng tập con, không kề nhau, bài nâng cao tám vị trí.
- **Hai cách đếm bài cuối**: 55−21=34 và 13+13+8=34.
- Mã Scene: `episodes/comb19_subsets.py` · Dữ liệu: `comb19_lesson_data.py`, `comb19_beats.json`.
- GitHub workflow: `.github/workflows/render-comb19-v2.yml`.
- Hướng dẫn riêng: `HUONG_DAN_RENDER_COMB19_V2.md`.
- Bản xem trước: `preview/comb19_v2/storyboard_8_chapters.png`.
- Video thực tế chưa được nghiệm thu: chạy workflow với preview, voice off trước khi phát hành.


## COMB19 V2 – Tập con và công thức 2^n

- 8 chương; 48 nhịp giảng; công thức Typst đúng ký hiệu `C^(n)_(k)` (n ở trên).
- Các mô hình: liệt kê tập con, 0/1, phân lớp theo kích thước, điều kiện A/B, chẵn–lẻ, mạng tập con, không kề nhau, bài nâng cao tám vị trí.
- **Hai cách đếm bài cuối**: 55−21=34 và 13+13+8=34.
- Mã Scene: `episodes/comb19_subsets.py` · Dữ liệu: `comb19_lesson_data.py`, `comb19_beats.json`.
- GitHub workflow: `.github/workflows/render-comb19-v2.yml`.
- Hướng dẫn riêng: `HUONG_DAN_RENDER_COMB19_V2.md`.
- Bản xem trước: `preview/comb19_v2/storyboard_8_chapters.png`.
- Video thực tế chưa được nghiệm thu: chạy workflow với preview, voice off trước khi phát hành.

## COMB20 V2 – Các tổng hệ số nhị thức

- 48 nhịp, 8 chương; bài giảng từ phép thế → đạo hàm → tích phân → tổng xen dấu → bài nâng cao.
- Mã scene: `episodes/comb20_binomial_sums.py` với lớp `COMB20`.
- Pipeline: `scripts/prepare_comb20_v2.py`, `scripts/qa_comb20_v2.py`.
- GitHub Actions: `.github/workflows/render-comb20-v2.yml`.
- Hướng dẫn render: `HUONG_DAN_RENDER_COMB20_V2.md`.
- Storyboard: `preview/comb20_v2/storyboard_8_chapters.png`.
- Lộ trình 5 tập Olympic: `LO_TRINH_COMB21_25_OLYMPIAD.md`.
- Tổng ở bài cuối: `Σ k² C^(6)_(k) 2^k 3^(6-k) = 112500`.
- Trạng thái: mã và toán đã kiểm thử; Manim/Typst thực tế cần chạy trên GitHub Actions.
