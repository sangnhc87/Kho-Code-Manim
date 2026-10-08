# COMB21 V2 — HÀM SINH (GENERATING FUNCTIONS)

**Series Đại số tổ hợp SANG MATH · Phần chuyên sâu 21–25**

Manim trực quan + Typst công thức; 48 nhịp trong 8 chương; thời lượng nền ~21 phút 41 giây.

Mỗi nhịp có dữ liệu công thức, ba gạch đầu dòng và một đoạn lời đọc tiếng Việt hoàn chỉnh.

> Chỉ là mã và storyboard; chưa nghiệm thu MP4.

## 01 · HÀM SINH LÀ GÌ?

### Nhịp 01 · Một dãy số có thể biến thành gì?

**Hoạt hình:** Dãy 1, 3, 6, 10, 15, 21; Mỗi số ứng với một bậc của x; Không tính giá trị x ngay.

**Thuyết minh:** Ta đã học cách đếm để tìm ra từng số. Hôm nay, ta thử một góc nhìn ngược lại: gom toàn bộ dãy số vào một biểu thức duy nhất. Mỗi vị trí của dãy được gắn với một lũy thừa của x. Mục tiêu chưa phải tính giá trị của x, mà là giữ nguyên thông tin đếm ở các hệ số.

**Công thức Typst:** `intro_0`

**Bài học:** Đọc hệ số để đếm.

### Nhịp 02 · Gắn số đếm vào hệ số

**Hoạt hình:** Hệ số của x⁰ là 1; Hệ số của x¹ là 3; Hệ số của x² là 6.

**Thuyết minh:** Hãy quan sát từng tấm thẻ số dịch vào vị trí có cùng bậc x. Số một nằm cạnh x mũ không, số ba nằm cạnh x, số sáu đứng trước x bình phương. Ta không làm mất bất kỳ số nào. Nhờ cách mã hóa này, những quy tắc cộng và nhân đại số có thể trở thành công cụ để giải bài toán đếm.

**Công thức Typst:** `intro_1`

**Bài học:** Đọc hệ số để đếm.

### Nhịp 03 · Đọc lại một hệ số

**Hoạt hình:** Chọn bậc n cần tìm; Bỏ qua mọi bậc còn lại; Ở bậc 3, ta đọc được 10.

**Thuyết minh:** Bây giờ, thay vì hỏi giá trị toàn đa thức, ta chỉ hỏi hệ số ở một bậc xác định. Trong dãy đang xét, hệ số x mũ ba bằng mười. Đây chính là thao tác nền tảng của phương pháp hàm sinh: mô hình hóa các lựa chọn thành một hàm, rồi trích ra hệ số tương ứng với điều kiện của đề bài.

**Công thức Typst:** `intro_2`

**Bài học:** Đọc hệ số để đếm.

### Nhịp 04 · Cấp số nhân vô hạn

**Hoạt hình:** Một đối tượng có thể lấy 0 lần; Có thể lấy 1, 2, 3, ... lần; Các trạng thái tương ứng 1, x, x²,....

**Thuyết minh:** Bước đầu tiên cần nhớ là tổng hình thức một cộng x cộng x bình phương và cứ tiếp tục như vậy. Nó được biểu diễn gọn bằng một chia một trừ x. Với bài toán đếm, mỗi số mũ ghi lại số lượng phần tử được sử dụng. Ta xem đây là một đẳng thức chuỗi lũy thừa hình thức; không cần thay x bằng một số cụ thể.

**Công thức Typst:** `intro_3`

**Bài học:** Đọc hệ số để đếm.

### Nhịp 05 · Ba nguồn lựa chọn giống nhau

**Hoạt hình:** Nhân ba chuỗi 1/(1−x); Hệ số đếm cách chia tổng n; Dãy bắt đầu 1, 3, 6, 10,....

**Thuyết minh:** Nếu có ba loại vật, mỗi loại được lấy bao nhiêu tùy ý, ta có ba nhân tử giống nhau. Khi nhân chúng, hệ số của x mũ n đếm số cách chọn tổng cộng n vật. Đây là chiếc cầu nối đầu tiên từ biểu thức đại số đến một bài toán chia số nguyên. Lát nữa ta sẽ chứng minh cách đếm ấy bằng sao và vạch.

**Công thức Typst:** `intro_4`

**Bài học:** Đọc hệ số để đếm.

### Nhịp 06 · Công thức hệ số quen mà lạ

**Hoạt hình:** Hệ số 1, 3, 6, 10,...; Đó là các số tổ hợp; Một công thức chứa cả dãy.

