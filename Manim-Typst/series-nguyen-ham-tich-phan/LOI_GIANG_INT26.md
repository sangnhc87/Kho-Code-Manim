# INT26 – Khối tròn xoay quanh Ox: Phương pháp đĩa: V = π∫f²(x)dx

> Sinh tự động từ `int26/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int26`.

**Số nhịp:** 25 · **Số công thức Typst:** 36 · **Từ:** 1166

## Mở đầu

### ⏱ Mở đầu: quay miền phẳng thành chiếc chén

**`h1`** — Lấy miền phẳng dưới đồ thị y bằng căn x, với x từ không đến bốn, rồi quay nó một vòng quanh trục hoành. Ta được một vật thể giống chiếc chén. Thể tích của nó là bao nhiêu? Đáp số là tám pi, và cách tính chỉ cần một tích phân.

**`h2`** — Đây là tập hai mươi sáu của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: thể tích khối tròn xoay quanh trục O x.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, công thức V bằng pi nhân tích phân của f bình phương, hiểu bằng các đĩa tròn mỏng. Hai, cách tránh những bẫy quen thuộc khi bình phương. Ba, dùng công thức để chứng minh thể tích hình nón và hình cầu.

## Bản chất

### ⏱ Thiết diện là hình tròn

**`c1`** — Khi quay miền dưới đồ thị y bằng f của x quanh trục O x, mỗi điểm trên đồ thị vạch ra một đường tròn. Vì vậy thiết diện vuông góc với trục tại x là một hình tròn bán kính trị tuyệt đối f của x. Diện tích thiết diện là pi nhân f bình phương.

### ⏱ Công thức V = π∫f²

**`c2`** — Áp dụng công thức của tập trước, thể tích bằng tích phân của diện tích thiết diện: V bằng pi nhân tích phân từ a đến b của f bình phương. Mỗi lát mỏng là một chiếc đĩa tròn, nên cách tính này gọi là phương pháp đĩa.

**`c2b`** — Đặt hai công thức cạnh nhau để khỏi nhầm. Diện tích miền phẳng là tích phân của trị tuyệt đối f, không có pi, không bình phương. Thể tích khi quay miền đó quanh O x là pi nhân tích phân của f bình phương. Đề thi thường hỏi cả hai trong cùng một câu đúng sai.

### ⏱ Quy trình bốn bước

**`c3`** — Quy trình bốn bước. Một, xác định hàm f và hai cận a, b. Hai, bình phương f, rút gọn. Ba, tính tích phân. Bốn, đừng quên nhân pi. Phần lớn lỗi sai nằm ở bước hai và bước bốn.

**`c4`** — Khi f âm, miền nằm dưới trục hoành, nhưng quay quanh trục vẫn cho cùng một khối, vì bán kính là trị tuyệt đối f, và bình phương đã xóa dấu. Không cần tách cận như khi tính diện tích.

### ⏱ Ba bẫy về bình phương

**`c5`** — Ba bẫy hay gặp. Một, quên bình phương, viết pi nhân tích phân của f. Hai, bình phương sai, ví dụ x cộng một bình phương thành x bình phương cộng một. Ba, bình phương cả tích phân, tức pi nhân bình phương của tích phân f, hoàn toàn khác pi nhân tích phân của f bình phương.

## Ví dụ

### ⏱ Ví dụ 1: chiếc chén

**`e1`** — Ví dụ một, giải bài mở đầu. f bằng căn x, f bình phương bằng x. Thể tích bằng pi nhân tích phân từ không đến bốn của x, bằng pi nhân tám, bằng tám pi.

### ⏱ Ví dụ 2: hình nón

**`e2`** — Ví dụ hai, chứng minh thể tích hình nón. Quay tam giác dưới đường y bằng r chia h nhân x, với x từ không đến h. Thể tích bằng pi nhân r bình phương chia h bình phương nhân tích phân của x bình phương, bằng một phần ba pi r bình phương h.

### ⏱ Ví dụ 3: hình cầu

