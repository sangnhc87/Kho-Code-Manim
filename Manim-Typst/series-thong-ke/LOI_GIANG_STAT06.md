# Lời giảng STAT06 – Phương sai và độ lệch chuẩn

## Chương 1, nhịp 1: Cùng trung bình có đủ chưa?

Có hai nhóm học sinh cùng số trung bình bằng bảy. Nhưng điều đó chưa đủ để nói mức điểm đồng đều như nhau. Quan sát năm điểm của từng nhóm trên cùng trục số. Nhóm thứ nhất tập trung gần bảy, nhóm thứ hai trải rộng hơn. Ta cần một đại lượng để mô tả độ phân tán, bên cạnh số đo trung tâm.

## Chương 1, nhịp 2: Mẫu A ở gần trung tâm

Mẫu A có năm giá trị năm, sáu, bảy, tám, chín. Tổng bằng ba mươi lăm nên trung bình là bảy. Các điểm trên hình không cách số bảy quá hai đơn vị. Những đoạn nối chấm với vạch trung bình chính là độ lệch có dấu. Hãy quan sát chúng trước khi biết công thức phương sai.

## Chương 1, nhịp 3: Mẫu B trải rộng hơn

Mẫu B gồm một, bốn, bảy, mười, mười ba. Tổng cũng là ba mươi lăm, nên trung bình vẫn bằng bảy. Song hai đầu của mẫu cách số bảy đến sáu đơn vị, khác xa mẫu A. Khi so sánh phân tán, ta phải đặt hai bộ dữ liệu lên cùng thang đo thay vì thay đổi tỉ lệ trục.

## Chương 1, nhịp 4: Phân tán đo bằng phương sai

Kết quả sẽ cho thấy phương sai A bằng hai, trong khi phương sai B bằng mười tám. Con số lớn hơn cho biết mức biến động quanh trung bình lớn hơn, không tự nói nhóm nào học giỏi hơn. Ta sẽ chứng minh hai kết quả ấy, từ các độ lệch cụ thể, chứ không chấp nhận công thức như một điều phải học thuộc.

## Chương 2, nhịp 1: Độ lệch âm và dương

Lấy từng phần tử của A trừ trung bình bảy, ta thu được âm hai, âm một, không, một, hai. Các điểm bên trái trung bình có độ lệch âm, bên phải có độ lệch dương. Nếu chỉ cộng các độ lệch này, dấu âm và dương triệt tiêu nhau, dù dữ liệu thực sự trải rộng.

## Chương 2, nhịp 2: Vì sao tổng độ lệch bằng 0?

Tổng của x thứ i trừ đi n lần số trung bình luôn bằng không, bởi trung bình chính là tổng dữ liệu chia n. Tính chất này đúng với mọi dãy không rỗng. Nó diễn tả vị trí cân bằng của trung bình, nhưng không đo khoảng cách các điểm đến tâm. Vì vậy cần một biến đổi khác.

## Chương 2, nhịp 3: Bình phương từng độ lệch

Ta bình phương từng độ lệch để loại dấu âm và nhấn mạnh các điểm cách xa trung bình. Các hình vuông xuất hiện với diện tích lần lượt bốn, một, không, một, bốn. Tổng bằng mười. Phương sai sử dụng độ lệch bình phương; nó không giống với trung bình khoảng cách tuyệt đối, một chỉ số có định nghĩa riêng.

## Chương 2, nhịp 4: Chia cho số quan sát

Lấy tổng bình phương độ lệch mười chia năm quan sát, ta được phương sai bằng hai. Trong thống kê mô tả ở chương trình phổ thông, mẫu số là n. Công thức chia cho n trừ một dùng khi ước lượng phương sai tổng thể không chệch, thuộc bối cảnh thống kê suy luận. Ở video này ta không đánh tráo hai công thức.

## Chương 3, nhịp 1: Dựng công thức tổng quát

Từ trực quan vừa xây dựng, ta lấy từng số trừ trung bình, bình phương, cộng tất cả và chia cho n. Công thức này được ký hiệu s bình phương. Hãy nhớ thứ tự thao tác: xác định trung bình trước, đo từng độ lệch, sau đó bình phương và lấy trung bình của các bình phương.

## Chương 3, nhịp 2: Độ lệch chuẩn là gì?

Phương sai có đơn vị bằng bình phương của đơn vị đo ban đầu. Nếu dữ liệu là điểm số, đơn vị của phương sai là điểm bình phương. Lấy căn bậc hai của phương sai, ta có độ lệch chuẩn s, trở lại đơn vị điểm. Điều này giúp việc trình bày kết quả dễ hiểu hơn, nhưng s không phải trung bình độ lệch tuyệt đối.

## Chương 3, nhịp 3: Trở lại 40 điểm giả lập

Ta quay lại bốn mươi điểm kiểm tra giả lập xuyên suốt các video đầu. Tổng điểm là hai trăm tám mươi bốn nên số trung bình bằng bảy phẩy một. Tổng bình phương từng điểm bằng hai nghìn một trăm lẻ tám. Từ đây ta có thể dùng công thức tính nhanh để giảm số phép trừ cần viết.

