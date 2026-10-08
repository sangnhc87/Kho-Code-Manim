# SANG MATH · COMB15 V2 · LẬP SỐ TỰ NHIÊN THỎA ĐIỀU KIỆN

## Bản thuyết minh đồng bộ

Số nhịp: 48 · 8 chương · TTS=off
Tổng thời lượng dự kiến: 1157.2 giây.
Lời giảng bên dưới là nội dung đầy đủ được đưa vào tổng hợp giọng đọc; không cắt tùy ý.


## 01 · CHỮ SỐ ĐẦU KHÁC 0

### Nhịp 01 · 00:00 · MỞ ĐẦU: LẬP SỐ BA CHỮ SỐ

Ta có sáu thẻ chữ số từ không đến năm, và ba ô hàng trăm, hàng chục, hàng đơn vị. Bài yêu cầu lập các số tự nhiên có ba chữ số khác nhau. Trước khi nhân số lựa chọn, hãy kiểm tra ô bên trái: một số có ba chữ số không thể bắt đầu bằng không. Chữ số không vẫn được phép xuất hiện ở hai vị trí phía sau.

**Trên màn hình:** Dùng các chữ số 0, 1, 2, 3, 4, 5. | Lập số có ba chữ số khác nhau. | Cần tìm tổng số kết quả.
**Ghi nhớ:** CHỮ SỐ ĐẦU KHÔNG ĐƯỢC LÀ 0.

### Nhịp 02 · 00:24 · ĐIỀN Ô HÀNG TRĂM

Ta điền ô hàng trăm trước bởi đây là ô có điều kiện đặc biệt. Sáu chữ số ban đầu có năm chữ số khác không, do đó ô đầu chỉ có năm cách lựa chọn. Khi chọn một chữ số, tấm thẻ tương ứng được chuyển vào ô và không quay lại kho, vì đề yêu cầu ba chữ số đôi một khác nhau.

**Trên màn hình:** Không được đặt 0 ở đầu. | Có năm lựa chọn: 1 đến 5. | Chọn một chữ số rồi khóa thẻ ấy.
**Ghi nhớ:** BƯỚC ĐẦU CÓ 5 CÁCH, KHÔNG PHẢI 6.

### Nhịp 03 · 00:48 · ĐIỀN HÀNG CHỤC

Sau khi điền hàng trăm, còn năm chữ số chưa dùng. Cả năm đều có thể đứng ở hàng chục, kể cả chữ số không. Sự khác biệt này rất quan trọng: điều kiện cấm số không ở đầu không có nghĩa là cấm số không ở mọi vị trí. Hình động giữ thẻ hàng trăm cố định và cho năm thẻ còn lại thử vào ô giữa.

**Trên màn hình:** Một thẻ đã được sử dụng. | Trong sáu thẻ còn đúng năm thẻ. | Chữ số 0 vẫn có thể được chọn.
**Ghi nhớ:** HÀNG CHỤC CÓ 5 CÁCH.

### Nhịp 04 · 01:12 · ĐIỀN HÀNG ĐƠN VỊ

Đến ô hàng đơn vị, ta đã sử dụng hai thẻ khác nhau, nên chỉ còn bốn thẻ chưa dùng. Không còn điều kiện về chữ số đầu ở đây và cũng chưa có ràng buộc chẵn lẻ, bởi thế mọi thẻ còn lại đều hợp lệ. Cây lựa chọn trên hình có năm nhánh ở bước một, năm nhánh ở bước hai, rồi bốn ở bước ba.

**Trên màn hình:** Đã sử dụng hai chữ số phân biệt. | Bây giờ còn bốn thẻ chưa dùng. | Không cần điều kiện bổ sung.
**Ghi nhớ:** Ô CUỐI CÓ 4 CÁCH.

### Nhịp 05 · 01:36 · KẾT LUẬN: 100 SỐ

Theo quy tắc nhân, số kết quả bằng năm nhân năm nhân bốn, tức một trăm. Mỗi đường đi qua ba ô cho một số duy nhất, và mọi số hợp lệ tương ứng một đường đi nên không bỏ sót hay đếm trùng. Chương trình Python cũng có thể liệt kê tất cả một trăm số để xác nhận lập luận của chúng ta.

**Trên màn hình:** Hàng trăm: 5 cách. | Hàng chục: 5 cách. | Hàng đơn vị: 4 cách.
**Ghi nhớ:** TỔNG CỘNG ĐÚNG 100 SỐ.

### Nhịp 06 · 02:00 · NẾU ĐƯỢC PHÉP LẶP

Ta thay đổi đúng một giả thiết: các chữ số được phép lặp. Ô hàng trăm vẫn có năm lựa chọn, nhưng thẻ đã dùng không bị loại khỏi kho nên hàng chục và hàng đơn vị đều có sáu lựa chọn. Kết quả lúc này là một trăm tám mươi. So sánh hai mô hình giúp ta thấy vì sao phải đọc kỹ cụm từ khác nhau hoặc có thể trùng nhau.

