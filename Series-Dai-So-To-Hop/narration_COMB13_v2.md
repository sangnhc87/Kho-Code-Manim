# SANG MATH · COMB13 V2 · PHƯƠNG PHÁP GỘP KHỐI

## Bản thuyết minh đồng bộ

Số nhịp: 48 · 8 chương · TTS=off
Tổng thời lượng dự kiến: 1123.6 giây.
Lời giảng bên dưới là nội dung đầy đủ được đưa vào tổng hợp giọng đọc; không cắt tùy ý.


## 01 · MỘT CẶP KHÔNG ĐƯỢC KỀ

### Nhịp 01 · 00:00 · NÊU BÀI TOÁN

Có năm học sinh A, B, C, D, E phân biệt. Ta muốn xếp thành một hàng, nhưng A và B không được ngồi ở hai vị trí liên tiếp. Nếu chỉ nói năm giai thừa, ta đã tính tất cả các hàng, kể cả những hàng vi phạm. Hãy quan sát các thẻ và đánh dấu chính xác hàng nào có hai bạn A, B đứng cạnh nhau. Khi biết phần bị cấm, ta mới xây dựng cách đếm đáng tin cậy.

**Trên màn hình:** Xếp A, B, C, D, E thành hàng. | A và B không được đứng cạnh nhau. | Đếm số cách xếp hợp lệ.
**Ghi nhớ:** TRƯỚC TIÊN, XÁC ĐỊNH ĐIỀU KIỆN CẤM.

### Nhịp 02 · 00:23 · TẠI SAO KHÔNG THỂ LẤY 5!

Ta thấy trong một số hàng như A B C D E, cặp A B nằm sát nhau, còn ở hàng A C B D E, cặp ấy đã bị tách ra. Vậy quy tắc nhân khi xếp đủ năm người chưa phản ánh điều kiện của đề. Chúng ta phân chia các hàng thành hai nhóm không giao nhau: nhóm A B đứng cạnh và nhóm A B không đứng cạnh. Tổng của hai nhóm luôn là toàn bộ năm giai thừa hàng.

**Trên màn hình:** Một số hàng có AB hoặc BA liền nhau. | Các hàng ấy không hợp lệ. | Vì vậy 5! chỉ là tổng ban đầu.
**Ghi nhớ:** TỔNG KHÁC SỐ CÁCH HỢP LỆ.

### Nhịp 03 · 00:46 · ĐẾM NHÓM BỊ CẤM

Khi A và B đứng cạnh, ta tạm xem chúng như một khối không bị tách. Khối ấy cùng ba người C, D, E tạo ra bốn đối tượng phân biệt để xếp thành hàng, nên có bốn giai thừa khả năng. Nhưng ở bên trong khối, A có thể đứng trước B hoặc B có thể đứng trước A. Vì thế số hàng bị cấm là hai nhân bốn giai thừa, tức bốn mươi tám.

**Trên màn hình:** Gộp A, B thành khối [AB]. | Còn [AB], C, D, E: bốn đối tượng. | Khối có hai thứ tự AB, BA.
**Ghi nhớ:** SỐ HÀNG BỊ CẤM BẰNG 2 × 4!.

### Nhịp 04 · 01:09 · LẤY PHẦN BÙ

Bây giờ ta chỉ cần lấy tổng số hàng trừ những hàng A và B đứng sát nhau. Số cách thỏa yêu cầu bằng một trăm hai mươi trừ bốn mươi tám, bằng bảy mươi hai. Không có hàng nào bị bỏ sót vì mỗi hàng hoặc thuộc nhóm hợp lệ, hoặc thuộc nhóm bị cấm. Cũng không có hàng nào bị trừ hai lần vì hai nhóm được xác định bằng một điều kiện đối lập duy nhất.

**Trên màn hình:** Tất cả có 120 cách. | Số cách A, B đứng cạnh là 48. | Số cách không đứng cạnh: 72.
**Ghi nhớ:** BÀI TOÁN ĐƯỢC GIẢI BẰNG PHẦN BÙ.

### Nhịp 05 · 01:33 · KIỂM CHỨNG BẰNG LIỆT KÊ

Để kiểm tra, chương trình có thể liệt kê tất cả một trăm hai mươi hoán vị và xem hai vị trí A, B có chênh nhau đúng một hay không. Sau khi loại bốn mươi tám hàng vi phạm, ta còn đúng bảy mươi hai. Cách thử nhỏ này rất hữu ích để bắt lỗi công thức. Nhưng khi số người lớn, không thể liệt kê tất cả; ta vẫn phải nắm được chứng minh bằng phép đếm phần bù.

**Trên màn hình:** Tạo đủ 120 hoán vị của 5 người. | Đánh dấu mọi hàng có |pos(A)-pos(B)|=1. | Đếm còn đúng 72 hàng.
**Ghi nhớ:** LIỆT KÊ LÀ KIỂM THỬ, KHÔNG THAY CHỨNG MINH.

### Nhịp 06 · 01:56 · TỔNG QUÁT CHO n NGƯỜI

Với n người phân biệt, tổng số cách xếp là n giai thừa. Nếu hai người cụ thể bắt buộc đứng cạnh, ta gộp thành một khối, có hai nhân n trừ một giai thừa cách. Vậy khi hai người ấy không được đứng cạnh, số cách là n giai thừa trừ hai nhân n trừ một giai thừa. Công thức này dùng cho một hàng thẳng và đúng một cặp chỉ định; nếu có nhiều cặp cấm, phải xét giao nhau giữa các điều kiện.

