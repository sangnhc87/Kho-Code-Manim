# INT17 – Tích phân từng phần: Chọn u – dv theo thứ tự ưu tiên

> Sinh tự động từ `int17/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int17`.

**Số nhịp:** 24 · **Số công thức Typst:** 44 · **Từ:** 1260

## Mở đầu

### ⏱ Mở đầu: tích của hai loại hàm

**`h1`** — Tính tích phân từ không đến một của x nhân e mũ x. Không có bảng nguyên hàm nào cho tích này, và đổi biến số cũng không giúp được gì. Vậy mà đáp số lại gọn đến bất ngờ: đúng bằng một. Công cụ giúp ta làm điều đó là tích phân từng phần.

**`h2`** — Đây là tập mười bảy của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: tích phân từng phần.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, công thức từng phần và ý nghĩa hình học của nó. Hai, quy tắc chọn u: nhất log, nhì đa, tam lượng, tứ mũ. Ba, các dạng phải dùng từng phần hai lần.

## Bản chất

### ⏱ Công thức từng phần

**`c1`** — Công thức xuất phát từ đạo hàm của tích: u nhân v, phẩy, bằng u phẩy v cộng u v phẩy. Lấy tích phân hai vế từ a đến b rồi chuyển vế, ta được: tích phân của u d v bằng u v lấy cận từ a đến b, trừ tích phân của v d u.

### ⏱ Diện tích hình chữ nhật uv tách làm hai

**`c2`** — Ý nghĩa hình học: vẽ đường cong với hoành độ u và tung độ v. Phần diện tích nằm giữa đường cong và trục tung là tích phân của u d v. Phần nằm giữa đường cong và trục hoành là tích phân của v d u. Hai phần ghép lại đúng bằng hình chữ nhật lớn trừ hình chữ nhật nhỏ, tức là u v lấy cận.

### ⏱ Nhất log, nhì đa, tam lượng, tứ mũ

**`c3`** — Muốn dùng công thức, ta tách biểu thức dưới dấu tích phân thành u nhân d v. Quy tắc chọn u theo thứ tự ưu tiên: nhất log, nhì đa, tam lượng, tứ mũ. Tức là ưu tiên chọn u là hàm logarit, rồi đến đa thức, rồi lượng giác, cuối cùng là hàm mũ. Phần còn lại là d v.

**`c4`** — Lý do: u được lấy đạo hàm nên cần trở nên đơn giản hơn. Logarit đạo hàm thành phân thức, đa thức giảm bậc. Còn d v được lấy nguyên hàm nên phải dễ tìm v, mà e mũ x hay sin, cốt thì nguyên hàm rất dễ.

**`c5`** — Áp dụng cho bài mở đầu. Đặt u bằng x, d v bằng e mũ x d x, suy ra d u bằng d x, v bằng e mũ x. Tích phân bằng x e mũ x lấy cận từ không đến một, trừ tích phân của e mũ x. Ta được e trừ, e trừ một, bằng một.

### ⏱ Chọn ngược thì sao?

**`c6`** — Nếu chọn ngược, đặt u bằng e mũ x và d v bằng x d x, thì v bằng x bình phương phần hai, và tích phân mới chứa x bình phương nhân e mũ x, còn khó hơn bài ban đầu. Chọn sai thứ tự làm bài toán phức tạp thêm.

### ⏱ Từng phần hay đổi biến?

**`c7`** — Khi nào dùng từng phần, khi nào dùng đổi biến? Nếu thấy hàm hợp đi kèm đạo hàm của phần bên trong, hãy đổi biến. Nếu thấy tích của hai loại hàm khác nhau, như đa thức nhân hàm mũ, đa thức nhân lượng giác, hay logarit nhân đa thức, thì dùng từng phần. Ví dụ x nhân e mũ x bình phương là đổi biến, còn x nhân e mũ x là từng phần.

## Ví dụ

### ⏱ Ví dụ 1: u = ln x

**`e1`** — Ví dụ một: tích phân từ một đến e của l n x. Chỉ có một hàm, ta vẫn dùng từng phần với u bằng l n x, d v bằng d x. d u bằng d x chia x, v bằng x. Kết quả: x l n x lấy cận, trừ tích phân của một, bằng e trừ, e trừ một, bằng một.