**Thuyết minh:** Dãy số quen thuộc hóa ra được mô tả bằng công thức tổ hợp. Hệ số của x mũ n trong một chia một trừ x tất cả mũ ba chính là số tổ hợp chập hai của n cộng hai. Ta vừa thấy hai ngôn ngữ khác nhau đang kể cùng một câu chuyện: một bên là chuỗi lũy thừa, bên còn lại là quy tắc chọn vị trí.

**Công thức Typst:** `intro_5`

**Bài học:** Đọc hệ số để đếm.

## 02 · PHÉP NHÂN VÀ TÍCH CHẬP

### Nhịp 07 · Hai phép chọn độc lập

**Hoạt hình:** A: 0, 1, 2 đơn vị; B: 0 hoặc 2 đơn vị; Tổng tạo thành bậc của tích.

**Thuyết minh:** Giả sử nguồn A có thể đóng góp không, một hoặc hai đơn vị. Nguồn B chỉ có hai khả năng là không hoặc hai đơn vị. Ta gắn mỗi khả năng với một đơn thức tương ứng. Sự lựa chọn độc lập ở hai nguồn có nghĩa là phải nhân hai hàm sinh, chứ không cộng chúng. Điều này chính là quy tắc nhân ở dạng mới.

**Công thức Typst:** `product_0`

**Bài học:** Nhân nguồn lựa chọn.

### Nhịp 08 · Hàm sinh của nguồn B

**Hoạt hình:** B không dùng: hệ số 1; B dùng: thêm đúng 2 đơn vị; Không có phương án thêm 1 đơn vị.

**Thuyết minh:** Hãy chú ý lỗ hổng ở bậc một trong hàm B. Đây không phải thiếu sót, mà thể hiện một điều kiện thật của bài toán: B không bao giờ đóng góp một đơn vị. Những hệ số bằng không có ý nghĩa rất lớn. Nhờ chúng, hàm sinh tự động loại những tổ hợp không hợp lệ mà ta không cần gạch từng trường hợp.

**Công thức Typst:** `product_1`

**Bài học:** Nhân nguồn lựa chọn.

### Nhịp 09 · Nhân và gom cùng bậc

**Hoạt hình:** Các cặp lựa chọn được nối; Bậc là tổng hai số mũ; Hệ số x² xuất hiện hai lần.

**Thuyết minh:** Khi nhân hai đa thức, mỗi hạng tử của A ghép với mỗi hạng tử của B. Số mũ mới bằng tổng số mũ của hai hạng tử đã chọn. Các tích có cùng số mũ được gom lại, và hệ số của chúng cộng lên. Trên màn hình, hai con đường khác nhau đều đưa đến tổng bằng hai, vì thế hệ số ở bậc hai là hai.

**Công thức Typst:** `product_2`

**Bài học:** Nhân nguồn lựa chọn.

### Nhịp 10 · Đếm trực tiếp hệ số x²

**Hoạt hình:** A=0 và B=2: một cách; A=2 và B=0: một cách; Không có A=1, B=1.

**Thuyết minh:** Ta hãy kiểm tra kết quả bằng liệt kê. Muốn tổng bằng hai, ta có thể lấy không đơn vị từ A và hai từ B, hoặc hai từ A và không từ B. Phương án một cộng một bị loại vì B không được lấy một đơn vị. Như vậy có đúng hai khả năng, trùng khớp hoàn toàn với hệ số mà phép nhân vừa tạo.

**Công thức Typst:** `product_3`

**Bài học:** Nhân nguồn lựa chọn.

### Nhịp 11 · Công thức tích chập Cauchy

**Hoạt hình:** Chọn k đơn vị từ A; Chọn n−k đơn vị từ B; Cộng theo mọi k hợp lệ.

**Thuyết minh:** Ví dụ nhỏ vừa rồi tổng quát thành công thức tích chập Cauchy. Hệ số bậc n của tích hai hàm sinh bằng tổng các tích hệ số bậc k của hàm thứ nhất và bậc n trừ k của hàm thứ hai. Đây là công thức then chốt để đếm khi một tổng phải được chia thành nhiều phần khác nhau.

**Công thức Typst:** `product_4`

**Bài học:** Nhân nguồn lựa chọn.

### Nhịp 12 · Tự kiểm tra quy tắc

**Hoạt hình:** Chọn bậc đích trước; Tìm các cặp chỉ số có tổng đúng; Đếm theo hệ số, không chỉ theo số mũ.

**Thuyết minh:** Điều quan trọng là không nhầm số hạng với số cách. Nếu một hạng tử có hệ số ba thì riêng nó đã biểu diễn ba cách khác nhau, không phải một cách. Từ tập này trở đi, mỗi lần nhân hàm sinh, hãy tự hỏi hai nguồn lựa chọn là gì và tại sao mọi cách hợp lệ được ghép đúng một lần. Đó là cách tránh học công thức một cách máy móc.

