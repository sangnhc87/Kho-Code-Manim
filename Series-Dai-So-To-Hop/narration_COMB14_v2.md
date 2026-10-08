# SANG MATH · COMB14 V2 · PHƯƠNG PHÁP GỘP KHỐI

## Bản thuyết minh đồng bộ

Số nhịp: 48 · 8 chương · TTS=off
Tổng thời lượng dự kiến: 1118.8 giây.
Lời giảng bên dưới là nội dung đầy đủ được đưa vào tổng hợp giọng đọc; không cắt tùy ý.


## 01 · TƯ DUY ĐẾM PHẦN BÙ

### Nhịp 01 · 00:00 · BÀI TOÁN KHỞI ĐỘNG

Mỗi dãy gồm bốn vị trí và ở mỗi vị trí ta được chọn một trong ba chữ A, B, C. Các chữ được phép lặp và vị trí có ý nghĩa. Thay vì liệt kê từng dãy có ít nhất một chữ A, ta thử hỏi câu dễ hơn: một dãy hoàn toàn không có chữ A thì trông như thế nào? Câu hỏi ngược lại này sẽ dẫn ta đến phương pháp đếm phần bù.

**Trên màn hình:** Lập dãy bốn chữ từ A, B, C. | Cho phép lặp chữ; có xét thứ tự. | Hỏi có ít nhất một chữ A?
**Ghi nhớ:** ĐỌC KỸ ĐỐI TƯỢNG ĐANG ĐẾM.

### Nhịp 02 · 00:23 · CHIA TOÀN BỘ THÀNH HAI

Hãy nhìn toàn bộ không gian gồm tám mươi mốt dãy. Mỗi dãy hoặc có ít nhất một chữ A, hoặc không hề có chữ A. Hai mệnh đề này là phủ định của nhau, nên chúng không thể đồng thời đúng và cũng không có trường hợp thứ ba. Đó là điều kiện toán học quan trọng nhất để phép trừ số cách trở thành một chứng minh chứ không phải mẹo tính.

**Trên màn hình:** Nhóm xanh: có ít nhất một A. | Nhóm đỏ: hoàn toàn không có A. | Mỗi dãy thuộc đúng một nhóm.
**Ghi nhớ:** HAI NHÓM RỜI NHAU VÀ PHỦ HẾT.

### Nhịp 03 · 00:46 · ĐẾM PHẦN KHÔNG CÓ A

Nếu một dãy không có chữ A, mỗi vị trí bắt buộc chọn giữa B và C. Bốn vị trí độc lập, nên theo quy tắc nhân số dãy bị loại là hai mũ bốn, bằng mười sáu. Điều quan trọng là ta không đếm dãy bị loại bằng cách chọn vị trí đặt A; khi không có A thì không cần chọn vị trí nào cả. Đây chính là sự đơn giản hóa mà phương pháp phần bù mang lại.

**Trên màn hình:** Bỏ chữ A khỏi các lựa chọn. | Mỗi vị trí chỉ còn B hoặc C. | Có 2⁴ = 16 dãy không chứa A.
**Ghi nhớ:** PHẦN KHÔNG THỎA DỄ ĐẾM HƠN.

### Nhịp 04 · 01:09 · LẤY TỔNG TRỪ PHẦN BÙ

Bây giờ lấy tổng tám mươi mốt trừ đi mười sáu dãy hoàn toàn không có chữ A, được sáu mươi lăm. Ta không cần phân chia thành các trường hợp có một A, hai A, ba A và bốn A; chính những trường hợp ấy đã được gom vào một miền duy nhất. Trên hình, các thẻ đỏ biến mất và bộ đếm xanh biểu diễn số dãy còn lại.

**Trên màn hình:** Tất cả: 3⁴ = 81 dãy. | Không có A: 2⁴ = 16 dãy. | Có ít nhất một A: 65 dãy.
**Ghi nhớ:** KẾT QUẢ LÀ 65, KHÔNG PHẢI 64.

### Nhịp 05 · 01:32 · HIỂU CỤM TỪ ÍT NHẤT

Khi đề bài nói ít nhất một chữ A, những dãy có hai chữ A hoặc cả bốn chữ A đều hợp lệ. Nếu chỉ tính dãy có đúng một chữ A, ta phải chọn một trong bốn vị trí cho A rồi điền B hoặc C vào ba vị trí còn lại, được bốn nhân hai mũ ba, tức ba mươi hai. Số ba mươi hai nhỏ hơn sáu mươi lăm vì ta vừa bỏ sót các dãy có từ hai chữ A trở lên.

**Trên màn hình:** Ít nhất một: 1, 2, 3 hoặc 4. | Đúng một: chỉ có một chữ A. | Hai điều kiện cho kết quả khác nhau.
**Ghi nhớ:** KHÔNG NHẦM ÍT NHẤT VỚI ĐÚNG MỘT.

### Nhịp 06 · 01:56 · CÔNG THỨC TỔNG QUÁT

Tổng quát, một dãy độ dài k tạo từ n ký hiệu, cho phép lặp và xét thứ tự, có n mũ k khả năng. Nếu yêu cầu xuất hiện ít nhất một ký hiệu cụ thể, phần bù là các dãy chỉ dùng n trừ một ký hiệu khác, có n trừ một mũ k khả năng. Do đó lấy hiệu hai số. Công thức không dùng nguyên xi khi mỗi vị trí có số lựa chọn khác nhau hoặc khi cấm lặp.

