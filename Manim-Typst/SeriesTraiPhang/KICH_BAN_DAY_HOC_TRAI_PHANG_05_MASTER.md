# KỊCH BẢN DẠY HỌC — TRẢI PHẲNG 05 MASTER
## Lăng trụ đứng tam giác đều — kiến đi qua đủ 3 mặt bên

### Mô hình
Cho lăng trụ đứng tam giác đều `ABC.A'B'C'` với:
- `AB=BC=CA=a`;
- `AA'=BB'=CC'=h`.

Kiến bắt đầu tại đỉnh `A`, kết thúc tại đỉnh `A'`.

Nếu đi tự do thì đường ngắn nhất chỉ là cạnh `AA'=h`.
Trong video này, kiến bắt buộc phải đi vòng qua đủ ba mặt bên theo thứ tự:

`ABB'A' → BCC'B' → CAA'C'`.

### Hai điểm đổi mặt
Gọi:
- `X in BB'`;
- `Y in CC'`.

Khi gấp lại, đường kiến là:

`A → X → Y → A'`.

### Trải phẳng
Giữ mặt `ABB'A'`.

Mở `BCC'B'` quanh `BB'` một góc `120°`.
Tiếp tục mở `CAA'C'` quanh `CC'` một góc `120°`.

Ba mặt bên trở thành một hình chữ nhật có kích thước:

`3a × h`.

### Độ dài ngắn nhất
Trên bản trải, ảnh của `A` và `A'` là hai đỉnh đối diện của hình chữ nhật `3a × h`.

Do đó:

`L_min = sqrt((3a)^2+h^2)=sqrt(9a^2+h^2)`.

Đây là cực tiểu thật sự trong dải ba mặt vì sau khi trải, mọi đường hợp lệ đều nối cùng hai điểm và đoạn thẳng là ngắn nhất trong mặt phẳng.

### Vị trí đổi mặt
Đường thẳng cắt hai cạnh chung lần lượt tại một phần ba và hai phần ba chiều ngang của bản trải.

Suy ra:

- `BX=h/3`;
- `CY=2h/3`.

Hai điểm đều nằm trong lòng cạnh nên đường thực sự đi qua đủ ba mặt bên.

### Kết luận

`A → X → Y → A'`

với:

`BX=h/3`, `CY=2h/3`,

và

`L_min=sqrt(9a^2+h^2)`.

Do ba mặt bên bằng nhau, đi vòng theo chiều ngược lại cho cùng độ dài.
