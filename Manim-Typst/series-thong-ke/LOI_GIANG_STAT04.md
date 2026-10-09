# THONG-KE-04 – TỨ PHÂN VỊ Q1, Q2, Q3

Dữ liệu: 40 điểm giả lập của STAT01–03. Quy ước SGK: lấy trung vị của hai nửa; nếu n lẻ, loại trung vị chung trước khi chia.

Lời giảng được căn theo 32 nhịp trong `stat04/lesson.py`. Khi bật TTS, mỗi nhịp có một tệp âm thanh độc lập.

## Chương 01 – TỪ 40 ĐIỂM ĐẾN BA TỨ PHÂN VỊ

### Nhịp 1 — Một lớp, bốn mươi điểm

Hôm nay chúng ta không thay bộ dữ liệu. Bốn mươi điểm kiểm tra giả lập vẫn nằm từ bốn đến mười và được dùng ở toàn bộ phần thống kê cơ bản. Trung bình của lớp là bảy phẩy một, trung vị là bảy. Nhưng nếu muốn biết một phần tư lớp đang ở khu vực điểm nào, hai số ấy chưa đủ. Ta cần các tứ phân vị.


### Nhịp 2 — Sắp xếp trước khi chia

Các thẻ điểm trên màn hình sẽ rời vị trí ban đầu rồi sắp xếp từ bé đến lớn. Sau sắp xếp, hai điểm bốn xuất hiện trước, rồi bốn điểm năm, rồi tám điểm sáu. Không được lấy vị trí trong danh sách chưa sắp xếp để xác định tứ phân vị. Thứ tự chính là chìa khóa để chia dữ liệu thành những phần có ý nghĩa.


### Nhịp 3 — Ba mốc cần tìm

Hãy tưởng tượng một hàng gồm bốn mươi bạn đã được sắp xếp theo điểm. Ta sẽ xác định ba mốc Q một, Q hai và Q ba. Q hai trùng với trung vị đã học. Q một nằm ở vùng giữa của nửa thấp, còn Q ba nằm ở vùng giữa của nửa cao. Các mốc này giúp quan sát phần giữa của phân bố.


### Nhịp 4 — Không phải bốn nhóm điểm khác nhau

Một nhầm lẫn là chia đoạn từ điểm bốn tới điểm mười thành bốn khoảng có độ dài bằng nhau. Đó không phải cách xác định tứ phân vị của mẫu số liệu. Ta chia dựa theo số lượng quan sát đã sắp xếp, không dựa vào khoảng cách số học giữa giá trị nhỏ nhất và lớn nhất. Các tứ phân vị thậm chí có thể trùng nhau.

## Chương 02 – CHIA DỮ LIỆU THÀNH HAI NỬA

### Nhịp 1 — Với 40 điểm, tìm hai nửa

Vì có bốn mươi quan sát, ta chia danh sách đã sắp xếp thành hai nửa, mỗi nửa gồm hai mươi điểm. Nửa dưới là các vị trí từ một đến hai mươi. Nửa trên là các vị trí từ hai mươi mốt đến bốn mươi. Màu xanh chỉ nửa dưới; màu tím chỉ nửa trên. Không có quan sát nào bị bỏ đi ở trường hợp cỡ mẫu chẵn này.


### Nhịp 2 — Trung vị nằm giữa hai nửa

Giữa hai nửa chính là khoảng phân cách sau vị trí thứ hai mươi. Muốn tìm tứ phân vị thứ hai, ta lấy trung bình hai giá trị ở vị trí hai mươi và hai mươi mốt. Chúng đều là điểm bảy. Vì thế Q hai bằng bảy. Nhớ rằng hai mươi, hai mươi mốt là vị trí, còn bảy mới là giá trị quan sát.


### Nhịp 3 — Quy tắc cho cỡ mẫu chẵn

Ta có ba bài toán trung vị nhỏ: trung vị của cả bốn mươi điểm, trung vị của hai mươi điểm phía dưới và trung vị của hai mươi điểm phía trên. Hai bài cuối lần lượt tạo Q một và Q ba. Phương pháp này tránh cách nhớ máy móc theo một công thức vị trí không thích hợp với quy ước sách giáo khoa.