**Trên màn hình:** Có n lựa chọn tại mỗi vị trí. | k vị trí, có xét thứ tự và cho lặp. | Cấm một ký hiệu: (n−1)ᵏ dãy.
**Ghi nhớ:** PHẢI XÁC ĐỊNH ĐÚNG PHẦN ĐỐI LẬP.


## 02 · CHỌN NHÓM CÓ ÍT NHẤT MỘT

### Nhịp 07 · 02:19 · CHỌN NHÓM HỌC SINH

Một lớp có năm học sinh nam và bốn học sinh nữ, tất cả đều phân biệt. Ta chọn một nhóm ba bạn đi thi mà yêu cầu nhóm có ít nhất một nữ. Vì chỉ chọn nhóm, đổi thứ tự tên các bạn không tạo ra nhóm mới. Có thể phân chia theo một, hai hoặc ba nữ, nhưng cách nhanh hơn là đếm tất cả nhóm ba người, rồi loại nhóm gồm toàn nam.

**Trên màn hình:** Lớp có 5 nam và 4 nữ. | Chọn một nhóm 3 học sinh. | Nhóm phải có ít nhất một nữ.
**Ghi nhớ:** KHÔNG CẦN CHIA BA TRƯỜNG HỢP NGAY.

### Nhịp 08 · 02:42 · VẼ MIỀN KHÔNG CÓ NỮ

Hãy tô màu những nhóm không có bất kỳ nữ nào. Ba thành viên đều phải đến từ năm học sinh nam, nên số nhóm này là tổ hợp chập ba của năm, bằng mười. Không có lý do gì để sắp thứ tự các bạn vì đề chỉ nói chọn đội. Trên hình, vùng đỏ chính là tập hợp bị loại, không có giao với vùng nhóm thỏa điều kiện.

**Trên màn hình:** Không có nữ nghĩa là cả ba đều nam. | Chọn 3 trong 5 nam. | Đó là phần bù của có ít nhất một nữ.
**Ghi nhớ:** PHẦN BÙ PHẢI PHỦ ĐÚNG TẤT CẢ TRƯỜNG HỢP SAI.

### Nhịp 09 · 03:05 · ĐÁP SỐ BẰNG PHẦN BÙ

Từ chín học sinh, có tám mươi tư nhóm ba người không xét thứ tự. Loại đi mười nhóm chỉ gồm nam, ta còn bảy mươi tư nhóm có ít nhất một nữ. Cách này không yêu cầu xét riêng một nữ, hai nữ, ba nữ. Mỗi nhóm hợp lệ chỉ xuất hiện đúng một lần trong phần tổng, và không nhóm hợp lệ nào nằm trong phần bị trừ.

**Trên màn hình:** Toàn bộ: 84 nhóm. | Nhóm toàn nam: 10 nhóm. | Hợp lệ: 84 − 10 = 74 nhóm.
**Ghi nhớ:** CHỌN NHÓM: SỬ DỤNG TỔ HỢP.

### Nhịp 10 · 03:28 · KIỂM BẰNG CÁC TRƯỜNG HỢP

Ta kiểm chứng bằng cách chia theo số nữ được chọn. Có đúng một nữ thì chọn một trong bốn nữ và hai trong năm nam, được bốn mươi nhóm. Có đúng hai nữ thì chọn hai trong bốn nữ và một trong năm nam, được ba mươi nhóm. Có ba nữ thì chọn ba trong bốn, được bốn nhóm. Ba trường hợp rời nhau, cộng lại bằng bảy mươi tư, khớp phép đếm phần bù.

**Trên màn hình:** Một nữ: 4·C₂⁵ = 40. | Hai nữ: C₂⁴·5 = 30. | Ba nữ: C₃⁴ = 4.
**Ghi nhớ:** TỔNG 40 + 30 + 4 = 74.

### Nhịp 11 · 03:51 · ĐỔI CÂU HỎI THÀNH ĐÚNG MỘT

Hãy thay đúng một chữ trong đề: từ ít nhất một nữ thành đúng một nữ. Khi đó nhóm có hai nữ hoặc ba nữ không còn hợp lệ. Ta chỉ giữ trường hợp một nữ và hai nam, được bốn mươi nhóm. Sự khác biệt giữa bốn mươi và bảy mươi tư chứng minh rằng không thể tùy tiện đồng nhất từ ít nhất với từ đúng.

**Trên màn hình:** Đúng một nữ không phải ít nhất một. | Chỉ chọn 1 nữ và 2 nam. | Số nhóm chỉ còn 40.
**Ghi nhớ:** ĐỌC MỘT TỪ SAI CÓ THỂ ĐỔI CẢ ĐÁP SỐ.

### Nhịp 12 · 04:15 · RÚT RA CÔNG THỨC CHUNG

Với n người phân biệt và r người thuộc nhóm đặc biệt, số cách chọn k người có ít nhất một người đặc biệt bằng tổ hợp chập k của n trừ tổ hợp chập k của n trừ r. Nếu n trừ r nhỏ hơn k thì không có nhóm nào hoàn toàn không đặc biệt, ta quy ước tổ hợp khi k lớn hơn số đối tượng bằng không. Mô hình này lặp lại trong rất nhiều bài toán chọn đội và chọn đồ vật.

