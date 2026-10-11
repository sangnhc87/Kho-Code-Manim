# INT25 – Thể tích theo thiết diện: Cắt lát, xếp chồng, cộng dồn: V = ∫S(x)dx

> Sinh tự động từ `int25/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int25`.

**Số nhịp:** 24 · **Số công thức Typst:** 36 · **Từ:** 1239

## Mở đầu

### ⏱ Mở đầu: cắt bánh mì thành lát

**`h1`** — Một ổ bánh mì được cắt thành rất nhiều lát mỏng. Thể tích ổ bánh bằng tổng thể tích các lát, và mỗi lát gần như một tấm phẳng: diện tích mặt cắt nhân độ dày. Ý tưởng đơn giản này cho ta công thức tính thể tích của mọi vật thể, chỉ cần biết diện tích mặt cắt.

**`h2`** — Đây là tập hai mươi lăm của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: thể tích vật thể theo thiết diện.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, công thức V bằng tích phân của S của x, hiểu bằng cắt lát và cộng dồn. Hai, cách tìm diện tích thiết diện cho các hình quen thuộc. Ba, dùng công thức này để chứng minh thể tích hình chóp bằng một phần ba diện tích đáy nhân chiều cao.

## Bản chất

### ⏱ Công thức V = ∫S(x)dx

**`c1`** — Đặt vật thể dọc theo trục O x, từ x bằng a đến x bằng b. Cắt vật thể bởi mặt phẳng vuông góc với trục tại điểm x, ta được một thiết diện có diện tích S của x. Khi S liên tục, thể tích V bằng tích phân từ a đến b của S của x.

**`c2`** — Vì sao? Chia vật thể thành n lát mỏng, mỗi lát có độ dày delta x. Thể tích mỗi lát xấp xỉ S của x nhân delta x. Cộng dồn n lát, ta được một tổng Riemann. Khi các lát mỏng dần, tổng tiến tới tích phân, giống hệt cách ta định nghĩa diện tích ở tập mười một.

**`c2b`** — Kiểm tra bằng đơn vị: S của x có đơn vị diện tích, mét vuông, nhân với d x có đơn vị độ dài, ta được mét khối. Vì vậy thứ nằm dưới dấu tích phân phải là một diện tích. Nếu em lấy tích phân của độ dài cạnh, kết quả chỉ là một diện tích, không phải thể tích. Đây là bẫy rất hay gặp.

### ⏱ Quy trình ba bước

**`c3`** — Quy trình ba bước. Một, chọn trục và xác định vật thể nằm từ a đến b. Hai, tại vị trí x, mô tả thiết diện và tính diện tích S của x. Ba, tính tích phân từ a đến b của S của x. Bước hai là bước quan trọng nhất.

### ⏱ Diện tích thiết diện hay gặp

**`c4`** — Nhắc lại diện tích các thiết diện hay gặp. Hình vuông cạnh a có diện tích a bình phương. Tam giác đều cạnh a có diện tích a bình phương nhân căn ba chia bốn. Nửa hình tròn bán kính r có diện tích pi r bình phương chia hai. Hình chữ nhật thì nhân hai cạnh.

**`c5`** — Nguyên lý Cavalieri: hai vật thể có thiết diện bằng nhau tại mọi vị trí x thì có thể tích bằng nhau. Một chồng đồng xu xếp thẳng và một chồng bị xô lệch có cùng thể tích. Đây chính là nội dung của công thức tích phân thể tích.

## Ví dụ

### ⏱ Ví dụ 1: thiết diện hình vuông

**`e1`** — Ví dụ một: vật thể nằm giữa x bằng không và x bằng bốn, thiết diện tại x là hình vuông cạnh căn x. Diện tích S của x bằng căn x bình phương, bằng x. Thể tích bằng tích phân từ không đến bốn của x, bằng tám.

### ⏱ Ví dụ 2: thiết diện tam giác đều

**`e2`** — Ví dụ hai: thiết diện tại x là tam giác đều cạnh x, với x từ không đến ba. Diện tích S của x bằng căn ba chia bốn nhân x bình phương. Thể tích bằng căn ba chia bốn nhân tích phân của x bình phương, bằng chín căn ba chia bốn.

### ⏱ Ví dụ: đáy là miền phẳng

