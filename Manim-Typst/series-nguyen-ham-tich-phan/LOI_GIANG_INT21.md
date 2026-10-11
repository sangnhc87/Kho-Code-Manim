# INT21 – Diện tích hình phẳng với trục Ox: Diện tích luôn dương: xét dấu rồi tách cận

> Sinh tự động từ `int21/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int21`.

**Số nhịp:** 24 · **Số công thức Typst:** 40 · **Từ:** 1232

## Mở đầu

### ⏱ Mở đầu: tích phân bằng 0, diện tích khác 0

**`h1`** — Tính diện tích hình phẳng giới hạn bởi đồ thị y bằng x bình phương trừ hai x, trục hoành, và hai đường thẳng x bằng không, x bằng ba. Nếu lấy tích phân từ không đến ba, ta được đúng bằng không! Nhưng trên hình rõ ràng có hai mảnh diện tích. Diện tích thật là tám phần ba.

**`h2`** — Đây là tập hai mươi mốt, mở đầu phần C của series: ứng dụng hình học của tích phân. Chủ đề hôm nay: diện tích hình phẳng giới hạn bởi đồ thị và trục hoành.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, công thức S bằng tích phân của trị tuyệt đối f. Hai, cách xác định cận khi đề không cho sẵn hai đường thẳng đứng. Ba, các bẫy thường gặp, đặc biệt là quên trị tuyệt đối.

## Bản chất

### ⏱ Công thức diện tích

**`c1`** — Cho hàm f liên tục trên đoạn từ a đến b. Hình phẳng giới hạn bởi đồ thị y bằng f của x, trục hoành, và hai đường thẳng x bằng a, x bằng b có diện tích S bằng tích phân từ a đến b của trị tuyệt đối f của x.

**`c2`** — Vì sao có trị tuyệt đối? Chia miền thành các dải hẹp. Mỗi dải có chiều cao là khoảng cách từ đồ thị đến trục, tức là trị tuyệt đối của f, luôn dương. Còn tích phân thường thì tính phần dưới trục là âm, nên các mảnh có thể triệt tiêu nhau như ở bài mở đầu.

### ⏱ Ba trường hợp

**`c3`** — Ba trường hợp. Nếu f không âm trên đoạn, S bằng tích phân của f. Nếu f không dương, S bằng trừ tích phân của f. Nếu f đổi dấu, tách cận tại các nghiệm, như cách ta đã làm ở tập mười bốn.

### ⏱ Tìm cận khi đề không cho

**`c4`** — Khi đề chỉ nói hình phẳng giới hạn bởi đồ thị và trục hoành, không cho hai đường thẳng đứng, thì cận chính là các nghiệm của f bằng không. Ví dụ y bằng x bình phương trừ bốn x cộng ba cắt trục hoành tại một và ba, nên miền nằm trên đoạn từ một đến ba.

**`c5`** — Mẹo tính nhanh: trên mỗi khoảng giữa hai nghiệm liên tiếp, f không đổi dấu, nên có thể đưa trị tuyệt đối ra ngoài tích phân của khoảng đó. Diện tích là tổng các trị tuyệt đối. Cách viết này rất tiện để bấm máy tính.

**`c5b`** — Với câu trắc nghiệm hay trả lời ngắn, có thể bấm máy tính trực tiếp: nhập tích phân của Abs của f, máy tự xử lý trị tuyệt đối. Nhưng với hàm có nhiều nghiệm, máy có thể chạy lâu hoặc kém chính xác, nên cách an toàn vẫn là tách cận tại các nghiệm rồi cộng các trị tuyệt đối.

### ⏱ Bẫy quên trị tuyệt đối

**`c6`** — Hai bẫy hay gặp. Một, quên trị tuyệt đối, tính tích phân trên cả đoạn rồi ghi đáp số, có khi ra số âm. Diện tích không bao giờ âm. Hai, đưa trị tuyệt đối ra ngoài toàn bộ tích phân khi f đổi dấu, kết quả bị nhỏ hơn diện tích thật.

## Ví dụ

### ⏱ Ví dụ 1: bài mở đầu

**`e1`** — Ví dụ một, giải bài mở đầu. x bình phương trừ hai x bằng không tại x bằng không và x bằng hai. Trên đoạn từ không đến hai, f âm, tích phân bằng trừ bốn phần ba. Trên đoạn từ hai đến ba, f dương, tích phân bằng bốn phần ba. Diện tích bằng bốn phần ba cộng bốn phần ba, bằng tám phần ba.

