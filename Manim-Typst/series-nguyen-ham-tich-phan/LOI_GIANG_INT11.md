# INT11 – Diện tích dưới đường cong: Tổng Riemann – vì sao tích phân là diện tích

> Sinh tự động từ `int11/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int11`.

**Số nhịp:** 23 · **Số công thức Typst:** 36 · **Từ:** 1250

## Mở đầu

### ⏱ Mở đầu: quãng đường là diện tích

**`h1`** — Nếu một chiếc xe chạy đều sáu mét mỗi giây trong ba giây, quãng đường là sáu nhân ba bằng mười tám mét. Trên đồ thị vận tốc, con số đó chính là diện tích hình chữ nhật dưới đường vận tốc. Nhưng nếu vận tốc thay đổi liên tục, đồ thị là một đường cong. Làm sao tính diện tích dưới một đường cong?

**`h2`** — Chào mừng các em đến với Phần B của series: tích phân. Tập mười một: diện tích dưới đường cong và tổng Riemann, lời giải thích vì sao tích phân chính là diện tích.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, cách xấp xỉ diện tích bằng các hình chữ nhật mảnh, gọi là tổng Riemann. Hai, khi các hình chữ nhật mảnh dần, tổng tiến tới diện tích thật. Ba, một bất ngờ lớn: diện tích đó tính được bằng nguyên hàm.

## Bản chất

### ⏱ Từ hình chữ nhật đến đường cong

**`c1`** — Bắt đầu từ trường hợp dễ nhất. Vận tốc không đổi bằng sáu: đồ thị là đường nằm ngang, và miền dưới nó từ không đến ba là một hình chữ nhật. Diện tích bằng chiều cao sáu nhân chiều rộng ba, đúng bằng quãng đường mười tám mét.

**`c2`** — Nếu vận tốc thay đổi theo từng bậc, mỗi đoạn một giá trị, thì quãng đường là tổng diện tích của nhiều hình chữ nhật. Ý tưởng then chốt: một đường cong bất kỳ có thể được xấp xỉ bằng các bậc thang như vậy.

### ⏱ Tổng Riemann

**`c3`** — Xét f của x bằng x bình phương trên đoạn từ không đến hai. Chia đoạn thành n phần bằng nhau, mỗi phần rộng đen ta x bằng hai chia n. Trên mỗi phần, dựng hình chữ nhật có chiều cao bằng giá trị của f tại mút phải. Tổng diện tích các hình chữ nhật gọi là tổng Riemann.

**`c4`** — Với bốn hình chữ nhật, tổng phải bằng ba phẩy bảy lăm, lớn hơn diện tích thật vì các hình nhô lên trên đường cong. Tăng lên tám hình: ba phẩy một tám. Mười sáu hình: hai phẩy chín hai. Sáu mươi tư hình: hai phẩy bảy ba. Phần thừa ngày càng nhỏ.

### ⏱ Kẹp giữa tổng trái và tổng phải

**`c5`** — Làm tương tự với mút trái, các hình chữ nhật nằm dưới đường cong, nên tổng nhỏ hơn diện tích thật. Diện tích thật bị kẹp giữa tổng trái và tổng phải. Khi n tiến ra vô cùng, cả hai tổng cùng tiến tới một số duy nhất: tám phần ba, xấp xỉ hai phẩy sáu sáu bảy.

### ⏱ Tổng điểm giữa

**`c5b`** — Còn một cách chọn chiều cao khôn ngoan hơn: lấy giá trị tại điểm giữa mỗi đoạn. Mỗi hình chữ nhật vừa nhô lên một chút, vừa hụt xuống một chút, phần thừa và phần thiếu bù trừ cho nhau. Chỉ với bốn hình, tổng điểm giữa đã bằng hai phẩy sáu hai lăm, rất sát giá trị đúng hai phẩy sáu sáu bảy.

### ⏱ Bất ngờ: diện tích bằng nguyên hàm

**`c6`** — Và đây là điều bất ngờ. Lấy một nguyên hàm của x bình phương, là x lập phương chia ba. Tính hiệu tại hai đầu mút: tám phần ba trừ không, bằng tám phần ba. Đúng bằng giới hạn của các tổng Riemann! Diện tích dưới đường cong được tính bằng nguyên hàm.

**`c7`** — Vì sao lại như vậy? Gọi S của x là diện tích từ a đến x. Khi x tăng thêm một lượng nhỏ h, diện tích tăng thêm một dải mảnh, xấp xỉ f của x nhân h. Vậy S phẩy bằng f: hàm diện tích chính là một nguyên hàm của f. Đó là cầu nối giữa Phần A và Phần B.

