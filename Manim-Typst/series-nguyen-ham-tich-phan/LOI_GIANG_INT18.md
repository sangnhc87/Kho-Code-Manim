# INT18 – Hàm ẩn & tính đối xứng: Phép đổi biến x → a + b − x

> Sinh tự động từ `int18/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int18`.

**Số nhịp:** 24 · **Số công thức Typst:** 48 · **Từ:** 1359

## Mở đầu

### ⏱ Mở đầu: ba dòng thay cho một trang

**`h1`** — Tính tích phân từ không đến pi phần hai của sin x chia cho sin x cộng cốt x. Tìm nguyên hàm khá vất vả. Nhưng có một cách chỉ mất ba dòng, dựa vào tính đối xứng, và đáp số là pi phần tư.

**`h2`** — Đây là tập mười tám của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: tích phân hàm ẩn và tính đối xứng.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, phép đổi biến x thành a cộng b trừ x và ý nghĩa gập đối xứng. Hai, kỹ thuật cộng hai tích phân để triệt tiêu phần khó. Ba, tính tích phân của hàm ẩn khi chỉ biết một hệ thức như f của x cộng f của trừ x.

## Bản chất

### ⏱ Gập đối xứng: x → a + b − x

**`c1`** — Tính chất then chốt: tích phân từ a đến b của f của x bằng tích phân từ a đến b của f của a cộng b trừ x. Về hình học, đồ thị của f của a cộng b trừ x là đồ thị của f lật qua đường thẳng đứng ở giữa đoạn. Lật một miền thì diện tích không đổi.

**`c2`** — Chứng minh bằng đổi biến: đặt t bằng a cộng b trừ x, d t bằng trừ d x. Khi x bằng a thì t bằng b, khi x bằng b thì t bằng a. Dấu trừ của d t vừa đủ để đảo cận trở lại. Ta thu được đúng tích phân ban đầu.

### ⏱ Cộng hai tích phân

**`c3`** — Áp dụng cho bài mở đầu, với a bằng không, b bằng pi phần hai. Sin của pi phần hai trừ x là cốt x, nên I cũng bằng tích phân của cốt x chia sin x cộng cốt x. Cộng hai cách viết của I, tử số cộng lại bằng mẫu số. Hai I bằng tích phân của một, bằng pi phần hai. Vậy I bằng pi phần tư.

### ⏱ Dấu hiệu dùng phép gập

**`c3b`** — Khi nào nên nghĩ đến phép gập? Ba dấu hiệu thường gặp. Một, biểu thức chứa sin và cốt trên đoạn từ không đến pi phần hai, vì phép gập đổi sin thành cốt. Hai, x nhân một hàm của sin x trên đoạn từ không đến pi. Ba, đoạn đối xứng từ trừ a đến a, hoặc đề cho hệ thức giữa f của x và f của a cộng b trừ x.

### ⏱ Hàm ẩn trên đoạn đối xứng

**`c4`** — Với đoạn đối xứng từ trừ a đến a, phép gập là x thành trừ x. Từ đó suy ra quen thuộc: hàm lẻ có tích phân bằng không, hàm chẵn có tích phân bằng hai lần nửa đoạn. Nhưng điều quan trọng hơn: tích phân của f của x luôn bằng tích phân của f của trừ x trên đoạn đối xứng.

**`c5`** — Vì vậy, khi đề chỉ cho hệ thức f của x cộng f của trừ x bằng g của x, ta lấy tích phân hai vế từ trừ a đến a. Vế trái thành hai lần tích phân của f. Suy ra tích phân của f bằng một nửa tích phân của g. Không cần biết f là hàm gì!

**`c6`** — Tổng quát hơn, nếu f của x cộng f của a cộng b trừ x bằng g của x trên đoạn từ a đến b, thì tích phân của f trên đoạn đó bằng một nửa tích phân của g. Đây là chìa khóa cho rất nhiều câu vận dụng cao.

## Ví dụ

### ⏱ Ví dụ 1: biết f(x) + f(−x)

**`e1`** — Ví dụ một: hàm f liên tục thỏa f của x cộng f của trừ x bằng cốt x. Tính tích phân từ trừ pi phần hai đến pi phần hai của f. Theo hệ quả trên, tích phân bằng một nửa tích phân của cốt x trên đoạn đó, bằng một nửa nhân hai, bằng một.

### ⏱ Ví dụ 2: khử x bằng đối xứng