**Trên màn hình:** n người có r người đặc biệt. | Chọn k người, cần ít nhất một đặc biệt. | Lấy toàn bộ trừ nhóm không đặc biệt.
**Ghi nhớ:** CÔNG THỨC CẦN k ≤ n VÀ r ≤ n.


## 03 · XẾP NGƯỜI VÀ ĐIỀU KIỆN CẤM

### Nhịp 13 · 04:38 · HAI NGƯỜI KHÔNG ĐỨNG KỀ

Với năm học sinh phân biệt, ta xét những hàng mà A và B không đứng cạnh nhau. Nếu xếp trực tiếp có thể phải chọn vị trí rất phức tạp, nhưng phần bù là A và B đứng cạnh. Điều kiện đối lập hoàn toàn rõ ràng: hai người hoặc cách nhau ít nhất một vị trí, hoặc họ đứng sát nhau. Không có trường hợp thứ ba, nên phép trừ sẽ không bỏ sót.

**Trên màn hình:** Xếp A, B, C, D, E vào một hàng. | Yêu cầu A và B không cạnh nhau. | Ta sẽ đếm trường hợp đứng cạnh.
**Ghi nhớ:** CẤM ĐỨNG CẠNH → PHẦN BÙ DỄ ĐẾM.

### Nhịp 14 · 05:01 · GỘP CẶP VI PHẠM

Khi A và B đứng cạnh nhau, ta xem hai người thành một khối. Khối đó cùng C, D, E là bốn đối tượng phân biệt để xếp, có bốn giai thừa cách. Bên trong khối, A đứng trước B hoặc B đứng trước A, tạo thêm thừa số hai. Vì vậy có bốn mươi tám hàng vi phạm điều kiện. Các hàng ấy chính là những hàng màu đỏ cần loại.

**Trên màn hình:** A và B đứng cạnh nhau. | Gộp thành một khối [AB]. | Còn 4 đối tượng; trong khối đổi được 2 cách.
**Ghi nhớ:** ĐỪNG QUÊN ĐỔI THỨ TỰ TRONG KHỐI.

### Nhịp 15 · 05:24 · TRỪ PHẦN VI PHẠM

Như vậy số cách xếp hợp lệ là năm giai thừa trừ hai nhân bốn giai thừa, bằng bảy mươi hai. Điều đáng nhớ là ta không hề giả định mọi vị trí A và B có xác suất như nhau. Ta dùng lập luận đếm chính xác bằng gộp khối. Sau phép trừ, hình động sẽ làm mờ toàn bộ các hàng chứa A B liên tiếp và chỉ để lại số lượng hợp lệ.

**Trên màn hình:** Tổng: 120 hàng. | Vi phạm: 48 hàng. | Hợp lệ: 72 hàng.
**Ghi nhớ:** PHẦN BÙ CHO KẾT QUẢ 72.

### Nhịp 16 · 05:47 · RÀNG BUỘC CẤM VỊ TRÍ ĐẦU

Đổi sang một điều kiện khác: có sáu học sinh xếp hàng, nhưng A không được đứng đầu. Tổng số hàng là sáu giai thừa bằng bảy trăm hai mươi. Nếu A bị cố định ở vị trí thứ nhất, năm người còn lại được xếp theo năm giai thừa, tức một trăm hai mươi. Trừ những hàng ấy ta còn sáu trăm cách phù hợp. Đây là ví dụ đơn giản nhất của điều kiện cấm một vị trí.

**Trên màn hình:** Sáu học sinh đứng thành hàng. | A không được đứng ở vị trí đầu. | Bù là A đứng đầu: 5! hàng.
**Ghi nhớ:** VỊ TRÍ CỐ ĐỊNH GIÚP ĐẾM PHẦN BÙ NHANH.

### Nhịp 17 · 06:11 · PHẢI ĐỌC TỪ KHÔNG

Bài toán có hai điều kiện như A không đứng đầu đồng thời A không đứng cạnh B thì không được cộng các số bị cấm rồi trừ một cách máy móc. Một hàng có thể vừa có A ở đầu vừa có A cạnh B, và khi đó đã bị trừ hai lần. Ta cần cộng lại phần giao hoặc chia các trường hợp rời nhau. Đây là tín hiệu dẫn tới nguyên lý bao hàm loại trừ ở những tập sau.

**Trên màn hình:** Không đứng kề: bù là đứng kề. | Không đứng đầu: bù là đứng đầu. | Không kề và không đầu: không chỉ trừ một lần.
**Ghi nhớ:** HAI ĐIỀU KIỆN CẤM CẦN XỬ LÝ GIAO.

### Nhịp 18 · 06:34 · THỬ THÁCH HAI CẤM

Với sáu người, điều kiện A không đứng đầu và A không đứng cạnh B có hai nhóm vi phạm. A đứng đầu có năm giai thừa, tức một trăm hai mươi hàng. A và B đứng cạnh có hai nhân năm giai thừa, tức hai trăm bốn mươi hàng. Phần giao buộc A ở đầu và B ở vị trí thứ hai, bốn người khác xếp tự do, có bốn giai thừa hàng. Lấy bảy trăm hai mươi trừ một trăm hai mươi, trừ hai trăm bốn mươi rồi cộng hai mươi bốn, được ba trăm tám mươi tư.

**Trên màn hình:** Sáu người: A không đứng đầu, AB không kề. | Tổng 720; A đầu 120; AB kề 240. | Giao: A đầu và B thứ hai có 24.
**Ghi nhớ:** ĐÁP SỐ 384 CÁCH HỢP LỆ.


