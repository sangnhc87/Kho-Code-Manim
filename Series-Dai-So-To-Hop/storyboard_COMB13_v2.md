# SANG MATH · COMB13 V2

# KỊCH BẢN STORYBOARD: CÁC PHẦN TỬ KHÔNG ĐƯỢC ĐỨNG CẠNH NHAU

Bố cục 16:9: trái mô hình trực quan, phải bài toán - suy luận - công thức.
Ký hiệu tổ hợp: C^(n)_(k) (n ở trên, k ở dưới).
48 nhịp, 8 chương. Mỗi nhịp có lời giảng đầy đủ (không đọc đáp số trước khi lập luận).

## 01 · MỘT CẶP KHÔNG ĐƯỢC KỀ

Phát hiện điều kiện cấm rồi giải bằng phần bù.

### 1. NÊU BÀI TOÁN

**Cột phải — trình bày tuần tự:**

- Xếp A, B, C, D, E thành hàng.
- A và B không được đứng cạnh nhau.
- Đếm số cách xếp hợp lệ.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** TRƯỚC TIÊN, XÁC ĐỊNH ĐIỀU KIỆN CẤM.

**Thuyết minh:** Có năm học sinh A, B, C, D, E phân biệt. Ta muốn xếp thành một hàng, nhưng A và B không được ngồi ở hai vị trí liên tiếp. Nếu chỉ nói năm giai thừa, ta đã tính tất cả các hàng, kể cả những hàng vi phạm. Hãy quan sát các thẻ và đánh dấu chính xác hàng nào có hai bạn A, B đứng cạnh nhau. Khi biết phần bị cấm, ta mới xây dựng cách đếm đáng tin cậy.

### 2. TẠI SAO KHÔNG THỂ LẤY 5!

**Cột phải — trình bày tuần tự:**

- Một số hàng có AB hoặc BA liền nhau.
- Các hàng ấy không hợp lệ.
- Vì vậy 5! chỉ là tổng ban đầu.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** TỔNG KHÁC SỐ CÁCH HỢP LỆ.

**Thuyết minh:** Ta thấy trong một số hàng như A B C D E, cặp A B nằm sát nhau, còn ở hàng A C B D E, cặp ấy đã bị tách ra. Vậy quy tắc nhân khi xếp đủ năm người chưa phản ánh điều kiện của đề. Chúng ta phân chia các hàng thành hai nhóm không giao nhau: nhóm A B đứng cạnh và nhóm A B không đứng cạnh. Tổng của hai nhóm luôn là toàn bộ năm giai thừa hàng.

### 3. ĐẾM NHÓM BỊ CẤM

**Cột phải — trình bày tuần tự:**

- Gộp A, B thành khối [AB].
- Còn [AB], C, D, E: bốn đối tượng.
- Khối có hai thứ tự AB, BA.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** SỐ HÀNG BỊ CẤM BẰNG 2 × 4!.

**Thuyết minh:** Khi A và B đứng cạnh, ta tạm xem chúng như một khối không bị tách. Khối ấy cùng ba người C, D, E tạo ra bốn đối tượng phân biệt để xếp thành hàng, nên có bốn giai thừa khả năng. Nhưng ở bên trong khối, A có thể đứng trước B hoặc B có thể đứng trước A. Vì thế số hàng bị cấm là hai nhân bốn giai thừa, tức bốn mươi tám.

### 4. LẤY PHẦN BÙ

**Cột phải — trình bày tuần tự:**

- Tất cả có 120 cách.
- Số cách A, B đứng cạnh là 48.
- Số cách không đứng cạnh: 72.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** BÀI TOÁN ĐƯỢC GIẢI BẰNG PHẦN BÙ.

**Thuyết minh:** Bây giờ ta chỉ cần lấy tổng số hàng trừ những hàng A và B đứng sát nhau. Số cách thỏa yêu cầu bằng một trăm hai mươi trừ bốn mươi tám, bằng bảy mươi hai. Không có hàng nào bị bỏ sót vì mỗi hàng hoặc thuộc nhóm hợp lệ, hoặc thuộc nhóm bị cấm. Cũng không có hàng nào bị trừ hai lần vì hai nhóm được xác định bằng một điều kiện đối lập duy nhất.

### 5. KIỂM CHỨNG BẰNG LIỆT KÊ

**Cột phải — trình bày tuần tự:**

- Tạo đủ 120 hoán vị của 5 người.
- Đánh dấu mọi hàng có |pos(A)-pos(B)|=1.
- Đếm còn đúng 72 hàng.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** LIỆT KÊ LÀ KIỂM THỬ, KHÔNG THAY CHỨNG MINH.

**Thuyết minh:** Để kiểm tra, chương trình có thể liệt kê tất cả một trăm hai mươi hoán vị và xem hai vị trí A, B có chênh nhau đúng một hay không. Sau khi loại bốn mươi tám hàng vi phạm, ta còn đúng bảy mươi hai. Cách thử nhỏ này rất hữu ích để bắt lỗi công thức. Nhưng khi số người lớn, không thể liệt kê tất cả; ta vẫn phải nắm được chứng minh bằng phép đếm phần bù.

### 6. TỔNG QUÁT CHO n NGƯỜI

**Cột phải — trình bày tuần tự:**

- Có n người phân biệt, n ≥ 2.
- A, B là hai người chỉ định.
- Số cách hợp lệ: n! - 2(n-1)!.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** PHẢI CHẮC CHẮN CHỈ CẤM MỘT CẶP.

