# SANG MATH · COMB18 V2 · TAM GIÁC PASCAL VÀ CÁC TÍNH CHẤT

## Bản thuyết minh đồng bộ

Số nhịp: 48 · 8 chương · TTS=on
Tổng thời lượng dự kiến: 1157.5 giây.
Lời giảng bên dưới là nội dung đầy đủ được đưa vào tổng hợp giọng đọc; không cắt tùy ý.


## 01 · TAM GIAC PASCAL DUOC SINH RA

### Nhịp 01 · 00:00 · HÀNG ĐẦU TIÊN

Trước khi học thuộc bất cứ công thức nào, ta hãy tạo ra tam giác Pascal từ một ô duy nhất. Ô này mang số một vì với tập hợp rỗng, có đúng một cách chọn không phần tử nào. Sự khởi đầu đơn giản ấy là nền móng cho các hàng tiếp theo. Hãy quan sát vị trí của từng ô, không chỉ nhìn con số.

**Trên màn hình:** Khởi đầu với hàng số 0. | Chỉ có một cách chọn rỗng. | Ô đầu có giá trị bằng 1.
**Ghi nhớ:** Ô đầu có giá trị bằng 1.

### Nhịp 02 · 00:24 · TỪ MỘT Ô THÀNH HAI Ô

Khi có một phần tử A, ta có thể không chọn A hoặc chọn đúng A. Mỗi trường hợp chỉ có một cách. Vì vậy hàng tiếp theo gồm hai số một. Hãy chú ý hai ô ở rìa được đặt lệch so với ô phía trên. Chính cách đặt này sẽ làm xuất hiện quy tắc cộng hai ô kề nhau.

**Trên màn hình:** Thêm hàng ứng với n bằng 1. | Hai ô biên luôn bằng 1. | Có chọn hoặc không chọn một phần tử.
**Ghi nhớ:** Có chọn hoặc không chọn một phần tử.

### Nhịp 03 · 00:48 · HÀNG CỦA HAI PHẦN TỬ

Ta bổ sung phần tử B. Chọn không phần tử nào vẫn có một cách, chọn cả hai phần tử cũng chỉ có một cách. Nhưng chọn đúng một phần tử có hai cách: chọn A hoặc chọn B. Hai cách ấy được biểu diễn bằng số hai ở chính giữa. Hàng mới hiện ra là một, hai, một.

**Trên màn hình:** Đặt hai số 1 ở hai biên. | Giữa hai biên sinh ra số 2. | Hàng thứ hai có dạng 1, 2, 1.
**Ghi nhớ:** Hàng thứ hai có dạng 1, 2, 1.

### Nhịp 04 · 01:12 · HÀNG THỨ BA

Sang ba phần tử, các nhóm chọn một phần tử là A, B hoặc C nên có ba cách. Các nhóm chọn hai phần tử cũng có ba cách. Bởi thế ta nhận được hàng một, ba, ba, một. Ở đây hình ảnh trực quan và kết quả đếm tổ hợp trùng khớp. Ta sẽ sớm giải thích tại sao hai số ở phía trên lại được cộng với nhau.

**Trên màn hình:** Các ô giữa nhận số từ hai ô trên. | Nhận được 1, 3, 3, 1. | Đối chiếu với các nhóm chọn 1 hoặc 2.
**Ghi nhớ:** Đối chiếu với các nhóm chọn 1 hoặc 2.

### Nhịp 05 · 01:36 · HÀNG THỨ TƯ

Khi xây dựng hàng của bốn phần tử, các ô giữa lần lượt mang số bốn, sáu và bốn. Toàn bộ hàng là một, bốn, sáu, bốn, một. Nếu quan sát kỹ, ta thấy các số bên trái và bên phải đối xứng nhau. Hãy thử đoán hàng tiếp theo trước khi các con số hiện ra trên màn hình.

**Trên màn hình:** Giữ hai ô biên bằng 1. | Ba ô giữa có giá trị 4, 6, 4. | Tam giác trở nên cân đối.
**Ghi nhớ:** Tam giác trở nên cân đối.

### Nhịp 06 · 02:00 · DỰ ĐOÁN HÀNG MỚI

Ta có thể dự đoán hàng thứ năm bằng cách giữ hai số một ở biên, rồi cộng từng cặp ô kề nhau của hàng thứ tư. Kết quả là một, năm, mười, mười, năm, một. Tổng các hệ số là ba mươi hai. Số ba mươi hai còn liên quan đến số tập con của một tập có năm phần tử, một kết nối rất đáng chú ý.

**Trên màn hình:** Hàng thứ năm có sáu ô. | Quy tắc cộng cho ra 1,5,10,10,5,1. | Tổng sáu ô bằng 32.
**Ghi nhớ:** Tổng sáu ô bằng 32.


