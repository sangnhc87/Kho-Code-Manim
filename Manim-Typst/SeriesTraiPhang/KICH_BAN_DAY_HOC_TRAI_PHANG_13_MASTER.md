# KỊCH BẢN DẠY HỌC — TRẢI PHẲNG 13 MASTER
## Hình nón — trải thành hình quạt

### Mô hình
Cho hình nón tròn xoay:
- bán kính đáy `r=3`;
- chiều cao `h=4`;
- đường sinh `l=5`.

Hai điểm `A`, `B` nằm trên vành đáy.

Nhìn từ trên xuống, góc nhỏ hơn giữa hai bán kính tới `A`, `B` là:

`delta=5 pi/6`.

Kiến chỉ được đi trên mặt xung quanh của hình nón.

### 1. Đường thẳng AB không hợp lệ
Đoạn thẳng `AB` là một dây cung của đường tròn đáy.

Nó nằm trong mặt phẳng đáy, không nằm trên mặt xung quanh.

Vì vậy phải khai triển mặt nón.

### 2. Bản khai triển của mặt nón
Đường sinh:

`l=sqrt(r^2+h^2)=sqrt(3^2+4^2)=5`.

Khi cắt theo một đường sinh và trải ra, mặt nón thành một hình quạt tròn bán kính `5`.

Gọi góc của toàn hình quạt là `Phi`.

Cung ngoài của hình quạt bằng đúng chu vi đáy:

`l Phi=2 pi r`.

Do đó:

`Phi=2 pi r/l=6 pi/5`.

Tức `216°`.

### 3. Góc quanh trục không giữ nguyên
Trên đường tròn đáy, cung nhỏ `AB` có độ dài:

`s=r delta`.

Với:

`r=3`, `delta=5 pi/6`,

ta được:

`s=5 pi/2`.

Trên bản khai triển, cùng cung ấy nằm trên đường tròn bán kính `l=5`.

Gọi góc tương ứng là `alpha`.

Vì độ dài cung giữ nguyên:

`r delta=l alpha`.

Suy ra:

`alpha=(r/l) delta`.

Thay số:

`alpha=(3/5)(5 pi/6)=pi/2`.

Vậy `150°` quanh trục của hình nón trở thành `90°` trên hình quạt.

### 4. Đường ngắn nhất
Trên bản khai triển:
- `SA=SB=5`;
- `angle ASB=pi/2`.

Đường ngắn nhất là đoạn thẳng `AB`.

Tam giác `SAB` vuông cân nên:

`AB=sqrt(5^2+5^2)=5 sqrt(2)`.

Do phép khai triển giữ nguyên độ dài trên mặt:

`L_min=5 sqrt(2)`.

### 5. So sánh với đường qua đỉnh
Nếu đi:

`A -> S -> B`

thì độ dài:

`AS+SB=10`.

Ta có:

`5 sqrt(2)<10`.

Vì vậy đường tối ưu không đi qua đỉnh nón.

### 6. Gấp lại
Khi gấp hình quạt trở lại thành nón, đoạn thẳng `AB` trên hình quạt trở thành một đường cong trên mặt nón.

Đường cong này là đường ngắn nhất trên bề mặt giữa hai điểm đã cho.

### 7. Công thức tổng quát cho hai điểm trên vành đáy
Với hình nón có:
- bán kính đáy `r`;
- đường sinh `l`;

và hai điểm trên vành đáy cách nhau góc quanh trục `delta`:

`alpha=(r/l) delta`.

Độ dài dây cung trên hình quạt:

`L=2l sin(alpha/2)`.

Do đó:

`L=2l sin(r delta/(2l))`.

### 8. Hai điểm bất kỳ trên mặt nón
Nếu hai điểm cách đỉnh theo đường sinh lần lượt là:

`rho_1`, `rho_2`,

và góc trên bản khai triển là:

`alpha=(r/l) delta`,

thì định lý cos cho:

`L^2=rho_1^2+rho_2^2-2 rho_1 rho_2 cos(alpha)`.

### Ý chính
Điểm mới của hình nón là **đổi góc**:

`alpha=(r/l) delta`.

Sau khi đổi đúng góc, bài toán trở lại hình học phẳng.
