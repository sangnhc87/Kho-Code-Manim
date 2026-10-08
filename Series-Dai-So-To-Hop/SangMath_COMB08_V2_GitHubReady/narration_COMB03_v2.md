# SANG MATH · COMB03 V2 · SƠ ĐỒ CÂY VÀ KHÔNG GIAN MẪU

## Bản thuyết minh đồng bộ

Số nhịp: 48 · 8 chương · TTS=off
Tổng thời lượng dự kiến: 821.2 giây.
Lời giảng bên dưới là nội dung đầy đủ được đưa vào tổng hợp giọng đọc; không cắt tùy ý.


## 01  BÀI TOÁN MỞ ĐẦU

### Nhịp 01 · 00:00 · BA LẦN TUNG ĐỒNG XU

Bài toán đầu tiên của chúng ta rất quen thuộc. Tung một đồng xu ba lần, mỗi lần ghi ngửa là N và sấp là S. Hãy dự đoán có bao nhiêu dãy kết quả. Chú ý rằng N rồi S khác S rồi N vì thứ tự các lần tung có ý nghĩa.

**Trên màn hình:** Một đồng xu có hai mặt N và S. | Tung liên tiếp ba lần. | Ta cần đếm các dãy kết quả.
**Ghi nhớ:** Thứ tự ba lần tung được giữ lại.

### Nhịp 02 · 00:17 · ĐÂU LÀ MỘT KẾT QUẢ?

Khi ta viết N S N, ký hiệu thứ nhất là lần gieo đầu, ký hiệu thứ hai là lần gieo tiếp theo, ký hiệu cuối là lần gieo thứ ba. Thay đổi thứ tự ký hiệu có thể tạo kết quả mới. Một kết quả hoàn chỉnh không thể thiếu vị trí nào.

**Trên màn hình:** Ví dụ: N, S, N là một dãy. | Dãy S, N, N là kết quả khác. | Mỗi dãy phải có đủ ba ký hiệu.
**Ghi nhớ:** Một kết quả có đúng ba vị trí.

### Nhịp 03 · 00:34 · TẠI SAO PHẢI LIỆT KÊ?

Nếu liệt kê ngẫu nhiên, em có thể viết trùng một dãy hoặc quên một dãy khác. Sơ đồ cây giúp mỗi bước chọn có một nhánh rõ ràng. Chúng ta sẽ nhìn tận mắt cách cây phát triển để biết tất cả kết quả xuất hiện từ đâu.

**Trên màn hình:** Đoán bằng cảm giác dễ thiếu. | Liệt kê tự do dễ bị lặp. | Cần một phương pháp có hệ thống.
**Ghi nhớ:** Sơ đồ cây sẽ giải quyết hai lỗi.

### Nhịp 04 · 00:51 · HAI KẾT QUẢ MỖI LẦN

Với mô hình đồng xu thông thường, ở mỗi lần tung ta ghi lại một trong hai ký hiệu N hoặc S. Ta không giả định kết quả lần trước sẽ hạn chế kết quả lần sau. Vì vậy mỗi bước luôn có hai lựa chọn, và ta cần đi qua cả ba bước.

**Trên màn hình:** Lần tung thứ nhất: N hoặc S. | Lần tung thứ hai: N hoặc S. | Lần tung thứ ba: N hoặc S.
**Ghi nhớ:** Mỗi bước có đúng hai lựa chọn.

### Nhịp 05 · 01:08 · DỰ ĐOÁN SỐ DÃY

Ta đã học quy tắc nhân ở bài trước. Nhưng ở đây hãy tạm chưa dùng công thức. Hãy cùng xây dựng từng tầng của cây lựa chọn, đếm số lá cuối cùng rồi mới giải thích vì sao phép nhân hai nhân hai nhân hai xuất hiện.

**Trên màn hình:** Có ba lần lựa chọn liên tiếp. | Mỗi lần có hai khả năng. | Đừng cộng hai với hai với hai.
**Ghi nhớ:** Hãy chờ cây cho câu trả lời.

### Nhịp 06 · 01:25 · QUY ƯỚC MÀU VÀ KÝ HIỆU

