# INT07 – Nguyên hàm phân thức hữu tỉ: Chia đa thức & tách phân thức

> Sinh tự động từ `int07/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int07`.

**Số nhịp:** 22 · **Số công thức Typst:** 47 · **Từ:** 1325

## Mở đầu

### ⏱ Mở đầu: phân thức không có trong bảng

**`h1`** — Nguyên hàm của x bình phương cộng một, chia cho x trừ một. Hàm này không có trong bảng nguyên hàm, và cũng không phải tổng các lũy thừa đơn giản. Nhưng chỉ với hai công cụ là chia đa thức và tách phân thức, ta sẽ đưa mọi phân thức như vậy về các hạng tử quen thuộc trong bảng.

**`h2`** — Đây là tập bảy của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: nguyên hàm phân thức hữu tỉ. Đây là nội dung mở rộng, ngoài chương trình bắt buộc, rất hữu ích cho học sinh giỏi và các kỳ thi đánh giá năng lực.

**`h3`** — Sau video này, em sẽ có ba kỹ năng. Một, chia đa thức khi bậc của tử lớn hơn hoặc bằng bậc của mẫu. Hai, tách phân thức thành các phân thức đơn giản bằng hệ số bất định và mẹo che nghiệm. Ba, nhận ra dạng tử số là đạo hàm của mẫu số.

## Bản chất

### ⏱ Bước 1: so sánh bậc và chia đa thức

**`c1`** — Bước đầu tiên luôn là so sánh bậc. Nếu bậc của tử nhỏ hơn bậc của mẫu, phân thức gọi là thực sự, ta tách ngay. Nếu bậc của tử lớn hơn hoặc bằng bậc của mẫu, ta phải chia đa thức trước, giống như đổi phân số tối giản thành hỗn số.

**`c2`** — Với x bình phương cộng một chia x trừ một: viết x bình phương cộng một bằng x trừ một nhân x cộng một, cộng hai. Vậy phân thức bằng x cộng một cộng hai chia x trừ một. Bây giờ mọi hạng tử đều có trong bảng: nguyên hàm là x bình phương chia hai cộng x cộng hai lô ga nê pe trị tuyệt đối x trừ một, cộng C.

**`c3`** — Trường hợp tử và mẫu cùng bậc một, ví dụ hai x cộng ba chia x cộng một. Tách tử theo mẫu: hai x cộng ba bằng hai nhân x cộng một, cộng một. Phân thức bằng hai cộng một chia x cộng một, và nguyên hàm là hai x cộng lô ga nê pe trị tuyệt đối x cộng một, cộng C.

### ⏱ Bước 2: tách phân thức

**`c4`** — Bước hai: tách phân thức thực sự. Với mẫu có hai nghiệm phân biệt, ví dụ x trừ một nhân x cộng hai, ta tách một chia tích đó thành hiệu hai phân thức đơn giản, nhân với một phần ba. Quy đồng lại để kiểm tra: tử số đúng bằng một.

**`c5`** — Tổng quát, dùng hệ số bất định. Viết ba x cộng một chia x trừ một nhân x cộng một bằng A chia x trừ một, cộng B chia x cộng một. Quy đồng: ba x cộng một bằng A nhân x cộng một, cộng B nhân x trừ một. Thay x bằng một: bốn bằng hai A, nên A bằng hai. Thay x bằng âm một: âm hai bằng âm hai B, nên B bằng một.

**`c6`** — Vậy nguyên hàm bằng hai lô ga nê pe trị tuyệt đối x trừ một cộng lô ga nê pe trị tuyệt đối x cộng một, cộng C. Mẹo nhanh, gọi là che nghiệm: muốn tìm A, che thừa số x trừ một ở mẫu, rồi thay x bằng một vào phần còn lại. Ba nhân một cộng một, chia một cộng một, bằng hai.

### ⏱ Mẫu có nghiệm kép

**`c7`** — Khi mẫu có nghiệm kép, ví dụ x trừ một tất cả bình phương, ta tách thành A chia x trừ một cộng B chia x trừ một bình phương. Với x chia x trừ một bình phương: x bằng x trừ một cộng một, nên được một chia x trừ một cộng một chia x trừ một bình phương. Nguyên hàm là lô ga nê pe trị tuyệt đối x trừ một, trừ một chia x trừ một, cộng C.

### ⏱ Tử số là đạo hàm của mẫu