**Thuyết minh:** Với n người phân biệt, tổng số cách xếp là n giai thừa. Nếu hai người cụ thể bắt buộc đứng cạnh, ta gộp thành một khối, có hai nhân n trừ một giai thừa cách. Vậy khi hai người ấy không được đứng cạnh, số cách là n giai thừa trừ hai nhân n trừ một giai thừa. Công thức này dùng cho một hàng thẳng và đúng một cặp chỉ định; nếu có nhiều cặp cấm, phải xét giao nhau giữa các điều kiện.

## 02 · PHƯƠNG PHÁP KHOẢNG TRỐNG

Xếp nhóm còn lại trước để tạo những khoảng an toàn.

### 1. XẾP NGƯỜI KHÁC TRƯỚC

**Cột phải — trình bày tuần tự:**

- Giữ nguyên bài toán 5 người.
- Xếp C, D, E trước.
- Có 3! cách tạo hàng nền.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** KHOẢNG TRỐNG XUẤT HIỆN TỪ HÀNG NỀN.

**Thuyết minh:** Thay vì đếm phần bù, ta sẽ trực tiếp tạo ra những cách xếp hợp lệ. Hãy bỏ A và B ra ngoài một lúc, rồi xếp C, D, E trước. Có ba giai thừa, tức sáu hàng nền khác nhau. Từ một hàng nền cụ thể như C D E, hãy nhìn kỹ những vị trí có thể cài thêm A hoặc B. Cách tạo hàng nền này bảo đảm rằng những khoảng trống đều độc lập với vị trí của A và B.

### 2. BỐN KHOẢNG AN TOÀN

**Cột phải — trình bày tuần tự:**

- Hàng nền: C  D  E.
- Các khoảng: _ C _ D _ E _.
- Có tất cả 4 khoảng.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** CHỌN HAI KHOẢNG KHÁC NHAU.

**Thuyết minh:** Sau khi xếp ba bạn C, D, E thành một hàng, xuất hiện bốn khoảng: trước C, giữa C và D, giữa D và E, và sau E. Nếu đặt A và B vào hai khoảng khác nhau, giữa họ chắc chắn có ít nhất một người thuộc hàng nền. Vì thế hai bạn không thể đứng cạnh. Nếu đặt cả hai vào cùng một khoảng, họ sẽ liền nhau. Điều kiện cấm được chuyển thành điều kiện chọn các khoảng khác nhau.

### 3. CHỌN VỊ TRÍ CHO A VÀ B

**Cột phải — trình bày tuần tự:**

- Chọn hai trong bốn khoảng.
- Không xét thứ tự khi chọn khoảng.
- Có C trên 4 dưới 2 = 6 cách.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** LÚC CHỌN KHOẢNG CHƯA PHÂN CÔNG A, B.

**Thuyết minh:** Trước tiên, ta chọn ra hai khoảng khác nhau trong bốn khoảng an toàn. Lúc này hai khoảng chỉ là một nhóm gồm hai vị trí, chưa nói A sẽ vào khoảng nào. Vì vậy số cách chọn khoảng là tổ hợp chập hai của bốn, bằng sáu. Ký hiệu trên màn hình dùng n ở chỉ số trên và k ở dưới theo chuẩn trình bày đã thống nhất cho cả Series. Bước tiếp theo mới quyết định thứ tự đặt A, B.

### 4. HOÁN ĐỔI A VÀ B

**Cột phải — trình bày tuần tự:**

- Mỗi cặp khoảng đã chọn có 2! cách.
- A ở khoảng trước hoặc khoảng sau.
- Tổng: 3! × 6 × 2! = 72.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** MỖI HÀNG HỢP LỆ ĐƯỢC TẠO ĐÚNG MỘT LẦN.

**Thuyết minh:** Với hai khoảng đã được lựa chọn, ta có thể đặt A vào khoảng thứ nhất và B vào khoảng thứ hai, hoặc đổi ngược lại. Đó là hai giai thừa cách phân công. Nhân với sáu cách xếp hàng nền và sáu cách chọn cặp khoảng, ta thu được bảy mươi hai. Mỗi hàng hợp lệ cho biết duy nhất hàng nền sau khi xóa A, B, hai khoảng được chọn và người được đặt vào từng khoảng. Vậy phép đếm không bị trùng.

### 5. SO SÁNH HAI CÁCH GIẢI

**Cột phải — trình bày tuần tự:**

- Cách 1: 5! - 2·4!.
- Cách 2: 3!·C trên 4 dưới 2·2!.
- Cả hai đều cho 72.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** ĐẾM BÙ VÀ CHỌN KHOẢNG BỔ SUNG CHO NHAU.

**Thuyết minh:** Cùng một bài toán, hai phương pháp cho cùng bảy mươi hai cách. Phương pháp phần bù thuận lợi khi chỉ cấm một cặp, vì đếm nhóm bị cấm rất đơn giản. Phương pháp khoảng trống lại cho chúng ta một cách dựng trực tiếp từng hàng hợp lệ, đặc biệt mạnh khi có nhiều người thuộc một nhóm không được đứng cạnh nhau. Sự trùng khớp của hai kết quả không phải ngẫu nhiên: cả hai đều đếm chính một tập hợp.

### 6. DẤU HIỆU NHẬN RA KHOẢNG TRỐNG

**Cột phải — trình bày tuần tự:**

- Có một nhóm cần tách nhau ra.
- Có một nhóm khác dùng làm ngăn cách.
- Hãy xếp nhóm ngăn cách trước.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** SỐ KHOẢNG BẰNG SỐ VẬT NỀN CỘNG MỘT.

**Thuyết minh:** Khi đề bài nói các bạn nữ không được đứng cạnh nhau, hoặc các chữ A không được liên tiếp, hãy nghĩ đến phương pháp khoảng trống. Ta thường xếp nhóm còn lại trước để tạo các khe trống. Sau đó chọn các khe khác nhau cho những phần tử cần tách nhau. Cần chú ý hai điều: các phần tử trong mỗi nhóm có phân biệt hay không, và số khoảng có đủ để đặt tất cả phần tử đặc biệt hay không.

