# INT05 – Nguyên hàm của f(ax + b): Hàm hợp tuyến tính – vì sao chia cho a

> Sinh tự động từ `int05/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int05`.

**Số nhịp:** 25 · **Số công thức Typst:** 55 · **Từ:** 1362

## Mở đầu

### ⏱ Mở đầu: số 2 ở mẫu từ đâu ra?

**`h1`** — Ở tập trước, ta đã dùng kết quả: nguyên hàm của cốt hai x bằng sin hai x chia hai. Con số hai ở mẫu từ đâu ra? Nếu thay hai bằng ba, bằng năm, hay bằng âm một, kết quả thay đổi thế nào? Hôm nay ta trả lời câu hỏi đó cho mọi hàm số có dạng f của a x cộng b.

**`h2`** — Đây là tập năm của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: nguyên hàm của f của a x cộng b, và vì sao luôn phải chia cho a.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, quy tắc tổng quát và cách chứng minh bằng đạo hàm hàm hợp. Hai, ý nghĩa hình học: co giãn đồ thị theo phương ngang làm độ dốc nhân lên a lần. Ba, hai cái bẫy: quên chia a, và áp dụng sai khi bên trong không phải bậc nhất.

## Bản chất

### ⏱ Quy tắc tổng quát

**`c1`** — Giả sử F là một nguyên hàm của f. Theo quy tắc đạo hàm hàm hợp, đạo hàm của F của a x cộng b bằng a nhân f của a x cộng b. Thừa ra một thừa số a, nên ta chia cho a để bù lại. Vậy nguyên hàm của f của a x cộng b bằng một phần a nhân F của a x cộng b, cộng C, với a khác không.

### ⏱ Bản chất hình học: nén ngang

**`c2`** — Vì sao lại là a? Hãy nhìn đồ thị sin x và sin hai x. Đồ thị sin hai x là sin x bị nén theo phương ngang hai lần. Nén ngang làm đồ thị dốc gấp đôi: tại các điểm tương ứng, độ dốc của sin hai x luôn gấp hai lần độ dốc của sin x.

**`c3`** — Khi nén với hệ số a bất kỳ, độ dốc nhân lên a lần. Đó là lý do đạo hàm sinh ra thừa số a, và nguyên hàm phải chia cho a. Hình bên trái cho thấy khi a tăng, đường cong dày đặc hơn và tiếp tuyến dốc hơn đúng a lần.

**`c4`** — Còn số b thì sao? Số b chỉ tịnh tiến đồ thị theo phương ngang, không làm thay đổi độ dốc. Vì vậy b không xuất hiện ở mẫu số: chỉ có a là quan trọng.

### ⏱ Bảng nguyên hàm mở rộng

**`c5`** — Áp dụng quy tắc cho bảng nguyên hàm cơ bản, ta được bảng mở rộng. Lũy thừa của a x cộng b, một chia a x cộng b, e mũ a x cộng b, cốt và sin của a x cộng b: tất cả đều giống bảng cũ, chỉ thêm một phần a ở phía trước.

**`c6`** — Ba ví dụ nhanh. Nguyên hàm của hai x cộng một mũ năm là hai x cộng một mũ sáu, chia mười hai. Nguyên hàm của e mũ ba x trừ một là e mũ ba x trừ một chia ba. Còn nguyên hàm của một chia một trừ hai x là âm một phần hai lô ga nê pe trị tuyệt đối của một trừ hai x: chú ý a bằng âm hai nên có dấu trừ.

### ⏱ Hai cái bẫy

**`c7`** — Cái bẫy thứ nhất: quên chia a, hoặc nhân a thay vì chia. Viết nguyên hàm của cốt ba x bằng ba sin ba x là sai. Lấy đạo hàm kiểm tra sẽ được chín cốt ba x. Đúng phải là sin ba x chia ba.

**`c8`** — Cái bẫy thứ hai nguy hiểm hơn: quy tắc chỉ đúng khi bên trong là bậc nhất. Nguyên hàm của e mũ x bình phương không phải e mũ x bình phương chia hai x. Đạo hàm của biểu thức đó phức tạp hơn nhiều. Với biểu thức bên trong bậc hai trở lên, ta phải khai triển hoặc dùng phương pháp khác.

## Ví dụ

### ⏱ Ví dụ 1–2: áp dụng trực tiếp

**`e1`** — Ví dụ một: nguyên hàm của ba x trừ hai, mũ bốn. Ở đây a bằng ba và số mũ mới là năm. Kết quả là ba x trừ hai mũ năm, chia ba nhân năm, tức là chia mười lăm, cộng C. So với cách khai triển cả biểu thức, cách này nhanh hơn rất nhiều.

