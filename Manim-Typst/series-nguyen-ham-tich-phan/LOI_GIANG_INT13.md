# INT13 – Tính chất của tích phân: Tuyến tính, cộng khoảng, so sánh

> Sinh tự động từ `int13/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int13`.

**Số nhịp:** 23 · **Số công thức Typst:** 39 · **Từ:** 1211

## Mở đầu

### ⏱ Mở đầu: tính tích phân khi không biết hàm số

**`h1`** — Đề thi thường cho một câu như sau: biết tích phân từ không đến hai của f bằng ba, tích phân của g bằng âm một, hãy tính tích phân của hai f trừ ba g cộng một. Ta không hề biết f và g là hàm gì! Bí quyết nằm ở các tính chất của tích phân, chủ đề của tập hôm nay.

**`h2`** — Đây là tập mười ba của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: các tính chất của tích phân.

**`h3`** — Sau video này, em sẽ nắm được ba nhóm tính chất. Một, tuyến tính: tách tổng và đưa hằng số ra ngoài. Hai, cộng khoảng và đổi cận. Ba, so sánh tích phân, ước lượng, và tính chất hàm chẵn, hàm lẻ.

## Bản chất

### ⏱ Tính chất tuyến tính

**`c1`** — Tính chất tuyến tính. Tích phân của k f cộng m g bằng k nhân tích phân của f, cộng m nhân tích phân của g. Lý do rất đơn giản: nguyên hàm có tính chất này, nên hiệu F của b trừ F của a cũng vậy. Về hình học, nhân f với k thì diện tích cũng nhân k.

**`c2`** — Áp dụng cho bài mở đầu. Tích phân của hai f trừ ba g cộng một bằng hai nhân ba, trừ ba nhân âm một, cộng tích phân của một trên đoạn dài hai, tức là cộng hai. Kết quả: sáu cộng ba cộng hai, bằng mười một. Đừng quên số hạng hằng số: tích phân của một bằng độ dài đoạn.

### ⏱ Cộng khoảng và đổi cận

**`c3`** — Tính chất cộng khoảng. Với b nằm giữa a và c, tích phân từ a đến c bằng tích phân từ a đến b cộng tích phân từ b đến c. Trên hình, miền diện tích được cắt làm hai mảnh tại b. Nhờ quy ước đổi cận, công thức còn đúng cả khi b nằm ngoài đoạn.

**`c4`** — Ví dụ: biết tích phân từ không đến một của f bằng hai và từ không đến ba bằng năm. Khi đó tích phân từ một đến ba bằng năm trừ hai, bằng ba. Và tích phân từ ba đến một, đổi chỗ cận, bằng âm ba.

**`c4b`** — Một chi tiết tinh tế: điểm chia b không nhất thiết nằm giữa a và c. Ví dụ, tích phân từ không đến một bằng tích phân từ không đến ba cộng tích phân từ ba đến một. Phần đi quá rồi quay lại tự triệt tiêu nhờ quy ước đổi cận. Vì vậy công thức cộng khoảng đúng với mọi ba số a, b, c trong miền liên tục.

### ⏱ So sánh và ước lượng

**`c5`** — Tính chất so sánh. Nếu f lớn hơn hoặc bằng g trên đoạn từ a đến b thì tích phân của f lớn hơn hoặc bằng tích phân của g. Đặc biệt, f không âm thì tích phân không âm. Nếu m nhỏ hơn f nhỏ hơn M, thì tích phân bị kẹp giữa m nhân b trừ a và M nhân b trừ a, giữa hai hình chữ nhật.

### ⏱ Hàm chẵn, hàm lẻ

**`c6`** — Hàm chẵn và hàm lẻ trên đoạn đối xứng từ âm a đến a. Với hàm lẻ, phần bên trái và bên phải có dấu ngược nhau, nên tích phân bằng không. Với hàm chẵn, hai phần bằng nhau, nên tích phân bằng hai lần tích phân từ không đến a.

### ⏱ Bẫy tích và thương

**`c7`** — Cái bẫy quen thuộc: tích phân của một tích không bằng tích các tích phân. Ví dụ, tích phân từ không đến một của x nhân x bằng một phần ba, trong khi tích phân của x nhân với chính nó chỉ bằng một phần tư. Tương tự với thương.