## Chương 3, nhịp 4: Kết quả của cả lớp

Chia hai nghìn một trăm lẻ tám cho bốn mươi, được năm mươi hai phẩy bảy. Trừ bình phương bảy phẩy một, tức năm mươi phẩy bốn mươi mốt, ta thu được phương sai hai phẩy hai mươi chín. Căn bậc hai cho độ lệch chuẩn xấp xỉ một phẩy năm một ba. Số làm tròn chỉ dùng ở bước kết luận cuối.

## Chương 4, nhịp 1: Bảng tần số giúp tính nhanh

Trong bốn mươi điểm có nhiều điểm trùng nhau. Ta dùng bảng tần số từ bốn đến mười để tính toán gọn hơn. Mỗi giá trị xuất hiện bao nhiêu lần thì đóng góp với trọng số là số lần ấy. Điều này không làm thay đổi bộ dữ liệu, chỉ thay đổi cách tổ chức phép tính.

## Chương 4, nhịp 2: Tính trung bình có trọng số

Dãy tần số là hai, bốn, tám, mười, tám, sáu, hai, tổng đúng bốn mươi. Nhân từng mức điểm với tần số rồi cộng, kết quả hai trăm tám mươi bốn. Lấy chia bốn mươi được trung bình bảy phẩy một. Hãy chú ý phân biệt tần số tuyệt đối với tần số tương đối.

## Chương 4, nhịp 3: Bình phương lệch có trọng số

Mỗi dòng bảng đóng góp bằng tần số nhân bình phương độ lệch so với bảy phẩy một. Cộng bảy dòng, ta được chín mươi mốt phẩy sáu. Lấy chia cho bốn mươi là hai phẩy hai mươi chín. Đây là phương sai của đúng bốn mươi quan sát ban đầu, không phải phương sai của riêng bảy giá trị phân biệt.

## Chương 4, nhịp 4: Công thức tính nhanh

Thay vì bình phương hiệu ở từng hàng, có thể lấy tổng tần số nhân bình phương giá trị, chia n, rồi trừ bình phương trung bình. Ở đây ta có hai nghìn một trăm lẻ tám chia bốn mươi, trừ bảy phẩy một bình phương, đúng bằng hai phẩy hai mươi chín. Hai cách giải đối chiếu nhau giúp giảm lỗi tính toán.

## Chương 5, nhịp 1: Nhìn thấy độ phân tán

Đặt hai mẫu A và B lên cùng trục số, vạch trung bình bảy giữ cố định. Khi các chấm di chuyển ra xa, ta nhìn thấy mức phân tán tăng lên. Điểm quan trọng là số trung bình không cần thay đổi khi độ phân tán thay đổi. Hai tính chất trung tâm và biến thiên trả lời hai câu hỏi thống kê khác nhau.

## Chương 5, nhịp 2: So sánh độ lệch chuẩn

Từ phương sai hai và mười tám, độ lệch chuẩn là căn hai và căn mười tám. Các giá trị gần đúng lần lượt là một phẩy bốn một bốn và bốn phẩy hai bốn ba. Trong ví dụ này, s của B lớn gấp ba lần s của A. Tuy nhiên đây là kết quả của bộ số liệu đã chọn, không phải quy luật cho mọi cặp dữ liệu.

## Chương 5, nhịp 3: Co giãn quanh tâm

Khi nhân mỗi độ lệch quanh bảy với một hệ số t, các chấm tự di chuyển xa hoặc gần tâm mà trung bình vẫn giữ bằng bảy. Phương sai tăng theo bình phương của t; độ lệch chuẩn tăng theo trị tuyệt đối của t. Ta có thể quan sát các con số cập nhật liên tục khi hệ số thay đổi, thay vì chỉ so sánh hai hình tĩnh.

## Chương 5, nhịp 4: Đọc độ lệch chuẩn đúng mức

Độ lệch chuẩn mô tả mức độ dao động theo một công thức cụ thể. Nó không tự kết luận một lớp học giỏi hay yếu, cũng không chỉ ra nguyên nhân của biến động. Khi so sánh hai mẫu, cần chú ý cùng đơn vị, cùng cách tính và bối cảnh thu thập số liệu. Thống kê giúp đặt câu hỏi, không thay thế suy luận về nguyên nhân.

## Chương 6, nhịp 1: Cộng một hằng số

Nếu cộng ba vào tất cả giá trị của mẫu A, trung bình từ bảy thành mười. Tuy vậy mỗi điểm và tâm cùng dịch ba đơn vị, nên độ lệch quanh tâm không đổi. Vì thế phương sai vẫn bằng hai và độ lệch chuẩn vẫn bằng căn hai. Trên trục số, cả nhóm chấm tịnh tiến mà khoảng cách tương đối không thay đổi.

## Chương 6, nhịp 2: Nhân đôi dữ liệu

