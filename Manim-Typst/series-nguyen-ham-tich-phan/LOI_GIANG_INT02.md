# INT02 – Tính chất nguyên hàm: Hàm lũy thừa & quy tắc tuyến tính

> Sinh tự động từ `int02/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int02`.

**Số nhịp:** 32 · **Số công thức Typst:** 79 · **Từ:** 1617

## Mở đầu

### ⏱ Mở đầu: không thể đoán mãi

**`h1`** — Ở tập trước, ta tìm nguyên hàm của hai x bằng cách đoán: x bình phương có đạo hàm là hai x. Nhưng nếu đề bài cho ba x bình phương trừ bốn x cộng năm, hay căn bậc hai của x, chẳng lẽ lần nào cũng phải đoán? Ta cần những quy tắc tính nhanh, giống như các quy tắc tính đạo hàm.

**`h2`** — Đây là tập hai của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: Tính chất của nguyên hàm, nguyên hàm của hàm lũy thừa và quy tắc tuyến tính.

**`h3`** — Sau video này, em sẽ có ba công cụ. Một, công thức nguyên hàm của hàm lũy thừa. Hai, hai tính chất: đưa hằng số ra ngoài, và tách tổng hiệu. Ba, nhận diện cái bẫy kinh điển: nguyên hàm của một tích không bằng tích các nguyên hàm.

## Bản chất

### ⏱ Đảo ngược bảng đạo hàm

**`c1`** — Nguyên tắc chung rất đơn giản: mỗi công thức đạo hàm, đọc theo chiều ngược lại, cho ta một công thức nguyên hàm. Đạo hàm của hằng số bằng không, nên nguyên hàm của không là hằng số C. Đạo hàm của x bằng một, nên nguyên hàm của một là x cộng C.

**`c2`** — Tổng quát hơn, nguyên hàm của hằng số k là k x cộng C. Về hình học, hàm f bằng hai là hằng số, nên trường hướng gồm các đoạn thẳng cùng độ dốc hai ở mọi nơi. Các nguyên hàm là những đường thẳng song song, y bằng hai x cộng C.

### ⏱ Nguyên hàm của hàm lũy thừa

**`c3`** — Bây giờ đến hàm lũy thừa. Ta biết đạo hàm của x mũ n cộng một bằng n cộng một nhân x mũ n. Chia hai vế cho n cộng một, ta được đạo hàm của x mũ n cộng một chia n cộng một đúng bằng x mũ n. Vậy nguyên hàm của x mũ n bằng x mũ n cộng một, chia n cộng một, cộng C.

**`c4`** — Cách nhớ: tăng số mũ thêm một, rồi chia cho số mũ mới. Với x lập phương: số mũ ba tăng thành bốn, rồi chia cho bốn, được x mũ bốn chia bốn. Tương tự, nguyên hàm của x bình phương là x lập phương chia ba, nguyên hàm của x mũ năm là x mũ sáu chia sáu.

**`c5`** — Kiểm tra bằng hình. Đường màu xanh là f bằng x bình phương, đường màu vàng là F bằng x lập phương chia ba. Khi điểm xét chạy dọc trục hoành, độ dốc tiếp tuyến của đường vàng luôn bằng đúng chiều cao của đường xanh tại cùng hoành độ. Đó chính là F phẩy bằng f.

**`c6`** — Công thức còn đúng với số mũ alpha là số thực bất kỳ khác âm một, trên khoảng mà hàm xác định. Chẳng hạn căn x bằng x mũ một phần hai, nên nguyên hàm là hai phần ba x mũ ba phần hai cộng C. Còn một chia x bình phương bằng x mũ âm hai, nên nguyên hàm là âm một chia x cộng C.

**`c7`** — Vì sao phải loại alpha bằng âm một? Khi đó số mũ mới bằng không, và ta phải chia cho không, vô nghĩa. Nguyên hàm của một chia x là một trường hợp đặc biệt, gắn với hàm lô ga rít, ta sẽ học ở tập ba.

### ⏱ Tính chất 1: hằng số ra ngoài

**`c8`** — Tính chất thứ nhất: nguyên hàm của k nhân f bằng k nhân nguyên hàm của f, với k khác không. Lý do: đạo hàm của k F bằng k nhân F phẩy, bằng k f. Về hình học, nhân k làm đồ thị giãn theo phương thẳng đứng, và mọi độ dốc cũng được nhân lên k lần.

**`c9`** — Điều kiện k khác không là cần thiết. Nguyên hàm của không nhân f là cả họ hằng số C, trong khi không nhân với nguyên hàm của f chỉ là số không. Hai vế không còn bằng nhau.

### ⏱ Tính chất 2: tổng và hiệu

**`c10`** — Tính chất thứ hai: nguyên hàm của tổng hay hiệu bằng tổng hay hiệu các nguyên hàm. Lý do: đạo hàm của F cộng G bằng f cộng g. Trên hình, độ dốc của đường tổng tại mỗi điểm đúng bằng tổng hai độ dốc thành phần.

**`c11`** — Gộp hai tính chất, ta tính được mọi đa thức theo từng hạng tử. Với ba x bình phương trừ bốn x cộng năm: ba nhân x lập phương chia ba, trừ bốn nhân x bình phương chia hai, cộng năm x. Kết quả là x lập phương trừ hai x bình phương cộng năm x cộng C.

**`c12`** — Lưu ý: mỗi hạng tử sinh ra một hằng số riêng, nhưng tổng các hằng số vẫn là một hằng số. Vì vậy, cuối cùng ta chỉ viết một chữ C duy nhất.

## Ví dụ

### ⏱ Ví dụ 1: khai triển trước khi tính