**Trên màn hình:** Hàng trăm vẫn chỉ có 5 cách. | Hai vị trí sau đều có 6 cách. | Có 180 số, thay vì 100.
**Ghi nhớ:** KHÁC NHAU VÀ ĐƯỢC LẶP LÀ HAI BÀI KHÁC.


## 02 · SỐ CHẴN VÀ SỐ LẺ

### Nhịp 07 · 02:24 · CHẴN HAY LẺ: XÉT Ô NÀO?

Lần này ta có năm chữ số từ không đến bốn. Muốn lập số chẵn, chữ số hàng đơn vị phải là không, hai hoặc bốn. Vì hàng trăm không thể là không nên các lựa chọn tại hai đầu có ảnh hưởng lẫn nhau. Nếu cứ lấy bốn cách điền đầu, ba cách điền cuối, ta có nguy cơ bỏ qua sự khác nhau giữa tận cùng không và tận cùng khác không.

**Trên màn hình:** Lấy 0, 1, 2, 3, 4. | Lập số có ba chữ số khác nhau. | Hỏi có bao nhiêu số chẵn?
**Ghi nhớ:** ĐIỀU KIỆN CHẴN NẰM Ở HÀNG ĐƠN VỊ.

### Nhịp 08 · 02:48 · TRƯỜNG HỢP CUỐI LÀ 0

Ta bắt đầu từ chữ số cuối bằng không. Khi đó ô hàng trăm được chọn thoải mái trong bốn chữ số một, hai, ba, bốn. Ô hàng chục còn ba thẻ chưa dùng. Số không đã cố định ở cuối, vì thế không còn trường hợp đầu bằng không phải loại. Bằng quy tắc nhân, ta được mười hai số trong trường hợp này.

**Trên màn hình:** Cố định số 0 ở hàng đơn vị. | Hàng trăm: 4 cách từ 1 đến 4. | Hàng chục: còn 3 cách.
**Ghi nhớ:** CÓ 12 SỐ KẾT THÚC BẰNG 0.

### Nhịp 09 · 03:12 · TRƯỜNG HỢP CUỐI LÀ 2 HOẶC 4

Nếu chữ số cuối là hai hoặc bốn, ta có hai cách chọn chữ số này. Trong các chữ số còn lại, chữ số không vẫn không được đứng đầu, nên hàng trăm chỉ có ba cách. Sau khi chọn hàng trăm, ô hàng chục còn ba lựa chọn. Như vậy hai nhân ba nhân ba bằng mười tám số, khác với mười hai ở trường hợp tận cùng bằng không.

**Trên màn hình:** Có 2 cách chọn chữ số cuối. | Hàng trăm: 3 chữ số khác 0 còn lại. | Hàng chục: có 3 chữ số còn lại.
**Ghi nhớ:** CÓ 18 SỐ TRONG TRƯỜNG HỢP NÀY.

### Nhịp 10 · 03:36 · CỘNG HAI TRƯỜNG HỢP

Một số không thể vừa tận cùng bằng không lại vừa tận cùng bằng hai hoặc bốn, nên hai trường hợp rời nhau. Ta cộng mười hai và mười tám, được ba mươi số chẵn. Trên hình, các cột kết quả chẵn đều được tô xanh, còn hai kiểu tận cùng được giữ màu khác nhau để học sinh nhận ra phép cộng trường hợp trước khi rút gọn.

**Trên màn hình:** Tận cùng 0: 12 số. | Tận cùng 2 hoặc 4: 18 số. | Hai trường hợp không giao nhau.
**Ghi nhớ:** CÓ ĐÚNG 30 SỐ CHẴN.

### Nhịp 11 · 04:00 · KIỂM TRA CÁC SỐ LẺ

Tổng số có ba chữ số khác nhau từ tập không đến bốn bằng bốn nhân bốn nhân ba, tức bốn mươi tám. Mỗi số nguyên hoặc chẵn hoặc lẻ, không thể đồng thời là cả hai. Bởi vậy số lẻ bằng bốn mươi tám trừ ba mươi, được mười tám. Chúng ta vừa kiểm tra đáp số bằng một cách phân chia độc lập.

**Trên màn hình:** Số có ba chữ số khác nhau: 48. | Số chẵn: 30. | Số lẻ còn 18.
**Ghi nhớ:** CHẴN VÀ LẺ PHÂN HOẠCH MỌI SỐ.

### Nhịp 12 · 04:24 · LỖI THƯỜNG GẶP

Một phép nhân như ba lựa chọn cuối nhân bốn lựa chọn đầu nhân ba lựa chọn giữa có vẻ hợp lý, nhưng sai vì khi số cuối bằng không thì hàng trăm có bốn cách, còn khi cuối là hai hoặc bốn thì hàng trăm chỉ có ba cách. Ta cần tách nhánh hoặc chọn thứ tự điền ô phù hợp. Đây là kỹ năng quan trọng cho mọi bài lập số có chữ số không.

**Trên màn hình:** Không chọn hàng trăm là 0. | Không coi ba số chẵn cuối là như nhau. | Đếm các nhánh theo điều kiện thật.
**Ghi nhớ:** ĐẦU VÀ CUỐI CÓ THỂ PHỤ THUỘC NHAU.