**Công thức Typst:** `product_5`

**Bài học:** Nhân nguồn lựa chọn.

## 03 · NGHIỆM NGUYÊN VÀ SAO–VẠCH

### Nhịp 13 · Bài toán chia 6 vật giống nhau

**Hoạt hình:** Ba hộp phân biệt; Mỗi hộp nhận số vật không âm; Tổng số vật bằng 6.

**Thuyết minh:** Ta có sáu viên bi giống nhau và ba hộp khác nhau. Mỗi hộp được phép rỗng. Gọi số bi trong ba hộp lần lượt là x một, x hai, x ba; tổng của chúng bằng sáu. Việc các viên bi giống nhau có nghĩa là ta chỉ quan tâm số lượng trong từng hộp, không quan tâm từng viên bi được đặt theo thứ tự nào.

**Công thức Typst:** `stars_0`

**Bài học:** Sao–vạch và hệ số.

### Nhịp 14 · Sao và hai vạch ngăn

**Hoạt hình:** Sáu ngôi sao biểu diễn bi; Hai vạch tách thành ba nhóm; Chọn vị trí vạch trong 8 ô.

**Thuyết minh:** Hãy đặt sáu dấu sao và hai dấu vạch thành một hàng. Những dấu sao trước vạch thứ nhất vào hộp một, ở giữa vào hộp hai, và sau vạch thứ hai vào hộp ba. Mỗi cách đặt hai vạch biểu diễn đúng một nghiệm nguyên không âm, kể cả khi hai vạch nằm sát nhau. Vì có tám vị trí tất cả, số nghiệm là tổ hợp chập hai của tám.

**Công thức Typst:** `stars_1`

**Bài học:** Sao–vạch và hệ số.

### Nhịp 15 · Đặt hàm sinh mỗi hộp

**Hoạt hình:** Hộp được nhận 0,1,2,... viên; Hệ số mỗi trạng thái bằng 1; Ba hộp cho ba nhân tử.

**Thuyết minh:** Ta xem mỗi hộp là một nguồn tạo số viên bi. Với một hộp, các lựa chọn không, một, hai và cứ thế tạo ra chuỗi một cộng x cộng x bình phương. Có ba hộp độc lập nên hàm sinh chung là lũy thừa bậc ba của một chia một trừ x. Hệ số x mũ sáu trong biểu thức này sẽ đếm đúng các phân phối mà ta vừa xem bằng dấu sao và vạch.

**Công thức Typst:** `stars_2`

**Bài học:** Sao–vạch và hệ số.

### Nhịp 16 · Đọc hệ số bậc sáu

**Hoạt hình:** Từ hàm sinh đã lập; Lấy hệ số của x⁶; So sánh với sao–vạch.

**Thuyết minh:** Khai triển một chia một trừ x tất cả mũ ba cho thấy hệ số bậc n là tổ hợp chập hai của n cộng hai. Khi n bằng sáu, ta được hai mươi tám. Hai cách giải có cơ sở hoàn toàn khác nhau nhưng chung một đáp số, giúp ta tin rằng mô hình hàm sinh đã phản ánh đúng từng cách phân phối.

**Công thức Typst:** `stars_3`

**Bài học:** Sao–vạch và hệ số.

### Nhịp 17 · Khái quát k hộp và n vật

**Hoạt hình:** k hộp có nhãn phân biệt; n vật giống nhau, được phép rỗng; Cần k−1 vạch trong n+k−1 vị trí.

**Thuyết minh:** Nếu có k hộp và n vật giống nhau, ta cần k trừ một vạch để chia n dấu sao. Tổng số dấu là n cộng k trừ một. Chọn vị trí các vạch cho ra công thức tổng quát. Ở ngôn ngữ hàm sinh, công thức này cũng là hệ số bậc n của một chia một trừ x mũ k.

**Công thức Typst:** `stars_4`

**Bài học:** Sao–vạch và hệ số.

### Nhịp 18 · Khi mỗi hộp ít nhất một vật

**Hoạt hình:** Dành trước 1 vật mỗi hộp; Phân phối số còn lại; Hàm sinh bắt đầu từ x thay vì 1.

**Thuyết minh:** Khi bắt buộc mỗi hộp có ít nhất một viên bi, ta không thể dùng trực tiếp hàm sinh của hộp cho phép rỗng. Mỗi hộp giờ có chuỗi x cộng x bình phương và cứ tiếp tục, tức x chia một trừ x. Nhân ba hộp tạo x mũ ba ở tử. Sự dịch bậc này biểu diễn chính xác ba viên đã dành trước.

**Công thức Typst:** `stars_5`