Để đọc hình nhanh, chúng ta thống nhất N màu xanh và S màu vàng. Các vòng tròn ở giữa chỉ là trạng thái chưa hoàn thành. Chỉ khi đi đủ ba nhánh, ta mới có một dãy đầy đủ để đưa vào không gian mẫu.

**Trên màn hình:** N: mặt ngửa, màu xanh cyan. | S: mặt sấp, màu vàng. | Mỗi đường đi là một dãy.
**Ghi nhớ:** Đếm lá, không đếm nút trung gian.


## 02  CÂY PHÁT TRIỂN TỪNG TẦNG

### Nhịp 07 · 01:42 · TỪ GỐC ĐẾN TẦNG MỘT

Đầu cây là trạng thái chưa ghi nhận lần tung nào. Từ đó mở ra hai khả năng của lần tung đầu. Đi theo N là bắt đầu một dãy bằng ngửa. Đi theo S là bắt đầu một dãy bằng sấp. Cả hai vẫn cần hai lần tung nữa.

**Trên màn hình:** Khởi đầu: chưa tung lần nào. | Mở hai nhánh N và S. | Mỗi nhánh là một tiền tố.
**Ghi nhớ:** Chưa có dãy dài ba ký hiệu.

### Nhịp 08 · 01:59 · MỞ TẦNG THỨ HAI

Từ nhánh N, lần tung thứ hai cho NN hoặc NS. Từ nhánh S, ta có SN hoặc SS. Vậy sau hai lần đã có bốn dãy tạm thời. Mỗi dãy tạm thời khác nhau ở ít nhất một vị trí, nên không bị đếm trùng.

**Trên màn hình:** Từ N mở tiếp NN và NS. | Từ S mở tiếp SN và SS. | Có bốn tiền tố dài hai.
**Ghi nhớ:** Hai bước tạo 2 × 2 = 4 nhánh.

### Nhịp 09 · 02:16 · THÊM LẦN TUNG THỨ BA

Giờ cây tiếp tục mọc thêm tầng thứ ba. Chẳng hạn từ NN, ta nối thêm N để có NNN, hoặc nối thêm S để có NNS. Tương tự cho NS, SN và SS. Mỗi tiền tố dài hai sinh ra đúng hai kết quả hoàn chỉnh.

**Trên màn hình:** Mỗi tiền tố dài hai mở hai lá. | NN tạo NNN và NNS. | Các tiền tố còn lại tương tự.
**Ghi nhớ:** Bốn nhánh, mỗi nhánh hai lá.

### Nhịp 10 · 02:33 · TÁM LÁ CUỐI CÙNG

Quan sát tất cả lá ở cột phải của cây. Ta có tám dãy, bắt đầu từ NNN và kết thúc bằng SSS. Không cần nhớ thuộc lòng danh sách. Ta chỉ cần biết rằng có hai nhánh ở mỗi tầng và mỗi đường đi đến đúng một lá cuối cùng.

**Trên màn hình:** Liệt kê theo thứ tự nhánh cây. | Mỗi lá là một dãy ba ký hiệu. | Số lá cuối cùng là tám.
**Ghi nhớ:** Có 2 × 2 × 2 = 8 dãy.

### Nhịp 11 · 02:50 · THEO DÕI MỘT ĐƯỜNG ĐI

Ta thử chọn ngửa ở lần một, sấp ở lần hai, rồi ngửa ở lần ba. Dấu chỉ dẫn đi theo nhánh N, sau đó S, sau đó N và dừng tại lá NSN. Đây là cách đọc một kết quả từ sơ đồ cây, theo đúng thứ tự thời gian.

**Trên màn hình:** Gốc → N → NS → NSN. | Một lần đi hết cây được một dãy. | Đường khác cho dãy khác.
**Ghi nhớ:** Đường đi mã hóa kết quả.

### Nhịp 12 · 03:07 · LIÊN HỆ QUY TẮC NHÂN

Sơ đồ cây chính là hình ảnh của quy tắc nhân. Mỗi lần gieo làm số đường đi có thể tăng gấp đôi. Một, rồi hai, rồi bốn, rồi tám. Kết luận là hai mũ ba bằng tám, bởi có ba bước và mỗi bước đều có hai lựa chọn.