**Trên màn hình:** Có n người phân biệt, n ≥ 2. | A, B là hai người chỉ định. | Số cách hợp lệ: n! - 2(n-1)!.
**Ghi nhớ:** PHẢI CHẮC CHẮN CHỈ CẤM MỘT CẶP.


## 02 · PHƯƠNG PHÁP KHOẢNG TRỐNG

### Nhịp 07 · 02:19 · XẾP NGƯỜI KHÁC TRƯỚC

Thay vì đếm phần bù, ta sẽ trực tiếp tạo ra những cách xếp hợp lệ. Hãy bỏ A và B ra ngoài một lúc, rồi xếp C, D, E trước. Có ba giai thừa, tức sáu hàng nền khác nhau. Từ một hàng nền cụ thể như C D E, hãy nhìn kỹ những vị trí có thể cài thêm A hoặc B. Cách tạo hàng nền này bảo đảm rằng những khoảng trống đều độc lập với vị trí của A và B.

**Trên màn hình:** Giữ nguyên bài toán 5 người. | Xếp C, D, E trước. | Có 3! cách tạo hàng nền.
**Ghi nhớ:** KHOẢNG TRỐNG XUẤT HIỆN TỪ HÀNG NỀN.

### Nhịp 08 · 02:43 · BỐN KHOẢNG AN TOÀN

Sau khi xếp ba bạn C, D, E thành một hàng, xuất hiện bốn khoảng: trước C, giữa C và D, giữa D và E, và sau E. Nếu đặt A và B vào hai khoảng khác nhau, giữa họ chắc chắn có ít nhất một người thuộc hàng nền. Vì thế hai bạn không thể đứng cạnh. Nếu đặt cả hai vào cùng một khoảng, họ sẽ liền nhau. Điều kiện cấm được chuyển thành điều kiện chọn các khoảng khác nhau.

**Trên màn hình:** Hàng nền: C  D  E. | Các khoảng: _ C _ D _ E _. | Có tất cả 4 khoảng.
**Ghi nhớ:** CHỌN HAI KHOẢNG KHÁC NHAU.

### Nhịp 09 · 03:06 · CHỌN VỊ TRÍ CHO A VÀ B

Trước tiên, ta chọn ra hai khoảng khác nhau trong bốn khoảng an toàn. Lúc này hai khoảng chỉ là một nhóm gồm hai vị trí, chưa nói A sẽ vào khoảng nào. Vì vậy số cách chọn khoảng là tổ hợp chập hai của bốn, bằng sáu. Ký hiệu trên màn hình dùng n ở chỉ số trên và k ở dưới theo chuẩn trình bày đã thống nhất cho cả Series. Bước tiếp theo mới quyết định thứ tự đặt A, B.

**Trên màn hình:** Chọn hai trong bốn khoảng. | Không xét thứ tự khi chọn khoảng. | Có C trên 4 dưới 2 = 6 cách.
**Ghi nhớ:** LÚC CHỌN KHOẢNG CHƯA PHÂN CÔNG A, B.

### Nhịp 10 · 03:29 · HOÁN ĐỔI A VÀ B

Với hai khoảng đã được lựa chọn, ta có thể đặt A vào khoảng thứ nhất và B vào khoảng thứ hai, hoặc đổi ngược lại. Đó là hai giai thừa cách phân công. Nhân với sáu cách xếp hàng nền và sáu cách chọn cặp khoảng, ta thu được bảy mươi hai. Mỗi hàng hợp lệ cho biết duy nhất hàng nền sau khi xóa A, B, hai khoảng được chọn và người được đặt vào từng khoảng. Vậy phép đếm không bị trùng.

**Trên màn hình:** Mỗi cặp khoảng đã chọn có 2! cách. | A ở khoảng trước hoặc khoảng sau. | Tổng: 3! × 6 × 2! = 72.
**Ghi nhớ:** MỖI HÀNG HỢP LỆ ĐƯỢC TẠO ĐÚNG MỘT LẦN.

### Nhịp 11 · 03:52 · SO SÁNH HAI CÁCH GIẢI

Cùng một bài toán, hai phương pháp cho cùng bảy mươi hai cách. Phương pháp phần bù thuận lợi khi chỉ cấm một cặp, vì đếm nhóm bị cấm rất đơn giản. Phương pháp khoảng trống lại cho chúng ta một cách dựng trực tiếp từng hàng hợp lệ, đặc biệt mạnh khi có nhiều người thuộc một nhóm không được đứng cạnh nhau. Sự trùng khớp của hai kết quả không phải ngẫu nhiên: cả hai đều đếm chính một tập hợp.

**Trên màn hình:** Cách 1: 5! - 2·4!. | Cách 2: 3!·C trên 4 dưới 2·2!. | Cả hai đều cho 72.
**Ghi nhớ:** ĐẾM BÙ VÀ CHỌN KHOẢNG BỔ SUNG CHO NHAU.

### Nhịp 12 · 04:15 · DẤU HIỆU NHẬN RA KHOẢNG TRỐNG

Khi đề bài nói các bạn nữ không được đứng cạnh nhau, hoặc các chữ A không được liên tiếp, hãy nghĩ đến phương pháp khoảng trống. Ta thường xếp nhóm còn lại trước để tạo các khe trống. Sau đó chọn các khe khác nhau cho những phần tử cần tách nhau. Cần chú ý hai điều: các phần tử trong mỗi nhóm có phân biệt hay không, và số khoảng có đủ để đặt tất cả phần tử đặc biệt hay không.

**Trên màn hình:** Có một nhóm cần tách nhau ra. | Có một nhóm khác dùng làm ngăn cách. | Hãy xếp nhóm ngăn cách trước.
**Ghi nhớ:** SỐ KHOẢNG BẰNG SỐ VẬT NỀN CỘNG MỘT.


