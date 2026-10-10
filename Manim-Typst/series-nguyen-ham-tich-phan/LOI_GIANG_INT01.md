# INT01 – Đi ngược đạo hàm: Bản chất của nguyên hàm

> Sinh tự động từ `int01/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int01`.

**Số nhịp:** 36 · **Số công thức Typst:** 49 · **Từ:** 1716

## Mở đầu

### ⏱ Mở đầu: chiếc xe mất đồng hồ quãng đường

**`h1`** — Hãy tưởng tượng em đang ngồi trên một chiếc xe. Đồng hồ quãng đường bị hỏng, chỉ còn đồng hồ tốc độ hoạt động. Tại mỗi thời điểm, em biết xe chạy nhanh bao nhiêu, nhưng không biết xe đã đi tới đâu.

**`h2`** — Câu hỏi đặt ra là: chỉ từ vận tốc, liệu ta có khôi phục được vị trí của xe hay không? Ở lớp mười một, ta đi từ vị trí sang vận tốc bằng phép lấy đạo hàm. Hôm nay, ta sẽ đi theo chiều ngược lại.

**`h3`** — Phép toán đi ngược đạo hàm có tên là nguyên hàm. Chào mừng các em đến với tập một của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: Đi ngược đạo hàm, bản chất của nguyên hàm.

**`h4`** — Sau video này, em sẽ nắm được ba điều. Một, nguyên hàm là gì. Hai, vì sao luôn có hằng số C. Ba, cách dùng một điều kiện để chọn đúng một nguyên hàm, và áp dụng vào bài toán chuyển động.

## Bản chất

### ⏱ Bài toán đi ngược đạo hàm

**`c1`** — Bắt đầu bằng một bài toán thật đơn giản. Tìm một hàm số F sao cho đạo hàm của F bằng hai x, tại mọi giá trị của x.

**`c2`** — Đồ thị bên trái là đường thẳng y bằng hai x. Đây là đồ thị của đạo hàm, chưa phải hàm ta cần tìm. Nó cho biết: tại mỗi hoành độ x, đồ thị của F phải dốc bao nhiêu. Tại x bằng một, độ dốc phải bằng hai. Tại x bằng âm một, độ dốc phải bằng âm hai.

### ⏱ Trường hướng và họ nguyên hàm

**`c3`** — Ta biến thông tin đó thành hình ảnh. Tại mỗi điểm của mặt phẳng, vẽ một đoạn thẳng nhỏ có hệ số góc bằng hai x. Bên trái trục tung, các đoạn dốc xuống. Bên phải, các đoạn dốc lên, càng xa trục tung càng dốc. Hình này gọi là trường hướng.

**`c4`** — Đồ thị của F phải đi theo đúng các hướng này, giống như một chiếc lá trôi theo dòng nước. Thả một điểm xuất phát tại gốc tọa độ. Đường cong mà nó vạch ra chính là parabol y bằng x bình phương.

**`c5`** — Kiểm tra lại bằng đạo hàm: x bình phương có đạo hàm là hai x, đúng như yêu cầu. Ta nói: F của x bằng x bình phương là một nguyên hàm của hàm số f của x bằng hai x.

**`c6`** — Nhưng hãy thử thả điểm xuất phát ở chỗ khác, chẳng hạn tại điểm không phẩy hai. Đường cong mới cũng đi đúng theo trường hướng: đó là parabol x bình phương cộng hai. Thả tại điểm không phẩy âm một, ta được x bình phương trừ một.

**`c7`** — Khi điểm xuất phát trượt lên xuống, ta thu được vô số đường cong, tất cả đều khớp với trường hướng. Mỗi đường ứng với một giá trị của hằng số C, và có phương trình y bằng x bình phương cộng C.

**`c8`** — Vì sao cộng thêm C không làm thay đổi đạo hàm? Về đại số, đạo hàm của hằng số bằng không. Về hình học, cộng C chỉ tịnh tiến đồ thị lên hoặc xuống, nên tại cùng một hoành độ, các tiếp tuyến luôn song song với nhau, dù điểm xét chạy tới đâu.

