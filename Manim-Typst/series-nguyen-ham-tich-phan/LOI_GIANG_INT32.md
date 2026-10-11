# INT32 – Tích phân trong kinh tế và sinh học: Từ chi phí biên, tốc độ tăng trưởng đến tổng lượng

> Sinh tự động từ `int32/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int32`.

**Số nhịp:** 24 · **Số công thức Typst:** 35 · **Từ:** 1275

## Mở đầu

### ⏱ Mở đầu: chi phí tăng thêm

**`h1`** — Một xưởng có chi phí biên C phẩy của x bằng không phẩy ba x cộng hai mươi nghìn đồng cho mỗi sản phẩm. Xưởng đang sản xuất một trăm sản phẩm. Nếu sản xuất thêm một trăm sản phẩm nữa, chi phí tăng bao nhiêu? Đáp số là sáu triệu rưỡi đồng, và đó lại là một tích phân.

**`h2`** — Đây là tập ba mươi hai của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: tích phân trong kinh tế và sinh học.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, đại lượng biên là đạo hàm, tổng lượng là tích phân. Hai, lợi nhuận tăng thêm và sản lượng tối ưu. Ba, các mô hình tăng trưởng trong sinh học và y học.

## Bản chất

### ⏱ Đại lượng biên là đạo hàm

**`c1`** — Trong kinh tế, chi phí biên là chi phí để sản xuất thêm một sản phẩm, chính là đạo hàm C phẩy của x. Biết chi phí biên, ta tìm được chi phí tăng thêm khi sản lượng tăng từ a đến b: C của b trừ C của a bằng tích phân từ a đến b của C phẩy.

### ⏱ Lợi nhuận tăng thêm

**`c2`** — Tương tự, doanh thu biên là R phẩy, và lợi nhuận biên là doanh thu biên trừ chi phí biên. Lợi nhuận tăng thêm khi sản lượng tăng từ a đến b là tích phân của R phẩy trừ C phẩy. Trên đồ thị, đó là phần diện tích nằm giữa hai đường biên.

### ⏱ Sản lượng tối ưu

**`c3`** — Lợi nhuận tăng khi doanh thu biên lớn hơn chi phí biên, giảm khi ngược lại. Vì vậy sản lượng tối ưu là nơi doanh thu biên bằng chi phí biên, tức giao điểm của hai đường biên. Ý tưởng này giống hệt bài toán hai xe ở tập hai mươi chín.

### ⏱ Thặng dư tiêu dùng

**`c3b`** — Một khái niệm nữa: thặng dư tiêu dùng. Với hàm cầu giá theo số lượng D của x và giá bán P, những người sẵn sàng trả cao hơn P đã được lợi. Tổng phần lợi đó là diện tích giữa đường cầu và đường giá: tích phân từ không đến Q của D trừ P. Ví dụ D bằng một trăm trừ không phẩy năm x, P bằng sáu mươi, thì Q bằng tám mươi và thặng dư bằng một nghìn sáu trăm.

### ⏱ Tăng trưởng trong sinh học

**`c4`** — Trong sinh học, tốc độ tăng trưởng của một quần thể là N phẩy của t. Số cá thể tại thời điểm T bằng số ban đầu cộng tích phân từ không đến T của tốc độ tăng trưởng. Mọi bài toán tốc độ đều theo cùng một khuôn: tổng lượng bằng giá trị đầu cộng tích phân của tốc độ.

**`c5`** — Trong y học, tốc độ đào thải thuốc thường giảm dần theo hàm mũ. Lượng thuốc bị đào thải sau T giờ là tích phân của tốc độ đào thải. Đơn vị cần nhất quán: mi li gam mỗi giờ nhân giờ cho mi li gam.

## Ví dụ

### ⏱ Ví dụ 1: chi phí tăng thêm

**`e1`** — Ví dụ một, giải bài mở đầu. Chi phí tăng thêm bằng tích phân từ một trăm đến hai trăm của không phẩy ba x cộng hai mươi, bằng không phẩy một năm nhân ba mươi nghìn, cộng hai nghìn, tức sáu nghìn năm trăm nghìn đồng, bằng sáu phẩy năm triệu đồng.

### ⏱ Ví dụ 2: sản lượng tối ưu

**`e2`** — Ví dụ hai: doanh thu biên một trăm trừ không phẩy hai x, chi phí biên hai mươi cộng không phẩy hai x, nghìn đồng mỗi sản phẩm. Lợi nhuận biên tám mươi trừ không phẩy bốn x bằng không tại x bằng hai trăm: đó là sản lượng tối ưu.