## 03 · CÁC VỊ TRÍ KHÔNG LIỀN NHAU

Xây dựng công thức chọn k vị trí cách nhau.

### 1. BỐN CHỮ A VÀ NĂM CHỮ B

**Cột phải — trình bày tuần tự:**

- Xếp bốn A giống hệt và năm B giống hệt.
- Không có hai A nào liên tiếp.
- Cần đếm số dãy khác nhau.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** CHỮ GIỐNG NHAU KHÔNG ĐƯỢC HOÁN ĐỔI THÀNH CÁCH MỚI.

**Thuyết minh:** Chúng ta xét chín vị trí, chứa bốn chữ A giống nhau và năm chữ B giống nhau, với điều kiện không xuất hiện hai A liên tiếp. Khác với bài xếp học sinh, việc đổi hai chữ A cho nhau không tạo một dãy mới. Nếu dùng thừa bốn giai thừa để nhân, kết quả sẽ bị sai. Đây là cơ hội để gắn kỹ thuật khoảng trống với những điều đã học về hoán vị có phần tử giống nhau.

### 2. TẠO SÁU KHOẢNG TỪ NĂM B

**Cột phải — trình bày tuần tự:**

- Xếp năm B trước: B B B B B.
- Có sáu khoảng đặt A.
- Mỗi khoảng nhận tối đa một A.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** KHOẢNG TRỐNG TỰ ĐỘNG ĐẢM BẢO KHÔNG KỀ.

**Thuyết minh:** Vì năm chữ B giống nhau, hàng nền của chúng chỉ có một cách. Trước, giữa và sau năm B xuất hiện đúng sáu khoảng trống. Đặt bốn chữ A vào bốn khoảng khác nhau thì không có hai A nằm sát nhau. Ngược lại, mọi dãy hợp lệ đều cho thấy bốn chữ A chiếm bốn khoảng riêng biệt của hàng B. Do đó ta đã lập được một tương ứng một-một giữa các dãy hợp lệ và các tập con bốn khoảng.

### 3. CHỌN BỐN TRONG SÁU KHOẢNG

**Cột phải — trình bày tuần tự:**

- Chọn 4 khoảng khác nhau trong 6.
- Các chữ A giống nhau, không cần 4!.
- Kết quả bằng tổ hợp 4 của 6.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** ĐẾM CHÍNH XÁC 15 DÃY.

**Thuyết minh:** Ta chỉ cần chọn bốn khoảng trong sáu khoảng có sẵn. Vì mọi chữ A đều như nhau, khi đã biết bốn khoảng, dãy được xác định duy nhất. Không có bước hoán vị bốn chữ A. Vậy số dãy bằng tổ hợp chập bốn của sáu, tức mười lăm. Đây là điểm khác biệt quan trọng với bài xếp bốn học sinh nữ phân biệt vào bốn khoảng, khi đó còn phải nhân bốn giai thừa.

### 4. CHỌN VỊ TRÍ KHÔNG LIỀN NHAU

**Cột phải — trình bày tuần tự:**

- Chọn k vị trí 1 ≤ i1 < ... < ik ≤ n.
- Điều kiện: i(j+1) ≥ i(j)+2.
- Đặt j(r)=i(r)-(r-1).

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** DỊCH CHỈ SỐ ĐỂ BỎ KHOẢNG CÁCH BẮT BUỘC.

**Thuyết minh:** Ta tổng quát hóa bằng cách chọn k vị trí trong n vị trí sao cho không có hai vị trí nào liền nhau. Viết các vị trí theo thứ tự tăng dần, mỗi vị trí sau phải cách vị trí trước ít nhất hai đơn vị. Hãy tạo một dãy vị trí mới: lấy vị trí thứ r trừ đi r trừ một. Như vậy mỗi khoảng trống bắt buộc giữa hai vị trí được nén lại, và dãy mới chỉ còn yêu cầu tăng nghiêm ngặt.

### 5. SUY RA CÔNG THỨC TỔNG QUÁT

**Cột phải — trình bày tuần tự:**

- Sau phép dịch: 1 ≤ j1 < ... < jk ≤ n-k+1.
- Chọn k số trong n-k+1 số.
- Số cách: C dưới k trên n-k+1.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** NẾU n < 2k-1 THÌ KHÔNG CÓ CÁCH NÀO.

**Thuyết minh:** Phép dịch làm vị trí cuối cùng không vượt quá n trừ k cộng một, trong khi các vị trí mới tăng nghiêm ngặt như cách chọn một tập con bình thường. Vì vậy số cách chọn k vị trí không kề nhau bằng tổ hợp chập k của n trừ k cộng một. Điều kiện tồn tại là n ít nhất bằng hai k trừ một, vì phải dành ra k vị trí được chọn cùng k trừ một vị trí ngăn cách.

### 6. NẾU HAI NHÓM ĐỀU PHÂN BIỆT

**Cột phải — trình bày tuần tự:**

- Có năm người B và bốn người A khác nhau.
- Xếp năm B: 5!; chọn bốn khoảng: 15.
- Xếp bốn A vào bốn khoảng: 4!.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** KHÔNG ĐƯỢC QUÊN HOÁN VỊ NỘI BỘ NHÓM.

**Thuyết minh:** Nếu thay năm chữ B bằng năm học sinh nam phân biệt và bốn chữ A bằng bốn học sinh nữ phân biệt, cách đếm phải thay đổi. Ta có năm giai thừa cách xếp nam, mười lăm cách chọn bốn trong sáu khoảng và bốn giai thừa cách phân công bốn nữ vào các khoảng. Kết quả là bốn mươi ba nghìn hai trăm. Như vậy cùng một sơ đồ khoảng trống, yếu tố các phần tử có phân biệt hay không quyết định những thừa số cuối cùng.

