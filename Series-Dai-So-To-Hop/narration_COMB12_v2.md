# SANG MATH · COMB12 V2 · PHƯƠNG PHÁP GỘP KHỐI

## Bản thuyết minh đồng bộ

Số nhịp: 48 · 8 chương · TTS=off
Tổng thời lượng dự kiến: 1092.4 giây.
Lời giảng bên dưới là nội dung đầy đủ được đưa vào tổng hợp giọng đọc; không cắt tùy ý.


## 01 · TỪ HAI NGƯỜI ĐẾN MỘT KHỐI

### Nhịp 01 · 00:00 · BÀI TOÁN MỞ ĐẦU

Có năm học sinh mang tên A, B, C, D và E. Chúng ta muốn xếp cả năm thành một hàng, nhưng A và B phải đứng cạnh nhau. Nếu chỉ dùng năm giai thừa, tức một trăm hai mươi cách, thì ta đã đếm cả những hàng có A, B đứng cách xa nhau. Hãy tìm mô hình buộc điều kiện đứng cạnh được giữ đúng ngay từ đầu.

**Trên màn hình:** Năm học sinh A, B, C, D, E. | Xếp thành một hàng. | A và B bắt buộc đứng liền nhau.
**Ghi nhớ:** HÃY BẮT ĐẦU TỪ ĐIỀU KIỆN, CHƯA VIẾT CÔNG THỨC.

### Nhịp 02 · 00:23 · THỬ ĐẶT HAI BẠN CẠNH NHAU

Khi quan sát hai bạn A và B, ta thấy hai cách xuất hiện trong một hàng: A đứng trước B hoặc B đứng trước A. Hai cách đó đều hợp lệ. Nếu chỉ gộp thành ký hiệu AB rồi quên cách BA, kết quả sẽ bị thiếu đúng một nửa. Chúng ta sẽ giữ lại sự lựa chọn thứ tự bên trong khối.

**Trên màn hình:** Xếp mẫu A – B – C – D – E. | Đổi A, B thành B – A. | Cả hai đều thỏa điều kiện.
**Ghi nhớ:** ĐỨNG CẠNH KHÔNG CÓ NGHĨA LÀ CỐ ĐỊNH THỨ TỰ.

### Nhịp 03 · 00:45 · GỘP A VÀ B THÀNH MỘT KHỐI

Thay vì cố xếp từng người và kiểm tra cặp đứng cạnh sau đó, ta tạm xem A và B như một thẻ mới mang tên khối AB. Bên cạnh khối là ba bạn C, D, E, vậy có tất cả bốn đối tượng phân biệt. Xếp bốn đối tượng này thành hàng sẽ tạo bốn giai thừa thứ tự và luôn bảo đảm A, B cùng một vị trí liên tiếp.

**Trên màn hình:** Đặt [AB] cạnh C, D, E. | Từ 5 người thành 4 đối tượng. | Bốn đối tượng có 4! thứ tự.
**Ghi nhớ:** KHỐI [AB] KHÔNG THỂ BỊ TÁCH RA KHI XẾP.

### Nhịp 04 · 01:07 · NHÂN SỐ CÁCH TRONG KHỐI

Đối với mỗi cách đặt khối AB cùng C, D, E, ta lại có hai cách sắp xếp nội bộ khối: A trước B hoặc B trước A. Hai việc lựa chọn nối tiếp nhau, vì thế phải nhân hai với bốn giai thừa. Kết quả là bốn mươi tám cách. Mỗi hàng hợp lệ xác định duy nhất một vị trí khối và một thứ tự trong khối nên không bị tính trùng.

**Trên màn hình:** Thứ tự bốn đối tượng: 4!. | Trong khối có AB hoặc BA: 2!. | Tổng 2! × 4! = 48.
**Ghi nhớ:** NHÂN HOÁN VỊ CÁC KHỐI VỚI HOÁN VỊ BÊN TRONG.

### Nhịp 05 · 01:30 · CHỨNG MINH LẠI BẰNG VỊ TRÍ

Ta hãy kiểm tra kết quả bằng phương pháp khác. Trong hàng năm chỗ, cặp A B đứng cạnh có thể chiếm các vị trí một và hai, hai và ba, ba và bốn, hoặc bốn và năm. Nghĩa là có bốn cách chọn chỗ bắt đầu của cặp, hai cách hoán đổi A B, và ba giai thừa cách xếp ba người còn lại. Tích cũng bằng bốn mươi tám.

**Trên màn hình:** Cặp AB có thể bắt đầu ở vị trí 1–4. | Mỗi vị trí có 2 thứ tự AB, BA. | Ba người còn lại có 3! cách.
**Ghi nhớ:** HAI CÁCH ĐẾM CÙNG CHO RA 48.

### Nhịp 06 · 01:52 · KHÁI QUÁT HAI NGƯỜI TRONG n NGƯỜI

Với n người phân biệt có hai người A, B bắt buộc đứng cạnh, ta có một khối và n trừ hai người riêng lẻ. Tổng số đối tượng là n trừ một, nên có n trừ một giai thừa cách xếp chúng. Nhân thêm hai thứ tự bên trong khối, ta được hai nhân n trừ một giai thừa. Công thức này dành cho một hàng thẳng, chưa phải bàn tròn.