### ⏱ Định nghĩa và định lý

**`c9`** — Bây giờ ta phát biểu chính xác. Cho hàm số f xác định trên K, với K là một khoảng, một đoạn hoặc một nửa khoảng. Hàm số F được gọi là nguyên hàm của f trên K nếu F phẩy của x bằng f của x với mọi x thuộc K.

**`c10`** — Từ hình ảnh vừa rồi, ta có định lý quan trọng. Nếu F là một nguyên hàm của f trên K, thì mọi nguyên hàm của f trên K đều có dạng F của x cộng C, với C là một hằng số. Ngược lại, với mỗi hằng số C, hàm F cộng C cũng là một nguyên hàm của f.

**`c11`** — Vì sao không thể có nguyên hàm nào khác? Lấy hai nguyên hàm, chẳng hạn x bình phương trừ một và x bình phương cộng hai. Cho điểm xét chạy dọc trục hoành: khoảng cách theo phương thẳng đứng giữa hai đồ thị luôn luôn bằng ba.

**`c12`** — Tổng quát, nếu G và F cùng là nguyên hàm của f, thì đạo hàm của G trừ F bằng f trừ f, bằng không trên K. Một hàm số có đạo hàm bằng không trên một khoảng thì là hàm hằng. Vậy G bằng F cộng một hằng số.

### ⏱ Kí hiệu họ nguyên hàm

**`c13`** — Cả họ nguyên hàm được viết gọn bằng một kí hiệu. Ta viết: tích phân f của x d x bằng F của x cộng C, và đọc là họ nguyên hàm của f. Chẳng hạn, nguyên hàm của hai x d x bằng x bình phương cộng C.

### ⏱ Bẫy: nguyên hàm trên từng khoảng

**`c14`** — Một lưu ý chuyên sâu: kết luận chỉ khác nhau một hằng số chỉ đúng trên từng khoảng. Hàm số âm một chia x bình phương không xác định tại x bằng không. Hàm một chia x là một nguyên hàm của nó trên từng khoảng: từ âm vô cùng đến không, và từ không đến dương vô cùng.

**`c15`** — Nếu dịch nhánh bên phải lên một đơn vị, và nhánh bên trái xuống hai đơn vị, hàm mới vẫn có đạo hàm bằng âm một chia x bình phương tại mọi x khác không. Hai nhánh mang hai hằng số khác nhau. Đây là cái bẫy hay gặp trong câu hỏi đúng sai.

## Ví dụ

### ⏱ Ví dụ 1: nguyên hàm thỏa điều kiện

**`e1`** — Ví dụ một. Tìm nguyên hàm F của hàm số f của x bằng ba x bình phương, biết F của một bằng năm.

**`e2`** — Bước một, tìm họ nguyên hàm. Ta nhớ đạo hàm của x lập phương bằng ba x bình phương. Vậy họ nguyên hàm là x lập phương cộng C. Bên trái là một vài thành viên của họ này.

**`e3`** — Bước hai, dùng điều kiện. Đồ thị phải đi qua điểm một phẩy năm. Thay x bằng một, ta được một cộng C bằng năm, suy ra C bằng bốn. Trên hình, đường cong được kéo lên cho tới khi đi qua đúng điểm này.

**`e4`** — Vậy F của x bằng x lập phương cộng bốn. Kiểm tra lại: đạo hàm bằng ba x bình phương, và F của một bằng năm. Cả hai điều kiện đều thỏa mãn.

### ⏱ Ví dụ 2: tìm vị trí từ vận tốc

**`e5`** — Ví dụ hai, quay lại chiếc xe ở đầu bài. Xe chuyển động thẳng với vận tốc v của t bằng hai t cộng một, đơn vị mét trên giây. Lúc bắt đầu, xe ở vị trí hai mét so với mốc. Hỏi sau ba giây, xe ở vị trí nào?

