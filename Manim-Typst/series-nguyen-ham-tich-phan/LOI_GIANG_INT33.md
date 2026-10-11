# INT33 – Mô hình hóa từ dữ liệu thực: Bảng số, hàm số, tích phân và quy tắc hình thang

> Sinh tự động từ `int33/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int33`.

**Số nhịp:** 25 · **Số công thức Typst:** 35 · **Từ:** 1265

## Mở đầu

### ⏱ Mở đầu: chỉ có một bảng số

**`h1`** — Một chiếc xe được đo vận tốc mỗi hai giây: không, sáu, mười, mười hai, rồi mười hai mét trên giây. Không ai cho ta công thức của vận tốc, chỉ có một bảng số. Xe đã đi được bao xa trong tám giây? Có hai cách trả lời: tìm một hàm số khớp dữ liệu, hoặc cộng các hình thang. Hai kết quả rất gần nhau.

**`h2`** — Đây là tập ba mươi ba, khép lại phần ứng dụng thực tế: mô hình hóa từ dữ liệu thực.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, quy trình mô hình hóa: từ bảng số đến hàm số. Hai, quy tắc hình thang khi không có công thức. Ba, các bài trả lời ngắn nhiều bước kết hợp mô hình và tích phân.

## Bản chất

### ⏱ Quy trình mô hình hóa

**`c1`** — Quy trình mô hình hóa năm bước. Một, đọc dữ liệu và vẽ các điểm. Hai, chọn dạng hàm phù hợp, ví dụ bậc nhất, bậc hai hay hàm mũ. Ba, tìm hệ số từ dữ liệu. Bốn, tính tích phân. Năm, kiểm tra lại với các điểm dữ liệu còn lại.

**`c2`** — Tìm hệ số: mỗi điểm dữ liệu cho một phương trình. Với hàm bậc hai đi qua gốc tọa độ, v bằng a t bình phương cộng b t, chỉ cần hai điểm là đủ hai phương trình. Các điểm còn lại dùng để kiểm tra mô hình có tốt hay không.

**`c2b`** — Chọn dạng hàm thế nào? Nhìn hiệu giữa hai lần đo liên tiếp: sáu, bốn, hai, không. Hiệu không đổi là dấu hiệu của hàm bậc nhất. Hiệu giảm đều, mỗi bước bớt hai, là dấu hiệu của hàm bậc hai. Còn nếu tỉ số giữa hai lần đo không đổi, ta nghĩ đến hàm mũ. Ở đây v của không bằng không, nên hệ số tự do bằng không.

### ⏱ Quy tắc hình thang

**`c3`** — Khi không tìm được công thức, ta dùng quy tắc hình thang: nối các điểm dữ liệu bằng đoạn thẳng, và cộng diện tích các hình thang. Với các bước đo cách đều h, tích phân xấp xỉ h nhân, một nửa giá trị đầu cộng các giá trị giữa cộng một nửa giá trị cuối.

**`c4`** — Quy tắc hình thang cho kết quả chính xác khi hàm là bậc nhất. Với đồ thị cong xuống, các đoạn thẳng nằm dưới đường cong, nên hình thang hơi thiếu; với đồ thị cong lên thì ngược lại. Đo dày hơn thì sai số nhỏ hơn.

### ⏱ Mô hình và hình thang

**`c5`** — Hai cách bổ sung cho nhau: mô hình hàm số cho công thức để dự đoán, quy tắc hình thang không cần giả thiết gì về dạng hàm. Trong đề thi mới, câu trả lời ngắn thường hỏi một trong hai cách, và yêu cầu làm tròn cẩn thận.

## Ví dụ

### ⏱ Ví dụ 1: tìm hàm khớp dữ liệu

**`e1`** — Ví dụ một, giải bài mở đầu bằng mô hình. Chọn v bằng a t bình phương cộng b t. Từ v của hai bằng sáu và v của bốn bằng mười, giải được a bằng trừ một phần tư, b bằng bảy phần hai. Kiểm tra: v của sáu bằng mười hai, v của tám bằng mười hai, khớp hoàn toàn.

**`e2`** — Quãng đường bằng tích phân từ không đến tám của trừ một phần tư t bình phương cộng bảy phần hai t, bằng hai trăm lẻ tám phần ba, khoảng sáu mươi chín phẩy ba ba mét.

**`e2b`** — Mô hình còn cho phép dự đoán. Thay t bằng mười, được v bằng mười; thay t bằng mười bốn, được v bằng không: mô hình nói xe dừng hẳn sau mười bốn giây. Nhưng dữ liệu chỉ đo đến giây thứ tám, nên dự đoán ngoài vùng dữ liệu, gọi là ngoại suy, luôn cần kiểm chứng thêm.