**Trên màn hình:** Ba bước liên tiếp. | Mỗi bước có hai cách. | Mỗi kết quả tương ứng một đường.
**Ghi nhớ:** Số dãy là 2³ = 8.


## 03  KHÔNG GIAN MẪU

### Nhịp 13 · 03:24 · KHÔNG GIAN MẪU LÀ GÌ?

Bây giờ ta đặt tên cho tập hợp tất cả các kết quả có thể xảy ra. Trong xác suất, tập đó gọi là không gian mẫu, ký hiệu ô mê ga. Với phép tung đồng xu ba lần, mỗi phần tử của không gian mẫu là một dãy có thứ tự gồm ba chữ N hoặc S.

**Trên màn hình:** Không gian mẫu gồm mọi kết quả. | Mỗi dãy ba ký hiệu là một phần tử. | Ký hiệu không gian mẫu là Ω.
**Ghi nhớ:** Phải có đầy đủ các khả năng.

### Nhịp 14 · 03:41 · VIẾT ĐẦY ĐỦ KHÔNG GIAN MẪU

Hãy đọc các lá của cây từ trên xuống. Ta thu được NNN, NNS, NSN, NSS, SNN, SNS, SSN và SSS. Đây là toàn bộ không gian mẫu của thí nghiệm. Ta không tự thêm dãy khác, và cũng không bỏ đi kết quả chỉ vì nó ít gặp.

**Trên màn hình:** Ω = {NNN, NNS, NSN, NSS, | SNN, SNS, SSN, SSS}. | Các phần tử không trùng nhau.
**Ghi nhớ:** Không gian mẫu có tám phần tử.

### Nhịp 15 · 03:58 · KÝ HIỆU SỐ PHẦN TỬ

Dấu gạch hai bên ô mê ga biểu thị số phần tử của tập hợp. Sơ đồ cây cho biết số phần tử ấy bằng tám. Đến đây chúng ta mới làm phép đếm. Muốn nói về xác suất, ta còn phải kiểm tra các kết quả có đồng khả năng hay không.

**Trên màn hình:** Dùng ký hiệu |Ω|. | Ở đây |Ω| = 8. | Đếm kết quả, chưa tính xác suất.
**Ghi nhớ:** |Ω| = 2³ = 8.

### Nhịp 16 · 04:15 · LÁ VÀ PHẦN TỬ TẬP HỢP

Mỗi lá được nhận diện bằng đúng ba lựa chọn trên đường từ gốc. Ngược lại, từ một dãy bất kỳ như S N S, ta lần lượt chọn nhánh S, N, S và tới một lá duy nhất. Sự tương ứng hai chiều ấy chứng minh phép đếm là đầy đủ, không trùng.

**Trên màn hình:** Mỗi lá cho một phần tử Ω. | Mỗi phần tử xác định một lá. | Hai chiều đối chiếu chính xác.
**Ghi nhớ:** Đếm lá tương đương đếm dãy.

### Nhịp 17 · 04:32 · ĐỒNG KHẢ NĂNG KHÁC ĐẾM

Nếu đồng xu cân đối và các lần tung độc lập, tám dãy có cùng xác suất một phần tám. Nếu đồng xu bị lệch, chúng ta vẫn có tám kết quả có thể xảy ra, nhưng chúng có thể không cùng xác suất. Vì thế đếm không gian mẫu và tính xác suất là hai việc khác nhau.

**Trên màn hình:** Đồng xu cân đối: các dãy đồng khả năng. | Khi đó mỗi dãy có xác suất 1/8. | Đồng xu lệch: không được suy như vậy.
**Ghi nhớ:** Phải nêu giả thiết đồng xu cân đối.

### Nhịp 18 · 04:49 · MỘT BIẾN CỐ LÀ TẬP CON

Ví dụ, biến cố xuất hiện đúng hai lần ngửa gồm một số dãy trong tám dãy. Ta không cần tạo không gian mẫu mới. Chỉ cần chọn những lá thỏa điều kiện bên trong cây đã có. Cách nhìn này sẽ giúp giải bài toán có ràng buộc ở phần tiếp theo.