## 03 · CÁC VỊ TRÍ KHÔNG LIỀN NHAU

### Nhịp 13 · 04:39 · BỐN CHỮ A VÀ NĂM CHỮ B

Chúng ta xét chín vị trí, chứa bốn chữ A giống nhau và năm chữ B giống nhau, với điều kiện không xuất hiện hai A liên tiếp. Khác với bài xếp học sinh, việc đổi hai chữ A cho nhau không tạo một dãy mới. Nếu dùng thừa bốn giai thừa để nhân, kết quả sẽ bị sai. Đây là cơ hội để gắn kỹ thuật khoảng trống với những điều đã học về hoán vị có phần tử giống nhau.

**Trên màn hình:** Xếp bốn A giống hệt và năm B giống hệt. | Không có hai A nào liên tiếp. | Cần đếm số dãy khác nhau.
**Ghi nhớ:** CHỮ GIỐNG NHAU KHÔNG ĐƯỢC HOÁN ĐỔI THÀNH CÁCH MỚI.

### Nhịp 14 · 05:03 · TẠO SÁU KHOẢNG TỪ NĂM B

Vì năm chữ B giống nhau, hàng nền của chúng chỉ có một cách. Trước, giữa và sau năm B xuất hiện đúng sáu khoảng trống. Đặt bốn chữ A vào bốn khoảng khác nhau thì không có hai A nằm sát nhau. Ngược lại, mọi dãy hợp lệ đều cho thấy bốn chữ A chiếm bốn khoảng riêng biệt của hàng B. Do đó ta đã lập được một tương ứng một-một giữa các dãy hợp lệ và các tập con bốn khoảng.

**Trên màn hình:** Xếp năm B trước: B B B B B. | Có sáu khoảng đặt A. | Mỗi khoảng nhận tối đa một A.
**Ghi nhớ:** KHOẢNG TRỐNG TỰ ĐỘNG ĐẢM BẢO KHÔNG KỀ.

### Nhịp 15 · 05:26 · CHỌN BỐN TRONG SÁU KHOẢNG

Ta chỉ cần chọn bốn khoảng trong sáu khoảng có sẵn. Vì mọi chữ A đều như nhau, khi đã biết bốn khoảng, dãy được xác định duy nhất. Không có bước hoán vị bốn chữ A. Vậy số dãy bằng tổ hợp chập bốn của sáu, tức mười lăm. Đây là điểm khác biệt quan trọng với bài xếp bốn học sinh nữ phân biệt vào bốn khoảng, khi đó còn phải nhân bốn giai thừa.

**Trên màn hình:** Chọn 4 khoảng khác nhau trong 6. | Các chữ A giống nhau, không cần 4!. | Kết quả bằng tổ hợp 4 của 6.
**Ghi nhớ:** ĐẾM CHÍNH XÁC 15 DÃY.

### Nhịp 16 · 05:49 · CHỌN VỊ TRÍ KHÔNG LIỀN NHAU

Ta tổng quát hóa bằng cách chọn k vị trí trong n vị trí sao cho không có hai vị trí nào liền nhau. Viết các vị trí theo thứ tự tăng dần, mỗi vị trí sau phải cách vị trí trước ít nhất hai đơn vị. Hãy tạo một dãy vị trí mới: lấy vị trí thứ r trừ đi r trừ một. Như vậy mỗi khoảng trống bắt buộc giữa hai vị trí được nén lại, và dãy mới chỉ còn yêu cầu tăng nghiêm ngặt.

**Trên màn hình:** Chọn k vị trí 1 ≤ i1 < ... < ik ≤ n. | Điều kiện: i(j+1) ≥ i(j)+2. | Đặt j(r)=i(r)-(r-1).
**Ghi nhớ:** DỊCH CHỈ SỐ ĐỂ BỎ KHOẢNG CÁCH BẮT BUỘC.

### Nhịp 17 · 06:12 · SUY RA CÔNG THỨC TỔNG QUÁT

Phép dịch làm vị trí cuối cùng không vượt quá n trừ k cộng một, trong khi các vị trí mới tăng nghiêm ngặt như cách chọn một tập con bình thường. Vì vậy số cách chọn k vị trí không kề nhau bằng tổ hợp chập k của n trừ k cộng một. Điều kiện tồn tại là n ít nhất bằng hai k trừ một, vì phải dành ra k vị trí được chọn cùng k trừ một vị trí ngăn cách.

**Trên màn hình:** Sau phép dịch: 1 ≤ j1 < ... < jk ≤ n-k+1. | Chọn k số trong n-k+1 số. | Số cách: C dưới k trên n-k+1.
**Ghi nhớ:** NẾU n < 2k-1 THÌ KHÔNG CÓ CÁCH NÀO.

### Nhịp 18 · 06:35 · NẾU HAI NHÓM ĐỀU PHÂN BIỆT

Nếu thay năm chữ B bằng năm học sinh nam phân biệt và bốn chữ A bằng bốn học sinh nữ phân biệt, cách đếm phải thay đổi. Ta có năm giai thừa cách xếp nam, mười lăm cách chọn bốn trong sáu khoảng và bốn giai thừa cách phân công bốn nữ vào các khoảng. Kết quả là bốn mươi ba nghìn hai trăm. Như vậy cùng một sơ đồ khoảng trống, yếu tố các phần tử có phân biệt hay không quyết định những thừa số cuối cùng.