### ⏱ Ví dụ 2: cận là nghiệm

**`e2`** — Ví dụ hai: diện tích giới hạn bởi y bằng x bình phương trừ bốn x cộng ba và trục hoành. Cận là hai nghiệm một và ba. Trên đoạn này, f âm, tích phân bằng trừ bốn phần ba. Diện tích bằng bốn phần ba.

### ⏱ Ví dụ 3: hàm bậc ba

**`e3`** — Ví dụ ba: y bằng x lập phương trừ x và trục hoành. Ba nghiệm trừ một, không và một. Đồ thị đối xứng qua gốc tọa độ, hai mảnh có diện tích bằng nhau, mỗi mảnh bằng một phần tư. Tổng diện tích bằng một phần hai, trong khi tích phân từ trừ một đến một bằng không.

### ⏱ Ví dụ 4: thiếu một cận

**`e4`** — Ví dụ bốn: y bằng l n x, trục hoành và đường thẳng x bằng e. Đề chỉ cho một đường thẳng đứng, cận còn lại là nghiệm của l n x bằng không, tức x bằng một. Diện tích bằng tích phân từ một đến e của l n x, bằng một, kết quả quen thuộc từ tập mười bảy.

### ⏱ Ví dụ 5: đọc công thức từ hình

**`e5`** — Ví dụ năm, dạng đọc hình: đề cho đồ thị f cắt trục hoành tại c nằm giữa a và b, phần từ a đến c ở trên trục, phần từ c đến b ở dưới trục. Công thức đúng là S bằng tích phân từ a đến c của f, trừ tích phân từ c đến b của f. Hãy nhìn dấu trên hình để quyết định dấu trước mỗi tích phân.

### ⏱ Ví dụ 6: biết diện tích, tính tích phân

**`e6`** — Ví dụ sáu, bài toán ngược rất hay gặp: đồ thị f cắt trục hoành tại c. Biết miền phía trên trục có diện tích ba, miền phía dưới có diện tích một. Tính tích phân từ a đến b của f. Phần trên mang dấu dương, phần dưới mang dấu âm, nên tích phân bằng ba trừ một, bằng hai, không phải bốn.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Gọi D là hình phẳng giới hạn bởi đồ thị y bằng x bình phương trừ x trừ hai, trục hoành, x bằng không và x bằng ba. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: f bằng x cộng một nhân x trừ hai, âm trên khoảng từ không đến hai. Ý b sai: f đổi dấu tại hai nên không thể dùng tích phân của f trên cả đoạn.

**`x3`** — Ý c đúng: tách tại hai và đổi dấu đoạn âm. Ý d sai: diện tích bằng mười phần ba cộng mười một phần sáu, bằng ba mươi mốt phần sáu, xấp xỉ năm phẩy mười bảy, lớn hơn năm.

### ⏱ Câu trả lời ngắn

**`x4`** — Câu trả lời ngắn: tính diện tích hình phẳng giới hạn bởi y bằng x bình phương trừ hai x trừ ba và trục hoành, làm tròn đến hàng phần mười. Cận là hai nghiệm trừ một và ba.

**`x5`** — Trên đoạn từ trừ một đến ba, f âm. Tích phân bằng trừ ba mươi hai phần ba, nên diện tích bằng ba mươi hai phần ba, xấp xỉ mười phẩy sáu bảy, làm tròn được mười phẩy bảy. Ghi vào phiếu: một, không, phẩy, bảy.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, diện tích bằng tích phân của trị tuyệt đối f, không bao giờ âm. Hai, đề không cho cận thì cận là nghiệm của f bằng không. Ba, tách cận tại các nghiệm, trên mỗi khoảng có thể đưa trị tuyệt đối ra ngoài.

**`o2`** — Bài tập tự luyện. Một, diện tích giới hạn bởi y bằng x bình phương trừ một và trục hoành. Hai, y bằng x lập phương, trục hoành, x bằng trừ một và x bằng hai. Ba, y bằng cốt x, trục hoành, x bằng không và x bằng pi. Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập hai mươi hai, ta tính diện tích giữa hai đường cong: tìm giao điểm, chia khoảng, và lấy đường trên trừ đường dưới. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. y = x² − 1 và trục Ox → **4/3**
2. y = x³, Ox, x = −1, x = 2 → **17/4**
3. y = cos x, Ox, x = 0, x = π → **2**
