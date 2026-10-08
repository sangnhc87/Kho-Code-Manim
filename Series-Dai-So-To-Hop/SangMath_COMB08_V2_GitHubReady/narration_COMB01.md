# COMB01 · QUY TẮC CỘNG · BẢN THUYẾT MINH ĐỒNG BỘ

Giọng mặc định: vi-VN-NamMinhNeural. Lời đọc được chia theo 42 nhịp.
Mỗi nhịp bắt đầu đồng thời với hoạt hình; thời gian dựa trên clip MP3 thật.

**Thời gian video dự kiến:** 12.9 phút; đọc 2145 từ tiếng Việt.


## 01  ĐẶT VẤN ĐỀ

### Nhịp 01 · 00:00 · MỘT CHUYẾN ĐI

Hãy quan sát hai địa điểm A và B trên màn hình. Giữa hai địa điểm này có hai tuyến xe buýt và ba tuyến tàu khác nhau. Một người chỉ cần chọn đúng một tuyến để di chuyển từ A tới B.

*Dòng chữ chính: Dự đoán: có bao nhiêu cách?*

### Nhịp 02 · 00:18 · NHẬN DIỆN LỰA CHỌN

Trước hết, ta chỉ xét phương tiện xe buýt. Có tuyến xe buýt thứ nhất và tuyến xe buýt thứ hai. Nếu chọn tuyến thứ nhất thì đó là một kết quả. Nếu chọn tuyến thứ hai thì đó là kết quả khác. Do vậy, trong nhóm xe buýt, chúng ta có đúng hai khả năng.

*Dòng chữ chính: Hai lựa chọn đầu tiên: Xe 1, Xe 2.*

### Nhịp 03 · 00:36 · CÒN MỘT NHÓM NỮA

Bây giờ ta chuyển sang nhóm tàu. Trên hình lần lượt xuất hiện tàu thứ nhất, tàu thứ hai và tàu thứ ba. Ba tuyến này tạo ra ba cách lựa chọn. Cần chú ý rằng, khi hành khách đã chọn một tuyến tàu thì không đồng thời chọn thêm tuyến xe buýt.

*Dòng chữ chính: Ba lựa chọn còn lại không phải xe buýt.*

### Nhịp 04 · 00:54 · CHỈ CHỌN MỘT TUYẾN

Có bạn nghĩ rằng phải lấy hai nhân ba, vì bài toán xuất hiện hai nhóm. Nhưng như thế sẽ đếm các cặp gồm một xe buýt và một tàu. Đề bài không yêu cầu đi cả hai phương tiện. Mỗi lần chọn chỉ tạo ra một trong năm tuyến riêng biệt.

*Dòng chữ chính: Từ “hoặc” gợi ý phép cộng.*

### Nhịp 05 · 01:12 · THỬ ĐẾM TRỰC TIẾP

Để chắc chắn, ta có thể liệt kê trực tiếp các kết quả: xe một, xe hai, tàu một, tàu hai và tàu ba. Không có kết quả nào xuất hiện hai lần. Cũng không còn kết quả hợp lệ nào bị bỏ sót. Tổng số cách chọn do đó là hai cộng ba, bằng năm.

*Dòng chữ chính: 2 + 3 = 5 cách chọn.*


## 02  PHÂN NHÓM

### Nhịp 06 · 01:31 · PHÂN NHÓM KẾT QUẢ

Ta sẽ biểu diễn lời giải bằng hai nhóm thẻ để nhìn rõ bản chất. Gọi X là tập gồm hai tuyến xe buýt, và Y là tập gồm ba tuyến tàu. Mỗi thẻ biểu diễn chính xác một cách thực hiện chuyến đi.

*Dòng chữ chính: X và Y là hai tập hợp kết quả.*

### Nhịp 07 · 01:49 · ĐẾM NHÓM X

Trong tập X, ta lần lượt nhìn thấy thẻ xe một và xe hai. Có hai phần tử nên có hai cách chọn xe buýt. Thứ tự kể tên các thẻ không ảnh hưởng tới số cách, bởi ta đang lựa chọn một phương án, không phải sắp xếp các phương án.

*Dòng chữ chính: Số cách của phương án X là 2.*

### Nhịp 08 · 02:07 · ĐẾM NHÓM Y

