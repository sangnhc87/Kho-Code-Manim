# INT01 – STORYBOARD 8 CHƯƠNG, 32 PHÂN CẢNH

**Bài:** Đi ngược đạo hàm – Bản chất của nguyên hàm.

**Tổng thời lượng nền:** 864 giây = 14 phút 24 giây (khi bật TTS có thể tăng).

**Khung:** 16:9, 2 cột cố định, đồ thị trái / giảng giải và Typst phải.

**Lưu ý:** Các số phân cảnh trong tài liệu chỉ để sản xuất, tuyệt đối không hiển thị trong video.

## Chương 01 – Câu hỏi đi ngược đạo hàm

### Phân cảnh 01.01 – Nhìn từ điều đã biết
- **Thông điệp:** Đạo hàm cho biết mức thay đổi của hàm số.
- **Mô hình động:** `question`.
- **Công thức Typst:** `definition` → `$F'(x) = f(x)$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Khi biết hàm số F, ta có thể tìm đạo hàm của nó. Nhưng bài học hôm nay đặt ra câu hỏi theo hướng ngược lại. Nếu chỉ biết tốc độ thay đổi, liệu ta có thể khôi phục hàm số ban đầu không?

### Phân cảnh 01.02 – Một câu hỏi rất cụ thể
- **Thông điệp:** Biết đạo hàm bằng 2x. Hãy tìm một hàm số.
- **Mô hình động:** `question`.
- **Công thức Typst:** `f` → `$f(x) = 2x$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Giả sử một hàm số có đạo hàm tại mọi điểm bằng hai lần hoành độ x. Thử bắt đầu bằng những hàm số quen thuộc, rồi lấy đạo hàm để kiểm tra. Chúng ta chưa cần đến một công thức mới.

### Phân cảnh 01.03 – Quan sát đường thẳng
- **Thông điệp:** Đồ thị y = 2x biểu diễn giá trị đạo hàm.
- **Mô hình động:** `question`.
- **Công thức Typst:** `f` → `$f(x) = 2x$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Đường thẳng đang xuất hiện biểu diễn giá trị hai x. Với x dương thì đạo hàm dương; khi x âm thì đạo hàm âm; tại x bằng không thì đạo hàm bằng không. Đồ thị này là đồ thị của đạo hàm, chưa phải hàm cần tìm.

### Phân cảnh 01.04 – Mục tiêu của bài
- **Thông điệp:** Tìm F sao cho F'(x) = f(x).
- **Mô hình động:** `question`.
- **Công thức Typst:** `definition` → `$F'(x) = f(x)$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Ta sẽ tìm một hàm F có đạo hàm bằng f, tìm hiểu vì sao không chỉ có một đáp án, và cách sử dụng một điều kiện ban đầu để chọn đúng một hàm. Hãy nhìn cả đồ thị lẫn công thức.

## Chương 02 – Tìm lại hàm số đã biết đạo hàm

### Phân cảnh 02.01 – Thử một ứng viên
- **Thông điệp:** Đạo hàm của x² là 2x.
- **Mô hình động:** `reverse`.
- **Công thức Typst:** `square` → `$F(x) = x^2$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Ta biết đạo hàm của x bình phương bằng hai x. Vậy F của x bằng x bình phương đáp ứng đúng yêu cầu. Đây là một nguyên hàm của hàm f bằng hai x, trên toàn bộ trục số thực.

### Phân cảnh 02.02 – Thấy rõ bằng tiếp tuyến
- **Thông điệp:** Tại x = 1, hệ số góc tiếp tuyến bằng 2.
- **Mô hình động:** `tangent_move`.
- **Công thức Typst:** `derivative` → `$F'(x) = 2x$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Trên parabol, tại hoành độ một, hệ số góc tiếp tuyến bằng hai. Khi chuyển tới x bằng không, tiếp tuyến nằm ngang. Điều đó phù hợp hoàn toàn với biểu thức đạo hàm hai x.

### Phân cảnh 02.03 – Nhớ đúng chiều suy luận
- **Thông điệp:** Lấy đạo hàm để kiểm tra nguyên hàm.
- **Mô hình động:** `reverse`.
- **Công thức Typst:** `square` → `$F(x) = x^2$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Ta đã đi từ yêu cầu đạo hàm bằng hai x, đoán ra hàm x bình phương, rồi lấy đạo hàm để kiểm tra. Chiều kiểm tra luôn là từ hàm tìm được quay về đạo hàm đã cho.

### Phân cảnh 02.04 – Khái niệm nguyên hàm
- **Thông điệp:** F là nguyên hàm của f trên một khoảng I nếu F' = f trên I.
- **Mô hình động:** `reverse`.
- **Công thức Typst:** `definition` → `$F'(x) = f(x)$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Một cách chính xác, hàm F được gọi là nguyên hàm của f trên khoảng I khi đạo hàm của F tại mọi điểm thuộc I bằng f. Chúng ta cần nói rõ khoảng đang xét, vì một số hàm không xác định trên toàn trục số.