## 02 · QUY TAC CONG HAI O KE NHAU

### Nhịp 07 · 02:24 · QUAN SÁT HAI Ô CHA

Bây giờ hãy tập trung vào ô có giá trị sáu ở giữa hàng thứ tư. Hai mũi tên xuất phát từ hai ô mang số ba ở hàng thứ ba cùng đi tới ô này. Ba cộng ba bằng sáu. Đây không phải một mẹo tính tự nhiên xuất hiện; phía sau nó là cách phân chia các lựa chọn thành hai nhóm không giao nhau.

**Trên màn hình:** Chọn một ô ở giữa hàng thứ tư. | Nối ô ấy với hai ô hàng trên. | Hai nhánh cùng dẫn đến một ô con.
**Ghi nhớ:** Hai nhánh cùng dẫn đến một ô con.

### Nhịp 08 · 02:48 · QUY TẮC CHO MỖI Ô GIỮA

Với một ô bất kỳ không nằm trên biên, hãy nhìn hai ô ngay phía trên: một ở góc trái và một ở góc phải. Giá trị ô mới bằng tổng hai giá trị đó. Viết bằng kí hiệu tổ hợp, ta được hệ thức Pascal. Chỉ số trên biểu diễn số phần tử của tập, chỉ số dưới biểu diễn số phần tử cần chọn, đúng theo quy ước của Series.

**Trên màn hình:** Hai ô phía trên nằm chéo trái và phải. | Cộng chúng để được ô phía dưới. | Ô biên vẫn luôn là 1.
**Ghi nhớ:** Ô biên vẫn luôn là 1.

### Nhịp 09 · 03:12 · ÁP DỤNG Ở HÀNG THỨ NĂM

Hãy dùng hệ thức vừa học để tính số mười thứ nhất ở hàng năm. Hai ô cha của nó có giá trị bốn và sáu. Cộng lại được mười. Với số mười còn lại, ta lấy sáu cộng bốn. Khi hoạt hình làm sáng hai mũi tên, chúng ta có thể nhìn thấy trực tiếp nguồn gốc của mỗi ô mới, không cần ghi nhớ một dãy số dài.

**Trên màn hình:** Muốn tính số 10 thứ nhất. | Lấy 4 cộng 6 của hàng trước. | Số 10 thứ hai bằng 6 cộng 4.
**Ghi nhớ:** Số 10 thứ hai bằng 6 cộng 4.

### Nhịp 10 · 03:36 · KIỂM TRA HÀNG SÁU

Nếu tiếp tục một hàng nữa, số ở giữa hàng sáu nhận hai số mười phía trên, cho kết quả hai mươi. Hai ô kế bên nhận năm cộng mười, được mười lăm. Cả hàng là một, sáu, mười lăm, hai mươi, mười lăm, sáu, một. Chúng ta đã có một thuật toán rất đơn giản để tạo toàn bộ tam giác Pascal.

**Trên màn hình:** Bắt đầu từ 1,5,10,10,5,1. | Tạo hàng 1,6,15,20,15,6,1. | Kiểm tra số giữa bằng 10+10.
**Ghi nhớ:** Kiểm tra số giữa bằng 10+10.

### Nhịp 11 · 04:00 · TRƯỜNG HỢP BIÊN

Tại hai mép của tam giác, ta không có đủ hai ô cha. Nhưng mỗi ô biên vẫn mang số một vì chỉ có một cách chọn không phần tử hoặc chọn hết các phần tử. Khi muốn viết quy tắc cộng thống nhất, ta có thể xem các ô nằm bên ngoài tam giác có giá trị không. Cách quy ước này giúp thuật toán gọn gàng và chính xác.

**Trên màn hình:** Không có ô cha phía ngoài tam giác. | Ô đầu và ô cuối luôn là 1. | Quy ước giá trị ngoài miền bằng 0.
**Ghi nhớ:** Quy ước giá trị ngoài miền bằng 0.

### Nhịp 12 · 04:24 · TỔNG QUÁT THUẬT TOÁN

Ta có thể nhờ máy tính sinh hàng thứ mười, thứ hai mươi, thậm chí hàng thứ một trăm mà không cần khai triển nhị thức. Bắt đầu với hàng chỉ gồm một số một. Trong mỗi bước, đặt một ở hai đầu và điền các số ở giữa bằng cách cộng hai số kề của hàng trước. Bài toán tổ hợp vì vậy trở thành một quy trình tính toán có thể kiểm chứng từng bước.

**Trên màn hình:** Khởi đầu bằng hàng [1]. | Chèn 1 ở hai đầu hàng tiếp theo. | Ô giữa là tổng hai ô kề hàng cũ.
**Ghi nhớ:** Ô giữa là tổng hai ô kề hàng cũ.