**Trên màn hình:** Tất cả n người phân biệt, n ≥ 2. | Gộp hai người thành một khối. | Có 2 × (n − 1)! cách.
**Ghi nhớ:** CHỈ ÁP DỤNG KHI ĐÚNG HAI NGƯỜI PHẢI ĐỨNG LIỀN.


## 02 · BA NGƯỜI ĐỨNG LIỀN NHAU

### Nhịp 07 · 02:15 · NẾU BA NGƯỜI PHẢI LIỀN NHAU?

Tình huống tiếp theo có sáu học sinh. Ba bạn A, B, C phải đứng thành một đoạn liên tiếp, không yêu cầu ai đứng trước ai. Đây vẫn là kỹ thuật gộp khối, nhưng số cách sắp xếp bên trong khối đã khác. Trước khi tính, ta cần biết có bao nhiêu đối tượng sau khi gộp và bao nhiêu hoán vị bên trong khối ba người.

**Trên màn hình:** Sáu học sinh A, B, C, D, E, F. | A, B, C đứng thành một đoạn liên tiếp. | Bên trong chưa quy định thứ tự.
**Ghi nhớ:** THAY BA NGƯỜI BẰNG MỘT KHỐI.

### Nhịp 08 · 02:39 · ĐẾM SỐ ĐỐI TƯỢNG SAU GỘP

Sau khi gộp A, B, C, ta có khối ABC cùng ba học sinh D, E, F. Tất cả chỉ có bốn đối tượng cần sắp hàng, vì vậy số cách đặt khối là bốn giai thừa. Đáng chú ý, gộp ba người làm số đối tượng giảm hai, không giảm ba. Công thức ngoài khối phụ thuộc chính xác vào số phần tử đã được gộp.

**Trên màn hình:** Khối [ABC], D, E, F. | Chỉ còn 4 đối tượng. | Sắp xếp ngoài khối: 4! cách.
**Ghi nhớ:** BA NGƯỜI CHIẾM MỘT ĐOẠN KHÔNG BỊ CHIA CẮT.

### Nhịp 09 · 03:01 · HOÁN VỊ BÊN TRONG KHỐI

Bây giờ giữ nguyên vị trí của khối trên hàng. Ta vẫn có thể xếp ba bạn A, B, C theo sáu thứ tự khác nhau. Khi lấy một thứ tự ngoài khối và một thứ tự bên trong, ta được đúng một hàng thỏa điều kiện. Do đó, ngoài bốn giai thừa, phải nhân thêm ba giai thừa.

**Trên màn hình:** ABC, ACB, BAC, BCA, CAB, CBA. | Có 3! = 6 thứ tự nội bộ. | Tất cả vẫn là ba người liền nhau.
**Ghi nhớ:** KHÔNG ĐƯỢC QUÊN 3! THỨ TỰ TRONG KHỐI.

### Nhịp 10 · 03:23 · SÁU NGƯỜI, BA NGƯỜI ĐI LIỀN

Ghép hai công đoạn, ta có ba giai thừa nhân bốn giai thừa, bằng một trăm bốn mươi bốn cách. Nếu lỡ coi cụm ABC đã cố định thứ tự, ta chỉ tìm được hai mươi bốn và bỏ sót năm phần sáu số hàng. Hình động sẽ cho thấy khối đứng yên trong khi ba thẻ bên trong liên tục hoán đổi vị trí.

**Trên màn hình:** Ngoài khối có 4! cách. | Bên trong khối có 3! cách. | Tổng cộng 3! × 4! = 144.
**Ghi nhớ:** BA NGƯỜI TÙY Ý: ĐẾM ĐỦ SÁU THỨ TỰ.

### Nhịp 11 · 03:46 · NẾU BẮT BUỘC ĐÚNG ABC

Chỉ thay đổi một cụm từ của đề bài, đáp số đã giảm mạnh. Nếu yêu cầu ba người xuất hiện đúng theo thứ tự A rồi B rồi C và phải kề nhau, bên trong khối chỉ có một cách. Ta vẫn có bốn đối tượng ngoài khối nên số hàng là bốn giai thừa, bằng hai mươi bốn. Hãy phân biệt rõ đứng thành một nhóm với đứng đúng thứ tự.

**Trên màn hình:** A phải trước B, B phải trước C. | Chỉ còn một thứ tự trong khối. | Có đúng 4! = 24 hàng.
**Ghi nhớ:** ĐIỀU KIỆN THỨ TỰ THAY ĐỔI ĐÁP SỐ.

### Nhịp 12 · 04:08 · CÔNG THỨC MỘT KHỐI k NGƯỜI

Với n người phân biệt, khi k người chỉ cần đứng liền nhau theo thứ tự tùy ý, ta thay nhóm k người bằng một khối. Số đối tượng còn n trừ k cộng một. Các đối tượng này có n trừ k cộng một giai thừa cách xếp; trong khối có k giai thừa hoán vị. Nhân lại ta được công thức chung, với một không nhỏ hơn k và k không lớn hơn n.