Tương tự, tập Y chứa ba thẻ tàu. Ta có ba cách chọn tàu. Bây giờ hãy quan sát đồng thời cả hai tập. Không có thẻ nào vừa nằm ở nhóm xe buýt vừa nằm ở nhóm tàu. Nói bằng ngôn ngữ tập hợp, hai nhóm không có phần tử chung.

*Dòng chữ chính: Số cách của phương án Y là 3.*

### Nhịp 09 · 02:25 · HỢP HAI NHÓM

Vì đề bài cho phép đi bằng xe buýt hoặc tàu nên tập tất cả kết quả hợp lệ chính là hợp của X và Y. Chúng ta đếm hai phần tử nhóm X, rồi tiếp tục đếm ba phần tử nhóm Y. Hai lượt đếm không đụng tới cùng một kết quả.

*Dòng chữ chính: Tổng: 2 + 3.*

### Nhịp 10 · 02:43 · KẾT LUẬN BÀI MỞ ĐẦU

Kết luận của bài mở đầu là năm cách. Ta nhắc lại lý do, chứ không chỉ nhắc lại đáp số: hành khách chọn đúng một tuyến, mọi tuyến đã được liệt kê, và không có tuyến nào bị đếm hai lần.

*Dòng chữ chính: Kết luận: 5 cách.*


## 03  KHÁI QUÁT

### Nhịp 11 · 03:01 · KHÁI QUÁT HAI PHƯƠNG ÁN

Bây giờ ta rời khỏi ví dụ xe buýt và tàu để phát biểu quy tắc ở dạng tổng quát. Giả sử một công việc có thể thực hiện theo phương án A hoặc theo phương án B. Phương án A có m kết quả khác nhau, còn phương án B có n kết quả khác nhau.

*Dòng chữ chính: Hỏi có bao nhiêu kết quả tất cả?*

### Nhịp 12 · 03:20 · ĐIỀU KIỆN QUAN TRỌNG

Nếu một kết quả không thể đồng thời được tính trong cả nhóm A và nhóm B, hai tập hợp kết quả là rời nhau. Khi đó, việc đếm hết A rồi đếm hết B không làm trùng bất kỳ kết quả nào. Ta có thể dùng công thức đơn giản m cộng n.

*Dòng chữ chính: Không giao nhau → không đếm trùng.*

### Nhịp 13 · 03:38 · QUY TẮC CỘNG

Ta có quy tắc cộng: nếu một công việc có thể thực hiện theo một trong hai phương án không trùng nhau, phương án thứ nhất có m cách và phương án thứ hai có n cách, thì có m cộng n cách thực hiện công việc.

*Dòng chữ chính: Tổng số cách là m + n.*

### Nhịp 14 · 03:56 · MỞ RỘNG NHIỀU NHÓM

Quy tắc cộng không chỉ dành cho đúng hai phương án. Nếu có ba phương án không trùng nhau, ta cộng số cách của cả ba. Nếu có nhiều nhóm hơn cũng làm như vậy. Tuy nhiên, không được tự động cộng mọi con số chỉ vì bài toán có nhiều trường hợp.

*Dòng chữ chính: m₁ + m₂ + … + mᵣ.*

### Nhịp 15 · 04:14 · KIỂM TRA TRƯỚC KHI CỘNG

Tôi gợi ý ba câu hỏi để kiểm tra mọi bài đếm bằng quy tắc cộng. Thứ nhất, các nhóm đã bao phủ tất cả kết quả hợp lệ chưa? Thứ hai, có kết quả nào nằm ở hai nhóm hay không? Thứ ba, một kết quả đã được tính đúng một lần chưa?

*Dòng chữ chính: Hai câu hỏi: đủ và không trùng.*


## 04  VẬN DỤNG 1

### Nhịp 16 · 04:32 · VÍ DỤ 2 · CHỌN SÁCH

Ta chuyển sang một ví dụ gần gũi hơn. Trên giá có bốn cuốn sách Toán khác nhau và ba cuốn sách Vật lí khác nhau. Một học sinh chỉ lấy đúng một cuốn để đọc. Em hãy nhìn bảy cuốn sách trên màn hình và dự đoán số cách chọn.

