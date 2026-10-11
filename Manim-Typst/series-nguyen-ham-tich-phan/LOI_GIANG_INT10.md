# INT10 – Từ tốc độ thay đổi đến đại lượng: Nguyên hàm trong thực tế & tổng ôn Phần A

> Sinh tự động từ `int10/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int10`.

**Số nhịp:** 22 · **Số công thức Typst:** 36 · **Từ:** 1245

## Mở đầu

### ⏱ Mở đầu: tốc độ thay đổi ở khắp nơi

**`h1`** — Trong đời sống, ta thường đo được tốc độ thay đổi trước khi biết chính đại lượng: đồng hồ tốc độ của xe, tốc độ tăng dân số mỗi năm, chi phí làm thêm một sản phẩm, hay tốc độ nguội đi của một cốc nước nóng. Nguyên hàm là chiếc cầu nối từ tốc độ thay đổi trở về đại lượng ban đầu.

**`h2`** — Đây là tập mười của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: từ tốc độ thay đổi đến đại lượng, và cũng là tập tổng ôn khép lại Phần A về nguyên hàm.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, quy trình chung cho mọi bài toán thực tế dùng nguyên hàm. Hai, cách đọc đơn vị và ý nghĩa của hằng số C. Ba, bốn mô hình tiêu biểu: dân số, chi phí, nhiệt độ và chuyển động.

## Bản chất

### ⏱ Quy trình chung

**`c1`** — Mọi bài toán đều theo cùng một khuôn. Biết tốc độ thay đổi Q phẩy của t, và biết giá trị của Q tại một thời điểm. Lấy nguyên hàm để được Q bằng một nguyên hàm cộng C, rồi dùng giá trị đã biết để tìm C. Cuối cùng, thay thời điểm cần hỏi để tính đại lượng.

### ⏱ Đơn vị và ý nghĩa của C

**`c2`** — Hãy để ý đơn vị. Nếu Q đo bằng người và t đo bằng năm, thì Q phẩy có đơn vị người mỗi năm. Lấy nguyên hàm theo t sẽ nhân lại đơn vị năm, đưa ta trở về đơn vị người. Hằng số C luôn mang đúng đơn vị của Q, và thường chính là giá trị ban đầu.

### ⏱ Độ thay đổi không phụ thuộc C

**`c3`** — Một quan sát rất quan trọng: độ thay đổi Q của b trừ Q của a không phụ thuộc vào C, vì hai chữ C triệt tiêu nhau. Muốn biết đại lượng tăng thêm bao nhiêu trong một khoảng thời gian, ta thậm chí không cần điều kiện ban đầu. Đây chính là hạt giống của tích phân ở Phần B.

### ⏱ Bảng đối chiếu thực tế

**`c4`** — Bảng đối chiếu giúp em nhận ra mô hình ngay khi đọc đề. Vận tốc là tốc độ thay đổi của vị trí. Chi phí biên là tốc độ thay đổi của tổng chi phí. Tốc độ tăng trưởng ứng với dân số, lưu lượng chảy ứng với thể tích nước. Thấy cặp nào, lấy nguyên hàm vế trái để được vế phải.

## Ví dụ

### ⏱ Mô hình 1: dân số

**`e1`** — Mô hình một, dân số. Một thị trấn có mười nghìn người, tốc độ tăng dân số là năm mươi nhân e mũ không phẩy không hai t người mỗi năm. Lấy nguyên hàm: P bằng hai nghìn năm trăm e mũ không phẩy không hai t cộng C. Điều kiện ban đầu cho C bằng bảy nghìn năm trăm.

**`e2`** — Sau mười năm, P bằng hai nghìn năm trăm e mũ không phẩy hai cộng bảy nghìn năm trăm, xấp xỉ mười nghìn năm trăm năm mươi tư người. Đồ thị cong lên dần vì tốc độ tăng cũng tăng theo thời gian.

### ⏱ Mô hình 2: chi phí biên

**`e3`** — Mô hình hai, chi phí biên. Chi phí để sản xuất thêm sản phẩm thứ x là không phẩy ba x cộng hai mươi nghìn đồng, và chi phí cố định là năm trăm nghìn đồng. Lấy nguyên hàm: tổng chi phí C của x bằng không phẩy một lăm x bình phương cộng hai mươi x cộng năm trăm.

**`e4`** — Câu hỏi thực tế: tăng sản lượng từ một trăm lên hai trăm sản phẩm thì tốn thêm bao nhiêu? Lấy C của hai trăm trừ C của một trăm: mười nghìn năm trăm trừ bốn nghìn, bằng sáu nghìn năm trăm nghìn đồng. Chi phí cố định năm trăm đã triệt tiêu, đúng như quan sát ở phần trước.