## 03 · CHIA HẾT CHO 5

### Nhịp 13 · 04:48 · QUY TẮC CHIA HẾT CHO 5

Trong các số tự nhiên, điều kiện chia hết cho năm chỉ phụ thuộc chữ số hàng đơn vị: số phải kết thúc bằng không hoặc năm. Ta lập số có bốn chữ số đôi một khác nhau từ bảy chữ số không đến sáu. Hình động làm sáng hai thẻ tận cùng không và năm rồi khóa vị trí cuối; ba ô bên trái sẽ được đếm riêng theo từng trường hợp.

**Trên màn hình:** Dùng các chữ số 0 đến 6. | Lập số có bốn chữ số khác nhau. | Yêu cầu chia hết cho 5.
**Ghi nhớ:** CHỮ SỐ CUỐI CHỈ CÓ THỂ LÀ 0 HOẶC 5.

### Nhịp 14 · 05:12 · TẬN CÙNG LÀ 0

Nếu chữ số cuối bằng không thì sáu chữ số từ một đến sáu đều có thể đứng ở hàng nghìn. Sau khi chọn hàng nghìn, còn năm thẻ cho hàng trăm, rồi bốn thẻ cho hàng chục. Chữ số không không còn trong kho, vì thế không phải loại thêm trường hợp đầu bằng không. Kết quả sáu nhân năm nhân bốn bằng một trăm hai mươi.

**Trên màn hình:** Cố định 0 ở hàng đơn vị. | Hàng nghìn: 6 cách từ 1 đến 6. | Hai ô giữa: 5 rồi 4 cách.
**Ghi nhớ:** TRƯỜNG HỢP NÀY CÓ 120 SỐ.

### Nhịp 15 · 05:36 · TẬN CÙNG LÀ 5

Nếu ô cuối là năm, các thẻ còn lại gồm không, một, hai, ba, bốn, sáu. Hàng nghìn không được là không, nên có năm lựa chọn. Sau khi điền hàng nghìn, còn năm thẻ khác cho ô tiếp theo, rồi bốn thẻ cho ô thứ ba. Ta được năm nhân năm nhân bốn bằng một trăm số. Hai trường hợp có số cách khác nhau vì sự hiện diện của chữ số không.

**Trên màn hình:** Khóa chữ số 5 ở ô cuối. | Hàng nghìn: 5 cách, không dùng 0 hoặc 5. | Hai ô giữa: 5 rồi 4 cách.
**Ghi nhớ:** TRƯỜNG HỢP NÀY CÓ 100 SỐ.

### Nhịp 16 · 06:00 · CỘNG ĐÚNG HAI NHÁNH

Hai trường hợp kết thúc bằng không và kết thúc bằng năm là rời nhau, vì mỗi số chỉ có một chữ số hàng đơn vị. Do đó số kết quả chia hết cho năm bằng một trăm hai mươi cộng một trăm, được hai trăm hai mươi. Trên hình, hai nhánh hội tụ vào cùng bộ đếm mà vẫn giữ hai nhãn riêng để học sinh không nghĩ rằng số lựa chọn ở mọi nhánh phải bằng nhau.

**Trên màn hình:** Tận cùng 0: 120 số. | Tận cùng 5: 100 số. | Không số nào thuộc đồng thời hai nhánh.
**Ghi nhớ:** TỔNG CỘNG 220 SỐ.

### Nhịp 17 · 06:24 · ĐỐI CHIẾU TOÀN BỘ

Nếu chỉ yêu cầu số có bốn chữ số khác nhau từ không đến sáu, hàng nghìn có sáu cách và ba ô sau có lần lượt sáu, năm, bốn cách, tổng cộng bảy trăm hai mươi. Trong đó có hai trăm hai mươi số chia hết cho năm; phần còn lại là năm trăm số. Đây là phép kiểm tra quan hệ tổng bằng phần thỏa cộng phần không thỏa.

**Trên màn hình:** Không điều kiện chia hết: 720 số. | Chia hết cho 5: 220 số. | Không chia hết cho 5: 500 số.
**Ghi nhớ:** PHẦN BÙ CŨNG LÀ MỘT CÁCH KIỂM.

### Nhịp 18 · 06:48 · NGUYÊN TẮC ĐIỀN TỪ PHẢI

Với những bài yêu cầu chia hết cho hai hoặc cho năm, chọn chữ số cuối trước giúp điều kiện được kiểm soát ngay từ đầu. Nhưng vì đã sử dụng một chữ số ở cuối, số lựa chọn của hàng đầu vẫn phải xét lại, đặc biệt khi bộ chữ số chứa không. Quy tắc đúng là lựa chọn thứ tự đếm linh hoạt, đồng thời luôn tính chính xác số chữ số còn lại ở mỗi nhánh.

**Trên màn hình:** Chẵn: xem chữ số cuối. | Chia hết cho 5: xem chữ số cuối. | Không bắt buộc đếm từ trái qua phải.
**Ghi nhớ:** HÃY XỬ LÝ VỊ TRÍ RÀNG BUỘC MẠNH TRƯỚC.


