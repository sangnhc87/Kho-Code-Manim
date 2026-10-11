# INT15 – Độ dời và quãng đường: Tích phân của vận tốc, gia tốc

> Sinh tự động từ `int15/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int15`.

**Số nhịp:** 23 · **Số công thức Typst:** 43 · **Từ:** 1224

## Mở đầu

### ⏱ Mở đầu: cách chỗ cũ 4/3 m nhưng đã đi 4 m

**`h1`** — Một chất điểm chuyển động trên đường thẳng với vận tốc v bằng t bình phương trừ bốn t cộng ba, mét trên giây. Sau bốn giây, nó chỉ cách vị trí ban đầu bốn phần ba mét. Nhưng tổng quãng đường nó đã đi lại là bốn mét, gấp ba lần! Chuyện gì đã xảy ra?

**`h2`** — Đây là tập mười lăm của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: tích phân, độ dời và quãng đường.

**`h3`** — Sau video này, em sẽ phân biệt rõ ba điều. Một, tích phân của vận tốc là độ dời. Hai, tích phân của trị tuyệt đối vận tốc là quãng đường. Ba, tích phân của gia tốc là độ thay đổi vận tốc.

## Bản chất

### ⏱ Tích phân của vận tốc là độ dời

**`c1`** — Gọi s của t là tọa độ của chất điểm. Vận tốc là đạo hàm của tọa độ, nên s là một nguyên hàm của v. Theo công thức Newton Leibniz, tích phân từ a đến b của v bằng s của b trừ s của a: đó là độ dời, tức là vị trí cuối trừ vị trí đầu.

**`c2`** — Hãy xem chất điểm ở bài mở đầu chạy. Từ không đến một giây, v dương, nó tiến lên bốn phần ba mét. Từ một đến ba giây, v âm, nó quay đầu lùi lại bốn phần ba mét, về đúng chỗ cũ. Từ ba đến bốn giây, nó lại tiến bốn phần ba mét.

**`c2b`** — Nhìn lại đồ thị tọa độ s của t: nó đi lên, rồi đi xuống, rồi lại đi lên. Những thời điểm chất điểm đổi chiều, t bằng một và t bằng ba, chính là các điểm cực trị của s, nơi đạo hàm v bằng không và đổi dấu. Vậy muốn tìm lúc đổi chiều, ta giải v bằng không và kiểm tra v có đổi dấu hay không.

### ⏱ Quãng đường: tích phân của |v|

**`c3`** — Trên đồ thị vận tốc, phần nằm dưới trục ứng với lúc chạy lùi. Tích phân của v là diện tích có dấu, nên phần lùi bị trừ đi: độ dời bằng bốn phần ba. Quãng đường thì đếm mọi mét đã đi, nên ta lật phần âm lên: quãng đường là tích phân của trị tuyệt đối v, bằng bốn.

**`c4`** — Như vậy, khi vận tốc không đổi dấu, độ dời và quãng đường có độ lớn bằng nhau. Khi vận tốc đổi dấu, tức là chất điểm đổi chiều, ta phải dùng đúng quy trình của tập mười bốn: giải v bằng không, xét dấu, rồi tách cận.

### ⏱ Gia tốc và vận tốc

**`c5`** — Cùng ý tưởng cho gia tốc. Gia tốc là đạo hàm của vận tốc, nên tích phân của a từ t một đến t hai bằng v của t hai trừ v của t một. Muốn biết vận tốc tại thời điểm t, ta lấy vận tốc ban đầu cộng tích phân của gia tốc.

**`c6`** — Một mẹo kiểm tra nhanh bằng đơn vị: diện tích dưới đồ thị vận tốc theo thời gian có đơn vị mét trên giây nhân giây, tức là mét. Diện tích dưới đồ thị gia tốc có đơn vị mét trên giây. Nếu đơn vị không khớp với câu hỏi, em đã chọn sai hàm để lấy tích phân.

## Ví dụ

### ⏱ Ví dụ 1: độ dời và quãng đường

**`e1`** — Ví dụ một, hoàn thành bài mở đầu. Giải t bình phương trừ bốn t cộng ba bằng không, được t bằng một và t bằng ba. Xét dấu: dương, âm, dương. Ba tích phân lần lượt là bốn phần ba, âm bốn phần ba và bốn phần ba. Độ dời là tổng có dấu, bằng bốn phần ba. Quãng đường là tổng độ lớn, bằng bốn.

