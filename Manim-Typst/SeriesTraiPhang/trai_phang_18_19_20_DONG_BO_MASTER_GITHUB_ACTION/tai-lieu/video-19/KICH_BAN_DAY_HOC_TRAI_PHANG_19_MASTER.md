# KỊCH BẢN DẠY HỌC — TRẢI PHẲNG 19 MASTER
## Hộp chữ nhật có tham số – điểm chuyển của phương án tối ưu

### Bài toán

Cho hình hộp chữ nhật `ABCD.EFGH` có:
- `AB=4`;
- `BC=6`;
- `AE=t`, với `2 ≤ t ≤ 10`.

Kiến xuất phát từ đỉnh `A` đến đỉnh đối diện `G` nhưng chỉ được đi trên **mặt ngoài** của hộp. Tìm độ dài ngắn nhất `L_min(t)` và mô tả đường đi tối ưu khi `t` thay đổi.

### 1. Tại sao cần nhiều bản khai triển?

Các mặt chứa A: mặt trước, mặt trái, mặt đáy.
Các mặt chứa G: mặt phải, mặt sau, mặt trên.

Một kiểu đường đi có thể đi từ một mặt chứa A sang một mặt chứa G qua cạnh chung, sau đó nối thẳng hai ảnh trên bản trải. Có ba kiểu kích thước hình chữ nhật:

| Kiểu | Dải mặt minh họa | Kích thước bản trải | Độ dài |
|---|---|---|---|
| I | Trái → Trên | `(t+4) × 6` | `sqrt((t+4)^2+36)` |
| II | Trước → Phải | `10 × t` | `sqrt(100+t^2)` |
| III | Đáy → Sau | `(t+6) × 4` | `sqrt((t+6)^2+16)` |

Do các đường đi ngắn nhất trong từng kiểu là đường chéo hợp lệ, ta có ba ứng viên thực sự. Các bản trải đối xứng khác có độ dài trùng với một trong ba ứng viên.

### 2. Mở kiểu I

Giữ mặt trái `AEHD`, mở mặt trên `EFGH` quanh cạnh `EH`. Hai mặt trở thành hình chữ nhật `(t+4) × 6`.

`L_I^2=(t+4)^2+6^2=(t+4)^2+36`.

Điểm chuyển trên `EH` là điểm có tọa độ theo chiều y kể từ E:

`EX=6t/(t+4)`.

Vì `0<t/(t+4)<1`, X luôn ở phần trong cạnh EH.

### 3. Mở kiểu II

Giữ mặt trước `ABFE`, mở mặt phải `BCGF` quanh cạnh `BF`. Hai mặt thành hình chữ nhật `10 × t`.

`L_II^2=10^2+t^2=100+t^2`.

Điểm chuyển nằm trên BF tại độ cao:

`BX=2t/5`.

Nên X nằm trong BF.

### 4. Kiểu III

Giữ mặt đáy `ABCD`, mở mặt sau `DCGH` quanh cạnh `DC`. Bản trải `(t+6) × 4`.

`L_III^2=(t+6)^2+16`.

### 5. Loại ứng viên không thắng

Không cần lấy căn:

`L_III^2-L_I^2=4t`.

Với `t>0`, hiệu này dương, nên III luôn dài hơn I. III không thể là đường ngắn nhất toàn cục.

### 6. Ngưỡng chuyển phương án

`L_I^2-L_II^2 = (t+4)^2+36-(100+t^2) = 8(t-6)`.

Suy ra:
- Nếu `2 ≤ t < 6`: I ngắn hơn II; đi theo dải trái → trên.
- Nếu `t=6`: I và II cùng ngắn nhất.
- Nếu `6 < t ≤ 10`: II ngắn hơn I; đi theo dải trước → phải.

Tại `t=6`:

`L_min = sqrt(136)=2sqrt(34)`.

### 7. Kết luận dưới dạng hàm số từng khoảng

`L_min(t) = sqrt((t+4)^2+36)` khi `2 ≤ t ≤ 6`.

`L_min(t) = sqrt(t^2+100)` khi `6 ≤ t ≤ 10`.

Các đoạn nối liên tục tại `t=6`, nhưng **phương án đi qua mặt nào thay đổi** khi qua ngưỡng này.

### 8. Chứng minh đã so đủ các dải mặt

Với hai đỉnh đối diện của hình hộp chữ nhật, ba kiểu kích thước bản trải ở trên là ba ứng viên kinh điển. Để kiểm tra kỹ trong mã:
- liệt kê mọi chuỗi mặt đơn, liền kề từ một mặt chứa A tới một mặt chứa G;
- trải bằng các phép quay cứng quanh cạnh chung;
- chỉ chấp nhận đoạn thẳng cắt các cạnh gấp ở phần trong và đúng thứ tự;
- đo lại chiều dài của đường trên hộp;
- đối chiếu kết quả tại 11 giá trị của t, bao gồm 5.9, 6 và 6.1.

Việc thử mẫu không thay thế chứng minh dấu của `8(t-6)`; dấu ấy mới giải thích chính xác vì sao xuất hiện ngưỡng.

### 9. Các cảnh animation quan trọng

1. Hình hộp 3D, điểm A xanh và G đỏ, t tăng giảm.
2. Mở thật mặt trên quanh EH cho kiểu I.
3. Hiển thị đường chéo bản trải I, đánh dấu vị trí giao EH.
4. Mở thật mặt phải quanh BF cho kiểu II.
5. Hiển thị đường chéo bản trải II.
6. So sánh ba biểu thức độ dài, loại III bằng `4t>0`.
7. Tại `t=6`, hiển thị hai đường gấp khác nhau cùng tối ưu.
8. Cho t chuyển động từ 2 đến 10; các đường và điểm chuyển mặt thay đổi cùng hộp.
9. Chốt công thức `L_min(t)` từng khoảng.

### Câu hỏi thảo luận

- Vì sao so sánh bình phương thuận lợi hơn so sánh trực tiếp các căn?
- Tại `t=6`, có duy nhất một đường đi ngắn nhất hay không?
- Phương án III có thể ngắn hơn II tại một vài giá trị t không? Nếu có thì vì sao vẫn có thể loại khỏi bài toán tối ưu?
- Khi hình hộp thay đổi chiều cao liên tục, độ dài tối ưu có bị nhảy đột ngột không?