**Trên màn hình:** Biến cố chứa các kết quả thỏa mãn. | Không gian mẫu là tập lớn. | Biến cố là tập con của Ω.
**Ghi nhớ:** Tô sáng lá chính là chọn phần tử.


## 04  BIẾN CỐ ĐÚNG HAI LẦN NGỬA

### Nhịp 19 · 05:06 · ĐÚNG HAI LẦN NGỬA

Bây giờ hãy tìm những dãy có chính xác hai lần ngửa. Từ chính xác rất quan trọng: dãy ba lần ngửa không được tính. Ta nhìn từng lá và đếm số chữ N. Những dãy có đúng hai chữ N sẽ được tô xanh, còn các dãy khác tạm thời mờ đi.

**Trên màn hình:** Ba lần tung, đúng hai ký hiệu N. | Ký hiệu còn lại phải là S. | Tìm những lá thỏa yêu cầu.
**Ghi nhớ:** Điều kiện đúng hai, không phải ít nhất hai.

### Nhịp 20 · 05:23 · DÃY THỨ NHẤT: NNS

Xét dãy NNS. Có hai chữ N ở hai vị trí đầu và một chữ S ở cuối, nên đây là một kết quả cần đếm. Ta chọn chính lá đó trong cây, không tô cả nhánh NN vì nhánh NN còn dẫn đến dãy NNN không thỏa điều kiện.

**Trên màn hình:** Hai lần đầu là N. | Lần thứ ba là S. | Dãy NNS thỏa mãn.
**Ghi nhớ:** Đánh dấu một lá hợp lệ.

### Nhịp 21 · 05:40 · DÃY THỨ HAI: NSN

Tiếp theo là NSN. Vẫn có đúng hai lần ngửa, nhưng chúng xuất hiện ở hai thời điểm khác với NNS. Vì thứ tự các lần tung tạo ra các dãy khác nhau, NSN phải được tính thêm như một kết quả riêng biệt trong biến cố.

**Trên màn hình:** Chữ N ở vị trí một và ba. | Chữ S ở vị trí giữa. | Dãy NSN cũng thỏa mãn.
**Ghi nhớ:** Đếm thêm một kết quả.

### Nhịp 22 · 05:57 · DÃY THỨ BA: SNN

Dãy SNN có một lần sấp ở đầu và hai lần ngửa liên tiếp phía sau. Bài này chỉ yêu cầu đúng hai lần ngửa, không cấm chúng đứng cạnh nhau. Vì vậy SNN vẫn là kết quả hợp lệ. Ta có đủ ba dãy NNS, NSN và SNN.

**Trên màn hình:** Chữ S xuất hiện đầu tiên. | Hai vị trí cuối đều là N. | Dãy SNN thỏa mãn.
**Ghi nhớ:** Đã có ba kết quả khác nhau.

### Nhịp 23 · 06:14 · TẬP HỢP BIẾN CỐ A

Ta gom ba dãy được tô sáng thành biến cố A. Số kết quả thuận lợi là ba. Hãy phân biệt số ba này với tổng số kết quả có thể xảy ra là tám. Hai số có vai trò khác nhau: một số đếm điều kiện, số còn lại đếm cả không gian mẫu.

**Trên màn hình:** A = {NNS, NSN, SNN}. | Biến cố A có ba phần tử. | Các dãy khác đều bị loại.
**Ghi nhớ:** |A| = 3.

### Nhịp 24 · 06:31 · NẾU ĐỒNG XU CÂN ĐỐI

Khi đồng xu cân đối và mỗi lần gieo độc lập, cả tám dãy là đồng khả năng. Xác suất của biến cố A bằng số kết quả thuận lợi chia tổng số kết quả, tức ba phần tám. Nếu không có giả thiết cân đối, ta không được tự động kết luận xác suất là ba phần tám.

**Trên màn hình:** Mỗi dãy có xác suất bằng nhau. | Có 3 kết quả thuận lợi trong 8. | Khi đó P(A) = 3/8.
**Ghi nhớ:** Đếm chính xác trước, xác suất sau.


## 05  ĐIỀU KIỆN KHÔNG LIÊN TIẾP

### Nhịp 25 · 06:48 · KHÔNG CÓ HAI N LIÊN TIẾP

