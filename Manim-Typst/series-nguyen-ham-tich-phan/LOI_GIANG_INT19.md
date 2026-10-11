# INT19 – Hàm ẩn từ phương trình vi phân: Dạng f'(x) = g(x)·h(f(x))

> Sinh tự động từ `int19/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int19`.

**Số nhịp:** 24 · **Số công thức Typst:** 42 · **Từ:** 1316

## Mở đầu

### ⏱ Mở đầu: biết đạo hàm liên hệ với chính f

**`h1`** — Hàm số f dương, có f phẩy của x bằng x nhân f của x, và f của không bằng một. Tính f của hai. Đề không cho công thức của f, chỉ cho một hệ thức giữa đạo hàm và chính hàm số. Vậy mà ta tìm được chính xác: f của hai bằng e bình phương.

**`h2`** — Đây là tập mười chín của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: hàm ẩn từ phương trình vi phân đơn giản.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, ý nghĩa hình học: trường hướng và đường cong đi qua một điểm. Hai, kỹ thuật tách biến: đưa mọi thứ chứa f về một vế. Ba, bốn dạng đạo hàm quen thuộc cần nhận ra ngay: l n f, một chia f, f bình phương và đạo hàm của tích.

## Bản chất

### ⏱ Trường hướng và điều kiện ban đầu

**`c1`** — Hệ thức f phẩy bằng x nhân f cho biết độ dốc của đồ thị tại mọi điểm. Vẽ một đoạn ngắn có độ dốc đó tại mỗi điểm, ta được trường hướng. Có vô số đường cong đi theo trường hướng này, nhưng chỉ có một đường đi qua điểm không, một. Điều kiện ban đầu chọn ra đúng một hàm.

### ⏱ Tách biến

**`c2`** — Kỹ thuật tách biến. Với f phẩy bằng g của x nhân h của f, chia hai vế cho h của f, ta được f phẩy chia h của f bằng g của x. Vế trái chỉ chứa f, vế phải chỉ chứa x. Lấy tích phân hai vế từ a đến b là xong.

**`c3`** — Vế trái thực chất là một phép đổi biến u bằng f của x, d u bằng f phẩy d x. Tích phân từ a đến b của f phẩy chia h của f, bằng tích phân từ f của a đến f của b của d u chia h của u. Đây chính là bài học đổi biến của tập mười sáu.

### ⏱ Bốn dạng cần nhận ra

**`c4`** — Dạng một, hay gặp nhất: f phẩy bằng g nhân f, với f dương. Khi đó f phẩy chia f chính là đạo hàm của l n f. Lấy tích phân: l n f của b trừ l n f của a bằng tích phân của g.

**`c5`** — Dạng hai: f phẩy bằng g nhân f bình phương. Chia cho f bình phương, vế trái là đạo hàm của trừ một chia f. Suy ra một chia f của a trừ một chia f của b bằng tích phân của g. Chú ý thứ tự trừ để khỏi sai dấu.

**`c6`** — Dạng ba: f nhân f phẩy bằng g. Vế trái là đạo hàm của f bình phương chia hai. Dạng bốn: x nhân f phẩy cộng f bằng g. Vế trái là đạo hàm của tích x nhân f. Nhận ra vế trái là đạo hàm của cái gì, đó là toàn bộ bí quyết.

**`c7`** — Một chi tiết hay bị bỏ qua: muốn chia cho f hay lấy l n f, cần f khác không hoặc f dương. Đề thi luôn cho điều kiện này, ví dụ f dương trên đoạn đang xét. Hãy đọc kỹ và dùng nó khi biến đổi.

## Ví dụ

### ⏱ Ví dụ 1: dạng ln f

**`e1`** — Ví dụ một, giải bài mở đầu. f phẩy chia f bằng x. Lấy tích phân từ không đến hai: l n f của hai trừ l n f của không bằng tích phân của x, bằng hai. Vì f của không bằng một, l n một bằng không, nên l n f của hai bằng hai, f của hai bằng e bình phương.

### ⏱ Ví dụ 2: dạng 1/f

