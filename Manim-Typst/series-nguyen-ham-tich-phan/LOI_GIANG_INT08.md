# INT08 – Phương pháp đổi biến số: Nhận diện u và du

> Sinh tự động từ `int08/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int08`.

**Số nhịp:** 24 · **Số công thức Typst:** 52 · **Từ:** 1337

## Mở đầu

### ⏱ Mở đầu: hai x là đạo hàm của x²

**`h1`** — Ở tập năm, ta biết quy tắc chia cho a chỉ dùng được khi bên trong là bậc nhất, nên nguyên hàm của e mũ x bình phương không làm được theo cách đó. Nhưng nếu đề cho hai x nhân e mũ x bình phương thì sao? Hãy để ý: hai x chính là đạo hàm của x bình phương. Sự xuất hiện của đạo hàm phần bên trong là chìa khóa của phương pháp đổi biến số.

**`h2`** — Đây là tập tám của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: phương pháp đổi biến số. Đây là nội dung mở rộng, rất hữu ích cho học sinh giỏi và các kỳ thi đánh giá năng lực.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, đổi biến chính là đạo hàm hàm hợp đọc ngược. Hai, quy trình bốn bước: chọn u, tính d u, đổi toàn bộ sang u, rồi trả về x. Ba, bảng nhận diện nhanh các dạng thường gặp và những bẫy cần tránh.

## Bản chất

### ⏱ Đạo hàm hàm hợp đọc ngược

**`c1`** — Nhắc lại đạo hàm hàm hợp: đạo hàm của F của u của x bằng f của u của x nhân u phẩy của x. Đọc ngược lại: nguyên hàm của f của u nhân u phẩy bằng F của u cộng C. Như vậy, khi thấy một hàm của u nhân với đạo hàm của u, ta lấy nguyên hàm theo u.

**`c2`** — Để viết gọn, ta dùng vi phân: d u bằng u phẩy của x nhân d x. Khi đó cả cụm f của u nhân u phẩy d x trở thành f của u d u, một nguyên hàm đơn giản theo biến mới u.

### ⏱ Ý nghĩa của du

**`c3`** — Ý nghĩa hình học của d u: hãy đặt trục x và trục u song song. Với u bằng x bình phương, một đoạn nhỏ độ dài d x trên trục x được ánh xạ thành đoạn d u trên trục u, dài gấp hai x lần. Hệ số co giãn đó chính là u phẩy, và nó phải có mặt trong biểu thức thì mới đổi biến được.

### ⏱ Quy trình 4 bước

**`c4`** — Quy trình bốn bước. Bước một, chọn u là phần bên trong, thường là phần mà đạo hàm của nó xuất hiện bên ngoài. Bước hai, tính d u. Bước ba, đổi toàn bộ biểu thức sang u, không để sót x nào. Bước bốn, tính nguyên hàm theo u rồi thay ngược u bằng biểu thức của x.

**`c5`** — Áp dụng cho bài mở đầu. Đặt u bằng x bình phương, thì d u bằng hai x d x. Biểu thức trở thành nguyên hàm của e mũ u d u, bằng e mũ u cộng C. Trả về biến x: e mũ x bình phương cộng C. Kiểm tra bằng đạo hàm: đúng bằng hai x e mũ x bình phương.

### ⏱ Sai khác hằng số vẫn đổi được

**`c6`** — Đạo hàm của u chỉ cần xuất hiện sai khác một hằng số. Ví dụ, nguyên hàm của x nhân x bình phương cộng một mũ năm. Đặt u bằng x bình phương cộng một, d u bằng hai x d x, nên x d x bằng d u chia hai. Kết quả là một phần hai nguyên hàm của u mũ năm, bằng x bình phương cộng một mũ sáu chia mười hai, cộng C.

**`c7`** — Với lượng giác: nguyên hàm của sin x nhân cốt lập phương x. Đặt u bằng cốt x, d u bằng âm sin x d x. Biểu thức trở thành âm nguyên hàm của u lập phương d u, bằng âm cốt mũ bốn x chia bốn, cộng C.

**`c8`** — Với lô ga rít: nguyên hàm của lô ga nê pe x chia x. Đặt u bằng lô ga nê pe x, d u bằng d x chia x. Kết quả là u bình phương chia hai, tức lô ga nê pe x tất cả bình phương chia hai, cộng C.

