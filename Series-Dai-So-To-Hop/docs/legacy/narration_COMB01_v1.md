# LỜI GIẢNG VIDEO 01 — QUY TẮC CỘNG

**Series:** ĐẠI SỐ TỔ HỢP · Sang Math  
**Phong cách:** Tường minh, không đọc mã nguồn; cho học sinh tự dự đoán trước khi hiện phép tính.  
**Độ dài mục tiêu của bản có thuyết minh:** khoảng 10–12 phút.  
**Lưu ý kỹ thuật:** Đây là kịch bản thu âm; source Manim chưa gắn voiceover. Mốc thời gian là storyboard định hướng, không phải thời gian xuất từ mã hiện tại.

## 00:00–00:50 | Mở đầu: Có bao nhiêu con đường?

Trong toán học, có những bài toán chúng ta có thể giải chỉ bằng việc suy nghĩ xem một công việc được thực hiện theo bao nhiêu cách. Nhưng điều thú vị là, trước khi tính toán, chúng ta phải xác định chính xác điều gì được tính là một cách.

Hãy nhìn vào hình bên trái. Từ địa điểm A đến địa điểm B, ta có hai tuyến xe buýt khác nhau và ba tuyến tàu khác nhau. Một người muốn đi từ A đến B và chỉ cần chọn đúng một tuyến đường. Theo em, có bao nhiêu lựa chọn? Hãy thử dự đoán trước khi xem lời giải.

## 00:50–02:20 | Liệt kê để không bỏ sót

Trước tiên, nếu chọn xe buýt, người đó có thể đi theo tuyến xe buýt thứ nhất, hoặc tuyến xe buýt thứ hai. Như vậy, nhóm phương án đi xe buýt có hai lựa chọn.

Nếu không đi xe buýt mà chọn tàu, người đó có thể chọn một trong ba tuyến tàu đang được tô màu vàng. Nhóm phương án đi tàu có ba lựa chọn.

Chú ý: đề bài nói rằng người đó chọn một tuyến để đi, chứ không phải chọn đồng thời một tuyến xe buýt và một tuyến tàu. Đây là điểm mấu chốt quyết định phép tính chúng ta sử dụng.

Bây giờ hãy đếm: xe buýt thứ nhất, xe buýt thứ hai, tàu thứ nhất, tàu thứ hai và tàu thứ ba. Tổng cộng là năm tuyến đường khác nhau. Ta đã đếm toàn bộ lựa chọn mà không bỏ sót tuyến nào và cũng không đếm một tuyến đến hai lần.

## 02:20–04:15 | Hai nhóm lựa chọn

Chúng ta có thể tổ chức lại cách đếm vừa rồi. Đặt tất cả các lựa chọn đi xe buýt vào nhóm thứ nhất và các lựa chọn đi tàu vào nhóm thứ hai.

Nhóm thứ nhất có hai cách. Nhóm thứ hai có ba cách. Vì người đi đường chỉ chọn một trong hai loại phương tiện và không có tuyến nào vừa là tuyến xe buýt vừa là tuyến tàu, nên các kết quả của hai nhóm không trùng nhau.

Do đó, muốn đếm toàn bộ các cách đi, chúng ta chỉ cần lấy số cách của nhóm thứ nhất cộng với số cách của nhóm thứ hai. Hai cộng ba bằng năm.

Hãy lưu ý cách lập luận vừa thực hiện: chúng ta không cộng chỉ vì trong đề bài xuất hiện từ *hoặc*. Chúng ta cộng vì toàn bộ khả năng được tách thành những nhóm riêng và không có lựa chọn nào bị tính hai lần.

## 04:15–06:00 | Hình thành quy tắc cộng

Từ ví dụ này, hãy thử tổng quát hóa. Giả sử một công việc có thể thực hiện theo phương án A hoặc theo phương án B. Nếu phương án A có m cách, phương án B có n cách, và không có kết quả nào được tính vào cả hai phương án, thì số cách thực hiện công việc đó là m cộng n.

Đó chính là quy tắc cộng trong đại số tổ hợp.

Quy tắc này có thể mở rộng cho ba nhóm, bốn nhóm hoặc nhiều nhóm hơn, miễn là từng lựa chọn cụ thể chỉ thuộc đúng một nhóm đang được cộng. Khi số cách ở từng nhóm đã biết, ta lấy tổng số cách của các nhóm.