## 04 · CHIA HẾT CHO 3

### Nhịp 19 · 07:12 · CHIA HẾT CHO 3 KHÁC GÌ?

Điều kiện chia hết cho ba khác hẳn yêu cầu chẵn hoặc chia hết cho năm. Một số chia hết cho ba khi tổng tất cả chữ số chia hết cho ba; ta không thể chỉ nhìn ô tận cùng. Với sáu chữ số không đến năm, bài toán trở thành chọn ba chữ số phân biệt sao cho tổng của chúng chia hết cho ba, sau đó xếp vào ba vị trí mà hàng trăm không bằng không.

**Trên màn hình:** Dùng 0, 1, 2, 3, 4, 5. | Lập số ba chữ số khác nhau. | Hỏi chia hết cho 3?
**Ghi nhớ:** PHẢI XÉT TỔNG CÁC CHỮ SỐ.

### Nhịp 20 · 07:36 · CHIA CÁC CHỮ SỐ THEO DƯ

Hãy tách sáu thẻ thành ba nhóm theo phần dư khi chia cho ba. Chữ số không và ba thuộc nhóm dư không; một và bốn thuộc nhóm dư một; hai và năm thuộc nhóm dư hai. Vì mỗi nhóm có hai thẻ, không thể chọn ba chữ số khác nhau cùng một nhóm. Muốn tổng chia hết cho ba, ta phải lấy mỗi nhóm một chữ số.

**Trên màn hình:** Nhóm dư 0: 0 và 3. | Nhóm dư 1: 1 và 4. | Nhóm dư 2: 2 và 5.
**Ghi nhớ:** THỬ CÁC KIỂU TỔNG CÓ DƯ 0.

### Nhịp 21 · 08:00 · CHỌN MỘT Ở MỖI NHÓM

Để tạo tổng có dư bằng không, ta chọn một chữ số dư không, một chữ số dư một và một chữ số dư hai. Mỗi nhóm có đúng hai khả năng, nên có hai nhân hai nhân hai bằng tám bộ chữ số. Đây mới là số bộ không xét thứ tự, chưa phải số tự nhiên. Ta sẽ tách các bộ có chứa không khỏi các bộ không chứa không trước khi xếp thứ tự.

**Trên màn hình:** Mỗi nhóm dư có 2 chữ số. | Số bộ ba chưa xét thứ tự: 2³ = 8. | Mỗi bộ có tổng chia hết cho 3.
**Ghi nhớ:** CÓ TÁM BỘ CHỮ SỐ KHÁC NHAU.

### Nhịp 22 · 08:24 · BỘ CÓ CHỨA 0

Trong tám bộ, có bốn bộ chứa chữ số không. Khi xếp mỗi bộ gồm ba chữ số, ta có sáu hoán vị nếu không ràng buộc. Nhưng những cách bắt đầu bằng không không phải số có ba chữ số; cố định không đầu và đổi hai chữ số kia có hai cách sai. Mỗi bộ chứa không vì vậy tạo bốn số hợp lệ, tất cả mười sáu số.

**Trên màn hình:** Chọn 0 cố định ở nhóm dư 0. | Hai nhóm khác có 2×2 = 4 bộ. | Mỗi bộ xếp thành số: 3!−2! = 4.
**Ghi nhớ:** CÓ 16 SỐ TỪ CÁC BỘ CHỨA 0.

### Nhịp 23 · 08:48 · BỘ KHÔNG CHỨA 0

Bốn bộ còn lại lấy chữ số ba ở nhóm dư không và không chứa chữ số không. Vì mọi chữ số đều khác không, cả ba vị trí có thể nhận mỗi chữ số của bộ nên có ba giai thừa, tức sáu cách xếp. Nhân với bốn bộ được hai mươi bốn số. Hai loại bộ có không và không có không là rời nhau nên ta sẽ cộng kết quả.

**Trên màn hình:** Lấy chữ số 3 của nhóm dư 0. | Có 2×2 = 4 bộ. | Mỗi bộ có 3! = 6 cách xếp.
**Ghi nhớ:** CÓ 24 SỐ TỪ CÁC BỘ NÀY.

### Nhịp 24 · 09:12 · KẾT LUẬN 40 SỐ

Như vậy có mười sáu số được lập từ bộ chứa không và hai mươi bốn số từ bộ không chứa không, tổng cộng bốn mươi số chia hết cho ba. Điểm then chốt không phải thử hàng trăm hay hàng đơn vị trước, mà là kiểm soát tổng chữ số theo phần dư. Nếu bài thay đổi tập chữ số, phải chia lại các nhóm dư, không thể dùng nguyên kết quả bốn mươi.

**Trên màn hình:** Bộ chứa 0: 16 số. | Bộ không chứa 0: 24 số. | Tổng cộng: 40 số chia hết cho 3.
**Ghi nhớ:** CHỨNG MINH BẰNG LỚP ĐỒNG DƯ.


