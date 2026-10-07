# KỊCH BẢN DẠY HỌC — TRẢI PHẲNG 10 MASTER
## Chóp cụt vuông — dải hình thang

### Mô hình
Cho chóp cụt vuông `ABCD.A'B'C'D'` có:
- đáy lớn là hình vuông cạnh `6`;
- đáy nhỏ là hình vuông cạnh `4`;
- chiều cao `H=2 sqrt(2)`.

Hai đáy đồng tâm và song song.

Mỗi đỉnh của đáy nhỏ lùi vào `1` theo hai phương so với đỉnh tương ứng của đáy lớn.

### 1. Hình dạng một mặt bên
Xét hình thang `ABB'A'`.

Hai đáy:
- `AB=6`;
- `A'B'=4`.

Mỗi đầu đáy nhỏ lệch vào `1`.

Chiều cao hình thang trên chính mặt bên:

`h_trap = sqrt(H^2+1^2)=3`.

Cạnh bên:

`BB' = sqrt(3^2+1^2)=sqrt(10)`.

Vậy mỗi mặt bên là hình thang cân có:
- hai đáy `6` và `4`;
- chiều cao `3`;
- hai cạnh bên `sqrt(10)`.

### 2. Bài toán
Kiến bắt đầu tại đỉnh `A`, kết thúc tại đỉnh đối diện `C`, và chỉ được đi trên các mặt bên.

Có hai hướng đối xứng:
- qua `B`: `ABB'A' -> BCC'B'`;
- qua `D`: `DAA'D' -> CDD'C'`.

Chỉ cần giải hướng qua `B`.

### 3. Gọi điểm đổi mặt
Gọi `X in BB'`.

Độ dài đường đi:

`L(X)=AX+XC`.

### 4. Trải hai hình thang
Giữ mặt `ABB'A'`.
Mở mặt `BCC'B'` quanh cạnh chung `BB'`.

Ảnh của `C` là `C_1`.

Hai hình thang cân bằng nhau nằm ở hai phía của `BB'`, nên `A` và `C_1` đối xứng qua `BB'`.

Do đó đường ngắn nhất là đoạn `AC_1`, vuông góc với `BB'`.

Gọi `M=AC_1 inter BB'`.

### 5. Tính AM bằng diện tích
Trong tam giác `ABB'`:

`K=1/2 * 6 * 3 = 9`.

Nếu lấy `BB'=sqrt(10)` làm đáy:

`K=1/2 * sqrt(10) * AM`.

Suy ra:

`AM=18/sqrt(10)=9 sqrt(10)/5`.

### 6. Tìm M trên BB'
Trong hình thang, từ `B` tới `B'` lệch vào `1` và đi lên `3`.

Đặt `beta = góc ABB'`.

`cos beta = 1/sqrt(10)`.

Do `AM ⟂ BB'`, trong tam giác vuông `ABM`:

`BM = AB cos beta`
`= 6/sqrt(10)`
`= 3 sqrt(10)/5`.

Vậy điểm đổi mặt nằm ở:

`BM=3 sqrt(10)/5`.

### 7. Độ dài nhỏ nhất
Do `A` và `C_1` đối xứng:

`MC_1=AM`.

Suy ra:

`L_min=AC_1=2AM=18 sqrt(10)/5`.

### 8. Nếu được đi trên đáy
Đường chéo đáy lớn:

`AC=6 sqrt(2)`.

Và:

`6 sqrt(2) < 18 sqrt(10)/5`.

Vì vậy điều kiện chỉ đi trên mặt bên là quan trọng.

### 9. Mở cả bốn mặt bên
Nếu cắt một cạnh bên và mở toàn bộ mặt xung quanh, ta được một dải gồm bốn hình thang cân nối tiếp nhau.

Khác lăng trụ:
- bản trải không phải một hình chữ nhật dài;
- mỗi hình thang làm hướng của dải thay đổi;
- phải chọn đúng chuỗi mặt trước khi nối thẳng hai điểm.

### 10. Công thức tổng quát
Với chóp cụt vuông có:
- cạnh đáy lớn `a`;
- cạnh đáy nhỏ `b`;
- chiều cao `H`.

Đặt:

`d=(a-b)/2`.

Chiều cao hình thang bên:

`s=sqrt(H^2+d^2)`.

Cạnh bên chóp cụt:

`l=sqrt(H^2+2d^2)`.

Với đường từ hai đỉnh đối diện qua hai mặt bên kề nhau:

`L=2as/l`.

Điểm đổi mặt trên cạnh bên thỏa:

`BM=ad/l`.

Thay:
- `a=6`;
- `b=4`;
- `H=2 sqrt(2)`;

ta có:
- `d=1`;
- `s=3`;
- `l=sqrt(10)`;
- `BM=3 sqrt(10)/5`;
- `L_min=18 sqrt(10)/5`.