Bài toán mới không hỏi số lần ngửa, mà hỏi vị trí của chúng. Trong ba lần tung, không được có hai chữ N nằm liền nhau. Điều này buộc ta kiểm tra cặp vị trí một và hai, đồng thời kiểm tra cặp vị trí hai và ba. Hãy cùng lọc trên cây.

**Trên màn hình:** Vẫn xét ba lần tung. | Không cho phép xuất hiện chuỗi NN. | Ta cần tìm mọi dãy hợp lệ.
**Ghi nhớ:** Kiểm tra hai cặp vị trí kề nhau.

### Nhịp 26 · 07:05 · KIỂM TRA CẶP ĐẦU

Ta quan sát hai lần tung đầu tiên. Nếu hai ký hiệu đầu là NN, điều kiện đã bị vi phạm ngay lập tức. Bất kể lần thứ ba là gì, dãy không hợp lệ. Vì vậy cả NNN và NNS đều bị loại, đúng hai lá chứ không phải một.

**Trên màn hình:** Nếu bắt đầu bằng NN thì sai. | Các dãy NNN và NNS bị loại. | Không xóa nhánh NS.
**Ghi nhớ:** Loại trọn nhánh NN.

### Nhịp 27 · 07:22 · KIỂM TRA CẶP CUỐI

Còn một lỗi có thể nằm ở hai vị trí cuối. Dãy SNN bắt đầu bằng S, nhưng hai lần tung tiếp theo đều ngửa nên vẫn vi phạm. Ta loại thêm dãy SNN. Đến đây ba lá bị loại là NNN, NNS và SNN, không trùng nhau.

**Trên màn hình:** Dãy SNN cũng chứa NN. | Loại SNN khỏi kết quả. | Các dãy còn lại phải kiểm tra đủ.
**Ghi nhớ:** Có tổng cộng ba lá bị loại.

### Nhịp 28 · 07:39 · NĂM DÃY HỢP LỆ

Quan sát năm lá còn sáng xanh: NSN, NSS, SNS, SSN và SSS. Hãy tự đọc từng dãy để chắc chắn không có hai lần ngửa đứng cạnh nhau. Ta đã loại tất cả trường hợp sai mà không vô tình xóa một trường hợp đúng.

**Trên màn hình:** NSN, NSS, SNS, SSN, SSS. | Không dãy nào chứa NN. | Mỗi lá được tính đúng một lần.
**Ghi nhớ:** Có năm kết quả thỏa điều kiện.

### Nhịp 29 · 07:56 · GIẢI BẰNG PHẦN BÙ

Có thể đếm bằng cách khác. Bắt đầu với toàn bộ tám dãy. Nhóm vi phạm điều kiện có ba dãy. Khi lấy tám trừ ba, ta còn năm dãy hợp lệ. Tuy nhiên, khi đếm phần bù phải lưu ý một dãy có thể vi phạm ở nhiều vị trí; ở đây danh sách đã loại trùng một cách cẩn thận.

**Trên màn hình:** Tổng số dãy: 8. | Số dãy có NN: 3. | Số dãy hợp lệ: 8 − 3 = 5.
**Ghi nhớ:** Phần bù giúp đếm ngắn gọn.

### Nhịp 30 · 08:13 · XÁC SUẤT KHI CÂN ĐỐI

Nếu đồng xu cân đối và ba lần tung độc lập, mỗi dãy có xác suất bằng nhau. Lúc ấy xác suất không có hai lần ngửa liên tiếp là năm phần tám. Nếu chỉ có yêu cầu đếm số dãy, đáp số của bài toán vẫn là năm, không cần giả thiết đồng xu cân đối.

**Trên màn hình:** Biến cố B có năm phần tử. | Không gian mẫu có tám phần tử. | Nếu đồng khả năng: P(B)=5/8.
**Ghi nhớ:** Không đánh đồng đếm và xác suất.


## 06  ĐẾM ĐỦ VÀ KHÔNG TRÙNG

### Nhịp 31 · 08:30 · VÌ SAO KHÔNG BỎ SÓT?