## 05 · RÀNG BUỘC KHOẢNG GIÁ TRỊ

### Nhịp 25 · 09:36 · ĐỒNG THỜI LỚN HƠN 300 VÀ CHẴN

Ta chuyển sang bài có hai điều kiện cùng lúc: từ tập không đến năm, lập số có ba chữ số khác nhau, chẵn và lớn hơn ba trăm. Điều kiện về độ lớn tác động vào hàng trăm, còn điều kiện chẵn tác động vào hàng đơn vị. Ta không thể đếm riêng số chẵn và số lớn hơn ba trăm rồi nhân hai kết quả. Cần đếm chung những số thỏa đồng thời cả hai.

**Trên màn hình:** Dùng các chữ số 0,1,2,3,4,5. | Lập số ba chữ số đôi một khác nhau. | Số phải chẵn và lớn hơn 300.
**Ghi nhớ:** HÀNG TRĂM CHỈ LÀ 3, 4 HOẶC 5.

### Nhịp 26 · 10:00 · HÀNG TRĂM LÀ 3

Khi hàng trăm là ba, mọi số có ba chữ số khác nhau đều lớn hơn ba trăm. Vì số phải chẵn, hàng đơn vị được chọn trong không, hai, bốn, có ba cách; cả ba thẻ đều khác ba. Sau khi chốt đầu và cuối, hàng chục còn bốn cách. Ta thu được mười hai số ở nhánh hàng trăm bằng ba.

**Trên màn hình:** Số cuối thuộc 0, 2 hoặc 4. | Có 3 lựa chọn hàng đơn vị. | Hàng chục còn 4 lựa chọn.
**Ghi nhớ:** NHÁNH HÀNG TRĂM 3 CÓ 12 SỐ.

### Nhịp 27 · 10:24 · HÀNG TRĂM LÀ 4

Nếu hàng trăm là bốn, chữ số bốn không được xuất hiện lại ở hàng đơn vị. Trong ba chữ số chẵn không, hai, bốn, ta chỉ còn không và hai, tức hai cách. Hàng chục tiếp tục có bốn cách chọn các chữ số chưa dùng. Kết quả nhánh này là tám số, ít hơn hai nhánh còn lại do chữ số đầu đã là một chữ số chẵn.

**Trên màn hình:** Chữ số 4 đã được sử dụng. | Ô cuối chỉ có thể là 0 hoặc 2. | Hàng chục còn 4 lựa chọn.
**Ghi nhớ:** NHÁNH HÀNG TRĂM 4 CÓ 8 SỐ.

### Nhịp 28 · 10:48 · HÀNG TRĂM LÀ 5

Với hàng trăm bằng năm, chữ số đầu không trùng với các thẻ chẵn không, hai, bốn, nên ô cuối có ba cách. Sau hai ô đầu cuối, còn bốn thẻ khác để điền hàng chục. Có mười hai số hợp lệ trong nhánh này. Dù điều kiện lớn hơn ba trăm đã được bảo đảm, ta vẫn phải giữ điều kiện khác nhau khi điền vị trí còn lại.

**Trên màn hình:** Số cuối có thể là 0, 2 hoặc 4. | Có 3 lựa chọn hàng đơn vị. | Hàng chục còn 4 lựa chọn.
**Ghi nhớ:** NHÁNH HÀNG TRĂM 5 CÓ 12 SỐ.

### Nhịp 29 · 11:12 · CỘNG TẤT CẢ NHÁNH

Ba trường hợp hàng trăm ba, bốn, năm không trùng nhau và bao phủ mọi số lớn hơn ba trăm trong tập chữ số đang xét. Vì thế ta cộng mười hai, tám và mười hai, được ba mươi hai số vừa chẵn vừa lớn hơn ba trăm. Cột hình bên trái hiển thị ba nhánh có chiều cao tương ứng, để học sinh thấy không thể nhân số cách của một nhánh cho ba.

**Trên màn hình:** Hàng trăm 3: 12 số. | Hàng trăm 4: 8 số. | Hàng trăm 5: 12 số.
**Ghi nhớ:** CÓ 32 SỐ THỎA CẢ HAI ĐIỀU KIỆN.

### Nhịp 30 · 11:36 · CÁCH NGHĨ TỔNG QUÁT

Từ bài này, ta rút ra một quy trình: xác định vị trí bị ràng buộc bởi độ lớn; xác định chữ số cuối để kiểm soát chẵn lẻ; sau đó đếm những chữ số chưa dùng. Nếu số lựa chọn thay đổi theo nhánh, phải cộng từng nhánh. Đó là cách xử lý chuẩn cho các bài lập số nhiều điều kiện và cũng là sự vận dụng linh hoạt của quy tắc cộng, nhân.

**Trên màn hình:** Bất đẳng thức thường xét chữ số đầu. | Chẵn/lẻ thường xét chữ số cuối. | Trùng chữ số buộc số nhánh thay đổi.
**Ghi nhớ:** ĐỌC CÙNG LÚC CẢ BA ĐIỀU KIỆN.


## 06 · CHỮ SỐ LẶP VÀ PHẦN BÙ

