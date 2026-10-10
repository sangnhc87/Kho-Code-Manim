# INT03 – Nguyên hàm của 1/x và hàm mũ: Hai nhánh của 1/x · hàm eˣ và aˣ

> Sinh tự động từ `int03/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int03`.

**Số nhịp:** 27 · **Số công thức Typst:** 61 · **Từ:** 1491

## Mở đầu

### ⏱ Mở đầu: lỗ thủng tại α = −1

**`h1`** — Ở tập trước, công thức nguyên hàm của x mũ alpha dùng được cho mọi số mũ, trừ đúng một giá trị: alpha bằng âm một. Trên trục số mũ, có một lỗ thủng tại âm một. Đó chính là hàm một chia x, một hàm rất hay gặp. Hôm nay ta vá lỗ thủng ấy, rồi gặp hàm số đặc biệt nhất của giải tích: hàm e mũ x, hàm có đạo hàm bằng chính nó.

**`h2`** — Đây là tập ba của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: nguyên hàm của một chia x và các hàm số mũ.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, vì sao nguyên hàm của một chia x là lô ga nê pe của trị tuyệt đối x. Hai, nguyên hàm của e mũ x và a mũ x. Ba, hai cái bẫy hay gặp: hằng số trên hai khoảng, và nhầm hàm mũ với hàm lũy thừa.

## Bản chất

### ⏱ Nguyên hàm của 1/x

**`c1`** — Bắt đầu với x dương. Ta đã biết đạo hàm của lô ga nê pe của x bằng một chia x. Đọc ngược lại: trên khoảng từ không đến dương vô cùng, nguyên hàm của một chia x là lô ga nê pe của x cộng C. Trên hình, độ dốc của đường lô ga rít luôn bằng chiều cao của đường một chia x.

**`c2`** — Còn khi x âm thì sao? Lô ga nê pe của x không xác định. Hãy lấy đối xứng đồ thị qua trục tung, được hàm lô ga nê pe của âm x. Đạo hàm của nó bằng âm một chia âm x, tức là một chia x. Vậy trên khoảng âm, lô ga nê pe của âm x cũng là một nguyên hàm của một chia x.

**`c3`** — Gộp hai trường hợp bằng trị tuyệt đối: nguyên hàm của một chia x bằng lô ga nê pe của trị tuyệt đối x, cộng C. Trị tuyệt đối không phải để trang trí: thiếu nó, công thức sai với mọi x âm.

**`c4`** — Lưu ý chuyên sâu: hàm một chia x xác định trên hai khoảng rời nhau, nên hai nhánh có thể mang hai hằng số khác nhau, C một bên phải và C hai bên trái. Hình bên trái cho thấy hai nhánh được tịnh tiến độc lập mà đạo hàm không thay đổi.

### ⏱ Hàm số e mũ x

**`c5`** — Chuyển sang hàm e mũ x. Tính chất nổi tiếng: đạo hàm của e mũ x bằng chính e mũ x. Vì vậy nguyên hàm của e mũ x là e mũ x cộng C. Trên đồ thị, tại mọi điểm, độ dốc tiếp tuyến đúng bằng chiều cao của điểm đó.

**`c6`** — Vì sao lại là số e? Xét các đường a mũ x với cơ số a khác nhau. Độ dốc tại x bằng không chính là lô ga nê pe của a. Khi a tăng dần, độ dốc này tăng theo, và có đúng một cơ số làm độ dốc bằng một: đó là số e, xấp xỉ hai phẩy bảy một tám.

### ⏱ Hàm số a mũ x

**`c7`** — Với cơ số a tổng quát, dương và khác một: đạo hàm của a mũ x bằng a mũ x nhân lô ga nê pe của a. Chia cho lô ga nê pe của a, ta được nguyên hàm của a mũ x bằng a mũ x chia lô ga nê pe của a, cộng C.

**`c8`** — Áp dụng: nguyên hàm của hai mũ x là hai mũ x chia lô ga nê pe hai. Với cơ số một phần hai, lô ga nê pe của một phần hai là số âm, bằng âm lô ga nê pe hai, nên kết quả mang dấu trừ. Nguyên hàm của mười mũ x là mười mũ x chia lô ga nê pe mười.

**`c9`** — Cái bẫy thứ hai: nhầm hàm mũ với hàm lũy thừa. Khi biến x nằm ở cơ số, như x mũ n, ta tăng số mũ. Khi biến x nằm ở số mũ, như hai mũ x, ta chia cho lô ga nê pe của cơ số. Viết nguyên hàm của hai mũ x thành hai mũ x cộng một chia x cộng một là sai hoàn toàn.

### ⏱ Bảng nguyên hàm cơ bản

**`c10`** — Đến đây, bảng nguyên hàm cơ bản của chúng ta đã có sáu dòng: hằng số, lũy thừa, một chia x, e mũ x và a mũ x. Đây là bộ công cụ nền cho mọi bài toán nguyên hàm phía sau.

## Ví dụ

### ⏱ Ví dụ 1: tổng hợp ba công thức

