# INT09 – Nguyên hàm từng phần: Chọn u, dv & sơ đồ đường chéo

> Sinh tự động từ `int09/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int09`.

**Số nhịp:** 24 · **Số công thức Typst:** 43 · **Từ:** 1318

## Mở đầu

### ⏱ Mở đầu: tích của hai hàm khác loại

**`h1`** — Nguyên hàm của x nhân e mũ x. Đây là tích của hai hàm khác loại: một đa thức và một hàm mũ. Không tách được như tổng, và đổi biến cũng bế tắc vì đạo hàm của phần bên trong không xuất hiện. Ta cần một công cụ mới, sinh ra từ quy tắc đạo hàm của một tích.

**`h2`** — Đây là tập chín của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: phương pháp nguyên hàm từng phần. Đây là nội dung mở rộng, dành cho học sinh giỏi và các kỳ thi đánh giá năng lực.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, công thức từng phần và ý nghĩa hình học bằng diện tích. Hai, quy tắc chọn u theo thứ tự nhất lô, nhì đa, tam lượng, tứ mũ. Ba, sơ đồ đường chéo để làm nhanh, và dạng lặp lại quay về chính nó.

## Bản chất

### ⏱ Công thức từng phần

**`c1`** — Đạo hàm của tích u nhân v bằng u phẩy v cộng u v phẩy. Lấy nguyên hàm hai vế rồi chuyển vế, ta được công thức: nguyên hàm của u d v bằng u v trừ nguyên hàm của v d u. Ý tưởng là đổi một nguyên hàm khó thành một nguyên hàm dễ hơn.

### ⏱ Ý nghĩa hình học: ghép diện tích

**`c2`** — Ý nghĩa hình học rất đẹp. Vẽ đường cong trên mặt phẳng với trục ngang là v và trục đứng là u. Phần diện tích màu xanh, nằm dưới đường cong, chính là nguyên hàm của u d v. Phần màu vàng, nằm bên trái đường cong, là nguyên hàm của v d u. Hai phần ghép lại đúng bằng hiệu diện tích hai hình chữ nhật u v.

### ⏱ Chọn u: nhất lô, nhì đa, tam lượng, tứ mũ

**`c3`** — Bước quan trọng nhất là chọn u. Thứ tự ưu tiên để chọn u là: nhất lô, nhì đa, tam lượng, tứ mũ. Tức là lô ga rít trước, rồi đến đa thức, rồi lượng giác, cuối cùng là hàm mũ. Phần còn lại là d v.

**`c4`** — Áp dụng cho x nhân e mũ x. Đa thức đứng trước hàm mũ, nên đặt u bằng x, d v bằng e mũ x d x. Khi đó d u bằng d x và v bằng e mũ x. Công thức cho: x e mũ x trừ nguyên hàm của e mũ x, bằng x e mũ x trừ e mũ x cộng C.

**`c5`** — Nếu chọn ngược, u bằng e mũ x và d v bằng x d x, thì v bằng x bình phương chia hai, và nguyên hàm còn lại là x bình phương e mũ x chia hai: khó hơn bài ban đầu. Đó là lý do thứ tự chọn u rất quan trọng.

### ⏱ Hai ví dụ kinh điển

**`c6`** — Với nguyên hàm của lô ga nê pe x, tưởng như không có tích, nhưng ta coi d v bằng d x. Đặt u bằng lô ga nê pe x, d u bằng d x chia x, v bằng x. Kết quả là x lô ga nê pe x trừ x cộng C.

**`c7`** — Với x nhân cốt x: đa thức đứng trước lượng giác, nên u bằng x, d v bằng cốt x d x, v bằng sin x. Được x sin x trừ nguyên hàm của sin x, tức là x sin x cộng cốt x cộng C.

### ⏱ Sơ đồ đường chéo

**`c8`** — Khi đa thức có bậc cao, ví dụ x bình phương e mũ x, phải từng phần nhiều lần. Sơ đồ đường chéo giúp làm nhanh: cột trái lấy đạo hàm liên tiếp của x bình phương cho tới khi bằng không, cột phải lấy nguyên hàm liên tiếp của e mũ x. Nhân theo đường chéo với dấu cộng, trừ xen kẽ.

**`c9`** — Kết quả: x bình phương e mũ x, trừ hai x e mũ x, cộng hai e mũ x, cộng C. Một đa thức bậc n cần đúng n lần từng phần, tương ứng n đường chéo trước khi cột đạo hàm về không.

