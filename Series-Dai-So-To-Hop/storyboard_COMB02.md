# COMB02 — QUY TẮC NHÂN — BẢNG PHÂN CẢNH

**Trạng thái:** source sẵn sàng để thử render bằng GitHub Actions. **Chưa** có thoại/TTS, chưa duyệt MP4 thực tế.

**Khung hình:** 1920 × 1080, 30 fps khi render fullhd, nền tối, 2 cột trái hình động/phải bài toán-lập luận, Typst cho công thức. **Màu:** cyan = áo/bước 1, vàng = quần/bước 2, tím = bước 3, đỏ = trường hợp cấm, xanh lá = kết quả hợp lệ.

| Phần | Hình động (trái) | Lời giải (phải) | Điểm cần kiểm tra |
|---|---|---|---|
| 01 Mở đầu | Ba áo A1–A3 xuất hiện; hai quần Q1–Q2 | Đề bài đầy đủ; dự đoán | Chữ đề vừa panel phải |
| 02 Liệt kê | Sáu bộ A1Q1, A1Q2,..., A3Q2 hiện theo từng cột | 2+2+2 = 6 và 3·2=6 | Đúng sáu cặp khác nhau |
| 03 Cây chọn | Từ một gốc tách ba nhánh áo, mỗi nhánh hai quần | Đếm lá = 3·2=6 | Không thiếu nhánh, không chồng nhãn |
| 04 Quy tắc | Hai ô bước 1/m cách → bước 2/n cách | m·n; điều kiện mỗi kết quả bước 1 đều có n lựa chọn | Không phát biểu quy tắc nhân quá rộng |
| 05 Mở rộng | Hàng áo 3 lựa chọn, quần 2, mũ 2 | 3·2·2=12 | Các bước độc lập về số lựa chọn |
| 06 Có cấm | Ma trận 3×2; gạch đúng ô A1-Q2 | 6-1=5 | Chỉ một ô bị cấm |
| 07 Đếm nhánh | A1:1; A2:2; A3:2 | 1+2+2=5; không được dùng 3·2 sau khi cấm | Tránh sai lầm phổ biến |
| 08 Phân biệt & vận dụng | Áo HOẶC quần (5); áo VÀ quần (6) | Thử thách bữa sáng 2·3·2=12 | Cho thời gian học sinh nghĩ trước khi hiện đáp án |

## Phân tích toán học

- Đối tượng được đếm là một **bộ trang phục** (áo, quần) có thứ tự vai trò, khác nhau nếu áo hoặc quần khác nhau.
- Khi không ràng buộc, tập kết quả là tích Descartes: `3 × 2 = 6`.
- Với A1 không được ghép Q2, tập hợp hợp lệ là tích Descartes trừ một cặp duy nhất, còn 5. Nếu đếm theo áo: `1 + 2 + 2 = 5`, không dùng sai `3 × 2`.
- Phân biệt cộng và nhân dựa vào **một lựa chọn từ hai loại không trùng** và **một cặp gồm đủ hai loại**.

## Yêu cầu nghiệm thu

1. Unit test đều đạt; dựng được 6 Typst asset cho COMB02.
2. MP4 preview không có chữ tràn panel, vật thể ngoài khung, các cảnh luôn giữ logic màu.
3. Test xem video có **audio hay không**: bản code hiện chưa chứa audio; không được ghi là đã thuyết minh.
4. Bản Full HD phải chạy toàn bộ không exception sau đó mới dùng trong giảng dạy.
