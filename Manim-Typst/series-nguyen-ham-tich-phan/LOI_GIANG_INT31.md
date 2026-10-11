# INT31 – Bồn chứa và lưu lượng: Lượng nước bằng tích phân của lưu lượng

> Sinh tự động từ `int31/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int31`.

**Số nhịp:** 24 · **Số công thức Typst:** 37 · **Từ:** 1224

## Mở đầu

### ⏱ Mở đầu: lưu lượng thay đổi

**`h1`** — Một bể rỗng chứa được một nghìn lít. Vòi nước mở càng lúc càng mạnh, lưu lượng hai mươi cộng bốn t lít mỗi phút. Bao lâu thì đầy bể? Không thể lấy một nghìn chia cho lưu lượng, vì lưu lượng thay đổi liên tục. Đáp số là khoảng mười bảy phẩy chín phút, và tích phân cho ta câu trả lời.

**`h2`** — Đây là tập ba mươi mốt của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: bồn chứa, bể nước và lưu lượng.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, lượng nước bằng tích phân của lưu lượng. Hai, bài toán vừa chảy vào vừa chảy ra. Ba, liên hệ giữa lượng nước và mực nước trong bể.

## Bản chất

### ⏱ Lưu lượng là đạo hàm của thể tích

**`c1`** — Lưu lượng là tốc độ thay đổi của thể tích nước: V phẩy của t bằng r của t. Vì vậy thể tích nước thay đổi một lượng bằng tích phân của lưu lượng: V của T trừ V của không bằng tích phân từ không đến T của r. Đây lại là công thức Newton Leibniz, với một ý nghĩa mới.

**`c2`** — Trên đồ thị lưu lượng theo thời gian, lượng nước chảy vào chính là diện tích dưới đồ thị. Lưu lượng không đổi thì diện tích là hình chữ nhật, quen thuộc như lưu lượng nhân thời gian. Lưu lượng thay đổi thì ta cần tích phân.

**`c2b`** — Vì sao là tích phân? Chia thời gian thành nhiều khoảng nhỏ. Trong mỗi khoảng, lưu lượng gần như không đổi, nên lượng nước xấp xỉ r của t nhân delta t, một cột hình chữ nhật. Cộng các cột lại và cho khoảng chia nhỏ dần, tổng tiến tới tích phân, giống hệt tập mười một.

### ⏱ Vào và ra

**`c3`** — Khi vừa có nước chảy vào, vừa có nước chảy ra, lưu lượng thực bằng lưu lượng vào trừ lưu lượng ra. Lượng nước trong bể tăng khi lưu lượng thực dương, giảm khi lưu lượng thực âm, và đạt lớn nhất đúng lúc lưu lượng vào bằng lưu lượng ra.

### ⏱ Mực nước trong bể trụ

**`c4`** — Với bể hình trụ diện tích đáy S, thể tích nước bằng S nhân chiều cao mực nước. Vì vậy mực nước dâng thêm một lượng bằng lượng nước chảy vào chia cho S, và tốc độ dâng bằng lưu lượng chia S.

**`c5`** — Cẩn thận với đơn vị: một mét khối bằng một nghìn lít, một phút bằng sáu mươi giây. Lưu lượng cho theo lít mỗi phút thì thời gian phải tính bằng phút. Rất nhiều lỗi sai trong bài thực tế đến từ đơn vị chứ không phải từ tích phân.

## Ví dụ

### ⏱ Ví dụ 1: thời gian đầy bể

**`e1`** — Ví dụ một, giải bài mở đầu. Lượng nước sau T phút bằng tích phân từ không đến T của hai mươi cộng bốn t, bằng hai mươi T cộng hai T bình phương. Cho bằng một nghìn, giải phương trình bậc hai, lấy nghiệm dương: T bằng trừ năm cộng năm căn hai mốt, khoảng mười bảy phẩy chín một phút.

### ⏱ Ví dụ 2: vừa vào vừa ra

**`e2`** — Ví dụ hai: bể đang có hai trăm lít. Nước chảy vào ba mươi lít mỗi phút, chảy ra hai t lít mỗi phút. Thể tích V của t bằng hai trăm cộng ba mươi t trừ t bình phương. Lớn nhất khi ba mươi bằng hai t, tức t bằng mười lăm, lúc đó bể có bốn trăm hai mươi lăm lít.

**`e3`** — Sau thời điểm đó, nước ra nhiều hơn vào. Bể cạn khi hai trăm cộng ba mươi t trừ t bình phương bằng không, tức t bằng mười lăm cộng căn bốn trăm hai mươi lăm, khoảng ba mươi lăm phẩy sáu hai phút.

