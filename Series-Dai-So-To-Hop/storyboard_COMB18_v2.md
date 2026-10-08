# COMB18 V2 - Storyboard 48 nhip / 8 chuong

**Phuong phap:** Manim render mo hinh ben trai; Typst render cong thuc ben phai. De va gia thiet phai duoc doc truoc khi ket luan xuat hien.
**Thoi luong:** 48 nhip x 24 giay + ket bai ~5.2 giay = 19:17 (khong TTS). Voice=on tu dong mo rong nhip theo MP3.

**Minh hoa:** `preview/comb18_v2/storyboard_8_chapters.png` la anh phac thao, chua phai khung hinh Manim that.

## 01 · TAM GIAC PASCAL DUOC SINH RA

### 01 - HÀNG ĐẦU TIÊN
- Mo hinh: `growth` - trang thai 0; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Khởi đầu với hàng số 0.; Chỉ có một cách chọn rỗng.; Ô đầu có giá trị bằng 1.
- Typst: `growth_0`.
- Loi giang: Trước khi học thuộc bất cứ công thức nào, ta hãy tạo ra tam giác Pascal từ một ô duy nhất. Ô này mang số một vì với tập hợp rỗng, có đúng một cách chọn không phần tử nào. Sự khởi đầu đơn giản ấy là nền móng cho các hàng tiếp theo. Hãy quan sát vị trí của từng ô, không chỉ nhìn con số.

### 02 - TỪ MỘT Ô THÀNH HAI Ô
- Mo hinh: `growth` - trang thai 1; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Thêm hàng ứng với n bằng 1.; Hai ô biên luôn bằng 1.; Có chọn hoặc không chọn một phần tử.
- Typst: `growth_1`.
- Loi giang: Khi có một phần tử A, ta có thể không chọn A hoặc chọn đúng A. Mỗi trường hợp chỉ có một cách. Vì vậy hàng tiếp theo gồm hai số một. Hãy chú ý hai ô ở rìa được đặt lệch so với ô phía trên. Chính cách đặt này sẽ làm xuất hiện quy tắc cộng hai ô kề nhau.

### 03 - HÀNG CỦA HAI PHẦN TỬ
- Mo hinh: `growth` - trang thai 2; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Đặt hai số 1 ở hai biên.; Giữa hai biên sinh ra số 2.; Hàng thứ hai có dạng 1, 2, 1.
- Typst: `growth_2`.
- Loi giang: Ta bổ sung phần tử B. Chọn không phần tử nào vẫn có một cách, chọn cả hai phần tử cũng chỉ có một cách. Nhưng chọn đúng một phần tử có hai cách: chọn A hoặc chọn B. Hai cách ấy được biểu diễn bằng số hai ở chính giữa. Hàng mới hiện ra là một, hai, một.

### 04 - HÀNG THỨ BA
- Mo hinh: `growth` - trang thai 3; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Các ô giữa nhận số từ hai ô trên.; Nhận được 1, 3, 3, 1.; Đối chiếu với các nhóm chọn 1 hoặc 2.
- Typst: `growth_3`.
- Loi giang: Sang ba phần tử, các nhóm chọn một phần tử là A, B hoặc C nên có ba cách. Các nhóm chọn hai phần tử cũng có ba cách. Bởi thế ta nhận được hàng một, ba, ba, một. Ở đây hình ảnh trực quan và kết quả đếm tổ hợp trùng khớp. Ta sẽ sớm giải thích tại sao hai số ở phía trên lại được cộng với nhau.

### 05 - HÀNG THỨ TƯ
- Mo hinh: `growth` - trang thai 4; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Giữ hai ô biên bằng 1.; Ba ô giữa có giá trị 4, 6, 4.; Tam giác trở nên cân đối.
- Typst: `growth_4`.
- Loi giang: Khi xây dựng hàng của bốn phần tử, các ô giữa lần lượt mang số bốn, sáu và bốn. Toàn bộ hàng là một, bốn, sáu, bốn, một. Nếu quan sát kỹ, ta thấy các số bên trái và bên phải đối xứng nhau. Hãy thử đoán hàng tiếp theo trước khi các con số hiện ra trên màn hình.

### 06 - DỰ ĐOÁN HÀNG MỚI
- Mo hinh: `growth` - trang thai 5; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Hàng thứ năm có sáu ô.; Quy tắc cộng cho ra 1,5,10,10,5,1.; Tổng sáu ô bằng 32.
- Typst: `growth_5`.
- Loi giang: Ta có thể dự đoán hàng thứ năm bằng cách giữ hai số một ở biên, rồi cộng từng cặp ô kề nhau của hàng thứ tư. Kết quả là một, năm, mười, mười, năm, một. Tổng các hệ số là ba mươi hai. Số ba mươi hai còn liên quan đến số tập con của một tập có năm phần tử, một kết nối rất đáng chú ý.

