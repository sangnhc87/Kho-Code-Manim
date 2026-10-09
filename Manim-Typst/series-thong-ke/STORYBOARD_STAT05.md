# STAT05 – Storyboard chi tiết (8 chương, 32 nhịp)

## Thiết kế
- Bố cục hai cột: hình động bên trái, phát biểu và công thức Typst bên phải.
- Sử dụng 40 điểm giả lập thống nhất với STAT01–STAT04.
- Tứ phân vị theo phương pháp trung vị hai nửa của STAT04.
- Khi có ngoại lệ, phân biệt hộp năm số và hộp Tukey; các râu Tukey tới quan sát hợp lệ xa nhất.
- Mỗi nhịp 27 giây nền; TTS có thể kéo dài từng nhịp.

## Chương 01 – KHOẢNG BIẾN THIÊN VÀ HAI CỰC TRỊ

### Nhịp 1 – Một câu hỏi mới
**Thông điệp:** Vị trí trung tâm chưa nói hết độ phân tán.
**Hình:** trạng thái 1.1 của mô hình chương 1.
**Lời giảng:** Ba tập trước đã hướng dẫn đọc dữ liệu và tìm số trung bình, trung vị, mốt, tứ phân vị. Nhưng hai lớp có thể cùng trung bình trong khi các điểm cách xa nhau rất khác. Hôm nay chúng ta sẽ đo độ trải rộng và biến bộ số liệu thành biểu đồ hộp. Mọi kết quả đều phải xuất phát từ dữ liệu thực tế được hiển thị, không phải con số chọn tùy ý.

### Nhịp 2 – Tìm hai cực trị
**Thông điệp:** 40 điểm: nhỏ nhất 4, lớn nhất 10.
**Hình:** trạng thái 1.2 của mô hình chương 1.
**Lời giảng:** Ta tiếp tục bộ bốn mươi điểm kiểm tra giả lập đã dùng ở các video đầu. Khi sắp xếp dữ liệu, điểm bốn ở đầu dãy, điểm mười ở cuối dãy. Hai giá trị này là giá trị nhỏ nhất và lớn nhất. Chúng quyết định khoảng biến thiên, nhưng chưa biểu diễn đầy đủ hình dạng các nhóm điểm nằm ở giữa.

### Nhịp 3 – Độ rộng của toàn dãy
**Thông điệp:** R = max − min = 10 − 4 = 6.
**Hình:** trạng thái 1.3 của mô hình chương 1.
**Lời giảng:** Khoảng biến thiên được ký hiệu R, bằng giá trị lớn nhất trừ giá trị nhỏ nhất. Ta lấy mười trừ bốn, được sáu điểm. Đoạn màu nối hai cực trị trên trục số có độ dài đúng sáu. Cách tính rất nhanh, nhưng cũng có nhược điểm: toàn bộ kết quả phụ thuộc vào chỉ hai quan sát biên.

### Nhịp 4 – Thay đổi một giá trị
**Thông điệp:** Kéo cực trị 10 thành 30: R = 26.
**Hình:** trạng thái 1.4 của mô hình chương 1.
**Lời giảng:** Hãy thử thay một điểm mười bằng ba mươi. Đây chỉ là thí nghiệm minh họa về toán học, không phải điểm số hợp lệ của thang mười. Khoảng biến thiên lập tức tăng từ sáu lên hai mươi sáu, dù ba mươi chín điểm còn lại không đổi. Vì vậy ta cần một số đo khác mô tả vùng trung tâm của dữ liệu.

## Chương 02 – NĂM MỐC ĐẶC TRƯNG VÀ KHOẢNG TỨ PHÂN VỊ

