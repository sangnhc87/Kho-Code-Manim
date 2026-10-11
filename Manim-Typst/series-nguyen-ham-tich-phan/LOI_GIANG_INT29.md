# INT29 – Bài toán chuyển động thực tế: Phanh xe, đuổi kịp, hai xe gặp nhau

> Sinh tự động từ `int29/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int29`.

**Số nhịp:** 24 · **Số công thức Typst:** 36 · **Từ:** 1245

## Mở đầu

### ⏱ Mở đầu: hai đồ thị cắt nhau có phải là gặp nhau?

**`h1`** — Xe A chạy đều hai mươi mét trên giây. Cùng lúc, xe B xuất phát từ trạng thái nghỉ tại cùng vị trí, tăng tốc với vận tốc v bằng hai t. Khi nào B đuổi kịp A? Nhiều bạn trả lời: lúc mười giây, khi hai đồ thị vận tốc cắt nhau. Sai! Lúc đó khoảng cách hai xe lại xa nhất. Đáp số đúng là hai mươi giây.

**`h2`** — Đây là tập hai mươi chín, mở đầu phần D về ứng dụng thực tế: bài toán chuyển động, từ phanh xe đến hai xe gặp nhau.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, vị trí bằng vị trí ban đầu cộng tích phân của vận tốc. Hai, gặp nhau khi hai vị trí bằng nhau, tức là hai diện tích bằng nhau. Ba, bài toán phanh xe và khoảng cách an toàn.

## Bản chất

### ⏱ Vị trí từ vận tốc

**`c1`** — Nhắc lại từ tập mười lăm: vị trí tại thời điểm t bằng vị trí ban đầu cộng tích phân từ không đến t của vận tốc. Với nhiều xe, ta viết riêng vị trí của từng xe trên cùng một trục tọa độ, chọn gốc và chiều dương rõ ràng.

### ⏱ Gặp nhau: hai diện tích bằng nhau

**`c2`** — Hai xe gặp nhau khi vị trí của chúng bằng nhau. Nếu hai xe xuất phát cùng lúc, cùng chỗ, cùng chiều, điều kiện này có nghĩa là diện tích dưới hai đồ thị vận tốc, từ không đến t, bằng nhau.

### ⏱ Giao điểm đồ thị vận tốc

**`c3`** — Vậy giao điểm của hai đồ thị vận tốc nói gì? Đó là lúc hai xe có cùng vận tốc. Trước thời điểm đó, một xe nhanh hơn nên khoảng cách tăng dần; sau đó, xe kia nhanh hơn nên khoảng cách giảm. Vì thế giao điểm là lúc khoảng cách lớn nhất, không phải lúc gặp nhau.

### ⏱ Bài toán phanh xe

**`c4`** — Bài toán phanh: xe đang chạy với vận tốc v không, phanh với gia tốc không đổi độ lớn a. Vận tốc v bằng v không trừ a t, xe dừng khi t bằng v không chia a. Quãng đường phanh bằng tích phân, cho kết quả v không bình phương chia hai a.

### ⏱ Đơn vị và thời gian phản xạ

**`c5`** — Hai chú ý về đơn vị. Vận tốc thường cho bằng ki lô mét trên giờ, phải đổi sang mét trên giây bằng cách chia ba phẩy sáu. Và thời gian phản xạ: trước khi phanh, xe vẫn chạy đều trong khoảng thời gian người lái phản ứng.

### ⏱ Quy trình bốn bước

**`c6`** — Quy trình bốn bước cho mọi bài hai xe. Một, chọn gốc tọa độ, chiều dương và mốc thời gian. Hai, viết vận tốc của từng xe, chú ý xe nào xuất phát muộn hơn. Ba, viết vị trí của từng xe bằng tích phân. Bốn, giải phương trình hai vị trí bằng nhau, và loại nghiệm không phù hợp.

## Ví dụ

### ⏱ Ví dụ 1: đuổi kịp

**`e1`** — Ví dụ một, giải bài mở đầu. Vị trí xe A là hai mươi t, vị trí xe B là tích phân của hai t, bằng t bình phương. Gặp nhau khi t bình phương bằng hai mươi t, tức t bằng hai mươi giây, lúc đó cả hai đi được bốn trăm mét.

**`e2`** — Khoảng cách hai xe là hai mươi t trừ t bình phương, lớn nhất tại t bằng mười, đúng lúc hai vận tốc bằng nhau. Khi đó khoảng cách bằng hai trăm trừ một trăm, bằng một trăm mét. Trên hình, đó là phần diện tích nằm giữa hai đồ thị vận tốc từ không đến mười.

### ⏱ Ví dụ 2: phanh xe