**Trên màn hình:** Có năm người B và bốn người A khác nhau. | Xếp năm B: 5!; chọn bốn khoảng: 15. | Xếp bốn A vào bốn khoảng: 4!.
**Ghi nhớ:** KHÔNG ĐƯỢC QUÊN HOÁN VỊ NỘI BỘ NHÓM.


## 04 · HAI CẶP CẤM ĐỨNG CẠNH

### Nhịp 19 · 06:59 · HAI CẶP ĐỀU BỊ CẤM

Ta xét sáu học sinh phân biệt, yêu cầu A không đứng cạnh B và đồng thời C không đứng cạnh D. Nếu chỉ trừ số hàng vi phạm cặp AB và trừ tiếp số hàng vi phạm cặp CD, ta có nguy cơ trừ hai lần những hàng mà cả hai cặp đều đứng cạnh nhau. Vì vậy ta sẽ gọi hai tập hợp điều kiện vi phạm là E một và E hai, rồi xử lý đúng phần giao giữa chúng.

**Trên màn hình:** Có sáu người A, B, C, D, E, F. | AB không kề và CD không kề. | Đếm số hàng hợp lệ.
**Ghi nhớ:** HAI ĐIỀU KIỆN CẤM CẦN XÉT PHẦN GIAO.

### Nhịp 20 · 07:23 · ĐẾM TỪNG CẶP VI PHẠM

Trong sáu người, nếu bắt buộc AB đứng cạnh thì ta gộp AB thành một khối, cùng bốn người còn lại tạo năm đối tượng. Hai cách sắp nội bộ của khối nhân năm giai thừa cho hai trăm bốn mươi hàng. Tương tự với CD, ta cũng được hai trăm bốn mươi. Nhưng các hàng có cả AB và CD đứng kề đang thuộc đồng thời hai tập hợp bị cấm, nên cần tìm phần giao.

**Trên màn hình:** E1: A và B đứng cạnh. | E2: C và D đứng cạnh. | Mỗi tập có 2·5! = 240 hàng.
**Ghi nhớ:** TRỪ RIÊNG TỪNG BIẾN CỐ CHƯA ĐỦ.

### Nhịp 21 · 07:45 · ĐẾM PHẦN GIAO HAI CẶP

Khi AB cùng đứng cạnh và CD cũng đứng cạnh, hai cặp không chung người nên có thể gộp thành hai khối độc lập. Cùng E và F, ta có bốn đối tượng, sắp được bốn giai thừa cách. Bên trong hai khối có hai nhân hai thứ tự. Do đó phần giao của E một và E hai gồm chín mươi sáu hàng, chính là phần đã bị trừ hai lần khi xử lý hai biến cố riêng rẽ.

**Trên màn hình:** E1 ∩ E2: AB và CD cùng kề. | Gộp hai khối [AB], [CD]. | Có 4!·2·2 = 96 hàng.
**Ghi nhớ:** PHẦN GIAO BỊ TRỪ HAI LẦN NÊN PHẢI CỘNG LẠI.

### Nhịp 22 · 08:08 · BAO HÀM - LOẠI TRỪ

Nguyên lý bao hàm loại trừ cho số hàng vi phạm ít nhất một cặp bằng hai trăm bốn mươi cộng hai trăm bốn mươi trừ chín mươi sáu, tức ba trăm tám mươi bốn. Vậy số hàng không vi phạm bất kỳ cặp nào là bảy trăm hai mươi trừ ba trăm tám mươi bốn, bằng ba trăm ba mươi sáu. Ta có thể tô vùng hợp của hai vòng trên sơ đồ để thấy rõ việc trừ phần giao đúng một lần.

**Trên màn hình:** Hợp hai tập cấm có 240+240-96=384. | Lấy 720 trừ 384. | Có 336 hàng thỏa cả hai điều kiện.
**Ghi nhớ:** CỘNG LẠI PHẦN GIAO ĐỂ KHÔNG TRỪ TRÙNG.

### Nhịp 23 · 08:32 · PHÂN BIỆT ĐÚNG MỘT CẶP

Ta thử câu hỏi khác để tránh nhầm lẫn: có bao nhiêu hàng mà đúng một trong hai cặp AB, CD đứng cạnh? Trường hợp AB kề nhưng CD không kề có hai trăm bốn mươi trừ chín mươi sáu, tức một trăm bốn mươi bốn. Trường hợp đối xứng cũng như vậy. Hai trường hợp rời nhau nên cộng được hai trăm tám mươi tám. Kết quả này khác ba trăm tám mươi bốn của điều kiện ít nhất một cặp.

**Trên màn hình:** Đúng một cặp đứng cạnh. | AB kề, CD không kề: 240-96=144. | Đổi hai cặp: cũng 144.
**Ghi nhớ:** ĐÚNG MỘT KHÁC VỚI ÍT NHẤT MỘT.

### Nhịp 24 · 08:55 · KIỂM TRA BẰNG PHÂN HOẠCH

Mọi hàng xếp sáu người đều rơi vào đúng một trong ba nhóm: không có cặp nào đứng cạnh, đúng một cặp đứng cạnh, hoặc cả hai cặp đều đứng cạnh. Ta đã tính được ba trăm ba mươi sáu, hai trăm tám mươi tám và chín mươi sáu. Tổng đúng bằng bảy trăm hai mươi. Kiểm tra phân hoạch như vậy là một công cụ phát hiện lỗi rất hiệu quả, đặc biệt với bài có nhiều biến cố và công thức dài.

**Trên màn hình:** Cả hai cặp cấm: 336 hàng. | Đúng một cặp kề: 288 hàng. | Cả hai cặp kề: 96 hàng.
**Ghi nhớ:** BA NHÓM CỘNG ĐÚNG TỔNG 720.