**`e2`** — Ví dụ hai: tích phân từ không đến pi của x sin x. Gập đối xứng: I bằng tích phân của pi trừ x, nhân sin x, vì sin của pi trừ x vẫn là sin x. Cộng lại, hai I bằng pi nhân tích phân của sin x, bằng hai pi. Vậy I bằng pi, không cần từng phần.

**`e2b`** — Tổng quát từ ví dụ hai: tích phân từ không đến pi của x nhân f của sin x bằng pi phần hai nhân tích phân của f của sin x. Chẳng hạn, tích phân của x sin x chia một cộng cốt bình phương x bằng pi phần hai nhân pi phần hai, bằng pi bình phương phần tư. Phần chứa x đã biến mất.

### ⏱ Ví dụ 3: hàm ẩn qua đổi biến

**`e3`** — Ví dụ ba: biết tích phân từ một đến ba của f bằng sáu. Tính tích phân từ không đến một của f của hai x cộng một. Đặt t bằng hai x cộng một, d t bằng hai d x, cận mới từ một đến ba. Kết quả bằng một nửa nhân sáu, bằng ba.

### ⏱ Ví dụ 4: hệ thức hai ẩn

**`e4`** — Ví dụ bốn: f liên tục thỏa f của x cộng hai f của một trừ x bằng ba x bình phương. Tính tích phân từ không đến một của f. Gọi I là tích phân cần tìm. Theo tính chất gập, tích phân của f của một trừ x cũng bằng I. Lấy tích phân hai vế: I cộng hai I bằng một. Vậy I bằng một phần ba.

### ⏱ Ví dụ 5: ln(1 + tan x)

**`e5`** — Ví dụ năm, một bài kinh điển: tích phân từ không đến pi phần tư của l n của một cộng tan x. Gập đối xứng: một cộng tan của pi phần tư trừ x bằng hai chia một cộng tan x. Nên I cũng bằng tích phân của l n hai trừ l n của một cộng tan x. Cộng lại, hai I bằng pi phần tư nhân l n hai. Vậy I bằng pi phần tám nhân l n hai.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Cho hàm số f liên tục trên R thỏa f của x cộng f của trừ x bằng hai x bình phương cộng hai. Gọi I là tích phân từ trừ một đến một của f. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: đây là tính chất gập trên đoạn đối xứng. Ý b đúng: lấy tích phân hai vế của hệ thức, vế trái bằng hai I.

**`x3`** — Ý c đúng: tích phân của hai x bình phương cộng hai từ trừ một đến một bằng mười sáu phần ba, nên I bằng tám phần ba. Ý d sai: f bằng x bình phương cộng một cộng x cũng thỏa hệ thức nhưng không phải hàm chẵn. Hệ thức chỉ xác định phần chẵn của f.

### ⏱ Câu trả lời ngắn

**`x4`** — Câu trả lời ngắn: tính tích phân từ không đến pi phần hai của sin lập phương x chia cho sin lập phương cộng cốt lập phương, làm tròn đến hàng phần trăm. Gập đối xứng đổi sin thành cốt và ngược lại.

**`x5`** — Cộng hai cách viết, tử bằng mẫu, nên hai I bằng pi phần hai, I bằng pi phần tư, xấp xỉ không phẩy bảy chín. Ghi vào phiếu: không, phẩy, bảy, chín. Số mũ ba không làm thay đổi gì cả: mọi số mũ đều cho pi phần tư.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, tích phân không đổi khi thay x bằng a cộng b trừ x. Hai, cộng hai cách viết để tử số khớp với mẫu số, hoặc để khử biến x. Ba, với hàm ẩn, lấy tích phân hai vế của hệ thức rồi giải phương trình theo I.

**`o2`** — Bài tập tự luyện. Một, tích phân từ không đến pi phần hai của cốt mũ năm chia sin mũ năm cộng cốt mũ năm. Hai, f của x cộng f của trừ x bằng ba x bình phương, tính tích phân từ trừ một đến một của f. Ba, biết tích phân từ một đến năm của f bằng mười, tính tích phân từ không đến hai của f của hai x cộng một. Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập mười chín, ta gặp một kiểu hàm ẩn khác: biết đạo hàm của f liên hệ với chính f, như f phẩy bằng x nhân f. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. ∫₀^(π/2) cos⁵x/(sin⁵x + cos⁵x) dx → **π/4**
2. f(x) + f(−x) = 3x²: ∫₋₁¹ f(x) dx → **1**
3. ∫₁⁵ f = 10: ∫₀² f(2x + 1) dx → **5**