### Nhịp 31 · 12:00 · ÍT NHẤT HAI CHỮ SỐ TRÙNG

Ta lại dùng sáu chữ số không đến năm, nhưng lần này lập số có bốn chữ số và cho phép sử dụng lại chữ số. Đề yêu cầu trong bốn vị trí phải có ít nhất hai vị trí mang cùng một chữ số. Thay vì phân loại một đôi trùng, hai đôi trùng, ba lần trùng hoặc bốn lần trùng, ta xét phần bù: tất cả bốn chữ số đôi một khác nhau.

**Trên màn hình:** Dùng tập 0,1,2,3,4,5. | Lập số có bốn chữ số, cho phép lặp. | Cần ít nhất một chữ số xuất hiện hai lần.
**Ghi nhớ:** ĐẾM PHẦN BÙ SẼ NGẮN HƠN.

### Nhịp 32 · 12:24 · ĐẾM TỔNG KHÔNG CẤM LẶP

Nếu được phép lặp chữ số, sau khi chọn hàng nghìn khác không theo năm cách, ba vị trí còn lại đều có sáu lựa chọn độc lập. Đã dùng số hai ở hàng nghìn cũng không cấm dùng số hai thêm ở hàng trăm hay hàng chục. Vì vậy toàn bộ có năm nhân sáu mũ ba, bằng một nghìn không trăm tám mươi số.

**Trên màn hình:** Hàng nghìn: 5 cách, không dùng 0. | Ba hàng phía sau: 6 cách mỗi hàng. | Tổng cộng 1.080 số.
**Ghi nhớ:** PHÉP NHÂN KHÔNG GIẢM KHI CHO LẶP.

### Nhịp 33 · 12:48 · ĐẾM PHẦN BÙ KHÔNG LẶP

Nếu bốn chữ số đôi một khác nhau, hàng nghìn có năm lựa chọn, hàng trăm còn năm, hàng chục còn bốn, hàng đơn vị còn ba. Ta được ba trăm số. Những số này chính là toàn bộ kết quả sai với yêu cầu có ít nhất một chữ số lặp. Không cần đếm chính xác mỗi chữ số lặp bao nhiêu lần, bởi phần bù đã gom hết các trường hợp không lặp.

**Trên màn hình:** Hàng nghìn: 5 cách. | Ba vị trí sau: 5, 4, 3 cách. | Tổng cộng 300 số khác nhau.
**Ghi nhớ:** PHẦN BÙ GỒM TOÀN BỘ SỐ KHÔNG TRÙNG.

### Nhịp 34 · 13:12 · LẤY TỔNG TRỪ PHẦN BÙ

Ta lấy một nghìn không trăm tám mươi trừ ba trăm, được bảy trăm tám mươi số có ít nhất hai vị trí trùng chữ số. Cần hiểu rằng một số như một một một hai vẫn được đếm đúng một lần, mặc dù bên trong nó có nhiều cặp vị trí trùng nhau. Đó là ưu thế của phương pháp phần bù so với việc đếm từng cặp trùng trực tiếp.

**Trên màn hình:** Tất cả: 1.080 số. | Không lặp: 300 số. | Có ít nhất một cặp trùng: 780 số.
**Ghi nhớ:** KẾT QUẢ ĐÚNG LÀ 780.

### Nhịp 35 · 13:36 · MÃ PIN KHÁC SỐ TỰ NHIÊN

Một mã PIN bốn vị trí có thể bắt đầu bằng không, vì thế nếu mã lấy từ sáu chữ số thì có sáu mũ bốn mã khác nhau khi cho lặp. Nhưng ở bài này đối tượng là số có bốn chữ số, nên hàng nghìn phải khác không, chỉ có năm lựa chọn. Hai bài dùng cùng bốn ô và cùng bộ chữ số nhưng số lượng kết quả không giống nhau.

**Trên màn hình:** PIN có thể bắt đầu bằng số 0. | Số có bốn chữ số không thể như vậy. | Không được thay 5×6³ thành 6⁴.
**Ghi nhớ:** MÔ HÌNH ĐẾM QUYẾT ĐỊNH CÔNG THỨC.

### Nhịp 36 · 14:00 · TỔNG QUÁT VỚI N CHỮ SỐ

Tổng quát, nếu bộ chữ số có n ký hiệu phân biệt và chứa không, một số tự nhiên k chữ số cho phép lặp có n trừ một cách ở vị trí đầu và n mũ k trừ một lựa chọn cho các vị trí sau. Phần không lặp có n trừ một cách ở đầu rồi giảm lần lượt n trừ một, n trừ hai và cứ thế. Lấy hiệu hai số này để đếm ít nhất một chữ số lặp.

**Trên màn hình:** Có n chữ số trong đó có 0. | Lập số k chữ số, k không lớn hơn n. | Lặp = tổng được lặp − không lặp.
**Ghi nhớ:** CẦN XÁC ĐỊNH TẬP VÀ VỊ TRÍ ĐẦU.


## 07 · CHIA HẾT CHO 4