## 04 · MÃ PIN CÓ CHỮ SỐ LẶP

### Nhịp 19 · 06:57 · PIN KHÔNG PHẢI SỐ TỰ NHIÊN

Một mã PIN gồm đúng bốn vị trí từ không đến chín. Mã 0007 vẫn khác mã 0070, và cả hai đều hợp lệ nếu đề không cấm. Đây là dãy có thứ tự, được lặp và chữ số đầu bằng không vẫn được chấp nhận. Vì mỗi vị trí có mười lựa chọn, toàn bộ không gian mẫu gồm mười nghìn mã. Ta muốn tìm những mã có ít nhất một chữ số được sử dụng nhiều lần.

**Trên màn hình:** Mã PIN có đúng bốn chữ số. | Chữ số đầu có thể bằng 0. | Các chữ số được phép lặp.
**Ghi nhớ:** MÃ 0007 VẪN LÀ MỘT MÃ HỢP LỆ.

### Nhịp 20 · 07:20 · THẾ NÀO LÀ CÓ LẶP

Điều kiện có ít nhất một chữ số lặp khá rộng. Có mã lặp đúng hai lần, có mã lặp ba lần, có mã gồm hai cặp và có cả bốn chữ số giống nhau. Thay vì phân chia hết những dạng này, ta đếm phần bù: cả bốn chữ số đôi một khác nhau. Khi xếp lần lượt, mỗi chữ số đã chọn sẽ không được dùng thêm một lần nữa.

**Trên màn hình:** Có lặp: tồn tại hai vị trí cùng chữ số. | Không lặp: cả bốn chữ số phân biệt. | Đếm không lặp dễ hơn đếm có lặp.
**Ghi nhớ:** PHẦN BÙ KHÔNG LẶP LÀ MỘT CHỈNH HỢP.

### Nhịp 21 · 07:43 · ĐẾM MÃ KHÔNG LẶP

Một mã không lặp có mười lựa chọn ở vị trí đầu, còn chín ở vị trí thứ hai, tám ở vị trí thứ ba và bảy ở vị trí cuối. Số mã không lặp là mười nhân chín nhân tám nhân bảy, bằng năm nghìn không trăm bốn mươi. Chúng ta vẫn cho phép chọn chữ số không ở vị trí đầu. Nếu chỉ cho chín lựa chọn ở vị trí đầu, ta đã lẫn sang một bài toán khác.

**Trên màn hình:** Vị trí một: 10 khả năng. | Tiếp theo: 9, rồi 8, rồi 7. | Có 5.040 mã không lặp.
**Ghi nhớ:** KHÔNG LOẠI CHỮ SỐ 0 Ở VỊ TRÍ ĐẦU.

### Nhịp 22 · 08:07 · TÌM MÃ CÓ LẶP

Lấy toàn bộ mười nghìn mã trừ đi năm nghìn không trăm bốn mươi mã không lặp, ta được bốn nghìn chín trăm sáu mươi mã có ít nhất một chữ số lặp. Phương pháp phần bù tự động bao gồm mọi kiểu lặp, dù một cặp hay nhiều cặp. Nó tránh tình trạng một mã như 1122 có thể bị tính trùng nếu ta chọn tùy tiện cặp chữ số giống nhau.

**Trên màn hình:** Tổng 10.000 mã. | Không lặp 5.040 mã. | Có ít nhất một lặp: 4.960 mã.
**Ghi nhớ:** CHỈ TRỪ MỘT LẦN TẬP KHÔNG LẶP.

### Nhịp 23 · 08:30 · NẾU LÀ SỐ CÓ BỐN CHỮ SỐ

Nếu đề chuyển thành số tự nhiên có bốn chữ số, chữ số đầu không thể bằng không. Khi đó toàn bộ chỉ có chín nghìn số. Để các chữ số phân biệt, chọn chữ số đầu trong chín chữ số từ một đến chín, chữ số tiếp theo trong chín chữ số còn lại gồm cả không, rồi tám và bảy. Có bốn nghìn năm trăm ba mươi sáu số không lặp. Vậy có bốn nghìn bốn trăm sáu mươi tư số lặp.

**Trên màn hình:** Chữ số đầu khác 0. | Tất cả 9·10³ = 9.000 số. | Không lặp 9·9·8·7 = 4.536.
**Ghi nhớ:** CÓ LẶP: 9.000 − 4.536 = 4.464.

### Nhịp 24 · 08:53 · SO SÁNH VÀ GHI NHỚ

Kết luận, hai bài toán chỉ khác một điều kiện về chữ số đầu nhưng đáp số khác nhau. Với mã PIN, đáp án là bốn nghìn chín trăm sáu mươi; với số tự nhiên có bốn chữ số, đáp án là bốn nghìn bốn trăm sáu mươi tư. Cả hai đều dùng phần bù của không lặp, song số phần tử của toàn bộ không gian mẫu thay đổi. Bởi vậy phải xác định tập tất cả thật chính xác trước mọi phép tính.

**Trên màn hình:** PIN: cho phép 0 ở đầu → 4.960. | Số bốn chữ số: cấm 0 ở đầu → 4.464. | Hai bài cùng phương pháp, khác tổng thể.
**Ghi nhớ:** XÁC ĐỊNH TẬP TẤT CẢ TRƯỚC KHI TRỪ.