**Trên màn hình:** n người phân biệt; k người tạo một khối. | Bên ngoài: (n − k + 1)! cách. | Bên trong: k! cách.
**Ghi nhớ:** k! × (n − k + 1)! NẾU KHÔNG RÀNG BUỘC THỨ TỰ.


## 03 · HAI KHỐI RỜI NHAU

### Nhịp 13 · 04:31 · HAI CẶP KHÁC NHAU

Giờ đây ta có sáu học sinh A đến F, và đồng thời yêu cầu A ngồi cạnh B, C đứng cạnh D. Hai cặp không có người chung nên có thể tạo thành hai khối riêng biệt. Điều quan trọng là phân biệt số cách xếp bốn đối tượng ngoài khối và hai số cách hoán vị bên trong hai khối.

**Trên màn hình:** A, B phải đứng cạnh nhau. | C, D cũng phải đứng cạnh nhau. | Có sáu học sinh phân biệt.
**Ghi nhớ:** GỘP THÀNH HAI KHỐI KHÔNG GIAO NHAU.

### Nhịp 14 · 04:55 · VẼ HAI KHỐI ĐỘC LẬP

Sau khi gộp, ta còn khối AB, khối CD và hai người E, F. Bốn đối tượng này có bốn giai thừa cách sắp thành hàng. Lúc này không nên mở khối quá sớm, vì nếu hoán đổi A với D giữa hai khối, chúng ta không còn giữ điều kiện cặp ban đầu. Đầu tiên hãy xếp các khối nguyên vẹn.

**Trên màn hình:** [AB], [CD], E, F. | Có bốn đối tượng phân biệt. | Sắp xếp ngoài khối: 4! cách.
**Ghi nhớ:** HAI KHỐI LÀ HAI ĐỐI TƯỢNG RIÊNG.

### Nhịp 15 · 05:17 · HAI HOÁN VỊ BÊN TRONG

Khi vị trí các khối đã được chọn, bên trong khối AB có hai thứ tự AB và BA, khối CD có hai thứ tự CD và DC. Chúng là các lựa chọn độc lập, vì hai cặp không có người chung. Ta nhân bốn giai thừa với hai và hai, nhận chín mươi sáu cách. Đây là điểm khác biệt lớn với những khối có phần tử chung ở chương sau.

**Trên màn hình:** Khối AB có 2 thứ tự. | Khối CD cũng có 2 thứ tự. | Tổng 2 × 2 × 4! = 96.
**Ghi nhớ:** CÁC KHỐI RỜI NHAU THÌ NHÂN ĐƯỢC CÁC SỐ CÁCH.

### Nhịp 16 · 05:39 · NẾU HAI KHỐI ĐÃ CỐ ĐỊNH THỨ TỰ

Nếu đề yêu cầu A đứng ngay trước B đồng thời C đứng ngay trước D, ta không được nhân thêm hai lựa chọn nội bộ cho từng cặp. Chỉ có đúng khối AB và đúng khối CD. Bên ngoài vẫn có bốn đối tượng nên số cách là hai mươi bốn. Khi đọc đề, từ ngay trước khác hẳn cụm từ đứng cạnh.

**Trên màn hình:** Phải là AB, không được BA. | Phải là CD, không được DC. | Chỉ còn 4! = 24 cách.
**Ghi nhớ:** KHÔNG NHÂN HOÁN VỊ NỘI BỘ KHI THỨ TỰ ĐÃ CỐ ĐỊNH.

### Nhịp 17 · 06:02 · BA CẶP TRONG SÁU NGƯỜI

Với sáu người được chia thành ba cặp AB, CD và EF, nếu cả ba cặp đều phải liền nhau, ta có đúng ba khối. Bên ngoài ba khối hoán vị theo ba giai thừa cách. Bên trong mỗi khối có hai cách, tổng là hai mũ ba. Do đó có bốn mươi tám cách, không phải hai nhân sáu giai thừa.

**Trên màn hình:** [AB], [CD], [EF]. | Ba khối phân biệt xếp 3! cách. | Mỗi khối có 2 thứ tự.
**Ghi nhớ:** 3! × 2³ = 48 CÁCH.

### Nhịp 18 · 06:24 · MỞ RỘNG n NGƯỜI, r KHỐI RỜI

Trong bài toán tổng quát, nhiều nhóm người không giao nhau lần lượt có k một, k hai, đến k r phần tử bắt buộc đứng liền. Mỗi khối làm giảm số đối tượng đi k i trừ một. Khi các khối sắp tự do, ta nhân giai thừa của số đối tượng còn lại với tích các giai thừa kích thước khối. Cách này chỉ đúng nếu các khối độc lập và không bị điều kiện vị trí khác cản trở.

**Trên màn hình:** Các khối có kích thước k₁, ..., kᵣ. | Số đối tượng còn n − ∑(kᵢ − 1). | Nhân với ∏kᵢ! nếu được đổi nội bộ.
**Ghi nhớ:** ĐẢM BẢO CÁC KHỐI KHÔNG CÓ PHẦN TỬ CHUNG.