**Bài học:** Sao–vạch và hệ số.

## 04 · RÀNG BUỘC VÀ HÀM SINH HỮU TỈ

### Nhịp 19 · Điều kiện chặn tạo khác biệt

**Hoạt hình:** Năm biến nguyên không âm; Hai biến đầu không quá 2; Tổng bằng 12.

**Thuyết minh:** Bài toán mới khó hơn vì hai hộp đầu chỉ chứa tối đa hai vật. Nếu vẫn dùng một chia một trừ x cho cả năm hộp, ta sẽ đếm cả trường hợp vượt quá giới hạn. Vì thế ta cần xây dựng một hàm sinh riêng cho mỗi hộp bị chặn. Đề bài trở thành một mô hình đại số rất tự nhiên.

**Công thức Typst:** `bounds_0`

**Bài học:** Ràng buộc bằng tử số.

### Nhịp 20 · Hàm sinh của hộp bị chặn

**Hoạt hình:** Lấy 0, 1 hoặc 2 vật; Không có hạng tử x³ trở lên; Một đa thức hữu hạn.

**Thuyết minh:** Các lựa chọn của một hộp bị chặn là không, một hoặc hai viên. Vì chỉ có ba khả năng, hàm sinh của nó là đa thức một cộng x cộng x bình phương. Ta có thể viết đa thức ấy thành một trừ x mũ ba chia một trừ x. Cách viết phân thức sẽ rất tiện khi nhân với các hộp không bị chặn.

**Công thức Typst:** `bounds_1`

**Bài học:** Ràng buộc bằng tử số.

### Nhịp 21 · Ghép năm hộp đúng điều kiện

**Hoạt hình:** Hai hộp bị chặn: (1+x+x²)²; Ba hộp còn lại: 1/(1−x)³; Nhân để lấy tổng số vật.

**Thuyết minh:** Hai hộp đầu đóng góp hai nhân tử có giới hạn, còn ba hộp sau mỗi hộp có thể nhận bất kỳ số vật không âm nào. Nhân năm hàm sinh, ta được một phân thức có tử là một trừ x mũ ba bình phương và mẫu là một trừ x mũ năm. Như vậy mọi nghiệm hợp lệ đã được mã hóa bằng một biểu thức.

**Công thức Typst:** `bounds_2`

**Bài học:** Ràng buộc bằng tử số.

### Nhịp 22 · Tử số chính là phần bù

**Hoạt hình:** Khai triển (1−x³)²; Xuất hiện 1, −2x³, +x⁶; Bao hàm–loại trừ ẩn trong phép nhân.

**Thuyết minh:** Hãy nhìn kỹ ba hạng tử của tử số. Hạng một đếm mọi trường hợp không chặn. Hạng trừ hai x mũ ba loại những cách có ít nhất một trong hai hộp vượt giới hạn. Hạng cộng x mũ sáu hoàn lại phần giao đã bị trừ hai lần. Nguyên lý bao hàm loại trừ đang xuất hiện ngay bên trong một phép khai triển đại số.

**Công thức Typst:** `bounds_3`

**Bài học:** Ràng buộc bằng tử số.

### Nhịp 23 · Trích hệ số bậc 12

**Hoạt hình:** Không chặn: tổ hợp chập 4 của 16; Trừ hai lần tổ hợp chập 4 của 13; Cộng tổ hợp chập 4 của 10.

**Thuyết minh:** Để tính hệ số của x mũ mười hai, ta lấy hệ số từ mẫu tương ứng với ba bậc mười hai, chín và sáu. Kết quả là tổ hợp chập bốn của mười sáu, trừ hai lần tổ hợp chập bốn của mười ba, rồi cộng tổ hợp chập bốn của mười. Mỗi số hạng có ý nghĩa rõ ràng chứ không phải phép biến đổi tùy ý.

**Công thức Typst:** `bounds_4`

**Bài học:** Ràng buộc bằng tử số.

### Nhịp 24 · Kết quả và kiểm chứng

**Hoạt hình:** 1820 cách trước khi loại; 1430 cách bị trừ kể bội; 210 cách hoàn lại phần giao.

**Thuyết minh:** Sau khi thực hiện phép tính, ta được sáu trăm cách phân phối. Có thể kiểm tra bằng thuật toán duyệt riêng từng giá trị của hai biến bị chặn và đếm phần còn lại theo sao và vạch. Kết quả trùng khớp chứng tỏ phép đổi từ bất phương trình về tử số một trừ x mũ ba đã xử lý chính xác điều kiện.

**Công thức Typst:** `bounds_5`

**Bài học:** Ràng buộc bằng tử số.

## 05 · FIBONACCI VÀ TRUY HỒI

### Nhịp 25 · Lát gạch một đoạn dài n

