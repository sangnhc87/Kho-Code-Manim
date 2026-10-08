# COMB06 V2 — CHỈNH HỢP · HƯỚNG DẪN RENDER GITHUB ACTIONS

## Dự án dùng để làm gì?

Video **COMB06** là một bài giảng riêng trong Series Đại số tổ hợp SangMath. Dự án này kế thừa đầy đủ COMB01–COMB05 V2 và GEO01. COMB06 dùng Manim cho hình động, Typst cho công thức và lời đọc tiếng Việt nếu bật dịch vụ TTS.

- **48 nhịp**, chia 8 chương; lời giảng 2.944 từ.
- **Thời lượng nền dự kiến 922,7 giây = 15 phút 22,7 giây**, gồm đoạn kết 5,2 giây, nếu không có TTS. Khi bật TTS thời lượng lấy theo âm thanh thực tế, có thể dài hơn.
- **Ký hiệu theo yêu cầu của thầy:** `A^(n)_(k)` / `C^(n)_(k)`: n ở trên, k ở dưới (cấu hình `COMB_NOTATION=user`).
- **Scene:** `COMB06`, tệp `episodes/comb06_arrangements.py`.
- **Workflow:** `.github/workflows/render-comb06-v2.yml`.

## Đưa lên GitHub

1. Giải nén file ZIP được gửi kèm. **Không đưa nguyên file ZIP** vào repository.
2. Sao chép **toàn bộ các tệp và thư mục bên trong ZIP** vào gốc repository hiện có. Chú ý cả thư mục ẩn `.github`.
3. Commit, push thay đổi. Kiểm tra có tệp `.github/workflows/render-comb06-v2.yml` trên GitHub.
4. Mở tab **Actions → Render COMB06 V2 - Bai giang day du Manim Typst → Run workflow**.
5. Lần đầu chọn `quality = preview`, `voice = off` để chỉ thử hình, tránh lỗi mạng TTS. Sau đó nên render `voice = on` để kiểm tra phần thuyết minh.
6. Khi QA đạt, mở workflow run → **Artifacts** → tải `COMB06-V2-preview-voice-off` hoặc `...voice-on`.
7. Cuối cùng chạy `quality = fullhd`, `voice = on` để nhận video 1920×1080, 30fps.

**Nếu bật `voice=on`:** workflow kết nối dịch vụ Edge TTS (`vi-VN-NamMinhNeural`). Nếu bị giới hạn hoặc chặn, bước chuẩn bị giọng đọc sẽ báo lỗi rõ ràng; hãy chọn `voice=off` để kiểm tra hình trước, hoặc chỉnh workflow dùng nguồn TTS của thầy. Chế độ off vẫn giữ thời lượng cơ bản nhưng không có âm thanh.

## Kiểm tra toán học

```bash
python -m unittest discover -s tests -v
```

Các phép đếm chủ chốt được kiểm tra bằng chương trình liệt kê:

| Bài toán | Kết quả |
|---|---:|
| Trao 3 giải khác nhau trong 6 người | 6 × 5 × 4 = 120 |
| 7 người phân công ba chức vụ, A không làm trưởng | 6 × 6 × 5 = 180 |
| Đếm phần bù ở bài trên | 210 − 30 = 180 |
| A phải được phân công nhưng không được làm trưởng | 2 × 6 × 5 = 60 |
| Lập số 3 chữ số khác nhau từ 0,1,2,3,4 | 4 × 4 × 3 = 48 |
| Lập số chẵn 3 chữ số khác nhau từ tập trên | 12 + 18 = 30 |

## Render thủ công trên máy Linux có Manim/Typst

```bash
python -m pip install -r requirements.txt
python scripts/prepare_comb06_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb06_arrangements.py COMB06
# hoặc chuẩn 1080p
manim -qh -r 1920,1080 --fps 30 episodes/comb06_arrangements.py COMB06
```

Sau khi render, chạy:

```bash
python scripts/qa_comb06_v2.py --video media/videos/comb06_arrangements/480p24/COMB06.mp4 --voice off
```

Đường dẫn output có thể khác tùy phiên bản Manim. Workflow GitHub tự tìm đúng `COMB06.mp4` bằng lệnh `find`.

## Nghiệm thu chất lượng

Sau khi render, workflow kiểm tra định dạng MP4, 854×480 hoặc 1920×1080, đủ **ít nhất 900 giây**, có audio nếu `voice=on`, khớp thời lượng trong `voice/comb06_voice_manifest.json`, rồi xuất 8 khung hình chương và `qa_comb06_v2/contact_sheet.jpg`.

Ngoài kiểm tra tự động, cần **xem video thật** để kiểm tra tiếng Việt không bị cắt, kí hiệu chỉ số đúng vị trí, font không vỡ, mô hình minh họa khớp lời đọc, không tràn khung và các chuyển cảnh không đơn điệu. Các kiểm thử Python **không thay thế việc render và duyệt hình Manim**.

## Tệp quan trọng

- `comb06_beats.json`: nguồn kịch bản 48 nhịp.
- `comb06_lesson_data.py`: công thức, phép liệt kê kiểm tra, cấu trúc bài giảng.
- `episodes/comb06_arrangements.py`: scene Manim.
- `scripts/prepare_comb06_v2.py`: Typst, MP3, SRT, manifest.
- `scripts/qa_comb06_v2.py`: kiểm tra video và trích khung hình.
- `narration_COMB06_v2.md`: lời giảng theo mốc thời gian.
- `subtitles_COMB06_v2.srt`: phụ đề đồng bộ nhịp.
- `preview/comb06_v2/storyboard_8_chapters.png`: storyboard tĩnh, không phải ảnh render Manim.

## Trạng thái bàn giao

Đã chạy kiểm thử nội dung/toán/Python và chuẩn bị storyboard tĩnh. Môi trường đóng gói không có Manim/Typst, **chưa chạy render video Manim thật**. Cần duyệt bản preview từ GitHub Actions trước khi xuất bản.
