# INT23 – Diện tích có tham số: Hình ghép, chia đôi diện tích, tối ưu

> Sinh tự động từ `int23/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int23`.

**Số nhịp:** 23 · **Số công thức Typst:** 35 · **Từ:** 1213

## Mở đầu

### ⏱ Mở đầu: chia đôi diện tích

**`h1`** — Miền giới hạn bởi parabol y bằng bốn trừ x bình phương và trục hoành có diện tích ba mươi hai phần ba. Kéo một đường nằm ngang y bằng m từ dưới lên: phần phía trên nhỏ dần. Với m bằng bao nhiêu thì đường này chia miền thành hai phần bằng nhau? Đáp số xấp xỉ một phẩy bốn tám.

**`h2`** — Đây là tập hai mươi ba của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: diện tích hình ghép và bài toán tham số.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, tính diện tích hình ghép bằng cộng và trừ các miền đơn giản. Hai, biểu diễn diện tích thành hàm của tham số rồi giải phương trình. Ba, tìm tham số để diện tích nhỏ nhất, với công thức nhanh cho parabol và đường thẳng.

## Bản chất

### ⏱ Hình ghép: cộng và trừ

**`c1`** — Hình ghép: khi miền có hình dạng phức tạp, hãy chia nó thành các miền đơn giản rồi cộng lại, hoặc lấy một miền lớn trừ đi phần thừa. Ví dụ miền dưới căn x, trên đường thẳng x trừ hai và trên trục hoành bằng toàn bộ miền dưới căn x, trừ đi một tam giác.

### ⏱ Diện tích là hàm của tham số

**`c2`** — Tham số trong cận: diện tích giới hạn bởi y bằng x bình phương, trục hoành và x bằng a là S của a bằng a lập phương chia ba. Diện tích lúc này là một hàm của a. Đề cho S bằng chín thì ta giải a lập phương bằng hai mươi bảy, được a bằng ba.

**`c3`** — Tham số trong hàm: parabol y bằng x bình phương và đường thẳng y bằng m x, với m dương. Hai đồ thị cắt nhau tại không và m. Diện tích S của m bằng tích phân từ không đến m của m x trừ x bình phương, bằng m lập phương chia sáu. Kéo m lớn dần, diện tích tăng rất nhanh, theo lập phương.

### ⏱ Công thức nhanh a·d³/6

**`c4`** — Nhắc lại công thức nhanh từ tập trước: diện tích giữa parabol hệ số a và một đường thẳng cắt nó tại x một và x hai bằng trị tuyệt đối a nhân x hai trừ x một, mũ ba, chia sáu. Chỉ cần biết khoảng cách giữa hai giao điểm.

### ⏱ Tối ưu diện tích

**`c5`** — Bài toán tối ưu: đường thẳng đi qua điểm một, hai cắt parabol y bằng x bình phương tại hai điểm. Khi xoay đường thẳng, khoảng cách hai giao điểm thay đổi, và diện tích cũng thay đổi. Diện tích nhỏ nhất khi khoảng cách đó nhỏ nhất.

## Ví dụ

### ⏱ Ví dụ 1: tìm m theo diện tích

**`e1`** — Ví dụ một: tìm m dương để diện tích giới hạn bởi y bằng x bình phương và y bằng m x bằng bốn phần ba. Ta có m lập phương chia sáu bằng bốn phần ba, nên m lập phương bằng tám, m bằng hai.

### ⏱ Ví dụ 2: tham số trong cận

**`e2`** — Ví dụ hai: tìm a dương để diện tích giới hạn bởi y bằng e mũ x, trục hoành, x bằng không và x bằng a, bằng e bình phương trừ một. Diện tích bằng e mũ a trừ một. Giải ra a bằng hai.

### ⏱ Ví dụ 3: giải bài mở đầu

**`e3`** — Ví dụ ba, giải bài mở đầu. Phần phía trên đường y bằng m là miền giữa parabol và đường nằm ngang, hai giao điểm cách nhau hai căn của bốn trừ m. Theo công thức nhanh, diện tích bằng bốn phần ba nhân bốn trừ m, mũ ba phần hai. Cho bằng một nửa của ba mươi hai phần ba, tức mười sáu phần ba.