## 03 · CHUNG MINH BANG HAI CACH DEM

### Nhịp 13 · 04:48 · BÀI TOÁN CHỌN BA NGƯỜI

Chúng ta sẽ chứng minh vì sao hai ô cha phải cộng với nhau. Cho sáu học sinh phân biệt, hỏi có bao nhiêu cách chọn ba học sinh thành một nhóm. Ta biết kết quả là hai mươi. Nhưng thay vì tính bằng giai thừa ngay, hãy chọn riêng bạn A làm đối tượng đặc biệt và chia các nhóm thành hai loại.

**Trên màn hình:** Có sáu học sinh A,B,C,D,E,F. | Chọn nhóm ba người, không xét thứ tự. | Số nhóm bằng 20.
**Ghi nhớ:** Số nhóm bằng 20.

### Nhịp 14 · 05:12 · NHÓM CÓ A

Trường hợp thứ nhất, nhóm được chọn có bạn A. Khi đó A đã chiếm một trong ba vị trí của nhóm, chúng ta chỉ cần chọn thêm hai người từ năm bạn B, C, D, E và F. Có mười cách. Mọi nhóm chứa A đều xuất hiện đúng một lần trong phép đếm này.

**Trên màn hình:** Nếu A có mặt trong nhóm. | Chọn thêm hai người từ năm bạn còn lại. | Số cách bằng 10.
**Ghi nhớ:** Số cách bằng 10.

### Nhịp 15 · 05:36 · NHÓM KHÔNG CÓ A

Trường hợp thứ hai, nhóm không có A. Toàn bộ ba thành viên phải được chọn từ năm bạn còn lại, nên có đúng mười cách. Một nhóm không thể vừa có A vừa không có A. Hai nhóm trường hợp này tách biệt hoàn toàn, đó là điều kiện cho phép ta sử dụng quy tắc cộng.

**Trên màn hình:** Nếu A không được chọn. | Cần chọn đủ ba người từ năm bạn. | Số cách cũng bằng 10.
**Ghi nhớ:** Số cách cũng bằng 10.

### Nhịp 16 · 06:00 · GHÉP HAI TRƯỜNG HỢP

Khi ghép hai loại nhóm, ta thu được mười cộng mười bằng hai mươi. Đây chính là ba ô nằm theo hình chữ vê trong tam giác Pascal: hai số mười ở trên và số hai mươi phía dưới. Như vậy quy tắc cộng hai ô cha không còn là một quan sát ngẫu nhiên mà xuất phát từ phép đếm cùng một tập kết quả theo hai trường hợp.

**Trên màn hình:** Có A: 10 nhóm. | Không có A: 10 nhóm. | Cộng để được 20 nhóm.
**Ghi nhớ:** Cộng để được 20 nhóm.

### Nhịp 17 · 06:24 · CHỨNG MINH CHO n, k

Với một tập gồm n phần tử, ta muốn chọn k phần tử. Chọn một phần tử A làm mốc. Nếu có A, ta chọn thêm k trừ một phần tử từ n trừ một phần tử còn lại. Nếu không có A, ta chọn đủ k phần tử từ phần còn lại. Hai trường hợp phủ kín và không giao nhau, nên cộng số cách lại được hệ thức Pascal tổng quát.

**Trên màn hình:** Đánh dấu một phần tử đặc biệt A. | Có A: chọn k-1 trong n-1. | Không A: chọn k trong n-1.
**Ghi nhớ:** Không A: chọn k trong n-1.

### Nhịp 18 · 06:48 · TẠI SAO KHÔNG ĐẾM TRÙNG?

Điểm quan trọng nhất của một chứng minh tổ hợp là kiểm tra hai việc: không đếm trùng và không bỏ sót. Ở đây, mọi nhóm hoặc chứa A hoặc không chứa A, không có khả năng thứ ba. Đồng thời hai tính chất ấy không thể xảy ra cùng lúc. Vì vậy phép cộng là hợp lệ, và chúng ta đã chứng minh được bản chất của tam giác Pascal.

**Trên màn hình:** Mỗi nhóm thuộc đúng một trong hai loại. | Không có nhóm vừa chứa vừa thiếu A. | Không có nhóm nào bị bỏ sót.
**Ghi nhớ:** Không có nhóm nào bị bỏ sót.


## 04 · DOI XUNG VA PHEP LAY PHAN BU

### Nhịp 19 · 07:12 · QUAN SÁT HÀNG ĐỐI XỨNG

Hãy quan sát hàng thứ sáu. Nếu gập hàng này qua chính giữa, những con số ở hai phía sẽ trùng khít: một đi với một, sáu đi với sáu, mười lăm đi với mười lăm. Tại sao một tính chất hình ảnh đẹp như vậy lại đúng với mọi hàng, chứ không phải chỉ đúng ở vài ví dụ đầu?

