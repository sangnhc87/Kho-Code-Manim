# INT14 – Tích phân chứa trị tuyệt đối: Và hàm từng khúc: xét dấu rồi tách cận

> Sinh tự động từ `int14/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int14`.

**Số nhịp:** 24 · **Số công thức Typst:** 46 · **Từ:** 1198

## Mở đầu

### ⏱ Mở đầu: bỏ trị tuyệt đối ra ngoài có được không?

**`h1`** — Tính tích phân từ không đến ba của trị tuyệt đối x bình phương trừ ba x cộng hai. Nhiều bạn bỏ dấu trị tuyệt đối ra ngoài, tính tích phân bên trong được ba phần hai, rồi lấy trị tuyệt đối. Kết quả đó sai! Đáp số đúng là mười một phần sáu. Vì sao lại lệch nhau?

**`h2`** — Đây là tập mười bốn của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: tích phân chứa trị tuyệt đối và hàm cho theo từng khúc.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, ý nghĩa hình học: trị tuyệt đối lật phần âm lên trên trục. Hai, quy trình ba bước: tìm nghiệm, xét dấu, tách cận. Ba, cách xử lý hàm từng khúc và hàm max, min.

## Bản chất

### ⏱ Ý nghĩa hình học: lật phần âm

**`c1`** — Nhìn đồ thị của f bằng x bình phương trừ ba x cộng hai trên đoạn từ không đến ba. Phần từ một đến hai nằm dưới trục hoành, mang dấu âm, nên khi tính tích phân nó bị trừ đi. Lấy trị tuyệt đối thì phần âm được lật lên trên trục, và mọi mảnh đều được cộng vào.

**`c2`** — Vì vậy tích phân của trị tuyệt đối f chính là tổng diện tích hình học giữa đồ thị và trục hoành. Nó luôn lớn hơn hoặc bằng trị tuyệt đối của tích phân. Dấu bằng chỉ xảy ra khi f không đổi dấu trên đoạn.

### ⏱ Quy trình ba bước

**`c3`** — Định nghĩa trị tuyệt đối cho ta công cụ: trị tuyệt đối của f bằng f khi f không âm, và bằng trừ f khi f âm. Muốn bỏ dấu trị tuyệt đối, ta phải biết dấu của f trên từng đoạn.

**`c4`** — Quy trình ba bước. Bước một: giải f bằng không, giữ lại các nghiệm nằm trong đoạn lấy tích phân. Bước hai: lập bảng xét dấu của f. Bước ba: tách cận tại các nghiệm, đoạn nào f âm thì đổi dấu, rồi tính từng tích phân.

**`c5`** — Áp dụng cho bài mở đầu. Phương trình x bình phương trừ ba x cộng hai bằng không có hai nghiệm một và hai, cả hai đều nằm trong đoạn từ không đến ba. Bảng xét dấu: dương, âm, dương.

**`c5b`** — Lưu ý: chỉ giữ những nghiệm nằm trong đoạn lấy tích phân. Nếu trên cả đoạn f không đổi dấu, ta được phép đưa trị tuyệt đối ra ngoài. Ví dụ, trên đoạn từ hai đến ba, x bình phương trừ ba x cộng hai không âm, nên tích phân của trị tuyệt đối bằng trị tuyệt đối của tích phân, bằng năm phần sáu. Còn trên đoạn từ không đến ba thì không được, vì f đổi dấu.

**`c6`** — Một ví dụ dễ hình dung: tích phân từ âm một đến hai của trị tuyệt đối x. Đồ thị là hai tam giác vuông cân. Tam giác bên trái có diện tích một phần hai, tam giác bên phải có diện tích hai. Tổng là năm phần hai.

### ⏱ Hàm từng khúc, max và min

**`c7`** — Hàm cho theo từng khúc cũng xử lý bằng cách tách cận, nhưng điểm cắt là điểm nối giữa các công thức. Trên mỗi đoạn con, ta dùng đúng công thức của khúc đó. Hàm max và min cũng là hàm từng khúc: so sánh hai hàm để biết hàm nào lớn hơn trên từng đoạn.

## Ví dụ

### ⏱ Ví dụ 1: hoàn thành bài mở đầu