## 04 · HAI CẶP CẤM ĐỨNG CẠNH

Dùng bao hàm–loại trừ khi hai điều kiện độc lập về người.

### 1. HAI CẶP ĐỀU BỊ CẤM

**Cột phải — trình bày tuần tự:**

- Có sáu người A, B, C, D, E, F.
- AB không kề và CD không kề.
- Đếm số hàng hợp lệ.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** HAI ĐIỀU KIỆN CẤM CẦN XÉT PHẦN GIAO.

**Thuyết minh:** Ta xét sáu học sinh phân biệt, yêu cầu A không đứng cạnh B và đồng thời C không đứng cạnh D. Nếu chỉ trừ số hàng vi phạm cặp AB và trừ tiếp số hàng vi phạm cặp CD, ta có nguy cơ trừ hai lần những hàng mà cả hai cặp đều đứng cạnh nhau. Vì vậy ta sẽ gọi hai tập hợp điều kiện vi phạm là E một và E hai, rồi xử lý đúng phần giao giữa chúng.

### 2. ĐẾM TỪNG CẶP VI PHẠM

**Cột phải — trình bày tuần tự:**

- E1: A và B đứng cạnh.
- E2: C và D đứng cạnh.
- Mỗi tập có 2·5! = 240 hàng.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** TRỪ RIÊNG TỪNG BIẾN CỐ CHƯA ĐỦ.

**Thuyết minh:** Trong sáu người, nếu bắt buộc AB đứng cạnh thì ta gộp AB thành một khối, cùng bốn người còn lại tạo năm đối tượng. Hai cách sắp nội bộ của khối nhân năm giai thừa cho hai trăm bốn mươi hàng. Tương tự với CD, ta cũng được hai trăm bốn mươi. Nhưng các hàng có cả AB và CD đứng kề đang thuộc đồng thời hai tập hợp bị cấm, nên cần tìm phần giao.

### 3. ĐẾM PHẦN GIAO HAI CẶP

**Cột phải — trình bày tuần tự:**

- E1 ∩ E2: AB và CD cùng kề.
- Gộp hai khối [AB], [CD].
- Có 4!·2·2 = 96 hàng.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** PHẦN GIAO BỊ TRỪ HAI LẦN NÊN PHẢI CỘNG LẠI.

**Thuyết minh:** Khi AB cùng đứng cạnh và CD cũng đứng cạnh, hai cặp không chung người nên có thể gộp thành hai khối độc lập. Cùng E và F, ta có bốn đối tượng, sắp được bốn giai thừa cách. Bên trong hai khối có hai nhân hai thứ tự. Do đó phần giao của E một và E hai gồm chín mươi sáu hàng, chính là phần đã bị trừ hai lần khi xử lý hai biến cố riêng rẽ.

### 4. BAO HÀM - LOẠI TRỪ

**Cột phải — trình bày tuần tự:**

- Hợp hai tập cấm có 240+240-96=384.
- Lấy 720 trừ 384.
- Có 336 hàng thỏa cả hai điều kiện.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** CỘNG LẠI PHẦN GIAO ĐỂ KHÔNG TRỪ TRÙNG.

**Thuyết minh:** Nguyên lý bao hàm loại trừ cho số hàng vi phạm ít nhất một cặp bằng hai trăm bốn mươi cộng hai trăm bốn mươi trừ chín mươi sáu, tức ba trăm tám mươi bốn. Vậy số hàng không vi phạm bất kỳ cặp nào là bảy trăm hai mươi trừ ba trăm tám mươi bốn, bằng ba trăm ba mươi sáu. Ta có thể tô vùng hợp của hai vòng trên sơ đồ để thấy rõ việc trừ phần giao đúng một lần.

### 5. PHÂN BIỆT ĐÚNG MỘT CẶP

**Cột phải — trình bày tuần tự:**

- Đúng một cặp đứng cạnh.
- AB kề, CD không kề: 240-96=144.
- Đổi hai cặp: cũng 144.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** ĐÚNG MỘT KHÁC VỚI ÍT NHẤT MỘT.

**Thuyết minh:** Ta thử câu hỏi khác để tránh nhầm lẫn: có bao nhiêu hàng mà đúng một trong hai cặp AB, CD đứng cạnh? Trường hợp AB kề nhưng CD không kề có hai trăm bốn mươi trừ chín mươi sáu, tức một trăm bốn mươi bốn. Trường hợp đối xứng cũng như vậy. Hai trường hợp rời nhau nên cộng được hai trăm tám mươi tám. Kết quả này khác ba trăm tám mươi bốn của điều kiện ít nhất một cặp.

### 6. KIỂM TRA BẰNG PHÂN HOẠCH

**Cột phải — trình bày tuần tự:**

- Cả hai cặp cấm: 336 hàng.
- Đúng một cặp kề: 288 hàng.
- Cả hai cặp kề: 96 hàng.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** BA NHÓM CỘNG ĐÚNG TỔNG 720.

**Thuyết minh:** Mọi hàng xếp sáu người đều rơi vào đúng một trong ba nhóm: không có cặp nào đứng cạnh, đúng một cặp đứng cạnh, hoặc cả hai cặp đều đứng cạnh. Ta đã tính được ba trăm ba mươi sáu, hai trăm tám mươi tám và chín mươi sáu. Tổng đúng bằng bảy trăm hai mươi. Kiểm tra phân hoạch như vậy là một công cụ phát hiện lỗi rất hiệu quả, đặc biệt với bài có nhiều biến cố và công thức dài.

