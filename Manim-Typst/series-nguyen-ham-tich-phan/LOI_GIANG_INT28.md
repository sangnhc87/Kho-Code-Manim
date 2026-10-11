# INT28 – Dựng lại công thức thể tích: Trụ, nón, cầu, chỏm cầu, nón cụt bằng tích phân

> Sinh tự động từ `int28/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int28`.

**Số nhịp:** 24 · **Số công thức Typst:** 40 · **Từ:** 1252

## Mở đầu

### ⏱ Mở đầu: công thức chỏm cầu từ đâu ra?

**`h1`** — Thể tích chỏm cầu bằng pi h bình phương nhân R trừ h phần ba. Công thức này trông khá lạ, và rất khó nhớ nếu học thuộc lòng. Nhưng với tích phân, ta dựng lại nó chỉ trong ba dòng, và không bao giờ quên nữa.

**`h2`** — Đây là tập hai mươi tám, khép lại phần ứng dụng hình học: dựng lại các công thức thể tích bằng tích phân.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, chiến lược chung: đặt vật thể vào hệ trục và tìm đường sinh. Hai, dựng lại thể tích hình trụ, hình nón, hình cầu. Ba, các khối khó hơn: chỏm cầu, nón cụt và khối elip tròn xoay.

## Bản chất

### ⏱ Chiến lược: tìm đường sinh

**`c1`** — Chiến lược chung: mọi khối tròn xoay đều sinh ra khi quay một đường y bằng f của x quanh trục O x. Việc của ta là chọn hệ trục khéo léo để đường sinh có phương trình đơn giản, xác định cận, rồi áp dụng công thức pi nhân tích phân của f bình phương.

### ⏱ Hình trụ

**`c2`** — Hình trụ bán kính r, chiều cao h: đường sinh là đường nằm ngang y bằng r, với x từ không đến h. Thể tích bằng pi nhân tích phân của r bình phương, bằng pi r bình phương h. Đúng là diện tích đáy nhân chiều cao.

**`c2b`** — Một biến thể: ống trụ rỗng, bán kính ngoài R, bán kính trong r, dài h. Đây là bài vành khăn của tập trước, với hai đường nằm ngang. Thể tích bằng pi nhân R bình phương trừ r bình phương, nhân h. Chú ý lại một lần nữa: không phải pi nhân R trừ r, bình phương.

### ⏱ Hình nón

**`c3`** — Hình nón: đường sinh là đoạn thẳng từ gốc tọa độ, y bằng r chia h nhân x. Tích phân của x bình phương từ không đến h cho h lập phương chia ba, nên thể tích bằng một phần ba pi r bình phương h. Hình nón bằng đúng một phần ba hình trụ cùng đáy, cùng chiều cao.

### ⏱ Hình cầu

**`c4`** — Hình cầu: đường sinh là nửa đường tròn y bằng căn của R bình phương trừ x bình phương, x từ trừ R đến R. Bình phương làm mất căn, tích phân của R bình phương trừ x bình phương cho bốn phần ba R lập phương. Thể tích hình cầu bằng bốn phần ba pi R lập phương.

**`c5`** — Một quan hệ đẹp do Archimedes phát hiện: hình cầu nội tiếp trong hình trụ cao hai R có thể tích bằng hai phần ba hình trụ. Hình trụ có thể tích hai pi R lập phương, hai phần ba của nó là bốn phần ba pi R lập phương. Archimedes tự hào về kết quả này đến mức muốn khắc nó lên bia mộ.

## Ví dụ

### ⏱ Chỏm cầu

**`e1`** — Chỏm cầu chiều cao h là phần hình cầu nằm giữa x bằng R trừ h và x bằng R. Vẫn đường sinh của hình cầu, chỉ đổi cận. Tích phân từ R trừ h đến R của R bình phương trừ x bình phương, rút gọn lại được pi h bình phương nhân R trừ h phần ba. Đó chính là công thức ở đầu bài.

**`e2`** — Kiểm tra hai trường hợp đặc biệt. Khi h bằng R, chỏm cầu là nửa hình cầu: pi R bình phương nhân hai R phần ba, bằng hai phần ba pi R lập phương, đúng một nửa hình cầu. Khi h bằng hai R, ta được cả hình cầu. Công thức đúng ở cả hai đầu.

### ⏱ Nón cụt