## 02 · QUY TAC CONG HAI O KE NHAU

### 07 - QUAN SÁT HAI Ô CHA
- Mo hinh: `parents` - trang thai 0; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Chọn một ô ở giữa hàng thứ tư.; Nối ô ấy với hai ô hàng trên.; Hai nhánh cùng dẫn đến một ô con.
- Typst: `parents_0`.
- Loi giang: Bây giờ hãy tập trung vào ô có giá trị sáu ở giữa hàng thứ tư. Hai mũi tên xuất phát từ hai ô mang số ba ở hàng thứ ba cùng đi tới ô này. Ba cộng ba bằng sáu. Đây không phải một mẹo tính tự nhiên xuất hiện; phía sau nó là cách phân chia các lựa chọn thành hai nhóm không giao nhau.

### 08 - QUY TẮC CHO MỖI Ô GIỮA
- Mo hinh: `parents` - trang thai 1; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Hai ô phía trên nằm chéo trái và phải.; Cộng chúng để được ô phía dưới.; Ô biên vẫn luôn là 1.
- Typst: `parents_1`.
- Loi giang: Với một ô bất kỳ không nằm trên biên, hãy nhìn hai ô ngay phía trên: một ở góc trái và một ở góc phải. Giá trị ô mới bằng tổng hai giá trị đó. Viết bằng kí hiệu tổ hợp, ta được hệ thức Pascal. Chỉ số trên biểu diễn số phần tử của tập, chỉ số dưới biểu diễn số phần tử cần chọn, đúng theo quy ước của Series.

### 09 - ÁP DỤNG Ở HÀNG THỨ NĂM
- Mo hinh: `parents` - trang thai 2; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Muốn tính số 10 thứ nhất.; Lấy 4 cộng 6 của hàng trước.; Số 10 thứ hai bằng 6 cộng 4.
- Typst: `parents_2`.
- Loi giang: Hãy dùng hệ thức vừa học để tính số mười thứ nhất ở hàng năm. Hai ô cha của nó có giá trị bốn và sáu. Cộng lại được mười. Với số mười còn lại, ta lấy sáu cộng bốn. Khi hoạt hình làm sáng hai mũi tên, chúng ta có thể nhìn thấy trực tiếp nguồn gốc của mỗi ô mới, không cần ghi nhớ một dãy số dài.

### 10 - KIỂM TRA HÀNG SÁU
- Mo hinh: `parents` - trang thai 3; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Bắt đầu từ 1,5,10,10,5,1.; Tạo hàng 1,6,15,20,15,6,1.; Kiểm tra số giữa bằng 10+10.
- Typst: `parents_3`.
- Loi giang: Nếu tiếp tục một hàng nữa, số ở giữa hàng sáu nhận hai số mười phía trên, cho kết quả hai mươi. Hai ô kế bên nhận năm cộng mười, được mười lăm. Cả hàng là một, sáu, mười lăm, hai mươi, mười lăm, sáu, một. Chúng ta đã có một thuật toán rất đơn giản để tạo toàn bộ tam giác Pascal.

### 11 - TRƯỜNG HỢP BIÊN
- Mo hinh: `parents` - trang thai 4; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Không có ô cha phía ngoài tam giác.; Ô đầu và ô cuối luôn là 1.; Quy ước giá trị ngoài miền bằng 0.
- Typst: `parents_4`.
- Loi giang: Tại hai mép của tam giác, ta không có đủ hai ô cha. Nhưng mỗi ô biên vẫn mang số một vì chỉ có một cách chọn không phần tử hoặc chọn hết các phần tử. Khi muốn viết quy tắc cộng thống nhất, ta có thể xem các ô nằm bên ngoài tam giác có giá trị không. Cách quy ước này giúp thuật toán gọn gàng và chính xác.

### 12 - TỔNG QUÁT THUẬT TOÁN
- Mo hinh: `parents` - trang thai 5; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Khởi đầu bằng hàng [1].; Chèn 1 ở hai đầu hàng tiếp theo.; Ô giữa là tổng hai ô kề hàng cũ.
- Typst: `parents_5`.
- Loi giang: Ta có thể nhờ máy tính sinh hàng thứ mười, thứ hai mươi, thậm chí hàng thứ một trăm mà không cần khai triển nhị thức. Bắt đầu với hàng chỉ gồm một số một. Trong mỗi bước, đặt một ở hai đầu và điền các số ở giữa bằng cách cộng hai số kề của hàng trước. Bài toán tổ hợp vì vậy trở thành một quy trình tính toán có thể kiểm chứng từng bước.