**Trên màn hình:** Hàng thứ sáu: 1,6,15,20,15,6,1. | Hai ô cách đều trung tâm bằng nhau. | Cặp chỉ số k và 6-k.
**Ghi nhớ:** Cặp chỉ số k và 6-k.

### Nhịp 20 · 07:36 · CHỌN VÀ KHÔNG CHỌN

Tưởng tượng sáu thẻ học sinh. Mỗi khi chọn hai thẻ vào nhóm, ta đồng thời xác định chính xác bốn thẻ không được chọn. Ngược lại, biết bốn thẻ bị bỏ lại thì suy ra ngay hai thẻ được chọn. Đây là một phép tương ứng một đối một giữa hai tập kết quả, nên hai tập có cùng số phần tử.

**Trên màn hình:** Chọn hai phần tử trong sáu. | Tương ứng với bỏ lại bốn phần tử. | Hai thao tác xác định nhau duy nhất.
**Ghi nhớ:** Hai thao tác xác định nhau duy nhất.

### Nhịp 21 · 08:00 · CÔNG THỨC ĐỐI XỨNG

Một tập gồm n phần tử được tách thành nhóm chọn k phần tử và nhóm không chọn n trừ k phần tử. Hai nhóm bổ sung nhau, nên một nhóm xác định hoàn toàn nhóm còn lại. Do đó, số cách chọn k phần tử bằng số cách chọn n trừ k phần tử. Tính đối xứng của các hàng Pascal thực ra là tính đối xứng của phép lấy phần bù.

**Trên màn hình:** Chọn k đồng nghĩa với bỏ n-k. | Phép tương ứng có hai chiều. | Hai số tổ hợp bằng nhau.
**Ghi nhớ:** Hai số tổ hợp bằng nhau.

### Nhịp 22 · 08:24 · TÍNH NHANH BẰNG ĐỐI XỨNG

Ta thử áp dụng vào một bài tính nhanh. Số cách chọn hai học sinh từ tám học sinh bằng hai mươi tám. Vì chọn hai người tương đương với chỉ định sáu người bị loại, số cách chọn sáu người cũng bằng hai mươi tám. Khi gặp k lớn gần n, đổi sang n trừ k thường làm phép tính ngắn hơn và dễ kiểm tra hơn.

**Trên màn hình:** Không cần tính lại hai phía. | Biết C của 2 từ 8 suy ra C của 6 từ 8. | Kết quả đều bằng 28.
**Ghi nhớ:** Kết quả đều bằng 28.

### Nhịp 23 · 08:48 · Ô GIỮA CỦA HÀNG CHẴN

Với hàng có chỉ số chẵn, ta tìm thấy một ô đúng ở giữa, chẳng hạn số hai mươi của hàng sáu. Những hệ số thường tăng dần về giữa rồi giảm dần sau giữa. Chúng ta có thể giải thích bằng tỉ số giữa hai hệ số kề nhau, nhưng ở đây trước hết hãy nhìn cách giá trị lan truyền và tích lũy từ hai phía qua từng hàng.

**Trên màn hình:** Hàng chẵn có một ô chính giữa. | Số C của n/2 trong n đạt cực đại. | Hai phía tăng rồi giảm đối xứng.
**Ghi nhớ:** Hai phía tăng rồi giảm đối xứng.

### Nhịp 24 · 09:12 · HÀNG LẺ VÀ HAI Ô GIỮA

Đối với hàng mang chỉ số lẻ, chính giữa có hai ô bằng nhau. Hàng thứ năm chẳng hạn có hai số mười nằm cạnh nhau. Tính đối xứng cho biết ngay chúng phải bằng nhau, bởi hai chỉ số hai và ba cộng lại bằng năm. Quan sát này giúp học sinh nhận dạng cấu trúc hàng Pascal mà không cần ghi nhớ toàn bộ bảng số.

**Trên màn hình:** Hàng lẻ có hai ô giữa bằng nhau. | Hàng 5 có hai số 10 ở giữa. | Kiểm tra bằng công thức đối xứng.
**Ghi nhớ:** Kiểm tra bằng công thức đối xứng.


## 05 · TONG CAC HANG VA DAU XEN KE

### Nhịp 25 · 09:36 · TỔNG TỪNG HÀNG

Ta chuyển sang một tính chất rất đẹp: tổng các số trên từng hàng. Các hàng đầu có tổng một, hai, bốn, tám, mười sáu và ba mươi hai. Mỗi khi số phần tử tăng một đơn vị, số tập con tăng gấp đôi vì phần tử mới có thể được chọn hoặc không được chọn. Điều đó cho ta công thức tổng hàng bằng hai mũ n.