## 05 · RÀNG BUỘC CÓ CHUNG PHẦN TỬ

### Nhịp 25 · 09:19 · CẶP CẤM CHUNG MỘT NGƯỜI

Bây giờ hai điều kiện cấm không còn rời nhau về đối tượng: cấm A đứng cạnh B và cấm B đứng cạnh C. Chữ B xuất hiện trong cả hai điều kiện. Ta vẫn có thể dùng nguyên lý bao hàm loại trừ, nhưng tuyệt đối không được giả định rằng hai khối AB và BC là hai khối độc lập, vì làm như vậy sẽ đếm người B hai lần. Ta cần quan sát cấu trúc hình học thật của phần giao.

**Trên màn hình:** Vẫn sáu người A, B, C, D, E, F. | Không cho AB đứng cạnh. | Không cho BC đứng cạnh.
**Ghi nhớ:** HAI CẶP CẤM ĐỀU CHỨA B.

### Nhịp 26 · 09:42 · MỖI CẶP VI PHẠM: 240

Số hàng A và B đứng cạnh bằng hai nhân năm giai thừa, tức hai trăm bốn mươi. Số hàng B và C đứng cạnh cũng là hai trăm bốn mươi. Tuy nhiên, muốn cùng thỏa cả hai sự đứng kề, B phải có hai hàng xóm trực tiếp A và C, nghĩa là B nằm ở giữa trong bộ ba liên tiếp. Không thể lấy hai khối riêng [AB] và [BC] rồi hoán đổi độc lập, vì chúng chồng nhau tại B.

**Trên màn hình:** AB đứng kề có 2·5! hàng. | BC đứng kề cũng có 2·5! hàng. | Phần giao phải xét riêng.
**Ghi nhớ:** KHÔNG DÙNG CÔNG THỨC HAI KHỐI RỜI NHAU.

### Nhịp 27 · 10:05 · PHẦN GIAO CÓ DẠNG ABC / CBA

Nếu A và B đứng cạnh, đồng thời B và C đứng cạnh, thì trong một hàng thẳng B buộc phải nằm giữa A và C. Chỉ có hai thứ tự của bộ ba liên tiếp là A B C hoặc C B A. Không được dùng sáu hoán vị của A B C, bởi bốn hoán vị còn lại không có B ở giữa. Gộp bộ ba thành một khối và xếp với D, E, F sẽ tạo bốn đối tượng.

**Trên màn hình:** B có A bên trái, C bên phải. | Hoặc B có C bên trái, A bên phải. | Gộp ba người thành một khối.
**Ghi nhớ:** CHỈ CÓ HAI THỨ TỰ ABC VÀ CBA.

### Nhịp 28 · 10:28 · ĐẾM HỢP, LẤY PHẦN BÙ

Khi đếm các hàng không có AB đứng kề và cũng không có BC đứng kề, ta lấy tổng bảy trăm hai mươi, trừ hai trăm bốn mươi hàng có AB kề, trừ thêm hai trăm bốn mươi hàng có BC kề, rồi cộng lại bốn mươi tám hàng thuộc phần giao. Kết quả là hai trăm tám mươi tám. Đây là ví dụ cho thấy công thức bao hàm loại trừ luôn giữ nguyên, nhưng cách đếm phần giao phụ thuộc rất mạnh vào cấu trúc ràng buộc.

**Trên màn hình:** Tổng số hàng: 720. | Hai tập cấm: 240 và 240. | Phần giao: 48.
**Ghi nhớ:** SỐ HÀNG HỢP LỆ BẰNG 288.

### Nhịp 29 · 10:52 · NẾU CẤM CẢ AB, BC, AC

Hãy tăng độ khó: yêu cầu A, B, C không có bất kỳ cặp nào đứng cạnh nhau. Có ba tập vi phạm tương ứng AB, BC, AC. Mỗi tập có hai trăm bốn mươi hàng, mỗi giao của hai tập có bốn mươi tám hàng, nhưng không thể ba người đều đứng cạnh nhau từng đôi một trong hàng thẳng. Vậy số hàng hợp lệ là bảy trăm hai mươi trừ ba lần hai trăm bốn mươi cộng ba lần bốn mươi tám, bằng một trăm bốn mươi bốn.

**Trên màn hình:** Ba cặp của A, B, C đều bị cấm. | Mỗi cặp riêng: 240 hàng. | Mỗi giao đôi: 48; giao ba: 0.
**Ghi nhớ:** KHÔNG THỂ BA NGƯỜI ĐỀU KỀ TỪNG ĐÔI TRÊN HÀNG.

### Nhịp 30 · 11:15 · ĐỐI CHIẾU BẰNG KHOẢNG TRỐNG

Với yêu cầu A, B và C đều không đứng cạnh nhau từng đôi một, ta còn có cách làm trực tiếp ngắn hơn. Xếp ba người D, E, F trước, có ba giai thừa cách. Họ tạo bốn khoảng trống; ta chọn ba khoảng khác nhau trong bốn, rồi đặt A, B, C vào ba khoảng đã chọn theo ba giai thừa cách. Kết quả cũng bằng một trăm bốn mươi bốn. Hai phương pháp khớp nhau, giúp xác nhận phép đếm phần giao ở bài nâng cao.

**Trên màn hình:** Xếp D, E, F trước: 3! cách. | Có bốn khoảng; chọn ba khoảng cho ABC. | Ba người A, B, C hoán vị: 3!.
**Ghi nhớ:** CÙNG MỘT KẾT QUẢ: 144 HÀNG.


## 06 · XẾP NAM NỮ VỚI KHOẢNG TRỐNG