**Hoạt hình:** Gạch 1 ô hoặc 2 ô; Các viên đặt theo hàng; f(n) đếm cách lát kín.

**Thuyết minh:** Ta chuyển sang một bài đếm có thứ tự. Một hành lang được chia thành các ô đơn vị. Ta có thể dùng viên gạch dài một ô hoặc viên gạch dài hai ô để lát kín. Ký hiệu f n là số cách lát một đoạn n ô. Đoạn rỗng có một cách lát: không đặt gì. Đoạn một ô cũng chỉ có một cách.

**Công thức Typst:** `recurrence_0`

**Bài học:** Truy hồi ↔ hàm hữu tỉ.

### Nhịp 26 · Tách theo viên gạch cuối

**Hoạt hình:** Cuối là viên 1 ô: còn n−1; Cuối là viên 2 ô: còn n−2; Hai loại tách biệt, không trùng.

**Thuyết minh:** Quan sát hai tình huống ở cuối hành lang. Nếu viên cuối dài một ô, phần trước dài n trừ một. Nếu viên cuối dài hai ô, phần trước dài n trừ hai. Hai trường hợp loại trừ nhau và bao quát mọi cách lát. Vì thế số cách là tổng của hai số trước đó. Đây là hệ thức truy hồi Fibonacci được chứng minh bằng phân loại trường hợp.

**Công thức Typst:** `recurrence_1`

**Bài học:** Truy hồi ↔ hàm hữu tỉ.

### Nhịp 27 · Đặt dãy vào hàm sinh

**Hoạt hình:** F(x) chứa f₀, f₁, f₂,...; Nhân x làm dịch chỉ số 1; Nhân x² làm dịch chỉ số 2.

**Thuyết minh:** Khi các hệ số thỏa truy hồi, ta có thể đưa toàn bộ dãy vào hàm sinh F. Nhân F với x sẽ dời tất cả số hạng sang phải một bậc; nhân với x bình phương sẽ dời sang phải hai bậc. Hai phép dịch chỉ số này chính là chìa khóa chuyển công thức truy hồi thành phương trình đại số.

**Công thức Typst:** `recurrence_2`

**Bài học:** Truy hồi ↔ hàm hữu tỉ.

### Nhịp 28 · Xóa các hệ số trừ hằng số

**Hoạt hình:** F − xF − x²F; Hệ số từ bậc 2 triệt tiêu; Còn lại hằng số 1.

**Thuyết minh:** Ta lấy F trừ x nhân F rồi trừ x bình phương nhân F. Từ bậc hai trở đi, mọi hệ số bằng không vì f n bằng tổng hai hệ số trước. Bậc không còn một, còn bậc một cũng triệt tiêu đúng nhờ điều kiện đầu. Ta nhận được một phương trình rất ngắn, thay thế cho cả một dãy vô hạn.

**Công thức Typst:** `recurrence_3`

**Bài học:** Truy hồi ↔ hàm hữu tỉ.

### Nhịp 29 · Giải phương trình hàm sinh

**Hoạt hình:** Chuyển vế như đại số; Một phân thức hữu tỉ; Hệ số cho đúng Fibonacci.

**Thuyết minh:** Từ phương trình vừa lập, hàm sinh của các cách lát bằng một chia một trừ x trừ x bình phương. Đây là một ví dụ tiêu biểu: dãy truy hồi có thể được biểu diễn bằng hàm hữu tỉ. Khi khai triển phân thức thành chuỗi, ta lần lượt thu lại một, một, hai, ba, năm, tám và các số tiếp theo.

**Công thức Typst:** `recurrence_4`

**Bài học:** Truy hồi ↔ hàm hữu tỉ.

### Nhịp 30 · Đếm độ dài 5 và 6

**Hoạt hình:** Dài 5 có 8 cách; Dài 6 có 13 cách; Truy hồi và liệt kê khớp nhau.

**Thuyết minh:** Với đoạn năm ô, hình động sẽ liệt kê tám cách lát. Ta không cần vẽ tất cả cách lát của đoạn rất dài; chỉ cần chứng minh quy luật tách theo viên cuối. Truy hồi cho đoạn sáu ô bằng tám cộng năm, tức mười ba. Tập này chuẩn bị nền tảng rất tốt cho quy hoạch động ở Video 22, nơi ta lưu các kết quả trung gian.

**Công thức Typst:** `recurrence_5`

**Bài học:** Truy hồi ↔ hàm hữu tỉ.

## 06 · HÀM SINH MŨ VÀ TOÀN ÁNH

### Nhịp 31 · Khi đối tượng có nhãn

**Hoạt hình:** 4 học sinh phân vào các nhóm; Học sinh phân biệt nhau; Cần hàm sinh mũ để quản lý nhãn.

