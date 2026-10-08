# HƯỚNG DẪN RENDER COMB02 V2 BẰNG GITHUB ACTIONS

## 1. Đưa gói ZIP lên repository

1. Tải `SangMath_COMB02_V2_GitHubReady.zip` và giải nén.
2. Chép **toàn bộ nội dung BÊN TRONG thư mục** vừa giải nén vào **gốc repository đang chứa COMB01 V2**. Giữ nguyên `.github/workflows/`.
3. Commit và push toàn bộ thay đổi. Không chỉ upload tệp ZIP, vì GitHub không tự mở ZIP.
4. Phần mới nhất của COMB02 là `episodes/comb02_rule_of_product.py`; mã COMB01 V2 và GEO01 vẫn giữ nguyên.

## 2. Render thử

1. Vào trang repository GitHub → **Actions**.
2. Chọn **Render COMB02 V2 - Bai giang day du Manim Typst**.
3. Bấm **Run workflow** → chọn `quality=preview` và `voice=on` → Run workflow.
4. Nếu dịch vụ TTS không truy cập được, chạy lại `voice=off` để kiểm tra hình. Video này sẽ không có tiếng đọc.
5. Khi workflow xong, mở trang run → **Artifacts** → tải gói `COMB02-V2-preview-voice-on`.
6. Mở `COMB02.mp4`, xem `qa_comb02_v2/contact_sheet.jpg` và `qa_comb02_v2/report.json`. Kịch bản và phụ đề SRT cũng có trong Artifacts.
7. Khi video preview đạt chất lượng → chạy lại `quality=fullhd` (1920×1080/30fps).

## 3. Lỗi thường gặp

- **Typst failed:** mở log `Compile Typst...` để xem công thức bị lỗi. Thử chạy lại workflow, gửi log và tên công thức nếu vẫn lỗi.
- **Edge TTS error:** giọng đọc trực tuyến có thể không hoạt động tạm thời. Chọn `voice=off` để phân biệt lỗi hình và lỗi TTS.
- **Video too short:** workflow có kiểm tra thời lượng tối thiểu 750 giây. Không tắt cảnh báo; lấy log Scene/MP4 để sửa code.
- **Audio stream missing:** với `voice=on`, workflow sẽ báo lỗi. MP4 phải có tiếng thật, không chấp nhận kịch bản chỉ lưu thành Markdown.
- **Khung hình lỗi:** tải `qa_comb02_v2/contact_sheet.jpg` và/hoặc MP4 để kiểm tra, sửa và chạy lại preview.

## 4. Cách chạy nếu có môi trường Linux với đủ phụ thuộc

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/prepare_comb02_v2.py --voice on
manim -ql -r 854,480 --fps 24 episodes/comb02_rule_of_product.py COMB02
# full HD:
manim -qh -r 1920,1080 --fps 30 episodes/comb02_rule_of_product.py COMB02
```

**Lưu ý:** Tại thời điểm bàn giao, đã kiểm tra Python và toán học, chưa thể kiểm tra MP4 Manim thật trong môi trường soạn mã. Không coi ảnh storyboard tĩnh là bằng chứng render thành công.