**`e1`** — Ví dụ một: tìm nguyên hàm của ba chia x cộng hai e mũ x trừ năm mũ x. Áp dụng quy tắc tuyến tính cho từng hạng tử: ba lô ga nê pe trị tuyệt đối x, cộng hai e mũ x, trừ năm mũ x chia lô ga nê pe năm, cộng C.

### ⏱ Ví dụ 2: tách phân thức ra 1/x

**`e2`** — Ví dụ hai: nguyên hàm của x bình phương cộng hai x trừ ba, chia cho x. Tách phân thức: được x cộng hai trừ ba chia x. Nguyên hàm là x bình phương chia hai, cộng hai x, trừ ba lô ga nê pe trị tuyệt đối x, cộng C. Hình bên trái kiểm tra trên khoảng x dương.

### ⏱ Ví dụ 3: nhân phân phối với eˣ

**`e3`** — Ví dụ ba: nguyên hàm của e mũ x nhân với một cộng e mũ âm x. Nhân phân phối, e mũ x nhân e mũ âm x bằng một, nên biểu thức trở thành e mũ x cộng một. Nguyên hàm là e mũ x cộng x cộng C.

### ⏱ Ví dụ 4: tăng trưởng vi khuẩn

**`e4`** — Ví dụ bốn, bài toán thực tế. Một quần thể vi khuẩn tăng với tốc độ N phẩy của t bằng năm trăm e mũ t con mỗi giờ. Lúc đầu có một nghìn năm trăm con. Hỏi sau hai giờ có khoảng bao nhiêu con?

**`e5`** — N là nguyên hàm của tốc độ tăng: N của t bằng năm trăm e mũ t cộng C. Điều kiện ban đầu: năm trăm cộng C bằng một nghìn năm trăm, nên C bằng một nghìn. Tại t bằng hai: năm trăm e bình phương cộng một nghìn, xấp xỉ bốn nghìn sáu trăm chín mươi lăm con.

**`e6`** — Hãy quan sát: số vi khuẩn tăng ngày càng nhanh, vì chính tốc độ năm trăm e mũ t cũng tăng theo thời gian. Đồ thị N cong dần lên, và đúng hai giờ sau, bộ đếm dừng ở khoảng bốn nghìn sáu trăm chín mươi lăm. Trong đề thi, dạng câu trả lời ngắn thường yêu cầu làm tròn đến hàng đơn vị như thế này.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Cho hàm số f của x bằng hai mũ x cộng một chia x, trên khoảng dương. Gọi F là một nguyên hàm của f. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: áp dụng hai công thức mới cho từng hạng tử. Ý b sai: đây là cái bẫy nhầm hàm mũ với lũy thừa. Nguyên hàm đúng của hai mũ x là hai mũ x chia lô ga nê pe hai.

**`x3`** — Ý c đúng: F của một bằng hai chia lô ga nê pe hai cộng lô ga nê pe một cộng C, mà lô ga nê pe một bằng không, nên C bằng không. Ý d sai: F của hai bằng bốn chia lô ga nê pe hai cộng lô ga nê pe hai, không phải lô ga nê pe bốn.

### ⏱ Trả lời ngắn: hai nhánh của ln|x|

**`x4`** — Câu trả lời ngắn, đúng dạng hai nhánh. F là nguyên hàm của một chia x trên tập số thực khác không, F của một bằng hai và F của âm một bằng ba. Tính F của e cộng F của âm e. Hai nhánh có hai hằng số: C một bằng hai, C hai bằng ba. Vậy kết quả là một cộng hai, cộng một cộng ba, bằng bảy.

**`x5`** — Mẹo nhận dạng nhanh. Thấy một chia x: viết lô ga nê pe trị tuyệt đối x, đừng quên trị tuyệt đối. Thấy e mũ x: giữ nguyên. Thấy a mũ x: giữ nguyên rồi chia lô ga nê pe a. Còn nếu biến nằm ở cơ số, quay về quy tắc lũy thừa.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba công thức. Nguyên hàm của một chia x là lô ga nê pe trị tuyệt đối x cộng C, xét trên từng khoảng. Nguyên hàm của e mũ x là e mũ x cộng C. Nguyên hàm của a mũ x là a mũ x chia lô ga nê pe a cộng C.

**`o2`** — Bài tập tự luyện. Một, tìm nguyên hàm của bốn chia x trừ e mũ x. Hai, tìm nguyên hàm của ba mũ x nhân hai mũ x, gợi ý: gộp hai cơ số. Ba, biết F phẩy bằng e mũ x cộng hai x và F của không bằng ba, tính F của một. Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập bốn, ta sẽ xây dựng nguyên hàm của các hàm số lượng giác sin, cos và các hàm liên quan. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. Tìm ∫(4/x − eˣ) dx. → **4 ln|x| − eˣ + C**
2. Tìm ∫3ˣ·2ˣ dx. → **6ˣ/ln 6 + C**
3. Biết F'(x) = eˣ + 2x, F(0) = 3. Tính F(1). → **F(1) = e + 3**