**Thuyết minh:** Đến đây, những vật ta phân phối thường giống nhau. Nhưng khi đối tượng có nhãn, chẳng hạn bốn học sinh khác nhau, phép nhân các hàm sinh thường không đủ thuận tiện để quản lý việc chọn chính xác ai vào nhóm nào. Ta giới thiệu hàm sinh mũ: hệ số bậc n được chia cho n giai thừa. Yếu tố này sẽ tạo ra đúng hệ số tổ hợp khi ta nhân hai hàm.

**Công thức Typst:** `exponential_0`

**Bài học:** Nhãn ↔ hàm sinh mũ.

### Nhịp 32 · Hàm mũ chứa các giai thừa

**Hoạt hình:** e^x có hệ số 1/n!; Nhóm rỗng được phép; Đối tượng có nhãn phân biệt.

**Thuyết minh:** Hàm mũ e mũ x có khai triển với mẫu n giai thừa. Vì một tập có n phần tử phân biệt chỉ có một cách xem là một nhóm duy nhất, e mũ x là hàm sinh mũ tự nhiên của loại nhóm tùy ý. Mẫu số giai thừa không mất thông tin; khi lấy hệ số x mũ n, ta nhân lại n giai thừa.

**Công thức Typst:** `exponential_1`

**Bài học:** Nhãn ↔ hàm sinh mũ.

### Nhịp 33 · Loại trường hợp nhóm rỗng

**Hoạt hình:** Muốn nhóm không rỗng; Bỏ hệ số ở bậc không; Hàm sinh trở thành e^x−1.

**Thuyết minh:** Nếu một nhóm bắt buộc phải có ít nhất một học sinh, ta bỏ trạng thái không chọn học sinh nào. Trong hàm sinh mũ, trạng thái đó chính là hạng một ở bậc không. Vì vậy hàm sinh của một nhóm không rỗng là e mũ x trừ một. Ta vừa đổi một điều kiện ngôn ngữ thành thao tác trừ cực kỳ đơn giản.

**Công thức Typst:** `exponential_2`

**Bài học:** Nhãn ↔ hàm sinh mũ.

### Nhịp 34 · Ba nhóm có nhãn không rỗng

**Hoạt hình:** Ba hộp ghi A, B, C; Mỗi hộp phải có người; Nhân ba hàm sinh nhóm.

**Thuyết minh:** Bây giờ ta có ba nhóm đặt tên rõ ràng. Mỗi nhóm nhận ít nhất một học sinh, nên mỗi nhóm đóng góp e mũ x trừ một. Vì các nhóm độc lập theo nhãn, hàm sinh chung là lũy thừa bậc ba của biểu thức này. Hệ số bậc bốn sẽ cho ta số cách chia bốn học sinh khác nhau vào ba nhóm có nhãn mà không nhóm nào rỗng.

**Công thức Typst:** `exponential_3`

**Bài học:** Nhãn ↔ hàm sinh mũ.

### Nhịp 35 · Đếm toàn ánh 4 vào 3

**Hoạt hình:** Có 3⁴ phép gán tùy ý; Trừ trường hợp có nhóm rỗng; Bao hàm–loại trừ cho 36.

**Thuyết minh:** Ta kiểm tra bằng cách đếm thông thường. Mỗi học sinh có ba lựa chọn nên có ba mũ bốn phép phân công. Nếu một nhóm rỗng, ta chỉ còn hai lựa chọn cho từng người; có ba nhóm có thể rỗng. Cộng lại các trường hợp chỉ dùng đúng một nhóm, ta được ba mươi sáu. Đây cũng là kết quả lấy từ hệ số bậc bốn của hàm sinh mũ.

**Công thức Typst:** `exponential_4`

**Bài học:** Nhãn ↔ hàm sinh mũ.

### Nhịp 36 · Nhóm không nhãn và số Stirling

**Hoạt hình:** Đổi tên nhóm không tạo cách mới; Hai nhóm không rỗng từ 4 phần tử; Chia thêm cho 2 giai thừa.

**Thuyết minh:** Nếu hai nhóm không được đặt tên, việc hoán đổi tên nhóm không tạo phương án mới. Có hai mũ bốn phép phân hai màu, bỏ hai cách dồn hết vào một nhóm, rồi chia hai vì đổi màu cho hai nhóm cho cùng một phân hoạch. Ta được bảy, chính là số Stirling loại hai S của bốn và hai. Đây là cửa ngõ của tổ hợp rất sâu.

**Công thức Typst:** `exponential_5`

**Bài học:** Nhãn ↔ hàm sinh mũ.

## 07 · ĐỔI XU VÀ TÌM HỆ SỐ