Nếu nhân tất cả số liệu với hai thì trung bình cũng nhân hai. Mỗi độ lệch quanh trung bình tăng gấp đôi, nên bình phương độ lệch tăng gấp bốn. Phương sai của mẫu A từ hai thành tám, còn độ lệch chuẩn tăng gấp hai. Cảnh này giúp phân biệt rõ hệ số biến đổi của phương sai và của độ lệch chuẩn.

## Chương 6, nhịp 3: Công thức biến đổi tổng quát

Với biến đổi y bằng a nhân x cộng b, trung bình mới bằng a nhân trung bình cũ cộng b. Lấy y trừ trung bình y chỉ còn a nhân độ lệch cũ. Do đó phương sai nhân a bình phương, độ lệch chuẩn nhân trị tuyệt đối của a. Quy tắc vẫn đúng khi a âm, vì dấu âm mất đi sau phép bình phương.

## Chương 6, nhịp 4: Đổi đơn vị đo

Nếu độ dài đổi từ mét sang xăng-ti-mét, các giá trị nhân một trăm. Độ lệch chuẩn cũng nhân một trăm về trị số, còn phương sai nhân mười nghìn. Ta phải so sánh cùng đơn vị trước khi kết luận mẫu nào phân tán hơn. Đừng nhầm sự thay đổi thước đo với biến động mới của dữ liệu.

## Chương 7, nhịp 1: Kéo một giá trị ra rất xa

Hãy thử thay đúng một quan sát mười bằng ba mươi trong bộ bốn mươi điểm. Đây là thí nghiệm về độ nhạy, không phải điểm kiểm tra hợp lệ trên thang mười. Ba mươi chín điểm còn lại giữ nguyên. Dự đoán xem trung bình dịch bao nhiêu, và độ lệch chuẩn có tăng mạnh hơn cảm nhận từ trung bình hay không.

## Chương 7, nhịp 2: Trung bình thay đổi

Khi thay mười bằng ba mươi, tổng tăng thêm hai mươi, tức từ hai trăm tám mươi bốn lên ba trăm lẻ bốn. Chia bốn mươi cho trung bình mới bảy phẩy sáu. Vạch trung bình dịch một đoạn nhỏ sang phải, còn chấm mới tiến ra rất xa. Đây là lý do dữ liệu ngoại lệ có thể tác động khác nhau tới từng số đo.

## Chương 7, nhịp 3: Độ phân tán tăng mạnh

Tổng bình phương mới bằng hai nghìn chín trăm lẻ tám. Chia bốn mươi được bảy mươi hai phẩy bảy; trừ bình phương bảy phẩy sáu, ta nhận phương sai mười bốn phẩy chín mươi bốn. Độ lệch chuẩn xấp xỉ ba phẩy tám sáu năm. So với phương sai gốc hai phẩy hai mươi chín, mức tăng là rất lớn.

## Chương 7, nhịp 4: So sánh với IQR

Ở video trước, hai tứ phân vị của bộ dữ liệu này vẫn là sáu và tám sau khi đổi một cực trị; IQR không đổi bằng hai. Phương sai lại tăng mạnh vì bình phương độ lệch của điểm xa tâm rất lớn. Không nên coi IQR hay phương sai là tốt nhất trong mọi bài toán; mỗi số đo phục vụ một góc nhìn.

## Chương 8, nhịp 1: Bài thử sức năm số

Em hãy tự làm bài cuối với năm giá trị hai, bốn, sáu, tám, mười. Tính trung bình, xác định các độ lệch, bình phương chúng, rồi suy ra phương sai và độ lệch chuẩn. Hãy dừng hình trước khi nhìn đáp án. Những phép tính này đủ ngắn để thực hiện bằng tay và đủ rõ để kiểm tra từng bước.

## Chương 8, nhịp 2: Tìm trung bình và độ lệch

Tổng năm giá trị bằng ba mươi nên trung bình là sáu. Độ lệch so với sáu lần lượt âm bốn, âm hai, không, hai, bốn. Bình phương ta được mười sáu, bốn, không, bốn, mười sáu. Tổng là bốn mươi. Quan sát hình vuông ứng với từng độ lệch để thấy tại sao điểm ở xa tâm đóng góp lớn.

## Chương 8, nhịp 3: Kết quả chính xác và gần đúng

Lấy tổng bình phương bốn mươi chia năm, phương sai bằng tám. Căn bậc hai cho độ lệch chuẩn bằng hai căn hai, xấp xỉ hai phẩy tám hai tám. Phương sai mang đơn vị bình phương; độ lệch chuẩn cùng đơn vị dữ liệu. Khi làm bài, giữ kết quả căn thức chính xác trước, sau đó mới làm tròn theo yêu cầu đề.

## Chương 8, nhịp 4: Thay một số, kết luận thay đổi

Nếu chỉ thay mười bằng hai mươi, tổng thành bốn mươi và trung bình thành tám. Tổng bình phương là năm trăm hai mươi; lấy chia năm rồi trừ tám bình phương, phương sai mới là bốn mươi. Độ lệch chuẩn là hai căn mười. Ví dụ cuối khép lại ý tưởng: số trung bình và độ phân tán đều cần được tính, không thể thay thế nhau.