### Nhịp 31 · 11:38 · NĂM NAM, BA NỮ PHÂN BIỆT

Một lớp có năm nam và ba nữ, tất cả đều là người phân biệt. Ta cần xếp tám người thành một hàng sao cho không có hai nữ nào đứng liền nhau. Hãy chú ý đề không nói nam và nữ phải xen kẽ hoàn toàn; vì số nam nhiều hơn, có thể xuất hiện hai hoặc ba nam đứng cạnh mà bài vẫn hợp lệ. Vì vậy mô hình chính xác là chọn khoảng trống trong một hàng nam, không phải ép một mẫu nữ nam cố định.

**Trên màn hình:** Có năm học sinh nam và ba học sinh nữ. | Không có hai nữ nào đứng cạnh nhau. | Xếp thành một hàng.
**Ghi nhớ:** ĐỪNG NHẦM KHÔNG KỀ VỚI XEN KẼ HOÀN TOÀN.

### Nhịp 32 · 12:02 · XẾP NĂM NAM TRƯỚC

Trước tiên, ta sắp xếp năm học sinh nam vào một hàng. Có năm giai thừa cách. Với bất cứ thứ tự nam nào, ta luôn có sáu khoảng: một trước hàng, bốn khoảng giữa hai nam liên tiếp và một ở cuối hàng. Để các bạn nữ không đứng cạnh nhau, mỗi khoảng chỉ được nhận tối đa một nữ. Khi đó mọi cách đặt các nữ vào những khoảng khác nhau đều hợp lệ.

**Trên màn hình:** Năm nam phân biệt: 5! cách. | Từ một hàng nam tạo sáu khoảng. | Mỗi khoảng có tối đa một nữ.
**Ghi nhớ:** ĐẶT NAM LÀM CÁC VẬT NGĂN CÁCH.

### Nhịp 33 · 12:25 · CHỌN BA TRONG SÁU KHOẢNG

Ta chọn ba trong sáu khoảng an toàn của hàng nam. Khi chọn, ba khoảng mới là một tập hợp, không phân biệt thứ tự chọn. Do đó có tổ hợp chập ba của sáu, tức hai mươi cách. Sau bước này, ta cần quyết định nữ thứ nhất vào khoảng nào, nữ thứ hai vào khoảng nào và nữ thứ ba vào khoảng nào. Đây là công việc khác với chọn tập hợp khoảng và sẽ đóng góp thừa số ba giai thừa.

**Trên màn hình:** Chọn ba khoảng khác nhau. | Số cách chọn: C dưới 3 trên 6 = 20. | Sau đó mới sắp ba nữ.
**Ghi nhớ:** CHỌN KHOẢNG KHÔNG ĐỒNG NGHĨA PHÂN CÔNG NỮ.

### Nhịp 34 · 12:48 · ĐẾM ĐẦY ĐỦ KẾT QUẢ

Mỗi cách xếp nam tạo sáu khoảng. Ta chọn ba khoảng, rồi hoán vị ba học sinh nữ vào đó. Áp dụng quy tắc nhân, số hàng hợp lệ là năm giai thừa nhân tổ hợp chập ba của sáu nhân ba giai thừa, cho kết quả mười bốn nghìn bốn trăm. Mỗi hàng có thể được khôi phục duy nhất bằng cách xóa các nữ để lấy hàng nam, xác định ba khoảng đã dùng, rồi đọc lại tên các nữ trong từng khoảng. Vì vậy không có đếm trùng.

**Trên màn hình:** Xếp nam: 5! = 120. | Chọn khoảng: 20. | Phân công nữ: 3! = 6.
**Ghi nhớ:** CÓ 14.400 CÁCH HỢP LỆ.

### Nhịp 35 · 13:12 · KHI NÀO KHÔNG CÓ CÁCH NÀO

Công thức phương pháp khoảng trống có một điều kiện tồn tại rất tự nhiên. Nếu có m bạn nam thì chỉ có m cộng một khoảng để chèn các nữ mà không có hai nữ đứng cạnh. Nếu số nữ k lớn hơn m cộng một, nguyên lý Dirichlet cho thấy chắc chắn có ít nhất hai nữ phải chung một khoảng, tức đứng cạnh nhau. Khi số nữ không vượt số khoảng, ta mới có thể chọn các khoảng khác nhau để xếp.

**Trên màn hình:** m nam tạo m+1 khoảng. | Muốn tách k nữ cần k khoảng riêng. | Nếu k > m+1 thì không thể.
**Ghi nhớ:** ĐIỀU KIỆN TỒN TẠI LÀ k ≤ m+1.

### Nhịp 36 · 13:35 · SO SÁNH VỚI XEN KẼ ĐÚNG

Hãy so sánh với bài có bốn nam, bốn nữ, yêu cầu nam nữ ngồi xen kẽ hoàn toàn. Chỉ có hai mẫu vị trí: nam trước hoặc nữ trước. Với mỗi mẫu, sắp bốn nam vào bốn vị trí nam và bốn nữ vào bốn vị trí nữ, được bốn giai thừa nhân bốn giai thừa cách. Nhân hai mẫu ta được một nghìn một trăm năm mươi hai. Điều kiện xen kẽ hoàn toàn mạnh hơn yêu cầu không có hai nữ đứng cạnh, nên không được dùng thay cho nhau.

**Trên màn hình:** Bốn nam và bốn nữ phân biệt. | Xen kẽ hoàn toàn có hai mẫu N–G. | Mỗi mẫu có 4!·4! cách.
**Ghi nhớ:** XEN KẼ HOÀN TOÀN CHẶT HƠN KHÔNG KỀ.


