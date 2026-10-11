# INT16 – Tích phân đổi biến số: Đổi biến phải đổi cận

> Sinh tự động từ `int16/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int16`.

**Số nhịp:** 24 · **Số công thức Typst:** 50 · **Từ:** 1274

## Mở đầu

### ⏱ Mở đầu: đổi biến nhưng quên đổi cận

**`h1`** — Tính tích phân từ không đến một của hai x nhân x bình phương cộng một, tất cả mũ ba. Một bạn đặt u bằng x bình phương cộng một, viết lại thành tích phân từ không đến một của u mũ ba, và được một phần tư. Sai rồi! Đáp số đúng là mười lăm phần tư, gấp mười lăm lần. Lỗi nằm ở đâu?

**`h2`** — Đây là tập mười sáu của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: tích phân đổi biến số.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, công thức đổi biến và vì sao phải đổi cận. Hai, quy trình bốn bước với bảng đổi cận. Ba, đổi biến lượng giác cho căn của một trừ x bình phương.

## Bản chất

### ⏱ Công thức đổi biến

**`c1`** — Công thức đổi biến: tích phân từ a đến b của f của u của x, nhân u phẩy x, d x, bằng tích phân từ u của a đến u của b của f của u, d u. Nó đến từ quy tắc đạo hàm hàm hợp mà ta đã gặp ở phần nguyên hàm.

**`c2`** — Vì sao cận thay đổi? Biến x chạy từ không đến một. Khi đó u bằng x bình phương cộng một chạy từ một đến hai. Tích phân mới tính theo u, nên cận phải là giá trị của u, không phải giá trị của x.

### ⏱ Miền tích phân co giãn theo u

**`c3`** — Nhìn bằng hình: diện tích dưới đồ thị hai x nhân x bình phương cộng một mũ ba trên đoạn từ không đến một, bằng đúng diện tích dưới đồ thị u mũ ba trên đoạn từ một đến hai. Miền lấy tích phân bị co giãn và dịch chuyển, nhưng diện tích được giữ nguyên, đều bằng mười lăm phần tư.

### ⏱ Quy trình bốn bước

**`c4`** — Quy trình bốn bước. Một, chọn u, thường là biểu thức bên trong hàm hợp. Hai, tính d u theo d x. Ba, lập bảng đổi cận: x bằng a thì u bằng bao nhiêu, x bằng b thì u bằng bao nhiêu. Bốn, tính tích phân mới theo u, và không cần thay lại x.

**`c5`** — Áp dụng cho bài mở đầu. Đặt u bằng x bình phương cộng một, d u bằng hai x d x. x bằng không thì u bằng một, x bằng một thì u bằng hai. Tích phân trở thành tích phân từ một đến hai của u mũ ba, bằng u mũ bốn phần bốn lấy cận, bằng mười sáu trừ một, chia bốn, bằng mười lăm phần tư.

**`c6`** — Cách khác: tìm nguyên hàm theo x, là x bình phương cộng một, mũ bốn, chia bốn, rồi thay cận không và một. Kết quả vẫn là mười lăm phần tư. Hai cách đều đúng. Lỗi chỉ xảy ra khi trộn hai cách: đã chuyển sang u mà vẫn giữ cận của x.

### ⏱ Dấu hiệu chọn u

**`c7`** — Dấu hiệu chọn u: trong tích phân có một hàm hợp, và đạo hàm của phần bên trong xuất hiện làm thừa số. Gặp cốt x đi cùng hàm của sin x, đặt u bằng sin x. Gặp một chia x đi cùng hàm của l n x, đặt u bằng l n x. Gặp x đi cùng hàm của x bình phương, đặt u bằng x bình phương. Thiếu hệ số thì bù bằng một hằng số.

## Ví dụ

### ⏱ Ví dụ 1: đặt u = sin x

**`e1`** — Ví dụ một: tích phân từ không đến pi phần hai của sin bình phương x nhân cốt x. Đặt u bằng sin x, d u bằng cốt x d x. x bằng không thì u bằng không, x bằng pi phần hai thì u bằng một. Tích phân bằng tích phân từ không đến một của u bình phương, bằng một phần ba.

