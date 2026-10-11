# INT12 – Định nghĩa tích phân: Newton–Leibniz & diện tích có dấu

> Sinh tự động từ `int12/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int12`.

**Số nhịp:** 24 · **Số công thức Typst:** 40 · **Từ:** 1224

## Mở đầu

### ⏱ Mở đầu: từ phát hiện đến định nghĩa

**`h1`** — Ở tập trước, ta phát hiện diện tích dưới đường x bình phương trên đoạn từ không đến hai bằng hiệu giá trị của nguyên hàm tại hai đầu mút. Liệu đó có phải trùng hợp? Và nếu đồ thị chui xuống dưới trục hoành, diện tích có còn dương không? Hôm nay ta biến phát hiện ấy thành một định nghĩa chính xác.

**`h2`** — Đây là tập mười hai của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: định nghĩa tích phân, công thức Newton Leibniz và diện tích có dấu.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, định nghĩa tích phân bằng hiệu F của b trừ F của a. Hai, vì sao kết quả không phụ thuộc vào hằng số C hay tên biến. Ba, ý nghĩa diện tích có dấu, và vì sao tích phân có thể âm hoặc bằng không.

## Bản chất

### ⏱ Định nghĩa và công thức Newton–Leibniz

**`c1`** — Định nghĩa. Cho hàm số f liên tục trên đoạn từ a đến b, và F là một nguyên hàm của f trên đoạn đó. Hiệu F của b trừ F của a được gọi là tích phân từ a đến b của f, kí hiệu tích phân từ a đến b của f của x d x. Ta còn viết gọn là F của x, lấy cận từ a đến b. Đây chính là công thức Newton Leibniz.

**`c2`** — Vì sao không phải lo chọn nguyên hàm nào? Nếu thay F bằng F cộng C, hiệu tại hai đầu mút là F của b cộng C trừ F của a trừ C, và hai chữ C triệt tiêu. Vì thế khi tính tích phân, ta chọn nguyên hàm đơn giản nhất, không cần viết C.

**`c3`** — Tích phân cũng không phụ thuộc tên biến. Tích phân từ a đến b của f của x d x bằng tích phân của f của t d t, hay của f của u d u. Biến lấy tích phân chỉ là một biến câm, kết quả là một con số.

### ⏱ Ba ví dụ nhanh

**`c4`** — Ba ví dụ nhanh. Tích phân từ một đến hai của ba x bình phương bằng x lập phương lấy cận, bằng tám trừ một, bằng bảy. Tích phân từ không đến pi của sin x bằng âm cốt x lấy cận, bằng một cộng một, bằng hai. Tích phân từ một đến e của một chia x bằng lô ga nê pe x lấy cận, bằng một.

### ⏱ Diện tích có dấu

**`c5`** — Bây giờ là điểm tinh tế. Xét sin x trên đoạn từ không đến hai pi. Phần đồ thị phía trên trục hoành cho diện tích dương bằng hai, phần phía dưới cho phần mang dấu âm, bằng âm hai. Tích phân cộng hai phần lại: hai trừ hai, bằng không.

**`c6`** — Như vậy tích phân là diện tích có dấu: phần trên trục hoành tính dương, phần dưới tính âm. Khi hàm số không đổi dấu và dương, tích phân đúng bằng diện tích. Khi hàm đổi dấu, tích phân khác diện tích, và ta sẽ xử lý bằng trị tuyệt đối ở các tập sau.

**`c7`** — Ý nghĩa vật lý giúp nhớ lâu. Tích phân của vận tốc theo thời gian là độ dời, có dấu: tiến thì dương, lùi thì âm. Còn quãng đường đi được luôn dương, là tích phân của trị tuyệt đối vận tốc. Chủ đề này sẽ được đào sâu ở tập mười lăm.

### ⏱ Hai quy ước về cận

**`c8`** — Hai quy ước cần nhớ. Tích phân từ a đến a bằng không, vì không có đoạn nào để cộng. Và đổi chỗ hai cận thì tích phân đổi dấu: tích phân từ b đến a bằng âm tích phân từ a đến b.

