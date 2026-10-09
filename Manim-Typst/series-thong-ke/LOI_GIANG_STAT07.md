# STAT07 – Mẫu số liệu ghép nhóm và bảng tần số

Video 07 thuộc **SangMath Thống kê trực quan 10–11–12**. Dữ liệu minh họa là dữ liệu giả lập, kế thừa 40 điểm của STAT01–06. 32 nhịp, 8 chương. Lời đọc cụ thể được sử dụng đồng bộ trong `stat07/lesson.py`.


## Chương 01 – TỪ 40 ĐIỂM RỜI RẠC ĐẾN BẢNG GHÉP NHÓM

**Nhịp 1 – 40 điểm kiểm tra nhìn rất rối.**

Hãy bắt đầu bằng bốn mươi điểm kiểm tra giả lập của một lớp học. Khi đặt từng điểm trên màn hình, các con số lặp đi lặp lại và chưa thể nhìn nhanh mức độ tập trung. Thay vì xóa thông tin ngay, ta đếm và giữ nguyên bốn mươi quan sát trước. Nhiệm vụ là tóm tắt những giá trị gần nhau, song không làm thay đổi tổng số học sinh.

**Nhịp 2 – Từ dữ liệu rời đến bốn khoảng.**

Ta thử chia trục điểm thành bốn khoảng liên tiếp. Khoảng thứ nhất từ bốn đến dưới sáu, thứ hai từ sáu đến dưới tám, thứ ba từ tám đến dưới mười, cuối cùng từ mười đến dưới mười hai. Hai dấu ngoặc không giống nhau: đầu trái được nhận, đầu phải bị loại. Mỗi điểm được kéo về đúng một ngăn.

**Nhịp 3 – Quan sát những ngăn đã đầy.**

Ngăn đầu chứa hai điểm bốn và bốn điểm năm, tức sáu học sinh. Ngăn thứ hai có tám điểm sáu và mười điểm bảy, được mười tám. Ngăn thứ ba có tám điểm tám và sáu điểm chín, được mười bốn. Ngăn cuối có hai điểm mười. Các ngăn giúp nhận ra nhóm có nhiều điểm nhất.

**Nhịp 4 – Kiểm soát tổng quan sát.**

Một bảng ghép nhóm chỉ đáng tin khi mọi quan sát xuất hiện đúng một lần. Ta cộng bốn tần số và thu được bốn mươi, bằng cỡ mẫu ban đầu. Nhưng tổng đúng chưa đủ chứng minh tuyệt đối không trùng, vì ta có thể bỏ sót một điểm rồi lặp một điểm khác. Ta còn phải chứng minh các khoảng không chồng lấn và phủ hết dữ liệu.


## Chương 02 – RANH GIỚI LỚP VÀ QUY TẮC KHÔNG ĐẾM TRÙNG

**Nhịp 1 – Định nghĩa lớp nửa kín.**

Ký hiệu ngoặc vuông ở trái và ngoặc tròn ở phải tương ứng với nhận đầu trái và không nhận đầu phải. Ví dụ, khoảng từ bốn đến dưới sáu nhận giá trị bốn, năm; nếu dữ liệu có điểm năm phẩy chín cũng nhận. Nhưng sáu tuyệt đối không thuộc khoảng đầu. Đây là quy tắc nền để dựng bảng bằng máy hoặc bằng tay.

**Nhịp 2 – Điểm ở ranh giới thuộc lớp nào?.**

Hãy nhìn điểm sáu đứng đúng vạch phân lớp. Nếu ta dùng dấu nhỏ hơn hoặc bằng ở cả hai khoảng thì sáu sẽ được đếm hai lần. Nếu hai đầu đều mở thì sáu có thể không được đếm lần nào. Quy tắc nửa kín liên tiếp loại bỏ cả hai lỗi ấy: điểm sáu vào lớp thứ hai, điểm tám vào lớp thứ ba.

**Nhịp 3 – Giữ một quy ước xuyên suốt.**

Với dữ liệu điểm số trên thang mười, khoảng cuối từ mười đến dưới mười hai được dùng như một khoảng kỹ thuật có độ rộng hai, để bốn lớp đều rộng bằng nhau. Điều đó không có nghĩa tồn tại điểm mười một. Khi vẽ, ta phải ghi đúng ranh giới trên trục và không tưởng tượng dữ liệu ở chỗ chưa quan sát.

**Nhịp 4 – Kiểm tra cách phân lớp.**