**`e3`** — Nón cụt có bán kính hai đáy R và r, chiều cao h. Đường sinh là đoạn thẳng y bằng r cộng R trừ r chia h nhân x. Tích phân cho pi h chia ba nhân R bình phương cộng R r cộng r bình phương. Khi r bằng không, ta trở về hình nón.

**`e3b`** — Thử với số: nón cụt có R bằng hai, r bằng một, h bằng ba. Thể tích bằng pi nhân ba chia ba, nhân bốn cộng hai cộng một, bằng bảy pi. Kiểm tra bằng hiệu hai hình nón: nón lớn cao sáu, đáy bán kính hai, trừ nón nhỏ cao ba, đáy bán kính một, tám pi trừ pi, cũng bằng bảy pi.

### ⏱ Khối elip tròn xoay

**`e4`** — Khối elip tròn xoay: quay elip x bình phương chia a bình phương cộng y bình phương chia b bình phương bằng một quanh O x. y bình phương bằng b bình phương nhân một trừ x bình phương chia a bình phương. Thể tích bằng bốn phần ba pi a b bình phương. Khi a bằng b bằng R, ta lại được hình cầu.

### ⏱ Ví dụ: nước trong bát

**`e5`** — Bài toán thực tế: một chiếc bát hình bán cầu bán kính mười xăng ti mét chứa nước sâu bốn xăng ti mét. Phần nước là một chỏm cầu với R bằng mười, h bằng bốn. Thể tích bằng pi nhân mười sáu nhân mười trừ bốn phần ba, bằng bốn trăm mười sáu pi chia ba, khoảng bốn trăm ba mươi sáu xăng ti mét khối.

### ⏱ Bonus: thể tích và diện tích mặt cầu

**`e6`** — Một điều thú vị để kết thúc phần ví dụ: đạo hàm của thể tích hình cầu theo R là bốn pi R bình phương, đúng bằng diện tích mặt cầu. Tương tự, đạo hàm của diện tích hình tròn pi R bình phương là chu vi hai pi R. Thêm một lớp vỏ mỏng dày d R thì thể tích tăng thêm khoảng diện tích mặt nhân d R.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai về khối cầu bán kính ba, sinh bởi nửa đường tròn quay quanh O x. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: nửa đường tròn tâm gốc tọa độ bán kính ba có phương trình y bằng căn chín trừ x bình phương. Ý b đúng: đây là công thức đĩa với cận từ trừ ba đến ba.

**`x3`** — Ý c sai: tích phân bằng ba mươi sáu, nên V bằng ba mươi sáu pi, không phải hai mươi bảy pi. Ý d đúng: chỏm cầu cao một có thể tích pi nhân ba trừ một phần ba, bằng tám pi chia ba.

### ⏱ Câu trả lời ngắn

**`x4`** — Câu trả lời ngắn: bồn chứa có dạng chỏm cầu bán kính năm mét, chiều cao hai mét. Tính thể tích bồn theo mét khối, làm tròn đến hàng đơn vị.

**`x5`** — Thể tích bằng pi nhân bốn nhân năm trừ hai phần ba, bằng năm mươi hai pi chia ba, xấp xỉ năm mươi tư phẩy năm. Làm tròn đến hàng đơn vị được năm mươi tư. Hoặc tính trực tiếp tích phân từ ba đến năm của hai lăm trừ x bình phương, nhân pi, cũng ra kết quả đó.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, mọi công thức thể tích tròn xoay đều đến từ pi nhân tích phân của f bình phương. Hai, chọn hệ trục để đường sinh đơn giản: đường nằm ngang, đường thẳng qua gốc, nửa đường tròn. Ba, chỏm cầu là hình cầu với cận khác; quên công thức thì dựng lại.

**`o2`** — Bài tập tự luyện. Một, thể tích hình trụ bán kính hai, cao năm. Hai, chỏm cầu bán kính bốn, cao một. Ba, khối elip tròn xoay với a bằng ba, b bằng hai. Đáp số hiện ở cuối màn hình.

**`o3`** — Từ tập hai mươi chín, ta bước sang phần D: ứng dụng thực tế, bắt đầu với các bài toán chuyển động như phanh xe và hai xe gặp nhau. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. Hình trụ r = 2, h = 5 → **20π**
2. Chỏm cầu R = 4, h = 1 → **11π/3**
3. Khối elip tròn xoay a = 3, b = 2 → **16π**
