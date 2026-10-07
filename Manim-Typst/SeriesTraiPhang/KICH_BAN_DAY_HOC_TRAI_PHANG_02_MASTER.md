# KỊCH BẢN DẠY HỌC — TRẢI PHẲNG 02 MASTER
## Lập phương — đường đi qua đúng 4 mặt

### Mô hình
Lập phương cạnh `a`. Kiến bắt đầu ở đỉnh `A'`, kết thúc ở đỉnh `D'`.

Đường đi bị ràng buộc trong dải bốn mặt theo thứ tự:

`mặt trước → mặt phải → mặt đáy → mặt sau`.

Đây là bài toán cực tiểu **trong dải mặt đã cho**, không phải đường ngắn nhất tự do trên toàn bộ lập phương.

### Mục tiêu
Học sinh cần nhìn được:
1. Ba lần đổi mặt tương ứng với ba cạnh chung `BB'`, `BC`, `CD`.
2. Mở cả dải bốn mặt làm đường gấp thành một đoạn thẳng.
3. Từ bản trải, tính được
   `L = a sqrt(13)`.
4. Đọc ngược được ba điểm đổi mặt:
   `BX=a/3`, `BY=a/2`, `DZ=2a/3`.
5. Gấp lại và kiểm tra bốn đoạn thật sự nằm trên bốn mặt tương ứng.

### Lời giải
Trên bản trải, lấy `A'` làm điểm đầu và ảnh của `D'` làm điểm cuối.
Độ lệch theo hai phương vuông góc lần lượt là `3a` và `2a`.

Do đó:
`L = sqrt((3a)^2+(2a)^2) = a sqrt(13)`.

Đoạn thẳng cắt ba cạnh bản lề lần lượt tại:
- `X in BB'`, `BX=a/3`;
- `Y in BC`, `BY=a/2`;
- `Z in CD`, `DZ=2a/3`.

Khi gấp lại:
`A' → X → Y → Z → D'`
lần lượt nằm trên các mặt trước, phải, đáy, sau.
