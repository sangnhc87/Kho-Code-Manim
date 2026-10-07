# KỊCH BẢN DẠY HỌC — TRẢI PHẲNG 17 MASTER
## Điểm đích chạy trên cạnh — đường tối ưu biến thiên theo tham số

### Mô hình
Cho khối lập phương cạnh `4`.

- `A` là điểm xuất phát cố định.
- `P` chạy trên cạnh `CC'`.
- Đường đi chỉ dùng hai mặt `ABCD` và `BCC'B'`.

Đặt:

`t=CP`, với `0<=t<=4`.

### 1. Gọi X là điểm đổi mặt
Với `X in BC`:

`L=AX+XP`.

Đoạn `AX` nằm trên đáy.
Đoạn `XP` nằm trên mặt bên phải.

### 2. Trải mặt bên
Giữ đáy `ABCD`.
Mở mặt `BCC'B'` quanh cạnh chung `BC`.

Chọn hệ trục trên bản trải:

- `A=(-2,-2)`;
- `B=(2,-2)`;
- `C=(2,2)`.

Ảnh của `P` sau khi mở là:

`P_1=(2+t,2)`.

### 3. Độ dài nhỏ nhất theo t
Độ lệch từ `A` tới `P_1`:

`Delta x=4+t`,

`Delta y=4`.

Do đó:

`L(t)=sqrt((4+t)^2+16)`.

### 4. Vị trí điểm đổi mặt
Đường thẳng `AP_1` cắt `BC` tại `X`.

Từ tam giác đồng dạng:

`BX/4=4/(4+t)`.

Suy ra:

`BX=16/(4+t)`.

Khi `t` tăng, `BX` giảm, nên X trượt từ C về phía B.

### 5. Ba giá trị đặc biệt
Khi `t=0`:

- `P=C`;
- `X=C`;
- `L=4 sqrt(2)`.

Khi `t=2`:

- `BX=8/3`;
- `L=2 sqrt(13)`.

Khi `t=4`:

- `P=C'`;
- `BX=2`;
- X là trung điểm `BC`;
- `L=4 sqrt(5)`.

### 6. Tính đơn điệu

`L(t)=sqrt((4+t)^2+16)`.

Đạo hàm:

`L'(t)=(4+t)/L(t)>0` trên `[0,4]`.

Vì vậy P càng đi lên thì đường ngắn nhất trong dải hai mặt càng dài.

### 7. Công thức tổng quát với cạnh a
Nếu khối lập phương có cạnh `a`, đặt `t=CP`, `0<=t<=a`.

Khi trải:

`L(t)=sqrt((a+t)^2+a^2)`.

Điểm đổi mặt thỏa:

`BX=a^2/(a+t)`.

Và:

`L'(t)=(a+t)/L(t)>0`.

### Ý chính
Một tham số `t` điều khiển đồng thời:

1. vị trí điểm đích P;
2. độ dài tối ưu `L(t)`;
3. vị trí điểm đổi mặt X.

Khi `t` thay đổi liên tục, cả đường đi tối ưu cũng chuyển động liên tục trên bề mặt.
