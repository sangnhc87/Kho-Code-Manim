# KỊCH BẢN DẠY HỌC — TRẢI PHẲNG 09 MASTER
## Chóp tam giác không đều — chọn đúng dải mặt

### Mô hình
Cho chóp tam giác `S.ABC`.

Bài toán chỉ cần hai mặt quanh cạnh đối `SC`.

Trong mặt `ASC`:
- `AH ⟂ SC`;
- `SH=2`;
- `AH=3`.

Trong mặt `BSC`:
- `BK ⟂ SC`;
- `SK=8`;
- `BK=5`.

Ngoài ra `SC=10`.

Kiến bắt đầu ở đỉnh `A`, kết thúc ở đỉnh `B`, nhưng bắt buộc phải cắt **phần bên trong** của cạnh `SC`.

### 1. Vì sao phải chọn đúng dải mặt?
Nếu bỏ điều kiện, đường ngắn nhất chỉ là cạnh `AB=sqrt(70)`.

Nhưng cạnh `AB` không cắt phần trong của `SC`.

Muốn cắt `SC`, ngay trước điểm cắt đường phải nằm trên mặt `ASC`; ngay sau điểm cắt đường phải nằm trên mặt `BSC`.

Vì vậy dải mặt đúng là:

`ASC -> BSC`.

Một dải khác, chẳng hạn `SAB + ABC`, có thể trải rất đúng nhưng không giải đúng điều kiện của bài.

### 2. Gọi điểm cắt là X
Với `X in SC`:

`L(X)=AX+XB`.

### 3. Trải hai mặt
Giữ mặt `ASC`.
Mở mặt `BSC` quanh cạnh chung `SC`.

Sau khi mở, ảnh của `B` là `B_1`.

Đặt hệ trục trên bản trải:
- `S=(0,0)`;
- `C=(10,0)`.

Từ dữ kiện:
- `A=(2,3)`;
- `B_1=(8,-5)`.

### 4. Tìm điểm đổi mặt
Đường thẳng qua `A(2,3)` và `B_1(8,-5)` có hệ số góc `-4/3`.

Phương trình:

`y-3 = -4/3 * (x-2)`.

Trên `SC`, `y=0`.

Suy ra:

`x_M=17/4`.

Do đó:

`SM=17/4`.

Điểm `M` nằm thực sự trong đoạn `SC`.

### 5. Tính độ dài
`AM = sqrt((9/4)^2+3^2)=15/4`.

`MB_1=25/4`.

Suy ra:

`L_min=AM+MB_1=10`.

### 6. Chứng minh tối ưu
Với mọi `X in SC`:

`AX+XB_1 >= AB_1`.

Dấu bằng xảy ra khi `A, X, B_1` thẳng hàng.

Do đó điểm tối ưu duy nhất là `M`.

### 7. Gấp lại
Đường kiến thật trên chóp là:

`A -> M -> B`.

Trong đó:
- `AM` nằm trên mặt `ASC`;
- `MB` nằm trên mặt `BSC`;
- `SM=17/4`.

### 8. Công thức tổng quát
Sau khi trải hai mặt quanh một cạnh, giả sử:

`A=(p,h_1)`

và:

`B_1=(q,-h_2)`.

Khi đó:

`L = sqrt((q-p)^2+(h_1+h_2)^2)`.

Điểm đổi mặt trên trục chung có hoành độ:

`x_M=(h_2 p+h_1 q)/(h_1+h_2)`.

Bài này tương ứng:
- `p=2`;
- `q=8`;
- `h_1=3`;
- `h_2=5`.

Suy ra:

`x_M=17/4`

và:

`L=10`.

### Ý chính của Video 09
Không phải cứ trải được là đã chọn đúng bài toán.

Trước khi tính, cần xác định:
1. đường bắt buộc đi qua cạnh nào;
2. hai mặt nào nằm ngay trước và sau cạnh đó;
3. chỉ sau khi chọn đúng dải mới bắt đầu trải.