**`e4`** — Ta được bốn trừ m, mũ ba phần hai, bằng bốn. Suy ra bốn trừ m bằng căn bậc ba của mười sáu, bằng hai căn bậc ba của hai. Vậy m bằng bốn trừ hai căn bậc ba của hai, xấp xỉ một phẩy bốn tám. Đường chia đôi không nằm giữa chiều cao, mà thấp hơn, vì phần dưới rộng hơn.

### ⏱ Ví dụ 4: diện tích nhỏ nhất

**`e5`** — Ví dụ bốn, tối ưu. Đường thẳng qua điểm một, hai có hệ số góc k: y bằng k nhân x trừ một, cộng hai. Phương trình hoành độ giao điểm là x bình phương trừ k x cộng k trừ hai bằng không, có biệt thức bằng k bình phương trừ bốn k cộng tám.

**`e6`** — Khoảng cách hai giao điểm bằng căn của biệt thức. Diện tích bằng biệt thức mũ ba phần hai, chia sáu. Biệt thức bằng k trừ hai, bình phương, cộng bốn, nhỏ nhất bằng bốn khi k bằng hai. Vậy diện tích nhỏ nhất bằng tám chia sáu, bằng bốn phần ba.

### ⏱ Ví dụ 5: hình ghép

**`e7`** — Ví dụ năm, hình ghép: miền giới hạn bởi y bằng căn x, y bằng x trừ hai và trục hoành. Lấy diện tích dưới căn x từ không đến bốn, bằng mười sáu phần ba, trừ đi tam giác dưới đường thẳng từ hai đến bốn, bằng hai. Kết quả mười phần ba.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Cho parabol y bằng x bình phương và đường thẳng y bằng m x, với m dương. Gọi S của m là diện tích hình phẳng giới hạn bởi hai đường. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: x bình phương bằng m x cho x bằng không hoặc x bằng m. Ý b đúng: tích phân từ không đến m của m x trừ x bình phương bằng m lập phương chia sáu.

**`x3`** — Ý c sai: gấp đôi m thì diện tích gấp tám lần, vì diện tích tỉ lệ với m lập phương. Ý d đúng: m lập phương chia sáu bằng ba mươi sáu cho m lập phương bằng hai trăm mười sáu, m bằng sáu.

### ⏱ Câu trả lời ngắn

**`x4`** — Câu trả lời ngắn: đường thẳng y bằng k x cộng một cắt parabol y bằng x bình phương tại hai điểm. Tìm giá trị nhỏ nhất của diện tích hình phẳng giới hạn bởi hai đường, làm tròn đến hàng phần trăm.

**`x5`** — Phương trình x bình phương trừ k x trừ một bằng không có biệt thức k bình phương cộng bốn. Diện tích bằng k bình phương cộng bốn, mũ ba phần hai, chia sáu, nhỏ nhất khi k bằng không: tám chia sáu, xấp xỉ một phẩy ba ba. Ghi vào phiếu: một, phẩy, ba, ba.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, hình ghép: cộng các miền đơn giản hoặc lấy miền lớn trừ phần thừa. Hai, tham số: viết diện tích thành hàm S của m, rồi giải phương trình. Ba, tối ưu: với parabol và đường thẳng, dùng công thức a nhân d lập phương chia sáu, rồi tìm d nhỏ nhất.

**`o2`** — Bài tập tự luyện. Một, tìm m trong khoảng không đến hai để diện tích giữa y bằng hai x trừ x bình phương và y bằng m x bằng một phần sáu. Hai, tìm a dương để diện tích dưới e mũ x từ không đến a bằng e bình phương trừ một. Ba, đường y bằng m chia đôi miền giữa y bằng x bình phương và y bằng bốn. Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập hai mươi bốn, ta đọc diện tích từ đồ thị của đạo hàm để so sánh các giá trị của f, một dạng vận dụng cao rất được yêu thích. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. y = 2x − x² và y = mx (0 < m < 2), S = 1/6: tìm m → **m = 1**
2. ∫₀ᵃ eˣ dx = e² − 1: tìm a > 0 → **a = 2**
3. y = m chia đôi miền giữa y = x² và y = 4 → **m = 2∛2**