Khi tự lập bảng ghép nhóm, em hãy kiểm tra ba điều. Thứ nhất các khoảng được mô tả bằng ranh giới rõ ràng. Thứ hai hai khoảng khác nhau không được nhận cùng một giá trị. Thứ ba mọi quan sát phải thuộc một trong các khoảng. Nếu khoảng thiếu đoạn, chồng lên nhau hoặc vượt khỏi phạm vi dữ liệu mà không giải thích, bảng sẽ dễ gây sai lệch.


## Chương 03 – BẢNG TẦN SỐ VÀ TẦN SỐ TÍCH LŨY

**Nhịp 1 – Tần số là gì?.**

Tần số của một lớp là số lượng quan sát nằm trong lớp ấy. Với bốn lớp đang xét, ta có bảng sáu, mười tám, mười bốn và hai. Không nên nhầm tần số là giá trị điểm hay là độ rộng của khoảng. Một lớp có tần số cao đơn giản vì nhiều quan sát rơi vào khoảng ấy, còn lớp rộng hơn có thể chứa nhiều quan sát chỉ vì rộng hơn.

**Nhịp 2 – Tần số tích lũy.**

Thay vì chỉ đọc từng lớp, đôi khi ta cần biết có bao nhiêu quan sát nằm dưới ranh giới phía trên của lớp ấy. Khi cộng dồn, lớp đầu có sáu, hai lớp đầu có hai mươi bốn, ba lớp đầu có ba mươi tám, và toàn bộ có bốn mươi. Đây là tần số tích lũy, giúp xác định nhanh số học sinh dưới một ngưỡng.

**Nhịp 3 – Giải thích từng con số.**

Dòng tích lũy ở cuối lớp từ sáu đến dưới tám bằng hai mươi bốn. Vì khoảng đầu nhận bốn đến dưới sáu và khoảng tiếp theo nhận sáu đến dưới tám, hai mươi bốn là số học sinh đạt dưới tám điểm. Nhớ rằng tám là ranh giới bị loại ở phía phải, nên các điểm bằng tám chưa được tính. Học sinh từ tám điểm trở lên có mười sáu em.

**Nhịp 4 – Một phép kiểm tra ngay trên bảng.**

Nếu các lớp phủ hết dữ liệu, giá trị cuối trong dãy tần số tích lũy phải bằng tổng số quan sát. Ở đây số đó là bốn mươi. Các giá trị tích lũy cũng không được giảm khi đi từ trái sang phải, vì mỗi bước chỉ cộng một tần số không âm. Nếu bảng có dòng tích lũy giảm hoặc tổng cuối khác n, chúng ta phải tìm lỗi trước khi vẽ biểu đồ.


## Chương 04 – TẦN SỐ TƯƠNG ĐỐI VÀ SO SÁNH HAI MẪU

**Nhịp 1 – Tần số khác tần số tương đối.**

Tần số tuyệt đối cho ta biết có bao nhiêu học sinh. Tần số tương đối cho biết phần của cả lớp thuộc một khoảng, bằng tần số lớp chia cho tổng bốn mươi. Chẳng hạn sáu chia bốn mươi bằng mười lăm phần trăm. Đây là cách chuẩn hóa để so sánh các lớp có sĩ số khác nhau mà không lấy số người nhiều hơn làm bằng chứng tỷ lệ cao hơn.

**Nhịp 2 – Biến bảng thành tỷ lệ.**

Bốn tần số tương đối lần lượt là mười lăm, bốn mươi lăm, ba mươi lăm và năm phần trăm. Chúng cộng lại đúng một trăm phần trăm. Khi đổi thành biểu đồ, ta có thể thể hiện theo tỷ lệ hoặc tần số nhưng phải ghi đơn vị trên trục. Phần lớn học sinh thuộc hai khoảng giữa, chứ không thể suy ra tất cả học sinh trong một lớp đều có cùng điểm.

**Nhịp 3 – So sánh hai lớp có sĩ số khác.**

Lớp thứ nhất có mười sáu trên bốn mươi học sinh đạt từ tám điểm, tức bốn mươi phần trăm. Một lớp giả lập thứ hai có hai mươi lăm trên năm mươi học sinh đạt từ tám điểm, tức năm mươi phần trăm. Nếu nhìn số tuyệt đối thì lớp thứ hai nhiều hơn chín học sinh. Muốn so sánh tỷ lệ học sinh đạt ngưỡng, ta dùng phần trăm, không dùng riêng số lượng.

**Nhịp 4 – Tần số tương đối tích lũy.**

Ta cũng có thể cộng dồn tỷ lệ, nhận được mười lăm, sáu mươi, chín mươi lăm và một trăm phần trăm. Ở mốc dưới tám điểm, sáu mươi phần trăm phù hợp với hai mươi bốn trên bốn mươi quan sát. Hai cách biểu diễn phải nhất quán vì đều xuất phát từ cùng bảng dữ liệu. Cảnh này giúp ta đọc ngưỡng từ một hình tích lũy mà không đếm từng chấm.


