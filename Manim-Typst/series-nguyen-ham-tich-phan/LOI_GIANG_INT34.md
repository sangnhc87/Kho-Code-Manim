# INT34 – Bẫy sai kinh điển & cách kiểm tra: Phòng khám lỗi sai: tám lỗi hay gặp, kiểm tra bằng đạo hàm và máy tính

> Sinh tự động từ `int34/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int34`.

**Số nhịp:** 26 · **Số công thức Typst:** 67 · **Từ:** 1344

## Mở đầu

### ⏱ Mở đầu: lời giải gọn nhưng sai

**`h1`** — Một bạn học sinh tính tích phân từ không đến một của hai x nhân x bình phương cộng một, tất cả mũ ba. Bạn đặt u bằng x bình phương cộng một, rồi ra đáp số một phần tư. Lời giải trông rất gọn. Nhưng bấm máy tính, kết quả lại là ba phẩy bảy lăm. Lỗi nằm ở đâu? Hôm nay ta mở phòng khám lỗi sai.

**`h2`** — Đây là tập ba mươi tư, mở đầu phần tổng ôn: những bẫy sai kinh điển và cách kiểm tra bằng máy tính.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, ba lớp kiểm tra: đạo hàm, máy tính và ước lượng. Hai, tám lỗi sai hay gặp nhất trong chương nguyên hàm, tích phân. Ba, cách nhận ra bẫy trong câu đúng sai và câu trả lời ngắn.

## Công cụ kiểm tra

### ⏱ Lớp 1: kiểm tra bằng đạo hàm

**`c1`** — Lớp kiểm tra thứ nhất: đạo hàm. F là một nguyên hàm của f khi và chỉ khi F phẩy bằng f. Vì vậy, mọi kết quả nguyên hàm đều kiểm tra được bằng cách lấy đạo hàm ngược lại. Ví dụ: đạo hàm của x ln x trừ x bằng ln x cộng một trừ một, đúng bằng ln x.

### ⏱ Lớp 2: kiểm tra bằng máy tính

**`c2`** — Lớp thứ hai: máy tính cầm tay có phím tích phân. Nhập tích phân từ một đến e của ln x, máy cho kết quả bằng một. Với tích phân xác định, hãy đổi đáp án phân số sang số thập phân rồi so với máy: mười lăm phần tư bằng ba phẩy bảy lăm, khớp; một phần tư bằng không phẩy hai lăm, không khớp.

### ⏱ Lớp 3: ước lượng bằng hình

**`c3`** — Lớp thứ ba: ước lượng. Nếu m nhỏ hơn hoặc bằng f, f nhỏ hơn hoặc bằng M trên đoạn a b, thì tích phân nằm giữa m nhân b trừ a và M nhân b trừ a. Ví dụ, e mũ x bình phương nằm giữa một và e trên đoạn không một, nên tích phân nằm giữa một và e. Máy cho khoảng một phẩy bốn sáu, hợp lý.

**`c4`** — Tóm lại ba lớp kiểm tra. Nguyên hàm: lấy đạo hàm. Tích phân xác định: so với máy tính. Và luôn hỏi: dấu và độ lớn của kết quả có hợp lý với hình vẽ không? Bây giờ ta dùng ba lớp này để khám từng lỗi sai.

## Phòng khám lỗi sai

### ⏱ Lỗi 1: quên trị tuyệt đối

**`e1`** — Lỗi một: quên trị tuyệt đối trong logarit. Nguyên hàm của một phần x là ln trị tuyệt đối x cộng C, không phải ln x. Kiểm tra: tích phân từ trừ hai đến trừ một của một phần x bằng trừ ln hai, khoảng trừ không phẩy sáu chín. Nếu viết ln x, ta không thể thay số âm vào.

### ⏱ Lỗi 2: nguyên hàm của tích

**`e2`** — Lỗi hai: coi nguyên hàm của tích là tích các nguyên hàm. Nguyên hàm của x e mũ x không phải x bình phương trên hai nhân e mũ x. Lấy đạo hàm thử là thấy ngay thừa một số hạng. Đúng phải dùng từng phần: x trừ một, nhân e mũ x, cộng C.

### ⏱ Lỗi 3: quên chia hệ số

**`e3`** — Lỗi ba: quên chia cho hệ số a khi nguyên hàm f của a x cộng b. Nguyên hàm của hai x cộng một, mũ năm, bằng hai x cộng một mũ sáu, chia mười hai, chứ không phải chia sáu. Đạo hàm lại: sáu nhân hai, chia mười hai, đúng bằng một.

### ⏱ Lỗi 4: sai dấu lượng giác

**`e4`** — Lỗi bốn: sai dấu với hàm lượng giác. Đạo hàm của cos là trừ sin, nên nguyên hàm của sin hai x là trừ một phần hai cos hai x cộng C. Quên dấu trừ là lỗi rất phổ biến, và đạo hàm lại sẽ phát hiện ngay.

### ⏱ Lỗi 5: đổi biến quên đổi cận