**`e2b`** — Dạng đề hay gặp: vật thể có đáy là miền phẳng. Đáy là miền giới hạn bởi y bằng căn x, trục hoành, x từ không đến bốn. Thiết diện vuông góc với O x là nửa hình tròn có đường kính là đoạn từ trục đến đồ thị, dài căn x. Bán kính căn x chia hai, diện tích pi x chia tám. Thể tích bằng pi chia tám nhân tám, bằng pi.

### ⏱ Ví dụ 3: chứng minh thể tích hình chóp

**`e3`** — Ví dụ ba, chứng minh công thức hình chóp. Chóp có đáy hình vuông cạnh a, chiều cao h. Đặt trục O x từ đỉnh xuống đáy. Thiết diện cách đỉnh x là hình vuông cạnh a x chia h, theo tam giác đồng dạng.

**`e4`** — Diện tích thiết diện bằng a bình phương x bình phương chia h bình phương. Tích phân từ không đến h cho a bình phương nhân h chia ba. Đó chính là một phần ba diện tích đáy nhân chiều cao, công thức em đã học từ lớp chín, giờ được chứng minh bằng tích phân.

### ⏱ Ví dụ 4: kết hợp đổi biến

**`e5`** — Ví dụ bốn: thiết diện tại x là hình chữ nhật có hai cạnh x và căn của chín trừ x bình phương, với x từ không đến ba. Thể tích bằng tích phân của x nhân căn chín trừ x bình phương. Đổi biến u bằng chín trừ x bình phương, ta được thể tích bằng chín.

### ⏱ Hướng tới khối tròn xoay

**`e6`** — Một trường hợp đặc biệt rất quan trọng: nếu thiết diện tại x là hình tròn bán kính f của x, thì S của x bằng pi nhân f bình phương, và thể tích bằng pi nhân tích phân của f bình phương. Đó chính là thể tích khối tròn xoay mà ta sẽ học kỹ ở tập sau.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Một vật thể nằm giữa hai mặt phẳng x bằng một và x bằng ba. Thiết diện tại x là hình vuông cạnh hai x. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: diện tích hình vuông cạnh hai x là bốn x bình phương. Ý b sai: phải lấy tích phân của diện tích S, không phải của cạnh hai x.

**`x3`** — Ý c đúng: tích phân từ một đến ba của bốn x bình phương bằng bốn phần ba nhân hai mươi sáu, bằng một trăm lẻ bốn phần ba. Ý d đúng: giá trị đó xấp xỉ ba mươi tư phẩy bảy.

### ⏱ Câu trả lời ngắn

**`x4`** — Câu trả lời ngắn: một vật thể nằm giữa x bằng không và x bằng pi, thiết diện tại x là tam giác đều cạnh hai căn sin x. Tính thể tích, làm tròn đến hàng phần trăm.

**`x5`** — Diện tích tam giác đều cạnh hai căn sin x bằng căn ba chia bốn nhân bốn sin x, bằng căn ba sin x. Thể tích bằng căn ba nhân tích phân từ không đến pi của sin x, bằng hai căn ba, xấp xỉ ba phẩy bốn sáu. Ghi vào phiếu: ba, phẩy, bốn, sáu.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, thể tích bằng tích phân của diện tích thiết diện: cắt lát rồi cộng dồn. Hai, bước quan trọng nhất là viết đúng S của x. Ba, công thức này chứng minh được thể tích hình chóp, và là nền tảng cho khối tròn xoay ở tập sau.

**`o2`** — Bài tập tự luyện. Một, thiết diện là hình vuông cạnh x, với x từ không đến hai. Hai, thiết diện là tam giác đều cạnh x, với x từ không đến hai. Ba, thiết diện là nửa hình tròn bán kính x, với x từ không đến ba. Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập hai mươi sáu, thiết diện trở thành hình tròn khi ta quay một miền phẳng quanh trục O x: đó là khối tròn xoay và phương pháp đĩa. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. Thiết diện hình vuông cạnh x, x ∈ [0; 2] → **8/3**
2. Thiết diện tam giác đều cạnh x, x ∈ [0; 2] → **2√3/3**
3. Thiết diện nửa hình tròn bán kính x, x ∈ [0; 3] → **9π/2**