### ⏱ Ví dụ 3: mực nước dâng

**`e4`** — Ví dụ ba: bể trụ có diện tích đáy hai mét vuông. Nước chảy vào với lưu lượng không phẩy một t mét khối mỗi phút. Sau mười phút, lượng nước vào là tích phân từ không đến mười của không phẩy một t, bằng năm mét khối. Mực nước dâng năm chia hai, bằng hai phẩy năm mét.

### ⏱ Ví dụ 4: đọc đồ thị lưu lượng

**`e5`** — Ví dụ bốn, đọc đồ thị: máy bơm khởi động trong hai phút, lưu lượng tăng đều từ không lên sáu mươi lít mỗi phút, bơm đều mười phút, rồi tắt dần trong hai phút. Lượng nước bơm được là diện tích hình thang: sáu mươi cộng sáu trăm cộng sáu mươi, bằng bảy trăm hai mươi lít.

### ⏱ Ví dụ 5: bể rò rỉ

**`e6`** — Ví dụ năm: một bể bị rò rỉ với lưu lượng tám nhân e mũ trừ t chia mười lít mỗi phút, giảm dần theo thời gian. Mười phút đầu rò mất tám mươi nhân một trừ một phần e, khoảng năm mươi phẩy năm bảy lít. Dù rò mãi mãi, tổng lượng nước mất cũng không vượt quá tám mươi lít, vì e mũ trừ t chia mười tiến về không.

### ⏱ Ví dụ 6: tìm tham số

**`e7`** — Ví dụ sáu, bài toán ngược: bể chín trăm lít đầy sau đúng mười phút với lưu lượng a cộng sáu t. Tìm a. Lượng nước sau mười phút là mười a cộng ba trăm. Cho bằng chín trăm, được a bằng sáu mươi lít mỗi phút.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Một bể chứa được năm trăm lít, đang có một trăm lít. Nước chảy vào với lưu lượng ba t bình phương lít mỗi phút. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: V bằng một trăm cộng tích phân của ba u bình phương từ không đến t, bằng một trăm cộng t lập phương. Ý b đúng: sau bốn phút, bể có một trăm sáu mươi tư lít.

**`x3`** — Ý c sai: bể đầy khi t lập phương bằng bốn trăm, t khoảng bảy phẩy ba bảy phút, không phải tám. Ý d đúng: lượng nước vào trong phút thứ ba, từ hai đến ba, bằng hai mươi bảy trừ tám, bằng mười chín lít.

### ⏱ Câu trả lời ngắn

**`x4`** — Câu trả lời ngắn: một bồn rỗng chứa được hai nghìn lít, nước chảy vào với lưu lượng năm mươi cộng hai t lít mỗi phút. Sau bao nhiêu phút thì đầy bồn? Làm tròn đến hàng phần mười.

**`x5`** — Lượng nước sau T phút bằng năm mươi T cộng T bình phương. Cho bằng hai nghìn: T bình phương cộng năm mươi T trừ hai nghìn bằng không, nghiệm dương T bằng trừ hai lăm cộng căn hai nghìn sáu trăm hai lăm, khoảng hai mươi sáu phẩy hai phút. Ghi vào phiếu: hai, sáu, phẩy, hai.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, lượng nước bằng tích phân của lưu lượng, là diện tích dưới đồ thị lưu lượng. Hai, vào và ra: lấy hiệu, lượng nước lớn nhất khi hai lưu lượng bằng nhau. Ba, bể trụ: mực nước dâng bằng lượng nước chia diện tích đáy, và luôn kiểm tra đơn vị.

**`o2`** — Bài tập tự luyện. Một, lưu lượng mười cộng hai t lít mỗi phút, tính lượng nước sau mười phút. Hai, bể rỗng, vào hai mươi lít mỗi phút, ra t lít mỗi phút: lượng nước lớn nhất. Ba, bể trụ đáy bốn mét vuông, lưu lượng không phẩy hai t mét khối mỗi phút: mực nước dâng sau mười phút. Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập ba mươi hai, cùng ý tưởng này áp dụng cho kinh tế và sinh học: chi phí biên, lợi nhuận, tốc độ tăng trưởng. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. r = 10 + 2t (L/phút): lượng nước sau 10 phút → **200 L**
2. Vào 20 L/phút, ra t L/phút, bể rỗng: lượng nước lớn nhất → **200 L**
3. Bể trụ đáy 4 m², r = 0,2t m³/phút: mực nước dâng sau 10 phút → **2,5 m**