## 04 · HAI ĐIỀU KIỆN CÓ CHUNG PHẦN TỬ

### Nhịp 19 · 06:47 · HAI CẶP CÓ CHUNG B

Chúng ta thay đổi yêu cầu: A phải cạnh B và B phải cạnh C. Hai cặp này cùng chứa người B, nên nếu xem chúng như hai khối tách rời AB và BC, ta đã dùng B hai lần. Đây là lỗi rất phổ biến khi vận dụng công thức gộp khối. Hãy nhìn vị trí của B trên hàng để dựng lại cấu trúc đúng.

**Trên màn hình:** A cạnh B và B cạnh C. | B tham gia cả hai điều kiện. | Không thể tạo hai khối độc lập [AB], [BC].
**Ghi nhớ:** KHỐI GIAO NHAU CẦN XÉT CẤU TRÚC LIÊN TIẾP.

### Nhịp 20 · 07:11 · AI PHẢI Ở GIỮA?

Để B đứng cạnh cả A lẫn C trong một hàng, hai bạn kia phải đứng ở hai phía khác nhau của B. Nghĩa là bộ ba chỉ có hai thứ tự hợp lệ: A B C hoặc C B A. Nếu xếp B ở một đầu, B chỉ có một hàng xóm trong đoạn ba người và không thể cùng lúc cạnh cả A và C. Điều kiện giao nhau đã xác định vị trí chính giữa.

**Trên màn hình:** B phải đứng cạnh cả A và C. | Trong hàng, B có tối đa hai hàng xóm. | Chỉ có A – B – C hoặc C – B – A.
**Ghi nhớ:** PHẢI CHUNG MỘT KHỐI BA NGƯỜI.

### Nhịp 21 · 07:33 · ĐẾM HÀNG CÓ SÁU NGƯỜI

Bây giờ xếp sáu người. Ta dùng một khối gồm A, B, C với hai thứ tự A B C và C B A, cùng ba học sinh D, E, F. Có bốn đối tượng nên có bốn giai thừa thứ tự ở ngoài, nhân hai ở trong. Kết quả là bốn mươi tám cách. Hệ số hai này bắt nguồn từ toàn bộ ba người, không phải nhân hai lần cho hai cặp.

**Trên màn hình:** [ABC] có đúng 2 dạng được phép. | Ngoài khối là D, E, F: 4 đối tượng. | Số cách 2 × 4! = 48.
**Ghi nhớ:** KHÔNG PHẢI 2² × 4! VÌ HAI CẶP KHÔNG ĐỘC LẬP.

### Nhịp 22 · 07:55 · NẾU A CẠNH C VÀ A CẠNH B

Khi đổi điều kiện thành A cạnh B và A cạnh C, chính A phải đứng giữa. Hai dạng hợp lệ trong đoạn ba người lúc này là B A C hoặc C A B. Số cách vẫn là bốn mươi tám, nhưng người ở giữa đã thay đổi. Đây là cách kiểm tra ý nghĩa hình học của điều kiện trước khi đưa vào phép tính.

**Trên màn hình:** A phải là người ở giữa. | Khối có B – A – C hoặc C – A – B. | Cũng có 2 × 4! = 48.
**Ghi nhớ:** ĐỌC ĐÚNG ĐỈNH CHUNG CỦA HAI ĐIỀU KIỆN.

### Nhịp 23 · 08:18 · CẢ BA CẶP ĐỀU CẠNH NHAU?

Nếu đồng thời đòi A cạnh B, B cạnh C và A cạnh C trên một hàng, bài toán trở nên bất khả thi. Trong ba vị trí liên tiếp, chỉ có hai cặp vị trí kề nhau. Không thể biến ba người thành ba cặp đôi một đều kề nhau trên đường thẳng. Vì vậy đáp số là không, và ta phải phát hiện điều này trước khi cố gộp khối.

**Trên màn hình:** A cạnh B, B cạnh C, A cạnh C. | Trong một hàng ba người chỉ có hai cặp kề. | Không có cách nào thỏa mãn.
**Ghi nhớ:** KHÔNG PHẢI HỆ ĐIỀU KIỆN NÀO CŨNG CÓ NGHIỆM.

### Nhịp 24 · 08:40 · NHẬN DIỆN KHỐI CHỒNG LẤN

Một mẹo hữu ích là vẽ mỗi học sinh thành một đỉnh và mỗi yêu cầu đứng cạnh thành một cạnh nối. Nếu các cạnh tạo một đường A B C, nhóm bắt buộc phải xuất hiện theo đường ấy hoặc theo chiều ngược lại. Nếu xuất hiện một chu trình ba cạnh như tam giác, không thể đặt toàn bộ các cạnh thành quan hệ kề nhau trong một hàng. Đây là công cụ nhận diện rất mạnh cho các bài khó.

**Trên màn hình:** Vẽ đồ thị điều kiện kề. | Các cạnh AB và BC nối thành đường A–B–C. | Dựa vào cấu trúc để đếm thứ tự hợp lệ.
**Ghi nhớ:** VẼ ĐIỀU KIỆN TRƯỚC, RỒI MỚI GỘP.