### ⏱ Ví dụ 2: từ gia tốc đến quãng đường

**`e2`** — Ví dụ hai: một vật xuất phát từ trạng thái nghỉ với gia tốc a bằng sáu trừ hai t. Vận tốc bằng không cộng tích phân của gia tốc, được v bằng sáu t trừ t bình phương. Vật dừng lại khi t bằng sáu giây, và trong khoảng đó v không âm.

**`e3`** — Vậy quãng đường vật đi được cho đến khi dừng là tích phân từ không đến sáu của sáu t trừ t bình phương, bằng một trăm lẻ tám trừ bảy mươi hai, bằng ba mươi sáu mét.

**`e3b`** — Đề thi còn hay hỏi thêm hai ý. Vận tốc lớn nhất đạt được khi gia tốc bằng không, tức là t bằng ba, khi đó v bằng chín mét trên giây. Còn tốc độ trung bình bằng quãng đường chia thời gian: ba mươi sáu chia sáu, bằng sáu mét trên giây. Chú ý: tốc độ trung bình không phải trung bình cộng của các vận tốc.

### ⏱ Ví dụ 3: đọc đồ thị vận tốc

**`e4`** — Ví dụ ba: đọc đồ thị. Một ô tô tăng tốc đều từ không lên mười mét trên giây trong bốn giây, chạy đều sáu giây, rồi phanh dừng hẳn trong hai giây. Quãng đường là diện tích hình thang dưới đồ thị: hai mươi cộng sáu mươi cộng mười, bằng chín mươi mét. Không cần viết công thức của v!

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Một chất điểm có vận tốc v bằng ba t bình phương trừ sáu t, mét trên giây, với t từ không đến ba giây. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: tích phân từ không đến ba của ba t bình phương trừ sáu t bằng hai mươi bảy trừ hai mươi bảy, bằng không. Chất điểm quay về đúng chỗ xuất phát. Ý b sai: độ dời bằng không nhưng quãng đường thì không.

**`x3`** — Ý c đúng: v âm trên khoảng từ không đến hai và dương sau đó, nên chất điểm đổi chiều tại t bằng hai. Ý d sai: gia tốc là sáu t trừ sáu, tại t bằng hai gia tốc bằng sáu. Đừng nhầm: vận tốc bằng không không có nghĩa là gia tốc bằng không.

### ⏱ Câu trả lời ngắn: quãng đường phanh

**`x4`** — Câu trả lời ngắn. Một ô tô đang chạy với vận tốc mười lăm mét trên giây thì phanh, vận tốc sau đó là v bằng mười lăm trừ ba t. Hỏi từ lúc phanh đến khi dừng hẳn, ô tô đi thêm bao nhiêu mét?

**`x5`** — Ô tô dừng khi v bằng không, tức là t bằng năm giây. Quãng đường bằng tích phân từ không đến năm của mười lăm trừ ba t, bằng bảy mươi lăm trừ ba mươi bảy phẩy năm, bằng ba mươi bảy phẩy năm mét. Ghi vào phiếu: ba, bảy, phẩy, năm. Bẫy thường gặp là lấy cận trên tùy ý thay vì thời điểm dừng.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, độ dời bằng tích phân của v, là diện tích có dấu. Hai, quãng đường bằng tích phân của trị tuyệt đối v: xét dấu v, tách cận tại lúc đổi chiều. Ba, vận tốc bằng vận tốc ban đầu cộng tích phân của gia tốc.

**`o2`** — Bài tập tự luyện. Một, v bằng hai t trừ bốn, tính quãng đường trong năm giây đầu. Hai, a bằng bốn trừ hai t và vận tốc ban đầu bằng năm, tính vận tốc tại t bằng ba. Ba, ô tô phanh với v bằng mười hai trừ bốn t, tính quãng đường đến khi dừng. Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập mười sáu, ta học phương pháp đổi biến số trong tích phân, với nguyên tắc vàng: đổi biến thì phải đổi cận. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. v = 2t − 4, t ∈ [0; 5]: quãng đường? → **13**
2. a = 4 − 2t, v(0) = 5: v(3)? → **8**
3. v = 12 − 4t: quãng đường phanh? → **18**
