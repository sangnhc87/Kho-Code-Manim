# KỊCH BẢN DẠY HỌC — TRẢI PHẲNG 11 MASTER
## Hình trụ — đường xoắn trở thành đường thẳng

### Mô hình
Cho hình trụ:
- bán kính `r=2`;
- chiều cao `h=3`.

Điểm `A` nằm trên vành dưới.
Điểm `B` nằm trên vành trên.

Hai đường sinh qua `A` và `B` đối diện nhau qua trục.

Kiến chỉ được đi trên **mặt xung quanh** của hình trụ.

### 1. Đường thẳng trong không gian không hợp lệ
Nếu nối thẳng `A` với `B` trong không gian:
- độ lệch ngang là đường kính `4`;
- độ lệch đứng là `3`.

Do đó:

`AB=5`.

Nhưng đoạn này xuyên qua lòng hình trụ, nên không phải đường đi trên bề mặt.

### 2. Đường hợp lệ trên mặt trụ
Có hai hướng nửa vòng đối xứng quanh trụ.

Đường tối ưu trên trụ có dạng một đường xoắn.
Ta chỉ cần xét một hướng.

### 3. Cắt theo đường sinh qua A
Cắt mặt xung quanh theo đường sinh qua `A`.

Chu vi đáy:

`2 pi r = 4 pi`.

Khi khai triển:
- chiều cao hình chữ nhật vẫn là `3`;
- chiều dài hình chữ nhật là `4 pi`.

### 4. A và B trên bản khai triển
Vì đường sinh qua `B` đối diện đường sinh qua `A`, khoảng cách theo phương ngang giữa `A` và ảnh của `B` là nửa chu vi:

`pi r = 2 pi`.

Độ lệch đứng:

`3`.

### 5. Độ dài nhỏ nhất
Trên bản khai triển, đường ngắn nhất là đoạn thẳng:

`L^2=(2 pi)^2+3^2`.

Do đó:

`L_min=sqrt(4 pi^2+9)`.

### 6. Vì sao có hai đường ngắn nhất?
Khi cắt theo đường sinh qua `A`, điểm `A` xuất hiện ở cả hai mép đứng của hình chữ nhật.

Điểm `B` nằm đúng giữa mép trên.

Hai đoạn nối `B` với hai bản sao của `A` có cùng độ dài.

Khi cuộn hình chữ nhật lại, chúng trở thành hai đường xoắn đối xứng trên mặt trụ.

### 7. Công thức tổng quát theo góc
Giả sử góc nhỏ hơn giữa hai đường sinh là `delta`, với:

`0<=delta<=pi`.

Độ dài cung tương ứng trên đường tròn:

`s=r delta`.

Sau khi khai triển, đây chính là độ lệch ngang.

Vì vậy:

`L_min=sqrt((r delta)^2+h^2)`.

### 8. Phương trình đường xoắn của bài cụ thể
Với `r=2`, `h=3`, đường đi nửa vòng có thể viết:

`0<=theta<=pi`

`x=2 cos theta`

`y=2 sin theta`

`z=3 theta/pi`.

Độ cao tăng tuyến tính theo góc quay.

### 9. Ý nghĩa hình học
Khai triển mặt trụ giữ nguyên độ dài đo trên bề mặt.

Mọi đường hợp lệ trên trụ trở thành một đường trong hình chữ nhật.

Giữa hai điểm trên mặt phẳng, đoạn thẳng là ngắn nhất.

Vì vậy khi cuộn đoạn thẳng đó lại, ta thu được đường xoắn ngắn nhất trên mặt trụ.

### 10. Cầu nối sang Video 12
Video 11 chỉ xét đường đi theo hướng ngắn nhất quanh trụ.

Video 12 sẽ cho đường đi **quấn thêm k vòng**.
Khi ấy điểm đích có nhiều ảnh trên các bản sao liên tiếp của hình chữ nhật.
