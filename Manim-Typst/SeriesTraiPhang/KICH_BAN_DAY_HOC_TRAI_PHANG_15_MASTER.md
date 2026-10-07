# KỊCH BẢN DẠY HỌC — TRẢI PHẲNG 15 MASTER
## Silo = hình trụ + hình nón — ghép hai phép khai triển

### Mô hình
Silo gồm:
- thân hình trụ bán kính `r=3`, cao `4`;
- mái hình nón cùng bán kính đáy `3`, cao `4`;
- đường sinh mái nón `l=5`.

Điểm:
- `A` nằm trên vành dưới của thân trụ;
- `M` là một điểm bảo trì **cố định** trên vòng nối giữa trụ và nón;
- `B` nằm trên mái nón.

Đường đi từ `A` tới `B` bắt buộc phải đi qua `M`.

### 1. Vị trí các điểm
Lấy đường sinh qua `A` làm mốc góc `0`.

Điểm `M` lệch `A`:

`Delta theta_cyl=2 pi/3`.

Từ phương của `M` tới đường sinh chứa `B`:

`Delta theta_cone=5 pi/6`.

Điểm `B` nằm giữa một đường sinh của mái:
- khoảng cách theo mặt nón từ đỉnh tới vành nối là `5`;
- từ đỉnh tới `B` là `5/2`.

### 2. Tại sao bài toán tách làm hai phần?
Vì `M` là điểm bắt buộc và đã cố định.

Mọi đường hợp lệ có dạng:

`A -> M -> B`.

Do đó:
- tối ưu đoạn `A -> M` trên hình trụ;
- tối ưu đoạn `M -> B` trên hình nón;
- rồi cộng hai độ dài.

### 3. Phần hình trụ
Trải mặt xung quanh hình trụ thành hình chữ nhật.

Độ lệch ngang:

`Delta s = r Delta theta`
`=3*(2 pi/3)`
`=2 pi`.

Độ lệch đứng:

`Delta z=4`.

Vì vậy:

`L_tru^2=(2 pi)^2+4^2`.

Suy ra:

`L_tru=2 sqrt(pi^2+4)`.

### 4. Phần hình nón
Mái nón có:
- bán kính `3`;
- đường sinh `5`.

Tỉ lệ đổi góc:

`r/l=3/5`.

Góc quanh trục từ `M` tới `B`:

`delta=5 pi/6`.

Trên hình quạt:

`alpha=(3/5)*(5 pi/6)=pi/2`.

Khoảng cách từ đỉnh hình quạt:
- `SM=5`;
- `SB=5/2`.

Do `angle MSB=pi/2`:

`L_non^2=5^2+(5/2)^2`.

Suy ra:

`L_non=5 sqrt(5)/2`.

### 5. Tổng độ dài
Vì M cố định:

`L_min=L_tru+L_non`.

Do đó:

`L_min=2 sqrt(pi^2+4)+5 sqrt(5)/2`.

### 6. Chứng minh tối ưu
Với mọi đường hợp lệ qua M:

`L_AM >= L_tru`

và:

`L_MB >= L_non`.

Cộng lại:

`L >= L_tru+L_non`.

Đường dựng bằng hai đoạn tối ưu đạt dấu bằng ở cả hai bất đẳng thức, nên là đường ngắn nhất qua M.

### 7. Hình dung trên silo
Trên thân trụ:
- đường tối ưu là một đường xoắn.

Tại M:
- đường đi chuyển từ mặt trụ sang mặt nón.

Trên mái nón:
- đường tối ưu là ảnh của một đoạn thẳng trên hình quạt.

### 8. Nếu M không cố định
Nếu M được phép chạy trên vòng nối thì hai phần không còn độc lập.

Khi M thay đổi:
- độ dài phần trụ thay đổi;
- độ dài phần nón cũng thay đổi.

Khi đó phải tối ưu:

`L(M)=L_tru(M)+L_non(M)`.

Đây là phiên bản nâng cao và là cầu nối tới các bài tham số cuối series.

### Ý chính
Một bài toán trên vật thể ghép có thể được xử lý bằng cách:
1. chia đường đi theo từng loại mặt;
2. khai triển mỗi mặt bằng mô hình thích hợp;
3. giữ đúng điểm chuyển mặt;
4. tối ưu từng phần nếu điểm chuyển đã cố định;
5. cộng các độ dài tối ưu.