## 05 · HOÁN VỊ KHÔNG ĐIỂM CỐ ĐỊNH

### Nhịp 25 · 09:16 · THƯ ĐÚNG PHONG BÌ

Một tình huống cổ điển: có bốn lá thư phân biệt và bốn phong bì có tên tương ứng. Ta bỏ ngẫu nhiên mỗi lá vào đúng một phong bì khác nhau, nhưng yêu cầu không lá nào vào đúng phong bì của chính nó. Nếu gọi một kết quả là một hoán vị, vị trí đứng đúng của một lá thư được gọi là điểm cố định. Đề đang yêu cầu số hoán vị không có bất kỳ điểm cố định nào.

**Trên màn hình:** Có bốn lá thư A, B, C, D. | Có bốn phong bì tương ứng. | Không lá thư nào vào đúng phong bì.
**Ghi nhớ:** ĐÂY LÀ HOÁN VỊ KHÔNG ĐIỂM CỐ ĐỊNH.

### Nhịp 26 · 09:39 · CÁC TẬP VI PHẠM

Hãy định nghĩa tập E A là những hoán vị mà thư A nằm đúng phong bì A. Ta có bốn tập tương tự. Hoán vị hợp lệ là những hoán vị nằm ngoài hợp của cả bốn tập này. Nếu chỉ trừ mỗi tập riêng thì một cách bỏ thư có hai lá đúng sẽ bị trừ hai lần. Vì vậy từ phương pháp phần bù, ta cần thêm nguyên lý bao hàm–loại trừ để xử lý các phần giao.

**Trên màn hình:** E_A: thư A vào đúng phong bì A. | Tương tự E_B, E_C, E_D. | Yêu cầu nằm ngoài hợp bốn tập.
**Ghi nhớ:** KHÔNG THỂ CHỈ LẤY 24 TRỪ 4·3!.

### Nhịp 27 · 10:03 · ĐẾM TẬP ĐƠN VÀ GIAO ĐÔI

Mỗi tập buộc một lá thư vào đúng phong bì, còn ba lá khác có ba giai thừa cách xếp, nên mỗi tập có sáu phần tử. Có bốn tập đơn, tổng là hai mươi bốn. Nếu hai lá thư được cố định đồng thời, có hai giai thừa cách xếp hai lá còn lại. Có tổ hợp chập hai của bốn cách chọn cặp, tức sáu phần giao đôi; tổng số phải cộng lại là mười hai.

**Trên màn hình:** Một lá cố định: 3! cách. | Chọn 2 lá đúng: 6 cách chọn. | Hai lá đúng chỉ còn 2! cách xếp.
**Ghi nhớ:** CỘNG LẠI CÁC PHẦN GIAO ĐÔI.

### Nhịp 28 · 10:26 · HOÀN THÀNH BAO HÀM–LOẠI TRỪ

Khi ba lá vào đúng vị trí, lá thứ tư buộc phải đúng, nhưng vẫn cần ghi số phần giao của ba tập theo công thức: bốn cách chọn bộ ba và một giai thừa cách. Sau đó phần giao cả bốn tập có đúng một cách. Ta lấy hai mươi bốn trừ hai mươi bốn, cộng mười hai, trừ bốn, cộng một, cuối cùng được chín. Dấu cộng trừ luân phiên có ý nghĩa khôi phục đúng số lần bị trừ trùng.

**Trên màn hình:** Giao ba tập: C₃⁴·1!. | Giao bốn tập: 1 cách. | D₄ = 24−24+12−4+1 = 9.
**Ghi nhớ:** CHỈ CÒN 9 HOÁN VỊ KHÔNG ĐIỂM CỐ ĐỊNH.

### Nhịp 29 · 10:49 · TỔNG QUÁT SỐ HOÁN VỊ LỆCH

Tổng quát cho n lá thư, chọn k lá buộc vào đúng phong bì rồi xếp n trừ k lá còn lại có n trừ k giai thừa cách. Cộng luân phiên theo nguyên lý bao hàm–loại trừ ta nhận được số hoán vị lệch D n bằng n giai thừa nhân tổng các số âm dương một chia k giai thừa, từ k bằng không tới n. Đây là một kết quả sâu bắt nguồn trực tiếp từ tư duy phần bù.

**Trên màn hình:** n lá thư, n phong bì khác nhau. | Không lá nào đặt đúng. | Dₙ = n!·(1−1/1!+1/2!−…).
**Ghi nhớ:** HIỂU CÔNG THỨC QUA CÁC TẬP PHẦN BÙ.

### Nhịp 30 · 11:12 · LƯU Ý CÁC LOẠI ĐÚNG VỊ TRÍ

Trong trường hợp bốn lá thư, không lá nào đúng có chín cách. Nếu yêu cầu đúng đúng một lá, chọn lá cố định rồi ba lá còn lại hoán vị lệch, được bốn nhân hai, bằng tám. Đúng cả bốn lá có một cách. Đặc biệt không thể đúng đúng ba lá mà lá còn lại lại sai, bởi vị trí cuối đã bị ép phải khớp. Những kiểm tra như vậy giúp phát hiện lỗi logic khi chia trường hợp.

**Trên màn hình:** Bốn thư: không đúng vị trí có 9. | Đúng đúng một vị trí có 8. | Đúng cả bốn có đúng 1 cách.
**Ghi nhớ:** ĐÚNG BA VỊ TRÍ NHƯNG SAI MỘT LÀ BẤT KHẢ.


