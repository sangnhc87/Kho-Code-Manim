# COMB02 V2 — QUY TẮC NHÂN · BÀI GIẢNG MANIM–TYPST

**Mục tiêu:** HS nhận diện một kết quả là đường lựa chọn đủ các bước; giải thích vì sao phải nhân và khi nào không được nhân; biết đếm theo từng nhánh và bằng phần bù. Kế thừa chuẩn COMB01 V2, tuyệt đối tránh chữ đè hình.

**Nhịp học:** 44 beat / 8 chương / thời gian nền 12 phút 57,7 giây. Bật TTS tiếng Việt thì tự động căn theo clip MP3 thực tế; có thể dài hơn. Đoạn mở + kết dài thêm 5,2 giây; kịch bản không kéo dài bằng cách kéo chậm video đầu ra.

| Chương | Nhịp | Mô hình hình động | Phép đếm và kết luận cần đạt |
|---|---:|---|---|
| 01. Tình huống | 6 | Ba áo, hai quần; cố định áo rồi ghép quần | Các cặp phân biệt; 3×2=6, không phải 3+2 |
| 02. Liệt kê hệ thống | 5 | Bảng 3 hàng, 2 cột; làm sáng từng hàng | Một ô ↔ một bộ; 2+2+2=6 |
| 03. Sơ đồ cây | 6 | Gốc → áo → quần; điểm sáng lần theo đường đi | Mỗi đường trọn vẹn ↔ một bộ; 6 lá |
| 04. Tổng quát | 5 | m nhánh, sau *mỗi* nhánh có n cách; so sánh hoặc/và | N=m×n khi các số nhánh như nhau |
| 05. Ba công đoạn | 5 | Thêm hai mũ cho mỗi bộ áo–quần | 3×2×2=12; quy tắc nhiều công đoạn |
| 06. Một cặp bị cấm | 6 | Bảng 3×2, gạch đúng ô A2Q2 | 6−1=5 và 2+1+2=5 |
| 07. Số nhánh không đều | 5 | Cây mới: A1→2, A2→1, A3→3 | 2+1+3=6; tổng theo nhánh, không nhân sai |
| 08. Luyện tập | 6 | Lập số; chọn một món; 4×3 cấm hai cặp | 4×3=12; 3+2=5; 4×3−2=10 |

## Điểm đặc biệt về sư phạm

- Trước công thức, phải nêu **đối tượng được đếm**: cặp áo–quần, đường đi, bộ áo–quần–mũ hoặc số tự nhiên.
- Học sinh được nhìn thấy phép tương ứng một-một giữa đường đi / ô bảng và kết quả.
- Giải thích điều kiện quy tắc nhân **sau mỗi lựa chọn bước trước có cùng số cách ở bước tiếp theo**, không đơn giản nói các lựa chọn độc lập.
- Các ví dụ cấm chọn dùng hai phương pháp đối chiếu độc lập. Không có trường hợp bị loại sai hoặc phép đếm trùng.
- Lời giải chỉ xuất hiện sau khi đặt vấn đề, quan sát nhánh, kiểm tra kết quả.

## Cách dựng

- Cột trái: hình động Manim thuần vector (thẻ, cây, bảng); cột phải: đề bài và lập luận có các công thức Typst biên dịch sẵn.
- 16:9; Full HD 1920×1080/30fps. Preview 854×480/24fps.
- Bảng màu và font Noto Sans đồng bộ COMB01 V2.
- Các nhịp được duy trì tối thiểu 17,5 giây; lời giảng có thể kéo nhịp dài hơn nếu cần. Mỗi nhịp có hoạt hình hướng chú ý, công thức và kết luận xuất hiện từng bước.
- Giọng Edge TTS `vi-VN-NamMinhNeural`; 44 clip tạo khi GitHub Actions chạy `voice=on`. Có thêm SRT và bản lời giảng đầy đủ.

## Kiểm tra chất lượng

- Liệt kê toán bằng `itertools.product`, với tất cả các đáp số: 6, 12, 5, 6, 12, 5, 10.
- Tổng quan 8 ảnh chương được trích từ **MP4 Manim thật sau render**, kèm `qa_comb02_v2/report.json`.
- Nếu video ngắn dưới 750 giây, có sai biệt thời gian lớn, hoặc bật voice mà không có luồng audio: workflow báo thất bại.
- Các hình trong `preview/comb02_v2` là ảnh dựng trước bằng PIL, KHÔNG phải khung hình Manim.
- Trước khi xuất bản cần mở MP4, nghe âm thanh, kiểm tra ảnh thật và duyệt giảng dạy. Bài kiểm thử logic không thay thế xem thực tế.