## 03 · CHUNG MINH BANG HAI CACH DEM

### 13 - BÀI TOÁN CHỌN BA NGƯỜI
- Mo hinh: `proof` - trang thai 0; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Có sáu học sinh A,B,C,D,E,F.; Chọn nhóm ba người, không xét thứ tự.; Số nhóm bằng 20.
- Typst: `proof_0`.
- Loi giang: Chúng ta sẽ chứng minh vì sao hai ô cha phải cộng với nhau. Cho sáu học sinh phân biệt, hỏi có bao nhiêu cách chọn ba học sinh thành một nhóm. Ta biết kết quả là hai mươi. Nhưng thay vì tính bằng giai thừa ngay, hãy chọn riêng bạn A làm đối tượng đặc biệt và chia các nhóm thành hai loại.

### 14 - NHÓM CÓ A
- Mo hinh: `proof` - trang thai 1; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Nếu A có mặt trong nhóm.; Chọn thêm hai người từ năm bạn còn lại.; Số cách bằng 10.
- Typst: `proof_1`.
- Loi giang: Trường hợp thứ nhất, nhóm được chọn có bạn A. Khi đó A đã chiếm một trong ba vị trí của nhóm, chúng ta chỉ cần chọn thêm hai người từ năm bạn B, C, D, E và F. Có mười cách. Mọi nhóm chứa A đều xuất hiện đúng một lần trong phép đếm này.

### 15 - NHÓM KHÔNG CÓ A
- Mo hinh: `proof` - trang thai 2; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Nếu A không được chọn.; Cần chọn đủ ba người từ năm bạn.; Số cách cũng bằng 10.
- Typst: `proof_2`.
- Loi giang: Trường hợp thứ hai, nhóm không có A. Toàn bộ ba thành viên phải được chọn từ năm bạn còn lại, nên có đúng mười cách. Một nhóm không thể vừa có A vừa không có A. Hai nhóm trường hợp này tách biệt hoàn toàn, đó là điều kiện cho phép ta sử dụng quy tắc cộng.

### 16 - GHÉP HAI TRƯỜNG HỢP
- Mo hinh: `proof` - trang thai 3; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Có A: 10 nhóm.; Không có A: 10 nhóm.; Cộng để được 20 nhóm.
- Typst: `proof_3`.
- Loi giang: Khi ghép hai loại nhóm, ta thu được mười cộng mười bằng hai mươi. Đây chính là ba ô nằm theo hình chữ vê trong tam giác Pascal: hai số mười ở trên và số hai mươi phía dưới. Như vậy quy tắc cộng hai ô cha không còn là một quan sát ngẫu nhiên mà xuất phát từ phép đếm cùng một tập kết quả theo hai trường hợp.

### 17 - CHỨNG MINH CHO n, k
- Mo hinh: `proof` - trang thai 4; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Đánh dấu một phần tử đặc biệt A.; Có A: chọn k-1 trong n-1.; Không A: chọn k trong n-1.
- Typst: `proof_4`.
- Loi giang: Với một tập gồm n phần tử, ta muốn chọn k phần tử. Chọn một phần tử A làm mốc. Nếu có A, ta chọn thêm k trừ một phần tử từ n trừ một phần tử còn lại. Nếu không có A, ta chọn đủ k phần tử từ phần còn lại. Hai trường hợp phủ kín và không giao nhau, nên cộng số cách lại được hệ thức Pascal tổng quát.

### 18 - TẠI SAO KHÔNG ĐẾM TRÙNG?
- Mo hinh: `proof` - trang thai 5; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Mỗi nhóm thuộc đúng một trong hai loại.; Không có nhóm vừa chứa vừa thiếu A.; Không có nhóm nào bị bỏ sót.
- Typst: `proof_5`.
- Loi giang: Điểm quan trọng nhất của một chứng minh tổ hợp là kiểm tra hai việc: không đếm trùng và không bỏ sót. Ở đây, mọi nhóm hoặc chứa A hoặc không chứa A, không có khả năng thứ ba. Đồng thời hai tính chất ấy không thể xảy ra cùng lúc. Vì vậy phép cộng là hợp lệ, và chúng ta đã chứng minh được bản chất của tam giác Pascal.

## 04 · DOI XUNG VA PHEP LAY PHAN BU

