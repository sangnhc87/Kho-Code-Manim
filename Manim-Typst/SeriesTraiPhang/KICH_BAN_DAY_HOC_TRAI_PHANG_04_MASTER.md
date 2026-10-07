# KỊCH BẢN DẠY HỌC — TRẢI PHẲNG 04 MASTER
## Lập phương — đường đi qua đủ 6 mặt

### 1. Mô hình
Cho lập phương cạnh `a`.

Kiến bắt đầu tại đỉnh `A'` và kết thúc tại đỉnh `B'`.

Nếu không có điều kiện gì thêm thì đường ngắn nhất chỉ là cạnh:

`A'B' = a`.

Nhưng trong bài này, kiến **bắt buộc** phải đi qua đủ sáu mặt theo thứ tự:

`mặt trước → mặt phải → mặt sau → mặt đáy → mặt trái → mặt trên`.

Vì vậy đây là bài toán đường đi ngắn nhất **có điều kiện**.

### 2. Năm cạnh chung
Đường đi phải lần lượt cắt:

- `BB'` tại `X`;
- `CC'` tại `Y`;
- `DC` tại `Z`;
- `AD` tại `T`;
- `A'D'` tại `U`.

Sau khi gấp trở lại, đường đi là:

`A' → X → Y → Z → T → U → B'`.

### 3. Trải phẳng
Giữ mặt trước làm mặt đầu tiên.

Mở lần lượt:
1. mặt phải quanh `BB'`;
2. mặt sau quanh `CC'`;
3. mặt đáy quanh `DC`;
4. mặt trái quanh `AD`;
5. mặt trên quanh `A'D'`.

Sau khi mở, sáu mặt tạo thành một dải phẳng.

### 4. Tính độ dài
Trên bản trải, gọi:
- `P` là ảnh của `A'`;
- `Q` là ảnh của `B'`.

Có thể chọn:

`P=(0,a)`, `Q=(5a,-a)`.

Do đó:

`Delta x = 5a`

và

`Delta y = 2a`.

Suy ra:

`PQ = sqrt((5a)^2+(2a)^2) = a sqrt(29)`.

Vì mọi đường hợp lệ trong dải sau khi trải đều nối cùng `P` và `Q`,
đoạn thẳng `PQ` là ngắn nhất.

Vậy:

`L_min = a sqrt(29)`.

### 5. Tìm năm điểm đổi mặt
Đường thẳng `PQ` có phương trình:

`y = a - (2/5)x`.

Từ đó:

- tại `BB'`: `BX = 3a/5`;
- tại `CC'`: `CY = a/5`;
- tại `DC`: `DZ = a/2`;
- tại `AD`: `AT = 4a/5`;
- tại `A'D'`: `A'U = 2a/5`.

Tất cả các tỷ số đều nằm nghiêm ngặt giữa `0` và `1`.
Vì vậy không giao điểm nào trùng với một đỉnh; đường thật sự đi qua đủ sáu mặt.

### 6. Kết luận
Đường ngắn nhất có điều kiện là:

`A' → X → Y → Z → T → U → B'`

với:

`L_min = a sqrt(29)`.

Điểm quan trọng nhất của bài:
**càng nhiều lần đổi mặt, càng nên trải cả dải thay vì cố tìm từng điểm trên hình không gian.**