### Nhịp 4 — Em thử dự đoán

Trước khi các thẻ được đánh dấu, em hãy dự đoán Q một và Q ba sẽ bằng mấy. Quan sát bảng tần số: nhóm điểm sáu nằm khá nhiều ở phần thấp; nhóm điểm tám chiếm đáng kể ở phần cao. Tuy nhiên chúng ta chưa kết luận chỉ bằng quan sát biểu đồ. Bước tiếp theo phải xác định đúng hai vị trí giữa của từng nửa.

## Chương 03 – TÌM Q1 VÀ Q3 TRÊN 40 ĐIỂM

### Nhịp 1 — Giữa nửa dưới là đâu?

Nửa dưới có hai mươi quan sát. Trong nửa dưới, hai vị trí ở giữa là thứ mười và thứ mười một. Vì nửa này bắt đầu từ vị trí một của cả dãy, đó cũng chính là vị trí mười và mười một của toàn bộ dữ liệu. Hai thẻ này đều mang điểm sáu. Ta lấy trung bình cộng của chúng để được Q một.


### Nhịp 2 — Tính Q1

Chúng ta phóng lớn riêng hai thẻ ở vị trí mười và mười một. Cả hai đều bằng sáu, do đó Q một bằng sáu. Điều này không có nghĩa đúng mười bạn có điểm nhỏ hơn sáu, bởi bộ số liệu chứa nhiều điểm trùng nhau. Hãy nói chính xác: Q một được xác định từ trung vị của nửa dãy dưới.


### Nhịp 3 — Giữa nửa trên là đâu?

Nửa trên bắt đầu ở vị trí hai mươi mốt và có hai mươi phần tử. Vậy hai vị trí trung tâm của nửa trên nằm tại vị trí ba mươi và ba mươi mốt trong toàn bộ danh sách. Ta tô vàng cặp thẻ này. Chúng đều bằng tám, nên tứ phân vị thứ ba bằng tám. Cách tìm hoàn toàn tương tự với Q một.


### Nhịp 4 — Bộ ba cuối cùng

Ta đã có đủ ba tứ phân vị: sáu, bảy và tám. Trên trục số, ba vạch đứng xuất hiện từ trái sang phải. Q hai là trung vị đã biết, Q một mô tả phần thấp, Q ba mô tả phần cao. Mỗi tứ phân vị là giá trị được tính theo quy tắc chia nửa; cần thận trọng khi diễn giải thành phần trăm vì dữ liệu có nhiều điểm trùng.

## Chương 04 – TỨ PHÂN VỊ VÀ TẦN SỐ TÍCH LŨY

### Nhịp 1 — Bảng tần số cũng đủ dữ kiện

Trong đề thi, đôi khi người ta chỉ cho bảng giá trị và tần số. Ta vẫn xác định tứ phân vị được vì bảng tần số cho phép khôi phục vị trí trong danh sách sắp xếp. Hãy cộng dồn tần số từ điểm nhỏ nhất trở lên. Tổng tích lũy không giảm và cho biết đã đi qua bao nhiêu quan sát.


### Nhịp 2 — Tích lũy đến 6 là 14

Điểm bốn chiếm vị trí một, hai; điểm năm nằm từ ba đến sáu. Khi đi qua tám lần xuất hiện của điểm sáu, tổng tích lũy đạt mười bốn. Vì thế hai vị trí mười và mười một thuộc nhóm điểm sáu. Ta kết luận Q một bằng sáu mà không cần liệt kê riêng từng thẻ.


### Nhịp 3 — Tích lũy đến 7 là 24

Sau nhóm điểm sáu có mười bốn quan sát. Điểm bảy xuất hiện thêm mười lần, đưa tổng tích lũy lên hai mươi bốn. Vậy hai vị trí hai mươi và hai mươi mốt đều bằng bảy. Phương pháp tần số tích lũy giúp tìm trung vị và tứ phân vị hiệu quả khi dữ liệu được cho bằng bảng.


### Nhịp 4 — Tích lũy đến 8 là 32

