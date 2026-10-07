# KỊCH BẢN DẠY HỌC — TRẢI PHẲNG 08 MASTER
## Chóp tứ giác đều — mở các mặt bên kiểu cánh quạt

### Mô hình
Cho hình chóp tứ giác đều `S.ABCD` với:

- `AB=BC=CD=DA=6`;
- `SA=SB=SC=SD=5`.

Tâm đáy là `O`. Vì `OA=3 sqrt(2)` nên:

`SO=sqrt(7)`.

Mỗi mặt bên là tam giác cân `5-5-6`.

Kiến bắt đầu tại đỉnh `A`, kết thúc tại đỉnh đối diện `C`, và **chỉ được đi trên các mặt bên**.

### 1. Hai hướng đối xứng
Có hai hướng:

- qua `SAB` rồi `SBC`;
- qua `SAD` rồi `SCD`.

Do hình chóp đều, hai hướng có cùng độ dài. Chỉ cần giải hướng qua cạnh chung `SB`.

### 2. Gọi điểm đổi mặt là X
Với `X in SB`:

`L(X)=AX+XC`.

Đoạn `AX` nằm trên mặt `SAB`.
Đoạn `XC` nằm trên mặt `SBC`.

### 3. Trải hai mặt
Giữ mặt `SAB`.
Mở mặt `SBC` quanh cạnh chung `SB`.

Ảnh của `C` là `C_1`.

Hai tam giác `SAB` và `SBC_1` bằng nhau, nằm ở hai phía của `SB`, nên `A` và `C_1` đối xứng qua `SB`.

Đường ngắn nhất là đoạn thẳng `AC_1`.

Gọi:

`M=AC_1 inter SB`.

Khi đó `AM` vuông góc `SB`.

### 4. Khai thác tam giác 5-5-6
Trong tam giác cân `SAB`, gọi `N` là trung điểm `AB`.

`AN=3`, `SA=5`.

Suy ra:

`SN=4`.

Diện tích:

`K=1/2 * 6 * 4 = 12`.

Mặt khác:

`K=1/2 * SB * AM`.

Do `SB=5`:

`12=1/2 * 5 * AM`.

Suy ra:

`AM=24/5`.

Trong tam giác vuông `AMS`:

`SA=5`, `AM=24/5`.

Do đó:

`SM=7/5`.

### 5. Kết quả
Vì `A` và `C_1` đối xứng qua `SB`:

`MC_1=AM=24/5`.

Suy ra:

`L_min=AC_1=48/5`.

Khi gấp lại, đường tối ưu là:

`A -> M -> C`

với:

`SM=7/5`.

### 6. So sánh với đường qua đáy
Nếu được phép đi trên đáy:

`AC=6 sqrt(2)`.

Ta có:

`6 sqrt(2) < 48/5`.

Vì vậy điều kiện chỉ đi trên các mặt bên là rất quan trọng.

### 7. Mở cả bốn mặt bên
Mỗi mặt bên có góc ở đỉnh `S` là `phi`, với:

`cos phi=7/25`.

Mở bốn mặt bên quanh `S` tạo một bản trải hình cánh quạt.

Vì:

`4 phi < 2 pi`

nên bản trải còn một khe hở.

Trên bản trải này, hai đường từ `A` tới `C` qua `B` hoặc qua `D` xuất hiện đối xứng.

### 8. Công thức tổng quát
Với chóp tứ giác đều có:

- cạnh đáy `a`;
- cạnh bên `l`;

mặt bên là tam giác cân `l-l-a`.

Diện tích một mặt:

`K = a/4 * sqrt(4l^2-a^2)`.

Khoảng cách từ một đỉnh đáy tới cạnh bên chung:

`d = a sqrt(4l^2-a^2)/(2l)`.

Sau khi trải hai mặt, đường ngắn nhất bằng hai lần khoảng cách này:

`L = a sqrt(4l^2-a^2)/l`.

Điểm đổi mặt thỏa:

`SM = l-a^2/(2l)`.

Thay `a=6`, `l=5`:

`SM=7/5`

và:

`L=48/5`.
