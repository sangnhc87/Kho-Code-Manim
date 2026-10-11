# INT06 – Nguyên hàm có điều kiện: Tìm C, nguyên hàm hai lần & hàm từng khúc

> Sinh tự động từ `int06/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int06`.

**Số nhịp:** 23 · **Số công thức Typst:** 43 · **Từ:** 1286

## Mở đầu

### ⏱ Mở đầu: vận tốc cho theo từng khúc

**`h1`** — Một chiếc xe xuất phát và tăng tốc đều trong ba giây đầu, sau đó giữ nguyên vận tốc sáu mét mỗi giây. Vận tốc được cho bởi hai công thức khác nhau trên hai khoảng thời gian. Muốn biết vị trí của xe, ta phải lấy nguyên hàm của một hàm số cho theo từng khúc, rồi nối các mảnh lại sao cho chiếc xe không bị dịch chuyển tức thời.

**`h2`** — Đây là tập sáu của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: nguyên hàm có điều kiện, nguyên hàm hai lần và hàm số cho theo từng khúc.

**`h3`** — Sau video này, em sẽ thành thạo ba dạng. Một, dùng một hoặc nhiều điều kiện để tìm hằng số C. Hai, lấy nguyên hàm hai lần, từ gia tốc ra vận tốc rồi ra vị trí. Ba, hàm từng khúc: mỗi khúc một hằng số, và hàn các khúc lại bằng tính liên tục.

## Bản chất

### ⏱ Dạng 1: điều kiện xác định C

**`c1`** — Nhắc lại dạng quen thuộc nhất: biết F phẩy bằng f và một giá trị F của x không bằng y không. Ta tìm họ nguyên hàm, rồi thay điều kiện vào để tìm C. Về hình học, điều kiện chọn ra đúng một đường cong trong cả họ, đường đi qua điểm x không, y không.

**`c2`** — Điều kiện không nhất thiết là một giá trị đơn lẻ. Ví dụ, F là nguyên hàm của hai x cộng một, và F của một cộng F của hai bằng mười. Ta có F bằng x bình phương cộng x cộng C. Thay vào: hai cộng C, cộng sáu cộng C, bằng mười. Vậy C bằng một. Chỉ cần đếm đúng: mỗi lần thay là một chữ C.

### ⏱ Dạng 2: nguyên hàm hai lần

**`c3`** — Dạng hai: nguyên hàm hai lần. Biết đạo hàm cấp hai của f bằng sáu x, f phẩy của không bằng hai và f của không bằng một. Lấy nguyên hàm lần thứ nhất: f phẩy bằng ba x bình phương cộng C một, điều kiện cho C một bằng hai. Lấy nguyên hàm lần thứ hai: f bằng x lập phương cộng hai x cộng C hai, và C hai bằng một.

**`c4`** — Ý nghĩa vật lý: từ gia tốc, nguyên hàm một lần ra vận tốc, nguyên hàm thêm lần nữa ra vị trí. Mỗi lần lấy nguyên hàm sinh ra một hằng số mới, nên cần đúng hai điều kiện: vận tốc ban đầu và vị trí ban đầu. Thiếu một điều kiện là không xác định được hàm số.

### ⏱ Dạng 3: hàm số cho theo từng khúc

**`c5`** — Dạng ba, quan trọng nhất: hàm số cho theo từng khúc. Xét f của x bằng hai x khi x lớn hơn hoặc bằng một, và bằng hai khi x nhỏ hơn một. Tại x bằng một, hai công thức cho cùng giá trị hai, nên f liên tục, đồ thị chỉ gãy góc chứ không đứt.

**`c6`** — Lấy nguyên hàm trên từng khúc. Với x lớn hơn hoặc bằng một: x bình phương cộng C một. Với x nhỏ hơn một: hai x cộng C hai. Hai khúc có hai hằng số khác nhau. Nếu chọn tùy ý, hai mảnh đồ thị của F sẽ bị lệch nhau tại x bằng một.

### ⏱ Hàn các khúc bằng tính liên tục

**`c7`** — Nhưng F có đạo hàm tại mọi điểm, nên F phải liên tục. Hai mảnh phải hàn khít tại x bằng một: một cộng C một bằng hai cộng C hai. Trên hình, ta kéo mảnh bên phải cho tới khi khớp với mảnh bên trái. Đây chính là bước mà nhiều bạn bỏ quên.

**`c8`** — Bây giờ thêm điều kiện F của không bằng một. Điểm không thuộc khúc bên trái, nên C hai bằng một. Từ phương trình hàn, C một bằng hai. Vậy F bằng x bình phương cộng hai khi x lớn hơn hoặc bằng một, và bằng hai x cộng một khi x nhỏ hơn một. Chẳng hạn F của hai bằng sáu.