## Chương 05 – HISTOGRAM: DIỆN TÍCH MỚI LÀ ĐIỀU QUAN TRỌNG

**Nhịp 1 – Biểu đồ tần số theo khoảng.**

Với số liệu ghép nhóm, histogram đặt các khoảng liên tiếp trên trục hoành, không để khoảng trống tùy tiện giữa hai lớp kề nhau. Nếu các lớp rộng bằng nhau, ta có thể dùng tần số làm chiều cao và các cột có độ rộng đúng như khoảng. Chẳng hạn lớp từ sáu đến dưới tám cao hơn lớp từ mười đến dưới mười hai vì số quan sát nhiều hơn.

**Nhịp 2 – Diện tích cột biểu diễn tần số.**

Ta thử thay cách ghép nhóm để có những khoảng rộng không đều. Khi đó chiều cao không nên lấy thẳng tần số, bởi cột rộng tự nhiên có diện tích lớn hơn. Muốn diện tích biểu diễn số quan sát, chiều cao phải bằng tần số chia cho độ rộng lớp, gọi là mật độ tần số. Đây là điểm thường nhầm khi đem công thức của biểu đồ cột sang histogram.

**Nhịp 3 – Đọc histogram không đều.**

Khoảng sáu đến dưới bảy có tám điểm và rộng một đơn vị nên mật độ bằng tám. Khoảng bảy đến dưới chín có mười tám điểm nhưng rộng hai đơn vị, nên mật độ bằng chín. Hai cột này có chiều cao gần nhau, tuy tần số chênh mười. Kiểm tra bằng diện tích: tám nhân một bằng tám, chín nhân hai bằng mười tám.

**Nhịp 4 – Không đánh tráo tần số và mật độ.**

Trong cách chia không đều, bốn tần số lần lượt là sáu, tám, mười tám và tám. Độ rộng các lớp là hai, một, hai và hai; mật độ tương ứng ba, tám, chín và bốn. Nếu lấy diện tích từng cột bằng chiều rộng nhân chiều cao rồi cộng lại, ta được đúng bốn mươi. Biểu đồ nào thể hiện đúng thông tin phụ thuộc vào ý nghĩa chiều cao và diện tích của nó.


## Chương 06 – THÔNG TIN MẤT ĐI KHI GHÉP NHÓM

**Nhịp 1 – Ghép nhóm là một phép nén dữ liệu.**

Từ dữ liệu gốc, ta biết chính xác có tám học sinh đạt sáu và mười học sinh đạt bảy. Sau khi ghép thành một lớp từ sáu đến dưới tám, bảng chỉ còn số mười tám. Nếu ai đó chỉ đưa bảng ghép nhóm, ta không thể khôi phục được phân chia tám và mười. Dữ liệu đã được tóm tắt, nhưng một phần chi tiết đã mất.

**Nhịp 2 – Hai dữ liệu gốc, cùng một bảng.**

Hãy tưởng tượng dữ liệu A lấy các giá trị gần đầu trái trong từng lớp, còn dữ liệu B lấy các giá trị gần đầu phải, vẫn bảo đảm mỗi giá trị thuộc khoảng tương ứng. Hai bảng tần số ghép nhóm giống hệt nhau: sáu, mười tám, mười bốn, hai. Tuy nhiên trung bình của hai bộ dữ liệu có thể khác nhau. Chỉ biết bảng ghép nhóm không đủ để tính đúng trung bình gốc.

**Nhịp 3 – Ước lượng trung bình từ trung điểm.**

Một cách ước lượng số trung bình cho mẫu ghép nhóm là xem mọi giá trị trong lớp nằm tại trung điểm của lớp đó. Với bốn khoảng có trung điểm năm, bảy, chín, mười một, ta thu được trung bình xấp xỉ bảy phẩy sáu. Nhưng từ dữ liệu gốc, trung bình chính xác bằng bảy phẩy một. Hai con số khác nhau vì thay các quan sát bằng đại diện của lớp.

**Nhịp 4 – Không đánh đồng xấp xỉ với chính xác.**

Việc thay bằng trung điểm rất tiện khi ta chỉ có bảng ghép nhóm, nhưng nó tạo ra sai số. Đừng viết rằng trung bình chính xác của lớp học bằng bảy phẩy sáu nếu dữ liệu gốc cho biết bảy phẩy một. Cần ghi chú rằng đó là giá trị ước lượng từ bảng ghép nhóm. Ở tập sau, ta sẽ đi sâu vào các số đặc trưng này với sự thận trọng tương tự.