Một sơ đồ cây chỉ đáng tin khi nó liệt kê hết các trường hợp. Tại mỗi nút chưa kết thúc, chúng ta đều mở đủ hai khả năng N và S. Vì mọi dãy ba lần tung là một chuỗi gồm ba lựa chọn như thế, nhất định nó xuất hiện tại một lá của cây.

**Trên màn hình:** Mỗi lần tung đều có hai nhánh. | Cây xét đủ N và S ở mỗi tầng. | Mọi dãy có một đường đi.
**Ghi nhớ:** Mọi kết quả có thể đều xuất hiện.

### Nhịp 32 · 08:47 · VÌ SAO KHÔNG ĐẾM TRÙNG?

Giả sử hai đường đi khác nhau. Sẽ tồn tại một tầng đầu tiên mà chúng tách sang hai nhánh N và S. Từ đó hai dãy cuối cùng phải khác nhau tại vị trí ấy. Vì thế hai lá khác nhau không thể đại diện cho cùng một kết quả. Ta tránh được lỗi đếm trùng.

**Trên màn hình:** Mỗi lá ghi đủ ba ký hiệu. | Hai dãy khác nhau có vị trí khác. | Đường đi duy nhất cho mỗi dãy.
**Ghi nhớ:** Không có hai lá cùng kết quả.

### Nhịp 33 · 09:04 · NGUYÊN TẮC TƯƠNG ỨNG

Đây là chứng minh bằng tương ứng một-một. Mỗi đường đi trọn vẹn cho một dãy, và từ mỗi dãy ta khôi phục đúng đường đi ấy. Không cần một công thức phức tạp. Chỉ cần chứng minh đầy đủ và duy nhất, phép đếm trên cây đã chặt chẽ về mặt toán học.

**Trên màn hình:** Đường đi → dãy kết quả. | Dãy kết quả → đường đi. | Tương ứng hai chiều, một-một.
**Ghi nhớ:** Đếm lá chính là đếm kết quả.

### Nhịp 34 · 09:21 · CÂY CÓ RÀNG BUỘC

Khi điều kiện của bài toán cấm hai lần ngửa liên tiếp, một nhánh bắt đầu bằng NN chắc chắn không thể được chấp nhận. Ta có thể cắt nhánh này ngay tại tầng thứ hai. Cách cắt sớm giúp sơ đồ gọn hơn, nhưng phải chứng minh rằng mọi phần mở rộng của nhánh ấy đều sai.

**Trên màn hình:** Một nhánh vi phạm phải dừng lại. | Không tạo thêm lá không hợp lệ. | Các nhánh còn lại vẫn tiếp tục.
**Ghi nhớ:** Cắt nhánh đúng lúc tiết kiệm phép đếm.

### Nhịp 35 · 09:38 · KHI NÀO KHÔNG ĐƯỢC CẮT?

Hãy xem tiền tố NS. Nó có một chữ N nhưng chưa có cặp NN. Nếu vội cắt chỉ vì thấy chữ N, ta sẽ bỏ sót NSN và NSS. Vì vậy điều kiện cắt nhánh phải dựa trên vi phạm chắc chắn, chứ không dựa trên cảm giác một nhánh có vẻ không thuận lợi.

**Trên màn hình:** Một tiền tố chưa đủ kết luận sai. | Ví dụ NS vẫn có thể tạo NSN. | Không loại nhầm kết quả tương lai.
**Ghi nhớ:** Chỉ cắt khi đã chắc chắn vi phạm.

### Nhịp 36 · 09:55 · TỔNG KẾT TƯ DUY CÂY

Chốt lại ba câu hỏi quan trọng. Cây đã mở đủ tất cả lựa chọn ở mỗi bước chưa? Một kết quả có tương ứng đúng một lá hay không? Và nếu có điều kiện cấm, ta đã loại chính xác các nhánh sai chưa? Trả lời được ba điều ấy, em có thể tin vào phép đếm.

**Trên màn hình:** Đủ nhánh ở mỗi bước. | Mỗi lá là một kết quả duy nhất. | Điều kiện được kiểm tra chính xác.
**Ghi nhớ:** Ba tiêu chuẩn để đếm tin cậy.


## 07  MỞ RỘNG BỐN LẦN GIEO