## 05 · RÀNG BUỘC CÓ CHUNG PHẦN TỬ

Hai điều kiện AB và BC cấm kề nhau; xác định phần giao.

### 1. CẶP CẤM CHUNG MỘT NGƯỜI

**Cột phải — trình bày tuần tự:**

- Vẫn sáu người A, B, C, D, E, F.
- Không cho AB đứng cạnh.
- Không cho BC đứng cạnh.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** HAI CẶP CẤM ĐỀU CHỨA B.

**Thuyết minh:** Bây giờ hai điều kiện cấm không còn rời nhau về đối tượng: cấm A đứng cạnh B và cấm B đứng cạnh C. Chữ B xuất hiện trong cả hai điều kiện. Ta vẫn có thể dùng nguyên lý bao hàm loại trừ, nhưng tuyệt đối không được giả định rằng hai khối AB và BC là hai khối độc lập, vì làm như vậy sẽ đếm người B hai lần. Ta cần quan sát cấu trúc hình học thật của phần giao.

### 2. MỖI CẶP VI PHẠM: 240

**Cột phải — trình bày tuần tự:**

- AB đứng kề có 2·5! hàng.
- BC đứng kề cũng có 2·5! hàng.
- Phần giao phải xét riêng.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** KHÔNG DÙNG CÔNG THỨC HAI KHỐI RỜI NHAU.

**Thuyết minh:** Số hàng A và B đứng cạnh bằng hai nhân năm giai thừa, tức hai trăm bốn mươi. Số hàng B và C đứng cạnh cũng là hai trăm bốn mươi. Tuy nhiên, muốn cùng thỏa cả hai sự đứng kề, B phải có hai hàng xóm trực tiếp A và C, nghĩa là B nằm ở giữa trong bộ ba liên tiếp. Không thể lấy hai khối riêng [AB] và [BC] rồi hoán đổi độc lập, vì chúng chồng nhau tại B.

### 3. PHẦN GIAO CÓ DẠNG ABC / CBA

**Cột phải — trình bày tuần tự:**

- B có A bên trái, C bên phải.
- Hoặc B có C bên trái, A bên phải.
- Gộp ba người thành một khối.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** CHỈ CÓ HAI THỨ TỰ ABC VÀ CBA.

**Thuyết minh:** Nếu A và B đứng cạnh, đồng thời B và C đứng cạnh, thì trong một hàng thẳng B buộc phải nằm giữa A và C. Chỉ có hai thứ tự của bộ ba liên tiếp là A B C hoặc C B A. Không được dùng sáu hoán vị của A B C, bởi bốn hoán vị còn lại không có B ở giữa. Gộp bộ ba thành một khối và xếp với D, E, F sẽ tạo bốn đối tượng.

### 4. ĐẾM HỢP, LẤY PHẦN BÙ

**Cột phải — trình bày tuần tự:**

- Tổng số hàng: 720.
- Hai tập cấm: 240 và 240.
- Phần giao: 48.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** SỐ HÀNG HỢP LỆ BẰNG 288.

**Thuyết minh:** Khi đếm các hàng không có AB đứng kề và cũng không có BC đứng kề, ta lấy tổng bảy trăm hai mươi, trừ hai trăm bốn mươi hàng có AB kề, trừ thêm hai trăm bốn mươi hàng có BC kề, rồi cộng lại bốn mươi tám hàng thuộc phần giao. Kết quả là hai trăm tám mươi tám. Đây là ví dụ cho thấy công thức bao hàm loại trừ luôn giữ nguyên, nhưng cách đếm phần giao phụ thuộc rất mạnh vào cấu trúc ràng buộc.

### 5. NẾU CẤM CẢ AB, BC, AC

**Cột phải — trình bày tuần tự:**

- Ba cặp của A, B, C đều bị cấm.
- Mỗi cặp riêng: 240 hàng.
- Mỗi giao đôi: 48; giao ba: 0.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** KHÔNG THỂ BA NGƯỜI ĐỀU KỀ TỪNG ĐÔI TRÊN HÀNG.

**Thuyết minh:** Hãy tăng độ khó: yêu cầu A, B, C không có bất kỳ cặp nào đứng cạnh nhau. Có ba tập vi phạm tương ứng AB, BC, AC. Mỗi tập có hai trăm bốn mươi hàng, mỗi giao của hai tập có bốn mươi tám hàng, nhưng không thể ba người đều đứng cạnh nhau từng đôi một trong hàng thẳng. Vậy số hàng hợp lệ là bảy trăm hai mươi trừ ba lần hai trăm bốn mươi cộng ba lần bốn mươi tám, bằng một trăm bốn mươi bốn.

### 6. ĐỐI CHIẾU BẰNG KHOẢNG TRỐNG

**Cột phải — trình bày tuần tự:**

- Xếp D, E, F trước: 3! cách.
- Có bốn khoảng; chọn ba khoảng cho ABC.
- Ba người A, B, C hoán vị: 3!.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** CÙNG MỘT KẾT QUẢ: 144 HÀNG.

**Thuyết minh:** Với yêu cầu A, B và C đều không đứng cạnh nhau từng đôi một, ta còn có cách làm trực tiếp ngắn hơn. Xếp ba người D, E, F trước, có ba giai thừa cách. Họ tạo bốn khoảng trống; ta chọn ba khoảng khác nhau trong bốn, rồi đặt A, B, C vào ba khoảng đã chọn theo ba giai thừa cách. Kết quả cũng bằng một trăm bốn mươi bốn. Hai phương pháp khớp nhau, giúp xác nhận phép đếm phần giao ở bài nâng cao.

## 06 · XẾP NAM NỮ VỚI KHOẢNG TRỐNG

Phân biệt không đứng kề và đứng xen kẽ.