### Nhịp 37 · 14:24 · CHIA HẾT CHO 4: XÉT HAI Ô CUỐI

Với chia hết cho bốn, điều kiện đúng là số tạo bởi hai chữ số cuối chia hết cho bốn. Vì vậy ta phải chọn một cặp hàng chục và hàng đơn vị hợp lệ, thay vì chỉ chọn chữ số cuối chẵn. Trên màn hình, hai ô cuối được đóng trong một khung sáng, còn hai ô hàng nghìn và hàng trăm tạm để trống cho bước tiếp theo.

**Trên màn hình:** Tập chữ số 0,1,2,3,4,5. | Lập số bốn chữ số khác nhau. | Yêu cầu chia hết cho 4.
**Ghi nhớ:** KHÔNG CHỈ NHÌN MỘT CHỮ SỐ CUỐI.

### Nhịp 38 · 14:48 · LIỆT KÊ HAI CHỮ SỐ CUỐI

Ta kiểm tra tất cả cặp có hai chữ số khác nhau lấy từ không đến năm. Những cặp tạo số chia hết cho bốn là không bốn, một hai, hai không, hai bốn, ba hai, bốn không và năm hai. Viết cặp không bốn có nghĩa hàng chục bằng không và đơn vị bằng bốn; điều này hoàn toàn hợp lệ vì đó là hai chữ số cuối, không phải hai chữ số đầu của toàn bộ số.

**Trên màn hình:** Các cặp hợp lệ trong tập chữ số: | 04, 12, 20, 24, 32, 40, 52. | Không được lặp chữ số.
**Ghi nhớ:** CHỈ CÓ BẢY CẶP CUỐI HỢP LỆ.

### Nhịp 39 · 15:12 · NHÓM CẶP CÓ CHỨA 0

Ba cặp tận cùng không bốn, hai không và bốn không đều sử dụng chữ số không. Do đó khi chọn hai chữ số đầu trong bốn thẻ còn lại, không có thẻ không nên hàng nghìn có cả bốn cách, rồi hàng trăm có ba cách. Mỗi cặp tạo mười hai số, tổng cộng ba nhân mười hai bằng ba mươi sáu số.

**Trên màn hình:** Có ba cặp: 04, 20, 40. | Trong bốn thẻ còn lại không có 0. | Hai ô đầu có 4×3 = 12 cách.
**Ghi nhớ:** BA CẶP NÀY CHO 36 SỐ.

### Nhịp 40 · 15:36 · NHÓM CẶP KHÔNG CHỨA 0

Bốn cặp cuối còn lại không sử dụng chữ số không, nên trong bốn thẻ chưa dùng có một thẻ không và ba thẻ khác không. Hàng nghìn chỉ được chọn một trong ba thẻ khác không; hàng trăm sau đó có ba lựa chọn. Mỗi cặp tạo chín số, cả bốn cặp tạo ba mươi sáu số. Một lần nữa việc có hay không có chữ số không ở phần đã điền làm thay đổi số cách điền phần còn lại.

**Trên màn hình:** Bốn cặp: 12, 24, 32, 52. | Còn 0 và ba chữ số khác. | Hàng nghìn 3 cách, hàng trăm 3 cách.
**Ghi nhớ:** BỐN CẶP NÀY CHO 36 SỐ.

### Nhịp 41 · 16:00 · KẾT LUẬN CHIA HẾT CHO 4

Hai nhóm cặp cuối không giao nhau, và mọi số chia hết cho bốn bắt buộc dùng một cặp nằm trong đúng một nhóm. Do đó có ba mươi sáu cộng ba mươi sáu bằng bảy mươi hai số có bốn chữ số khác nhau từ tập không đến năm và chia hết cho bốn. Phép liệt kê bằng chương trình xác nhận đúng bảy mươi hai kết quả.

**Trên màn hình:** Nhóm có 0: 36 số. | Nhóm không có 0: 36 số. | Tổng cộng: 72 số.
**Ghi nhớ:** ĐÃ XÉT ĐÚNG ĐIỀU KIỆN HAI CHỮ SỐ CUỐI.

### Nhịp 42 · 16:24 · SAI LẦM: CỨ SỐ CHẴN LÀ /4

Số chia hết cho bốn luôn chẵn, nhưng một số chẵn như một nghìn hai trăm ba mươi hai chia hết cho bốn, còn một nghìn hai trăm ba mươi bốn thì không. Nếu ta chỉ chọn hàng đơn vị là không, hai hay bốn thì đã đếm thừa các số không chia hết cho bốn. Mẹo hai chữ số cuối là điều kiện cần và đủ, phải được sử dụng nguyên vẹn.

**Trên màn hình:** Mọi bội của 4 đều là số chẵn. | Không phải mọi số chẵn đều chia hết cho 4. | Phải kiểm tra hai chữ số cuối.
**Ghi nhớ:** ĐỪNG THAY ĐIỀU KIỆN MẠNH BẰNG ĐIỀU KIỆN YẾU.


## 08 · THỬ THÁCH BA ĐIỀU KIỆN

