# INT04 – Nguyên hàm lượng giác: Bảng cơ bản & kỹ thuật hạ bậc

> Sinh tự động từ `int04/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int04`.

**Số nhịp:** 27 · **Số công thức Typst:** 72 · **Từ:** 1476

## Mở đầu

### ⏱ Mở đầu: những gì dao động

**`h1`** — Mọi thứ dao động quanh ta, từ con lắc, chiếc lò xo đến dòng điện xoay chiều, đều được mô tả bằng hàm sin và hàm cốt. Khi biết vận tốc của một vật dao động, muốn tìm lại vị trí của nó, ta cần nguyên hàm của các hàm số lượng giác.

**`h2`** — Đây là tập bốn của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: nguyên hàm hàm số lượng giác, bảng cơ bản và kỹ thuật hạ bậc.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, bốn công thức nguyên hàm lượng giác cơ bản và dấu trừ dễ nhầm. Hai, ý nghĩa hình học: nguyên hàm làm sóng lệch pha một phần tư chu kỳ. Ba, kỹ thuật hạ bậc để tính nguyên hàm của sin bình phương và cốt bình phương.

## Bản chất

### ⏱ Nguyên hàm của sin và cốt

**`c1`** — Ta đọc ngược bảng đạo hàm. Đạo hàm của sin x là cốt x, nên nguyên hàm của cốt x là sin x cộng C. Đạo hàm của cốt x là âm sin x, nên đạo hàm của âm cốt x là sin x. Vậy nguyên hàm của sin x là âm cốt x cộng C.

**`c2`** — Lỗi sai phổ biến nhất là quên dấu trừ, viết nguyên hàm của sin x bằng cốt x. Hãy kiểm tra bằng hình: đường vàng là âm cốt x, đường xanh là sin x. Độ dốc của đường vàng luôn bằng chiều cao của đường xanh. Nếu bỏ dấu trừ, mọi độ dốc đều bị đảo dấu.

### ⏱ Bản chất: lệch pha một phần tư chu kỳ

**`c3`** — Có một cách nhìn rất đẹp. Đồ thị cốt x chính là đồ thị sin x dịch sang trái một phần tư chu kỳ, tức là pi phần hai. Lấy đạo hàm làm sóng dịch sang trái, nên lấy nguyên hàm làm sóng dịch sang phải pi phần hai. Dịch sin x sang phải pi phần hai, ta được đúng đường âm cốt x.

### ⏱ Nguyên hàm của 1/cos²x và 1/sin²x

**`c4`** — Tiếp theo là hai công thức với tang và cô tang. Đạo hàm của tang x bằng một chia cốt bình phương x, nên nguyên hàm của một chia cốt bình phương x là tang x cộng C. Đạo hàm của cô tang x bằng âm một chia sin bình phương x, nên nguyên hàm của một chia sin bình phương x là âm cô tang x cộng C.

**`c5`** — Lưu ý chuyên sâu: tang x chỉ xác định trên từng khoảng giữa hai đường tiệm cận đứng. Giống như với lô ga nê pe trị tuyệt đối x, trên mỗi khoảng ta có thể có một hằng số riêng. Đề thi thường cho sẵn một khoảng cụ thể, chẳng hạn từ âm pi phần hai đến pi phần hai.

### ⏱ Kỹ thuật hạ bậc

**`c6`** — Bây giờ là sin bình phương x. Nhiều bạn bắt chước quy tắc lũy thừa và viết sin lập phương chia ba. Lấy đạo hàm để kiểm tra: kết quả là sin bình phương nhân cốt x, không phải sin bình phương. Sai. Cách đúng là hạ bậc: sin bình phương x bằng một trừ cốt hai x, tất cả chia hai.

**`c7`** — Ta cần thêm nguyên hàm của cốt hai x. Theo đạo hàm hàm hợp ở lớp mười một, đạo hàm của sin hai x bằng hai cốt hai x. Vậy nguyên hàm của cốt hai x là sin hai x chia hai cộng C. Quy tắc tổng quát cho f của a x cộng b sẽ được xây dựng ở tập năm.

**`c8`** — Ghép lại: nguyên hàm của sin bình phương x bằng x chia hai trừ sin hai x chia bốn, cộng C. Hình bên trái xác nhận: độ dốc của đường vàng luôn bằng chiều cao của sin bình phương. Tương tự, nguyên hàm của cốt bình phương x là x chia hai cộng sin hai x chia bốn, cộng C.

**`c9`** — Một dạng hay gặp khác là tang bình phương x. Dùng hằng đẳng thức: tang bình phương bằng một chia cốt bình phương trừ một. Vậy nguyên hàm của tang bình phương x là tang x trừ x cộng C.

### ⏱ Bảng nguyên hàm lượng giác

**`c10`** — Tổng kết phần lý thuyết bằng bảng nguyên hàm lượng giác: bốn công thức cơ bản, cùng hai công thức hạ bậc cho sin bình phương và cốt bình phương.

## Ví dụ