### Nhịp 1 – Ba tứ phân vị đã học
**Thông điệp:** Q1 = 6, Q2 = 7, Q3 = 8.
**Hình:** trạng thái 2.1 của mô hình chương 2.
**Lời giảng:** Từ bài trước, các tứ phân vị của bốn mươi điểm lần lượt bằng sáu, bảy, tám. Ta đặt chúng lên cùng trục số với hai cực trị. Q hai chính là trung vị. Q một và Q ba là trung vị của hai nửa đã sắp xếp, theo quy ước sách giáo khoa đang dùng. Chúng không phải ba mốc chia đoạn từ bốn đến mười thành bốn đoạn bằng nhau.

### Nhịp 2 – Khoảng tứ phân vị
**Thông điệp:** IQR = Q3 − Q1 = 2.
**Hình:** trạng thái 2.2 của mô hình chương 2.
**Lời giảng:** Khoảng tứ phân vị bằng Q ba trừ Q một. Với bộ dữ liệu này, tám trừ sáu bằng hai. Phần trục số từ sáu đến tám được tô sáng để học sinh nhìn ra vùng giữa của phân bố. IQR ít nhạy hơn khoảng biến thiên đối với một thay đổi ở cực trị, nhưng không phải hoàn toàn bất biến với mọi thay đổi dữ liệu.

### Nhịp 3 – Năm số đặc trưng
**Thông điệp:** 4 – 6 – 7 – 8 – 10.
**Hình:** trạng thái 2.3 của mô hình chương 2.
**Lời giảng:** Đặt năm mốc theo thứ tự: nhỏ nhất bốn, Q một bằng sáu, trung vị bảy, Q ba bằng tám, lớn nhất mười. Ta gọi đây là tóm tắt năm số. Nó cho phép dựng một biểu đồ hộp đơn giản. Tóm tắt năm số không biểu diễn từng tần số, vì vậy cần tránh suy diễn về hình dạng phân bố chỉ bằng năm mốc.

### Nhịp 4 – So sánh R và IQR
**Thông điệp:** R = 6; IQR = 2.
**Hình:** trạng thái 2.4 của mô hình chương 2.
**Lời giảng:** Hai đoạn có độ dài khác nhau cùng xuất hiện trên trục số. Đoạn dài sáu cho biết dữ liệu trải rộng từ cực tiểu đến cực đại. Đoạn dài hai cho biết độ rộng phần trung tâm giữa Q một và Q ba. Khoảng biến thiên và khoảng tứ phân vị cùng đo mức độ phân tán nhưng không thể thay thế nhau. Khi giải bài, hãy ghi rõ đại lượng đang tính.

## Chương 03 – DỰNG BIỂU ĐỒ HỘP TỪ 40 ĐIỂM

### Nhịp 1 – Dựng chiếc hộp
**Thông điệp:** Hộp có hai mép tại Q1 = 6 và Q3 = 8.
**Hình:** trạng thái 3.1 của mô hình chương 3.
**Lời giảng:** Giờ chúng ta bắt đầu xây dựng biểu đồ hộp từng bước. Đầu tiên, dựng một hình chữ nhật có cạnh trái ở Q một bằng sáu, cạnh phải ở Q ba bằng tám. Hộp biểu diễn độ trải rộng giữa hai tứ phân vị. Trên cùng thang đo, hộp rộng hơn nghĩa là IQR lớn hơn. Đây là cách nhìn rất nhanh khi so sánh nhiều mẫu.

### Nhịp 2 – Vạch trung vị
**Thông điệp:** Đặt đường đậm tại Q2 = 7.
**Hình:** trạng thái 3.2 của mô hình chương 3.
**Lời giảng:** Vạch dọc bên trong hộp biểu thị trung vị. Với bộ số liệu này, trung vị bảy nằm giữa sáu và tám. Tuy nhiên ở dữ liệu bất đối xứng, trung vị có thể nằm gần mép trái hoặc mép phải của hộp. Không nên mặc định vạch trung vị luôn đi qua tâm hình chữ nhật. Đó là dấu hiệu cần đọc trực tiếp từ số liệu.