### ⏱ Bảng nhận diện nhanh

**`c9`** — Tổng hợp thành bảng nhận diện nhanh. Thấy x nhân một hàm của x bình phương: đặt u bằng x bình phương. Thấy e mũ một biểu thức nhân đạo hàm của nó: đặt u là số mũ. Thấy sin nhân lũy thừa của cốt, hoặc ngược lại: đặt u là hàm có lũy thừa. Thấy lô ga nê pe x chia x: đặt u bằng lô ga nê pe x.

### ⏱ Ba cái bẫy

**`c10`** — Ba cái bẫy hay gặp. Một, quên trả về biến x ở bước cuối. Hai, quên đổi d x, dẫn tới thiếu hệ số như một phần hai. Ba, chọn u mà đạo hàm của nó không có mặt trong biểu thức, khi đó phép đổi biến bế tắc.

## Ví dụ

### ⏱ Ví dụ 1–3

**`e1`** — Ví dụ một: nguyên hàm của e mũ x chia e mũ x cộng một. Đặt u bằng e mũ x cộng một, d u bằng e mũ x d x. Ta được nguyên hàm của d u chia u, bằng lô ga nê pe của e mũ x cộng một, cộng C. Không cần trị tuyệt đối vì biểu thức luôn dương.

**`e2`** — Ví dụ hai: nguyên hàm của x nhân căn x bình phương cộng ba. Đặt u bằng x bình phương cộng ba, x d x bằng d u chia hai. Được một phần hai nguyên hàm của u mũ một phần hai, bằng một phần ba nhân x bình phương cộng ba mũ ba phần hai, cộng C.

**`e3`** — Ví dụ ba: nguyên hàm của sin căn x chia căn x, với x dương. Đặt u bằng căn x, d u bằng d x chia hai căn x. Biểu thức trở thành hai nhân nguyên hàm của sin u d u, bằng âm hai cốt căn x, cộng C.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Cho hàm số f của x bằng x nhân e mũ x bình phương. F là một nguyên hàm của f trên R. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: đạo hàm của x bình phương là hai x. Ý b sai: đây là bẫy quên hệ số. Vì x d x bằng d u chia hai, kết quả phải có một phần hai đứng trước.

**`x3`** — Ý c đúng, chính là kết quả có hệ số một phần hai. Ý d đúng: F bằng một phần hai e mũ x bình phương cộng C, F của không bằng một phần hai cộng C bằng một nên C bằng một phần hai, và F của một bằng e cộng một, chia hai.

### ⏱ Trả lời ngắn và mẹo kiểm tra

**`x4`** — Câu trả lời ngắn. F là nguyên hàm của cốt x nhân sin bình phương x, F của không bằng không. Tính F của pi phần hai, làm tròn đến hàng phần trăm. Đặt u bằng sin x, d u bằng cốt x d x. F bằng sin lập phương x chia ba cộng C, và C bằng không. Vậy F của pi phần hai bằng một phần ba, xấp xỉ không phẩy ba ba.

**`x5`** — Mẹo kiểm tra nhanh: sau khi đổi biến, lấy đạo hàm kết quả theo x. Nếu ra đúng biểu thức ban đầu, kể cả hệ số, là chắc chắn đúng. Nếu lệch một hằng số như hai hay một phần hai, em đã quên đổi d x.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, đổi biến là đạo hàm hàm hợp đọc ngược: thấy hàm của u nhân u phẩy. Hai, quy trình bốn bước: chọn u, tính d u, đổi hết sang u, trả về x. Ba, đạo hàm của u chỉ cần xuất hiện sai khác hằng số, nhưng phải bù hằng số đó.

**`o2`** — Bài tập tự luyện. Một, nguyên hàm của ba x bình phương nhân x lập phương cộng một mũ bốn. Hai, nguyên hàm của cốt x chia sin x cộng hai. Ba, nguyên hàm của lô ga nê pe x bình phương chia x. Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập chín, ta học phương pháp nguyên hàm từng phần, dành cho tích của hai hàm khác loại như x nhân e mũ x. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. Tìm ∫3x²(x³ + 1)⁴ dx. → **(x³ + 1)⁵/5 + C**
2. Tìm ∫cos x/(sin x + 2) dx. → **ln(sin x + 2) + C**
3. Tìm ∫ln²x/x dx. → **ln³x/3 + C**
