# INT24 – Đọc diện tích từ đồ thị f': So sánh f(a), f(b), f(c) không cần công thức

> Sinh tự động từ `int24/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int24`.

**Số nhịp:** 24 · **Số công thức Typst:** 36 · **Từ:** 1278

## Mở đầu

### ⏱ Mở đầu: chỉ có đồ thị f'

**`h1`** — Đề chỉ cho đồ thị của đạo hàm f phẩy: từ không đến hai nằm trên trục với diện tích bốn, từ hai đến năm nằm dưới trục với diện tích bảy. Hãy sắp xếp f của không, f của hai và f của năm. Không có công thức nào của f, nhưng ta vẫn trả lời được chắc chắn.

**`h2`** — Đây là tập hai mươi bốn của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: đọc diện tích từ đồ thị của đạo hàm.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, diện tích dưới đồ thị f phẩy chính là độ biến thiên của f. Hai, cách so sánh các giá trị của f và tìm giá trị lớn nhất, nhỏ nhất. Ba, tính diện tích bằng hình học khi đồ thị f phẩy là đường thẳng hay đường tròn.

## Bản chất

### ⏱ Diện tích = độ biến thiên của f

**`c1`** — Chìa khóa là công thức Newton Leibniz đọc theo chiều ngược: f của b trừ f của a bằng tích phân từ a đến b của f phẩy. Nói bằng hình: diện tích có dấu dưới đồ thị f phẩy cho biết f đã tăng hay giảm bao nhiêu.

**`c2`** — Trên đoạn mà f phẩy dương, đồ thị f phẩy nằm trên trục, f tăng đúng bằng diện tích phần đó. Trên đoạn mà f phẩy âm, f giảm đúng bằng diện tích phần nằm dưới trục. Ta có thể vẽ song song: mỗi mảnh diện tích là một bước đi lên hoặc đi xuống của f.

### ⏱ Quy trình so sánh

**`c3`** — Quy trình so sánh. Một, đọc dấu của f phẩy để lập bảng biến thiên của f. Hai, đọc diện tích các mảnh. Ba, viết mỗi giá trị cần so sánh theo một giá trị gốc, ví dụ f của hai bằng f của không cộng bốn, rồi so sánh các số cộng thêm.

**`c4`** — Giá trị lớn nhất và nhỏ nhất. Cực đại xảy ra khi f phẩy đổi dấu từ dương sang âm, cực tiểu khi đổi từ âm sang dương. Nhưng giá trị lớn nhất trên đoạn còn phải so với hai đầu mút, và việc so sánh đó lại dựa vào diện tích.

### ⏱ Tính diện tích bằng hình học

**`c5`** — Khi đồ thị f phẩy là đoạn thẳng, parabol hay cung tròn, diện tích tính được bằng hình học: tam giác, hình thang, một phần tư hình tròn. Đề thi thường vẽ trên lưới ô vuông để ta đếm được diện tích.

### ⏱ Bẫy: nhầm f với f′

**`c6`** — Bẫy lớn nhất: nhầm đồ thị f phẩy với đồ thị f. Đồ thị f phẩy nằm trên trục nghĩa là f đang tăng, không phải f dương. Và điểm cao nhất của đồ thị f phẩy là nơi f tăng nhanh nhất, không phải cực đại của f.

## Ví dụ

### ⏱ Ví dụ 1: bài mở đầu

**`e1`** — Ví dụ một, giải bài mở đầu. f của hai bằng f của không cộng bốn. f của năm bằng f của hai trừ bảy, tức f của không trừ ba. So sánh ba số cộng thêm: không, cộng bốn, trừ ba. Vậy f của năm nhỏ hơn f của không, nhỏ hơn f của hai. Giá trị lớn nhất trên đoạn là f của hai.

### ⏱ Ví dụ 2: đồ thị là đường thẳng

**`e2`** — Ví dụ hai: f phẩy bằng x trừ một trên đoạn từ không đến ba, đồ thị là một đường thẳng. Từ không đến một là tam giác dưới trục, diện tích một phần hai. Từ một đến ba là tam giác trên trục, diện tích hai. Vậy f nhỏ nhất tại một, và f của ba lớn hơn f của không là ba phần hai.

### ⏱ Ví dụ 3: cung tròn

