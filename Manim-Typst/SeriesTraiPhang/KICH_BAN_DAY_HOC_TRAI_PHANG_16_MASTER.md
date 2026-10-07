# KỊCH BẢN DẠY HỌC — TRẢI PHẲNG 16 MASTER
## Mái nhà lăng trụ tam giác — dây cáp qua hai mái dốc

### Mô hình
Mái nhà có tiết diện trước là tam giác cân `ASB`:
- `AB=6`;
- gọi `N` là trung điểm `AB`, `AN=NB=3`;
- `SN=4`.

Suy ra:

`AS=SB=5`.

Ngôi nhà dài:

`SS'=8`.

Hai mặt mái là hai hình chữ nhật `5 x 8`:
- mái trái `ASS'A'`;
- mái phải `SBB'S'`.

Sợi cáp bắt đầu tại `A`, kết thúc tại `B'`, và chỉ được nằm trên hai mặt mái.

### 1. Đường thẳng trong không gian không hợp lệ
Khoảng cách thẳng từ `A` tới `B'` có:
- độ lệch ngang `6`;
- độ lệch dọc `8`.

Do đó:

`AB'=10`.

Nhưng đoạn này đi xuyên qua khoảng không dưới mái, không nằm trên bề mặt.

### 2. Gọi điểm vượt nóc là X
Với `X in SS'`:

`L(X)=AX+XB'`.

Trong đó:
- `AX` nằm trên mái trái;
- `XB'` nằm trên mái phải.

### 3. Trải hai mái
Giữ mái trái.
Mở mái phải quanh đường nóc `SS'`.

Hai hình chữ nhật `5 x 8` ghép thành một hình chữ nhật:

`10 x 8`.

Đường nóc trở thành đường thẳng chính giữa bản trải, cách hai mép bên mỗi bên `5`.

### 4. Đường ngắn nhất
Trên bản trải:
- `A=(0,0)`;
- `B'=(10,8)`.

Đường ngắn nhất là đoạn thẳng `AB'`.

`L^2=10^2+8^2=164`.

Suy ra:

`L_min=2 sqrt(41)`.

### 5. Điểm cắt đường nóc
Đường nóc có phương trình `x=5`.

Đoạn `AB'` đi từ `x=0` tới `x=10`, nên cắt đường nóc đúng tại nửa hành trình.

Gọi giao điểm là `M`.

Vì `SS'=8`:

`SM=MS'=4`.

### 6. Độ dài từng phần
Trên mái trái:

`AM=sqrt(5^2+4^2)=sqrt(41)`.

Tương tự:

`MB'=sqrt(41)`.

Do đó:

`L_min=2 sqrt(41)`.

### 7. Gấp lại
Khi gấp mái về vị trí ban đầu:
- cáp đi từ `A` tới `M` trên mái trái;
- vượt đường nóc tại `M`;
- đi từ `M` tới `B'` trên mái phải.

### 8. So sánh với đường men theo cạnh
Nếu đi:

`A -> S -> S' -> B'`

thì:

`L_edge=5+8+5=18`.

Trong khi:

`2 sqrt(41)<18`.

Vì vậy đường tối ưu đi chéo qua hai mái chứ không bám theo cạnh.

### 9. Công thức tổng quát
Gọi:
- nửa chiều rộng nhà là `a`;
- độ cao mái là `h`;
- chiều dài nhà là `d`.

Độ dài một mái dốc:

`s=sqrt(a^2+h^2)`.

Sau khi trải, hai mái tạo thành hình chữ nhật có:
- chiều ngang `2s`;
- chiều dọc `d`.

Vì vậy:

`L_min=sqrt((2s)^2+d^2)`

hay:

`L_min=sqrt(4(a^2+h^2)+d^2)`.

Trong cấu hình hai đầu đối xứng như bài này, đường tối ưu luôn cắt đường nóc tại trung điểm.

### Ý chính
Một đường gấp trên hai mái dốc trở thành một đoạn thẳng khi hai mái được mở quanh đường nóc.
