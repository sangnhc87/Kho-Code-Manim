# KỊCH BẢN DẠY HỌC — TRẢI PHẲNG 01 MASTER

## Chủ đề
**Lập phương — Kiến đi ngắn nhất qua hai mặt kề nhau**

## Mục tiêu học sinh
- Nhận ra điểm đổi mặt phải nằm trên cạnh chung `BC`.
- Hiểu vì sao trải phẳng biến đường gấp trên hai mặt thành bài toán phẳng.
- Chứng minh ngắn nhất bằng bất đẳng thức tam giác, không đoán bằng mắt.
- Tính được `M` là trung điểm `BC` và `L_min = a√5`.
- Gấp trở lại để kiểm tra đường tìm được nằm trên đúng hai mặt.

## Nguyên tắc lời giảng
- Chỉ nói toán và dẫn dắt học sinh.
- Không đọc thuật ngữ sản xuất video, code, render, workflow hay kiểm thử.
- Mỗi ý được nói xong mới xuất hiện công thức tương ứng.
- Có khoảng dừng sau câu hỏi và sau kết luận quan trọng.

## 01. Đặt bài toán

**Lời 1:** Các em nhìn vào khối lập phương. Con kiến bắt đầu ở đỉnh A và muốn tới đỉnh C phẩy. Trong bài này, nó chỉ được bò trên hai mặt: mặt đáy A B C D và mặt bên B C C phẩy B phẩy. Câu hỏi là: nó nên đổi từ mặt đáy sang mặt bên tại đâu để tổng quãng đường ngắn nhất?

**Lời 2:** Nếu cho kiến đi xuyên qua lòng khối thì bài toán quá dễ, nhưng đó không phải đường đi trên bề mặt. Vì vậy ta phải tôn trọng hai mặt đã cho và tìm đường ngắn nhất ngay trên chúng.

## 02. Thử các đường đi dễ thấy

**Lời 1:** Cách đầu tiên rất tự nhiên: đi theo ba cạnh của lập phương. Khi đó quãng đường bằng ba a. Đường này chắc chắn hợp lệ, nhưng khá dài.

**Lời 2:** Ta có thể làm tốt hơn: từ A đi tới B, rồi đi theo đường chéo của mặt bên tới C phẩy. Độ dài lúc này là a cộng a căn hai. Nhưng câu hỏi vẫn còn: có thể ngắn hơn nữa không?

## 03. Điểm đổi mặt X

**Lời 1:** Mọi đường đi từ mặt đáy sang mặt bên đều phải đi qua cạnh chung B C. Gọi X là điểm mà con kiến đổi mặt. Khi X thay đổi, hai đoạn A X và X C phẩy cũng thay đổi. Ta cần tìm vị trí của X để tổng hai đoạn nhỏ nhất.

**Lời 2:** Nhìn trực tiếp trên hình ba chiều thì rất khó đoán X nên nằm ở đâu. Đây chính là lúc trải phẳng phát huy tác dụng.

## 04. Mở hai mặt

**Lời 1:** Ta giữ nguyên mặt đáy. Bây giờ mở mặt bên B C C phẩy B phẩy xuống quanh cạnh B C, giống như mở một cánh cửa. Các em để ý: B và C không di chuyển, còn C phẩy đi theo mặt bên.

**Lời 2:** Khi mở đủ chín mươi độ, hai mặt nằm trên cùng một mặt phẳng. Ta đổi sang góc nhìn thẳng từ trên xuống để thấy bản trải thật rõ.

## 05. Chứng minh bằng đường thẳng trên bản trải

**Lời 1:** Sau khi trải phẳng, điểm X vẫn nằm trên cạnh B C. Đường A X rồi X C một là một đường gấp khúc trong mặt phẳng. Theo bất đẳng thức tam giác, tổng A X cộng X C một luôn lớn hơn hoặc bằng đoạn thẳng A C một.

**Lời 2:** Dấu bằng chỉ xảy ra khi A, X và C một nằm trên cùng một đường thẳng. Vì vậy ta không cần đoán nữa: chỉ việc nối thẳng A với C một; giao điểm của đường thẳng này với B C chính là vị trí đổi mặt tối ưu.

## 06. Tính M và độ dài ngắn nhất

**Lời 1:** Hai hình vuông ghép lại thành một hình chữ nhật có chiều dài hai a và chiều rộng a. Vì thế đoạn A C một là đường chéo của hình chữ nhật này.

**Lời 2:** Áp dụng định lý Pythagore, A C một bằng căn của hai a bình phương cộng a bình phương, tức là a căn năm. Đây chính là độ dài nhỏ nhất mà con kiến có thể đi trên hai mặt đã cho.

**Lời 3:** Đường A C một đi qua B C tại trung điểm M. Do đó B M bằng M C bằng a trên hai. Vậy trên khối ban đầu, con kiến phải đổi mặt đúng tại trung điểm của cạnh B C.

## 07. So sánh với các đường thử ban đầu

**Lời 1:** Bây giờ ta quay lại hai đường đã thử lúc đầu. Đường đi theo ba cạnh dài ba a. Đường đi qua B rồi chéo tới C phẩy dài a nhân một cộng căn hai. Còn đường vừa tìm được chỉ dài a căn năm.

**Lời 2:** Vì căn năm nhỏ hơn một cộng căn hai, và một cộng căn hai nhỏ hơn ba, đường qua trung điểm M thật sự ngắn hơn cả hai cách ban đầu. Quan trọng hơn, ta đã chứng minh được nó ngắn nhất trong tất cả các vị trí X trên B C, chứ không chỉ ngắn hơn vài đường thử.

## 08. Gấp trở lại khối

**Lời 1:** Ta đã giải xong trên bản trải. Bây giờ gấp mặt bên trở lại để xem đường thẳng vừa tìm biến thành đường nào trên lập phương.

**Lời 2:** Đoạn A M nằm nguyên trên mặt đáy. Đoạn M C một đi cùng mặt bên khi mặt này được gấp lên. Khi khối trở lại hình dạng ban đầu, M C một trở thành đúng đoạn M C phẩy.

**Lời 3:** Như vậy đường ngắn nhất trên khối là A đến M, rồi M đến C phẩy, với M là trung điểm B C. Không có đoạn nào xuyên qua bên trong lập phương.

## 09. Kiến đi trên đường tối ưu

**Lời 1:** Con kiến đi từ A tới trung điểm M của B C trên mặt đáy.

**Lời 2:** Tại M, nó chuyển sang mặt bên và tiếp tục đi thẳng tới C phẩy. Hai đoạn này chính là hai phần của một đoạn thẳng duy nhất khi ta mở hai mặt ra.

## 10. Tổng kết phương pháp

**Lời 1:** Ta chốt lại cách làm. Trước hết xác định những mặt mà con kiến được phép đi qua. Sau đó mở các mặt ấy ra quanh cạnh chung. Khi đã nằm trên cùng một mặt phẳng, nối hai điểm bằng đoạn thẳng. Giao điểm của đoạn thẳng với cạnh chung cho ta điểm đổi mặt trên khối.

**Lời 2:** Trong bài này, điểm đổi mặt là trung điểm M của B C và quãng đường ngắn nhất bằng a căn năm. Điều cần nhớ nhất không phải con số a căn năm, mà là ý tưởng: một đường gấp trên hai mặt có thể trở thành một đoạn thẳng sau khi trải đúng hai mặt đó.

**Lời 3:** Ở video tiếp theo, hai điểm sẽ nằm trên hai mặt không kề nhau. Khi đó con kiến bắt buộc phải đi qua một mặt trung gian, và bản trải sẽ gồm ba mặt nối tiếp.