**Trên màn hình:** Hàng 0 có tổng 1. | Hàng 1 có tổng 2, hàng 2 có tổng 4. | Mỗi hàng sau gấp đôi hàng trước.
**Ghi nhớ:** Mỗi hàng sau gấp đôi hàng trước.

### Nhịp 26 · 10:00 · KIỂM TRA HÀNG SÁU

Hãy kiểm tra cụ thể trên hàng sáu. Cộng một, sáu, mười lăm, hai mươi, mười lăm, sáu và một, ta được sáu mươi bốn. Một tập có sáu phần tử cũng có sáu mươi bốn tập con vì mỗi phần tử có đúng hai trạng thái được chọn hoặc không được chọn. Hai lập luận dẫn tới cùng một kết quả.

**Trên màn hình:** Hàng 6: 1,6,15,20,15,6,1. | Cộng tất cả được 64. | Bằng số tập con của 6 phần tử.
**Ghi nhớ:** Bằng số tập con của 6 phần tử.

### Nhịp 27 · 10:24 · NHÌN TỪ NHỊ THỨC NEWTON

Còn một cách chứng minh đại số cực ngắn. Trong khai triển Nhị thức Newton, thay cả a và b bằng một. Vế trái là hai mũ n. Ở vế phải, mọi đơn thức còn lại đúng bằng một, nên chỉ còn tổng các hệ số tổ hợp. Đây là cách kết nối trực tiếp Video 17 với tam giác Pascal đang được xây dựng.

**Trên màn hình:** Thay a bằng 1 và b bằng 1. | Vế trái trở thành 2 mũ n. | Vế phải là tổng các hệ số.
**Ghi nhớ:** Vế phải là tổng các hệ số.

### Nhịp 28 · 10:48 · CỘNG XEN DẤU

Bây giờ, thay vì cộng tất cả các ô, ta gắn dấu cộng và trừ xen kẽ. Với hàng sáu, biểu thức một trừ sáu cộng mười lăm trừ hai mươi cộng mười lăm trừ sáu cộng một bằng không. Đó là vì theo Nhị thức Newton, tổng xen dấu chính là một trừ một, tất cả lũy thừa n, nên bằng không khi n dương.

**Trên màn hình:** Lấy tổng các hệ số với dấu xen kẽ. | Hàng sáu: 1-6+15-20+15-6+1. | Kết quả bằng 0.
**Ghi nhớ:** Kết quả bằng 0.

### Nhịp 29 · 11:12 · CHẴN VÀ LẺ CÂN BẰNG

Từ hai công thức tổng hàng và tổng xen dấu, ta rút ra rằng tổng hệ số tại các vị trí k chẵn bằng tổng hệ số ở vị trí k lẻ, mỗi bên bằng hai mũ n trừ một với n dương. Ở hàng sáu, mỗi phía bằng ba mươi hai. Đây là một ví dụ về cách dùng hai phương trình để xác định hai tổng chưa biết.

**Trên màn hình:** Tổng hệ số ở cột k chẵn. | Tổng hệ số ở cột k lẻ. | Mỗi tổng bằng 2 mũ n-1.
**Ghi nhớ:** Mỗi tổng bằng 2 mũ n-1.

### Nhịp 30 · 11:36 · LƯU Ý TRƯỜNG HỢP n BẰNG 0

Một lưu ý nhỏ nhưng quan trọng: công thức tổng xen dấu bằng không cần điều kiện n lớn hơn không. Với n bằng không, hàng Pascal chỉ có một ô bằng một và tổng xen dấu cũng bằng một. Nếu bỏ quên điều kiện biên, ta có thể dùng một đẳng thức đúng trong phần lớn trường hợp nhưng sai ngay ở điểm khởi đầu. Tính chính xác toán học bắt đầu từ những chi tiết như vậy.

**Trên màn hình:** Tổng hàng luôn là 2 mũ n. | Tổng xen dấu bằng 0 khi n dương. | Với n bằng 0, tổng xen dấu bằng 1.
**Ghi nhớ:** Với n bằng 0, tổng xen dấu bằng 1.


## 06 · DUONG CHEO VA HINH GAY KHUC

### Nhịp 31 · 12:00 · ĐƯỜNG CHÉO TRONG PASCAL

Bên cạnh từng hàng ngang, tam giác Pascal còn chứa nhiều cấu trúc thú vị theo đường chéo. Hãy tô sáng bốn số một, ba, sáu và mười theo một đường chéo đi xuống. Khi cộng chúng ta được hai mươi. Số hai mươi xuất hiện ở một vị trí khác của tam giác, giống như hình một chiếc gậy khúc côn cầu với phần cán và đầu cong.

