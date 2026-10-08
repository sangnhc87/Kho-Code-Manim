# SANG MATH — Đại số tổ hợp (Manim–Typst)

**Mùa 1 — Tập 01: QUY TẮC CỘNG (`COMB01`)**

Gói mã nguồn gồm một tập phim Manim trọn tuyến nội dung, các công thức Typst biên dịch trước thành PNG trong suốt, bộ kiểm thử toán, kịch bản thuyết minh và workflow GitHub Actions. Hình minh họa bên trái, đề bài/lập luận bên phải, Full HD 1920 × 1080, 30 fps.

> Hiện trạng: mã nguồn đã qua kiểm tra cú pháp Python và kiểm thử toán tại nơi tạo; **chưa render Manim/Typst trực tiếp tại đây** vì môi trường thiếu hai chương trình và không thể tải package. Chạy workflow GitHub Actions để thực sự render và kiểm chứng bố cục.

## Ký hiệu chỉ số rất quan trọng

- Mặc định theo **ví dụ thầy đưa** `C^(n)_(k)`, tức \(C_k^n\), với *n trên, k dưới*, và `A^(n)_(k)` cho chỉnh hợp. Trong series, chúng được *định nghĩa* lần lượt là số tổ hợp/chỉnh hợp chập k của n phần tử.
- Tuy nhiên, **SGK Toán 10 phổ biến dùng** \(C_n^k, A_n^k\) (*n dưới, k trên*). Do hai kiểu ký hiệu trái ngược, cấu hình có thể chuyển ngay mà không sửa từng cảnh:

```bash
COMB_NOTATION=sgk python scripts/build_formulas.py
```

Hoặc trên GitHub Actions chọn `notation: sgk`/`user`. Tập 01 chưa cần công thức chỉnh hợp/tổ hợp; hai quy ước đều được chuẩn bị cho tập 06–08. Nên chốt một quy ước trước khi sản xuất các tập này để tránh nhầm lẫn trong tài liệu giảng dạy.

## Cấu trúc

```text
series_config.py               # Màu sắc, quy ước A/C, logic toán
scripts/build_formulas.py      # Biên dịch Typst ra PNG trong suốt
assets/formulas/              # 10 công thức Typst, có cả công thức cho các tập sau
assets/rendered/              # PNG tự sinh, không cần lưu Git
episodes/comb01_rule_of_sum.py # Toàn bộ Scene COMB01
narration_COMB01.md            # Kịch bản lời giảng và nhịp dựng
storyboard_COMB01.md           # Shot list / checklist kiểm duyệt
tests/test_math.py             # Kiểm chứng độc lập bằng liệt kê
.github/workflows/render-comb01.yml
```

## Render tự động trên GitHub Actions

1. Giải nén gói vào gốc một repository GitHub.
2. Commit/push các tệp và `.github/workflows/render-comb01.yml`.
3. Vào **Actions → Render COMB01 · Manim + Typst → Run workflow**.
4. Chọn `preview` để duyệt nhanh, sau đó `fullhd` để render 1080p.
5. Khi hoàn tất, vào phần **Artifacts** của workflow để tải `COMB01-...` chứa MP4. GitHub xóa artifact theo thời hạn lưu trữ nếu không tải về; bản mã nguồn trong repository được giữ nguyên.

**Lưu ý:** workflow chưa được chạy thực tế trong môi trường này, nên cần xem log của lần chạy đầu để hiệu chỉnh cài đặt nếu API Manim/Typst thay đổi.

## Render cục bộ (Mac/Windows/Linux sau khi cài Manim và Typst)

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/build_formulas.py
manim -pql episodes/comb01_rule_of_sum.py COMB01
manim -qh -r 1920,1080 --fps 30 episodes/comb01_rule_of_sum.py COMB01
```

Công thức Typst được biên dịch thành PNG trong suốt và được Manim dùng như đối tượng đồ họa. Kịch bản hiện **chưa có bản thu giọng đọc/TTS**, do vậy thời lượng Manim không đồng nhất với các mốc mục tiêu của lời dẫn. Khi có file giọng đọc, phải căn nhịp animation theo lời, xem trước và duyệt cảnh rồi mới phát hành bản cuối.

## Nội dung tập 01

1. Tình huống 2 tuyến xe + 3 tuyến tàu → 5 cách.
2. Tách các lựa chọn vào hai nhóm rời nhau.
3. Phát biểu quy tắc cộng \(m+n\).
4. Ví dụ 4 sách Toán + 3 sách Vật lí → 7 cách.
5. Phản ví dụ: số từ 1 đến 12 chia hết cho 2 **hoặc** 3 → \(6+4-2=8\), vì 6 và 12 bị đếm trùng.
6. Kiểm tra: 5 lựa chọn nhóm A + 2 lựa chọn nhóm B không trùng → 7 cách.

## Điểm cần kiểm soát trước khi công bố

- Các chữ tiếng Việt không bị tràn khung phải; không đè lên đường đi hay ô minh họa.
- Kết quả từng bài toán đúng với bộ kiểm thử.
- Từng đối tượng màu đỏ chính là trường hợp trùng cần trừ.
- Công thức Typst đã được render, không phải fallback Text.
- Có giọng thuyết minh và duyệt video hoàn chỉnh trước khi sử dụng trong lớp.