**`e2`** — Ví dụ hai: nguyên hàm của một chia hai x cộng một, cộng e mũ hai x. Cả hai hạng tử đều có a bằng hai. Kết quả là một phần hai lô ga nê pe trị tuyệt đối hai x cộng một, cộng một phần hai e mũ hai x, cộng C.

### ⏱ Ví dụ 3–4: có điều kiện và căn thức

**`e3`** — Ví dụ ba: tìm F là nguyên hàm của sin của hai x trừ pi phần ba, biết F của pi phần sáu bằng một. Ta có F bằng âm một phần hai cốt của hai x trừ pi phần ba cộng C. Tại pi phần sáu, góc bên trong bằng không, nên âm một phần hai cộng C bằng một, suy ra C bằng ba phần hai.

**`e4`** — Ví dụ bốn: nguyên hàm của một chia căn hai x cộng một. Viết lại thành hai x cộng một mũ âm một phần hai. Số mũ mới là một phần hai, a bằng hai, nên ta chia cho hai nhân một phần hai, bằng một. Kết quả gọn đến bất ngờ: căn của hai x cộng một, cộng C.

### ⏱ Ví dụ 5: bể nước bị rò

**`e5`** — Ví dụ năm, bài toán thực tế. Một bể chứa năm trăm lít nước bị rò. Tốc độ rò giảm dần theo thời gian: r của t bằng hai mươi e mũ âm không phẩy một t, lít mỗi giờ. Hỏi sau mười giờ, bể đã mất bao nhiêu lít nước?

**`e6`** — Lượng nước đã mất L là nguyên hàm của r. Ở đây a bằng âm không phẩy một, nên L bằng âm hai trăm e mũ âm không phẩy một t cộng C. Lúc đầu chưa mất nước, nên C bằng hai trăm. Sau mười giờ, L bằng hai trăm nhân một trừ e mũ âm một, xấp xỉ một trăm hai mươi sáu phẩy bốn lít.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai, tất cả xoay quanh việc chia cho a. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: a bằng hai nên chia hai. Ý b sai: thiếu một phần hai, đúng phải là một phần hai lô ga nê pe trị tuyệt đối hai x trừ một.

**`x3`** — Ý c đúng: ở đây a bằng âm ba, nên một phần a là âm một phần ba. Ý d sai: ngoài việc chia cho số mũ mới là bốn, còn phải chia cho a bằng hai, nên đúng phải là chia tám.

### ⏱ Trả lời ngắn và mẹo nhẩm nhanh

**`x4`** — Câu trả lời ngắn. F là nguyên hàm của e mũ hai x trừ hai, và F của một bằng một. Tính F của hai, làm tròn đến hàng phần trăm. F bằng một phần hai e mũ hai x trừ hai cộng C. F của một bằng một phần hai cộng C bằng một, nên C bằng một phần hai. F của hai bằng e bình phương chia hai cộng một phần hai, xấp xỉ bốn phẩy một chín.

**`x5`** — Mẹo nhẩm nhanh hai bước. Bước một: coi a x cộng b như một biến mới, viết nguyên hàm theo bảng cơ bản. Bước hai: chia cho a. Trước khi làm, kiểm tra biểu thức bên trong có đúng là bậc nhất hay không.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, nguyên hàm của f của a x cộng b bằng một phần a nhân F của a x cộng b cộng C. Hai, a xuất hiện vì nén ngang làm độ dốc nhân a, còn b chỉ tịnh tiến. Ba, quy tắc chỉ dùng khi bên trong là bậc nhất, và đừng quên dấu khi a âm.

**`o2`** — Bài tập tự luyện. Một, tìm nguyên hàm của một trừ ba x mũ năm. Hai, tìm nguyên hàm của e mũ âm x cộng sin bốn x. Ba, biết F phẩy bằng một chia hai x cộng ba và F của âm một bằng hai, tính F của một phần hai. Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập sáu, ta sẽ luyện kỹ dạng nguyên hàm có điều kiện và hàm số cho theo từng khúc, một dạng rất hay ra trong câu đúng sai. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. Tìm ∫(1 − 3x)⁵ dx. → **−(1 − 3x)⁶/18 + C**
2. Tìm ∫(e⁻ˣ + sin 4x) dx. → **−e⁻ˣ − cos 4x/4 + C**
3. Biết F'(x) = 1/(2x + 3), F(−1) = 2. Tính F(1/2). → **F(1/2) = 2 + ln 2**