**Trên màn hình:** Chọn một đường chéo hướng xuống. | Giá trị lần lượt 1,3,6,10. | Tổng các giá trị là 20.
**Ghi nhớ:** Tổng các giá trị là 20.

### Nhịp 32 · 12:24 · VIẾT DƯỚI DẠNG TỔ HỢP

Bốn giá trị trên có thể viết thành tổ hợp chập hai của hai, ba, bốn và năm. Cộng chúng ta được tổ hợp chập ba của sáu, tức hai mươi. Tên gọi hình gậy khúc côn cầu giúp chúng ta nhớ vị trí của các ô, nhưng điều quan trọng hơn là hiểu phép đếm nào đứng phía sau phép cộng theo đường chéo.

**Trên màn hình:** Bốn số thuộc các hàng 2,3,4,5. | Cùng có chỉ số dưới bằng 2. | Tổng bằng số tổ hợp chọn 3 từ 6.
**Ghi nhớ:** Tổng bằng số tổ hợp chọn 3 từ 6.

### Nhịp 33 · 12:48 · GIẢI THÍCH BẰNG PHẦN TỬ LỚN NHẤT

Hãy đếm các tập ba phần tử chọn từ các số một đến sáu. Mỗi tập có một phần tử lớn nhất, chỉ có thể là ba, bốn, năm hoặc sáu. Nếu phần tử lớn nhất bằng t, ta cần chọn hai phần tử trong t trừ một số nhỏ hơn nó. Số cách tương ứng lần lượt là một, ba, sáu và mười. Cộng bốn trường hợp sẽ được hai mươi.

**Trên màn hình:** Chọn ba số từ 1 đến 6. | Phân loại theo số lớn nhất: 3,4,5,6. | Phần còn lại chọn hai số nhỏ hơn.
**Ghi nhớ:** Phần còn lại chọn hai số nhỏ hơn.

### Nhịp 34 · 13:12 · HÌNH GẬY KHÚC CÔN CẦU

Nếu kéo dài lập luận vừa rồi, ta nhận được đẳng thức tổng quát: tổng các số tổ hợp có cùng chỉ số dưới k, chạy từ hàng k đến hàng n, bằng số tổ hợp với chỉ số trên n cộng một và chỉ số dưới k cộng một. Trong hình, các ô nằm trên cán gậy được tô xanh; ô kết quả ở đầu gậy được tô vàng.

**Trên màn hình:** Các ô trên cán gậy cùng chỉ số k. | Ô đích lệch sang phải một vị trí. | Quan sát phép cộng tích lũy.
**Ghi nhớ:** Quan sát phép cộng tích lũy.

### Nhịp 35 · 13:36 · KIỂM TRA MỘT VÍ DỤ KHÁC

Ta kiểm tra thêm một ví dụ dễ tính nhẩm: một cộng hai cộng ba cộng bốn bằng mười. Các số một, hai, ba, bốn chính là số tổ hợp chập một của một, hai, ba, bốn; kết quả mười bằng số tổ hợp chập hai của năm. Ví dụ này cho thấy đẳng thức đường chéo không chỉ đúng tại một vị trí đặc biệt.

**Trên màn hình:** Chọn k bằng 1, n bằng 4. | Tổng 1+2+3+4 bằng 10. | Đúng bằng C chọn 2 từ 5.
**Ghi nhớ:** Đúng bằng C chọn 2 từ 5.

### Nhịp 36 · 14:00 · KHI NÀO NÊN DÙNG?

Khi gặp một tổng dài gồm các số tổ hợp cùng chỉ số dưới, còn chỉ số trên tăng đều qua từng số nguyên liên tiếp, hãy nghĩ đến công thức đường chéo. Thay vì tính từng số hạng rồi cộng, ta có thể viết gọn thành một tổ hợp duy nhất. Nhưng cần kiểm tra cẩn thận điểm đầu, điểm cuối và chỉ số tăng thêm để không lệch một đơn vị.

**Trên màn hình:** Gặp tổng các C có cùng chỉ số dưới. | Kiểm tra chỉ số trên tăng liên tiếp. | Thay phép cộng dài bằng một tổ hợp.
**Ghi nhớ:** Thay phép cộng dài bằng một tổ hợp.


## 07 · CHAN LE VA HOA TIET TUONG TU

### Nhịp 37 · 14:24 · TÔ MÀU THEO TÍNH CHẴN LẺ

Đến đây, ta khám phá một lớp hình ảnh khác của tam giác Pascal. Thay vì đọc toàn bộ số lớn, hãy chỉ quan tâm một ô là chẵn hay lẻ. Tô sáng các ô lẻ và làm mờ những ô chẵn. Dần dần xuất hiện một họa tiết lặp lại rất đẹp. Manim sẽ cho hiện nhiều hàng liên tiếp để học sinh quan sát quy luật.