### ⏱ Ví dụ 2: đặt u = ln x

**`e2`** — Ví dụ hai: tích phân từ một đến e của l n x chia x. Đặt u bằng l n x, d u bằng d x chia x. Cận mới: x bằng một thì u bằng không, x bằng e thì u bằng một. Kết quả là tích phân từ không đến một của u, bằng một phần hai.

### ⏱ Ví dụ 3: hệ số một nửa

**`e3`** — Ví dụ ba: tích phân từ không đến một của x nhân e mũ x bình phương. Đặt u bằng x bình phương, d u bằng hai x d x, nên x d x bằng một nửa d u. Cận mới từ không đến một. Kết quả: một phần hai nhân e trừ một.

### ⏱ Cận mới bị đảo chiều

**`e3b`** — Chú ý: cận mới có thể bị đảo chiều. Với tích phân từ không đến một của x nhân một trừ x bình phương, mũ ba, đặt u bằng một trừ x bình phương thì x bằng không cho u bằng một, x bằng một cho u bằng không. Cứ giữ đúng thứ tự: tích phân từ một đến không của trừ một nửa u mũ ba, bằng một phần tám. Đừng tự ý đổi chỗ cận.

### ⏱ Ví dụ 4: đổi biến lượng giác

**`e4`** — Ví dụ bốn, đổi biến lượng giác: tích phân từ không đến một của căn một trừ x bình phương. Đặt x bằng sin t, d x bằng cốt t d t, cận mới từ không đến pi phần hai. Căn một trừ sin bình phương là cốt t, nên tích phân bằng tích phân của cốt bình phương t, bằng pi phần tư.

**`e5`** — Kết quả pi phần tư có ý nghĩa hình học rất đẹp: đồ thị y bằng căn một trừ x bình phương là nửa trên đường tròn bán kính một. Từ không đến một, miền dưới đồ thị là một phần tư hình tròn, diện tích đúng bằng pi phần tư.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Cho I bằng tích phân từ không đến hai của hai x chia x bình phương cộng một. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: đặt u bằng x bình phương cộng một thì d u bằng hai x d x. Ý b sai: đây chính là bẫy giữ nguyên cận cũ. Cận đúng là từ một đến năm.

**`x3`** — Ý c đúng: tích phân từ một đến năm của một chia u bằng l n năm. Ý d đúng: l n năm xấp xỉ một phẩy sáu một, nhỏ hơn hai.

### ⏱ Câu trả lời ngắn

**`x4`** — Câu trả lời ngắn: tính tích phân từ không đến căn ba của x nhân căn x bình phương cộng một, làm tròn đến hàng phần trăm. Đặt u bằng x bình phương cộng một, cận mới từ một đến bốn, và x d x bằng một nửa d u.

**`x5`** — Tích phân bằng một nửa nhân tích phân từ một đến bốn của căn u, bằng một phần ba nhân u mũ ba phần hai lấy cận, bằng một phần ba nhân tám trừ một, bằng bảy phần ba, xấp xỉ hai phẩy ba ba. Ghi vào phiếu: hai, phẩy, ba, ba.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, công thức đổi biến: đổi cả hàm, cả vi phân và cả cận. Hai, quy trình bốn bước với bảng đổi cận, không cần quay về x. Ba, gặp căn một trừ x bình phương, hãy nghĩ đến đặt x bằng sin t.

**`o2`** — Bài tập tự luyện. Một, tích phân từ không đến một của ba x bình phương nhân x lập phương cộng một, bình phương. Hai, tích phân từ không đến pi phần hai của cốt x nhân e mũ sin x. Ba, tích phân từ không đến l n hai của e mũ x chia e mũ x cộng một. Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập mười bảy, ta học tích phân từng phần, công cụ cho tích của hai loại hàm khác nhau như x nhân e mũ x. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. ∫₀¹ 3x²(x³ + 1)² dx → **7/3**
2. ∫₀^(π/2) cos x · e^(sin x) dx → **e − 1**
3. ∫₀^(ln 2) eˣ/(eˣ + 1) dx → **ln(3/2)**
