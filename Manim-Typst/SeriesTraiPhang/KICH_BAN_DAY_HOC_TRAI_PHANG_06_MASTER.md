# KỊCH BẢN DẠY HỌC — TRẢI PHẲNG 06 MASTER
## Lăng trụ lục giác đều — hai hướng quanh khối

### Mô hình
Cho lăng trụ đứng có đáy là lục giác đều `ABCDEF`, cạnh đáy `a`, chiều cao `h`.

Kiến bắt đầu tại đỉnh `A` ở đáy dưới và kết thúc tại `C'` ở đáy trên.
Kiến chỉ đi trên các mặt bên.

Có hai hướng quanh lăng trụ:

- Hướng ngắn quanh chu vi: qua 2 mặt `ABB'A'`, `BCC'B'`.
- Hướng còn lại: qua 4 mặt `FAA'F'`, `EFF'E'`, `DEE'D'`, `CDD'C'`.

### Hướng 2 mặt
Trải hai mặt thành hình chữ nhật `2a × h`.

Do đó:

`L_2 = sqrt((2a)^2+h^2)`.

Đường chéo cắt `BB'` tại trung điểm:

`BX=h/2`.

### Hướng 4 mặt
Trải bốn mặt thành hình chữ nhật `4a × h`.

Do đó:

`L_4 = sqrt((4a)^2+h^2)`.

Ba điểm đổi mặt có độ cao:

`h/4`, `h/2`, `3h/4`.

### So sánh
`L_4^2-L_2^2 = 12a^2 > 0`.

Vì vậy:

`L_2<L_4`.

Hướng qua 2 mặt luôn ngắn hơn hướng qua 4 mặt.

### Trường hợp đối xứng
Nếu điểm cuối đổi thành `D'`, hai chiều quanh đáy đều gồm 3 cạnh.
Hai bản trải cùng là hình chữ nhật `3a × h`.

Do đó hai hướng cùng có:

`L = sqrt((3a)^2+h^2)`.

### Quy tắc tổng quát
Nếu theo một chiều cần đi `m` cạnh quanh đáy, chiều còn lại cần `6-m` cạnh:

`L_m=sqrt((ma)^2+h^2)`

và

`L_(6-m)=sqrt(((6-m)a)^2+h^2)`.

Với lục giác đều:
- `m=1`: chọn hướng 1 mặt;
- `m=2`: chọn hướng 2 mặt;
- `m=3`: hai hướng hòa nhau.

### Ví dụ kiểm tra
Nếu `h=3a` và đi từ `A` đến `C'`:

`L_2=a sqrt(13)`

trong khi:

`L_4=5a`.

Nên hướng 2 mặt ngắn hơn.
