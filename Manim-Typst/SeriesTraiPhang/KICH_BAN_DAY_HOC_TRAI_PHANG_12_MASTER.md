# KỊCH BẢN DẠY HỌC — TRẢI PHẲNG 12 MASTER
## Hình trụ — đường đi quấn k vòng

### Mô hình
Cho hình trụ:
- bán kính `r=2`;
- chiều cao `h=3`.

Điểm `A` ở vành dưới.
Điểm `B` ở vành trên, **cùng một đường sinh** với `A`.

Bài toán yêu cầu đường đi trên mặt xung quanh phải quấn đúng `k` vòng trước khi tới `B`.

### 1. Trường hợp k=0
Nếu không quấn vòng:

`L_0=h=3`.

Đây là đường sinh thẳng đứng.

### 2. Vì sao cần nhiều bản sao của hình chữ nhật?
Chu vi đáy:

`C=2 pi r=4 pi`.

Sau khi cắt và khai triển, một hình chữ nhật chỉ biểu diễn một vòng quanh trụ.

Muốn theo dõi đường quấn nhiều vòng, ta đặt các bản sao của hình chữ nhật nối tiếp nhau.

Cùng một điểm `B` trên hình trụ có các ảnh:

`..., B_-2, B_-1, B_0, B_1, B_2, ...`

trên dải phẳng kéo dài vô hạn.

### 3. Quấn đúng một vòng
Với `k=1`, ảnh cần nối là `B_1`.

Độ lệch ngang:

`Delta s_1=4 pi`.

Độ lệch đứng:

`3`.

Do đó:

`L_1=sqrt((4 pi)^2+3^2)=sqrt(16 pi^2+9)`.

Khi cuộn lại, đoạn thẳng từ `A` tới `B_1` trở thành một đường xoắn đúng một vòng.

### 4. Quấn đúng hai vòng
Với `k=2`:

`Delta s_2=8 pi`.

Suy ra:

`L_2=sqrt((8 pi)^2+3^2)=sqrt(64 pi^2+9)`.

### 5. Mỗi k là một lớp đường riêng
Các lớp:
- `k=0`: không quấn;
- `k=1`: một vòng;
- `k=2`: hai vòng;
- ...

không phải là cùng một điều kiện.

Trong **mỗi lớp k**, đường ngắn nhất là đoạn thẳng nối `A` với đúng bản sao `B_k`.

Nếu không ràng buộc số vòng, `k=0` là ngắn nhất toàn cục.

### 6. Công thức cho k vòng
Với `r=2`, mỗi vòng thêm:

`4 pi`

vào độ lệch ngang.

Vì vậy:

`Delta s_k=4 pi k`.

Do đó:

`L_k=sqrt((4 pi k)^2+9)`.

Dạng tổng quát khi `A`, `B` cùng một đường sinh:

`L_k=sqrt((2 pi r k)^2+h^2)`.

### 7. k có dấu
Có thể cho `k` là số nguyên:
- `k>0`: quấn theo một chiều;
- `k<0`: quấn theo chiều ngược lại.

Khi `A` và `B` cùng một đường sinh:

`L_-k=L_k`.

Hai hướng quấn đối xứng.

### 8. Hai điểm không cùng đường sinh
Giả sử từ đường sinh qua `A` tới đường sinh qua `B` có góc lệch ban đầu `delta`.

Nếu đường đi có số vòng đại số `k`, tổng góc quay là:

`Delta theta_k=delta+2 pi k`.

Độ lệch ngang trên dải phẳng:

`Delta s_k=r(delta+2 pi k)`.

Vì vậy:

`L_k=sqrt((r(delta+2 pi k))^2+h^2)`.

### 9. Tìm đường ngắn nhất toàn cục
Nếu đề bài không cho trước `k`, xét tất cả các ảnh `B_k`.

Chọn `k` làm cho:

`|delta+2 pi k|`

nhỏ nhất.

Ảnh tương ứng gần `A` nhất theo phương ngang, nên cho đường ngắn nhất toàn cục.

### 10. Trường hợp đối diện
Nếu:

`delta=pi`

thì hai ảnh:
- `k=0`;
- `k=-1`;

cách `A` theo phương ngang như nhau.

Do đó:

`L_0=L_-1`.

Trên hình trụ ta được hai đường xoắn đối xứng cùng ngắn nhất.

### Ý chính
Mỗi lần quấn thêm một vòng tương ứng với việc đi sang thêm một bản sao của hình chữ nhật khai triển.

Bài toán đường xoắn nhiều vòng trên hình trụ vì vậy biến thành bài toán nối thẳng tới đúng bản sao của điểm đích.