### 1. NĂM NAM, BA NỮ PHÂN BIỆT

**Cột phải — trình bày tuần tự:**

- Có năm học sinh nam và ba học sinh nữ.
- Không có hai nữ nào đứng cạnh nhau.
- Xếp thành một hàng.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** ĐỪNG NHẦM KHÔNG KỀ VỚI XEN KẼ HOÀN TOÀN.

**Thuyết minh:** Một lớp có năm nam và ba nữ, tất cả đều là người phân biệt. Ta cần xếp tám người thành một hàng sao cho không có hai nữ nào đứng liền nhau. Hãy chú ý đề không nói nam và nữ phải xen kẽ hoàn toàn; vì số nam nhiều hơn, có thể xuất hiện hai hoặc ba nam đứng cạnh mà bài vẫn hợp lệ. Vì vậy mô hình chính xác là chọn khoảng trống trong một hàng nam, không phải ép một mẫu nữ nam cố định.

### 2. XẾP NĂM NAM TRƯỚC

**Cột phải — trình bày tuần tự:**

- Năm nam phân biệt: 5! cách.
- Từ một hàng nam tạo sáu khoảng.
- Mỗi khoảng có tối đa một nữ.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** ĐẶT NAM LÀM CÁC VẬT NGĂN CÁCH.

**Thuyết minh:** Trước tiên, ta sắp xếp năm học sinh nam vào một hàng. Có năm giai thừa cách. Với bất cứ thứ tự nam nào, ta luôn có sáu khoảng: một trước hàng, bốn khoảng giữa hai nam liên tiếp và một ở cuối hàng. Để các bạn nữ không đứng cạnh nhau, mỗi khoảng chỉ được nhận tối đa một nữ. Khi đó mọi cách đặt các nữ vào những khoảng khác nhau đều hợp lệ.

### 3. CHỌN BA TRONG SÁU KHOẢNG

**Cột phải — trình bày tuần tự:**

- Chọn ba khoảng khác nhau.
- Số cách chọn: C dưới 3 trên 6 = 20.
- Sau đó mới sắp ba nữ.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** CHỌN KHOẢNG KHÔNG ĐỒNG NGHĨA PHÂN CÔNG NỮ.

**Thuyết minh:** Ta chọn ba trong sáu khoảng an toàn của hàng nam. Khi chọn, ba khoảng mới là một tập hợp, không phân biệt thứ tự chọn. Do đó có tổ hợp chập ba của sáu, tức hai mươi cách. Sau bước này, ta cần quyết định nữ thứ nhất vào khoảng nào, nữ thứ hai vào khoảng nào và nữ thứ ba vào khoảng nào. Đây là công việc khác với chọn tập hợp khoảng và sẽ đóng góp thừa số ba giai thừa.

### 4. ĐẾM ĐẦY ĐỦ KẾT QUẢ

**Cột phải — trình bày tuần tự:**

- Xếp nam: 5! = 120.
- Chọn khoảng: 20.
- Phân công nữ: 3! = 6.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** CÓ 14.400 CÁCH HỢP LỆ.

**Thuyết minh:** Mỗi cách xếp nam tạo sáu khoảng. Ta chọn ba khoảng, rồi hoán vị ba học sinh nữ vào đó. Áp dụng quy tắc nhân, số hàng hợp lệ là năm giai thừa nhân tổ hợp chập ba của sáu nhân ba giai thừa, cho kết quả mười bốn nghìn bốn trăm. Mỗi hàng có thể được khôi phục duy nhất bằng cách xóa các nữ để lấy hàng nam, xác định ba khoảng đã dùng, rồi đọc lại tên các nữ trong từng khoảng. Vì vậy không có đếm trùng.

### 5. KHI NÀO KHÔNG CÓ CÁCH NÀO

**Cột phải — trình bày tuần tự:**

- m nam tạo m+1 khoảng.
- Muốn tách k nữ cần k khoảng riêng.
- Nếu k > m+1 thì không thể.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** ĐIỀU KIỆN TỒN TẠI LÀ k ≤ m+1.

**Thuyết minh:** Công thức phương pháp khoảng trống có một điều kiện tồn tại rất tự nhiên. Nếu có m bạn nam thì chỉ có m cộng một khoảng để chèn các nữ mà không có hai nữ đứng cạnh. Nếu số nữ k lớn hơn m cộng một, nguyên lý Dirichlet cho thấy chắc chắn có ít nhất hai nữ phải chung một khoảng, tức đứng cạnh nhau. Khi số nữ không vượt số khoảng, ta mới có thể chọn các khoảng khác nhau để xếp.

### 6. SO SÁNH VỚI XEN KẼ ĐÚNG

**Cột phải — trình bày tuần tự:**

- Bốn nam và bốn nữ phân biệt.
- Xen kẽ hoàn toàn có hai mẫu N–G.
- Mỗi mẫu có 4!·4! cách.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** XEN KẼ HOÀN TOÀN CHẶT HƠN KHÔNG KỀ.

**Thuyết minh:** Hãy so sánh với bài có bốn nam, bốn nữ, yêu cầu nam nữ ngồi xen kẽ hoàn toàn. Chỉ có hai mẫu vị trí: nam trước hoặc nữ trước. Với mỗi mẫu, sắp bốn nam vào bốn vị trí nam và bốn nữ vào bốn vị trí nữ, được bốn giai thừa nhân bốn giai thừa cách. Nhân hai mẫu ta được một nghìn một trăm năm mươi hai. Điều kiện xen kẽ hoàn toàn mạnh hơn yêu cầu không có hai nữ đứng cạnh, nên không được dùng thay cho nhau.

## 07 · KHÔNG ĐỨNG KỀ QUANH BÀN TRÒN

Tạo khoảng trên vòng tròn; phép quay được xem là như nhau.