*Dòng chữ chính: Dự đoán số cách chọn sách.*

### Nhịp 17 · 04:51 · PHƯƠNG ÁN THỨ NHẤT

Trước tiên, ta xét phương án chọn sách Toán. Bốn cuốn lần lượt được ký hiệu T một, T hai, T ba và T bốn. Vì chúng là bốn cuốn khác nhau, mỗi cuốn tạo ra một cách chọn. Vậy phương án lấy sách Toán có bốn cách.

*Dòng chữ chính: Nhóm Toán: 4 cách.*

### Nhịp 18 · 05:09 · PHƯƠNG ÁN THỨ HAI

Tiếp theo, học sinh cũng có thể chọn một cuốn Vật lí. Có ba cuốn L một, L hai và L ba, tương ứng ba cách. Không một cuốn nào đồng thời được xếp vào loại Toán và loại Vật lí trong bài toán này. Vì thế, hai nhóm sách là hai nhóm lựa chọn rời nhau.

*Dòng chữ chính: Nhóm Vật lí: 3 cách.*

### Nhịp 19 · 05:27 · TỔNG HỢP HAI NHÓM

Vì chỉ lấy đúng một cuốn, ta không ghép một cuốn Toán với một cuốn Vật lí thành một cặp. Nếu làm như vậy, ta đang giải một bài toán khác. Ở đây, tập kết quả là tất cả bảy cuốn sách được trưng bày.

*Dòng chữ chính: 4 + 3 = 7 cách.*

### Nhịp 20 · 05:45 · THAY ĐỔI YÊU CẦU

Hãy kiểm tra sự hiểu bài bằng một thay đổi rất nhỏ trong đề: bây giờ chọn một cuốn Toán và một cuốn Vật lí. Kết quả không còn là một cuốn sách nữa mà là một cặp gồm hai cuốn. Ta không được dùng đáp số bảy của bài vừa rồi.

*Dòng chữ chính: Nhận ra sự khác biệt “hoặc” và “và”.*


## 05  ĐẾM TRÙNG

### Nhịp 21 · 06:03 · THỬ THÁCH · CÓ TRÙNG KHÔNG?

Bây giờ là thử thách quan trọng nhất của tập này. Xét các số nguyên từ một đến mười hai. Ta cần đếm những số chia hết cho hai hoặc chia hết cho ba. Từ hoặc khiến ta nghĩ tới quy tắc cộng, nhưng liệu hai nhóm có rời nhau không?

*Dòng chữ chính: Cần kiểm tra xem hai nhóm có giao nhau.*

### Nhịp 22 · 06:22 · CÁC SỐ CHIA HẾT CHO 2

Các số chia hết cho hai trong phạm vi một đến mười hai là hai, bốn, sáu, tám, mười và mười hai. Tổng cộng có sáu số. Ta tô chúng bằng màu xanh. Số sáu ở đây hoàn toàn chính xác, nhưng chỉ là số phần tử của nhóm A.

*Dòng chữ chính: Nhóm A có 6 phần tử.*

### Nhịp 23 · 06:40 · CÁC SỐ CHIA HẾT CHO 3

Nhóm thứ hai gồm các số chia hết cho ba, đó là ba, sáu, chín và mười hai. Như vậy nhóm B có bốn số. Khi đặt cạnh danh sách số chẵn, ta dễ dàng nhận thấy số sáu và số mười hai xuất hiện trong cả hai danh sách.

*Dòng chữ chính: Chú ý các số 6 và 12.*

### Nhịp 24 · 06:58 · PHÁT HIỆN PHẦN GIAO

Hãy quan sát hai ô số sáu và mười hai chuyển sang màu đỏ. Màu đỏ không có nghĩa chúng không được chọn; chúng vẫn là kết quả hợp lệ. Màu đỏ báo rằng mỗi số đã bị tính thêm một lần khi cộng hai lượng sáu và bốn.

*Dòng chữ chính: 6 + 4 đã đếm trùng 2 lần.*

### Nhịp 25 · 07:16 · SỬA PHÉP ĐẾM

Phép đếm đúng là sáu cộng bốn trừ hai, bằng tám. Nếu liệt kê trực tiếp, ta nhận được hai, ba, bốn, sáu, tám, chín, mười và mười hai, đúng tám số. Việc trừ phần giao không phải mẹo ghi nhớ tùy ý mà là cách sửa lại số lần mỗi kết quả được tính.

