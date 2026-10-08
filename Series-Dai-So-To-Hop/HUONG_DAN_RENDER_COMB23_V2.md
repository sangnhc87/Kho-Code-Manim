# COMB23 V2 — HƯỚNG DẪN RENDER GITHUB ACTIONS

## Video 23: Bao hàm–loại trừ nâng cao, hoán vị không điểm cố định và đa thức xe

Tập học gồm **8 chương, 48 nhịp**, **3.992 từ lời giảng tiếng Việt**; thời lượng nền **22 phút 29 giây**, bản bật giọng đọc có thể khác vì từng nhịp được căn theo tệp MP3 thực tế. Đây là mã sẵn sàng **chạy thử render**, chưa có MP4 Manim được kiểm tra hình và tiếng ở môi trường phát triển.

### Bước 1 — Cập nhật repository cũ

1. Giải nén `SangMath_COMB23_V2_GitHubReady.zip`.
2. Đưa **toàn bộ nội dung bên trong** thư mục giải nén vào thư mục gốc của repository GitHub đang chứa COMB01–COMB22. **Không đẩy nguyên tệp ZIP lên repo**.
3. Giữ nguyên tên và vị trí thư mục ẩn `.github/workflows/`.
4. Commit rồi push lên nhánh mặc định của repository.

### Bước 2 — Chạy thử không có giọng đọc

Trên GitHub mở **Actions → Render COMB23 V2 - Bao ham loai tru - Da thuc xe → Run workflow**.

- `quality = preview`
- `voice = off`

Pipeline sẽ: cài Manim và Typst → chạy tất cả unit tests → biên dịch **48 công thức Typst** thành PNG → chuẩn bị lời dẫn và SRT → render Scene `COMB23` ở 854×480, 24 fps → kiểm tra MP4 và trích tám khung hình chương.

Khi chạy xong, tải **Artifacts → COMB23-V2-preview-voice-off**. Xem tệp MP4 cùng `qa_comb23_v2/contact_sheet.jpg` và `qa_comb23_v2/report.json`.

### Bước 3 — Giọng đọc và Full HD

- Chạy `preview, voice = on` để kiểm tra giọng đọc tiếng Việt. Chức năng TTS sử dụng dịch vụ `edge-tts` ngoài GitHub và cần kết nối mạng tại thời điểm chạy.
- Sau khi duyệt, chạy `fullhd, voice = on` (hoặc `off`) để render 1920×1080, 30 fps.
- Nếu TTS không kết nối, có thể render `voice=off` và giữ lời giảng `.md` / phụ đề `.srt` để xử lý âm thanh riêng.

### Tệp mới của COMB23

| Tệp | Vai trò |
|---|---|
| `episodes/comb23_inclusion_rook.py` | Scene Manim `COMB23` |
| `comb23_lesson_data.py` | Kịch bản 48 nhịp và các mô hình đếm toán học |
| `comb23_formulas.json` | Danh mục công thức Typst |
| `scripts/prepare_comb23_v2.py` | Công thức Typst PNG, lời đọc, phụ đề và manifest thời gian |
| `scripts/qa_comb23_v2.py` | QA sau render: thời lượng, độ phân giải, giọng đọc và khung chương |
| `tests/test_comb23_inclusion_rook.py` | Kiểm chứng bằng brute force, DP, công thức |
| `.github/workflows/render-comb23-v2.yml` | Workflow mới; không thay thế workflow của tập cũ |
| `preview/comb23_v2/` | Tám ảnh storyboard để tham chiếu, **không phải ảnh Manim** |
| `narration_COMB23_v2.md`, `subtitles_COMB23_v2.srt` | Lời giảng, phụ đề |

### Kiểm tra cục bộ (chỉ khi máy đã cài dependencies)

```bash
python -m unittest discover -s tests -v
python scripts/prepare_comb23_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb23_inclusion_rook.py COMB23
python scripts/qa_comb23_v2.py --video media/videos/comb23_inclusion_rook/480p24/COMB23.mp4 --voice off
```

Đường dẫn MP4 có thể khác tùy bản Manim; workflow tự dò tệp video.

### Kết quả toán học và các giới hạn nghiệm thu

- `D_4=9`, `D_5=44`, `D_6=265`.
- 6 người, chỉ 3 vị trí đầu bị cấm cố định: **426** cách.
- Bàn cấm 4×4 có hệ số xe `[1,5,8,5,1]`: **6** cách phân công hợp lệ.
- Bài vòng ghế **có đánh số** 5×5, cấm ghế cùng số và ghế tiếp theo: hệ số `[1,10,35,50,25,2]`, kết quả **13**.

**Lưu ý:** kiểm thử Python và toán học không thay thế cho biên dịch công thức Typst và nghiệm thu MP4 trong GitHub Actions. Nếu Action báo lỗi, gửi log hoặc MP4 để sửa đúng cảnh. Trước khi công bố, cần xem đặc biệt ảnh kiểm tra ô cấm, cách hiện công thức và thời điểm phát lời đọc.