**`e2`** — Ví dụ hai: f phẩy bằng hai x nhân f bình phương, f của không bằng trừ một. Tính f của một. Đạo hàm của trừ một chia f bằng hai x, nên trừ một chia f bằng x bình phương cộng C. Thay x bằng không: C bằng một. Vậy f bằng trừ một chia x bình phương cộng một, f của một bằng trừ một phần hai.

### ⏱ Ví dụ 3: dạng f²

**`e3`** — Ví dụ ba: f dương, f nhân f phẩy bằng x, f của không bằng một. Tính f của căn ba. Đạo hàm của f bình phương chia hai bằng x, nên f bình phương bằng x bình phương cộng C. Với f của không bằng một thì C bằng một. Vậy f của căn ba bằng căn bốn, bằng hai.

### ⏱ Ví dụ 4: đạo hàm của tích

**`e4`** — Ví dụ bốn: x nhân f phẩy cộng f bằng ba x bình phương, f của một bằng hai. Tính f của hai. Vế trái là đạo hàm của x nhân f. Lấy nguyên hàm: x nhân f bằng x lập phương cộng C. Tại x bằng một: hai bằng một cộng C, C bằng một. Vậy f của hai bằng tám cộng một, chia hai, bằng chín phần hai.

**`e5`** — Khi đã tìm được f, đề có thể hỏi tiếp tích phân. Ở ví dụ bốn, f bằng x bình phương cộng một chia x. Tích phân từ một đến hai của f bằng bảy phần ba cộng l n hai. Câu hỏi nhiều bước như vậy rất phổ biến trong phần trả lời ngắn.

**`e6`** — Mẹo kiểm tra: sau khi tìm được f, hãy thay ngược lại vào hệ thức đề cho và kiểm tra điều kiện ban đầu. Ví dụ f bằng e mũ x bình phương phần hai: đạo hàm là x nhân e mũ x bình phương phần hai, đúng bằng x nhân f, và f của không bằng một. Chỉ mất mười giây mà tránh được sai sót.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Hàm số f dương, f phẩy của x bằng hai x cộng một, nhân f của x, và f của không bằng một. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: vì f dương nên đạo hàm của l n f bằng f phẩy chia f, bằng hai x cộng một. Ý b đúng: l n f bằng x bình phương cộng x cộng C, và C bằng không vì f của không bằng một.

**`x3`** — Ý c sai: f của một bằng e mũ hai, không phải e. Ý d đúng: tích phân từ không đến một của f phẩy chia f bằng l n f của một trừ l n f của không, bằng hai.

### ⏱ Câu trả lời ngắn

**`x4`** — Câu trả lời ngắn: hàm số f thỏa f phẩy bằng x nhân f bình phương và f của không bằng một phần hai. Tính f của một, làm tròn đến hàng phần trăm. Đây là dạng hai: đạo hàm của trừ một chia f bằng x.

**`x5`** — Trừ một chia f bằng x bình phương phần hai cộng C. Thay x bằng không: trừ hai bằng C. Vậy f bằng hai chia bốn trừ x bình phương, f của một bằng hai phần ba, xấp xỉ không phẩy sáu bảy. Ghi vào phiếu: không, phẩy, sáu, bảy.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, hệ thức giữa f phẩy và f cho một trường hướng, điều kiện ban đầu chọn ra một hàm duy nhất. Hai, tách biến: f phẩy chia h của f bằng g của x, rồi lấy tích phân hai vế. Ba, nhận ra vế trái là đạo hàm của l n f, của trừ một chia f, của f bình phương phần hai, hay của x nhân f.

**`o2`** — Bài tập tự luyện. Một, f dương, f phẩy bằng ba x bình phương nhân f, f của không bằng hai, tính f của một. Hai, f dương, f nhân f phẩy bằng hai x, f của không bằng ba, tính f của hai. Ba, x nhân f phẩy cộng f bằng hai x, f của một bằng ba, tính f của hai. Đáp số hiện ở cuối màn hình.

**`o3`** — Tập hai mươi là tập tổng ôn phần tích phân, với một mini đề gồm đủ ba dạng câu hỏi: trắc nghiệm, đúng sai và trả lời ngắn. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. f' = 3x²f, f(0) = 2: f(1)? → **2e**
2. f·f' = 2x, f(0) = 3: f(2)? → **√17**
3. x f' + f = 2x, f(1) = 3: f(2)? → **3**