*Dòng chữ chính: Có 8 số thỏa mãn.*

### Nhịp 26 · 07:34 · CÔNG THỨC HAI TẬP HỢP

Qua hình ảnh hai nhóm có phần chung, ta đi tới công thức đếm phần tử của hợp hai tập hợp. Số phần tử của hợp bằng số phần tử của tập thứ nhất cộng số phần tử tập thứ hai rồi trừ số phần tử giao.

*Dòng chữ chính: |A ∪ B| = |A| + |B| − |A ∩ B|.*

### Nhịp 27 · 07:53 · ĐIỀU CẦN NHỚ

Đây là một cảnh báo quan trọng: không phải gặp chữ hoặc là lấy ngay hai con số cộng lại. Trước khi làm phép tính, ta phải xác định tập các kết quả, kiểm tra phần giao và quyết định công thức thích hợp.

*Dòng chữ chính: Đủ trường hợp — không đếm trùng.*


## 06  VẬN DỤNG 2

### Nhịp 28 · 08:11 · VÍ DỤ 3 · CÁC NHÓM RỜI NHAU

Xét các số nguyên từ một đến hai mươi. Hỏi có bao nhiêu số lẻ hoặc chia hết cho bốn? Hãy phân tích hai điều kiện: một số lẻ không chia hết cho hai, trong khi số chia hết cho bốn chắc chắn là số chẵn.

*Dòng chữ chính: Lần này có phần giao không?*

### Nhịp 29 · 08:29 · ĐẾM CÁC SỐ LẺ

Trong dãy từ một đến hai mươi có mười số lẻ, bắt đầu từ một và kết thúc ở mười chín. Trên lưới số, các ô lẻ được tô sáng. Dù nằm xen kẽ các số chẵn, chúng vẫn tạo thành một nhóm hợp lệ vì cùng thỏa điều kiện đầu tiên.

*Dòng chữ chính: Nhóm thứ nhất: 10 cách.*

### Nhịp 30 · 08:47 · ĐẾM CÁC BỘI CỦA 4

Các số chia hết cho bốn là bốn, tám, mười hai, mười sáu và hai mươi. Có tất cả năm số. Vì mọi số này đều chẵn, chúng không thể thuộc danh sách mười số lẻ vừa rồi. Như vậy, hai nhóm đã được kiểm tra là không trùng.

*Dòng chữ chính: Nhóm thứ hai: 5 cách.*

### Nhịp 31 · 09:05 · ÁP DỤNG QUY TẮC CỘNG

Kết quả là mười cộng năm bằng mười lăm số. Hãy so sánh với bài chia hết cho hai hoặc ba lúc trước. Ở ví dụ này, phép cộng trực tiếp hoàn toàn đúng vì phần giao là rỗng. Trong bài trước, phải trừ đi hai phần tử chung.

*Dòng chữ chính: 10 + 5 = 15 số.*

### Nhịp 32 · 09:24 · BÀI HỌC TỪ HAI VÍ DỤ

Qua hai bài toán số học, ta đã thấy cùng một yêu cầu kiểu hoặc có thể dẫn tới hai phép đếm khác nhau. Thay vì học thuộc một mẹo, em hãy vẽ hoặc tưởng tượng hai nhóm kết quả. Nếu hai nhóm không có phần giao, cộng trực tiếp. Nếu có phần giao, phải tránh đếm lặp.

*Dòng chữ chính: Không học công thức tách khỏi mô hình.*


## 07  PHÂN BIỆT

### Nhịp 33 · 09:42 · “HOẶC” VÀ “VÀ” KHÁC NHAU

Để tránh nhầm lẫn giữa hai quy tắc đếm đầu tiên, ta xét ba chiếc áo khác nhau và hai chiếc mũ khác nhau. Nếu chỉ chọn một món đồ, có thể chọn áo hoặc mũ. Nhưng nếu yêu cầu một bộ gồm một áo và một mũ, ta phải tạo ra các cặp.

*Dòng chữ chính: Hai bài toán — hai loại kết quả.*

### Nhịp 34 · 10:00 · TRƯỜNG HỢP “HOẶC”