### Nhịp 37 · 10:12 · MỞ RỘNG THÀNH BỐN LẦN

Ta thử kéo dài thí nghiệm thành bốn lần tung. Nếu không ràng buộc, mỗi dãy ba ký hiệu có thể nối thêm N hoặc S, nên số dãy tăng gấp đôi thành mười sáu. Đây là bước mở rộng hoàn toàn tương tự quy tắc nhân ở video trước.

**Trên màn hình:** Tung đồng xu bốn lần. | Mỗi vị trí có N hoặc S. | Không điều kiện: 2⁴ = 16 dãy.
**Ghi nhớ:** Thêm một tầng thì số lá gấp đôi.

### Nhịp 38 · 10:29 · GIỮ ĐIỀU KIỆN KHÔNG NN

Bây giờ tiếp tục yêu cầu không có hai lần ngửa liên tiếp. Với bốn vị trí, danh sách mười sáu dãy rất dễ kiểm tra nhầm. Ta có thể lọc từng kết quả, nhưng một cách chặt chẽ hơn là chia theo ký hiệu cuối cùng, tạo ra hai nhóm không giao nhau.

**Trên màn hình:** Bốn ký hiệu liên tiếp. | Không cho phép cặp NN ở bất cứ đâu. | Đếm trực tiếp bằng tám dãy hợp lệ.
**Ghi nhớ:** Cần phân loại thông minh hơn.

### Nhịp 39 · 10:46 · NHÓM KẾT THÚC BẰNG S

Nhóm đầu tiên gồm các dãy bốn ký hiệu kết thúc bằng S. Để có một dãy như vậy, chỉ cần lấy một dãy ba ký hiệu hợp lệ rồi nối thêm S. Chữ S không tạo cặp NN mới, nên cả năm dãy ba ký hiệu hợp lệ đều được phép sử dụng.

**Trên màn hình:** Thêm S sau mọi dãy dài ba hợp lệ. | Dãy dài ba hợp lệ có năm cách. | Nhóm kết thúc S có năm dãy.
**Ghi nhớ:** Đuôi S không tạo cặp NN mới.

### Nhịp 40 · 11:03 · NHÓM KẾT THÚC BẰNG NS

Nhóm thứ hai gồm các dãy kết thúc bằng N. Để không có NN, ký hiệu ngay trước N buộc phải là S. Như vậy hai ký hiệu cuối phải là S N. Hai vị trí đầu được chọn thành một dãy dài hai không có NN, có ba khả năng: NS, SN hoặc SS.

**Trên màn hình:** Nếu cuối là N thì trước đó phải S. | Hai vị trí cuối là SN. | Hai vị trí đầu có ba cách hợp lệ.
**Ghi nhớ:** Nhóm kết thúc SN có ba dãy.

### Nhịp 41 · 11:20 · CỘNG HAI NHÓM KHÔNG TRÙNG

Hai nhóm này không trùng nhau, vì một nhóm kết thúc bằng S còn nhóm kia kết thúc bằng N. Đồng thời chúng bao phủ mọi dãy hợp lệ, bởi một dãy phải kết thúc bằng S hoặc N. Theo quy tắc cộng, năm cộng ba bằng tám kết quả.

**Trên màn hình:** Nhóm cuối S: 5 dãy. | Nhóm cuối SN: 3 dãy. | Tổng số hợp lệ: 5 + 3 = 8.
**Ghi nhớ:** Bốn lần tung có tám dãy hợp lệ.

### Nhịp 42 · 11:37 · DẤU HIỆU CỦA FIBONACCI

Lập luận chia theo ký hiệu cuối áp dụng cho mọi độ dài n từ hai trở lên. Nhóm cuối S tương ứng dãy dài n trừ một; nhóm cuối S N tương ứng dãy dài n trừ hai. Vì thế xuất hiện hệ thức truy hồi Fibonacci. Đây là một cánh cửa dẫn đến các bài tổ hợp khó hơn.

**Trên màn hình:** Gọi fₙ là số dãy độ dài n hợp lệ. | f₀=1, f₁=2, f₂=3. | fₙ=fₙ₋₁+fₙ₋₂.
**Ghi nhớ:** Sơ đồ cây gợi mở hệ thức truy hồi.