## 05 · ÍT NHẤT MỘT CẶP ĐỨNG CẠNH

### Nhịp 25 · 09:03 · Ít NHẤT MỘT CẶP PHẢI KỀ

Ta trở lại hai cặp AB và CD, nhưng chỉ yêu cầu ít nhất một cặp đứng cạnh nhau. Có thể chỉ cặp AB đứng cạnh, chỉ cặp CD đứng cạnh, hoặc cả hai cùng thỏa. Vì hai biến cố có phần giao, nếu cộng số cách của từng cặp riêng rẽ thì những hàng có cả hai cặp sẽ được tính hai lần.

**Trên màn hình:** Sáu người A, B, C, D, E, F. | A đứng cạnh B hoặc C đứng cạnh D. | Có thể cả hai cặp cùng đứng cạnh.
**Ghi nhớ:** CHỮ HOẶC CẦN KIỂM TRA PHẦN GIAO.

### Nhịp 26 · 09:26 · ĐẶT HAI BIẾN CỐ

Kí hiệu E một là biến cố A cạnh B, E hai là biến cố C cạnh D. Với sáu người, mỗi biến cố có hai nhân năm giai thừa, bằng hai trăm bốn mươi cách. Nếu cộng hai số này, ta được bốn trăm tám mươi. Nhưng số đó chưa đúng, vì mọi hàng có cả AB và CD liền nhau đều xuất hiện trong cả hai nhóm.

**Trên màn hình:** E₁: A cạnh B. | E₂: C cạnh D. | Mỗi biến cố có 2 × 5! = 240.
**Ghi nhớ:** HAI SỐ 240 CHƯA PHẢI ĐÁP SỐ CẦN TÌM.

### Nhịp 27 · 09:48 · TÍNH PHẦN GIAO

Phần giao chính là bài toán hai khối rời nhau ở chương ba. Ta có các đối tượng AB, CD, E, F. Chúng có bốn giai thừa thứ tự ngoài và hai lựa chọn bên trong mỗi cặp. Do đó phần giao có chín mươi sáu cách. Đây là những hàng đã bị cộng hai lần khi ta lấy hai trăm bốn mươi cộng hai trăm bốn mươi.

**Trên màn hình:** E₁ ∩ E₂: cả hai cặp đều kề. | Gộp [AB], [CD], E, F. | Phần giao có 2² × 4! = 96.
**Ghi nhớ:** PHẦN GIAO ĐÃ BỊ ĐẾM HAI LẦN.

### Nhịp 28 · 10:10 · ÁP DỤNG BAO HÀM–LOẠI TRỪ

Ta áp dụng công thức đếm phần hợp của hai tập: số phần tử nhóm thứ nhất cộng số phần tử nhóm thứ hai rồi trừ phần giao. Thay số, hai trăm bốn mươi cộng hai trăm bốn mươi trừ chín mươi sáu bằng ba trăm tám mươi bốn. Mỗi hàng hợp lệ giờ được đếm đúng một lần, kể cả những hàng thỏa đồng thời hai điều kiện.

**Trên màn hình:** |E₁ ∪ E₂| = |E₁| + |E₂| − |E₁ ∩ E₂|. | Thay số: 240 + 240 − 96. | Kết quả 384 cách.
**Ghi nhớ:** TRỪ MỘT LẦN PHẦN GIAO ĐỂ HẾT ĐẾM TRÙNG.

### Nhịp 29 · 10:34 · KHÔNG CẶP NÀO ĐƯỢC KỀ

Nếu đề hỏi ngược lại rằng A không cạnh B và C không cạnh D, ta có thể dùng phần bù của biến cố ít nhất một cặp kề. Tổng số cách xếp sáu người là sáu giai thừa, bằng bảy trăm hai mươi. Trừ ba trăm tám mươi bốn trường hợp vi phạm, ta còn ba trăm ba mươi sáu hàng hợp lệ.

**Trên màn hình:** Tất cả sáu người: 6! = 720. | Có ít nhất một cặp kề: 384. | Không cặp nào kề: 720 − 384 = 336.
**Ghi nhớ:** PHẦN BÙ LÀ CÁCH ĐẾM MẠNH KHI CÓ CHỮ KHÔNG.

### Nhịp 30 · 10:56 · KIỂM CHỨNG BẰNG LIỆT KÊ

Để yên tâm rằng không nhầm điều kiện, ta có thể dùng Python duyệt toàn bộ bảy trăm hai mươi hoán vị và đánh dấu những hàng có AB hoặc CD kề nhau. Kết quả nhóm có ít nhất một cặp là ba trăm tám mươi bốn, nhóm không cặp nào kề là ba trăm ba mươi sáu. Tổng trở lại đúng bảy trăm hai mươi, tạo một phép kiểm tra độc lập.