**Trên màn hình:** Ô lẻ tô sáng, ô chẵn để tối. | Các hàng đầu tạo một hoa văn lặp. | Chỉ quan tâm số dư khi chia 2.
**Ghi nhớ:** Chỉ quan tâm số dư khi chia 2.

### Nhịp 38 · 14:48 · CỘNG THEO PHÉP TOÁN MODULO 2

Ta vẫn dùng đúng quy tắc Pascal: ô mới bằng tổng hai ô phía trên. Nhưng khi chỉ quan sát tính chẵn lẻ, lẻ cộng lẻ tạo thành chẵn, còn chẵn cộng lẻ tạo thành lẻ. Vì thế các ô sáng và tối tiếp tục sinh ra hình mới theo một quy luật cục bộ rất đơn giản. Đây là cách một cấu trúc lớn nảy sinh từ phép tính nhỏ.

**Trên màn hình:** Lẻ cộng lẻ thành chẵn. | Chẵn cộng lẻ thành lẻ. | Hàng mới vẫn cộng hai ô phía trên.
**Ghi nhớ:** Hàng mới vẫn cộng hai ô phía trên.

### Nhịp 39 · 15:12 · HÀNG CHỈ SỐ 7 TOÀN SỐ LẺ

Ở hàng mang chỉ số bảy, các hệ số lần lượt là một, bảy, hai mươi mốt, ba mươi lăm, ba mươi lăm, hai mươi mốt, bảy và một. Tất cả đều lẻ. Trong mô hình chẵn lẻ, cả hàng sẽ sáng lên. Đây là dấu hiệu đặc biệt giúp chia hoa văn thành những khối nhỏ giống nhau ở nhiều mức độ.

**Trên màn hình:** Các số hàng 7 là 1,7,21,35,35,21,7,1. | Tất cả đều lẻ. | Một dải sáng xuất hiện trọn hàng.
**Ghi nhớ:** Một dải sáng xuất hiện trọn hàng.

### Nhịp 40 · 15:36 · HÀNG CHỈ SỐ 8 CHỈ SÁNG Ở BIÊN

Khi chuyển sang hàng tám, chỉ hai ô ở hai mép có giá trị lẻ. Các ô còn lại đều chẵn nên chuyển sang màu tối. Sự thay đổi đột ngột này tạo thành khoảng trống đặc trưng trong họa tiết tam giác. Nếu tiếp tục đến hàng mười lăm và mười sáu, ta sẽ quan sát những bước lặp lại tương tự.

**Trên màn hình:** Hàng 8 có 1 ở hai đầu. | Những ô ở giữa đều chẵn. | Hai điểm sáng nằm tại biên.
**Ghi nhớ:** Hai điểm sáng nằm tại biên.

### Nhịp 41 · 16:00 · HOA VĂN SIERPINSKI

Khi tô sáng các số lẻ trong ba mươi hai hàng Pascal, ta nhìn thấy các tam giác nhỏ nằm trong tam giác lớn, một hoa văn gần với tam giác Sierpinski. Điều bất ngờ là hình ảnh này không cần thêm quy tắc vẽ riêng. Chúng ta chỉ lặp phép cộng hai ô cha rồi lấy số dư chia hai. Toán tổ hợp, số học và hình học kết nối với nhau qua một hình động.

**Trên màn hình:** Hiển thị 32 hàng với độ tương phản cao. | Nhận diện những tam giác lồng nhau. | Tất cả sinh từ quy tắc cộng.
**Ghi nhớ:** Tất cả sinh từ quy tắc cộng.

### Nhịp 42 · 16:24 · KHÁM PHÁ, KHÔNG ĐOÁN VÔ CĂN CỨ

Hình ảnh khiến ta muốn dự đoán rằng tam giác Pascal có tính tự đồng dạng khi xét theo modulo hai. Tuy nhiên, xem một số hàng chưa đủ để kết luận cho mọi hàng. Muốn chứng minh tổng quát cần thêm công cụ về hệ số nhị thức và số học, chẳng hạn cách viết số theo hệ nhị phân. Ở đây, ta dùng hình động để khám phá và khơi gợi câu hỏi mới.

**Trên màn hình:** Họa tiết là bằng chứng quan sát. | Chứng minh cần định lý số học sâu hơn. | Phân biệt dự đoán và chứng minh.
**Ghi nhớ:** Phân biệt dự đoán và chứng minh.


## 08 · HE SO VA BAI TOAN TONG HOP

### Nhịp 43 · 16:48 · BÀI TOÁN HỆ SỐ

