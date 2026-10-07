# KỊCH BẢN DẠY HỌC — TRẢI PHẲNG 18 MASTER
## Một mặt bị cấm — thay đổi đường đi ngắn nhất

### 1. Bài toán

Hộp chữ nhật có kích thước dài `8`, rộng `5`, cao `4`. Tọa độ để kiểm tra mô hình:

- Điểm xuất phát `P=(2,0,3)` nằm trong mặt trước `y=0`.
- Điểm kết thúc `Q=(6,5,3)` nằm trong mặt sau `y=5`.
- **Toàn bộ mặt trên `z=4` bị cấm**; kiến chỉ được đi trên năm mặt còn lại, kể cả các cạnh chung của những mặt được phép.

Mục tiêu: tìm đường ngắn nhất hợp lệ trên vỏ hộp từ `P` tới `Q`.

### 2. Nếu không cấm mặt trên

Trải dải ba mặt:

`mặt trước -> mặt trên -> mặt sau`.

Trên bản trải, hai ảnh của `P,Q` lệch theo chiều dài hộp:

`delta_x=6-2=4`.

Theo chiều ngang qua ba mặt:

`delta_y=(4-3)+5+(4-3)=7`.

Do đó:

`L_1=sqrt(4^2+7^2)=sqrt(65)`.

Đường này cắt **phần bên trong** mặt trên nên bị loại khi áp dụng lệnh cấm.

### 3. Đổi sang dải mặt qua đáy

Trải dải ba mặt được phép:

`mặt trước -> đáy -> mặt sau`.

Lần này:

`delta_x=4`, `delta_y=3+5+3=11`.

Suy ra:

`L_2=sqrt(4^2+11^2)=sqrt(137)`.

Đường thẳng thực sự cắt hai cạnh gấp, mỗi giao điểm đều nằm trong cạnh.

### 4. Hai điểm đổi mặt

Gọi `X` là giao điểm với cạnh chung giữa mặt trước và đáy (`y=0, z=0`).

Gọi `Y` là giao điểm với cạnh chung giữa đáy và mặt sau (`y=5, z=0`).

Dùng tham số trên đoạn thẳng của bản trải:

`t_X=3/11`, `t_Y=8/11`.

Hoành độ:

`x_X=2+(3/11)(6-2)=34/11`.

`x_Y=2+(8/11)(6-2)=54/11`.

Do:

`0<34/11<8`, `0<54/11<8`,

nên cả hai điểm chuyển mặt đều hợp lệ.

Trên hình hộp, đường kiến là:

`P -> X -> Y -> Q`.

### 5. So sánh với dải qua hai mặt bên

Dải ba mặt:

`trước -> trái -> sau`:

`L_3=2+5+6=13`.

Dải:

`trước -> phải -> sau`:

`L_4=6+5+2=13`.

Vì:

`sqrt(137)<13`,

nên dải đáy tốt hơn cả hai dải cạnh bên.

### 6. Kiểm tra những dải bốn mặt

Không kết luận vội chỉ từ ba dải mặt. Trong phần kiểm tra hình học, liệt kê tất cả chuỗi mặt kề nhau **không lặp mặt**, bắt đầu từ mặt trước và kết thúc trên mặt sau; loại mọi chuỗi chứa mặt trên; trải cứng từng mặt quanh cạnh chung; chỉ nhận đường thẳng cắt đủ cạnh gấp, theo đúng thứ tự và trong phần trong cạnh.

Với cấu hình này, có **7 chuỗi mặt hợp lệ** sau khi cấm mặt trên.

| Dải mặt | Độ dài |
| --- | ---: |
| trước → đáy → sau | `sqrt(137) ≈ 11.7047` |
| trước → trái → sau | `13` |
| trước → phải → sau | `13` |
| trước → đáy → phải → sau | `≈13.4536` |
| trước → trái → đáy → sau | `≈13.4536` |
| trước → đáy → trái → sau | `≈14.8661` |
| trước → phải → đáy → sau | `≈14.8661` |

Các đường ứng viên bị loại nếu đường thẳng sau khi trải không đi qua những cạnh gấp tương ứng. Trên bề mặt hộp lồi, đường ngắn nhất không xuyên qua một đỉnh lồi, nên phép kiểm tra các dải mặt thẳng hợp lệ bao phủ những đường tối ưu kiểu này.

### 7. Kết luận

Nếu không có mặt cấm:

`L_free=sqrt(65)`.

Khi cấm mặt trên:

`L_min=sqrt(137)`.

Đường tối ưu đổi từ dải **qua nắp** sang dải **qua đáy**.

### 8. Nguyên tắc dạy học

Lời giảng chỉ dẫn dắt học sinh quan sát hình, đặt câu hỏi, trải mặt, kiểm tra đường đi và kết luận; không đọc thuật ngữ sản xuất video hoặc kỹ thuật chương trình. Đặc biệt nhấn mạnh **một đường ngắn về độ dài nhưng không hợp lệ phải bị loại**.