### 1. VÒNG TRÒN CÓ SỰ KHÁC BIỆT

**Cột phải — trình bày tuần tự:**

- Sáu người phân biệt ngồi bàn tròn.
- Hai cách chỉ khác phép quay là một.
- A, B không được ngồi cạnh.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** KHÔNG DÙNG N! CHO BÀN TRÒN KHÔNG ĐÁNH SỐ.

**Thuyết minh:** Chuyển sang bàn tròn, chúng ta phải quyết định thế nào là một cách xếp khác nhau. Nếu các ghế không đánh số và chỉ quay cả bàn không tạo ra cách mới, số cách xếp sáu người là năm giai thừa. Trong bài này hai người A và B không được ngồi sát nhau theo hai phía vòng tròn, tức mỗi người có đúng hai hàng xóm. Chú ý hai ghế đầu và cuối của hàng thẳng khi uốn thành vòng cũng trở thành kề nhau.

### 2. ĐẾM NHÓM A B NGỒI CẠNH

**Cột phải — trình bày tuần tự:**

- Gộp A, B thành một khối quanh bàn.
- Còn năm đối tượng phân biệt.
- Có (5-1)!·2 = 48 cách.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** PHẢI GIỮ TÍNH VÒNG SAU KHI GỘP KHỐI.

**Thuyết minh:** Khi A và B ngồi cạnh trên vòng tròn, ta gộp hai người thành một khối. Cùng bốn người còn lại, có năm đối tượng quanh bàn. Vì các phép quay được đồng nhất, số thứ tự của năm đối tượng là bốn giai thừa, không phải năm giai thừa. Nhân thêm hai thứ tự AB, BA bên trong khối, ta được bốn mươi tám cách vi phạm. Ta đang xem các chiều kim đồng hồ và ngược chiều là khác nhau, không tự động đồng nhất ảnh gương.

### 3. LẤY PHẦN BÙ TRÊN VÒNG

**Cột phải — trình bày tuần tự:**

- Tất cả: 5! = 120.
- A và B ngồi cạnh: 48.
- Không cạnh nhau: 72.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** PHẢI KIỂM TRA CẠNH NỐI CUỐI VÀ ĐẦU.

**Thuyết minh:** Vậy số cách để hai người A và B không ngồi cạnh nhau là một trăm hai mươi trừ bốn mươi tám, bằng bảy mươi hai. Nếu thử biến vòng tròn thành hàng thẳng bằng cách cắt tại một điểm tùy ý, ta sẽ dễ quên rằng hai đầu hàng đang kề nhau trên vòng. Đó là lý do nên cố định một người hoặc giữ trực tiếp mô hình vòng tròn trong mọi bước lập luận.

### 4. BỐN NAM, BA NỮ NGỒI VÒNG

**Cột phải — trình bày tuần tự:**

- Bốn nam và ba nữ phân biệt.
- Không có hai nữ ngồi cạnh.
- Xếp nam quanh bàn rồi chèn nữ.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** TRÊN VÒNG CÓ m KHOẢNG, KHÔNG PHẢI m+1.

**Thuyết minh:** Ta xét bốn nam và ba nữ phân biệt quanh một bàn tròn không đánh số. Muốn các nữ không ngồi cạnh nhau, ta xếp bốn nam quanh bàn trước. Khác với hàng thẳng, vòng tròn tạo ra đúng bốn khoảng giữa bốn người nam, vì không có khoảng trước đầu hàng hay sau cuối hàng. Mỗi nữ phải chiếm một khoảng khác nhau. Đây là nét khác biệt cốt lõi khi vận dụng phương pháp khoảng trống trên vòng.

### 5. CHỌN BA TRONG BỐN KHOẢNG

**Cột phải — trình bày tuần tự:**

- Xếp nam vòng tròn: 3! cách.
- Chọn ba trong bốn khoảng: 4 cách.
- Sắp ba nữ: 3! cách.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** KẾT QUẢ 144 CÁCH.

**Thuyết minh:** Số cách xếp bốn nam quanh bàn là ba giai thừa, bằng sáu. Có bốn khoảng trên vòng nên số cách chọn ba khoảng là tổ hợp chập ba của bốn, bằng bốn. Ba nữ phân biệt được hoán vị vào ba khoảng đã chọn theo ba giai thừa cách. Nhân ba thừa số cho kết quả một trăm bốn mươi bốn cách. Mỗi cách xếp hợp lệ xác định duy nhất thứ tự vòng của bốn nam và ba khoảng chứa nữ.

### 6. SO SÁNH HÀNG VÀ VÒNG

**Cột phải — trình bày tuần tự:**

- Hàng thẳng: m+1 khoảng.
- Bàn tròn: m khoảng.
- Xoay bàn là cùng cách, lật gương thì khác.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** LÀM RÕ QUY ƯỚC TRƯỚC KHI ÁP DỤNG.

**Thuyết minh:** Chốt lại, khi xếp một nhóm nền gồm m người thành hàng thẳng, ta có m cộng một khoảng chèn. Khi xếp quanh bàn tròn không đánh số, ta chỉ có m khoảng và còn phải đồng nhất các hoán vị khác nhau bởi phép quay. Nếu đề bài quy định ghế đánh số thì mỗi vị trí ghế là cố định, phép quay không được đồng nhất. Nếu đề bài cho phép đồng nhất cả ảnh gương, lại là một mô hình đếm khác. Phải đọc rõ quy ước trước khi tính.

## 08 · BA CẶP CẤM KỀ - HSG

Phối hợp toàn bộ kỹ thuật trên 8 người phân biệt.

### 1. BÀI TOÁN BA CẶP BỊ CẤM

**Cột phải — trình bày tuần tự:**