### 19 - QUAN SÁT HÀNG ĐỐI XỨNG
- Mo hinh: `mirror` - trang thai 0; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Hàng thứ sáu: 1,6,15,20,15,6,1.; Hai ô cách đều trung tâm bằng nhau.; Cặp chỉ số k và 6-k.
- Typst: `mirror_0`.
- Loi giang: Hãy quan sát hàng thứ sáu. Nếu gập hàng này qua chính giữa, những con số ở hai phía sẽ trùng khít: một đi với một, sáu đi với sáu, mười lăm đi với mười lăm. Tại sao một tính chất hình ảnh đẹp như vậy lại đúng với mọi hàng, chứ không phải chỉ đúng ở vài ví dụ đầu?

### 20 - CHỌN VÀ KHÔNG CHỌN
- Mo hinh: `mirror` - trang thai 1; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Chọn hai phần tử trong sáu.; Tương ứng với bỏ lại bốn phần tử.; Hai thao tác xác định nhau duy nhất.
- Typst: `mirror_1`.
- Loi giang: Tưởng tượng sáu thẻ học sinh. Mỗi khi chọn hai thẻ vào nhóm, ta đồng thời xác định chính xác bốn thẻ không được chọn. Ngược lại, biết bốn thẻ bị bỏ lại thì suy ra ngay hai thẻ được chọn. Đây là một phép tương ứng một đối một giữa hai tập kết quả, nên hai tập có cùng số phần tử.

### 21 - CÔNG THỨC ĐỐI XỨNG
- Mo hinh: `mirror` - trang thai 2; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Chọn k đồng nghĩa với bỏ n-k.; Phép tương ứng có hai chiều.; Hai số tổ hợp bằng nhau.
- Typst: `mirror_2`.
- Loi giang: Một tập gồm n phần tử được tách thành nhóm chọn k phần tử và nhóm không chọn n trừ k phần tử. Hai nhóm bổ sung nhau, nên một nhóm xác định hoàn toàn nhóm còn lại. Do đó, số cách chọn k phần tử bằng số cách chọn n trừ k phần tử. Tính đối xứng của các hàng Pascal thực ra là tính đối xứng của phép lấy phần bù.

### 22 - TÍNH NHANH BẰNG ĐỐI XỨNG
- Mo hinh: `mirror` - trang thai 3; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Không cần tính lại hai phía.; Biết C của 2 từ 8 suy ra C của 6 từ 8.; Kết quả đều bằng 28.
- Typst: `mirror_3`.
- Loi giang: Ta thử áp dụng vào một bài tính nhanh. Số cách chọn hai học sinh từ tám học sinh bằng hai mươi tám. Vì chọn hai người tương đương với chỉ định sáu người bị loại, số cách chọn sáu người cũng bằng hai mươi tám. Khi gặp k lớn gần n, đổi sang n trừ k thường làm phép tính ngắn hơn và dễ kiểm tra hơn.

### 23 - Ô GIỮA CỦA HÀNG CHẴN
- Mo hinh: `mirror` - trang thai 4; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Hàng chẵn có một ô chính giữa.; Số C của n/2 trong n đạt cực đại.; Hai phía tăng rồi giảm đối xứng.
- Typst: `mirror_4`.
- Loi giang: Với hàng có chỉ số chẵn, ta tìm thấy một ô đúng ở giữa, chẳng hạn số hai mươi của hàng sáu. Những hệ số thường tăng dần về giữa rồi giảm dần sau giữa. Chúng ta có thể giải thích bằng tỉ số giữa hai hệ số kề nhau, nhưng ở đây trước hết hãy nhìn cách giá trị lan truyền và tích lũy từ hai phía qua từng hàng.

### 24 - HÀNG LẺ VÀ HAI Ô GIỮA
- Mo hinh: `mirror` - trang thai 5; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Hàng lẻ có hai ô giữa bằng nhau.; Hàng 5 có hai số 10 ở giữa.; Kiểm tra bằng công thức đối xứng.
- Typst: `mirror_5`.
- Loi giang: Đối với hàng mang chỉ số lẻ, chính giữa có hai ô bằng nhau. Hàng thứ năm chẳng hạn có hai số mười nằm cạnh nhau. Tính đối xứng cho biết ngay chúng phải bằng nhau, bởi hai chỉ số hai và ba cộng lại bằng năm. Quan sát này giúp học sinh nhận dạng cấu trúc hàng Pascal mà không cần ghi nhớ toàn bộ bảng số.

## 05 · TONG CAC HANG VA DAU XEN KE