## Chương 03 – Vì sao có hằng số C?

### Phân cảnh 03.01 – Có phải chỉ có x²?
- **Thông điệp:** x² + 2 cũng có đạo hàm là 2x.
- **Mô hình động:** `family`.
- **Công thức Typst:** `shiftplus` → `$F(x) = x^2+2$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Hãy thử cộng thêm hai vào hàm x bình phương. Đồ thị đi lên hai đơn vị, nhưng đạo hàm vẫn bằng hai x. Như vậy, chúng ta đã tìm được đáp án thứ hai.

### Phân cảnh 03.02 – Thử thêm những giá trị khác
- **Thông điệp:** x² − 2, x², x² + 2 đều phù hợp.
- **Mô hình động:** `family`.
- **Công thức Typst:** `family` → `$x^2-2 quad x^2 quad x^2+2$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Nếu cộng thêm âm hai, đồ thị đi xuống hai đơn vị. Cả ba đường parabol có cùng hình dạng, chỉ khác vị trí theo chiều thẳng đứng. Đạo hàm của chúng đều bằng hai x tại cùng một hoành độ.

### Phân cảnh 03.03 – Hằng số tự do
- **Thông điệp:** Với mọi hằng số C, F(x) = x² + C.
- **Mô hình động:** `family`.
- **Công thức Typst:** `general` → `$F(x) = x^2+C$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Thay hai, âm hai, hay bất kỳ số thực nào bởi ký hiệu C, ta được cả một họ nguyên hàm. Phép lấy đạo hàm làm mất hằng số cộng thêm, vì đạo hàm của một hằng số bằng không.

### Phân cảnh 03.04 – Một họ, không phải một đường
- **Thông điệp:** Mỗi C cho một đồ thị khác nhau.
- **Mô hình động:** `family_shift`.
- **Công thức Typst:** `general` → `$F(x) = x^2+C$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Quan sát các đường cong xê dịch lên hoặc xuống. Ta có vô số hàm số khác nhau nhưng cùng một đạo hàm. Đó là ý nghĩa hình học của hằng số C trong phép tính nguyên hàm.

## Chương 04 – Các tiếp tuyến có cùng hệ số góc

### Phân cảnh 04.01 – Phóng to một điểm
- **Thông điệp:** Xét các đồ thị tại cùng hoành độ x = 1.
- **Mô hình động:** `tangent`.
- **Công thức Typst:** `sameslope` → `$F_1'(x) = F_2'(x) = 2x$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Lấy một điểm có hoành độ bằng một trên từng parabol. Dù tung độ khác nhau, các tiếp tuyến tại những điểm này đều có cùng hệ số góc bằng hai. Chúng ta đang so sánh các tiếp tuyến tại cùng một hoành độ.

### Phân cảnh 04.02 – Ba đường tiếp tuyến song song
- **Thông điệp:** Đổi C không làm đổi độ dốc.
- **Mô hình động:** `tangent`.
- **Công thức Typst:** `sameslope` → `$F_1'(x) = F_2'(x) = 2x$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Ba đường tiếp tuyến màu vàng trên màn hình song song với nhau. Vì cộng hằng số chỉ tịnh tiến đồ thị lên xuống, nó không làm thay đổi độ dốc của đường cong. Đây là lý do trực quan cho việc đạo hàm không đổi.

### Phân cảnh 04.03 – Đạo hàm phụ thuộc x
- **Thông điệp:** Tại x khác, hệ số góc có thể thay đổi.
- **Mô hình động:** `tangent_move`.
- **Công thức Typst:** `derivative` → `$F'(x) = 2x$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Khi dịch điểm xét sang một hoành độ khác, chẳng hạn x bằng âm một, hệ số góc trở thành âm hai. Cần phân biệt hai điều: hệ số góc đổi theo x, nhưng không đổi theo hằng số C tại cùng x.

### Phân cảnh 04.04 – Kết luận từ hình học
- **Thông điệp:** Tất cả F(x) = x² + C có cùng đạo hàm 2x.
- **Mô hình động:** `tangent`.
- **Công thức Typst:** `general` → `$F(x) = x^2+C$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Từ ba đường parabol và các tiếp tuyến, ta đã nhìn thấy lý do cùng một đạo hàm lại ứng với nhiều hàm số. Điều này không riêng x bình phương, mà là tính chất chung của nguyên hàm trên một khoảng.