## 07 · KHÔNG ĐỨNG KỀ QUANH BÀN TRÒN

### Nhịp 37 · 13:58 · VÒNG TRÒN CÓ SỰ KHÁC BIỆT

Chuyển sang bàn tròn, chúng ta phải quyết định thế nào là một cách xếp khác nhau. Nếu các ghế không đánh số và chỉ quay cả bàn không tạo ra cách mới, số cách xếp sáu người là năm giai thừa. Trong bài này hai người A và B không được ngồi sát nhau theo hai phía vòng tròn, tức mỗi người có đúng hai hàng xóm. Chú ý hai ghế đầu và cuối của hàng thẳng khi uốn thành vòng cũng trở thành kề nhau.

**Trên màn hình:** Sáu người phân biệt ngồi bàn tròn. | Hai cách chỉ khác phép quay là một. | A, B không được ngồi cạnh.
**Ghi nhớ:** KHÔNG DÙNG N! CHO BÀN TRÒN KHÔNG ĐÁNH SỐ.

### Nhịp 38 · 14:22 · ĐẾM NHÓM A B NGỒI CẠNH

Khi A và B ngồi cạnh trên vòng tròn, ta gộp hai người thành một khối. Cùng bốn người còn lại, có năm đối tượng quanh bàn. Vì các phép quay được đồng nhất, số thứ tự của năm đối tượng là bốn giai thừa, không phải năm giai thừa. Nhân thêm hai thứ tự AB, BA bên trong khối, ta được bốn mươi tám cách vi phạm. Ta đang xem các chiều kim đồng hồ và ngược chiều là khác nhau, không tự động đồng nhất ảnh gương.

**Trên màn hình:** Gộp A, B thành một khối quanh bàn. | Còn năm đối tượng phân biệt. | Có (5-1)!·2 = 48 cách.
**Ghi nhớ:** PHẢI GIỮ TÍNH VÒNG SAU KHI GỘP KHỐI.

### Nhịp 39 · 14:45 · LẤY PHẦN BÙ TRÊN VÒNG

Vậy số cách để hai người A và B không ngồi cạnh nhau là một trăm hai mươi trừ bốn mươi tám, bằng bảy mươi hai. Nếu thử biến vòng tròn thành hàng thẳng bằng cách cắt tại một điểm tùy ý, ta sẽ dễ quên rằng hai đầu hàng đang kề nhau trên vòng. Đó là lý do nên cố định một người hoặc giữ trực tiếp mô hình vòng tròn trong mọi bước lập luận.

**Trên màn hình:** Tất cả: 5! = 120. | A và B ngồi cạnh: 48. | Không cạnh nhau: 72.
**Ghi nhớ:** PHẢI KIỂM TRA CẠNH NỐI CUỐI VÀ ĐẦU.

### Nhịp 40 · 15:08 · BỐN NAM, BA NỮ NGỒI VÒNG

Ta xét bốn nam và ba nữ phân biệt quanh một bàn tròn không đánh số. Muốn các nữ không ngồi cạnh nhau, ta xếp bốn nam quanh bàn trước. Khác với hàng thẳng, vòng tròn tạo ra đúng bốn khoảng giữa bốn người nam, vì không có khoảng trước đầu hàng hay sau cuối hàng. Mỗi nữ phải chiếm một khoảng khác nhau. Đây là nét khác biệt cốt lõi khi vận dụng phương pháp khoảng trống trên vòng.

**Trên màn hình:** Bốn nam và ba nữ phân biệt. | Không có hai nữ ngồi cạnh. | Xếp nam quanh bàn rồi chèn nữ.
**Ghi nhớ:** TRÊN VÒNG CÓ m KHOẢNG, KHÔNG PHẢI m+1.

### Nhịp 41 · 15:32 · CHỌN BA TRONG BỐN KHOẢNG

Số cách xếp bốn nam quanh bàn là ba giai thừa, bằng sáu. Có bốn khoảng trên vòng nên số cách chọn ba khoảng là tổ hợp chập ba của bốn, bằng bốn. Ba nữ phân biệt được hoán vị vào ba khoảng đã chọn theo ba giai thừa cách. Nhân ba thừa số cho kết quả một trăm bốn mươi bốn cách. Mỗi cách xếp hợp lệ xác định duy nhất thứ tự vòng của bốn nam và ba khoảng chứa nữ.

**Trên màn hình:** Xếp nam vòng tròn: 3! cách. | Chọn ba trong bốn khoảng: 4 cách. | Sắp ba nữ: 3! cách.
**Ghi nhớ:** KẾT QUẢ 144 CÁCH.

### Nhịp 42 · 15:54 · SO SÁNH HÀNG VÀ VÒNG

Chốt lại, khi xếp một nhóm nền gồm m người thành hàng thẳng, ta có m cộng một khoảng chèn. Khi xếp quanh bàn tròn không đánh số, ta chỉ có m khoảng và còn phải đồng nhất các hoán vị khác nhau bởi phép quay. Nếu đề bài quy định ghế đánh số thì mỗi vị trí ghế là cố định, phép quay không được đồng nhất. Nếu đề bài cho phép đồng nhất cả ảnh gương, lại là một mô hình đếm khác. Phải đọc rõ quy ước trước khi tính.

**Trên màn hình:** Hàng thẳng: m+1 khoảng. | Bàn tròn: m khoảng. | Xoay bàn là cùng cách, lật gương thì khác.
**Ghi nhớ:** LÀM RÕ QUY ƯỚC TRƯỚC KHI ÁP DỤNG.


## 08 · BA CẶP CẤM KỀ - HSG