Khi đề yêu cầu một áo hoặc một mũ, một kết quả chỉ là một món đồ. Các kết quả là áo một, áo hai, áo ba, mũ một và mũ hai. Tất cả có năm món riêng biệt. Vì các nhóm không trùng nhau nên số cách chọn là ba cộng hai bằng năm.

*Dòng chữ chính: 3 + 2 = 5 lựa chọn.*

### Nhịp 35 · 10:18 · TRƯỜNG HỢP “VÀ”

Ngược lại, khi đề yêu cầu một áo và một mũ, mỗi kết quả gồm hai món đồ. Áo thứ nhất ghép với hai mũ tạo hai cặp; áo thứ hai cũng vậy, và áo thứ ba cũng vậy. Tổng cộng có sáu cặp.

*Dòng chữ chính: 3 × 2 = 6 lựa chọn.*

### Nhịp 36 · 10:37 · KHÔNG ĐOÁN THEO TỪ KHÓA

Tuy chữ hoặc và chữ và gợi ý khá nhiều, ta không nên chỉ học thuộc dấu hiệu ngôn ngữ. Câu hỏi sâu hơn là: một kết quả hợp lệ cụ thể trông như thế nào? Nếu là một món đồ, ta đếm từng món. Nếu là một bộ hai món, ta đếm từng cặp.

*Dòng chữ chính: Xác định kết quả trước phép tính.*

### Nhịp 37 · 10:55 · TỔNG KẾT PHÂN BIỆT

Chúng ta đã hoàn thành sự phân biệt cơ bản giữa lựa chọn thay thế và lựa chọn phối hợp. Quy tắc cộng dùng để gộp các nhóm kết quả không trùng nhau. Quy tắc nhân sẽ xuất hiện khi kết quả được tạo qua nhiều bước kết hợp.

*Dòng chữ chính: Học bản chất, không học máy móc.*


## 08  CỦNG CỐ

### Nhịp 38 · 11:13 · TỰ KIỂM TRA · CÂU 1

Trước khi kết thúc, em hãy làm hai câu tự kiểm tra. Câu thứ nhất, có năm phần quà loại A khác nhau và hai phần quà loại B khác nhau. Chọn đúng một phần quà. Em hãy tạm dừng video, viết tập kết quả nếu cần, rồi quyết định nên dùng quy tắc nào.

*Dòng chữ chính: Hãy tạm dừng để tính số cách.*

### Nhịp 39 · 11:31 · GIẢI CÂU 1

Lời giải câu một: có năm cách chọn một phần quà A và hai cách chọn một phần quà B. Vì một phần quà không thể vừa là phần quà A vừa là phần quà B trong đề này, các nhóm rời nhau. Chọn đúng một phần quà nghĩa là gộp hai nhóm kết quả.

*Dòng chữ chính: 5 + 2 = 7 cách.*

### Nhịp 40 · 11:49 · TỰ KIỂM TRA · CÂU 2

Câu thứ hai khó hơn một chút. Từ một đến mười lăm, có bao nhiêu số chia hết cho ba hoặc chia hết cho năm? Các số chia hết cho ba có năm số, còn chia hết cho năm có ba số. Nếu cộng ngay ta được tám.

*Dòng chữ chính: Tìm xem có số nào thỏa cả hai.*

### Nhịp 41 · 12:08 · GIẢI CÂU 2

Trong các số từ một tới mười lăm, số mười lăm vừa chia hết cho ba vừa chia hết cho năm. Đó là phần giao duy nhất. Khi cộng năm với ba, số mười lăm đã bị tính hai lần. Trừ bớt một lần, chúng ta được năm cộng ba trừ một bằng bảy số.

*Dòng chữ chính: 5 + 3 − 1 = 7 số.*

### Nhịp 42 · 12:26 · KẾT THÚC · COMB01

Hãy giữ lại ba câu hỏi cốt lõi sau bài học này. Một kết quả hợp lệ là gì? Ta đã kể hết các khả năng chưa? Và có khả năng nào bị tính hai lần không? Quy tắc cộng sẽ trở nên đơn giản khi ta trả lời được ba câu hỏi đó.

*Dòng chữ chính: Hiểu đối tượng được đếm trước.*