**`e3`** — Lợi nhuận tăng thêm khi nâng sản lượng từ một trăm lên hai trăm bằng tích phân của tám mươi trừ không phẩy bốn x, bằng tám nghìn trừ sáu nghìn, bằng hai nghìn nghìn đồng, tức hai triệu đồng. Nếu sản xuất vượt hai trăm, mỗi sản phẩm thêm lại làm lợi nhuận giảm.

### ⏱ Ví dụ 3: vi khuẩn

**`e4`** — Ví dụ ba: một đàn vi khuẩn có năm nghìn con, tốc độ tăng trưởng một nghìn nhân e mũ không phẩy hai t con mỗi giờ. Sau mười giờ, số vi khuẩn bằng năm nghìn cộng năm nghìn nhân e bình phương trừ một, bằng năm nghìn e bình phương, khoảng ba mươi sáu nghìn chín trăm bốn mươi lăm con.

### ⏱ Ví dụ 4: đào thải thuốc

**`e5`** — Ví dụ bốn: tốc độ đào thải thuốc là hai mươi nhân e mũ trừ không phẩy năm t mi li gam mỗi giờ. Trong bốn giờ đầu, lượng thuốc bị đào thải bằng bốn mươi nhân một trừ e mũ trừ hai, khoảng ba mươi tư phẩy năm chín mi li gam.

### ⏱ Ví dụ 5: dân số

**`e6`** — Ví dụ năm: dân số một thành phố tăng với tốc độ hai cộng không phẩy một t nghìn người mỗi năm. Sau mười năm, dân số tăng thêm tích phân từ không đến mười, bằng hai mươi cộng năm, bằng hai mươi lăm nghìn người.

### ⏱ Ví dụ 6: tìm tham số

**`e7`** — Ví dụ sáu, bài toán ngược: dân số tăng với tốc độ a cộng không phẩy hai t nghìn người mỗi năm, và sau mười năm tăng thêm ba mươi nghìn người. Tích phân từ không đến mười bằng mười a cộng mười. Cho bằng ba mươi, ta được a bằng hai.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Một doanh nghiệp có chi phí biên C phẩy của x bằng hai x cộng năm mươi nghìn đồng, chi phí cố định C của không bằng một nghìn nghìn đồng. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: C bằng một nghìn cộng tích phân của hai u cộng năm mươi, bằng x bình phương cộng năm mươi x cộng một nghìn. Ý b đúng: C của mười bằng một trăm cộng năm trăm cộng một nghìn, bằng một nghìn sáu trăm.

**`x3`** — Ý c sai: chi phí tăng thêm từ mười đến hai mươi bằng tích phân của hai x cộng năm mươi, bằng ba trăm cộng năm trăm, bằng tám trăm. Ý d đúng: chi phí biên tại x bằng mười là hai mươi cộng năm mươi, bằng bảy mươi.

### ⏱ Câu trả lời ngắn

**`x4`** — Câu trả lời ngắn: một quần thể cá ban đầu có hai nghìn con, tốc độ tăng trưởng ba trăm căn t con mỗi năm. Sau bốn năm có bao nhiêu con cá?

**`x5`** — Số cá tăng thêm bằng tích phân từ không đến bốn của ba trăm căn t, bằng ba trăm nhân hai phần ba nhân t mũ ba phần hai lấy cận, bằng hai trăm nhân tám, bằng một nghìn sáu trăm. Tổng cộng ba nghìn sáu trăm con. Ghi vào phiếu: ba, sáu, không, không.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, đại lượng biên và tốc độ là đạo hàm; tổng lượng là giá trị đầu cộng tích phân. Hai, lợi nhuận tăng thêm là tích phân của doanh thu biên trừ chi phí biên; tối ưu khi hai đại lượng biên bằng nhau. Ba, sinh học và y học dùng cùng khuôn đó, thường với hàm mũ.

**`o2`** — Bài tập tự luyện. Một, chi phí biên không phẩy bốn x cộng mười, tính chi phí tăng thêm từ năm mươi đến một trăm sản phẩm. Hai, doanh thu biên sáu mươi trừ không phẩy một x, chi phí biên hai mươi cộng không phẩy một x: sản lượng tối ưu. Ba, quần thể năm trăm cá thể, tốc độ năm mươi e mũ không phẩy một t: số cá thể sau mười năm. Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập ba mươi ba, ta đi từ bảng số liệu thực tế đến hàm số và tích phân: mô hình hóa từ dữ liệu, với những câu trả lời ngắn nhiều bước. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. C'(x) = 0,4x + 10: chi phí tăng thêm từ 50 đến 100 sản phẩm → **2000 (nghìn đồng)**
2. R' = 60 − 0,1x, C' = 20 + 0,1x: sản lượng tối ưu → **x = 200**
3. N(0) = 500, N' = 50e^(0,1t): N(10) → **500e ≈ 1359**