**`e1`** — Ví dụ một, hoàn thành bài mở đầu. Tách thành ba tích phân: từ không đến một giữ nguyên, từ một đến hai đổi dấu, từ hai đến ba giữ nguyên. Ba giá trị lần lượt là năm phần sáu, một phần sáu và năm phần sáu. Tổng bằng mười một phần sáu.

### ⏱ Ví dụ 2: hàm lượng giác

**`e2`** — Ví dụ hai: tích phân từ không đến pi của trị tuyệt đối cốt x. Cốt x đổi dấu tại pi phần hai. Từ không đến pi phần hai, cốt x dương, tích phân bằng một. Từ pi phần hai đến pi, cốt x âm, đổi dấu cũng được một. Kết quả là hai, trong khi tích phân của cốt x không có trị tuyệt đối lại bằng không.

### ⏱ Ví dụ 3: hàm max

**`e3`** — Ví dụ ba: tích phân từ không đến hai của max của x và x bình phương. Trên đoạn từ không đến một, x lớn hơn x bình phương. Trên đoạn từ một đến hai, x bình phương lớn hơn. Vậy tích phân bằng một phần hai cộng bảy phần ba, bằng mười bảy phần sáu.

### ⏱ Ví dụ 4: hàm từng khúc có tham số

**`e4`** — Ví dụ bốn: hàm f bằng x bình phương cộng a khi x nhỏ hơn hoặc bằng một, bằng hai x cộng một khi x lớn hơn một. Tìm a để f liên tục, rồi tính tích phân từ không đến hai. Tại x bằng một, hai khúc phải gặp nhau: một cộng a bằng ba, nên a bằng hai.

**`e5`** — Khi a bằng hai, cắt tại điểm nối x bằng một. Tích phân từ không đến một của x bình phương cộng hai bằng bảy phần ba. Tích phân từ một đến hai của hai x cộng một bằng bốn. Tổng là mười chín phần ba.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Cho hàm số f bằng x bình phương trừ bốn trên đoạn từ không đến ba. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: với x từ không đến hai, x bình phương không vượt quá bốn. Ý b đúng: tích phân từ không đến ba của x bình phương trừ bốn bằng chín trừ mười hai, bằng âm ba.

**`x3`** — Ý c sai: đây chính là cái bẫy bỏ trị tuyệt đối ra ngoài. Ý d đúng: tách cận tại hai, đoạn đầu đổi dấu được mười sáu phần ba, đoạn sau được bảy phần ba, tổng là hai mươi ba phần ba.

### ⏱ Câu trả lời ngắn

**`x4`** — Câu trả lời ngắn: tính tích phân từ không đến hai của trị tuyệt đối e mũ x trừ hai, làm tròn đến hàng phần trăm. e mũ x bằng hai khi x bằng l n hai. Trước l n hai, biểu thức âm nên đổi dấu, sau đó giữ nguyên.

**`x5`** — Tính hai tích phân rồi cộng lại, ta được e bình phương trừ bảy cộng bốn l n hai, xấp xỉ ba phẩy một sáu. Ghi vào phiếu trả lời: ba, phẩy, một, sáu. Em có thể bấm máy tính với hàm Abs để kiểm tra kết quả.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, tích phân của trị tuyệt đối là tổng diện tích, phần âm được lật lên. Hai, quy trình: tìm nghiệm trong đoạn, xét dấu, tách cận và đổi dấu đoạn âm. Ba, hàm từng khúc và hàm max, min: cắt tại điểm nối hoặc giao điểm.

**`o2`** — Bài tập tự luyện. Một, tích phân từ không đến hai của trị tuyệt đối x trừ một. Hai, tích phân từ không đến hai pi của trị tuyệt đối sin x. Ba, tích phân từ không đến ba của trị tuyệt đối x bình phương trừ một. Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập mười lăm, ta dùng đúng ý tưởng này cho chuyển động: tích phân của vận tốc cho độ dời, còn tích phân của trị tuyệt đối vận tốc mới là quãng đường. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. ∫₀² |x − 1| dx → **1**
2. ∫₀^2π |sin x| dx → **4**
3. ∫₀³ |x² − 1| dx → **22/3**