Bài toán cuối tập yêu cầu tìm hệ số của x mũ ba trong tích một cộng x mũ năm nhân với một cộng x mũ ba. Ta có thể gộp hai lũy thừa thành một cộng x mũ tám. Khi đó hệ số cần tìm chính là số cách chọn ba trong tám nhân tử để lấy x. Hãy thử dự đoán kết quả từ hàng thứ tám của tam giác Pascal.

**Trên màn hình:** Tìm hệ số của x mũ 3. | Biểu thức là (1+x)^5(1+x)^3. | Có tất cả 8 nhân tử (1+x).
**Ghi nhớ:** Có tất cả 8 nhân tử (1+x).

### Nhịp 44 · 17:12 · CÁCH MỘT: GỘP HAI LŨY THỪA

Theo cách thứ nhất, ta đơn giản hóa tích ban đầu thành một cộng x mũ tám. Hàng thứ tám của Pascal có hệ số thứ ba bằng năm mươi sáu nếu đánh chỉ số bắt đầu từ không. Vậy hệ số của x mũ ba là năm mươi sáu. Phương pháp này nhanh, nhưng chúng ta còn có thể tự kiểm chứng bằng cách phân chia các nhân tử thành hai nhóm.

**Trên màn hình:** Gộp thành (1+x)^8. | Đọc ô k bằng 3 của hàng 8. | Nhận được 56.
**Ghi nhớ:** Nhận được 56.

### Nhịp 45 · 17:36 · CÁCH HAI: CHIA PHẦN CHỌN x

Ở cách thứ hai, giữ hai nhóm nhân tử riêng biệt. Giả sử ta chọn i ngoặc lấy x trong nhóm năm ngoặc, thì phải chọn ba trừ i ngoặc lấy x trong nhóm ba ngoặc còn lại. Vì tổng số chữ x cần đúng bằng ba, i chỉ có thể nhận bốn giá trị không, một, hai và ba. Mỗi trường hợp có số cách tính bằng tích hai tổ hợp.

**Trên màn hình:** Chọn i chữ x trong nhóm năm ngoặc. | Chọn 3-i chữ x trong nhóm ba ngoặc. | Có bốn giá trị i: 0,1,2,3.
**Ghi nhớ:** Có bốn giá trị i: 0,1,2,3.

### Nhịp 46 · 18:00 · LIỆT KÊ BỐN TRƯỜNG HỢP

Ta tính lần lượt bốn trường hợp. Nếu không chọn x từ nhóm năm ngoặc thì nhóm ba ngoặc phải chọn cả ba, có một cách. Nếu chọn một x ở nhóm thứ nhất thì có mười lăm cách. Nếu chọn hai x thì có ba mươi cách. Nếu chọn ba x thì có mười cách. Cộng lại bằng năm mươi sáu, đúng với cách một.

**Trên màn hình:** i=0 đóng góp 1. | i=1 đóng góp 15; i=2 đóng góp 30. | i=3 đóng góp 10.
**Ghi nhớ:** i=3 đóng góp 10.

### Nhịp 47 · 18:24 · ĐẲNG THỨC VANDERMONDE

Hai phép đếm vừa rồi tính cùng một đối tượng: chọn ba vị trí từ tám vị trí. Một cách coi tất cả là một tập lớn, cách còn lại chia trước thành nhóm năm và nhóm ba. Vì cùng đếm một tập kết quả, hai biểu thức phải bằng nhau. Đây là trường hợp cụ thể của đồng nhất thức Vandermonde, một chủ đề chúng ta sẽ tiếp tục nghiên cứu ở các video sau.

**Trên màn hình:** Hai cách đếm cùng một tập lựa chọn. | Gộp tám phần tử hoặc chia thành hai nhóm 5-3. | Tổng các tích tổ hợp bằng 56.
**Ghi nhớ:** Tổng các tích tổ hợp bằng 56.

### Nhịp 48 · 18:48 · TỔNG KẾT TAM GIÁC PASCAL

Chúng ta đã đi từ một ô mang số một đến nhiều tính chất sâu sắc. Tam giác Pascal cho phép tính các tổ hợp nhờ cộng hai ô cha, chứng minh tính đối xứng, tổng hệ số, hệ thức đường chéo, và khám phá các hoa văn chẵn lẻ. Cuối cùng, nó trở thành công cụ mạnh để tìm hệ số trong khai triển nhị thức. Quan trọng nhất, mỗi công thức đều được gắn với một cách đếm có ý nghĩa.

**Trên màn hình:** Hàng được sinh từ hai ô cha. | Đối xứng, tổng hàng, đường chéo. | Tính chẵn lẻ và bài tìm hệ số.
**Ghi nhớ:** Tính chẵn lẻ và bài tìm hệ số.