## 06 · DÃY NHỊ PHÂN CHỨA 11

### Nhịp 31 · 11:36 · DÃY NHỊ PHÂN DÀI SÁU

Xét tất cả các dãy nhị phân dài sáu. Một dãy có thể chứa một hoặc nhiều cặp số một đứng liền nhau, chẳng hạn 110110. Nếu đếm trực tiếp theo vị trí cặp đầu tiên, những dãy có nhiều cặp sẽ dễ bị tính lại. Thay vào đó hãy đếm phần bù: những dãy hoàn toàn không chứa hai số một liên tiếp. Từ đó ta dùng phép trừ trên tổng hai mũ sáu dãy.

**Trên màn hình:** Mỗi vị trí là 0 hoặc 1. | Dãy dài sáu, có xét thứ tự. | Yêu cầu xuất hiện 11 liền nhau.
**Ghi nhớ:** TÌM PHẦN BÙ: KHÔNG CHỨA 11.

### Nhịp 32 · 11:59 · PHÂN LOẠI DÃY TRÁNH 11

Gọi f n là số dãy nhị phân dài n không có hai số một liền nhau. Một dãy hợp lệ hoặc bắt đầu bằng số không, sau đó còn một dãy hợp lệ dài n trừ một, hoặc bắt đầu bằng một rồi bắt buộc đến không, sau đó còn một dãy hợp lệ dài n trừ hai. Hai dạng đầu này khác nhau nên chúng rời nhau và bao phủ mọi dãy hợp lệ. Đây là nguồn gốc của truy hồi Fibonacci.

**Trên màn hình:** Gọi fₙ là số dãy dài n tránh 11. | Nếu bắt đầu bằng 0: còn n−1 vị trí. | Nếu bắt đầu bằng 10: còn n−2 vị trí.
**Ghi nhớ:** HAI NHÓM MỞ ĐẦU RỜI NHAU.

### Nhịp 33 · 12:22 · ĐIỀU KIỆN ĐẦU CHO TRUY HỒI

Để áp dụng hệ thức truy hồi, ta cần hai giá trị đầu. Với độ dài bằng không, chỉ có một dãy rỗng, nên f không bằng một. Với độ dài bằng một, có hai dãy 0 và 1, đều không chứa 11, nên f một bằng hai. Từ đó f hai bằng ba, rồi f ba bằng năm. Việc đếm một dãy rỗng là một cách là quy ước tự nhiên và nhất quán với phép nối thêm ký hiệu.

**Trên màn hình:** Dãy rỗng: một khả năng. | Dãy dài một: 0 hoặc 1. | Vậy f₀=1, f₁=2.
**Ghi nhớ:** DÙNG ĐÚNG GIÁ TRỊ KHỞI ĐẦU.

### Nhịp 34 · 12:45 · TÍNH ĐẾN ĐỘ DÀI SÁU

Lần lượt cộng hai giá trị liền trước, ta được f hai bằng ba, f ba bằng năm, f bốn bằng tám, f năm bằng mười ba và f sáu bằng hai mươi mốt. Nghĩa là trong sáu mươi tư dãy nhị phân dài sáu có đúng hai mươi mốt dãy tránh hoàn toàn mẫu 11. Mỗi dãy được phân vào một trong hai nhóm bắt đầu bằng 0 hoặc 10, nên truy hồi không bỏ sót và không tính trùng.

**Trên màn hình:** f₂=3, f₃=5, f₄=8. | f₅=13, f₆=21. | Có 21 dãy không chứa 11.
**Ghi nhớ:** PHẦN BÙ ĐƯỢC ĐẾM BẰNG TRUY HỒI.

### Nhịp 35 · 13:08 · LẤY PHẦN BÙ ĐỂ KẾT LUẬN

Kết quả bài toán bằng sáu mươi tư trừ hai mươi mốt, tức bốn mươi ba dãy có ít nhất một cặp 11 liên tiếp. Một dãy như 111111 có đến năm cặp 11 chồng lấn nhưng vẫn chỉ là một dãy. Đây là lợi ích của phần bù: ta không cần kiểm soát số lần xuất hiện của mẫu bị yêu cầu, chỉ cần biết dãy có tránh mẫu hoàn toàn hay không.

**Trên màn hình:** Toàn bộ: 64 dãy. | Không có 11: 21 dãy. | Có ít nhất một 11: 43 dãy.
**Ghi nhớ:** NHIỀU CẶP 11 VẪN CHỈ ĐẾM MỘT DÃY.

### Nhịp 36 · 13:32 · KẾT NỐI BÀI TOÁN TRÁNH MẪU

Kỹ thuật này còn áp dụng cho các bài tìm chuỗi xuất hiện một mẫu con, xếp vật không có hai đối tượng giống nhau đứng liền và nhiều bài tổ hợp về trạng thái. Nhưng không nên thuộc lòng dãy Fibonacci rồi gắn vào mọi bài. Phải giải thích tại sao các dãy tránh mẫu tách đúng thành hai dạng, và xác định rõ giá trị khởi đầu. Khi đó phép trừ tổng trừ phần bù mới có cơ sở toán học.

**Trên màn hình:** Đếm mẫu bị cấm thường dễ hơn. | Phần bù có thể đếm bằng truy hồi. | Đếm thỏa = tổng − số tránh.
**Ghi nhớ:** ĐỪNG DÙNG TRUY HỒI KHI CHƯA GIẢI THÍCH.