### ⏱ Dạng lặp lại

**`c10`** — Dạng chuyên sâu: nguyên hàm lặp lại. Với e mũ x nhân sin x, từng phần hai lần sẽ quay về chính nguyên hàm ban đầu, gọi là I. Ta được phương trình I bằng e mũ x sin x trừ e mũ x cốt x trừ I. Giải ra: I bằng e mũ x nhân sin x trừ cốt x, chia hai, cộng C.

## Ví dụ

### ⏱ Ví dụ 1–2

**`e1`** — Ví dụ một: nguyên hàm của x lô ga nê pe x. Lô ga rít đứng đầu, nên u bằng lô ga nê pe x, d v bằng x d x, v bằng x bình phương chia hai. Kết quả là x bình phương lô ga nê pe x chia hai, trừ x bình phương chia bốn, cộng C.

**`e2`** — Ví dụ hai: nguyên hàm của x sin hai x. Đặt u bằng x, v bằng âm cốt hai x chia hai. Kết quả là âm x cốt hai x chia hai, cộng sin hai x chia bốn, cộng C.

### ⏱ Ví dụ 3: sơ đồ đường chéo bậc ba

**`e3`** — Ví dụ ba, dùng sơ đồ đường chéo: nguyên hàm của x lập phương e mũ x. Cột đạo hàm: x lập phương, ba x bình phương, sáu x, sáu, rồi không. Cột nguyên hàm toàn là e mũ x. Nhân chéo với dấu xen kẽ, ta được x lập phương e mũ x, trừ ba x bình phương e mũ x, cộng sáu x e mũ x, trừ sáu e mũ x, cộng C. Ba lần từng phần chỉ gói gọn trong một bảng.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Cho hàm số f của x bằng x e mũ x. F là một nguyên hàm của f trên R. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: đây là cách chọn chuẩn theo thứ tự ưu tiên. Ý b sai: dấu cộng phải là dấu trừ. Lấy đạo hàm vế phải sẽ ra x e mũ x cộng hai e mũ x, không bằng f.

**`x3`** — Ý c đúng: x e mũ x trừ e mũ x chính là e mũ x nhân x trừ một. Ý d sai: F của không bằng âm một cộng C bằng không nên C bằng một, và F của một bằng không cộng một, bằng một chứ không phải e.

### ⏱ Trả lời ngắn và mẹo kiểm tra

**`x4`** — Câu trả lời ngắn. F là nguyên hàm của lô ga nê pe x trên khoảng dương, F của một bằng không. Tính F của hai, làm tròn đến hàng phần trăm. F bằng x lô ga nê pe x trừ x cộng C, F của một bằng âm một cộng C nên C bằng một. Vậy F của hai bằng hai lô ga nê pe hai trừ một, xấp xỉ không phẩy ba chín.

**`x5`** — Mẹo kiểm tra: kết quả từng phần luôn có dạng u v trừ một phần bù. Lấy đạo hàm để kiểm tra, đặc biệt chú ý dấu. Phần lớn lỗi sai của từng phần nằm ở dấu trừ trước nguyên hàm thứ hai. Ví dụ, đạo hàm của x e mũ x trừ e mũ x bằng e mũ x cộng x e mũ x trừ e mũ x, còn lại đúng x e mũ x.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, nguyên hàm của u d v bằng u v trừ nguyên hàm của v d u. Hai, chọn u theo thứ tự nhất lô, nhì đa, tam lượng, tứ mũ. Ba, đa thức bậc cao dùng sơ đồ đường chéo, còn dạng lặp lại thì giải phương trình theo I.

**`o2`** — Bài tập tự luyện. Một, nguyên hàm của x e mũ hai x. Hai, nguyên hàm của lô ga nê pe của x cộng một. Ba, nguyên hàm của x bình phương cốt x, dùng sơ đồ đường chéo. Đáp số hiện ở cuối màn hình.

**`o3`** — Tập mười sẽ khép lại phần nguyên hàm bằng các bài toán thực tế: từ tốc độ thay đổi tìm lại đại lượng, cùng một bài tổng ôn. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. Tìm ∫x e²ˣ dx. → **x e²ˣ/2 − e²ˣ/4 + C**
2. Tìm ∫ln(x + 1) dx. → **(x + 1) ln(x + 1) − x + C**
3. Tìm ∫x² cos x dx. → **x² sin x + 2x cos x − 2 sin x + C**