### ⏱ Kí hiệu tích phân

**`c8`** — Từ đây ta có kí hiệu tích phân từ a đến b của f của x d x. Dấu tích phân là chữ S kéo dài, nghĩa là tổng, còn d x là chiều rộng vô cùng nhỏ của mỗi hình chữ nhật. Tập sau, ta sẽ định nghĩa chính xác và học công thức Newton Leibniz.

## Ví dụ

### ⏱ Ví dụ 1: ước lượng từ bảng số liệu

**`e1`** — Ví dụ một, dạng bài thực tế. Bảng đo vận tốc của một vật mỗi giây: không, ba, tám, mười lăm, hai mươi tư mét mỗi giây, tại t bằng không, một, hai, ba, bốn. Ước lượng quãng đường trong bốn giây. Tổng trái là không cộng ba cộng tám cộng mười lăm, bằng hai mươi sáu. Tổng phải là ba cộng tám cộng mười lăm cộng hai mươi tư, bằng năm mươi.

**`e2`** — Vận tốc tăng dần nên quãng đường thật nằm giữa hai mươi sáu và năm mươi mét. Trung bình hai tổng là ba mươi tám. Nếu biết công thức v bằng t bình phương cộng hai t, nguyên hàm cho giá trị chính xác ba mươi bảy phẩy ba ba mét.

### ⏱ Ví dụ 2: kiểm tra bằng tam giác

**`e3`** — Ví dụ hai, kiểm tra với hình quen thuộc. Diện tích dưới đường y bằng x từ không đến hai là một tam giác, bằng một nửa nhân hai nhân hai, bằng hai. Dùng nguyên hàm x bình phương chia hai: bốn chia hai trừ không, cũng bằng hai. Hai cách cho cùng một kết quả.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Cho f của x bằng hai x trên đoạn từ không đến ba, chia thành ba đoạn con bằng nhau. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: ba chia ba bằng một. Ý b đúng: các mút phải là một, hai, ba, nên tổng phải bằng hai cộng bốn cộng sáu, nhân một, bằng mười hai.

**`x3`** — Ý c đúng: các mút trái là không, một, hai, tổng trái bằng không cộng hai cộng bốn, bằng sáu. Ý d sai: diện tích thật là một tam giác, bằng một nửa nhân ba nhân sáu, bằng chín, nằm giữa sáu và mười hai.

### ⏱ Trả lời ngắn và mẹo kẹp

**`x4`** — Câu trả lời ngắn. Tính tổng Riemann phải với bốn hình chữ nhật cho f của x bằng x bình phương trên đoạn không đến hai. Đen ta x bằng không phẩy năm, các mút phải là không phẩy năm, một, một phẩy năm, hai. Tổng bằng không phẩy năm nhân không phẩy hai lăm cộng một cộng hai phẩy hai lăm cộng bốn, bằng ba phẩy bảy lăm.

**`x5`** — Mẹo nhận định nhanh: nếu hàm số tăng, tổng trái nhỏ hơn diện tích và tổng phải lớn hơn. Nếu hàm số giảm thì ngược lại. Câu đúng sai thường hỏi chính điều này. Hãy nhìn hai hình: với hàm tăng, các hình chữ nhật điểm trái nằm gọn dưới đường cong; với hàm giảm, chúng lại nhô lên trên. Chỉ cần xác định chiều biến thiên là biết ngay chiều của bất đẳng thức.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, diện tích dưới đường cong được xấp xỉ bằng tổng các hình chữ nhật mảnh, tổng Riemann. Hai, khi số hình chữ nhật tiến ra vô cùng, tổng tiến tới diện tích thật. Ba, diện tích đó bằng hiệu giá trị của một nguyên hàm tại hai đầu mút.

**`o2`** — Bài tập tự luyện. Một, tính tổng Riemann phải với bốn hình chữ nhật cho f bằng x cộng một trên đoạn không đến hai. Hai, dùng nguyên hàm tính diện tích dưới y bằng ba x bình phương trên đoạn không đến một. Ba, vận tốc đo tại t bằng không, hai, bốn, sáu phút là mười, mười bốn, mười sáu, mười tám mét mỗi phút, ước lượng quãng đường bằng tổng trái.

**`o3`** — Tập mười hai sẽ định nghĩa chính xác tích phân bằng công thức Newton Leibniz, và giải thích diện tích có dấu. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. f(x) = x + 1 trên [0; 2], n = 4: tổng Riemann phải. → **R₄ = 4,5**
2. Diện tích dưới y = 3x² trên [0; 1]. → **S = 1**
3. v(0), v(2), v(4), v(6) = 10, 14, 16, 18 m/phút: tổng trái. → **80 m**
