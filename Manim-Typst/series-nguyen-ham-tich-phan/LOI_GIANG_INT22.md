# INT22 – Diện tích giữa hai đường cong: Tìm giao điểm, chia khoảng, trên trừ dưới

> Sinh tự động từ `int22/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int22`.

**Số nhịp:** 24 · **Số công thức Typst:** 38 · **Từ:** 1189

## Mở đầu

### ⏱ Mở đầu: chiếc thuyền giữa parabol và đường thẳng

**`h1`** — Parabol y bằng x bình phương và đường thẳng y bằng x cộng hai cắt nhau, tạo thành một miền giống chiếc thuyền. Diện tích chiếc thuyền đó bằng bao nhiêu? Đáp số là chín phần hai. Hôm nay ta học cách tính diện tích của mọi miền nằm giữa hai đường cong.

**`h2`** — Đây là tập hai mươi hai của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: diện tích giữa hai đường cong.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, công thức tích phân của trị tuyệt đối hiệu hai hàm, hiểu bằng dải mỏng trên trừ dưới. Hai, quy trình: tìm giao điểm, chia khoảng, xác định đường nào ở trên. Ba, các miền phức tạp hơn, kể cả khi nên tính tích phân theo biến y.

## Bản chất

### ⏱ Công thức diện tích giữa hai đường

**`c1`** — Cho hai hàm f và g liên tục trên đoạn từ a đến b. Diện tích hình phẳng giới hạn bởi hai đồ thị và hai đường thẳng x bằng a, x bằng b là S bằng tích phân từ a đến b của trị tuyệt đối f trừ g. Khi g bằng không, ta trở về công thức của tập hai mươi mốt.

### ⏱ Dải mỏng: trên trừ dưới

**`c2`** — Hình dung một dải mỏng thẳng đứng quét từ trái sang phải. Chiều cao của dải là khoảng cách giữa hai đồ thị: đường trên trừ đường dưới. Cộng dồn diện tích các dải, ta được tích phân của trên trừ dưới.

**`c3`** — Một điều thú vị: vị trí của trục hoành không quan trọng. Nếu dời cả hai đồ thị lên hoặc xuống cùng một đoạn, hiệu trên trừ dưới không đổi, nên diện tích không đổi. Vì vậy ta không cần quan tâm miền nằm trên hay dưới trục.

### ⏱ Quy trình ba bước

**`c4`** — Quy trình ba bước. Một, giải phương trình f bằng g để tìm hoành độ giao điểm. Hai, trên mỗi khoảng giữa hai giao điểm, xác định đường nào nằm trên, bằng cách thử một điểm. Ba, tính tích phân của trên trừ dưới trên từng khoảng rồi cộng lại.

**`c5`** — Khi hai đồ thị cắt nhau nhiều lần, vai trò trên và dưới đổi chỗ sau mỗi giao điểm. Nếu dùng một tích phân cho cả đoạn mà không có trị tuyệt đối, các phần sẽ triệt tiêu nhau như ở tập trước.

### ⏱ Bẫy thường gặp

**`c6`** — Ba bẫy thường gặp. Một, lấy dưới trừ trên, ra số âm. Hai, quên tách khoảng khi hai đường cắt nhau ở giữa. Ba, nhầm với công thức thể tích, viết bình phương của f trừ g. Diện tích chỉ cần hiệu, không bình phương.

## Ví dụ

### ⏱ Ví dụ 1: parabol và đường thẳng

**`e1`** — Ví dụ một, giải bài mở đầu. x bình phương bằng x cộng hai cho x bằng trừ một và x bằng hai. Thử x bằng không: đường thẳng bằng hai, parabol bằng không, vậy đường thẳng ở trên. Diện tích bằng tích phân từ trừ một đến hai của x cộng hai trừ x bình phương, bằng chín phần hai.

### ⏱ Ví dụ 2: đổi vai trên dưới

**`e2`** — Ví dụ hai: y bằng x lập phương và y bằng x. Giao tại trừ một, không và một. Trên khoảng từ trừ một đến không, đường cong bậc ba ở trên; từ không đến một, đường thẳng ở trên. Mỗi phần bằng một phần tư, tổng bằng một phần hai.