Điểm tám xuất hiện tám lần, từ vị trí hai mươi lăm đến ba mươi hai. Bởi vậy vị trí ba mươi và ba mươi mốt đều bằng tám. Q ba nhận giá trị tám. Em hãy ghi nhớ quy trình: xác định cỡ mẫu, tìm các vị trí cần thiết rồi đọc giá trị từ tần số tích lũy. Tuyệt đối không coi tần số là giá trị điểm.

## Chương 05 – CỠ MẪU CHẴN, LẺ VÀ QUY ƯỚC

### Nhịp 1 — Ví dụ có 8 quan sát

Để thấy rõ các tứ phân vị không phải lúc nào cũng là giá trị có sẵn, ta dùng tám số từ một đến tám. Q hai là trung bình của bốn và năm, bằng bốn phẩy năm. Q một là trung bình của hai và ba, bằng hai phẩy năm. Q ba là trung bình của sáu và bảy, bằng sáu phẩy năm.


### Nhịp 2 — Ví dụ có 9 quan sát

Bây giờ thêm số chín và có chín quan sát từ một đến chín. Trung vị chính là số năm ở vị trí thứ năm. Khi tìm Q một và Q ba theo quy ước của bài học, ta không đưa số năm vào hai nửa. Nửa dưới gồm một, hai, ba, bốn; nửa trên gồm sáu, bảy, tám, chín.


### Nhịp 3 — Tính ba mốc khi n lẻ

Trung vị của bốn giá trị phía dưới là trung bình hai và ba, nên Q một bằng hai phẩy năm. Trung vị cả dãy bằng năm. Nửa trên có bốn số sáu, bảy, tám, chín nên Q ba là trung bình của bảy và tám, bằng bảy phẩy năm. Chú ý phép tách nửa khác trường hợp chẵn đúng một giá trị ở giữa.


### Nhịp 4 — Vì sao tài liệu có thể khác kết quả?

Một số phần mềm hoặc tài liệu sử dụng cách nội suy theo phần trăm, khiến Q một và Q ba khác kết quả tính bằng trung vị của hai nửa. Điều đó không tự động có nghĩa một nguồn sai. Trong bài học này, ta dùng quy ước phổ thông Việt Nam: tìm trung vị của nửa dưới, nửa trên và bỏ trung vị chung khi cỡ mẫu lẻ. Khi giải đề phải theo quy ước được yêu cầu.

## Chương 06 – GIÁ TRỊ NGOẠI LỆ VÀ PHÉP DỊCH

### Nhịp 1 — Kéo một điểm ngoại lệ

Ta trở lại bốn mươi điểm ban đầu. Thử thay một điểm mười bằng ba mươi, làm một quan sát trở nên rất lớn. Các thẻ còn lại không đổi; chỉ thẻ ở cuối hàng được kéo sang phải. Trung bình tăng vì tổng tăng, nhưng các vị trí mười, mười một, hai mươi, hai mươi mốt, ba mươi, ba mươi mốt đều không đổi.


### Nhịp 2 — Kết quả tứ phân vị có đổi?

Sau thay đổi, ba tứ phân vị vẫn là sáu, bảy và tám. Trung bình, trong khi đó, tăng từ bảy phẩy một lên bảy phẩy sáu. Đây là một minh họa rằng tứ phân vị thường ít nhạy với một giá trị cực đoan ở đầu hoặc cuối. Nhưng không được kết luận rằng tứ phân vị bất biến với mọi phép thay đổi dữ liệu.


### Nhịp 3 — Dịch tất cả điểm thêm hai

Giờ hãy cộng hai vào tất cả các điểm ban đầu. Thứ tự các điểm không đổi vì cộng cùng một số giữ quan hệ lớn nhỏ. Ba vạch Q một, Q hai, Q ba cùng chuyển sang phải hai đơn vị. Kết quả mới lần lượt là tám, chín và mười. Khoảng cách giữa Q ba và Q một vẫn bằng hai.


### Nhịp 4 — Phân biệt thay một điểm và thay cả dãy

Khi chỉ thay một giá trị xa phần trung tâm, tứ phân vị có thể giữ nguyên. Khi cộng cùng một hằng số vào tất cả giá trị, chúng cùng dịch đúng bằng hằng số ấy. Hai hiện tượng có nguyên nhân hoàn toàn khác nhau. Em hãy mô tả phép biến đổi dữ liệu trước khi suy luận về sự biến đổi của các số đặc trưng.