## 07 · ÍT NHẤT MỘT TRONG HAI NGƯỜI

### Nhịp 37 · 13:55 · ÍT NHẤT A HOẶC B

Có tám học sinh phân biệt và ta cần chọn một đội gồm ba bạn. Đội phải chứa ít nhất một trong hai bạn A, B; nghĩa là có A, hoặc có B, hoặc cả hai. Nếu dùng từ hoặc theo nghĩa bao gồm, hai bạn cùng xuất hiện vẫn hợp lệ. Phần bù của điều kiện là đội không có A lẫn B, tức cả ba thành viên đều thuộc sáu bạn còn lại.

**Trên màn hình:** Có tám học sinh A đến H. | Chọn đội ba người, không phân vai. | Đội phải có A hoặc B hoặc cả hai.
**Ghi nhớ:** PHẦN BÙ: KHÔNG CÓ CẢ A LẪN B.

### Nhịp 38 · 14:18 · CHỌN ĐỘI KHÔNG CÓ A B

Những đội sai điều kiện phải không chứa bất kỳ ai trong hai bạn A và B. Vì vậy ta chỉ chọn ba trong sáu bạn C, D, E, F, G, H, được hai mươi nhóm. Đội có A nhưng không B không nằm trong nhóm bị loại; đội có B mà không A cũng không. Đội chứa cả hai cũng hoàn toàn hợp lệ. Vùng đỏ trên hình minh họa đúng các nhóm hoàn toàn vắng A và B.

**Trên màn hình:** Bỏ A và B khỏi danh sách. | Chỉ chọn trong sáu người khác. | Có C₃⁶ = 20 nhóm bị loại.
**Ghi nhớ:** ĐẾM PHẦN BÙ KHÔNG GIAO NHAU.

### Nhịp 39 · 14:41 · ĐÁP SỐ ÍT NHẤT MỘT

Kết quả là năm mươi sáu trừ hai mươi bằng ba mươi sáu. Ta không phải chia ba trường hợp trước khi tính mà vẫn bao phủ đầy đủ những đội có A, có B và có cả hai. Sau đó có thể kiểm tra bằng cách chia lại thành đúng một trong hai bạn hoặc có cả hai. Hai tập hợp ấy rời nhau và cộng lại phải bằng ba mươi sáu.

**Trên màn hình:** Toàn bộ C₃⁸ = 56 đội. | Loại C₃⁶ = 20 đội. | Hợp lệ 36 đội.
**Ghi nhớ:** CÓ THỂ GỒM A, B HOẶC CẢ HAI.

### Nhịp 40 · 15:04 · ĐÚNG MỘT TRONG HAI

Điều kiện đúng một trong hai bạn A và B yêu cầu chỉ xuất hiện A hoặc chỉ xuất hiện B, không bao giờ có cả hai. Ta chọn người đặc biệt theo hai cách, rồi chọn hai người còn lại từ sáu học sinh khác, được hai nhân tổ hợp chập hai của sáu, bằng ba mươi nhóm. So sánh với ba mươi sáu ở câu trước, số nhóm bị loại thêm chính là những nhóm chứa đồng thời A và B.

**Trên màn hình:** Chọn một trong A, B: 2 cách. | Chọn hai trong sáu bạn còn lại. | Có 2·C₂⁶ = 30 đội.
**Ghi nhớ:** ĐÚNG MỘT KHÁC ÍT NHẤT MỘT.

### Nhịp 41 · 15:28 · CÓ ĐỒNG THỜI CẢ A VÀ B

Khi đội bắt buộc có cả A và B, hai thành viên đã được xác định. Thành viên thứ ba có sáu cách chọn trong những bạn còn lại. Vì vậy có sáu nhóm chứa cả hai. Ghép với ba mươi nhóm chỉ có đúng một trong hai, ta trở lại ba mươi sáu nhóm có ít nhất một. Đây là một phép kiểm chứng rất tốt vì ba trường hợp của từ hoặc đã được phân chia chính xác.

**Trên màn hình:** Hai vị trí đã là A và B. | Chọn người thứ ba trong sáu. | Có đúng 6 đội.
**Ghi nhớ:** 36 = 30 + 6 XÁC NHẬN KHÔNG ĐẾM TRÙNG.

### Nhịp 42 · 15:51 · TỔNG QUÁT VỚI NHIỀU NGƯỜI

Với n học sinh và r bạn được đánh dấu đặc biệt, chọn k người có ít nhất một trong r bạn. Ta luôn có thể đếm phần bù bằng cách bỏ toàn bộ r người đặc biệt rồi chọn k người trong n trừ r người còn lại. Công thức vì thế là tổ hợp chập k của n trừ tổ hợp chập k của n trừ r. Đây là cùng cấu trúc với bài có ít nhất một nữ ở chương trước.

**Trên màn hình:** n người, r người được đánh dấu. | Chọn k người, ít nhất một được đánh dấu. | Tổng trừ nhóm chỉ chọn ngoài r người.
**Ghi nhớ:** CÔNG THỨC KHÔNG PHỤ THUỘC PHÂN CHIA SỐ ĐẶC BIỆT.


## 08 · THỬ THÁCH TỔNG HỢP

### Nhịp 43 · 16:14 · THỬ THÁCH CUỐI VIDEO