### ⏱ Ví dụ 2: đa thức và lượng giác

**`e2`** — Ví dụ hai: tích phân từ không đến pi phần hai của x cốt x. Đa thức đứng trước lượng giác, nên u bằng x, d v bằng cốt x d x, v bằng sin x. Ta được x sin x lấy cận, bằng pi phần hai, trừ tích phân của sin x, bằng một. Kết quả: pi phần hai trừ một.

### ⏱ Ví dụ 3: logarit và đa thức

**`e3`** — Ví dụ ba: tích phân từ một đến e của x l n x. Logarit được ưu tiên, nên u bằng l n x, d v bằng x d x, v bằng x bình phương phần hai. Ta được e bình phương phần hai, trừ tích phân của x phần hai, bằng e bình phương trừ một, chia bốn. Kết quả: e bình phương cộng một, chia bốn.

### ⏱ Ví dụ 4: từng phần hai lần

**`e4`** — Ví dụ bốn: tích phân từ không đến một của x bình phương e mũ x. Từng phần lần một hạ x bình phương xuống hai x: được e trừ hai nhân tích phân của x e mũ x. Tích phân còn lại chính là bài mở đầu, bằng một. Kết quả: e trừ hai.

### ⏱ Sơ đồ đường chéo

**`e4b`** — Mẹo trình bày nhanh cho đa thức nhân hàm mũ: sơ đồ đường chéo. Cột trái lấy đạo hàm liên tiếp của x bình phương: hai x, hai, rồi không. Cột phải lấy nguyên hàm liên tiếp của e mũ x. Nhân chéo với dấu cộng, trừ, cộng xen kẽ, ta có nguyên hàm x bình phương trừ hai x cộng hai, nhân e mũ x. Thay cận được e trừ hai, khớp với kết quả trên.

**`e5`** — Dạng đặc biệt: tích phân của e mũ x nhân sin x. Từng phần hai lần, tích phân ban đầu xuất hiện lại ở vế phải. Coi nó là ẩn I rồi giải phương trình bậc nhất. Từ không đến pi, ta được I bằng e mũ pi cộng một, chia hai.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Cho I bằng tích phân từ không đến một của hai x cộng một, nhân e mũ x. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a sai: theo thứ tự ưu tiên, đa thức đứng trước hàm mũ, nên u là hai x cộng một. Ý b đúng: d u bằng hai d x, nên tích phân còn lại có hệ số hai.

**`x3`** — Ý c đúng: ba e trừ một, trừ hai nhân e trừ một, bằng e cộng một. Ý d sai: e cộng một xấp xỉ ba phẩy bảy hai, nhỏ hơn bốn.

### ⏱ Câu trả lời ngắn

**`x4`** — Câu trả lời ngắn: tính tích phân từ không đến một của x nhân e mũ trừ x, làm tròn đến hàng phần trăm. Đặt u bằng x, d v bằng e mũ trừ x d x, suy ra v bằng trừ e mũ trừ x. Chú ý dấu trừ!

**`x5`** — Ta được trừ x e mũ trừ x lấy cận, bằng trừ một phần e, cộng tích phân của e mũ trừ x, bằng một trừ một phần e. Tổng là một trừ hai phần e, xấp xỉ không phẩy hai sáu. Ghi vào phiếu: không, phẩy, hai, sáu.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, công thức: tích phân u d v bằng u v lấy cận trừ tích phân v d u. Hai, chọn u theo thứ tự nhất log, nhì đa, tam lượng, tứ mũ. Ba, đa thức bậc cao thì từng phần nhiều lần, còn mũ nhân lượng giác thì giải phương trình theo I.

**`o2`** — Bài tập tự luyện. Một, tích phân từ không đến pi của x sin x. Hai, tích phân từ một đến hai của x l n x. Ba, tích phân từ không đến một của x e mũ hai x. Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập mười tám, ta học tích phân hàm ẩn và tính đối xứng, với phép đổi biến x thành a cộng b trừ x. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. ∫₀^π x sin x dx → **π**
2. ∫₁² x ln x dx → **2 ln 2 − 3/4**
3. ∫₀¹ x e^(2x) dx → **(e² + 1)/4**