**`c9`** — Lưu ý chuyên sâu: nếu f bị đứt quãng, tức có bước nhảy, thì đạo hàm của F không thể nhảy giá trị như vậy, và f không có nguyên hàm trên cả trục số. Vì thế đề thi luôn cho f liên tục tại điểm nối. Em hãy kiểm tra điều đó trước khi giải.

## Ví dụ

### ⏱ Ví dụ 1: chiếc xe tăng tốc rồi chạy đều

**`e1`** — Quay lại chiếc xe ở đầu bài: v của t bằng hai t khi t từ không đến ba, và bằng sáu khi t lớn hơn ba. Vị trí ban đầu bằng không. Trên khúc đầu, s bằng t bình phương. Trên khúc sau, s bằng sáu t cộng C. Hàn tại t bằng ba: chín bằng mười tám cộng C, nên C bằng âm chín.

**`e2`** — Vậy sau năm giây, s bằng sáu nhân năm trừ chín, bằng hai mươi mốt mét. Hãy quan sát: đồ thị vị trí cong trong ba giây đầu, rồi chuyển mượt thành đường thẳng, không có bước nhảy nào.

### ⏱ Ví dụ 2: nguyên hàm của |x|

**`e3`** — Ví dụ hai, chuyên sâu: nguyên hàm của trị tuyệt đối x. Khi x không âm, được x bình phương chia hai cộng C một. Khi x âm, được âm x bình phương chia hai cộng C hai. Hàn tại không cho C một bằng C hai. Kết quả viết gọn: x nhân trị tuyệt đối x, chia hai, cộng C.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Cho hàm số f bằng ba x bình phương khi x lớn hơn hoặc bằng một, và bằng ba khi x nhỏ hơn một. F là nguyên hàm của f trên R và F của không bằng hai. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: điểm không thuộc khúc bên trái, F bằng ba x cộng C hai, và C hai bằng hai. Ý b sai: hàn tại một cho một cộng C một bằng ba cộng hai, tức C một bằng bốn, không phải hai.

**`x3`** — Ý c đúng: F của hai bằng tám cộng bốn, bằng mười hai. Ý d đúng: âm một thuộc khúc bên trái, F của âm một bằng âm ba cộng hai, bằng âm một.

### ⏱ Trả lời ngắn và quy trình 3 bước

**`x4`** — Câu trả lời ngắn. F là nguyên hàm của hàm số bằng hai x cộng một khi x không âm, bằng e mũ x khi x âm, và F của không bằng một. Tính F của hai cộng F của âm lô ga nê pe hai. Khúc phải: x bình phương cộng x cộng một. Hàn tại không: một cộng C hai bằng một, nên C hai bằng không. Vậy kết quả là bảy cộng một phần hai, bằng bảy phẩy năm.

**`x5`** — Quy trình ba bước cho hàm từng khúc. Bước một, lấy nguyên hàm từng khúc, mỗi khúc một hằng số riêng. Bước hai, hàn tại điểm nối bằng tính liên tục. Bước ba, dùng điều kiện đề cho, và nhớ xem điểm đó thuộc khúc nào.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, mỗi điều kiện cho một phương trình của C. Hai, nguyên hàm hai lần cần hai hằng số và hai điều kiện. Ba, hàm từng khúc: mỗi khúc một C, hàn bằng tính liên tục, rồi mới dùng điều kiện.

**`o2`** — Bài tập tự luyện. Một, F phẩy bằng bốn x lập phương trừ một, F của một cộng F của âm một bằng bốn, tìm F. Hai, đạo hàm cấp hai của f bằng mười hai x bình phương, f phẩy của một bằng năm, f của một bằng hai, tính f của hai. Ba, f bằng hai x khi x lớn hơn hoặc bằng hai, bằng bốn khi x nhỏ hơn hai, F của không bằng không, tính F của ba.

**`o3`** — Ở tập bảy, ta sẽ học cách tìm nguyên hàm của phân thức hữu tỉ: chia đa thức và tách phân thức. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. F'(x) = 4x³ − 1, F(1) + F(−1) = 4. Tìm F. → **F(x) = x⁴ − x + 1**
2. f''(x) = 12x², f'(1) = 5, f(1) = 2. Tính f(2). → **f(2) = 18**
3. f(x) = 2x (x ≥ 2), 4 (x < 2); F(0) = 0. Tính F(3). → **F(3) = 13**