**Trên màn hình:** Duyệt tất cả 720 hoán vị. | Đếm riêng hai biến cố và phần giao. | 384 + 336 = 720.
**Ghi nhớ:** HAI NHÓM KẾT QUẢ PHÂN HOẠCH TOÀN BỘ CÁC HÀNG.


## 06 · ĐÚNG MỘT CẶP ĐỨNG CẠNH

### Nhịp 31 · 11:19 · ĐÚNG MỘT TRONG HAI CẶP

Một đề bài rất dễ bị nhầm là chỉ được đúng một trong hai cặp AB, CD đứng cạnh nhau. Điều này khác với ít nhất một cặp, vì khi cả hai đều kề nhau thì không còn hợp lệ. Ta sẽ tách thành hai trường hợp rời nhau: AB kề nhưng CD không kề, hoặc CD kề nhưng AB không kề.

**Trên màn hình:** AB đứng kề hoặc CD đứng kề. | Nhưng không được đồng thời cả hai. | Đây là điều kiện hoặc loại trừ.
**Ghi nhớ:** KHÁC HẲN CỤM TỪ ÍT NHẤT MỘT.

### Nhịp 32 · 11:42 · TRƯỜNG HỢP AB CÓ, CD KHÔNG

Với trường hợp thứ nhất, ta đếm tất cả hàng có AB đứng cạnh, được hai trăm bốn mươi. Trong số đó có chín mươi sáu hàng mà CD cũng đứng cạnh; chúng phải bị loại bỏ vì vi phạm yêu cầu đúng một. Số cách còn lại là một trăm bốn mươi bốn. Đây là phép đếm phần bù trong phạm vi nhóm AB.

**Trên màn hình:** AB kề: 240 cách. | AB và CD cùng kề: 96 cách. | Còn 240 − 96 = 144 cách.
**Ghi nhớ:** TRỪ PHẦN GIAO NGAY TRONG NHÓM AB.

### Nhịp 33 · 12:04 · TRƯỜNG HỢP CD CÓ, AB KHÔNG

Trường hợp thứ hai hoàn toàn tương tự: CD đứng cạnh nhưng AB không đứng cạnh. Số cách cũng là hai trăm bốn mươi trừ chín mươi sáu, bằng một trăm bốn mươi bốn. Hai nhóm không có hàng chung, vì một hàng không thể vừa có AB kề, CD không kề, vừa có CD kề, AB không kề. Ta được phép áp dụng quy tắc cộng.

**Trên màn hình:** Tương tự trường hợp trước. | Có 240 − 96 = 144 cách. | Hai trường hợp không giao nhau.
**Ghi nhớ:** DÙNG QUY TẮC CỘNG CHO HAI NHÓM RỜI NHAU.

### Nhịp 34 · 12:26 · TỔNG HỢP KẾT QUẢ

Cộng hai nhóm rời nhau, ta có hai trăm tám mươi tám cách. Ngoài ra, từ kết quả phần hợp ba trăm tám mươi bốn ở chương trước, ta chỉ cần trừ đi chín mươi sáu hàng mà cả hai cặp đều kề, cũng nhận đúng hai trăm tám mươi tám. Hai hướng đi khác nhau cùng cho kết quả, nên đây là một phép đối chiếu tốt.

**Trên màn hình:** Đúng một cặp kề: 144 + 144. | Kết quả 288 cách. | Có thể lấy 384 − 96 để kiểm tra.
**Ghi nhớ:** ĐẾM ĐÚNG MỘT = ĐẾM ÍT NHẤT MỘT − ĐẾM CẢ HAI.

### Nhịp 35 · 12:50 · BÀI BIẾN THỂ: AB CÓ, CD KHÔNG

Hãy đọc thật kỹ sự khác biệt: nếu đề chỉ yêu cầu AB phải đứng cạnh còn CD không được đứng cạnh, kết quả chỉ là một trăm bốn mươi bốn. Ta không được nhân đôi vì trường hợp đối xứng CD kề, AB không kề đã không được đề cho phép. Đây là lỗi đọc đề có thể khiến đáp án bị gấp đôi.

**Trên màn hình:** Không yêu cầu đổi vai trò hai cặp. | Chỉ đếm một trong hai nhóm. | Kết quả riêng là 144 cách.
**Ghi nhớ:** CẦN XEM ĐỀ NÓI ĐÚNG MỘT HAY ĐÚNG CẶP CHỈ ĐỊNH.

### Nhịp 36 · 13:12 · NÂNG CAO: E ĐỨNG TRƯỚC F

Ta thêm một điều kiện thứ tự vào bài hai khối AB và CD đều kề nhau: E phải đứng trước F. Trong chín mươi sáu hàng hợp lệ, việc đổi tên E và F tạo một song ánh giữa nhóm E đứng trước F và nhóm F đứng trước E. Hai nhóm có kích thước bằng nhau, vì vậy số hàng thỏa yêu cầu mới là chín mươi sáu chia hai, bằng bốn mươi tám.

**Trên màn hình:** AB và CD đều đứng cạnh nhau. | E phải xuất hiện trước F. | 96 : 2 = 48 cách.
**Ghi nhớ:** DÙNG PHÉP ĐỔI CHỖ E VÀ F ĐỂ CHIA ĐÔI.