### ⏱ Nguyên hàm khác tích phân

**`c9`** — Phân biệt thật rõ hai khái niệm. Nguyên hàm là cả một họ hàm số, viết có cộng C. Tích phân từ a đến b là một con số cụ thể, không có C. Viết tích phân bằng x lập phương cộng C là một lỗi trình bày rất hay gặp, và có thể bị trừ điểm.

## Ví dụ

### ⏱ Ví dụ 1–3

**`e1`** — Ví dụ một: tích phân từ không đến một của e mũ x cộng hai x. Nguyên hàm là e mũ x cộng x bình phương. Lấy cận: e cộng một, trừ một cộng không, bằng e.

**`e2`** — Ví dụ hai: tích phân từ không đến pi phần hai của cốt hai x. Nguyên hàm là sin hai x chia hai. Tại pi phần hai, sin pi bằng không; tại không cũng bằng không. Kết quả bằng không, dù hàm số không hề bằng không: phần dương và phần âm bù trừ nhau đúng như trên hình.

**`e3`** — Ví dụ ba: tích phân từ một đến bốn của một chia căn x. Nguyên hàm là hai căn x. Lấy cận: hai nhân hai, trừ hai nhân một, bằng hai.

### ⏱ Ví dụ 4: đổi dấu và bằng không

**`e4`** — Ví dụ bốn: tích phân từ âm một đến hai của x bình phương trừ một. Nguyên hàm là x lập phương chia ba trừ x. Tại hai được hai phần ba, tại âm một cũng được hai phần ba. Kết quả bằng không! Trên hình, phần âm từ âm một đến một và phần dương từ một đến hai có cùng độ lớn bốn phần ba, nên triệt tiêu nhau.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Cho f của x bằng hai x trừ hai trên đoạn từ không đến ba. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: nguyên hàm x bình phương trừ hai x, lấy cận từ không đến ba được chín trừ sáu, bằng ba. Ý b đúng: trên đoạn từ không đến một, hàm số âm, tích phân bằng một trừ hai, bằng âm một.

**`x3`** — Ý c sai: diện tích phải cộng giá trị tuyệt đối từng phần, bằng một cộng bốn, bằng năm, không phải ba. Ý d đúng: đổi chỗ hai cận thì tích phân đổi dấu, bằng âm ba.

### ⏱ Trả lời ngắn và mẹo máy tính

**`x4`** — Câu trả lời ngắn. Tính tích phân từ không đến hai của ba x bình phương trừ hai x cộng một. Nguyên hàm là x lập phương trừ x bình phương cộng x. Lấy cận: tám trừ bốn cộng hai, bằng sáu.

**`x5`** — Mẹo thực chiến: máy tính cầm tay có phím tích phân. Nhập hàm số, cận dưới, cận trên, máy cho ngay kết quả số. Dùng nó để kiểm tra đáp số, chẳng hạn tích phân từ một đến hai của ba x bình phương cho đúng bảy. Với lượng giác, nhớ chuyển sang chế độ ra đi an.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, tích phân từ a đến b của f bằng F của b trừ F của a, với F là một nguyên hàm bất kỳ. Hai, kết quả không phụ thuộc hằng số C và tên biến. Ba, tích phân là diện tích có dấu, có thể âm hoặc bằng không khi hàm đổi dấu.

**`o2`** — Bài tập tự luyện. Một, tích phân từ không đến một của bốn x lập phương trừ hai x. Hai, tích phân từ không đến pi phần ba của hai sin x. Ba, tích phân từ một đến e của một cộng một chia x. Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập mười ba, ta học các tính chất của tích phân: tuyến tính, cộng khoảng và so sánh, những công cụ giúp tính nhanh và lập luận chặt chẽ. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. ∫₀¹(4x³ − 2x) dx → **0**
2. ∫₀^(π/3) 2 sin x dx → **1**
3. ∫₁ᵉ(1 + 1/x) dx → **e**