### 25 - TỔNG TỪNG HÀNG
- Mo hinh: `sums` - trang thai 0; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Hàng 0 có tổng 1.; Hàng 1 có tổng 2, hàng 2 có tổng 4.; Mỗi hàng sau gấp đôi hàng trước.
- Typst: `sums_0`.
- Loi giang: Ta chuyển sang một tính chất rất đẹp: tổng các số trên từng hàng. Các hàng đầu có tổng một, hai, bốn, tám, mười sáu và ba mươi hai. Mỗi khi số phần tử tăng một đơn vị, số tập con tăng gấp đôi vì phần tử mới có thể được chọn hoặc không được chọn. Điều đó cho ta công thức tổng hàng bằng hai mũ n.

### 26 - KIỂM TRA HÀNG SÁU
- Mo hinh: `sums` - trang thai 1; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Hàng 6: 1,6,15,20,15,6,1.; Cộng tất cả được 64.; Bằng số tập con của 6 phần tử.
- Typst: `sums_1`.
- Loi giang: Hãy kiểm tra cụ thể trên hàng sáu. Cộng một, sáu, mười lăm, hai mươi, mười lăm, sáu và một, ta được sáu mươi bốn. Một tập có sáu phần tử cũng có sáu mươi bốn tập con vì mỗi phần tử có đúng hai trạng thái được chọn hoặc không được chọn. Hai lập luận dẫn tới cùng một kết quả.

### 27 - NHÌN TỪ NHỊ THỨC NEWTON
- Mo hinh: `sums` - trang thai 2; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Thay a bằng 1 và b bằng 1.; Vế trái trở thành 2 mũ n.; Vế phải là tổng các hệ số.
- Typst: `sums_2`.
- Loi giang: Còn một cách chứng minh đại số cực ngắn. Trong khai triển Nhị thức Newton, thay cả a và b bằng một. Vế trái là hai mũ n. Ở vế phải, mọi đơn thức còn lại đúng bằng một, nên chỉ còn tổng các hệ số tổ hợp. Đây là cách kết nối trực tiếp Video 17 với tam giác Pascal đang được xây dựng.

### 28 - CỘNG XEN DẤU
- Mo hinh: `sums` - trang thai 3; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Lấy tổng các hệ số với dấu xen kẽ.; Hàng sáu: 1-6+15-20+15-6+1.; Kết quả bằng 0.
- Typst: `sums_3`.
- Loi giang: Bây giờ, thay vì cộng tất cả các ô, ta gắn dấu cộng và trừ xen kẽ. Với hàng sáu, biểu thức một trừ sáu cộng mười lăm trừ hai mươi cộng mười lăm trừ sáu cộng một bằng không. Đó là vì theo Nhị thức Newton, tổng xen dấu chính là một trừ một, tất cả lũy thừa n, nên bằng không khi n dương.

### 29 - CHẴN VÀ LẺ CÂN BẰNG
- Mo hinh: `sums` - trang thai 4; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Tổng hệ số ở cột k chẵn.; Tổng hệ số ở cột k lẻ.; Mỗi tổng bằng 2 mũ n-1.
- Typst: `sums_4`.
- Loi giang: Từ hai công thức tổng hàng và tổng xen dấu, ta rút ra rằng tổng hệ số tại các vị trí k chẵn bằng tổng hệ số ở vị trí k lẻ, mỗi bên bằng hai mũ n trừ một với n dương. Ở hàng sáu, mỗi phía bằng ba mươi hai. Đây là một ví dụ về cách dùng hai phương trình để xác định hai tổng chưa biết.

### 30 - LƯU Ý TRƯỜNG HỢP n BẰNG 0
- Mo hinh: `sums` - trang thai 5; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Tổng hàng luôn là 2 mũ n.; Tổng xen dấu bằng 0 khi n dương.; Với n bằng 0, tổng xen dấu bằng 1.
- Typst: `sums_5`.
- Loi giang: Một lưu ý nhỏ nhưng quan trọng: công thức tổng xen dấu bằng không cần điều kiện n lớn hơn không. Với n bằng không, hàng Pascal chỉ có một ô bằng một và tổng xen dấu cũng bằng một. Nếu bỏ quên điều kiện biên, ta có thể dùng một đẳng thức đúng trong phần lớn trường hợp nhưng sai ngay ở điểm khởi đầu. Tính chính xác toán học bắt đầu từ những chi tiết như vậy.

## 06 · DUONG CHEO VA HINH GAY KHUC

### 31 - ĐƯỜNG CHÉO TRONG PASCAL
- Mo hinh: `hockey` - trang thai 0; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Chọn một đường chéo hướng xuống.; Giá trị lần lượt 1,3,6,10.; Tổng các giá trị là 20.
- Typst: `hockey_0`.
- Loi giang: Bên cạnh từng hàng ngang, tam giác Pascal còn chứa nhiều cấu trúc thú vị theo đường chéo. Hãy tô sáng bốn số một, ba, sáu và mười theo một đường chéo đi xuống. Khi cộng chúng ta được hai mươi. Số hai mươi xuất hiện ở một vị trí khác của tam giác, giống như hình một chiếc gậy khúc côn cầu với phần cán và đầu cong.