### ⏱ Ví dụ 2: quy tắc hình thang

**`e3`** — Ví dụ hai, cùng dữ liệu nhưng dùng quy tắc hình thang với bước h bằng hai: hai nhân, không cộng sáu cộng mười cộng mười hai cộng sáu, bằng sáu mươi tám mét. Hơi thiếu so với mô hình, đúng như dự đoán vì đồ thị cong xuống.

### ⏱ Ví dụ 3: lượng mưa

**`e4`** — Ví dụ ba: cường độ mưa đo mỗi giờ là không, bốn, mười, sáu, hai mi li mét mỗi giờ. Tổng lượng mưa trong bốn giờ, theo quy tắc hình thang, bằng không cộng bốn cộng mười cộng sáu cộng một, bằng hai mươi mốt mi li mét.

### ⏱ Ví dụ 4: mặt cắt con mương

**`e5`** — Ví dụ bốn, nhiều bước: mặt cắt một con mương được đo độ sâu tại năm điểm cách nhau một mét: không, một phẩy hai, một phẩy sáu, một phẩy hai, không. Dữ liệu khớp parabol y bằng một phẩy sáu trừ không phẩy bốn x bình phương.

**`e6`** — Diện tích mặt cắt bằng tích phân từ trừ hai đến hai, bằng sáu mươi tư phần mười lăm, khoảng bốn phẩy hai bảy mét vuông. Nước chảy với vận tốc không phẩy năm mét trên giây, nên lưu lượng khoảng hai phẩy một ba mét khối mỗi giây. Quy tắc hình thang cho bốn mét vuông, nhỏ hơn một chút.

### ⏱ Ví dụ 5: tìm số liệu bị thiếu

**`e7`** — Ví dụ năm, tìm số liệu bị thiếu: cường độ mưa đo mỗi giờ là không, bốn, a, sáu, hai mi li mét mỗi giờ, và tổng lượng mưa theo quy tắc hình thang là mười chín mi li mét. Tổng bằng không cộng bốn cộng a cộng sáu cộng một, tức mười một cộng a. Cho bằng mười chín, ta được a bằng tám mi li mét mỗi giờ.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Vận tốc một vật được đo mỗi giây: một, ba, năm, bảy, chín mét trên giây tại t từ không đến bốn. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: dữ liệu khớp chính xác v bằng hai t cộng một. Ý b đúng: tích phân từ không đến bốn của hai t cộng một bằng mười sáu cộng bốn, bằng hai mươi mét.

**`x3`** — Ý c đúng: với hàm bậc nhất, quy tắc hình thang cho kết quả chính xác: một nửa cộng ba cộng năm cộng bảy cộng bốn phẩy năm, bằng hai mươi. Ý d sai: hình chữ nhật trái chỉ cho một cộng ba cộng năm cộng bảy, bằng mười sáu.

### ⏱ Câu trả lời ngắn

**`x4`** — Câu trả lời ngắn: lưu lượng nước vào bể được đo mỗi năm phút: mười, mười bốn, hai mươi, mười tám, mười hai lít mỗi phút. Dùng quy tắc hình thang, ước lượng lượng nước vào bể trong hai mươi phút.

**`x5`** — Bước h bằng năm. Tổng bằng năm nhân, năm cộng mười bốn cộng hai mươi cộng mười tám cộng sáu, bằng năm nhân sáu mươi ba, bằng ba trăm mười lăm lít. Ghi vào phiếu: ba, một, năm.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, mô hình hóa: chọn dạng hàm, tìm hệ số từ dữ liệu, kiểm tra với điểm còn lại, rồi lấy tích phân. Hai, quy tắc hình thang: h nhân, một nửa đầu cộng các giá trị giữa cộng một nửa cuối. Ba, hình thang chính xác với hàm bậc nhất, sai số nhỏ khi đo dày.

**`o2`** — Bài tập tự luyện. Một, quy tắc hình thang với bước một và dữ liệu hai, bốn, tám, bốn. Hai, vận tốc dạng a t bình phương với v của hai bằng tám, tính quãng đường trong ba giây. Ba, mương sâu không, một, một phẩy năm, một, không, cách nhau một mét: diện tích theo hình thang. Đáp số hiện ở cuối màn hình.

**`o3`** — Phần D khép lại tại đây. Từ tập ba mươi tư là phần tổng ôn, bắt đầu với những bẫy sai kinh điển và cách kiểm tra đáp án bằng máy tính. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. Hình thang, h = 1, dữ liệu 2, 4, 8, 4 → **15**
2. v = at², v(2) = 8: quãng đường trong 3 giây → **18 m**
3. Mương sâu 0; 1; 1,5; 1; 0 (cách 1 m): diện tích → **3,5 m²**