**`e5`** — Lỗi năm, chính là bài mở đầu: đổi biến nhưng quên đổi cận. Khi x đi từ không đến một, u bằng x bình phương cộng một đi từ một đến hai. Tích phân từ một đến hai của u mũ ba bằng mười lăm phần tư, đúng bằng ba phẩy bảy lăm như máy tính.

### ⏱ Lỗi 6: diện tích quên trị tuyệt đối

**`e6`** — Lỗi sáu: tính diện tích nhưng quên trị tuyệt đối. Với y bằng x bình phương trừ một trên đoạn không hai, tích phân bằng hai phần ba, vì phần âm đã triệt tiêu một phần diện tích. Phải tách tại nghiệm x bằng một: hai phần ba cộng bốn phần ba, diện tích bằng hai.

### ⏱ Lỗi 7: bình phương của hiệu

**`e7`** — Lỗi bảy: thể tích vành khăn. Quay miền giữa y bằng hai và y bằng x trên đoạn không một quanh trục hoành. Sai khi viết pi nhân tích phân của hiệu, bình phương. Đúng là pi nhân tích phân của hiệu các bình phương: bốn trừ x bình phương, được mười một pi phần ba.

### ⏱ Lỗi 8: độ dời và quãng đường

**`e8`** — Lỗi tám: nhầm độ dời với quãng đường. Vận tốc v bằng t trừ hai trên đoạn không bốn: tích phân của v bằng không, đó là độ dời, vật quay về chỗ cũ. Nhưng quãng đường là tích phân của trị tuyệt đối v, bằng hai cộng hai, bằng bốn mét.

### ⏱ Danh sách kiểm tra

**`e9`** — Trước khi nộp bài, hãy rà nhanh danh sách tám điểm: trị tuyệt đối trong ln, nguyên hàm của tích, chia hệ số, dấu lượng giác, đổi cận, trị tuyệt đối trong diện tích, bình phương trong thể tích, và quãng đường. Mỗi điểm chỉ mất vài giây, nhưng giữ lại rất nhiều điểm số.

## Đề thi mới

### ⏱ Câu trắc nghiệm

**`x1`** — Câu trắc nghiệm: tích phân từ không đến pi của sin x bằng bao nhiêu? Bốn phương án: không, trừ hai, hai và một. Hai phương án sai được dựng từ đúng các lỗi ta vừa học. Em hãy tạm dừng và chọn.

**`x2`** — Đáp án C. Nguyên hàm của sin x là trừ cos x, nên kết quả bằng trừ cos pi cộng cos không, bằng hai. Ai quên dấu trừ sẽ ra trừ hai; ai nghĩ diện tích hai phía triệt tiêu sẽ chọn không. Máy tính cũng cho đúng bằng hai.

### ⏱ Câu hỏi Đúng/Sai

**`x3`** — Câu hỏi đúng sai: mỗi mệnh đề có thể chứa một bẫy. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x4`** — Ý a sai: thiếu hệ số một phần hai, đạo hàm của ln trị tuyệt đối hai x cộng một là hai chia hai x cộng một. Ý b đúng: tích phân từ không đến pi phần hai của cos x bằng sin pi phần hai trừ sin không, bằng một.

**`x5`** — Ý c sai: đường thẳng y bằng x trừ một đổi dấu tại x bằng một, tích phân bằng không nhưng diện tích bằng một. Ý d đúng: vành khăn bán kính ngoài hai, bán kính trong một, thể tích bằng pi nhân bốn trừ một nhân ba, bằng chín pi.

### ⏱ Câu trả lời ngắn

**`x6`** — Câu trả lời ngắn: một vật chuyển động với vận tốc v bằng t bình phương trừ bốn t cộng ba mét trên giây. Tính quãng đường vật đi được trong ba giây đầu, làm tròn đến hàng phần trăm. Cẩn thận: vận tốc đổi dấu.

**`x7`** — Vận tốc bằng không tại t bằng một và t bằng ba. Tích phân từ không đến một bằng bốn phần ba, tích phân từ một đến ba bằng trừ bốn phần ba. Độ dời bằng không, nhưng quãng đường bằng tám phần ba, khoảng hai phẩy sáu bảy mét. Ghi vào phiếu: hai, phẩy, sáu, bảy.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, nguyên hàm luôn kiểm tra được bằng đạo hàm. Hai, tích phân xác định kiểm tra bằng máy tính, đổi đáp án sang số thập phân để so. Ba, tám lỗi kinh điển xoay quanh dấu, hệ số, cận và trị tuyệt đối.

**`o2`** — Bài tập tự luyện. Một, tích phân từ không đến một của ba x cộng một, bình phương. Hai, diện tích giữa y bằng x bình phương trừ x và trục hoành trên đoạn không hai. Ba, quãng đường với v bằng hai t trừ bốn trên đoạn không ba. Đáp số hiện ở cuối màn hình.

**`o3`** — Tập sau, ta luyện một đề theo đúng cấu trúc thi tốt nghiệp: trắc nghiệm, đúng sai và trả lời ngắn, có đồng hồ đếm giờ và lời giải nhanh. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. ∫₀¹ (3x + 1)² dx → **7**
2. Diện tích giữa y = x² − x và Ox trên [0; 2] → **1**
3. Quãng đường với v = 2t − 4 trên [0; 3] → **5 m**