### Nhịp 3 – Thêm hai râu
**Thông điệp:** Trái dừng ở 4, phải dừng ở 10.
**Hình:** trạng thái 3.3 của mô hình chương 3.
**Lời giảng:** Kế tiếp vẽ hai đoạn râu nối hộp đến các quan sát hai đầu. Với dữ liệu gốc, không có điểm nào vượt ngưỡng ngoại lệ theo quy tắc Tukey, nên râu trái đến bốn và râu phải đến mười. Hai vạch ngắn được đặt ở hai đầu râu. Tập này sẽ làm rõ sự khác nhau giữa râu chạm cực trị và râu dừng ở quan sát không ngoại lệ.

### Nhịp 4 – Đọc biểu đồ hoàn chỉnh
**Thông điệp:** Năm số lần lượt 4, 6, 7, 8, 10.
**Hình:** trạng thái 3.4 của mô hình chương 3.
**Lời giảng:** Biểu đồ hộp đã hoàn chỉnh. Đọc từ trái sang phải, ta thu được nhỏ nhất bốn, Q một sáu, trung vị bảy, Q ba tám, lớn nhất mười. Hình hộp tóm tắt vị trí trung tâm và mức phân tán, nhưng không cho ta biết trực tiếp có bao nhiêu điểm bảy hay phân bố có mấy đỉnh. Hãy phối hợp biểu đồ hộp với biểu đồ điểm nếu cần.

## Chương 04 – NGƯỠNG NGOẠI LỆ VÀ BIỂU ĐỒ TUKEY

### Nhịp 1 – Kéo một điểm ra xa
**Thông điệp:** Điểm lớn nhất dịch từ 10 đến 30.
**Hình:** trạng thái 4.1 của mô hình chương 4.
**Lời giảng:** Hãy quan sát một điểm số dịch từ mười sang ba mươi trên trục ngang. Trong lúc kéo, giá trị cực đại và khoảng biến thiên thay đổi liên tục, nhưng ba tứ phân vị vẫn là sáu, bảy, tám. Chuyển động này minh họa vì sao IQR ổn định trước thay đổi của một cực trị. Không được vì thế khẳng định mọi phép thay điểm đơn lẻ đều để IQR không đổi.

### Nhịp 2 – Đặt hai hàng rào Tukey
**Thông điệp:** Ngưỡng dưới 3 và ngưỡng trên 11.
**Hình:** trạng thái 4.2 của mô hình chương 4.
**Lời giảng:** Một quy tắc nhận diện ngoại lệ phổ biến lấy Q một trừ một phẩy năm lần IQR và Q ba cộng một phẩy năm lần IQR. Với Q một sáu, Q ba tám và IQR hai, ta nhận được ngưỡng dưới bằng ba, ngưỡng trên bằng mười một. Những quan sát nằm ngoài hai ngưỡng này được đánh dấu để kiểm tra thêm.

### Nhịp 3 – Râu không nằm ở hàng rào
**Thông điệp:** Râu vẫn chạm 4 và 10; 30 vẽ riêng.
**Hình:** trạng thái 4.3 của mô hình chương 4.
**Lời giảng:** Trong biểu đồ hộp Tukey, hai đầu râu là quan sát xa nhất vẫn còn nằm bên trong hai ngưỡng, không phải chính tọa độ ngưỡng. Với dữ liệu sau thay đổi, đầu râu trái tại bốn, đầu râu phải tại mười; điểm ba mươi được tách thành một dấu riêng. Đây là chỗ rất dễ vẽ nhầm nếu chỉ học thuộc công thức một phẩy năm IQR.

### Nhịp 4 – Ngoại lệ không đồng nghĩa lỗi
**Thông điệp:** 30 được gắn cờ; cần bối cảnh để kết luận.
**Hình:** trạng thái 4.4 của mô hình chương 4.
**Lời giảng:** Dấu chấm đỏ báo một quan sát ngoại lệ theo quy tắc IQR. Ngoại lệ không nhất thiết là lỗi nhập liệu và cũng không phải giá trị phải xóa bỏ. Khi thống kê dữ liệu thật, chúng ta cần kiểm tra đơn vị, cách ghi, nguồn số liệu và nguyên nhân. Quy tắc phát hiện giúp đặt câu hỏi, chứ không tự đưa ra kết luận về chất lượng dữ liệu.

