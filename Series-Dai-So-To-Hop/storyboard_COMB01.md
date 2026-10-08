# STORYBOARD / SHOT LIST — COMB01 — QUY TẮC CỘNG

**Cấu trúc hình:** 16:9 · nền navy · khung trái 45% mô hình · khung phải 55% đề bài/lời giải; không xếp chữ lên vật thể.  
**Định dạng cuối:** MP4, H.264, 1920 × 1080, 30 fps.  
**Phụ đề:** soạn sau khi có file giọng đọc, tuyệt đối không để phụ đề chồng vùng công thức.

| Mốc mục tiêu | Cảnh bên trái | Cảnh bên phải | Hoạt hình toán bắt buộc | Kiểm tra |
|---|---|---|---|---|
| 00:00–00:50 | A, B, 2 đường cyan, 3 đường vàng | Hiện nguyên bài toán | Di chuyển điểm đánh dấu theo mỗi tuyến | Có đúng 5 tuyến, không thiếu đường |
| 00:50–02:20 | Thay hình đường bằng 5 lựa chọn | Gạch đầu dòng đếm 2 xe + 3 tàu | Tô sáng lần lượt từng nhóm | Mỗi tuyến được tính một lần |
| 02:20–04:15 | Hai nhóm được khoanh riêng | Phép cộng 2 + 3 = 5 (Typst) | Gom nhóm có ý nghĩa | Không biến phép đếm thành phép nhân |
| 04:15–06:00 | Hai ô phương án A, B | Quy tắc tổng quát m + n | Nhấn mạnh A và B không trùng | Không được thiếu điều kiện rời nhau |
| 06:00–07:45 | Giá sách: 4 Toán, 3 Vật lí | 4 + 3 = 7 (Typst) | Xếp 7 quyển có mã riêng | Chọn một quyển, không chọn một cặp |
| 07:45–10:20 | Lưới 1–12 | 6 + 4 − 2 = 8 (Typst) | Chẵn cyan → bội 3 vàng → giao đỏ | 6 và 12 bị đếm hai lần |
| 10:20–11:40 | Hai nhãn “CỘNG”, “KHÔNG TRÙNG” | Câu kiểm tra 5 + 2 = 7 | Giữ thời gian để học sinh tự trả lời | Có câu hỏi → chờ → hiện đáp án |

## Quy chuẩn hiển thị công thức cho cả Series

Các công thức thực tế được tạo trong `assets/formulas/` bằng **Typst** rồi render trước ra PNG trong suốt. Điều này giảm phụ thuộc LaTeX và tránh lỗi khi Manim dựng nhiều khung hình.

- Theo ví dụ ghi của người yêu cầu: `C^(n)_(k)` và `A^(n)_(k)` tương ứng với `C_k^n`, `A_k^n` khi hiển thị kiểu TeX; `n` **ở trên**.
- Theo SGK Việt Nam thông dụng: `C_(n)^(k)` và `A_(n)^(k)` tương ứng với `C_n^k`, `A_n^k`; `n` **ở dưới**.
- Không có ký hiệu chỉnh hợp/tổ hợp ở COMB01; công thức hai quy ước đã đưa vào generator cho COMB06–08. Chỉ chọn một hệ trước khi thu lời giảng các tập này.

## Checklist trước xuất bản

- [ ] Chạy test: `python -m unittest discover -s tests -v`.
- [ ] Biên dịch 10 công thức bằng `python scripts/build_formulas.py`, không lỗi Typst.
- [ ] Render thử `manim -pql episodes/comb01_rule_of_sum.py COMB01`.
- [ ] Đối chiếu hình preview với lời dẫn; kiểm tra nhất quán chuyển động.
- [ ] Kiểm tra 7 nhóm khung hình tương ứng storyboard.
- [ ] Thu âm tiếng Việt, rồi căn thời lượng từng đoạn theo âm thanh thật.
- [ ] Chạy Full HD, kiểm tra không có chữ đè đường đi, vật thể hoặc công thức.