### Nhịp 43 · 16:48 · THỬ THÁCH CUỐI VIDEO

Bài cuối yêu cầu lập số có bốn chữ số đôi một khác nhau từ tập không đến năm, lớn hơn ba nghìn và chia hết cho mười lăm. Vì mười lăm bằng ba nhân năm và ba, năm nguyên tố cùng nhau, ta phải đồng thời bảo đảm chia hết cho ba và chia hết cho năm. Ta không thể đếm số chia hết cho ba rồi nhân số chia hết cho năm, mà phải tìm giao của hai điều kiện.

**Trên màn hình:** Dùng 0,1,2,3,4,5. | Lập số bốn chữ số khác nhau. | Số lớn hơn 3000 và chia hết cho 15.
**Ghi nhớ:** PHỐI HỢP ĐỘ LỚN, CHIA HẾT VÀ KHÔNG LẶP.

### Nhịp 44 · 17:12 · PHÂN TÍCH CÁC ĐIỀU KIỆN

Số lớn hơn ba nghìn nên trong tập chữ số đã cho, hàng nghìn chỉ có thể là ba, bốn hoặc năm. Điều kiện chia hết cho năm ép chữ số cuối bằng không hoặc năm, và tất nhiên hai đầu không được trùng nhau. Sau khi cố định hai đầu, ta phải chọn hai chữ số giữa sao cho tổng bốn chữ số chia hết cho ba. Đây chính là bước quyết định của bài.

**Trên màn hình:** Hàng nghìn chỉ có thể là 3,4,5. | Hàng đơn vị chỉ có thể là 0,5. | Tổng bốn chữ số chia hết cho 3.
**Ghi nhớ:** BẮT ĐẦU TỪ HAI Ô BỊ KHÓA MẠNH.

### Nhịp 45 · 17:36 · HÀNG NGHÌN 3, CUỐI 0

Khi hàng nghìn là ba và đơn vị là không, tổng hai chữ số cố định đã chia hết cho ba. Vì vậy tổng hai chữ số ở giữa cũng phải chia hết cho ba. Trong tập một, hai, bốn, năm, các cặp không thứ tự phù hợp là một với hai, một với năm, hai với bốn và bốn với năm. Mỗi cặp đổi thứ tự được hai cách, nên có tám số.

**Trên màn hình:** Đầu là 3, cuối là 0. | Hai chữ số giữa chọn và sắp từ 1,2,4,5. | Có đúng 8 cách hợp lệ.
**Ghi nhớ:** NHÁNH 3…0 CÓ 8 SỐ.

### Nhịp 46 · 18:00 · HÀNG NGHÌN 3, CUỐI 5

Nếu số bắt đầu bằng ba và kết thúc bằng năm, tổng của hai chữ số cố định bằng tám, dư hai khi chia cho ba. Vậy hai chữ số giữa cần có tổng dư một. Từ không, một, hai, bốn, chỉ có các cặp không thứ tự không với một và không với bốn phù hợp. Mỗi cặp có hai thứ tự, nên có bốn số trong nhánh hàng nghìn ba, đơn vị năm.

**Trên màn hình:** Đầu là 3, cuối là 5. | Hai chữ số giữa chọn từ 0,1,2,4. | Có đúng 4 cách hợp lệ.
**Ghi nhớ:** NHÁNH 3…5 CÓ 4 SỐ.

### Nhịp 47 · 18:24 · HÀNG NGHÌN 4 HOẶC 5

Ta tiếp tục làm tương tự khi chữ số đầu là bốn hoặc năm. Với đầu bốn cuối không, hai ô giữa tạo bốn số hợp lệ; với đầu bốn cuối năm, cũng có bốn; với đầu năm thì chữ số cuối không thể là năm nên buộc là không, tạo bốn số. Ba nhóm này rời nhau, tổng cộng mười hai số. Tất cả đều đã thỏa điều kiện không lặp và lớn hơn ba nghìn.

**Trên màn hình:** Đầu 4 cuối 0: 4 cách. | Đầu 4 cuối 5: 4 cách. | Đầu 5 cuối 0: 4 cách.
**Ghi nhớ:** BA NHÁNH CÒN LẠI CHO 12 SỐ.

### Nhịp 48 · 18:48 · KẾT LUẬN VÀ KIỂM CHỨNG

Cộng các trường hợp theo chữ số đầu, ta được mười hai cộng tám cộng bốn, bằng hai mươi bốn số thỏa mãn tất cả điều kiện. Để kiểm chứng độc lập, chương trình có thể tạo mọi hoán vị bốn chữ số khác nhau từ tập không đến năm, bỏ những kết quả bắt đầu bằng không, rồi kiểm tra lớn hơn ba nghìn và chia hết cho mười lăm. Kết quả đúng hai mươi bốn số, khớp lời giải.

**Trên màn hình:** Đầu 3: 8+4 = 12 số. | Đầu 4: 4+4 = 8 số. | Đầu 5: 4 số, tổng cộng 24.
**Ghi nhớ:** CÓ 24 SỐ THỎA BA ĐIỀU KIỆN.