## Chương 07 – KHOẢNG TỨ PHÂN VỊ VÀ SO SÁNH

### Nhịp 1 — Khoảng tứ phân vị

Khoảng tứ phân vị được tính bằng Q ba trừ Q một. Với lớp bốn mươi điểm, đó là tám trừ sáu, bằng hai điểm. Đại lượng này mô tả độ trải rộng của vùng trung tâm dữ liệu. Nó không phải khoảng biến thiên từ điểm nhỏ nhất đến điểm lớn nhất; khoảng biến thiên của bộ dữ liệu này bằng mười trừ bốn, tức sáu.


### Nhịp 2 — Hai mẫu cùng trung vị

So sánh hai mẫu tám số. Mẫu A là hai, ba, bốn, năm, sáu, bảy, tám, chín. Mẫu B là hai, hai, hai, năm, sáu, mười, mười, mười. Cả hai có trung vị năm phẩy năm. Nhưng các điểm của mẫu B tập trung hơn ở hai phía, khiến khoảng tứ phân vị của nó lớn hơn rõ rệt.


### Nhịp 3 — Tính Q1 và Q3 cho hai mẫu

Với mẫu A, Q một bằng ba phẩy năm và Q ba bằng bảy phẩy năm, nên khoảng tứ phân vị là bốn. Với mẫu B, Q một bằng hai và Q ba bằng mười, nên khoảng tứ phân vị là tám. Dù cùng trung vị, mẫu B có phần giữa trải rộng gấp đôi theo thước đo IQR. Điều này minh họa vì sao cần thêm số đo phân tán.


### Nhịp 4 — Dẫn sang biểu đồ hộp

Ba tứ phân vị có thể kết hợp với giá trị nhỏ nhất và lớn nhất tạo thành tóm tắt năm số. Từ năm mốc này, ta sẽ dựng biểu đồ hộp ở tập tiếp theo. Ngay lúc này, em hãy ghi nhớ khoảng tứ phân vị đo độ trải rộng giữa Q một và Q ba, chứ không nói lên tất cả hình dạng phân bố hoặc tự động phát hiện ngoại lệ.

## Chương 08 – BÀI TOÁN NGƯỢC VÀ TỔNG KẾT

### Nhịp 1 — Bài toán tìm số còn thiếu

Bài cuối dành cho em tự kiểm tra. Tám giá trị đã ở thứ tự không giảm, nhưng giá trị thứ tư chưa biết và được ký hiệu x. Biết rằng trung vị Q hai bằng sáu phẩy năm. Hãy tìm x, sau đó tính Q một, Q ba và khoảng tứ phân vị. Em có thể dừng video khoảng mười giây để tự làm trước khi xem phép tính.


### Nhịp 2 — Tìm x bằng Q2

Vì cỡ mẫu bằng tám, Q hai là trung bình cộng của vị trí thứ tư và thứ năm. Vậy x cộng bảy rồi chia hai bằng sáu phẩy năm. Nhân hai vế ta được x cộng bảy bằng mười ba; suy ra x bằng sáu. Kết quả thỏa điều kiện dãy tăng dần, bởi sáu nằm giữa năm và bảy.


### Nhịp 3 — Tìm các tứ phân vị

Nửa dưới là ba, bốn, năm, sáu; trung vị nửa dưới bằng trung bình của bốn và năm, tức bốn phẩy năm. Nửa trên là bảy, tám, chín, mười; trung vị bằng trung bình của tám và chín, tức tám phẩy năm. Khoảng tứ phân vị bằng tám phẩy năm trừ bốn phẩy năm, bằng bốn.


### Nhịp 4 — Bốn bước để tránh nhầm

Ta tổng kết Video bốn bằng bốn thao tác: sắp xếp dữ liệu, tìm Q hai, chia hai nửa theo đúng quy ước để tính Q một và Q ba, rồi đối chiếu kết quả với vị trí hoặc bảng tần số. Bộ bốn mươi điểm xuyên suốt cho kết quả sáu, bảy, tám. Tập sau sẽ dùng các giá trị ấy để dựng biểu đồ hộp và phân tích khoảng tứ phân vị.