### 32 - VIẾT DƯỚI DẠNG TỔ HỢP
- Mo hinh: `hockey` - trang thai 1; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Bốn số thuộc các hàng 2,3,4,5.; Cùng có chỉ số dưới bằng 2.; Tổng bằng số tổ hợp chọn 3 từ 6.
- Typst: `hockey_1`.
- Loi giang: Bốn giá trị trên có thể viết thành tổ hợp chập hai của hai, ba, bốn và năm. Cộng chúng ta được tổ hợp chập ba của sáu, tức hai mươi. Tên gọi hình gậy khúc côn cầu giúp chúng ta nhớ vị trí của các ô, nhưng điều quan trọng hơn là hiểu phép đếm nào đứng phía sau phép cộng theo đường chéo.

### 33 - GIẢI THÍCH BẰNG PHẦN TỬ LỚN NHẤT
- Mo hinh: `hockey` - trang thai 2; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Chọn ba số từ 1 đến 6.; Phân loại theo số lớn nhất: 3,4,5,6.; Phần còn lại chọn hai số nhỏ hơn.
- Typst: `hockey_2`.
- Loi giang: Hãy đếm các tập ba phần tử chọn từ các số một đến sáu. Mỗi tập có một phần tử lớn nhất, chỉ có thể là ba, bốn, năm hoặc sáu. Nếu phần tử lớn nhất bằng t, ta cần chọn hai phần tử trong t trừ một số nhỏ hơn nó. Số cách tương ứng lần lượt là một, ba, sáu và mười. Cộng bốn trường hợp sẽ được hai mươi.

### 34 - HÌNH GẬY KHÚC CÔN CẦU
- Mo hinh: `hockey` - trang thai 3; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Các ô trên cán gậy cùng chỉ số k.; Ô đích lệch sang phải một vị trí.; Quan sát phép cộng tích lũy.
- Typst: `hockey_3`.
- Loi giang: Nếu kéo dài lập luận vừa rồi, ta nhận được đẳng thức tổng quát: tổng các số tổ hợp có cùng chỉ số dưới k, chạy từ hàng k đến hàng n, bằng số tổ hợp với chỉ số trên n cộng một và chỉ số dưới k cộng một. Trong hình, các ô nằm trên cán gậy được tô xanh; ô kết quả ở đầu gậy được tô vàng.

### 35 - KIỂM TRA MỘT VÍ DỤ KHÁC
- Mo hinh: `hockey` - trang thai 4; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Chọn k bằng 1, n bằng 4.; Tổng 1+2+3+4 bằng 10.; Đúng bằng C chọn 2 từ 5.
- Typst: `hockey_4`.
- Loi giang: Ta kiểm tra thêm một ví dụ dễ tính nhẩm: một cộng hai cộng ba cộng bốn bằng mười. Các số một, hai, ba, bốn chính là số tổ hợp chập một của một, hai, ba, bốn; kết quả mười bằng số tổ hợp chập hai của năm. Ví dụ này cho thấy đẳng thức đường chéo không chỉ đúng tại một vị trí đặc biệt.

### 36 - KHI NÀO NÊN DÙNG?
- Mo hinh: `hockey` - trang thai 5; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Gặp tổng các C có cùng chỉ số dưới.; Kiểm tra chỉ số trên tăng liên tiếp.; Thay phép cộng dài bằng một tổ hợp.
- Typst: `hockey_5`.
- Loi giang: Khi gặp một tổng dài gồm các số tổ hợp cùng chỉ số dưới, còn chỉ số trên tăng đều qua từng số nguyên liên tiếp, hãy nghĩ đến công thức đường chéo. Thay vì tính từng số hạng rồi cộng, ta có thể viết gọn thành một tổ hợp duy nhất. Nhưng cần kiểm tra cẩn thận điểm đầu, điểm cuối và chỉ số tăng thêm để không lệch một đơn vị.

## 07 · CHAN LE VA HOA TIET TUONG TU