### ⏱ Mô hình 3: nhiệt độ

**`e5`** — Mô hình ba, nhiệt độ. Một cốc nước chín mươi độ nguội đi với tốc độ âm hai e mũ âm không phẩy một t độ mỗi phút. Nguyên hàm: T bằng hai mươi e mũ âm không phẩy một t cộng C, và C bằng bảy mươi. Sau mười phút, nhiệt độ xấp xỉ bảy mươi bảy phẩy bốn độ, và về lâu dài tiến dần tới bảy mươi độ.

### ⏱ Mô hình 4: quãng đường phanh

**`e6`** — Mô hình bốn, phanh xe. Một ô tô đang chạy hai mươi mét mỗi giây thì phanh, vận tốc giảm theo v bằng hai mươi trừ năm t. Xe dừng khi v bằng không, tức t bằng bốn giây. Quãng đường phanh là s của bốn, với s bằng hai mươi t trừ hai phẩy năm t bình phương: tám mươi trừ bốn mươi, bằng bốn mươi mét.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai dựa trên mô hình dân số. Tốc độ tăng là năm mươi e mũ không phẩy không hai t người mỗi năm, dân số ban đầu mười nghìn người. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: chia năm mươi cho không phẩy không hai được hai nghìn năm trăm. Ý b đúng: hai nghìn năm trăm cộng C bằng mười nghìn, nên C bằng bảy nghìn năm trăm.

**`x3`** — Ý c đúng: P của mười xấp xỉ mười nghìn năm trăm năm mươi tư người. Ý d sai: dân số chỉ tăng thêm khoảng năm trăm năm mươi tư người trong mười năm, không phải một nghìn.

### ⏱ Trả lời ngắn và bản đồ Phần A

**`x4`** — Câu trả lời ngắn. Chiều cao của một cây tăng với tốc độ một chia t cộng một mét mỗi năm, lúc trồng cây cao không phẩy năm mét. Tìm chiều cao sau bốn năm, làm tròn đến hàng phần trăm. h bằng lô ga nê pe của t cộng một, cộng không phẩy năm. Vậy h của bốn bằng lô ga nê pe năm cộng không phẩy năm, xấp xỉ hai phẩy một một mét.

**`x5`** — Tổng ôn Phần A bằng bản đồ chọn phương pháp. Gặp tổng hiệu: tách từng hạng tử theo bảng. Gặp f của a x cộng b: chia cho a. Gặp phân thức: chia đa thức hoặc tách. Gặp hàm của u nhân u phẩy: đổi biến. Gặp tích hai hàm khác loại: từng phần. Và luôn dùng điều kiện để tìm C.

**`x6`** — Nhìn lại chín tập đã qua: bản chất nguyên hàm, tính chất và hàm lũy thừa, một chia x và hàm mũ, lượng giác, quy tắc chia cho a, nguyên hàm có điều kiện và hàm từng khúc, phân thức hữu tỉ, đổi biến số, và từng phần. Tất cả hội tụ trong tập hôm nay: biết tốc độ thay đổi, tìm lại đại lượng.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, đại lượng bằng nguyên hàm của tốc độ thay đổi, cộng hằng số xác định từ điều kiện ban đầu. Hai, hằng số C mang đơn vị của đại lượng, thường là giá trị ban đầu. Ba, độ thay đổi giữa hai thời điểm không phụ thuộc C.

**`o2`** — Bài tập tự luyện. Một, vật có gia tốc sáu t, vận tốc ban đầu hai, vị trí ban đầu không, tính quãng đường sau hai giây. Hai, doanh thu biên một trăm trừ không phẩy hai x, doanh thu ban đầu bằng không, tính doanh thu khi bán ba trăm sản phẩm. Ba, nước chảy vào bể với tốc độ bốn căn t lít mỗi phút, bể ban đầu rỗng, tính lượng nước sau chín phút.

**`o3`** — Phần A đã khép lại. Từ tập mười một, ta bước sang Phần B: tích phân, bắt đầu từ câu hỏi diện tích dưới một đường cong và tổng Riemann. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. a(t) = 6t, v(0) = 2, s(0) = 0. Tính s(2). → **s(2) = 12**
2. R'(x) = 100 − 0,2x, R(0) = 0. Tính R(300). → **R(300) = 21000**
3. V'(t) = 4√t, V(0) = 0. Tính V(9). → **V(9) = 72**
