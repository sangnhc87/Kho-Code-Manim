# VIDEO 20 MASTER — CAPSTONE: THUẬT TOÁN ĐƯỜNG NGẮN NHẤT TRÊN BỀ MẶT

**Sản phẩm:** video Manim–Typst 1920×1080, 30 fps, lời giảng tiếng Việt. Đây là tập tổng kết series 20 video.

## Mục tiêu

HS biết chuyển một bài toán đường đi trên khối đa diện sang quy trình hình học có thể kiểm tra:

1. Xác định đầu cuối, mặt hợp lệ và các ràng buộc.
2. Liệt kê dải gồm các mặt kề nhau.
3. Mở từng dải bằng phép quay quanh cạnh chung thật, bảo toàn độ dài.
4. Nối thẳng hai điểm trên bản trải; kiểm tra cạnh gấp được cắt trong nội phần, đúng thứ tự, đúng miền.
5. Loại đường sai; so sánh độ dài các đường còn lại.

## Ví dụ minh họa

Hộp chữ nhật kích thước `8 × 5 × 4`; P nằm trên mặt trước, cách mép trái 2 và cách đáy 3; Q nằm trên mặt sau, cách mép trái 6 và cách đáy 3.

**Lúc đầu cho đi qua mọi mặt.** Qua dải `trước → nắp → sau`, bản trải cho:

- Độ lệch theo phương dài: `6-2=4`.
- Độ lệch theo các mặt: `1+5+1=7`.

Suy ra `L_top = sqrt(4^2+7^2) = sqrt(65)`.

**Thay điều kiện: cấm mặt trên.** Mọi dải đi qua nắp đều bị loại. Dải `trước → đáy → sau` cho:

- Độ lệch theo phương dài: `4`.
- Độ lệch trên ba mặt: `3+5+3=11`.

Suy ra `L_bottom = sqrt(4^2+11^2) = sqrt(137)`.

Hai giao điểm với cạnh bản lề có tọa độ hoành:

- `x_X = 2 + (3/11)×4 = 34/11`.
- `x_Y = 2 + (8/11)×4 = 54/11`.

Vì `0 < x_X < x_Y < 8`, đường đi cắt các cạnh trong nội phần theo đúng thứ tự.

Hai phương án khác qua bên trái và bên phải đều dài `13`; và `sqrt(137)<13`.

### Kết luận

Khi không bị cấm: `L_min=sqrt(65)`.

Khi cấm nắp trên: `L_min=sqrt(137)`.

Chỉ kết luận sau khi kiểm tra toàn bộ những dải mặt hợp lệ cần xét, không chỉ bốn dải trực quan ban đầu.

## Các cảnh trong video

- Mở đề bài cuối series: vì sao không được chọn đường bằng mắt.
- Hiển thị năm bước giải.
- Xác định hai điểm và đồ thị kề mặt.
- Liệt kê dải mặt, tránh bỏ sót dải nhiều mặt.
- Trải thật ba mặt trước – nắp – sau; tính `sqrt(65)`.
- Đặt điều kiện cấm nắp, loại đường không hợp lệ.
- Trải thật ba mặt trước – đáy – sau; tính `sqrt(137)`.
- Kiểm tra hai vị trí cắt cạnh gấp.
- So sánh với các dải qua mặt trái và phải.
- Đưa đường tối ưu ngược lên hình hộp, kiến di chuyển qua ba mặt.
- Chốt năm bước như một phương pháp giải tổng quát.

## Phạm vi của thuật toán

Ở ví dụ này hình hộp **lồi**, các mặt là đa giác phẳng và phép trải là quay cứng quanh các cạnh chung. Bài học không khẳng định quy trình liệt kê dải đơn giản tự động giải mọi bài trên bề mặt không lồi, có lỗ hoặc chứa mặt cong; những dạng đó cần kiểm tra thêm ràng buộc riêng.