**`c8`** — Một dạng đặc biệt cần nhận ra ngay: tử số là đạo hàm của mẫu số. Vì đạo hàm của lô ga nê pe trị tuyệt đối u bằng u phẩy chia u, nên nguyên hàm của u phẩy chia u là lô ga nê pe trị tuyệt đối u cộng C. Ví dụ, nguyên hàm của hai x chia x bình phương cộng một là lô ga nê pe của x bình phương cộng một.

### ⏱ Sơ đồ quyết định

**`c9`** — Tổng hợp thành sơ đồ quyết định. Bậc tử lớn hơn hoặc bằng bậc mẫu: chia đa thức. Tử là đạo hàm của mẫu: lô ga nê pe ngay. Mẫu có nghiệm phân biệt: tách A, B. Mẫu có nghiệm kép: thêm hạng tử bình phương.

## Ví dụ

### ⏱ Ví dụ 1: chia đa thức

**`e1`** — Ví dụ một: nguyên hàm của x lập phương trừ x cộng hai, chia x cộng một. Bậc tử lớn hơn, nên chia đa thức: x lập phương trừ x cộng hai bằng x cộng một nhân x bình phương trừ x, cộng hai. Nguyên hàm là x lập phương chia ba, trừ x bình phương chia hai, cộng hai lô ga nê pe trị tuyệt đối x cộng một, cộng C.

### ⏱ Ví dụ 2: tách bằng mẹo che nghiệm

**`e2`** — Ví dụ hai: nguyên hàm của năm x trừ một chia x bình phương trừ x trừ hai. Mẫu bằng x trừ hai nhân x cộng một. Che nghiệm: A bằng năm nhân hai trừ một, chia hai cộng một, bằng ba. B bằng âm năm trừ một, chia âm một trừ hai, bằng hai. Kết quả: ba lô ga nê pe trị tuyệt đối x trừ hai cộng hai lô ga nê pe trị tuyệt đối x cộng một, cộng C.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Cho hàm số f của x bằng hai x cộng một, chia x bình phương cộng x, trên khoảng dương. F là một nguyên hàm của f. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: quy đồng một chia x cộng một chia x cộng một, được đúng hai x cộng một chia x nhân x cộng một. Ý b đúng: tử số hai x cộng một chính là đạo hàm của mẫu x bình phương cộng x.

**`x3`** — Ý c sai: đây là cái bẫy nhân hai lô ga rít. Tổng hai lô ga rít là lô ga rít của tích, không phải tích hai lô ga rít. Ý d đúng: F của một bằng lô ga nê pe hai cộng C bằng lô ga nê pe hai nên C bằng không, và F của hai bằng lô ga nê pe sáu.

### ⏱ Trả lời ngắn và mẹo che nghiệm

**`x4`** — Câu trả lời ngắn. F là nguyên hàm của một chia x nhân x cộng một trên khoảng dương, F của một bằng không. Tính F của hai, làm tròn đến hàng phần trăm. Tách: một chia x trừ một chia x cộng một. F bằng lô ga nê pe của x chia x cộng một, cộng C, và C bằng lô ga nê pe hai. Vậy F của hai bằng lô ga nê pe bốn phần ba, xấp xỉ không phẩy hai chín.

**`x5`** — Mẹo che nghiệm, nhắc lại từng bước. Muốn tìm hệ số ứng với nghiệm a: che thừa số x trừ a ở mẫu, thay x bằng a vào phần còn lại. Chỉ mất vài giây cho mỗi hệ số, và chỉ dùng được khi các nghiệm phân biệt.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, bậc tử lớn hơn hoặc bằng bậc mẫu thì chia đa thức trước. Hai, mẫu phân tích được thì tách thành các phân thức đơn giản, dùng hệ số bất định hoặc che nghiệm. Ba, tử là đạo hàm của mẫu thì ra lô ga nê pe trị tuyệt đối mẫu ngay.

**`o2`** — Bài tập tự luyện. Một, nguyên hàm của x bình phương cộng x cộng một, chia x cộng một. Hai, nguyên hàm của một chia x bình phương trừ bốn. Ba, nguyên hàm của hai x chia x bình phương cộng ba. Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập tám, ta học phương pháp đổi biến số, công cụ mạnh nhất để xử lý các hàm hợp phức tạp. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. Tìm ∫(x² + x + 1)/(x + 1) dx. → **x²/2 + ln|x + 1| + C**
2. Tìm ∫1/(x² − 4) dx. → **(1/4) ln|(x − 2)/(x + 2)| + C**
3. Tìm ∫2x/(x² + 3) dx. → **ln(x² + 3) + C**