**`e6`** — Vị trí s là một nguyên hàm của vận tốc, vì s phẩy bằng v. Đạo hàm của t bình phương cộng t bằng hai t cộng một, nên s của t bằng t bình phương cộng t cộng C.

**`e7`** — Điều kiện s của không bằng hai cho ta C bằng hai. Vậy s của t bằng t bình phương cộng t cộng hai. Hằng số C ở đây có ý nghĩa thực tế rất rõ: đó chính là vị trí ban đầu của xe.

**`e8`** — Tại t bằng ba, s bằng chín cộng ba cộng hai, bằng mười bốn mét. Hãy quan sát chiếc xe chạy, đồng thời với điểm chạy trên đồ thị vị trí. Đúng ba giây sau, xe dừng ở vạch mười bốn mét.

**`e9`** — Tính từ lúc bắt đầu, xe đã đi thêm mười bốn trừ hai, bằng mười hai mét. Hiệu s của ba trừ s của không này sẽ gặp lại ở các tập sau, với tên gọi tích phân.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Bây giờ là một câu hỏi dạng đúng sai của đề thi tốt nghiệp. Cho hàm số f của x bằng sáu x bình phương trừ hai x. Gọi F là nguyên hàm của f trên R thỏa mãn F của không bằng một. Em hãy tạm dừng video và tự đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng, vì đó chính là định nghĩa nguyên hàm. Ý b sai: hàm này có đạo hàm đúng, nhưng tại không nó bằng không, chứ không bằng một. Đúng phải là F của x bằng hai x lập phương trừ x bình phương cộng một.

**`x3`** — Ý c đúng: F của một bằng hai trừ một cộng một, bằng hai. Ý d đúng: G chỉ khác F một hằng số, nên G vẫn là một nguyên hàm của f, chỉ là không thỏa điều kiện F của không bằng một.

### ⏱ Câu trả lời ngắn và mẹo kiểm tra

**`x4`** — Thêm một câu trả lời ngắn. Biết F là một nguyên hàm của hai x, và F của hai bằng một. Tính F của ba. Ta có F bằng x bình phương cộng C. Thay x bằng hai: bốn cộng C bằng một, nên C bằng âm ba. Vậy F của ba bằng chín trừ ba, bằng sáu.

**`x5`** — Mẹo thực chiến: muốn kiểm tra một nguyên hàm, hãy lấy đạo hàm ngược lại. Trên máy tính cầm tay, tính đạo hàm của F tại một điểm, rồi so sánh với giá trị của f tại điểm đó. Ví dụ, đạo hàm của x lập phương cộng bốn tại hai bằng mười hai, và f của hai cũng bằng mười hai.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt bài học bằng ba ý. Một, nguyên hàm là đi ngược đạo hàm: F là nguyên hàm của f khi F phẩy bằng f. Hai, trên một khoảng, các nguyên hàm chỉ khác nhau một hằng số C; về hình học, đó là các đồ thị tịnh tiến theo phương thẳng đứng. Ba, một điều kiện ban đầu xác định được hằng số C.

**`o2`** — Bài tập tự luyện. Một, tìm họ nguyên hàm của bốn x lập phương. Hai, tìm F biết F phẩy bằng hai x cộng ba, và F của không bằng một. Ba, một vật có vận tốc ba t bình phương mét trên giây, vị trí ban đầu bằng không. Tìm vị trí của vật sau hai giây. Đáp số hiện ở cuối màn hình, em hãy tự làm trước khi xem.

**`o3`** — Ở tập hai, ta sẽ xây dựng các tính chất của nguyên hàm và nguyên hàm của hàm lũy thừa, cùng một cái bẫy rất hay gặp với tích và thương. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. Tìm ∫4x³ dx. → **x⁴ + C**
2. Tìm F biết F'(x) = 2x + 3 và F(0) = 1. → **F(x) = x² + 3x + 1**
3. Vật có v(t) = 3t² (m/s), s(0) = 0. Tìm s(2). → **s(2) = 8 m**