Bài tổng hợp cuối tập kết hợp hai điều kiện. Từ tám học sinh, ta chọn đội bốn người và chỉ định một đội trưởng thuộc đội. Đội phải chứa ít nhất một trong A, B, nhưng đội trưởng không được là A. Vì có chức vụ, một đội cố định có thể tạo ra nhiều kết quả khác nhau theo người làm đội trưởng. Ta sẽ giải bằng hai phương pháp độc lập để kiểm chứng.

**Trên màn hình:** Tám học sinh A, B, C, D, E, F, G, H. | Chọn bốn người; chỉ định một đội trưởng. | Có A hoặc B; đội trưởng không là A.
**Ghi nhớ:** PHẢI ĐẾM CẢ NHÓM VÀ CHỨC VỤ.

### Nhịp 44 · 16:37 · BẮT ĐẦU TỪ TẤT CẢ

Khi chưa có điều kiện, chọn bốn trong tám học sinh có bảy mươi đội khác nhau. Với mỗi đội, ta có bốn cách chọn đội trưởng, nên số kết quả là hai trăm tám mươi. Chú ý nếu chỉ lấy bảy mươi thì ta đang quên vai trò đội trưởng. Ngược lại, nếu dùng chỉnh hợp chập bốn của tám thì ta đã sắp thứ tự cả bốn người, thừa những thứ tự không được đề phân biệt.

**Trên màn hình:** Có C₄⁸ = 70 đội. | Mỗi đội có 4 cách chọn trưởng. | Toàn bộ 280 kết quả.
**Ghi nhớ:** ĐỐI TƯỢNG ĐẾM LÀ ĐỘI KÈM ĐỘI TRƯỞNG.

### Nhịp 45 · 17:00 · LOẠI ĐỘI KHÔNG A KHÔNG B

Nhóm kết quả bị loại thứ nhất là những đội không có A và cũng không có B. Khi đó phải chọn bốn trong sáu người còn lại, có mười lăm đội; mỗi đội vẫn có bốn lựa chọn đội trưởng, nên có sáu mươi kết quả vi phạm. Ta đã xác định phần bù của điều kiện ít nhất một trong A, B. Nhưng vẫn còn điều kiện cấm A làm đội trưởng, cần loại thêm một nhóm kết quả nữa.

**Trên màn hình:** Đội chỉ gồm sáu người C đến H. | Chọn 4 trong 6: 15 đội. | Mỗi đội có 4 đội trưởng → 60.
**Ghi nhớ:** ĐÂY LÀ NHÓM VI PHẠM THỨ NHẤT.

### Nhịp 46 · 17:24 · LOẠI A LÀM ĐỘI TRƯỞNG

Nhóm bị loại thứ hai có A làm đội trưởng. Khi đó A đương nhiên nằm trong đội, và chỉ cần chọn ba thành viên khác từ bảy bạn còn lại, được ba mươi lăm kết quả. Điều thú vị là hai nhóm bị loại hoàn toàn không giao nhau: nhóm không có A, B thì chắc chắn A không thể làm đội trưởng. Nhờ sự rời nhau này, ta được phép trừ sáu mươi và ba mươi lăm trực tiếp mà không cần cộng lại giao.

**Trên màn hình:** A đã được chọn và giữ chức trưởng. | Chọn thêm 3 trong 7 người còn lại. | Có C₃⁷ = 35 kết quả bị cấm.
**Ghi nhớ:** HAI NHÓM VI PHẠM KHÔNG GIAO NHAU.

### Nhịp 47 · 17:47 · TÍNH ĐÁP SỐ BẰNG PHẦN BÙ

Ta lấy toàn bộ hai trăm tám mươi kết quả, trừ sáu mươi kết quả đội không có A cũng không có B, tiếp tục trừ ba mươi lăm kết quả A làm đội trưởng, được một trăm tám mươi lăm. Phép trừ hợp lệ vì hai loại vi phạm không chồng lấn nhau. Nếu có giao, ta phải cộng lại phần giao. Hình minh họa thể hiện rõ hai miền đỏ riêng biệt được loại bỏ khỏi tập tất cả.

**Trên màn hình:** Tất cả: 280 kết quả. | Vi phạm nhóm thiếu A,B: 60. | Vi phạm A làm trưởng: 35.
**Ghi nhớ:** KẾT QUẢ HỢP LỆ LÀ 185.

### Nhịp 48 · 18:10 · KIỂM CHỨNG CÁCH HAI

Giải cách hai bằng cách phân loại đội trưởng. Nếu B làm trưởng, chọn thêm ba trong bảy người khác, có ba mươi lăm kết quả. Nếu đội trưởng thuộc sáu bạn C đến H, ta có sáu cách chọn người trưởng. Sau đó chọn ba người khác trong bảy người còn lại, nhưng phải có ít nhất một trong A và B: lấy tổ hợp chập ba của bảy trừ tổ hợp chập ba của năm, được hai mươi lăm. Vậy tổng là ba mươi lăm cộng sáu nhân hai mươi lăm, bằng một trăm tám mươi lăm.

**Trên màn hình:** Trưởng là B: chọn 3 trong 7 → 35. | Trưởng thuộc C–H: 6 cách chọn. | Ba người thêm phải có A hoặc B: 25.
**Ghi nhớ:** 35 + 6·25 = 185, TRÙNG KHỚP.