- Tám người A, B, C, D, E, F, G, H.
- AB, CD và EF đều không kề nhau.
- Tìm số hàng thỏa ba điều kiện.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** BA RÀNG BUỘC CẤM CẦN BAO HÀM–LOẠI TRỪ.

**Thuyết minh:** Ở bài cuối, chúng ta xét tám người phân biệt và ba cặp chỉ định AB, CD, EF. Mỗi cặp đều không được đứng cạnh nhau khi xếp tám người thành một hàng. Người G, H không thuộc cặp cấm nào. Với ba điều kiện, việc lấy tổng trừ đơn giản dễ bị trừ trùng. Hãy đặt ba tập hợp vi phạm tương ứng E một, E hai, E ba rồi áp dụng bao hàm loại trừ đầy đủ đến phần giao ba tập.

### 2. ĐẾM HÀNG VI PHẠM MỘT CẶP

**Cột phải — trình bày tuần tự:**

- Một cặp đứng kề: 2·7!.
- Có ba cặp chỉ định giống cấu trúc.
- Tổng ba số riêng: 3·2·7!.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** CHÚ Ý MỖI HÀNG CÓ THỂ VI PHẠM NHIỀU CẶP.

**Thuyết minh:** Nếu chỉ bắt buộc A và B đứng cạnh, ta gộp thành một khối cùng sáu người còn lại, tức bảy đối tượng. Có bảy giai thừa cách xếp ngoài và hai thứ tự trong khối, cho mười nghìn không trăm tám mươi hàng. Các cặp CD và EF có cùng số lượng. Tổng ba số riêng là ba nhân hai nhân bảy giai thừa, nhưng đang tính nhiều lần những hàng vi phạm hơn một cặp, nên chưa phải số hàng bị cấm cuối cùng.

### 3. ĐẾM GIAO CỦA HAI CẶP

**Cột phải — trình bày tuần tự:**

- Chọn hai trong ba cặp: 3 cách.
- Gộp hai khối và hai người còn lại.
- Mỗi giao có 2²·6! hàng.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** PHẢI CỘNG LẠI BA PHẦN GIAO ĐÔI.

**Thuyết minh:** Nếu AB và CD cùng đứng kề, chúng là hai khối rời nhau cùng bốn người E, F, G, H, vậy có sáu đối tượng. Hai khối có tổng cộng bốn thứ tự nội bộ. Do đó mỗi giao đôi có bốn nhân sáu giai thừa, bằng hai nghìn tám trăm tám mươi hàng. Có tổ hợp chập hai của ba cách chọn hai cặp trong ba cặp, tức ba giao đôi. Tổng phần được cộng trở lại bằng ba nhân bốn nhân sáu giai thừa.

### 4. ĐẾM GIAO CỦA BA CẶP

**Cột phải — trình bày tuần tự:**

- AB, CD và EF đồng thời kề.
- Ba khối cùng G, H: 5 đối tượng.
- Có 2³·5! = 960 hàng.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** PHẦN GIAO BA PHẢI BỊ TRỪ LẦN CUỐI.

**Thuyết minh:** Nếu cả ba cặp AB, CD và EF đều đứng cạnh nhau, gộp mỗi cặp thành một khối. Ta có ba khối và hai người còn lại G, H, tổng cộng năm đối tượng. Có năm giai thừa cách xếp năm đối tượng và tám thứ tự bên trong ba khối. Như vậy phần giao ba tập cấm có chín trăm sáu mươi hàng. Trong bao hàm loại trừ, sau khi đã trừ các tập đơn và cộng các giao đôi, ta phải trừ đi giao ba này một lần.

### 5. TÍNH SỐ HÀNG HỢP LỆ

**Cột phải — trình bày tuần tự:**

- Tổng: 40320.
- Trừ 30240, cộng 8640, trừ 960.
- Còn 17760 hàng hợp lệ.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** CÔNG THỨC PHẢI ĐÚNG TỪNG HẠNG TỬ.

**Thuyết minh:** Ghép các kết quả lại, số hàng hợp lệ là tám giai thừa, trừ ba lần hai nhân bảy giai thừa, cộng ba lần bốn nhân sáu giai thừa, rồi trừ tám nhân năm giai thừa. Ta được mười bảy nghìn bảy trăm sáu mươi hàng. Điều quan trọng không chỉ là đáp số mà là ý nghĩa của dấu trừ, cộng, trừ theo từng tầng giao biến cố. Hình động sẽ lần lượt tô những vùng vừa được loại, rồi được hoàn lại.

### 6. BÀI HỌC CUỐI VÀ KIỂM CHỨNG

**Cột phải — trình bày tuần tự:**

- Liệt kê 8! hàng bằng Python để kiểm tra.
- So sánh 17760 với công thức.
- Phân biệt phương pháp thích hợp từng bài.

**Cột trái — mô hình:**
- Hình động diễn tả điều kiện được chọn/cấm; đỏ biểu thị vi phạm, xanh biểu thị hợp lệ.

**Kết luận:** ĐỌC ĐIỀU KIỆN TRƯỚC, CÔNG THỨC SAU.

**Thuyết minh:** Ta có thể liệt kê toàn bộ bốn mươi nghìn ba trăm hai mươi hoán vị của tám người để kiểm tra rằng đúng mười bảy nghìn bảy trăm sáu mươi hàng không chứa bất kỳ cặp đứng kề bị cấm nào. Kết thúc bài, hãy tự hỏi: khi cấm một cặp, dùng phần bù; khi cần tách một nhóm, dùng khoảng trống; khi có nhiều cặp cấm, dùng bao hàm loại trừ; khi các cặp chung phần tử, cần xử lý riêng phần giao. Đó mới là tư duy giải toán tổ hợp.

