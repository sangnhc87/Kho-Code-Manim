# Hướng dẫn COMB14 V2 — Phương pháp đếm phần bù

**Tệp Manim:** `episodes/comb14_complement.py`  
**Scene:** `COMB14`  
**Workflow:** `.github/workflows/render-comb14-v2.yml`  
**Dự án:** giữ nguyên COMB01–COMB13 và GEO01.

## Chạy trên GitHub Actions

1. Giải nén ZIP, chép **toàn bộ nội dung bên trong** vào thư mục gốc repository hiện có. Không upload nguyên ZIP; chú ý giữ thư mục ẩn `.github`.
2. `git add .`, commit và push lên GitHub.
3. Vào **Actions → Render COMB14 V2 - Phuong phap dem phan bu → Run workflow**.
4. Lần đầu chọn `quality=preview`, `voice=off` để kiểm tra hình và công thức. Chờ hoàn tất, tải `COMB14-V2-preview-voice-off` ở **Artifacts**.
5. Xem `qa_comb14_v2/contact_sheet.jpg` và MP4. Kiểm tra chữ, màu, trạng thái được chọn/bị loại, thời lượng và tính khớp của kết luận.
6. Nếu hình ổn, chạy `quality=preview`, `voice=on` để kiểm tra tiếng đọc. Edge TTS dùng kết nối mạng; nếu TTS không thể kết nối, workflow **báo lỗi**, không coi video câm là bản hoàn thiện.
7. Sau khi duyệt hình và tiếng, chạy `quality=fullhd`, `voice=on`: 1920×1080, 30 fps.

## Các lệnh tương đương chạy trên máy đã cài Manim/Typst

```bash
python -m unittest discover -s tests -v
python scripts/prepare_comb14_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb14_complement.py COMB14
```

Nếu muốn tiếng đọc, sử dụng `--voice on` ở lệnh chuẩn bị. Tốc độ lời đọc được tính bằng **thời lượng MP3 thực tế** trong manifest, không được cắt ngắn lời giảng để khớp video.

## Kiểm tra chất lượng

- 8 chương × 6 nhịp = 48 nhịp; thời lượng nền theo mã là 18 phút 33,6 giây + kết đoạn. Khi bật TTS có thể dài hơn.
- Công thức ở `assets/comb14v2/` phải được Typst biên dịch thành PNG trước render.
- `scripts/qa_comb14_v2.py` dùng ffprobe kiểm tra độ phân giải, độ dài, audio nếu bật TTS và trích 8 ảnh QA.
- Xác nhận trước khi xuất bản: đọc chính xác cụm từ **ít nhất một / đúng một / không có**, và tính đúng miền bị loại.
- Công thức chỉnh hợp, tổ hợp theo quy ước Series: **n ở chỉ số trên, k ở chỉ số dưới** (ví dụ `C^(9)_(3)`).

## Các kết quả dùng để đối chiếu

- Dãy độ dài 4 trên `{A,B,C}` có ít nhất một A: **65**.
- Chọn đội 3 người từ 5 nam, 4 nữ, có ít nhất 1 nữ: **74**.
- Sáu người xếp hàng, A không đứng đầu và AB không kề: **384**.
- PIN bốn chữ số có ít nhất một chữ số lặp: **4.960** (cho phép 0 ở đầu).
- Bốn thư vào bốn phong bì, không lá nào đúng: **9**.
- Dãy nhị phân dài sáu chứa ít nhất một cặp `11`: **43**.
- Chọn ba trong tám người, có A hoặc B: **36**.
- Chọn đội bốn trong tám, đội phải có A/B và trưởng không là A: **185**.

**Trạng thái phát hành:** Đã kiểm thử toán học và cú pháp Python. Chưa render Manim thực tế trong môi trường tạo mã; cần chạy GitHub Actions và duyệt MP4.