**`e1`** — Ví dụ một: tìm nguyên hàm của hai x trừ một, tất cả bình phương. Không có quy tắc nguyên hàm cho bình phương của một biểu thức, vì vậy việc đầu tiên là khai triển.

**`e2`** — Hai x trừ một, tất cả bình phương, bằng bốn x bình phương trừ bốn x cộng một. Nguyên hàm từng hạng tử: bốn phần ba x lập phương, trừ hai x bình phương, cộng x, cộng C. Hình bên trái xác nhận: độ dốc của F luôn bằng chiều cao của f.

### ⏱ Ví dụ 2: tách phân thức

**`e3`** — Ví dụ hai: tìm nguyên hàm của x bình phương cộng một, chia cho x bình phương. Cũng không có quy tắc cho thương, nên ta tách phân thức thành tổng các lũy thừa.

**`e4`** — Chia từng hạng tử cho x bình phương, ta được một cộng x mũ âm hai. Nguyên hàm là x trừ một chia x cộng C, xét trên từng khoảng không chứa số không. Bên trái, ta kiểm tra trên khoảng x dương.

### ⏱ Ví dụ 3: bể nước

**`e5`** — Ví dụ ba, bài toán thực tế. Nước chảy vào một bể với tốc độ r của t bằng ba t bình phương cộng hai t, đơn vị lít mỗi phút. Lúc đầu bể có mười lít nước. Hỏi sau bốn phút, trong bể có bao nhiêu lít?

**`e6`** — Thể tích V là một nguyên hàm của tốc độ chảy, vì V phẩy bằng r. Theo quy tắc tuyến tính, V của t bằng t lập phương cộng t bình phương cộng C. Điều kiện V của không bằng mười cho C bằng mười.

**`e7`** — Tại t bằng bốn: sáu mươi tư cộng mười sáu cộng mười, bằng chín mươi lít. Hãy quan sát mực nước dâng lên đồng thời với điểm chạy trên đồ thị thể tích.

## Đề thi mới

### ⏱ Bẫy: nguyên hàm của một tích

**`x1`** — Bây giờ là cái bẫy kinh điển. Có quy tắc cho tổng, vậy có quy tắc cho tích không? Nhiều bạn viết: nguyên hàm của f nhân g bằng nguyên hàm của f nhân nguyên hàm của g. Điều này sai.

**`x2`** — Phản ví dụ: lấy f và g cùng bằng x. Đúng ra, nguyên hàm của x nhân x là x lập phương chia ba. Cách làm sai cho x mũ bốn chia bốn, có đạo hàm là x lập phương, không phải x bình phương. Trên hình, đường màu đỏ dốc quá mức cần thiết.

### ⏱ Câu hỏi Đúng/Sai

**`x3`** — Câu hỏi dạng đúng sai. Cho hàm số f của x bằng ba x bình phương cộng hai x trừ một. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x4`** — Ý a đúng, áp dụng quy tắc lũy thừa cho từng hạng tử. Ý b sai: đây chính là cái bẫy tích. Lấy đạo hàm vế phải được bốn x lập phương cộng ba x bình phương trừ hai x, không bằng x nhân f của x.

**`x5`** — Ý c đúng: F bằng x lập phương cộng x bình phương trừ x cộng C. F của một bằng hai cho C bằng một, nên F của không bằng một. Ý d đúng: f trừ ba x bình phương bằng hai x trừ một, có nguyên hàm x bình phương trừ x cộng C.

### ⏱ Trả lời ngắn và mẹo đổi về lũy thừa

**`x6`** — Câu trả lời ngắn. Biết F phẩy bằng sáu x bình phương trừ bốn x cộng một, và F của một bằng ba. Tính F của hai. Ta có F bằng hai x lập phương trừ hai x bình phương cộng x cộng C. F của một bằng một cộng C bằng ba, nên C bằng hai. Vậy F của hai bằng mười sáu trừ tám cộng hai cộng hai, bằng mười hai.

**`x7`** — Mẹo thực chiến: trước khi tính, hãy đổi mọi căn và phân thức về dạng lũy thừa. Căn x là x mũ một phần hai, một chia x mũ n là x mũ âm n, căn bậc ba của x bình phương là x mũ hai phần ba. Ví dụ, một chia căn x là x mũ âm một phần hai, có nguyên hàm là hai căn x cộng C.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, nguyên hàm của x mũ alpha bằng x mũ alpha cộng một chia alpha cộng một, cộng C, với alpha khác âm một. Hai, hằng số khác không được đưa ra ngoài dấu nguyên hàm. Ba, nguyên hàm của tổng hiệu bằng tổng hiệu các nguyên hàm, nhưng với tích và thương thì không.

**`o2`** — Bài tập tự luyện. Một, tìm nguyên hàm của x bình phương trừ ba x cộng hai. Hai, tìm nguyên hàm của x cộng một chia căn x, với x dương. Ba, biết F phẩy bằng bốn x lập phương trừ hai x và F của một bằng ba, tính F của hai. Đáp số hiện ở cuối màn hình, em hãy tự làm trước khi xem.

**`o3`** — Ở tập ba, ta sẽ giải quyết trường hợp đặc biệt alpha bằng âm một, với nguyên hàm của một chia x, và nguyên hàm của các hàm số mũ. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. Tìm ∫(x² − 3x + 2) dx. → **x³/3 − 3x²/2 + 2x + C**
2. Tìm ∫(x + 1)/√x dx với x > 0. → **(2/3)x√x + 2√x + C**
3. Biết F'(x) = 4x³ − 2x, F(1) = 3. Tính F(2). → **F(2) = 15**
