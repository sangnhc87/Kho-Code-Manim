# HƯỚNG DẪN RENDER COMB21 V2 — HÀM SINH

## 1. Sử dụng đúng ZIP

Giải nén `SangMath_COMB21_V2_GitHubReady.zip` rồi **chép toàn bộ nội dung** (kể cả thư mục ẩn `.github`) vào gốc repository cũ đang có COMB01–20. Không nộp nguyên tệp ZIP lên repository. Commit và push các tệp mới.

Gói kế thừa mã các tập 01–20 và GEO01. Nó bổ sung COMB21, không yêu cầu tạo repository mới.

## 2. Chạy GitHub Actions

Vào tab **Actions** → chọn **Render COMB21 V2 - Ham sinh - Generating Functions** → **Run workflow**.

- Lượt đầu chọn `quality=preview`, `voice=off`: 854×480, 24fps, kiểm tra hình động và công thức.
- Duyệt hình xong chọn `quality=preview`, `voice=on`: dịch vụ edge-tts cần truy cập Internet từ runner. Có thể thất bại nếu dịch vụ tạm gián đoạn.
- Khi đủ tốt chọn `quality=fullhd`, `voice=on` để xuất 1920×1080, 30fps.

Tải MP4, báo cáo JSON và ảnh chụp tám chương từ **Artifacts**. Workflow tự kiểm tra thời lượng, độ phân giải và luồng tiếng nếu bật TTS. Hãy xem kỹ khung hình, ký hiệu và thuyết minh; qua unit tests không có nghĩa là render thành công.

## 3. Các tệp quan trọng

| Tệp | Công dụng |
|---|---|
| `episodes/comb21_generating_functions.py` | Scene `COMB21` với tám mô hình động |
| `comb21_lesson_data.py`, `comb21_beats.json` | Logic toán học và 48 nhịp giảng |
| `comb21_formulas.json`, `assets/comb21v2/*.typ` | Công thức Typst, giữ quy ước `C^(n)_(k)` (n phía trên) |
| `scripts/prepare_comb21_v2.py` | Typst PNG, TTS và thời gian phụ đề |
| `scripts/qa_comb21_v2.py` | Kiểm tra MP4 và trích ảnh từng chương |
| `tests/test_comb21_generating_functions.py` | Các kiểm chứng toán độc lập |
| `narration_COMB21_v2.md`, `subtitles_COMB21_v2.srt` | Lời giảng tiếng Việt và phụ đề |
| `.github/workflows/render-comb21-v2.yml` | Render tự động |

## 4. Chạy thủ công nếu máy có đầy đủ môi trường

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/prepare_comb21_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb21_generating_functions.py COMB21
```

Bản xuất Full HD:

```bash
manim -qh -r 1920,1080 --fps 30 episodes/comb21_generating_functions.py COMB21
```

## 5. Thời lượng và các lưu ý

Thời lượng nền dự kiến **21 phút 41 giây**: 48 nhịp × 27 giây cộng phần kết. Bản có TTS căn theo thời lượng giọng đọc thực tế và có thể dài hơn. Đây không phải thời lượng đã đo từ MP4.

**Hình ảnh trong `preview/` là storyboard tham khảo, không phải hình render thực tế từ Manim.** Biên dịch Typst, cấu trúc chuyển cảnh Manim, giọng đọc và ảnh kiểm tra thực tế cần nghiệm thu qua GitHub Actions.

## 6. Những lỗi cần gửi lại để sửa

Nếu Actions báo đỏ, gửi tên bước lỗi và khoảng 40 dòng cuối log, đặc biệt là lỗi `typst compile`, `manim`, `edge_tts`, `qa_comb21_v2`. Nếu render được nhưng có chữ tràn, gửi ảnh QA hoặc MP4. Không tự sửa công thức chỉ để vượt quá trình biên dịch.