**`e3`** — Ví dụ ba, chứng minh thể tích hình cầu. Quay nửa đường tròn y bằng căn của R bình phương trừ x bình phương quanh trục hoành. f bình phương bằng R bình phương trừ x bình phương, và tích phân từ trừ R đến R cho bốn phần ba R lập phương. Nhân pi: bốn phần ba pi R lập phương.

### ⏱ Ví dụ 4: hàm lượng giác

**`e4`** — Ví dụ bốn: quay miền dưới y bằng sin x, với x từ không đến pi. Sin bình phương x bằng một trừ cốt hai x, chia hai. Tích phân từ không đến pi bằng pi chia hai. Vậy thể tích bằng pi bình phương chia hai.

### ⏱ Ví dụ 5: hàm mũ

**`e5`** — Ví dụ năm: y bằng e mũ x, với x từ không đến một. f bình phương là e mũ hai x, nguyên hàm là e mũ hai x chia hai. Thể tích bằng pi nhân e bình phương trừ một, chia hai.

### ⏱ Ví dụ 6: miền dưới trục

**`e6`** — Ví dụ sáu: miền giới hạn bởi y bằng x bình phương trừ hai x và trục hoành nằm dưới trục. Không cần quan tâm dấu: bình phương lên rồi lấy tích phân từ không đến hai, được mười sáu phần mười lăm. Thể tích bằng mười sáu pi chia mười lăm.

### ⏱ Ví dụ 7: biết thể tích, tìm cận

**`e7`** — Dạng ngược: quay miền dưới y bằng căn x, với x từ không đến a, được khối có thể tích tám pi. Tìm a. Thể tích bằng pi nhân a bình phương chia hai. Cho bằng tám pi, ta được a bình phương bằng mười sáu, a bằng bốn.

**`e8`** — Mẹo kiểm tra bằng máy tính: nhập pi nhân tích phân của f bình phương. Ví dụ năm cho pi nhân e bình phương trừ một, chia hai, máy tính ra khoảng mười phẩy không bốn. Nếu đáp án trắc nghiệm ở dạng chính xác, hãy bấm từng phương án để so sánh.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Gọi H là hình phẳng giới hạn bởi y bằng hai x trừ x bình phương và trục hoành, V là thể tích khối tròn xoay khi quay H quanh O x. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: hai x trừ x bình phương bằng không tại x bằng không và x bằng hai. Ý b sai: đó là bẫy quên bình phương.

**`x3`** — Ý c đúng: đây chính là công thức đĩa. Ý d sai: tích phân của f bình phương bằng mười sáu phần mười lăm, nhưng thể tích phải nhân thêm pi, tức mười sáu pi chia mười lăm.

### ⏱ Câu trả lời ngắn

**`x4`** — Câu trả lời ngắn: quay miền dưới đồ thị y bằng một chia x, với x từ một đến ba, quanh trục hoành. Tính thể tích, làm tròn đến hàng phần trăm.

**`x5`** — f bình phương bằng một chia x bình phương, nguyên hàm là trừ một chia x. Tích phân từ một đến ba bằng một trừ một phần ba, bằng hai phần ba. Thể tích bằng hai pi chia ba, xấp xỉ hai phẩy không chín. Ghi vào phiếu: hai, phẩy, không, chín.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, quay quanh O x, thiết diện là hình tròn, thể tích bằng pi nhân tích phân của f bình phương. Hai, bình phương đúng, không bình phương cả tích phân, và nhớ nhân pi. Ba, công thức này chứng minh được thể tích hình nón và hình cầu.

**`o2`** — Bài tập tự luyện. Một, quay miền dưới y bằng x, với x từ không đến ba. Hai, quay nửa đường tròn y bằng căn bốn trừ x bình phương. Ba, quay miền dưới y bằng cốt x, với x từ không đến pi phần hai. Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập hai mươi bảy, ta quay miền nằm giữa hai đường cong, được những chiếc đĩa có lỗ ở giữa, gọi là vành khăn. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. Quay y = x, x ∈ [0; 3] → **9π**
2. Quay y = √(4 − x²) → **32π/3**
3. Quay y = cos x, x ∈ [0; π/2] → **π²/4**