Tuy nhiên, nếu một kết quả có thể nằm trong nhiều nhóm, cộng trực tiếp sẽ dẫn đến đếm trùng. Chúng ta sẽ xem một phản ví dụ để hiểu rõ điều kiện này.

## 06:00–07:45 | Ví dụ chọn sách

Một bạn học sinh đứng trước giá sách. Có bốn quyển sách Toán khác nhau và ba quyển sách Vật lí khác nhau. Bạn ấy muốn chọn đúng một quyển để mang về đọc. Hỏi có bao nhiêu cách chọn?

Ta có thể chia thành hai trường hợp. Trường hợp thứ nhất: chọn một quyển sách Toán, có bốn cách. Trường hợp thứ hai: chọn một quyển sách Vật lí, có ba cách.

Mỗi quyển sách đều được nhận diện riêng. Một quyển sách Toán không đồng thời là một trong ba quyển sách Vật lí đã nêu. Do đó hai nhóm không trùng nhau. Theo quy tắc cộng, số cách chọn một quyển sách là bốn cộng ba, bằng bảy cách.

Các em thấy rằng hình ảnh đường đi và hình ảnh giá sách rất khác nhau, nhưng tư duy đếm lại hoàn toàn giống nhau: chia các kết quả thành các nhóm không trùng, rồi cộng số cách ở từng nhóm.

## 07:45–10:20 | Thử thách: Vì sao 6 + 4 không phải 10?

Đến một bài toán khó hơn một chút. Hãy xét các số tự nhiên từ một đến mười hai. Có bao nhiêu số chia hết cho hai hoặc chia hết cho ba?

Trước hết, các số chia hết cho hai là hai, bốn, sáu, tám, mười và mười hai. Có tất cả sáu số. Các số chia hết cho ba là ba, sáu, chín và mười hai. Có bốn số.

Nếu lấy sáu cộng bốn bằng mười, liệu có đúng không? Hãy quan sát hai ô số vừa được đánh dấu màu đỏ. Số sáu có mặt trong cả hai nhóm, bởi sáu chia hết cho hai và cũng chia hết cho ba. Số mười hai cũng thuộc cả hai nhóm với cùng một lí do.

Như vậy, khi cộng sáu và bốn, hai số sáu và mười hai đã bị đếm mỗi số hai lần. Nhưng đề bài chỉ yêu cầu đếm mỗi số một lần.

Để sửa lại, ta lấy sáu cộng bốn rồi trừ đi hai kết quả bị trùng. Kết quả là tám. Có đúng tám số chia hết cho hai hoặc cho ba trong đoạn từ một đến mười hai.

Ta có thể kiểm tra bằng cách liệt kê: hai, ba, bốn, sáu, tám, chín, mười, mười hai. Đúng tám số.

Phản ví dụ này cho thấy một bài học quan trọng: khi dùng quy tắc cộng, hãy kiểm tra xem những nhóm được cộng có phần chung hay không. Với hai nhóm có phần chung, cần trừ đi số kết quả nằm trong cả hai nhóm.

## 10:20–11:40 | Tổng kết và câu hỏi kiểm tra

Hãy cùng ghi nhớ những câu hỏi cần tự đặt ra trước khi giải một bài toán bằng quy tắc cộng. Thứ nhất, công việc được thực hiện bằng cách chọn một trong những phương án nào? Thứ hai, mỗi phương án có bao nhiêu kết quả? Và thứ ba, các nhóm kết quả có trùng nhau hay không?

Bây giờ là câu hỏi cuối cùng. Một trò chơi có năm phần thưởng loại A khác nhau và hai phần thưởng loại B khác nhau. Người chơi được chọn đúng một phần thưởng. Hỏi có bao nhiêu cách chọn? Hãy dừng video vài giây để suy nghĩ.

Vì hai loại phần thưởng là những đối tượng khác nhau, ta có thể áp dụng quy tắc cộng: năm cộng hai bằng bảy cách. Nếu em tìm được kết quả và giải thích được vì sao không đếm trùng, em đã nắm vững ý tưởng chính của bài học.

Ở video tiếp theo, chúng ta sẽ chuyển từ tình huống chọn *một trong nhiều nhóm* sang tình huống phải thực hiện *nhiều bước lựa chọn liên tiếp*. Khi ấy, phép nhân sẽ xuất hiện một cách tự nhiên.