### Nhịp 37 · Đổi xu 1, 2, 3 đơn vị

**Hoạt hình:** Mỗi loại xu được dùng tùy ý; Tổng giá trị cần đúng 12; Không xét thứ tự đưa xu.

**Thuyết minh:** Một bài toán cổ điển là đổi đúng mười hai đơn vị tiền bằng các đồng xu mệnh giá một, hai, ba. Mỗi loại có thể dùng nhiều lần, và thứ tự đưa xu không làm thành một cách mới. Gọi số đồng từng loại là x, y, z, ta được phương trình x cộng hai y cộng ba z bằng mười hai. Hàm sinh sẽ ghi nhận giá trị thay vì số đồng.

**Công thức Typst:** `coins_0`

**Bài học:** Trọng số đi vào số mũ.

### Nhịp 38 · Hàm sinh của mệnh giá d

**Hoạt hình:** Lấy 0 đồng: hệ số 1; Lấy r đồng: số mũ rd; Bước nhảy theo bội của d.

**Thuyết minh:** Với đồng mệnh giá d, nếu lấy r đồng thì tổng giá trị tăng r nhân d. Do đó các lựa chọn được mã hóa bởi một cộng x mũ d cộng x mũ hai d và cứ tiếp tục. Tổng cấp số nhân cho một chia một trừ x mũ d. Chỉ cần đổi d, ta đã thay đổi loại đồng xu mà không cần lập lại cả thuật toán đếm.

**Công thức Typst:** `coins_1`

**Bài học:** Trọng số đi vào số mũ.

### Nhịp 39 · Nhân ba nguồn mệnh giá

**Hoạt hình:** Đồng 1: 1/(1−x); Đồng 2: 1/(1−x²); Đồng 3: 1/(1−x³).

**Thuyết minh:** Ba loại xu là ba nguồn lựa chọn độc lập nên phải nhân ba hàm sinh. Hệ số x mũ mười hai của tích này là số cách đổi tiền đúng yêu cầu. Điều hay là điều kiện tổng giá trị đã được đưa thẳng vào số mũ: mọi bộ số đồng thỏa phương trình đều tạo đúng một tích ở bậc mười hai.

**Công thức Typst:** `coins_2`

**Bài học:** Trọng số đi vào số mũ.

### Nhịp 40 · Chia trường hợp theo đồng 3

**Hoạt hình:** z chạy từ 0 đến 4; Mỗi z còn phương trình x+2y=12−3z; Các số cách: 7,5,4,2,1.

**Thuyết minh:** Để kiểm tra, ta chọn trước số đồng mệnh giá ba, từ không tới bốn. Với mỗi lựa chọn, số đồng mệnh giá hai có thể chạy từ không đến phần nguyên của số tiền còn lại chia hai; đồng mệnh giá một được xác định tự động. Số cách lần lượt là bảy, năm, bốn, hai và một, tổng bằng mười chín.

**Công thức Typst:** `coins_3`

**Bài học:** Trọng số đi vào số mũ.

### Nhịp 41 · Hàm sinh thay cho liệt kê dài

**Hoạt hình:** Tích ba chuỗi gom đúng bậc; Các bậc không bằng 12 bị bỏ qua; Hệ số cần tìm là 19.

**Thuyết minh:** Bây giờ hãy hình dung khi tổng tiền tăng lên một trăm hoặc một nghìn. Liệt kê bằng tay trở nên bất tiện, nhưng quy tắc hàm sinh hoàn toàn không thay đổi. Ta vẫn lấy đúng một hệ số của tích ba chuỗi. Trong tính toán thực tế, ta có thể nhân và cắt chuỗi tới bậc cần thiết, đây cũng chính là tư tưởng của quy hoạch động đếm số cách đổi tiền.

**Công thức Typst:** `coins_4`

**Bài học:** Trọng số đi vào số mũ.

### Nhịp 42 · Phân biệt số cách và thứ tự

**Hoạt hình:** 1+2+3 và 3+2+1 là một; Nếu đếm dãy xu cần mô hình khác; Kiểm tra ý nghĩa từng nhân tử.

**Thuyết minh:** Đừng quên giả thiết quan trọng: các đồng xu cùng mệnh giá được xem là giống nhau, và thứ tự chọn các mệnh giá không được tính. Nếu bài toán hỏi các dãy đưa xu có thứ tự, đáp số sẽ khác. Trước khi dựng hàm sinh, luôn phải xác nhận đâu là một kết quả riêng biệt. Khi mô hình đúng, đại số mới đưa ra câu trả lời đúng.

**Công thức Typst:** `coins_5`

**Bài học:** Trọng số đi vào số mũ.

## 08 · BÀI TOÁN OLYMPIC TỔNG HỢP

