# HƯỚNG DẪN RENDER COMB09 V2 – CHỌN CÓ LẶP

## Một gói ZIP cho cả COMB01–COMB09 và GEO01

1. Giải nén ZIP, **chép nội dung thư mục vào gốc repository GitHub**, không đưa nguyên ZIP vào repository. Đảm bảo có `.github/workflows/render-comb09-v2.yml`.
2. Commit và push vào nhánh mặc định (thường là `main`).
3. Trong GitHub → **Actions** → **Render COMB09 V2 - Chon co lap va lap day n mu k** → **Run workflow**.
4. Chọn `quality=preview`, `voice=off` để kiểm tra hình trước. Khi hình ổn, chạy lại `voice=on` để nghe thuyết minh tiếng Việt. Cuối cùng chọn `quality=fullhd`.
5. Tại mục **Artifacts** của run, tải MP4, phụ đề `.srt`, bảng ảnh chụp 8 chương, và `report.json`.

## Nội dung kiểm chứng

- 8 chương × 6 nhịp = 48 nhịp.
- Không có giọng: thời lượng thiết kế ~16:29, âm thanh bật có thể lâu hơn.
- Đếm dãy từ A/B/C: 2 vị trí có 9, 3 vị trí có 27.
- Mã PIN 4 chữ số cho phép lặp: 10000, có thể bắt đầu bằng 0.
- Chuỗi 4 chữ số không lặp: 5040; số có 4 chữ số khác nhau: 4536.
- Chọn ba thẻ từ ba loại A/B/C, có lặp nhưng không xét thứ tự: 10 nhóm (không phải 27).
- Dãy 4 từ A/B/C: có ít nhất một A = 65; đúng hai A = 24; không có AA = 60.

**Ký hiệu yêu cầu:** `C^(n)_(k)` đặt n ở trên, k ở dưới. Trong các ví dụ dùng `C^(4)_(2)` và `C^(5)_(3)`.

## Chạy ngoài GitHub (nếu có Manim và Typst)

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/prepare_comb09_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb09_repetition.py COMB09
```

Để bật lời đọc (cần mạng Internet đến dịch vụ TTS):

```bash
python scripts/prepare_comb09_v2.py --voice on
manim -qh -r 1920,1080 --fps 30 episodes/comb09_repetition.py COMB09
```

## Lưu ý nghiệm thu

Bộ test Python chỉ chứng minh các phép đếm, cấu trúc chương và mã biên dịch Python không có lỗi cú pháp. **Không thay thế việc kiểm tra render Manim–Typst thực tế.** Nếu workflow thất bại, tải log của step lỗi và gửi lại để sửa chính xác. Sau render thầy nên xem kỹ các nhịp có công thức, tốc độ lời nói, nhãn tiếng Việt và độ rõ của 81 chấm trong cảnh phần bù.
