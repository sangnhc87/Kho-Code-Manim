# SANG MATH · ĐẠI SỐ TỔ HỢP — COMB01 đến COMB09 (V2)

**Mới:** COMB09 — Chọn có lặp, dãy có thứ tự và quy tắc n^k.

- Manim: `episodes/comb09_repetition.py` → `COMB09`
- Nội dung chính xác: `comb09_lesson_data.py`, `comb09_beats.json`
- Chuẩn bị Typst, giọng đọc và phụ đề: `scripts/prepare_comb09_v2.py`
- Kiểm tra MP4: `scripts/qa_comb09_v2.py`
- GitHub Actions: `.github/workflows/render-comb09-v2.yml`
- Tài liệu: `HUONG_DAN_RENDER_COMB09_V2.md`

Bản này giữ nguyên mã nguồn tập 01–08 V2 và video phụ GEO01.

**Trạng thái:** mã đã kiểm thử Python; phải chạy preview trên GitHub Actions để duyệt Manim/Typst thực tế.

---

# COMB08 V2 - TONG HOP / SEASON 1 FINALE

**Video moi nhat:** COMB08 - Hoan vi, Chinh hop, To hop; 48 nhip / 8 chuong / nen 16:53 / 3.522 tu tieng Viet. Cac ket qua chinh: 720, 30, 15, 168, 180, 31, 18, 30 va 87. Co hai cach dem cho capstone 87.

**Nguon Manim:** `episodes/comb08_synthesis.py` (scene `COMB08`); **workflow GitHub:** `.github/workflows/render-comb08-v2.yml`; **huong dan:** `HUONG_DAN_RENDER_COMB08_V2.md`; **storyboard:** `preview/comb08_v2/storyboard_8_chapters.png`.

Bo code nay **giu nguyen COMB01-COMB07 V2 va GEO01**. Python + kiem thu toan hoc da chay, chua co MP4 Manim thuc te da render tai moi truong dong goi. Phai duyet video tu Actions truoc khi dua len lop.

---

# COMB07 V2 – TỔ HỢP (bản mới nhất)

**Tập mới:** 48 nhịp / 8 chương / khoảng 15 phút 29 giây không giọng đọc; 3.035 từ thuyết minh tiếng Việt, giọng TTS và SRT theo nhịp; 25 biểu thức Typst biên dịch trong workflow; bộ kiểm thử toán học liệt kê độc lập.

**Render:** `.github/workflows/render-comb07-v2.yml`. **Mã:** `episodes/comb07_combinations.py`. **Hướng dẫn:** `HUONG_DAN_RENDER_COMB07_V2.md`.

Bản này **giữ nguyên COMB01–COMB06 V2 và GEO01**. Chưa có MP4 Manim nghiệm thu; cần chạy GitHub Actions và kiểm tra ảnh QA.

---

# SANG MATH — MANIM–TYPST · ĐẠI SỐ TỔ HỢP (MÙA 1)

## MỚI: COMB02 V2 — QUY TẮC NHÂN (BÀI GIẢNG ĐẦY ĐỦ)

Bản này thay thế video 02 ngắn cũ bằng **44 nhịp / 8 chương**, có các mô hình đếm, bài tập nhiều mức độ, lời giảng đầy đủ và phụ đề SRT. Thời lượng nền **12:57,7** (bao gồm đoạn kết). Khi TTS chạy, nhịp tự động theo độ dài âm thanh nên có thể dài hơn. Code V1 dự phòng tại `episodes/comb02_rule_of_product_v1_backup.py`.

**Nút Actions:** `Render COMB02 V2 - Bai giang day du Manim Typst` → `preview` → `voice=on` → Run workflow. Sau khi duyệt MP4 và 8 ảnh QA mới render `fullhd`.

**Tệp:** `episodes/comb02_rule_of_product.py`, `comb02_lesson_data.py`, `scripts/prepare_comb02_v2.py`, `scripts/qa_comb02_v2.py`, `narration_COMB02_v2.md`, `subtitles_COMB02_v2.srt`, `storyboard_COMB02_v2.md`, `HUONG_DAN_RENDER_COMB02_V2.md`.

**Bộ test:** `python -m unittest discover -s tests -v`. **Trạng thái:** đã kiểm tra toán, Python và chuẩn bị storyboard tĩnh; chưa render MP4 Manim thật tại môi trường đóng gói.

**Đặc biệt về phương pháp:** số cách sau mỗi lựa chọn bước một phải bằng nhau mới nhân trực tiếp; nếu khác nhau thì cộng theo nhánh. Bài áo–quần có cặp cấm được giải theo cả hai cách để HS hiểu bản chất.

---

# SANG MATH · Manim–Typst · Đại số tổ hợp (mùa 1)

## COMB01 v2.0 — QUY TẮC CỘNG (nâng cấp bài giảng dài)

**Thay thế hẳn code COMB01 ngắn trước đây.** Scene giữ tên `COMB01`, tệp giữ đường dẫn `episodes/comb01_rule_of_sum.py`, workflow giữ đường dẫn `.github/workflows/render-comb01.yml`, nên chỉ cần chép đè code vào repository cũ. GEO01 **giữ nguyên**; COMB02 đã được nâng cấp V2, không bị xóa.

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
| `episodes/comb02_rule_of_product.py` | Code COMB02 nay đã nâng cấp V2 |
| `episodes/geo01_point_inside_triangle.py` | Code GEO01 cũ giữ nguyên |