### Nhịp 43 · 16:18 · BÀI TOÁN BA CẶP BỊ CẤM

Ở bài cuối, chúng ta xét tám người phân biệt và ba cặp chỉ định AB, CD, EF. Mỗi cặp đều không được đứng cạnh nhau khi xếp tám người thành một hàng. Người G, H không thuộc cặp cấm nào. Với ba điều kiện, việc lấy tổng trừ đơn giản dễ bị trừ trùng. Hãy đặt ba tập hợp vi phạm tương ứng E một, E hai, E ba rồi áp dụng bao hàm loại trừ đầy đủ đến phần giao ba tập.

**Trên màn hình:** Tám người A, B, C, D, E, F, G, H. | AB, CD và EF đều không kề nhau. | Tìm số hàng thỏa ba điều kiện.
**Ghi nhớ:** BA RÀNG BUỘC CẤM CẦN BAO HÀM–LOẠI TRỪ.

### Nhịp 44 · 16:42 · ĐẾM HÀNG VI PHẠM MỘT CẶP

Nếu chỉ bắt buộc A và B đứng cạnh, ta gộp thành một khối cùng sáu người còn lại, tức bảy đối tượng. Có bảy giai thừa cách xếp ngoài và hai thứ tự trong khối, cho mười nghìn không trăm tám mươi hàng. Các cặp CD và EF có cùng số lượng. Tổng ba số riêng là ba nhân hai nhân bảy giai thừa, nhưng đang tính nhiều lần những hàng vi phạm hơn một cặp, nên chưa phải số hàng bị cấm cuối cùng.

**Trên màn hình:** Một cặp đứng kề: 2·7!. | Có ba cặp chỉ định giống cấu trúc. | Tổng ba số riêng: 3·2·7!.
**Ghi nhớ:** CHÚ Ý MỖI HÀNG CÓ THỂ VI PHẠM NHIỀU CẶP.

### Nhịp 45 · 17:05 · ĐẾM GIAO CỦA HAI CẶP

Nếu AB và CD cùng đứng kề, chúng là hai khối rời nhau cùng bốn người E, F, G, H, vậy có sáu đối tượng. Hai khối có tổng cộng bốn thứ tự nội bộ. Do đó mỗi giao đôi có bốn nhân sáu giai thừa, bằng hai nghìn tám trăm tám mươi hàng. Có tổ hợp chập hai của ba cách chọn hai cặp trong ba cặp, tức ba giao đôi. Tổng phần được cộng trở lại bằng ba nhân bốn nhân sáu giai thừa.

**Trên màn hình:** Chọn hai trong ba cặp: 3 cách. | Gộp hai khối và hai người còn lại. | Mỗi giao có 2²·6! hàng.
**Ghi nhớ:** PHẢI CỘNG LẠI BA PHẦN GIAO ĐÔI.

### Nhịp 46 · 17:28 · ĐẾM GIAO CỦA BA CẶP

Nếu cả ba cặp AB, CD và EF đều đứng cạnh nhau, gộp mỗi cặp thành một khối. Ta có ba khối và hai người còn lại G, H, tổng cộng năm đối tượng. Có năm giai thừa cách xếp năm đối tượng và tám thứ tự bên trong ba khối. Như vậy phần giao ba tập cấm có chín trăm sáu mươi hàng. Trong bao hàm loại trừ, sau khi đã trừ các tập đơn và cộng các giao đôi, ta phải trừ đi giao ba này một lần.

**Trên màn hình:** AB, CD và EF đồng thời kề. | Ba khối cùng G, H: 5 đối tượng. | Có 2³·5! = 960 hàng.
**Ghi nhớ:** PHẦN GIAO BA PHẢI BỊ TRỪ LẦN CUỐI.

### Nhịp 47 · 17:51 · TÍNH SỐ HÀNG HỢP LỆ

Ghép các kết quả lại, số hàng hợp lệ là tám giai thừa, trừ ba lần hai nhân bảy giai thừa, cộng ba lần bốn nhân sáu giai thừa, rồi trừ tám nhân năm giai thừa. Ta được mười bảy nghìn bảy trăm sáu mươi hàng. Điều quan trọng không chỉ là đáp số mà là ý nghĩa của dấu trừ, cộng, trừ theo từng tầng giao biến cố. Hình động sẽ lần lượt tô những vùng vừa được loại, rồi được hoàn lại.

**Trên màn hình:** Tổng: 40320. | Trừ 30240, cộng 8640, trừ 960. | Còn 17760 hàng hợp lệ.
**Ghi nhớ:** CÔNG THỨC PHẢI ĐÚNG TỪNG HẠNG TỬ.

### Nhịp 48 · 18:14 · BÀI HỌC CUỐI VÀ KIỂM CHỨNG

Ta có thể liệt kê toàn bộ bốn mươi nghìn ba trăm hai mươi hoán vị của tám người để kiểm tra rằng đúng mười bảy nghìn bảy trăm sáu mươi hàng không chứa bất kỳ cặp đứng kề bị cấm nào. Kết thúc bài, hãy tự hỏi: khi cấm một cặp, dùng phần bù; khi cần tách một nhóm, dùng khoảng trống; khi có nhiều cặp cấm, dùng bao hàm loại trừ; khi các cặp chung phần tử, cần xử lý riêng phần giao. Đó mới là tư duy giải toán tổ hợp.

**Trên màn hình:** Liệt kê 8! hàng bằng Python để kiểm tra. | So sánh 17760 với công thức. | Phân biệt phương pháp thích hợp từng bài.
**Ghi nhớ:** ĐỌC ĐIỀU KIỆN TRƯỚC, CÔNG THỨC SAU.