## Ví dụ

### ⏱ Ví dụ 1: cắt tại điểm nối

**`e1`** — Ví dụ một: hàm từng khúc. f bằng x bình phương khi x nhỏ hơn hoặc bằng một, bằng hai x trừ một khi x lớn hơn một. Tính tích phân từ không đến hai. Cắt tại một: tích phân từ không đến một của x bình phương bằng một phần ba, cộng tích phân từ một đến hai của hai x trừ một, bằng hai. Tổng là bảy phần ba.

### ⏱ Ví dụ 2: ước lượng

**`e2`** — Ví dụ hai: ước lượng tích phân từ không đến một của e mũ x bình phương, một tích phân không tính được bằng nguyên hàm sơ cấp. Trên đoạn này, e mũ x bình phương nằm giữa một và e. Vậy tích phân nằm giữa một và e. Máy tính cho giá trị xấp xỉ một phẩy bốn sáu, đúng trong khoảng đó.

### ⏱ Ví dụ 3: tách chẵn lẻ

**`e3`** — Ví dụ ba: tích phân từ âm hai đến hai của x lập phương cộng ba x bình phương. Phần x lập phương là hàm lẻ, cho không. Phần ba x bình phương là hàm chẵn, bằng hai lần tích phân từ không đến hai, tức là hai nhân tám, bằng mười sáu.

### ⏱ Ví dụ 4: tìm cận

**`e4`** — Ví dụ bốn, bài toán ngược: tìm số dương m sao cho tích phân từ không đến m của hai x cộng một bằng sáu. Tích phân bằng m bình phương cộng m. Giải phương trình m bình phương cộng m trừ sáu bằng không, được m bằng hai hoặc m bằng âm ba. Vì m dương nên m bằng hai.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Biết tích phân từ một đến ba của f bằng bốn, của g bằng âm hai, và tích phân từ ba đến năm của f bằng một. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: bốn cộng âm hai bằng hai. Ý b đúng: ba nhân bốn bằng mười hai.

**`x3`** — Ý c sai: cộng khoảng cho bốn cộng một, bằng năm, không phải ba. Ý d sai: đây là bẫy tích. Tích phân của f nhân g không thể suy ra từ hai tích phân riêng lẻ.

### ⏱ Trả lời ngắn và mẹo hàm thay thế

**`x4`** — Câu trả lời ngắn. Biết tích phân từ không đến hai của f bằng năm. Tính tích phân từ không đến hai của ba f trừ hai x. Theo tuyến tính: ba nhân năm, trừ tích phân của hai x từ không đến hai bằng bốn. Kết quả mười một.

**`x5`** — Mẹo hàm thay thế: khi đề chỉ cho giá trị tích phân, hãy chọn một hàm hằng thỏa điều kiện. Ở bài vừa rồi, chọn f bằng năm phần hai trên đoạn dài hai, rồi bấm máy tính tích phân của ba nhân năm phần hai trừ hai x. Máy cho đúng mười một. Mẹo này chỉ dùng khi đề hỏi biểu thức tuyến tính theo f.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, tuyến tính: tách tổng hiệu, đưa hằng số ra ngoài, và tích phân của hằng số bằng hằng số nhân độ dài đoạn. Hai, cộng khoảng và đổi cận. Ba, so sánh, ước lượng, và tính chất chẵn lẻ trên đoạn đối xứng.

**`o2`** — Bài tập tự luyện. Một, biết tích phân từ không đến ba của f bằng sáu và của g bằng hai, tính tích phân của f trừ hai g cộng ba. Hai, tích phân từ âm hai đến hai của x lập phương cộng x. Ba, tích phân từ âm một đến một của ba x bình phương cộng năm x. Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập mười bốn, ta xử lý tích phân chứa trị tuyệt đối và hàm cho theo từng khúc: xét dấu rồi tách cận. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. ∫₀³f = 6, ∫₀³g = 2: tính ∫₀³(f − 2g + 3) dx. → **11**
2. ∫₋₂²(x³ + x) dx → **0**
3. ∫₋₁¹(3x² + 5x) dx → **2**
