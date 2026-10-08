# SANG MATH · COMB25 V2 – BỘ 25 VIDEO ĐẠI SỐ TỔ HỢP

**Trạng thái:** Đã tạo bộ mã nguồn 25 tập và tệp GEO01; mã COMB25 qua kiểm thử Python độc lập.
**Chưa nghiệm thu:** Công thức Typst và MP4 Manim thật của tập 25 cần render trên GitHub Actions. Không xem việc kiểm thử Python là chứng nhận chất lượng hình ảnh.

## Tập 25 – Những công thức tổ hợp HAY – LẠ – KHÓ

- 8 chương × 6 nhịp = 48 nhịp.
- Thuyết minh tiếng Việt: 3,538 từ; phụ đề được tạo từ chính kịch bản.
- Thời lượng nền (voice off): 24:53, không phải thời lượng MP4 đã đo.
- Mã Scene: `episodes/comb25_olympiad_finale.py`, Scene `COMB25`.
- Kịch bản: `comb25_lesson_data.py`, `narration_COMB25_v2.md`.
- Biên dịch Typst / tạo tiếng: `scripts/prepare_comb25_v2.py`.
- Kiểm tra MP4 / trích 8 ảnh: `scripts/qa_comb25_v2.py`.
- Workflow: `.github/workflows/render-comb25-v2.yml`.

### Nội dung
1. 01 · VÒNG HẠT VÀ BỔ ĐỀ BURNSIDE
2. 02 · THÊM ĐỐI XỨNG GƯƠNG: NHÓM DIHEDRAL
3. 03 · CỐ ĐỊNH SỐ HẠT MỖI MÀU
4. 04 · ĐỊNH LÝ PÓLYA VÀ ĐA THỨC CHU TRÌNH
5. 05 · BỘ LỌC CĂN ĐƠN VỊ
6. 06 · PÓLYA CÓ RÀNG BUỘC MÀU
7. 07 · NHẬN DIỆN CÔNG CỤ CHO BÀI CỰC KHÓ
8. 08 · OLYMPIC: TÔ MÀU SÁU MẶT LẬP PHƯƠNG

### Các phép đếm đã kiểm chứng độc lập

| Mô hình | Chỉ quay | Quay + gương |
|---|---:|---:|
| 6 hạt, hai màu | 14 | 13 |
| 6 hạt, đúng ba hạt đen | 4 | – |
| 4 đỉnh hình vuông, ba màu | 24 | 21 |
| 8 hạt, đúng bốn hạt đen | 10 | 8 |

Bộ lọc căn đơn vị: `C_0^9+C_3^9+C_6^9+C_9^9=170`.

Kết thúc: tô sáu mặt lập phương bằng ba màu, chỉ xét 24 phép quay cứng, có **57 quỹ đạo**. Không tự động đồng nhất các ảnh gương.

## Chạy thử

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/prepare_comb25_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb25_olympiad_finale.py COMB25
VIDEO=$(find media/videos -type f -name 'COMB25.mp4' | head -n 1)
python scripts/qa_comb25_v2.py --video "$VIDEO" --voice off
```

Phải cài Manim, Typst, FFmpeg và font Noto Sans/Noto Serif. GitHub Actions có bước tự cài dependencies.

Workflow GitHub: **Actions → Render COMB25 V2 - Olympiad Finale - Burnside - Polya → Run workflow**.
Nên kiểm tra `preview / voice off`, tiếp `voice on`, cuối cùng `fullhd`.

## Danh mục Series

- COMB01 Quy tắc cộng
- COMB02 Quy tắc nhân
- COMB03 Sơ đồ cây và không gian mẫu
- COMB04 Thứ tự có quan trọng?
- COMB05 Hoán vị
- COMB06 Chỉnh hợp
- COMB07 Tổ hợp
- COMB08 Tổng hợp phương pháp đếm
- COMB09 Chọn có lặp và lập dãy
- COMB10 Hoán vị phần tử giống nhau
- COMB11 Hoán vị vòng tròn
- COMB12 Phương pháp gộp khối
- COMB13 Các phần tử không đứng cạnh nhau
- COMB14 Phương pháp đếm phần bù
- COMB15 Lập số theo điều kiện chữ số
- COMB16 Chia nhóm và phân công vai trò
- COMB17 Nhị thức Newton
- COMB18 Tam giác Pascal
- COMB19 Tập con và 2^n
- COMB20 Tổng hệ số nhị thức
- COMB21 Hàm sinh
- COMB22 Quy hoạch động
- COMB23 Bao hàm–loại trừ và đa thức xe
- COMB24 Catalan, Dyck, nguyên lý phản xạ
- COMB25 Burnside, Pólya, bộ lọc căn đơn vị và lập phương

---

**Quy ước ký hiệu theo yêu cầu:** tổ hợp `C_k^n` và chỉnh hợp `A_k^n`, nghĩa là n ở trên, k ở dưới. Typst chịu trách nhiệm hiển thị công thức (không dùng cách ảnh hóa toàn bộ khung hình).
**Nghiệm thu trước khi dạy:** xem các ảnh QA, phụ đề, thuyết minh, thời lượng và các bước hình học/đối xứng của khối lập phương. Những hình trước khi render trong `preview/comb25_v2/` chỉ là phác thảo.