### Nhịp 43 · Bài Olympic: 5 biến, 2 biến bị chặn

**Hoạt hình:** Tổng năm biến là 12; Hai biến đầu từ 0 tới 2; Ba biến còn lại tùy ý.

**Thuyết minh:** Ta kết thúc tập bằng một bài toán phối hợp nhiều kỹ thuật. Tìm số nghiệm nguyên không âm của tổng năm biến bằng mười hai, trong đó hai biến đầu không vượt quá hai. Không nên bắt đầu bằng công thức ngay. Trước tiên hãy nhận diện mỗi biến là một nguồn lựa chọn, giới hạn nào cần đưa vào hàm sinh, và bậc nào ta phải trích hệ số.

**Công thức Typst:** `capstone_0`

**Bài học:** Mô hình → hệ số → kết quả.

### Nhịp 44 · Ghép các nhân tử

**Hoạt hình:** Hai chuỗi hữu hạn 1+x+x²; Ba chuỗi 1/(1−x); Lấy hệ số x¹² của tích.

**Thuyết minh:** Hai biến bị chặn tạo ra hai nhân tử hữu hạn, ba biến không bị chặn tạo ra ba cấp số nhân. Nhân các phần lại, ta nhận được một phân thức đã từng xuất hiện ở chương bốn. Lần này, ta sẽ trình bày lời giải như một bài Olympiad ngắn gọn: biến điều kiện thành hàm sinh, biến hàm sinh thành tổ hợp và kết luận.

**Công thức Typst:** `capstone_1`

**Bài học:** Mô hình → hệ số → kết quả.

### Nhịp 45 · Tách ba hạng tử của tử

**Hoạt hình:** Một hạng dương; Một hạng âm có hệ số 2; Một hạng dương bậc 6.

**Thuyết minh:** Tử số được khai triển thành ba hạng. Hạng đầu đóng góp hệ số bậc mười hai của mẫu; hạng giữa đóng góp trừ hai lần hệ số bậc chín; hạng cuối cộng hệ số bậc sáu. Trong hình động, ba mũi tên màu khác nhau sẽ đưa các bậc này về cùng bậc mười hai, cho thấy phép nhân chuỗi tự động thực hiện bao hàm loại trừ.

**Công thức Typst:** `capstone_2`

**Bài học:** Mô hình → hệ số → kết quả.

### Nhịp 46 · Hệ số đầu tiên

**Hoạt hình:** Không xét giới hạn hai biến đầu; Đếm nghiệm không âm năm biến; Có tổ hợp chập bốn của 16.

**Thuyết minh:** Nếu tạm bỏ cả hai điều kiện chặn, ta đang phân phối mười hai vật giống nhau vào năm hộp. Công thức sao và vạch cho tổ hợp chập bốn của mười sáu, bằng một nghìn tám trăm hai mươi. Đây là số cách xuất phát. Những trường hợp không hợp lệ phải được trừ và phần giao phải được cộng lại.

**Công thức Typst:** `capstone_3`

**Bài học:** Mô hình → hệ số → kết quả.

### Nhịp 47 · Loại vượt giới hạn và hoàn lại

**Hoạt hình:** Trừ 2×715 cách; Cộng lại 210 cách bị trừ đôi; Cả hai biến bị chặn được xử lý.

**Thuyết minh:** Nếu biến thứ nhất lớn hơn hoặc bằng ba, ta trừ trước ba và còn tổng chín. Số nghiệm khi đó là tổ hợp chập bốn của mười ba. Biến thứ hai cho đúng một số lượng như vậy, nên phải trừ hai lần. Nhưng khi cả hai biến đều vượt giới hạn, ta đã trừ trùng, cần cộng lại tổ hợp chập bốn của mười.

**Công thức Typst:** `capstone_4`

**Bài học:** Mô hình → hệ số → kết quả.

### Nhịp 48 · Kết luận và liên hệ kỹ thuật

**Hoạt hình:** 1820 − 1430 + 210; Có đúng 600 nghiệm; Kiểm chứng bằng duyệt hai biến đầu.

**Thuyết minh:** Kết quả cuối cùng là sáu trăm nghiệm. Bài này kết hợp sao và vạch, hàm sinh hữu tỉ và bao hàm loại trừ trong cùng một lời giải. Chúng ta có thể kiểm chứng bằng cách cho hai biến đầu chạy từ không tới hai rồi đếm ba biến còn lại. Đây chính là sức mạnh của hàm sinh: một ngôn ngữ thống nhất cho nhiều kỹ thuật đếm tưởng chừng khác nhau.

**Công thức Typst:** `capstone_5`

**Bài học:** Mô hình → hệ số → kết quả.