### ⏱ Ví dụ 3: chiếc lá

**`e3`** — Ví dụ ba: y bằng căn x và y bằng x bình phương. Giao tại không và một. Trên đoạn này căn x ở trên. Diện tích bằng tích phân của căn x trừ x bình phương, bằng hai phần ba trừ một phần ba, bằng một phần ba. Miền này có hình chiếc lá, đối xứng qua đường y bằng x.

### ⏱ Ví dụ 4: có đường nằm ngang

**`e4`** — Ví dụ bốn: y bằng e mũ x, y bằng e và trục tung. Đường nằm ngang y bằng e cắt e mũ x tại x bằng một, và trục tung là x bằng không. Diện tích bằng tích phân từ không đến một của e trừ e mũ x, bằng e trừ, e trừ một, bằng một.

### ⏱ Ví dụ 5: biên thay đổi

**`e5`** — Ví dụ năm: miền giới hạn bởi y bằng căn x, y bằng hai trừ x và trục hoành. Biên dưới luôn là trục hoành, nhưng biên trên đổi từ căn x sang hai trừ x tại x bằng một. Chia hai khoảng: hai phần ba cộng một phần hai, bằng bảy phần sáu.

### ⏱ Ví dụ 6: tích phân theo y

**`e6`** — Cách khác cho ví dụ năm: tính theo y. Với y từ không đến một, biên trái là x bằng y bình phương, biên phải là x bằng hai trừ y. Diện tích bằng tích phân của phải trừ trái theo d y, bằng hai trừ một phần hai trừ một phần ba, cũng bằng bảy phần sáu, mà chỉ cần một tích phân.

### ⏱ Ví dụ 7: parabol và tiếp tuyến

**`e7`** — Ví dụ bảy, dạng rất hay gặp: parabol y bằng x bình phương, tiếp tuyến của nó tại điểm một, một, và trục tung. Tiếp tuyến là y bằng hai x trừ một. Parabol luôn nằm trên tiếp tuyến, hiệu bằng x trừ một, bình phương. Diện tích bằng tích phân từ không đến một của x trừ một bình phương, bằng một phần ba.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Gọi D là hình phẳng giới hạn bởi y bằng x bình phương trừ hai x và y bằng x. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: x bình phương trừ hai x bằng x cho x bằng không hoặc x bằng ba. Ý b đúng: thử x bằng một, đường thẳng bằng một, parabol bằng trừ một, đường thẳng ở trên.

**`x3`** — Ý c đúng: đó chính là công thức tích phân của trị tuyệt đối hiệu. Ý d sai: tích phân từ không đến ba của ba x trừ x bình phương bằng chín phần hai, không phải chín.

### ⏱ Câu trả lời ngắn

**`x4`** — Câu trả lời ngắn: tính diện tích hình phẳng giới hạn bởi y bằng x bình phương và y bằng x cộng sáu, làm tròn đến hàng phần mười. Giao điểm tại x bằng trừ hai và x bằng ba.

**`x5`** — Đường thẳng ở trên. Diện tích bằng tích phân từ trừ hai đến ba của x cộng sáu trừ x bình phương, bằng một trăm hai mươi lăm phần sáu, xấp xỉ hai mươi phẩy tám. Ghi vào phiếu: hai, không, phẩy, tám. Mẹo: với parabol và đường thẳng, diện tích bằng hệ số a nhân độ dài khoảng mũ ba, chia sáu.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, diện tích bằng tích phân của trị tuyệt đối f trừ g, hiểu là trên trừ dưới. Hai, quy trình: giao điểm, chia khoảng, thử điểm để biết đường nào ở trên. Ba, khi biên thay đổi, chia khoảng hoặc chuyển sang tích phân theo y.

**`o2`** — Bài tập tự luyện. Một, y bằng x bình phương và y bằng hai x. Hai, y bằng x lập phương và y bằng bốn x. Ba, y bằng căn x và y bằng x. Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập hai mươi ba, ta gặp các bài diện tích có tham số: kéo tham số để diện tích thay đổi, tìm giá trị làm hai phần bằng nhau. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. y = x² và y = 2x → **4/3**
2. y = x³ và y = 4x → **8**
3. y = √x và y = x → **1/6**