## Chương 05 – Hai nguyên hàm sai khác một hằng số

### Phân cảnh 05.01 – So sánh hai nguyên hàm
- **Thông điệp:** Lấy F₁(x) = x² − 1 và F₂(x) = x² + 2.
- **Mô hình động:** `difference`.
- **Công thức Typst:** `difference` → `$F_1(x) = x^2-1 quad F_2(x) = x^2+2$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Giờ hãy xét hai nguyên hàm khác nhau của cùng hàm hai x. Một hàm là x bình phương trừ một, hàm còn lại là x bình phương cộng hai. Ta muốn biết chúng khác nhau theo quy luật nào.

### Phân cảnh 05.02 – Hiệu có thay đổi không?
- **Thông điệp:** F₂(x) − F₁(x) luôn bằng 3.
- **Mô hình động:** `difference`.
- **Công thức Typst:** `constantdifference` → `$F_2(x)-F_1(x)=3$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Tại x bằng âm một, bằng không, bằng một hay bất kỳ giá trị nào, khoảng cách theo phương thẳng đứng giữa hai đường đều bằng ba. Về đại số, hiệu của chúng rút gọn thành hằng số ba.

### Phân cảnh 05.03 – Tại sao luôn như vậy?
- **Thông điệp:** Đạo hàm của hiệu bằng 0.
- **Mô hình động:** `difference`.
- **Công thức Typst:** `zeroderivative` → `$(F_2-F_1)'=0$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Nếu F một và F hai có cùng đạo hàm trên một khoảng, đạo hàm của F hai trừ F một bằng không. Theo tính chất hàm có đạo hàm bằng không trên một khoảng, hiệu đó là hằng số trên khoảng ấy.

### Phân cảnh 05.04 – Chú ý miền xác định
- **Thông điệp:** Kết luận về hằng số được xét trên từng khoảng.
- **Mô hình động:** `difference`.
- **Công thức Typst:** `interval` → `$F_2(x)-F_1(x)=C$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Trong các bài toán có miền xác định bị tách rời, ta phải xét từng khoảng riêng biệt. Không được khẳng định cùng một hằng số C cho hai khoảng rời nhau nếu không có thêm điều kiện.

## Chương 06 – Xác định nguyên hàm bằng một điều kiện

### Phân cảnh 06.01 – Chọn một thành viên của họ
- **Thông điệp:** Biết thêm F(1) = 3.
- **Mô hình động:** `condition`.
- **Công thức Typst:** `condition` → `$F(1)=3$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Chúng ta vẫn có vô số hàm x bình phương cộng C. Nhưng bài toán cho biết đồ thị cần đi qua điểm có hoành độ một và tung độ ba. Điều kiện này sẽ giúp xác định hằng số chưa biết.

### Phân cảnh 06.02 – Thay tọa độ điểm
- **Thông điệp:** 1 + C = 3.
- **Mô hình động:** `condition`.
- **Công thức Typst:** `solveC` → `$1+C=3$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Thay x bằng một vào F của x bằng x bình phương cộng C. Ta được một cộng C bằng ba. Đây là phương trình đơn giản để tìm hằng số.

### Phân cảnh 06.03 – Xác định C
- **Thông điệp:** C = 2, nên F(x) = x² + 2.
- **Mô hình động:** `condition_shift`.
- **Công thức Typst:** `answerC` → `$F(x)=x^2+2$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Giải phương trình ta được C bằng hai. Khi ấy đồ thị tương ứng chính là parabol đi qua điểm một phẩy ba. Hình động đang đưa đường cong đến đúng vị trí của điểm điều kiện.

### Phân cảnh 06.04 – Kiểm tra hai điều kiện
- **Thông điệp:** F'(x) = 2x và F(1) = 3.
- **Mô hình động:** `condition`.
- **Công thức Typst:** `answerC` → `$F(x)=x^2+2$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Đừng dừng ở kết quả C bằng hai. Hãy kiểm tra cả hai yêu cầu: đạo hàm phải bằng hai x, đồng thời giá trị hàm tại x bằng một phải bằng ba. Khi cả hai đều đúng, lời giải mới hoàn chỉnh.