### 37 - TÔ MÀU THEO TÍNH CHẴN LẺ
- Mo hinh: `parity` - trang thai 0; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Ô lẻ tô sáng, ô chẵn để tối.; Các hàng đầu tạo một hoa văn lặp.; Chỉ quan tâm số dư khi chia 2.
- Typst: `parity_0`.
- Loi giang: Đến đây, ta khám phá một lớp hình ảnh khác của tam giác Pascal. Thay vì đọc toàn bộ số lớn, hãy chỉ quan tâm một ô là chẵn hay lẻ. Tô sáng các ô lẻ và làm mờ những ô chẵn. Dần dần xuất hiện một họa tiết lặp lại rất đẹp. Manim sẽ cho hiện nhiều hàng liên tiếp để học sinh quan sát quy luật.

### 38 - CỘNG THEO PHÉP TOÁN MODULO 2
- Mo hinh: `parity` - trang thai 1; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Lẻ cộng lẻ thành chẵn.; Chẵn cộng lẻ thành lẻ.; Hàng mới vẫn cộng hai ô phía trên.
- Typst: `parity_1`.
- Loi giang: Ta vẫn dùng đúng quy tắc Pascal: ô mới bằng tổng hai ô phía trên. Nhưng khi chỉ quan sát tính chẵn lẻ, lẻ cộng lẻ tạo thành chẵn, còn chẵn cộng lẻ tạo thành lẻ. Vì thế các ô sáng và tối tiếp tục sinh ra hình mới theo một quy luật cục bộ rất đơn giản. Đây là cách một cấu trúc lớn nảy sinh từ phép tính nhỏ.

### 39 - HÀNG CHỈ SỐ 7 TOÀN SỐ LẺ
- Mo hinh: `parity` - trang thai 2; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Các số hàng 7 là 1,7,21,35,35,21,7,1.; Tất cả đều lẻ.; Một dải sáng xuất hiện trọn hàng.
- Typst: `parity_2`.
- Loi giang: Ở hàng mang chỉ số bảy, các hệ số lần lượt là một, bảy, hai mươi mốt, ba mươi lăm, ba mươi lăm, hai mươi mốt, bảy và một. Tất cả đều lẻ. Trong mô hình chẵn lẻ, cả hàng sẽ sáng lên. Đây là dấu hiệu đặc biệt giúp chia hoa văn thành những khối nhỏ giống nhau ở nhiều mức độ.

### 40 - HÀNG CHỈ SỐ 8 CHỈ SÁNG Ở BIÊN
- Mo hinh: `parity` - trang thai 3; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Hàng 8 có 1 ở hai đầu.; Những ô ở giữa đều chẵn.; Hai điểm sáng nằm tại biên.
- Typst: `parity_3`.
- Loi giang: Khi chuyển sang hàng tám, chỉ hai ô ở hai mép có giá trị lẻ. Các ô còn lại đều chẵn nên chuyển sang màu tối. Sự thay đổi đột ngột này tạo thành khoảng trống đặc trưng trong họa tiết tam giác. Nếu tiếp tục đến hàng mười lăm và mười sáu, ta sẽ quan sát những bước lặp lại tương tự.

### 41 - HOA VĂN SIERPINSKI
- Mo hinh: `parity` - trang thai 4; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Hiển thị 32 hàng với độ tương phản cao.; Nhận diện những tam giác lồng nhau.; Tất cả sinh từ quy tắc cộng.
- Typst: `parity_4`.
- Loi giang: Khi tô sáng các số lẻ trong ba mươi hai hàng Pascal, ta nhìn thấy các tam giác nhỏ nằm trong tam giác lớn, một hoa văn gần với tam giác Sierpinski. Điều bất ngờ là hình ảnh này không cần thêm quy tắc vẽ riêng. Chúng ta chỉ lặp phép cộng hai ô cha rồi lấy số dư chia hai. Toán tổ hợp, số học và hình học kết nối với nhau qua một hình động.

### 42 - KHÁM PHÁ, KHÔNG ĐOÁN VÔ CĂN CỨ
- Mo hinh: `parity` - trang thai 5; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Họa tiết là bằng chứng quan sát.; Chứng minh cần định lý số học sâu hơn.; Phân biệt dự đoán và chứng minh.
- Typst: `parity_5`.
- Loi giang: Hình ảnh khiến ta muốn dự đoán rằng tam giác Pascal có tính tự đồng dạng khi xét theo modulo hai. Tuy nhiên, xem một số hàng chưa đủ để kết luận cho mọi hàng. Muốn chứng minh tổng quát cần thêm công cụ về hệ số nhị thức và số học, chẳng hạn cách viết số theo hệ nhị phân. Ở đây, ta dùng hình động để khám phá và khơi gợi câu hỏi mới.

## 08 · HE SO VA BAI TOAN TONG HOP

