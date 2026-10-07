# KỊCH BẢN DẠY HỌC — TRẢI PHẲNG 14 MASTER
## Hình nón cụt — vành quạt và bài toán đường thẳng không hợp lệ

### Mô hình
Cho hình nón cụt tròn xoay:
- bán kính đáy lớn `R=6`;
- bán kính đáy nhỏ `r=3`;
- chiều cao `H=4`.

Độ chênh hai bán kính là `3`, nên đường sinh nón cụt:

`g=sqrt(3^2+4^2)=5`.

Hai điểm `A`, `B` nằm trên vành đáy lớn.

### 1. Kéo dài thành nón đầy
Nếu kéo dài các đường sinh tới đỉnh tưởng tượng:
- bán kính ngoài của bản khai triển là `rho_2=10`;
- bán kính trong là `rho_1=5`.

Toàn mặt xung quanh trải thành một **vành quạt**.

Góc toàn vành quạt:

`Phi=6 pi/5`.

### 2. Chọn lớp đường dài quanh trục
Hai điểm A, B chỉ cách nhau `60°` theo chiều ngắn.

Nhưng ta xét lớp đường đi theo chiều còn lại:

`delta_L=300°=5 pi/3`.

Vì tỉ lệ đổi góc là:

`R/rho_2=6/10=3/5`,

nên trên bản khai triển:

`alpha_L=(3/5)delta_L=pi`.

Tức A và B nằm đối nhau qua tâm của hai đường tròn đồng tâm.

### 3. Vì sao đoạn thẳng AB không hợp lệ?
Nếu nối thẳng A với B trên bản trải:

`AB=20`.

Nhưng đoạn thẳng này đi qua tâm, do đó xuyên qua toàn bộ phần lỗ bán kính `5`.

Phần lỗ không thuộc mặt nón cụt.

Vì vậy đoạn thẳng AB **không phải** một đường trên bề mặt.

### 4. Cấu trúc của đường tối ưu
Khi một lỗ tròn chắn đoạn thẳng, đường ngắn nhất phải gồm:

1. tiếp tuyến `AP` tới đường tròn trong;
2. cung tròn `PQ` trên đường tròn trong;
3. tiếp tuyến `QB` tới B.

### 5. Tính hai đoạn tiếp tuyến
Trong tam giác vuông `SAP`:

`SA=10`,
`SP=5`.

Do đó:

`AP=sqrt(10^2-5^2)=5 sqrt(3)`.

Tương tự:

`QB=5 sqrt(3)`.

### 6. Tính cung PQ
Gọi:

`beta=angle ASP`.

Ta có:

`cos beta=5/10=1/2`.

Suy ra:

`beta=pi/3`.

Vì:

`angle ASB=pi`,

nên:

`angle PSQ=pi-2 beta=pi/3`.

Bán kính đường tròn trong là `5`, nên:

`s_PQ=5*pi/3`.

### 7. Kết quả trong lớp đường 300°
Cộng ba phần:

`L=AP+s_PQ+QB`.

Suy ra:

`L=10 sqrt(3)+5 pi/3`.

Khi gấp lại, đường này:
- đi từ A lên vành trên;
- chạm vành trên tại P;
- men theo một đoạn của vành trên;
- rời vành tại Q;
- đi xuống B.

### 8. Nếu không ràng buộc chiều dài
Chiều ngắn quanh trục chỉ là:

`delta_S=pi/3`.

Trên bản khai triển:

`alpha_S=(3/5)(pi/3)=pi/5`.

Đoạn dây cung tương ứng có độ dài:

`L_short=20 sin(pi/10)`.

Khoảng cách từ tâm tới dây cung là:

`10 cos(pi/10)`,

lớn hơn `5`, nên đoạn thẳng không đi vào lỗ.

Do đó đây là đường hợp lệ và ngắn hơn rất nhiều.

### 9. Quy tắc kiểm tra tính hợp lệ
Với hai điểm cùng nằm trên đường tròn ngoài bán kính `R_out`, cách nhau góc `alpha` trên bản khai triển:

Khoảng cách từ tâm tới dây cung là:

`d=R_out cos(alpha/2)`.

Nếu:

`d >= R_in`

thì đoạn thẳng nằm hoàn toàn ngoài lỗ.

Nếu:

`d < R_in`

thì đoạn thẳng bị lỗ chặn và phải thay bằng:

`tiếp tuyến + cung tròn + tiếp tuyến`.

### Ý chính
Ở hình nón đầy, nối thẳng hai ảnh trên hình quạt thường là bước cuối.

Ở hình nón cụt, chưa đủ.

Phải kiểm tra thêm:
**đoạn thẳng có nằm hoàn toàn trong miền vành quạt hay không?**
