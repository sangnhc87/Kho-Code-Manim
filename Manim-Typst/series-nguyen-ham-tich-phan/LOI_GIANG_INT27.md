# INT27 – Khối tròn xoay giữa hai đường: Vành khăn: khối ngoài trừ khối trong

> Sinh tự động từ `int27/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int27`.

**Số nhịp:** 24 · **Số công thức Typst:** 40 · **Từ:** 1164

## Mở đầu

### ⏱ Mở đầu: một lỗi rất phổ biến

**`h1`** — Quay miền nằm giữa đường thẳng y bằng x và parabol y bằng x bình phương quanh trục hoành. Rất nhiều bạn viết pi nhân tích phân của x trừ x bình phương, bình phương, và được pi chia ba mươi. Đáp số đúng là hai pi chia mười lăm, lớn gấp bốn lần. Sai ở đâu?

**`h2`** — Đây là tập hai mươi bảy của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: khối tròn xoay giữa hai đường.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, thiết diện là vành khăn, một chiếc đĩa bị khoét lỗ ở giữa. Hai, công thức pi nhân tích phân của f bình phương trừ g bình phương. Ba, vì sao bình phương của hiệu là một cái bẫy.

## Bản chất

### ⏱ Thiết diện là vành khăn

**`c1`** — Khi quay miền giữa hai đồ thị y bằng f và y bằng g, với f lớn hơn g và cả hai không âm, mỗi lát cắt vuông góc với trục là một vành khăn: hình tròn lớn bán kính f bị khoét đi hình tròn nhỏ bán kính g.

### ⏱ Công thức vành khăn

**`c2`** — Diện tích vành khăn bằng diện tích hình tròn lớn trừ hình tròn nhỏ: pi f bình phương trừ pi g bình phương. Lấy tích phân, ta được V bằng pi nhân tích phân từ a đến b của f bình phương trừ g bình phương. Nói cách khác: thể tích khối ngoài trừ thể tích khối trong.

### ⏱ Bẫy bình phương của hiệu

**`c3`** — Cái bẫy: f bình phương trừ g bình phương không bằng f trừ g, bình phương. Về hình học, f trừ g là bề dày của vành khăn. Bình phương của bề dày cho diện tích một hình tròn nhỏ, chứ không phải diện tích vành khăn, vì vành khăn nằm xa trục và rộng hơn nhiều.

**`c3b`** — Thử với số cụ thể: vành khăn có bán kính ngoài hai, bán kính trong một. Diện tích đúng là pi nhân bốn trừ một, bằng ba pi. Còn pi nhân hai trừ một, bình phương, chỉ bằng pi, nhỏ hơn ba lần. Một phép thử nhỏ như vậy giúp em nhớ mãi.

### ⏱ Quy trình bốn bước

**`c4`** — Quy trình bốn bước. Một, tìm giao điểm để có cận. Hai, xác định đường ngoài, là đường xa trục hơn, và đường trong. Ba, bình phương từng hàm rồi mới trừ. Bốn, tính tích phân và nhân pi.

**`c5`** — Lưu ý: công thức này dùng khi miền nằm hoàn toàn một phía của trục hoành. Đề thi trong chương trình mới hầu như luôn cho miền như vậy. Nếu cả hai hàm đều âm, ta lấy trị tuyệt đối: đường ngoài vẫn là đường xa trục hơn.

## Ví dụ

### ⏱ Ví dụ 1: bài mở đầu

**`e1`** — Ví dụ một, giải bài mở đầu. Giao điểm tại không và một. Trên đoạn này x lớn hơn x bình phương, nên đường ngoài là y bằng x. Thể tích bằng pi nhân tích phân của x bình phương trừ x mũ bốn, bằng pi nhân một phần ba trừ một phần năm, bằng hai pi chia mười lăm.

**`e2`** — So sánh với cách sai: pi nhân tích phân của x trừ x bình phương, bình phương, chỉ bằng pi chia ba mươi, bằng một phần tư đáp số đúng. Sai lệch lớn như vậy, nên trắc nghiệm thường đặt đúng phương án sai này để bẫy.