## Chương 05 – SO SÁNH HAI MẪU CÓ CÙNG TRUNG VỊ

### Nhịp 1 – Hai mẫu có trung vị bằng nhau
**Thông điệp:** Trung vị A và B đều là 5,5.
**Hình:** trạng thái 5.1 của mô hình chương 5.
**Lời giảng:** Ta đưa vào hai bộ số liệu minh họa độc lập, không phải bốn mươi điểm của lớp. Mẫu A và mẫu B đều có trung vị năm phẩy năm. Nếu chỉ nhìn trung vị, ta sẽ bỏ qua một khác biệt quan trọng: các quan sát phân tán xa hay gần giá trị giữa. Hãy dùng hai biểu đồ hộp chung một thang số để quan sát.

### Nhịp 2 – Hộp của mẫu A
**Thông điệp:** Q1 = 3,5; Q3 = 7,5; IQR = 4.
**Hình:** trạng thái 5.2 của mô hình chương 5.
**Lời giảng:** Mẫu A có các số từ hai đến chín. Tứ phân vị dưới bằng ba phẩy năm, tứ phân vị trên bằng bảy phẩy năm, nên IQR bằng bốn. Hộp màu xanh được dựng tương ứng trên trục. Vạch trung vị ở năm phẩy năm. Đọc ba mốc này giúp ta mô tả phần trung tâm của mẫu mà không cần xem từng điểm riêng lẻ.

### Nhịp 3 – Hộp của mẫu B
**Thông điệp:** Q1 = 2; Q3 = 10; IQR = 8.
**Hình:** trạng thái 5.3 của mô hình chương 5.
**Lời giảng:** Mẫu B có nhiều giá trị hai và mười. Tứ phân vị dưới bằng hai và tứ phân vị trên bằng mười, nên IQR bằng tám. Hộp màu cam rộng hơn rõ rệt, trong khi trung vị của hai mẫu vẫn bằng nhau. Đây là ví dụ tốt cho thấy vì sao mô tả phân bố không thể chỉ dừng ở một số đo xu thế trung tâm.

### Nhịp 4 – Kết luận đúng mức
**Thông điệp:** IQR mẫu B gấp đôi mẫu A.
**Hình:** trạng thái 5.4 của mô hình chương 5.
**Lời giảng:** Khi hai biểu đồ dùng cùng đơn vị, cùng tỷ lệ trục, có thể kết luận IQR của mẫu B gấp đôi mẫu A. Nhưng từ đó không thể suy ra phương sai của B cũng gấp đôi A, hay chất lượng dữ liệu của B thấp hơn. Mỗi đại lượng chỉ đo một khía cạnh. Ta sẽ học phương sai và độ lệch chuẩn kỹ hơn trong những video tiếp theo.

## Chương 06 – CÙNG KHOẢNG BIẾN THIÊN, KHÁC PHÂN TÁN

### Nhịp 1 – Hai mẫu cùng khoảng biến thiên
**Thông điệp:** Nhỏ nhất 1, lớn nhất 9 cho cả hai.
**Hình:** trạng thái 6.1 của mô hình chương 6.
**Lời giảng:** Bây giờ xét hai dãy tám số khác nhau về tần số nhưng cùng có cực tiểu một và cực đại chín. Do đó cả hai có khoảng biến thiên bằng tám. Các chấm được xếp thành hai hàng, cùng một hệ trục số. Từ hai đầu của dãy, ta chưa thể phân biệt được mức độ tập trung của phần giữa.

