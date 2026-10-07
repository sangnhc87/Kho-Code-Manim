# KỊCH BẢN DẠY HỌC — TRẢI PHẲNG 07 MASTER
## Tứ diện đều — từ A đến B nhưng phải chạm cạnh đối CD

### Mô hình
Cho tứ diện đều `ABCD` cạnh `a`.

Kiến bắt đầu tại đỉnh `A`, kết thúc tại đỉnh `B`, nhưng bắt buộc phải chạm cạnh đối `CD`.

Nếu không có điều kiện này thì đường ngắn nhất chỉ là cạnh `AB=a`.
Điều kiện phải chạm `CD` khiến bài toán trở thành một bài trải phẳng thực sự.

### 1. Gọi điểm chạm là X
Với `X in CD`:

`L(X)=AX+XB`.

Đoạn `AX` nằm trên mặt `ACD`.
Đoạn `XB` nằm trên mặt `BCD`.

### 2. Mở hai mặt
Giữ mặt `ACD`, mở mặt `BCD` quanh cạnh chung `CD`.

Sau khi mở, ảnh của `B` là `B_1`.
Hai tam giác đều nằm ở hai phía của `CD`.

Do tính đối xứng:
- `A` và `B_1` đối xứng qua `CD`;
- đoạn `AB_1` vuông góc `CD`;
- `AB_1` cắt `CD` tại trung điểm `M`.

Vì vậy điểm tối ưu là:

`CM=MD=a/2`.

### 3. Tính độ dài
Trong tam giác đều cạnh `a`:

`AM=a sqrt(3)/2`.

Tương tự:

`MB_1=a sqrt(3)/2`.

Suy ra:

`L_min=AB_1=a sqrt(3)`.

### 4. Kiểm tra bằng biến
Đặt `CX=x`, `0<=x<=a`.

Ta có:

`AX^2=(x-a/2)^2+3a^2/4`

và:

`XB^2=(x-a/2)^2+3a^2/4`.

Do đó tổng nhỏ nhất khi:

`x=a/2`.

Một lần nữa, `X=M`.

### 5. Gấp lại
Khi gấp hai mặt trở lại:
- `AM` nằm trên mặt `ACD`;
- `MB` nằm trên mặt `BCD`.

Đường kiến tối ưu là:

`A -> M -> B`.

### Kết quả
`CM=MD=a/2`

và

`L_min=a sqrt(3)`.

### Mở rộng
Tứ diện đều có ba cặp cạnh đối:
- `AB` và `CD`;
- `AC` và `BD`;
- `AD` và `BC`.

Do tính đối xứng, ba bài toán tương ứng được giải hoàn toàn giống nhau.