### ⏱ Ví dụ 1: tổng hợp bảng cơ bản

**`e1`** — Ví dụ một: tìm nguyên hàm của hai sin x trừ ba cốt x cộng một chia cốt bình phương x. Tách từng hạng tử và nhớ dấu trừ của sin: kết quả là âm hai cốt x trừ ba sin x cộng tang x cộng C.

### ⏱ Ví dụ 2: dùng công thức lượng giác

**`e2`** — Ví dụ hai: nguyên hàm của sin x chia hai cộng cốt x chia hai, tất cả bình phương. Khai triển: sin bình phương cộng cốt bình phương bằng một, còn hai sin nhân cốt của x chia hai bằng sin x. Biểu thức trở thành một cộng sin x, có nguyên hàm x trừ cốt x cộng C.

### ⏱ Ví dụ 3–4: hạ bậc và góc nhân đôi

**`e5`** — Ví dụ ba: tìm nguyên hàm F của bốn sin bình phương x, biết F của không bằng một. Hạ bậc: bốn sin bình phương x bằng hai trừ hai cốt hai x. Nguyên hàm là hai x trừ sin hai x cộng C. Điều kiện F của không bằng một cho C bằng một, nên F của x bằng hai x trừ sin hai x cộng một.

**`e6`** — Ví dụ bốn: nguyên hàm của sin x nhân cốt x. Đây là một tích, không tách được. Nhưng sin x cốt x bằng một nửa sin hai x. Nguyên hàm của sin hai x là âm cốt hai x chia hai, nên kết quả là âm cốt hai x chia bốn cộng C.

### ⏱ Ví dụ 5: dao động của lò xo

**`e3`** — Ví dụ năm, dao động của lò xo. Một vật dao động trên trục ngang với vận tốc v của t bằng hai cốt t, đơn vị xăng ti mét mỗi giây. Lúc đầu vật ở vị trí một xăng ti mét. Tìm vị trí của vật tại t bằng pi phần hai.

**`e4`** — Vị trí là nguyên hàm của vận tốc: x của t bằng hai sin t cộng C. Điều kiện x của không bằng một cho C bằng một. Tại t bằng pi phần hai, x bằng hai cộng một, bằng ba xăng ti mét, đúng ở biên dao động. Hãy quan sát vật chạy đồng thời với điểm trên đồ thị.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Cho hàm số f của x bằng sin x cộng cốt x. Gọi F là một nguyên hàm của f trên R. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: nguyên hàm của sin là âm cốt, của cốt là sin. Ý b sai: đây là cái bẫy lũy thừa của hàm lượng giác. Đạo hàm của sin lập phương chia ba là sin bình phương nhân cốt x, phải dùng hạ bậc.

**`x3`** — Ý c đúng: F bằng sin x trừ cốt x cộng C, F của không bằng âm một cộng C bằng không nên C bằng một, và F của pi phần hai bằng một trừ không cộng một, bằng hai. Ý d sai: f bình phương bằng một cộng sin hai x, có nguyên hàm x trừ cốt hai x chia hai, dấu trừ chứ không phải dấu cộng.

### ⏱ Trả lời ngắn và mẹo máy tính

**`x4`** — Câu trả lời ngắn. Biết F là nguyên hàm của một chia cốt bình phương x trên khoảng từ âm pi phần hai đến pi phần hai, và F của pi phần tư bằng ba. Tính F của pi phần ba, làm tròn đến hàng phần trăm. F bằng tang x cộng C, một cộng C bằng ba nên C bằng hai. Vậy F của pi phần ba bằng căn ba cộng hai, xấp xỉ ba phẩy bảy ba.

**`x5`** — Mẹo thực chiến: khi kiểm tra nguyên hàm lượng giác bằng máy tính, nhất định phải chuyển sang chế độ ra đi an. Ví dụ, đạo hàm của âm cốt x tại x bằng một là xấp xỉ không phẩy tám bốn một, bằng đúng sin một. Ở chế độ độ, kết quả sẽ sai hoàn toàn.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, nguyên hàm của sin là âm cốt, của cốt là sin. Hai, nguyên hàm của một chia cốt bình phương là tang, của một chia sin bình phương là âm cô tang, xét trên từng khoảng. Ba, gặp sin bình phương hay cốt bình phương, hãy hạ bậc trước.

**`o2`** — Bài tập tự luyện. Một, tìm nguyên hàm của ba cốt x trừ một chia sin bình phương x. Hai, tìm nguyên hàm của cốt bình phương x. Ba, biết F phẩy bằng sin x và F của pi bằng ba, tính F của không. Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập năm, ta sẽ xây dựng quy tắc tổng quát cho nguyên hàm của f của a x cộng b, và hiểu vì sao luôn phải chia cho a. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. Tìm ∫(3cos x − 1/sin²x) dx. → **3 sin x + cot x + C**
2. Tìm ∫cos²x dx. → **x/2 + sin 2x/4 + C**
3. Biết F'(x) = sin x, F(π) = 3. Tính F(0). → **F(0) = 1**