### Quy ước ký hiệu tổ hợp/chỉnh hợp cho các tập sau

Thực hiện đúng ký hiệu thầy đã chốt: `C^(n)_(k)` và `A^(n)_(k)` (n phía trên, k phía dưới). Đây là chế độ `COMB_NOTATION=user` được khai báo trong `series_config.py`. SGK Việt Nam thường in chỉ số ngược lại; lựa chọn này đã được ghi chú rõ. COMB01 chưa cần dùng ký hiệu A/C.

### Tinh thần thiết kế

Chú trọng **bản chất phép đếm**, không kéo dài bằng animation trang trí. Công thức chỉ xuất hiện sau lập luận, màu đỏ dùng để cảnh báo kết quả bị tính hai lần (không phải kết quả không hợp lệ); phân biệt rõ trường hợp không giao nhau và có giao nhau.


## COMB03 V2 – Sơ đồ cây và không gian mẫu

- 48 nhịp nội dung, 8 chương, khoảng 13 phút 41 giây theo kịch bản nền; giọng đọc TTS có thể thay đổi thời lượng.
- `episodes/comb03_tree_sample_space.py` – Scene `COMB03`.
- `.github/workflows/render-comb03-v2.yml` – tự cài Manim, Typst, Noto Fonts, làm TTS nếu bật, render và kiểm tra MP4.
- `comb03_beats.json` và `comb03_lesson_data.py` – nguồn duy nhất cho hoạt hình, lời giảng và kiểm thử.
- `HUONG_DAN_RENDER_COMB03_V2.md` – hướng dẫn thao tác chi tiết.

Các video COMB01 V2, COMB02 V2 và GEO01 vẫn được giữ nguyên trong gói. COMB03 chưa được render và nghiệm thu thực tế trong môi trường tạo mã nguồn.
---

## COMB04 V2 — Khi nào thứ tự quan trọng? (MỚI)

Tập này có 48 nhịp, 8 chương, 2.497 từ lời giảng và thời lượng nền **14:10**. Mã Scene: `episodes/comb04_order_matters.py` / `COMB04`. Workflow mới: `.github/workflows/render-comb04-v2.yml`. Gói giữ nguyên toàn bộ mã COMB01 V2, COMB02 V2, COMB03 V2, GEO01. Xem **`HUONG_DAN_RENDER_COMB04_V2.md`** để render.

Kết quả toán trọng tâm: 4×3=12 phân công; 12÷2=6 nhóm; 5×4×3=60 dãy, 60÷3!=10 nhóm; 6×5=30 phân công và 15 nhóm; chọn đội có trưởng từ 8 học sinh bằng 8×21=56×3=168. Bài 04 chưa dùng ký hiệu A/C để học sinh tiếp cận bản chất trước khi học công thức. Khi dùng từ tập sau, n ở trên k ở dưới theo ví dụ người dùng.

**Chú ý nghiệm thu:** Gói hiện là mã nguồn đã kiểm thử Python, chưa render được MP4 bằng Manim/Typst trong môi trường đóng gói. Hãy chạy workflow ở chế độ preview trước.


## COMB05 V2 — Hoán vị (mới)

- Video 05: 8 chương / 48 nhịp, tối thiểu ~14:58, có tùy chọn giọng đọc tiếng Việt.
- Scene: `episodes/comb05_permutations.py`, class `COMB05`.
- Script: `scripts/prepare_comb05_v2.py`; QA: `scripts/qa_comb05_v2.py`.
- GitHub Actions: `.github/workflows/render-comb05-v2.yml`.
- Hướng dẫn: `HUONG_DAN_RENDER_COMB05_V2.md`.
- Storyboard: `preview/comb05_v2/storyboard_8_chapters.png`.
- Nội dung: hoán vị `P_n=n!`, 24 hoán vị bốn phần tử, khối AB (48), A/B không kề (72) theo hai cách, A trước B (60), bài ràng buộc nâng cao.
- Sau khi chạy Actions, phải duyệt video MP4 và ảnh QA bằng mắt; kiểm thử Python không thay cho render.

---

## COMB06 V2 — CHỈNH HỢP (MỚI)

Đã bổ sung `episodes/comb06_arrangements.py` / Scene `COMB06`, **48 nhịp trong 8 chương**, 2.944 từ thuyết minh và thời lượng nền 15 phút 22,7 giây. Bài giảng đi từ 6 học sinh nhận ba giải khác nhau, giải thích chỉnh hợp và công thức `A^(n)_(k)`, đến bài toán chức vụ có ràng buộc, lập số không lặp và phân biệt hoán vị–chỉnh hợp–tổ hợp.

**Render:** vào GitHub → Actions → **Render COMB06 V2 - Bai giang day du Manim Typst**. Xem `HUONG_DAN_RENDER_COMB06_V2.md`. Bản này kế thừa COMB01–COMB05 V2 và GEO01, không thay thế workflow các tập cũ.

**Trạng thái:** kiểm thử toán học và cấu trúc Python đã chạy. Storyboard chỉ là ảnh mô phỏng. Cần GitHub Actions render Manim, sau đó duyệt tiếng và hình trước khi công bố.