## Chương 07 – Ứng dụng: tìm vị trí từ vận tốc

### Phân cảnh 07.01 – Vận tốc chưa cho vị trí
- **Thông điệp:** Giả sử v(t) = 2t + 1 mét mỗi giây.
- **Mô hình động:** `motion_v`.
- **Công thức Typst:** `velocity` → `$v(t)=2t+1$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Trong chuyển động thẳng theo một trục tọa độ, vận tốc là đạo hàm của tọa độ theo thời gian. Nếu biết vận tốc bằng hai t cộng một, liệu ta có biết vật đang ở vị trí nào tại mỗi thời điểm không?

### Phân cảnh 07.02 – Khôi phục hàm tọa độ
- **Thông điệp:** s(t) = t² + t + C.
- **Mô hình động:** `motion_s`.
- **Công thức Typst:** `position` → `$s(t)=t^2+t+C$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Do đạo hàm của t bình phương cộng t là hai t cộng một, nên một nguyên hàm của vận tốc là t bình phương cộng t. Ta vẫn phải cộng hằng số C, vì riêng vận tốc không cho biết tọa độ ban đầu.

### Phân cảnh 07.03 – Tọa độ ban đầu
- **Thông điệp:** Nếu s(0) = 2 mét thì C = 2.
- **Mô hình động:** `motion_s`.
- **Công thức Typst:** `position_final` → `$s(t)=t^2+t+2$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Giả sử tại thời điểm không giây, vật ở vị trí hai mét so với gốc tọa độ. Thay t bằng không vào biểu thức s, ta tìm được C bằng hai. Đây chính là ý nghĩa thực tế của hằng số nguyên hàm.

### Phân cảnh 07.04 – Đọc đúng các đại lượng
- **Thông điệp:** Vận tốc là mét/giây; tọa độ là mét.
- **Mô hình động:** `motion_s`.
- **Công thức Typst:** `position_final` → `$s(t)=t^2+t+2$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Hàm tọa độ của vật trở thành t bình phương cộng t cộng hai. Đơn vị của tọa độ là mét; vận tốc là mét trên giây. Trong bài toán thực tế, phải phân biệt tọa độ, độ dời và tổng quãng đường đi được.

## Chương 08 – Tự luyện và tổng kết

### Phân cảnh 08.01 – Bài tập tự luyện
- **Thông điệp:** Biết G'(x) = 3x² và G(1) = 5.
- **Mô hình động:** `practice`.
- **Công thức Typst:** `practice` → `$G'(x)=3x^2$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Trước khi xem lời giải, em hãy thử tìm một hàm G có đạo hàm bằng ba x bình phương và đi qua điểm một phẩy năm. Hãy làm theo ba bước: tìm một nguyên hàm, thêm hằng số C, rồi dùng điều kiện để xác định C.

### Phân cảnh 08.02 – Bước một: tìm họ nguyên hàm
- **Thông điệp:** G(x) = x³ + C.
- **Mô hình động:** `practice`.
- **Công thức Typst:** `practice_primitive` → `$G(x)=x^3+C$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Vì đạo hàm của x lập phương bằng ba x bình phương, họ nguyên hàm là x lập phương cộng C. Đó mới là đáp án tổng quát, chưa thỏa mãn đủ điều kiện ban đầu.

### Phân cảnh 08.03 – Bước hai: dùng điều kiện
- **Thông điệp:** G(1) = 5 suy ra C = 4.
- **Mô hình động:** `practice_shift`.
- **Công thức Typst:** `practice_condition` → `$1+C=5$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Thay x bằng một, ta có một cộng C bằng năm, nên C bằng bốn. Đồ thị đang được tịnh tiến để đi qua điểm có tọa độ một và năm.

### Phân cảnh 08.04 – Bước ba: kiểm tra và ghi nhớ
- **Thông điệp:** G(x) = x³ + 4.
- **Mô hình động:** `practice`.
- **Công thức Typst:** `practice_final` → `$G(x)=x^3+4$`.
- **Thời lượng nền:** 27 giây.
- **Thuyết minh:** Kết quả là G bằng x lập phương cộng bốn. Đạo hàm đúng bằng ba x bình phương và giá trị tại một là năm. Từ bài này, em hãy nhớ: nguyên hàm là đi ngược đạo hàm; trên một khoảng, các nguyên hàm chỉ khác nhau một hằng số; điều kiện ban đầu giúp xác định hằng số đó.