## 08  LUYỆN TẬP VÀ TỔNG KẾT

### Nhịp 43 · 11:54 · LUYỆN TẬP 1: ĐÚNG MỘT N

Bài kiểm tra thứ nhất: tung đồng xu ba lần, chỉ có đúng một lần ngửa. Hãy tự tìm các lá thỏa điều kiện trước khi xem đáp án. Em nên hỏi chữ N đứng ở vị trí nào, và hai vị trí còn lại phải mang ký hiệu gì.

**Trên màn hình:** Tung ba lần, đúng một lần ngửa. | Tìm tất cả dãy thỏa mãn. | Hãy tự dừng và thử liệt kê.
**Ghi nhớ:** Đếm bằng lá trên cây.

### Nhịp 44 · 12:11 · GIẢI BÀI ĐÚNG MỘT N

Muốn chỉ có đúng một lần ngửa, chữ N có thể nằm ở vị trí đầu, giữa hoặc cuối. Tương ứng ta được NSS, SNS và SSN. Cả ba dãy có đúng một chữ N, và không còn vị trí nào khác để đặt. Vậy có ba kết quả thuận lợi.

**Trên màn hình:** Các dãy là NSS, SNS, SSN. | Có ba vị trí đặt chữ N. | Số kết quả thuận lợi là ba.
**Ghi nhớ:** Ba kết quả, không bỏ sót.

### Nhịp 45 · 12:28 · LUYỆN TẬP 2: LẦN ĐẦU SẤP

Bài tiếp theo yêu cầu lần đầu tiên phải sấp. Trên sơ đồ cây, ta chỉ cần giữ lại nhánh bắt đầu bằng S, vì mọi dãy bắt đầu bằng N đều vi phạm. Trong nhánh S, hai lần tung tiếp theo vẫn tự do chọn N hoặc S.

**Trên màn hình:** Tung ba lần. | Điều kiện lần thứ nhất là S. | Hai lần sau tùy ý N hoặc S.
**Ghi nhớ:** Còn bao nhiêu lá trên cây?

### Nhịp 46 · 12:45 · GIẢI BÀI LẦN ĐẦU SẤP

Từ nhánh S ở tầng một, hai vị trí còn lại mỗi vị trí có hai lựa chọn. Vì vậy ta có bốn kết quả: SNN, SNS, SSN và SSS. Có thể đếm bốn lá của nhánh S hoặc lấy hai nhân hai. Hai cách cho cùng một đáp số.

**Trên màn hình:** Có SNN, SNS, SSN, SSS. | Sau S có 2 × 2 khả năng. | Tổng cộng bốn kết quả.
**Ghi nhớ:** Đếm theo nhánh và theo nhân đều đúng.

### Nhịp 47 · 13:02 · LUYỆN TẬP 3: NHÁNH KHÔNG ĐỀU

Bài cuối liên hệ lại quy tắc nhân. Có ba lựa chọn món chính. Với món thứ nhất, có hai thức uống phù hợp; món thứ hai chỉ có một; món thứ ba có ba. Hãy vẽ ba nhánh và đếm số lá của từng nhánh, thay vì lấy ba nhân một con số tùy ý.

**Trên màn hình:** Chọn một trong ba món chính. | Số thức uống phù hợp: 2, 1, 3. | Có bao nhiêu suất ăn hợp lệ?
**Ghi nhớ:** Đừng nhân 3 với 2 máy móc.

### Nhịp 48 · 13:19 · CHỐT BÀI VÀ CHUYỂN TẬP 04

Ba nhánh ứng với ba món chính có lần lượt hai, một và ba kết quả. Vì ba nhóm không trùng nhau, tổng số suất ăn là sáu. Hôm nay chúng ta đã thấy sơ đồ cây là một phương pháp chứng minh phép đếm. Tập tiếp theo sẽ tìm hiểu khi nào việc đổi thứ tự tạo kết quả mới.

**Trên màn hình:** Số suất ăn là 2 + 1 + 3 = 6. | Cây giúp kiểm tra đủ và không trùng. | Tập sau: thứ tự có quan trọng?
**Ghi nhớ:** Học tư duy đếm trước công thức.