## Chương 07 – CÙNG MỘT DỮ LIỆU, NHIỀU CÁCH GHÉP NHÓM

**Nhịp 1 – Số lớp quyết định độ chi tiết.**

Nếu gộp cả bốn khoảng thành một khoảng từ bốn đến dưới mười hai, ta chỉ biết có bốn mươi quan sát trong vùng rộng ấy. Khi chia thành bốn lớp, ta nhìn được vùng tập trung ở sáu đến dưới tám. Nếu chia quá nhiều lớp, histogram có thể trở nên vụn vặt. Chọn cách ghép phù hợp với dữ liệu và mục tiêu, không có một con số lớp tốt nhất cho mọi tình huống.

**Nhịp 2 – Thay ranh giới sẽ thay bảng.**

Ta thử chia lại các khoảng thành từ bốn đến dưới sáu, sáu đến dưới bảy, bảy đến dưới chín và chín đến dưới mười một. Dù dữ liệu gốc giữ nguyên, tần số trở thành sáu, tám, mười tám, tám. Như vậy bảng ghép nhóm không chỉ phản ánh dữ liệu mà còn phụ thuộc cách đặt ranh giới lớp. Khi so sánh hai nhóm, nên dùng cách phân lớp tương thích.

**Nhịp 3 – Tránh gây hiểu nhầm bằng chiều rộng.**

Cảnh này đặt cạnh nhau biểu đồ theo tần số và biểu đồ theo mật độ của cùng các khoảng không đều. Nếu cứ giữ chiều cao bằng tần số, ta tạo ra diện tích không tương xứng với số quan sát. Khi dùng mật độ, mỗi đơn vị diện tích ứng với một quan sát theo đúng tỷ lệ vẽ. Đây là lý do phải đọc cả trục hoành lẫn chú thích trục tung.

**Nhịp 4 – Khi nào nên hoặc không nên ghép nhóm?.**

Ghép nhóm giúp bảng gọn, dễ nhận diện dạng phân bố và so sánh tổng quát. Tuy nhiên nếu bộ dữ liệu chỉ có vài chục điểm và cần tính chính xác số trung bình, tứ phân vị hoặc ngoại lệ, ta nên giữ lại dữ liệu ban đầu. Một nguyên tắc tốt là dùng biểu đồ để giao tiếp, nhưng lưu dữ liệu gốc để kiểm chứng. Thống kê tốt không chỉ là công thức đúng mà còn là trình bày trung thực.


## Chương 08 – BÀI TẬP TỔNG HỢP VÀ TƯ DUY PHÊ PHÁN

**Nhịp 1 – Bài toán tự làm với 20 quan sát.**

Bài cuối dùng bộ dữ liệu giả lập khác: hai mươi thời lượng luyện tập theo phút. Ta chia thành bốn lớp liên tiếp, từ hai đến dưới bốn, bốn đến dưới sáu, sáu đến dưới tám, và tám đến dưới mười. Trước khi xem bảng, hãy thử đếm thủ công hoặc trên giấy. Quy tắc ranh giới trái nhận, phải loại vẫn không thay đổi.

**Nhịp 2 – Lập bảng tần số.**

Lớp từ hai đến dưới bốn có năm quan sát, lớp bốn đến dưới sáu có bảy, lớp sáu đến dưới tám có sáu, lớp cuối có hai. Cộng lại được hai mươi. Hãy tự kiểm tra xem các giá trị bốn và sáu đã được đưa vào lớp bên phải hay chưa. Sai lầm thường gặp là tính trùng một giá trị ở ranh giới rồi vẫn làm đúng công thức chia phần trăm.

**Nhịp 3 – Tỷ lệ và tích lũy.**

Chia từng tần số cho hai mươi, ta có tỷ lệ hai mươi lăm, ba mươi lăm, ba mươi và mười phần trăm. Tần số tích lũy là năm, mười hai, mười tám và hai mươi. Từ bảng này, có mười hai quan sát dưới sáu phút; tám quan sát từ sáu phút trở lên. Hãy luôn nêu rõ dấu nghiêm ngặt khi phát biểu một ngưỡng.

**Nhịp 4 – Chốt lại phương pháp.**

Khi gặp một bài ghép nhóm, em hãy làm theo một chuỗi tư duy. Chọn ranh giới lớp rõ ràng và nhất quán. Phân mỗi quan sát vào đúng một lớp, đếm tần số rồi kiểm tổng. Tính tỷ lệ hay tần số tích lũy nếu đề yêu cầu. Khi vẽ histogram, chú ý độ rộng và mật độ. Cuối cùng, tự hỏi còn điều gì không thể khôi phục từ bảng đã ghép nhóm.