## 07 · GỘP KHỐI KHI XẾP VÒNG TRÒN

### Nhịp 37 · 13:35 · KHI KHỐI ĐƯỢC XẾP QUANH BÀN

Sau những bài xếp thành hàng, ta chuyển sang bàn tròn không đánh số ghế. Sáu người phân biệt ngồi quanh bàn, A và B cần kề nhau, và hai cách chỉ khác bởi phép quay được xem như một. Phần khó là xác định số đối tượng sau khi gộp khối rồi đếm theo vòng, chứ không dùng giai thừa của hàng ngang.

**Trên màn hình:** Sáu người ngồi bàn tròn không đánh số. | A và B bắt buộc ngồi kề. | Hai cách chỉ khác phép quay xem như một.
**Ghi nhớ:** KHÔNG ÁP DỤNG CÔNG THỨC HÀNG NGANG NGUYÊN XI.

### Nhịp 38 · 13:58 · GỘP AB TRÊN BÀN TRÒN

Gộp A, B thành một đối tượng. Khi ấy quanh bàn có năm đối tượng phân biệt gồm khối AB và C, D, E, F. Muốn đếm cách xếp vòng, ta có thể cố định khối AB như một mốc rồi hoán vị bốn người còn lại. Số thứ tự vòng bên ngoài khối là bốn giai thừa, không phải năm giai thừa.

**Trên màn hình:** Khối [AB], C, D, E, F. | Có 5 đối tượng trên vòng. | Chỉ xét phép quay: (5 − 1)! cách.
**Ghi nhớ:** CỐ ĐỊNH MỘT KHỐI LÀM MỐC.

### Nhịp 39 · 14:20 · ĐẾM HAI CHIỀU TRONG KHỐI

Ở mỗi vị trí của khối trên bàn tròn, A và B vẫn có hai thứ tự quanh chiều kim đồng hồ. Nhân hai với bốn giai thừa ta được bốn mươi tám cách. Con số vô tình bằng bài năm người đứng hàng lúc đầu, nhưng hai bài có số người và mô hình đếm khác nhau. Ta phải hiểu điều kiện, không học thuộc một đáp số cố định.

**Trên màn hình:** AB hoặc BA vẫn khác nhau. | Nhân 2 với 4!. | Có 48 cách ngồi vòng.
**Ghi nhớ:** CÙNG LÀ 48 NHƯ VÍ DỤ NĂM NGƯỜI XẾP HÀNG, NHƯNG LÝ DO KHÁC.

### Nhịp 40 · 14:42 · HAI KHỐI RỜI NHAU TRÊN VÒNG

Nếu hai cặp AB và CD đều phải ngồi cạnh nhau, ta gộp thành hai khối cùng E, F, tổng cộng bốn đối tượng quanh vòng. Số thứ tự vòng là ba giai thừa. Hai khối mỗi khối có hai cách đổi chỗ nội bộ, nên có bốn nhân ba giai thừa, bằng hai mươi bốn cách. Không được lấy chín mươi sáu của bài xếp hàng.

**Trên màn hình:** [AB], [CD], E, F. | Bốn đối tượng vòng tròn: 3!. | Nhân 2² được 24 cách.
**Ghi nhớ:** CÔNG THỨC VÒNG TRÒN DÙNG (SỐ ĐỐI TƯỢNG − 1)!

### Nhịp 41 · 15:05 · BA NGƯỜI LIỀN NHAU TRÊN VÒNG

Ba bạn A, B, C cần ngồi thành ba vị trí liên tiếp quanh bàn và không bị cố định thứ tự. Gộp thành một khối cùng D, E, F, tổng cộng bốn đối tượng. Bên ngoài có ba giai thừa cách xếp vòng; bên trong có ba giai thừa cách đổi ba bạn. Tích bằng ba mươi sáu cách.

**Trên màn hình:** [ABC] cùng D, E, F: 4 đối tượng. | 3! thứ tự vòng ngoài khối. | 3! thứ tự trong khối: 36 cách.
**Ghi nhớ:** ĐẾM VÒNG VÀ ĐẾM BÊN TRONG LÀ HAI BƯỚC.

### Nhịp 42 · 15:27 · LƯU Ý NGƯỜI NÀO LÀM MỐC

Các công thức vừa sử dụng giả thiết rằng cách xếp quanh bàn tròn chỉ được đồng nhất khi có phép quay. Nếu mặt bàn hay ghế có số thứ tự cố định, phép quay không còn cho cùng cách phân công ghế. Nếu đề cho phép lật mặt vòng hạt, lại phải xét ảnh gương. Vì thế trước khi gộp khối trong bài vòng tròn, hãy kiểm tra kỹ quy ước của phép đếm.

**Trên màn hình:** Bàn tròn chỉ đồng nhất phép quay. | Không đồng nhất phép lật trái–phải. | Ghế đánh số thì cách đếm thay đổi.
**Ghi nhớ:** PHẢI NÊU RÕ QUY ƯỚC CỦA BÀI TOÁN VÒNG.