### Nhịp 2 – Mẫu A phân cực
**Thông điệp:** Q1 = 1; Q3 = 9; IQR = 8.
**Hình:** trạng thái 6.2 của mô hình chương 6.
**Lời giảng:** Trong dãy đầu tiên, bốn giá trị bằng một và bốn giá trị bằng chín. Trung vị bằng năm, nhưng Q một bằng một, Q ba bằng chín. Chiều rộng hộp bằng tám, trải gần hết khoảng biến thiên. Đây là ví dụ phân bố gồm hai cụm xa nhau. Biểu đồ hộp cho thấy hộp rộng, nhưng bản thân nó chưa chứng minh số đỉnh của phân bố.

### Nhịp 3 – Mẫu B tập trung ở giữa
**Thông điệp:** Q1 = 4; Q3 = 6; IQR = 2.
**Hình:** trạng thái 6.3 của mô hình chương 6.
**Lời giảng:** Ở dãy thứ hai, các giá trị giữa tập trung quanh bốn, năm và sáu; chỉ hai cực trị giữ tại một và chín. Trung vị vẫn là năm, khoảng biến thiên vẫn bằng tám, nhưng tứ phân vị dưới bằng bốn, tứ phân vị trên bằng sáu. IQR chỉ bằng hai. So hai hộp ta thấy ngay vùng giữa phân tán khác nhau.

### Nhịp 4 – Biểu đồ hộp không kể hết câu chuyện
**Thông điệp:** Kết hợp thêm biểu đồ điểm khi cần.
**Hình:** trạng thái 6.4 của mô hình chương 6.
**Lời giảng:** Dù hai dãy có cùng cực trị và cùng trung vị, hình dạng tần số có thể khác nhau đáng kể. Khoảng biến thiên và IQR bổ sung thông tin nhưng không đủ để mô tả toàn bộ phân bố. Khi cần quan sát cụm dữ liệu, tính đối xứng hay các đỉnh, hãy dùng thêm biểu đồ điểm hoặc histogram. Đây là một thói quen tốt khi trình bày thống kê.

## Chương 07 – QUY ƯỚC VẼ HỘP VÀ CÁC TRƯỜNG HỢP ĐẶC BIỆT

### Nhịp 1 – Hai cách dựng râu
**Thông điệp:** Râu cực trị và râu theo quy tắc Tukey.
**Hình:** trạng thái 7.1 của mô hình chương 7.
**Lời giảng:** Một số bài học dùng biểu đồ hộp với hai râu kéo thẳng đến giá trị nhỏ nhất và lớn nhất. Một quy ước khác, biểu đồ Tukey, đánh dấu các điểm ngoài khoảng một phẩy năm IQR và đặt râu ở quan sát hợp lệ xa nhất. Với dữ liệu có ngoại lệ, hai biểu đồ sẽ khác nhau. Đọc chú thích của đề để dùng đúng quy ước.

### Nhịp 2 – Mọi giá trị đều bằng 5
**Thông điệp:** R = 0; IQR = 0; hộp co thành vạch.
**Hình:** trạng thái 7.2 của mô hình chương 7.
**Lời giảng:** Nếu tám quan sát đều bằng năm, giá trị nhỏ nhất, hai tứ phân vị, trung vị và giá trị lớn nhất trùng nhau. Cả khoảng biến thiên và khoảng tứ phân vị bằng không. Khi đó hình hộp không có chiều rộng; tất cả mốc nằm trên một vạch. Phần mềm vẽ tốt phải hiển thị đúng tình huống này, không tự tạo độ rộng giả.

### Nhịp 3 – Nếu có nhiều số trùng
**Thông điệp:** IQR bằng 0 vẫn cần xem dữ liệu gốc.
**Hình:** trạng thái 7.3 của mô hình chương 7.
**Lời giảng:** Dữ liệu rời rạc có thể chứa nhiều giá trị lặp. Khi Q một bằng Q ba, IQR bằng không và hai ngưỡng một phẩy năm IQR trùng nhau. Quy tắc nhận diện ngoại lệ sẽ cần được diễn giải thận trọng theo bối cảnh. Không nên kết luận một quan sát sai chỉ vì nó nằm bên ngoài ngưỡng, nhất là khi mẫu nhỏ hoặc rất nhiều giá trị trùng.