**`e3`** — Ví dụ ba: f của không bằng hai, đồ thị f phẩy trên đoạn từ không đến hai là một phần tư đường tròn bán kính hai. Diện tích bằng một phần tư nhân pi nhân bốn, bằng pi. Vậy f của hai bằng hai cộng pi, tính được mà không cần biết công thức của f phẩy.

### ⏱ Ví dụ 4: các mảnh bằng nhau

**`e4`** — Ví dụ bốn: f phẩy bằng x bình phương trừ hai x trên đoạn từ trừ một đến ba. Ba mảnh diện tích đều bằng bốn phần ba: trên, dưới, rồi trên. Vì vậy f của hai bằng f của trừ một, và f của ba bằng f của không. Giá trị lớn nhất đạt tại cả không và ba, giá trị nhỏ nhất đạt tại cả trừ một và hai.

**`e5`** — Mẹo trình bày: vẽ một trục số dọc cho các giá trị của f, đặt f của điểm đầu tại số không, rồi đi lên hoặc đi xuống theo từng mảnh diện tích. Thứ tự trên trục dọc chính là đáp án so sánh.

### ⏱ Ví dụ 5: đếm nghiệm

**`e6`** — Ví dụ năm, đếm nghiệm: với đồ thị f phẩy ở bài mở đầu và f của không bằng một. Trên đoạn từ không đến hai, f tăng từ một lên năm, nên không có nghiệm. Từ hai đến năm, f giảm từ năm xuống trừ hai, đi qua giá trị không đúng một lần. Vậy phương trình f bằng không có đúng một nghiệm trên đoạn từ không đến năm.

### ⏱ Ví dụ 6: hàm g = f − x

**`e7`** — Ví dụ sáu, vận dụng cao: xét g bằng f trừ x, thì g phẩy bằng f phẩy trừ một. Diện tích cần đọc bây giờ nằm giữa đồ thị f phẩy và đường thẳng y bằng một. Chẳng hạn f phẩy bằng x bình phương trên đoạn từ không đến hai: g của hai trừ g của không bằng tám phần ba trừ hai, bằng hai phần ba, nên g của hai lớn hơn.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Đồ thị f phẩy trên đoạn từ không đến sáu gồm ba mảnh: từ không đến một nằm trên trục, diện tích ba; từ một đến bốn nằm dưới trục, diện tích năm; từ bốn đến sáu nằm trên trục, diện tích bốn. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: f phẩy dương trên khoảng từ không đến một. Ý b đúng: f của bốn bằng f của một trừ năm, nhỏ hơn f của một.

**`x3`** — Ý c sai: f của sáu bằng f của không cộng ba trừ năm cộng bốn, bằng f của không cộng hai, lớn hơn f của không. Ý d sai: f của một bằng f của không cộng ba, lớn hơn f của sáu, nên giá trị lớn nhất là f của một.

### ⏱ Câu trả lời ngắn

**`x4`** — Câu trả lời ngắn: biết f của một bằng năm, đồ thị f phẩy là đường thẳng đi qua hai điểm một, không và ba, bốn. Tính f của bốn. Đường thẳng có phương trình f phẩy bằng hai nhân x trừ một.

**`x5`** — Từ một đến bốn, đồ thị f phẩy là tam giác trên trục với đáy ba và chiều cao sáu, diện tích chín. Vậy f của bốn bằng năm cộng chín, bằng mười bốn. Ghi vào phiếu: một, bốn.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, f của b trừ f của a bằng diện tích có dấu dưới đồ thị f phẩy. Hai, so sánh bằng cách quy mọi giá trị về một giá trị gốc rồi cộng trừ diện tích. Ba, đừng nhầm đồ thị f phẩy với đồ thị f.

**`o2`** — Bài tập tự luyện. Một, f phẩy bằng x trừ hai trên đoạn từ không đến bốn, so sánh f của không và f của bốn. Hai, f của không bằng một và f phẩy bằng hai x, tính f của ba. Ba, f phẩy bằng cốt x, tìm điểm mà f lớn nhất trên đoạn từ không đến hai pi. Đáp số hiện ở cuối màn hình.

**`o3`** — Tập hai mươi lăm bước sang không gian ba chiều: tính thể tích vật thể bằng cách cắt lát và cộng dồn diện tích thiết diện. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. f'(x) = x − 2 trên [0; 4]: so sánh f(0), f(4) → **f(0) = f(4)**
2. f(0) = 1, f'(x) = 2x: f(3) → **10**
3. f'(x) = cos x trên [0; 2π]: f lớn nhất tại → **x = π/2**