## 08 · BA CẶP CẤM KỀ NHAU

### Nhịp 43 · 15:51 · BÀI TỔNG HỢP BẢY NGƯỜI

Đến bài tổng hợp cuối, ta có bảy người phân biệt và ba cặp AB, CD, EF đều không được đứng cạnh nhau. Nếu chỉ lấy tổng số cách trừ riêng số hàng có từng cặp kề, ta sẽ trừ lặp những hàng vi phạm hai hoặc ba cặp. Đây là lúc sử dụng nguyên lý bao hàm – loại trừ với ba biến cố.

**Trên màn hình:** A, B, C, D, E, F, G xếp hàng. | Không AB, không CD, không EF kề. | Tìm số cách hợp lệ.
**Ghi nhớ:** BA ĐIỀU KIỆN CẤM KHÔNG THỂ TRỪ ĐỘC LẬP.

### Nhịp 44 · 16:14 · TỔNG VÀ MỘT BIẾN CỐ VI PHẠM

Tổng số cách xếp bảy người là bảy giai thừa, tức năm nghìn không trăm bốn mươi. Xét mỗi biến cố một cặp đứng cạnh, ta gộp hai người thành một khối nên có hai nhân sáu giai thừa, bằng một nghìn bốn trăm bốn mươi cách. Có ba biến cố như vậy; trước tiên trừ ba lần con số đó. Nhưng đây chưa phải đáp số cuối.

**Trên màn hình:** Tổng số hàng là 7! = 5040. | Mỗi cặp kề: 2 × 6! = 1440. | Ba cặp: trừ 3 × 1440.
**Ghi nhớ:** PHẢI ĐẾM ĐƯỢC CẢ TRƯỜNG HỢP GIAO NHAU.

### Nhịp 45 · 16:36 · HAI CẶP CÙNG VI PHẠM

Khi cả hai cặp chỉ định đều đứng cạnh, ta có hai khối cỡ hai cùng ba người riêng, tức năm đối tượng xếp hàng. Các khối có hai lựa chọn nội bộ mỗi khối, cho bốn nhân năm giai thừa bằng bốn trăm tám mươi cách. Chọn hai trong ba cặp được ba giao đôi. Mỗi hàng thuộc giao đôi đã bị trừ hai lần nên phải cộng lại một lần.

**Trên màn hình:** Chọn hai cặp trong ba: 3 cách. | Hai khối, còn 5 đối tượng. | Mỗi giao có 2² × 5! = 480.
**Ghi nhớ:** CỘNG LẠI VÌ VỪA BỊ TRỪ HAI LẦN.

### Nhịp 46 · 16:58 · CẢ BA CẶP CÙNG VI PHẠM

Nếu cả ba cặp đều kề nhau, ta có ba khối AB, CD, EF và một người G, tổng là bốn đối tượng. Có bốn giai thừa thứ tự ngoài và hai mũ ba thứ tự bên trong ba khối. Phần giao ba biến cố có một trăm chín mươi hai cách. Trong công thức bao hàm – loại trừ ba tập, phần giao này phải bị trừ ở bước cuối.

**Trên màn hình:** Khối [AB], [CD], [EF], và G. | Có 4 đối tượng và 2³ dạng nội bộ. | Giao ba biến cố: 2³ × 4! = 192.
**Ghi nhớ:** TRỪ PHẦN GIAO BA LẦN CUỐI CÙNG.

### Nhịp 47 · 17:21 · RÚT GỌN BIỂU THỨC

Tập hợp các hàng hợp lệ là phần bù của ba biến cố kề nhau. Theo nguyên lý bao hàm – loại trừ, ta lấy năm nghìn không trăm bốn mươi trừ ba nhân một nghìn bốn trăm bốn mươi, cộng ba nhân bốn trăm tám mươi, rồi trừ một trăm chín mươi hai. Kết quả là một nghìn chín trăm sáu mươi tám cách.

**Trên màn hình:** 5040 − 3×1440 + 3×480 − 192. | Tính được 1968. | Kiểm tra bằng liệt kê đủ 7! hàng.
**Ghi nhớ:** ĐÁP SỐ CUỐI CÙNG LÀ 1968 CÁCH.

### Nhịp 48 · 17:43 · PHƯƠNG PHÁP CHO BÀI KHÓ TIẾP THEO

Hãy kết thúc bài bằng một quy trình bốn bước: xác định điều kiện, mô hình hóa các cặp và khối, đếm số cách của từng nhóm hợp lệ hoặc vi phạm, rồi kiểm tra trùng lặp. Gộp khối rất hiệu quả khi các phần tử phải đứng cạnh nhau, nhưng không phải một công thức máy móc. Đó là nền tảng để học các bài cấm đứng cạnh ở tập tiếp theo.

**Trên màn hình:** Nhận diện các nhóm bắt buộc / bị cấm. | Xét khối rời hay khối giao nhau. | Dùng phần bù và bao hàm–loại trừ khi cần.
**Ghi nhớ:** MỖI PHÉP NHÂN PHẢI GẮN VỚI MỘT SONG ÁNH ĐÚNG.