### 43 - BÀI TOÁN HỆ SỐ
- Mo hinh: `challenge` - trang thai 0; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Tìm hệ số của x mũ 3.; Biểu thức là (1+x)^5(1+x)^3.; Có tất cả 8 nhân tử (1+x).
- Typst: `challenge_0`.
- Loi giang: Bài toán cuối tập yêu cầu tìm hệ số của x mũ ba trong tích một cộng x mũ năm nhân với một cộng x mũ ba. Ta có thể gộp hai lũy thừa thành một cộng x mũ tám. Khi đó hệ số cần tìm chính là số cách chọn ba trong tám nhân tử để lấy x. Hãy thử dự đoán kết quả từ hàng thứ tám của tam giác Pascal.

### 44 - CÁCH MỘT: GỘP HAI LŨY THỪA
- Mo hinh: `challenge` - trang thai 1; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Gộp thành (1+x)^8.; Đọc ô k bằng 3 của hàng 8.; Nhận được 56.
- Typst: `challenge_1`.
- Loi giang: Theo cách thứ nhất, ta đơn giản hóa tích ban đầu thành một cộng x mũ tám. Hàng thứ tám của Pascal có hệ số thứ ba bằng năm mươi sáu nếu đánh chỉ số bắt đầu từ không. Vậy hệ số của x mũ ba là năm mươi sáu. Phương pháp này nhanh, nhưng chúng ta còn có thể tự kiểm chứng bằng cách phân chia các nhân tử thành hai nhóm.

### 45 - CÁCH HAI: CHIA PHẦN CHỌN x
- Mo hinh: `challenge` - trang thai 2; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Chọn i chữ x trong nhóm năm ngoặc.; Chọn 3-i chữ x trong nhóm ba ngoặc.; Có bốn giá trị i: 0,1,2,3.
- Typst: `challenge_2`.
- Loi giang: Ở cách thứ hai, giữ hai nhóm nhân tử riêng biệt. Giả sử ta chọn i ngoặc lấy x trong nhóm năm ngoặc, thì phải chọn ba trừ i ngoặc lấy x trong nhóm ba ngoặc còn lại. Vì tổng số chữ x cần đúng bằng ba, i chỉ có thể nhận bốn giá trị không, một, hai và ba. Mỗi trường hợp có số cách tính bằng tích hai tổ hợp.

### 46 - LIỆT KÊ BỐN TRƯỜNG HỢP
- Mo hinh: `challenge` - trang thai 3; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: i=0 đóng góp 1.; i=1 đóng góp 15; i=2 đóng góp 30.; i=3 đóng góp 10.
- Typst: `challenge_3`.
- Loi giang: Ta tính lần lượt bốn trường hợp. Nếu không chọn x từ nhóm năm ngoặc thì nhóm ba ngoặc phải chọn cả ba, có một cách. Nếu chọn một x ở nhóm thứ nhất thì có mười lăm cách. Nếu chọn hai x thì có ba mươi cách. Nếu chọn ba x thì có mười cách. Cộng lại bằng năm mươi sáu, đúng với cách một.

### 47 - ĐẲNG THỨC VANDERMONDE
- Mo hinh: `challenge` - trang thai 4; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Hai cách đếm cùng một tập lựa chọn.; Gộp tám phần tử hoặc chia thành hai nhóm 5-3.; Tổng các tích tổ hợp bằng 56.
- Typst: `challenge_4`.
- Loi giang: Hai phép đếm vừa rồi tính cùng một đối tượng: chọn ba vị trí từ tám vị trí. Một cách coi tất cả là một tập lớn, cách còn lại chia trước thành nhóm năm và nhóm ba. Vì cùng đếm một tập kết quả, hai biểu thức phải bằng nhau. Đây là trường hợp cụ thể của đồng nhất thức Vandermonde, một chủ đề chúng ta sẽ tiếp tục nghiên cứu ở các video sau.

### 48 - TỔNG KẾT TAM GIÁC PASCAL
- Mo hinh: `challenge` - trang thai 5; nhan manh doi tuong va nhom dang duoc dem.
- Hinh hien: Hàng được sinh từ hai ô cha.; Đối xứng, tổng hàng, đường chéo.; Tính chẵn lẻ và bài tìm hệ số.
- Typst: `challenge_5`.
- Loi giang: Chúng ta đã đi từ một ô mang số một đến nhiều tính chất sâu sắc. Tam giác Pascal cho phép tính các tổ hợp nhờ cộng hai ô cha, chứng minh tính đối xứng, tổng hệ số, hệ thức đường chéo, và khám phá các hoa văn chẵn lẻ. Cuối cùng, nó trở thành công cụ mạnh để tìm hệ số trong khai triển nhị thức. Quan trọng nhất, mỗi công thức đều được gắn với một cách đếm có ý nghĩa.