### ⏱ Ví dụ 2: chiếc lá quay

**`e3`** — Ví dụ hai: y bằng căn x và y bằng x bình phương, giao tại không và một. Đường ngoài là căn x. Thể tích bằng pi nhân tích phân của x trừ x mũ bốn, bằng ba pi chia mười.

### ⏱ Ví dụ 3: hai parabol

**`e4`** — Ví dụ ba: y bằng ba trừ x bình phương và y bằng x bình phương cộng một, giao tại trừ một và một. Đường ngoài là ba trừ x bình phương. Hiệu bình phương rút gọn được tám trừ tám x bình phương. Thể tích bằng ba mươi hai pi chia ba.

### ⏱ Ví dụ 4: có đường nằm ngang

**`e5`** — Ví dụ bốn: y bằng e mũ x, y bằng một và x bằng một. Với x từ không đến một, e mũ x lớn hơn một, là đường ngoài. Thể tích bằng pi nhân tích phân của e mũ hai x trừ một, bằng pi nhân e bình phương trừ ba, chia hai.

**`e6`** — Cách nhìn khác cho mọi bài vành khăn: thể tích bằng khối ngoài trừ khối trong. Ở ví dụ bốn, khối ngoài là khối quay e mũ x, khối trong là hình trụ bán kính một, cao một, thể tích pi. Lấy pi nhân e bình phương trừ một chia hai, trừ pi, được cùng kết quả.

### ⏱ Chọn đúng công thức

**`e7`** — Luyện phản xạ chọn công thức. Quay miền dưới một đường cong: dùng đĩa, pi nhân tích phân f bình phương. Quay miền giữa hai đường không cắt trục: dùng vành khăn, pi nhân tích phân f bình phương trừ g bình phương. Hỏi diện tích miền phẳng: không có pi, tích phân của trị tuyệt đối f trừ g. Ba công thức, ba tình huống.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Quay miền giới hạn bởi y bằng hai x và y bằng x bình phương quanh trục hoành, được khối có thể tích V. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: hai x bằng x bình phương tại không và hai. Ý b đúng: thử x bằng một, đường thẳng bằng hai, parabol bằng một.

**`x3`** — Ý c sai: đó chính là bẫy bình phương của hiệu. Ý d đúng: pi nhân tích phân của bốn x bình phương trừ x mũ bốn bằng pi nhân ba mươi hai phần ba trừ ba mươi hai phần năm, bằng sáu mươi tư pi chia mười lăm.

### ⏱ Câu trả lời ngắn

**`x4`** — Câu trả lời ngắn: quay miền giới hạn bởi y bằng căn x và y bằng x chia hai quanh trục hoành. Tính thể tích, làm tròn đến hàng phần trăm. Hai đường giao tại không và bốn.

**`x5`** — Trên đoạn từ không đến bốn, căn x lớn hơn x chia hai. Thể tích bằng pi nhân tích phân của x trừ x bình phương chia bốn, bằng pi nhân tám trừ mười sáu phần ba, bằng tám pi chia ba, xấp xỉ tám phẩy ba tám. Ghi vào phiếu: tám, phẩy, ba, tám.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, quay miền giữa hai đường, thiết diện là vành khăn. Hai, thể tích bằng pi nhân tích phân của f bình phương trừ g bình phương, hay khối ngoài trừ khối trong. Ba, tuyệt đối không viết bình phương của hiệu.

**`o2`** — Bài tập tự luyện. Một, quay miền giữa y bằng x và y bằng x lập phương, với x từ không đến một. Hai, quay miền giữa y bằng một và y bằng x bình phương. Ba, quay miền giữa y bằng căn x và y bằng một, với x từ một đến bốn. Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập hai mươi tám, ta dùng tích phân để dựng lại các công thức thể tích quen thuộc: hình nón, hình cầu và chỏm cầu. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. Quay miền giữa y = x và y = x³, x ∈ [0; 1] → **4π/21**
2. Quay miền giữa y = 1 và y = x² → **8π/5**
3. Quay miền giữa y = √x và y = 1, x ∈ [1; 4] → **9π/2**