**`e3`** — Ví dụ hai: ô tô chạy bảy mươi hai ki lô mét trên giờ, tức hai mươi mét trên giây, phanh với gia tốc năm mét trên giây bình phương. Xe dừng sau bốn giây. Quãng đường phanh bằng tích phân từ không đến bốn của hai mươi trừ năm t, bằng bốn mươi mét.

### ⏱ Ví dụ 3: khoảng cách an toàn

**`e4`** — Ví dụ ba, khoảng cách an toàn: phía trước năm mươi mét có vật cản. Người lái mất một giây để phản xạ, xe đi thêm hai mươi mét, rồi phanh như ví dụ hai thêm bốn mươi mét. Tổng sáu mươi mét, lớn hơn năm mươi: va chạm!

**`e5`** — Muốn an toàn, quãng đường phanh tối đa còn ba mươi mét. Hai mươi bình phương chia hai a nhỏ hơn hoặc bằng ba mươi, suy ra a lớn hơn hoặc bằng hai mươi phần ba, khoảng sáu phẩy sáu bảy mét trên giây bình phương.

### ⏱ Ví dụ 4: ngược chiều

**`e6`** — Ví dụ bốn, hai xe ngược chiều: cách nhau ba trăm mét, xe A chạy đều mười mét trên giây, xe B từ nghỉ với vận tốc hai t, chạy về phía A. Gặp nhau khi tổng quãng đường bằng ba trăm: mười t cộng t bình phương bằng ba trăm. Giải ra t bằng trừ năm cộng năm căn mười ba, khoảng mười ba giây.

### ⏱ Ví dụ 5: xuất phát lệch giờ

**`e7`** — Ví dụ năm, xuất phát lệch giờ: xe A chạy đều mười mét trên giây. Hai giây sau, xe B xuất phát từ cùng chỗ với vận tốc bốn nhân t trừ hai. Vị trí xe B là tích phân từ hai đến t, bằng hai nhân t trừ hai, bình phương. Giải mười t bằng hai nhân t trừ hai bình phương, lấy nghiệm lớn hơn hai: khoảng tám phẩy năm ba giây.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Xe A chạy đều mười lăm mét trên giây. Xe B xuất phát cùng lúc, cùng chỗ, từ trạng thái nghỉ, với vận tốc ba t. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: ba t bằng mười lăm khi t bằng năm. Ý b sai: tại t bằng năm, A đi bảy mươi lăm mét còn B chỉ đi ba mươi bảy phẩy năm mét.

**`x3`** — Ý c đúng: khoảng cách lớn nhất tại t bằng năm, bằng bảy mươi lăm trừ ba mươi bảy phẩy năm, bằng ba mươi bảy phẩy năm mét. Ý d đúng: mười lăm t bằng một phẩy năm t bình phương cho t bằng mười.

### ⏱ Câu trả lời ngắn

**`x4`** — Câu trả lời ngắn: ô tô chạy năm mươi tư ki lô mét trên giờ thì người lái thấy vật cản. Sau không phẩy năm giây phản xạ, xe phanh với vận tốc v bằng mười lăm trừ năm t. Tính tổng quãng đường từ lúc thấy vật cản đến khi dừng.

**`x5`** — Năm mươi tư ki lô mét trên giờ bằng mười lăm mét trên giây. Trong không phẩy năm giây phản xạ, xe đi bảy phẩy năm mét. Khi phanh, xe dừng sau ba giây và đi thêm hai mươi hai phẩy năm mét. Tổng cộng ba mươi mét. Ghi vào phiếu: ba, không.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, vị trí bằng vị trí đầu cộng tích phân của vận tốc. Hai, gặp nhau khi hai vị trí bằng nhau; giao điểm đồ thị vận tốc là lúc khoảng cách lớn nhất. Ba, phanh xe: quãng đường v không bình phương chia hai a, cộng thêm quãng đường phản xạ.

**`o2`** — Bài tập tự luyện. Một, xe A đều mười mét trên giây, xe B từ nghỉ với v bằng hai t, cùng chỗ: khi nào B đuổi kịp? Hai, xe ba mươi sáu ki lô mét trên giờ phanh với gia tốc hai: quãng đường phanh? Ba, v A bằng hai mươi, v B bằng bốn t: khoảng cách lớn nhất? Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập ba mươi, ta dùng tích phân để thiết kế: cổng hình parabol, logo, mảnh vườn, và tính chi phí theo diện tích. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. A đều 10 m/s, B từ nghỉ v = 2t, cùng chỗ: B đuổi kịp lúc → **t = 10 s**
2. Xe 36 km/h phanh với gia tốc 2 m/s²: quãng đường phanh → **25 m**
3. v_A = 20, v_B = 4t: khoảng cách lớn nhất → **50 m**