### Nhịp 4 – Điều biểu đồ không tiết lộ
**Thông điệp:** Năm mốc không thay thế phân bố đầy đủ.
**Hình:** trạng thái 7.4 của mô hình chương 7.
**Lời giảng:** Biểu đồ hộp giỏi tóm tắt vị trí giữa và độ phân tán, nhưng không cung cấp đầy đủ tần số hay nguyên nhân của biến thiên. Tới đây, chúng ta đã biết tính khoảng biến thiên, IQR, xác định ngoại lệ và chọn loại râu thích hợp. Trong bài thi, luôn viết rõ quy ước tứ phân vị và kiểm tra xem đề yêu cầu biểu đồ hộp năm số hay biểu đồ Tukey.

## Chương 08 – LUYỆN TẬP: ĐỌC HỘP VÀ PHÁT HIỆN NGOẠI LỆ

### Nhịp 1 – Bài thử sức với 11 giá trị
**Thông điệp:** Tìm năm mốc, hai độ rộng và ngoại lệ.
**Hình:** trạng thái 8.1 của mô hình chương 8.
**Lời giảng:** Hãy tự giải bài cuối với dãy đã xếp: hai, bốn, bốn, năm, năm, sáu, bảy, tám, tám, chín, hai mươi. Có mười một quan sát. Em hãy tìm ba tứ phân vị, khoảng biến thiên và IQR. Sau đó áp dụng ngưỡng một phẩy năm IQR, xác định hai đầu râu Tukey. Hãy tạm dừng hình để thực hành trước khi xem lời giải.

### Nhịp 2 – Tính tứ phân vị trước
**Thông điệp:** Q1 = 4; Q2 = 6; Q3 = 8.
**Hình:** trạng thái 8.2 của mô hình chương 8.
**Lời giảng:** Vì số quan sát lẻ bằng mười một, trung vị là phần tử ở vị trí thứ sáu, bằng sáu. Bỏ phần tử giữa ra trước khi chia thành hai nửa. Nửa dưới có trung vị bốn, nửa trên có trung vị tám. Do đó Q một bằng bốn, Q hai bằng sáu, Q ba bằng tám. Ta kiểm tra bằng việc đánh dấu từng vị trí của dãy.

### Nhịp 3 – Tính hai hàng rào
**Thông điệp:** IQR = 4; ngưỡng dưới -2; ngưỡng trên 14.
**Hình:** trạng thái 8.3 của mô hình chương 8.
**Lời giảng:** Khoảng tứ phân vị bằng tám trừ bốn, được bốn. Một phẩy năm lần IQR bằng sáu, nên ngưỡng dưới bằng âm hai và ngưỡng trên bằng mười bốn. Quan sát hai mươi vượt ngưỡng trên nên là một ngoại lệ theo quy tắc Tukey. Giá trị hợp lệ thấp nhất là hai, giá trị hợp lệ cao nhất là chín.

### Nhịp 4 – Vẽ hộp đúng quy ước
**Thông điệp:** R = 18, IQR = 4, râu 2 đến 9, điểm 20 riêng.
**Hình:** trạng thái 8.4 của mô hình chương 8.
**Lời giảng:** Ta hoàn thiện hình: hộp từ bốn đến tám, trung vị tại sáu, râu trái tới hai, râu phải tới chín và điểm hai mươi đứng riêng. Khoảng biến thiên của dữ liệu gốc vẫn bằng hai mươi trừ hai, được mười tám; IQR bằng bốn. Từ đây chúng ta chuyển sang phương sai và độ lệch chuẩn để hiểu sâu hơn độ phân tán của cả dãy.

