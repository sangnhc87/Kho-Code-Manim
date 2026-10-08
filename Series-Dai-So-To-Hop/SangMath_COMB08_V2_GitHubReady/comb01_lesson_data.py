"""Source of truth: pedagogical narration, reveal states, timings for COMB01 v2.

40 separate narrated beats across eight conceptually distinct sections.
Each beat contains non-trivial spoken content and its visual reveal state.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Beat:
    section: str
    step: int
    heading: str
    lines: tuple[str, ...]
    takeaway: str
    narration: str
    formula: str = ""
    min_seconds: float = 18.2


def b(section, step, heading, lines, takeaway, narration, formula="", seconds=18.2):
    return Beat(section, step, heading, tuple(lines), takeaway, narration, formula, seconds)


BEATS = [
# 1. Create cognitive conflict: what is a single choice?
b('roads',0,'MỘT CHUYẾN ĐI', ['Từ A đến B có 2 tuyến xe buýt,', 'và 3 tuyến tàu khác nhau.', 'Chỉ được chọn đúng 1 tuyến.'], 'Dự đoán: có bao nhiêu cách?',
  'Hãy quan sát hai địa điểm A và B trên màn hình. Giữa hai địa điểm này có hai tuyến xe buýt và ba tuyến tàu khác nhau. Một người chỉ cần chọn đúng một tuyến để di chuyển từ A tới B. Theo em, ta có thể thực hiện chuyến đi đó bằng bao nhiêu cách khác nhau? Hãy thử dự đoán trước khi đếm.'),
b('roads',1,'NHẬN DIỆN LỰA CHỌN', ['Hai tuyến xe buýt là hai kết quả', 'khác nhau, dù cùng là xe buýt.', 'Ta chưa xét các tuyến tàu.'], 'Hai lựa chọn đầu tiên: Xe 1, Xe 2.',
  'Trước hết, ta chỉ xét phương tiện xe buýt. Có tuyến xe buýt thứ nhất và tuyến xe buýt thứ hai. Nếu chọn tuyến thứ nhất thì đó là một kết quả. Nếu chọn tuyến thứ hai thì đó là kết quả khác. Do vậy, trong nhóm xe buýt, chúng ta có đúng hai khả năng. Hãy theo dõi hai đường màu xanh đang được tô sáng.'),
b('roads',2,'CÒN MỘT NHÓM NỮA', ['Nhóm tàu có 3 tuyến độc lập:', 'Tàu 1, Tàu 2, Tàu 3.', 'Chọn một tuyến tàu bất kỳ.'], 'Ba lựa chọn còn lại không phải xe buýt.',
  'Bây giờ ta chuyển sang nhóm tàu. Trên hình lần lượt xuất hiện tàu thứ nhất, tàu thứ hai và tàu thứ ba. Ba tuyến này tạo ra ba cách lựa chọn. Cần chú ý rằng, khi hành khách đã chọn một tuyến tàu thì không đồng thời chọn thêm tuyến xe buýt. Đây là một công việc với những phương án thay thế cho nhau.'),
b('roads',3,'CHỈ CHỌN MỘT TUYẾN', ['Một kết quả hợp lệ là một tuyến,', 'không phải một cặp xe và tàu.', 'Hai nhóm phương án không trùng.'], 'Từ “hoặc” gợi ý phép cộng.',
  'Có bạn nghĩ rằng phải lấy hai nhân ba, vì bài toán xuất hiện hai nhóm. Nhưng như thế sẽ đếm các cặp gồm một xe buýt và một tàu. Đề bài không yêu cầu đi cả hai phương tiện. Mỗi lần chọn chỉ tạo ra một trong năm tuyến riêng biệt. Như vậy, ta cần gộp các khả năng của hai nhóm, chứ không phải ghép chúng thành từng cặp.'),
b('roads',4,'THỬ ĐẾM TRỰC TIẾP', ['Liệt kê: Xe 1, Xe 2;', 'Tàu 1, Tàu 2, Tàu 3.', 'Có đúng 5 kết quả khác nhau.'], '2 + 3 = 5 cách chọn.',
  'Để chắc chắn, ta có thể liệt kê trực tiếp các kết quả: xe một, xe hai, tàu một, tàu hai và tàu ba. Không có kết quả nào xuất hiện hai lần. Cũng không còn kết quả hợp lệ nào bị bỏ sót. Tổng số cách chọn do đó là hai cộng ba, bằng năm. Đây là hạt nhân của quy tắc cộng mà chúng ta chuẩn bị phát biểu.', 'sum5'),
# 2. explicitly classify
b('count',0,'PHÂN NHÓM KẾT QUẢ', ['Đặt X là nhóm tuyến xe buýt.', 'Đặt Y là nhóm tuyến tàu.', 'Mỗi nhóm được mô tả bằng thẻ.'], 'X và Y là hai tập hợp kết quả.',
  'Ta sẽ biểu diễn lời giải bằng hai nhóm thẻ để nhìn rõ bản chất. Gọi X là tập gồm hai tuyến xe buýt, và Y là tập gồm ba tuyến tàu. Mỗi thẻ biểu diễn chính xác một cách thực hiện chuyến đi. Việc chuyển từ đường vẽ sang thẻ giúp ta tập trung vào số lượng kết quả, không bị chi phối bởi hình dạng tuyến đường.'),
b('count',1,'ĐẾM NHÓM X', ['X = {Xe 1, Xe 2}.', 'Nhóm X có đúng 2 phần tử.', 'Không cần quan tâm thứ tự kể tên.'], 'Số cách của phương án X là 2.',
  'Trong tập X, ta lần lượt nhìn thấy thẻ xe một và xe hai. Có hai phần tử nên có hai cách chọn xe buýt. Thứ tự kể tên các thẻ không ảnh hưởng tới số cách, bởi ta đang lựa chọn một phương án, không phải sắp xếp các phương án. Con số hai phải xuất phát từ việc đếm các kết quả thực sự khác nhau.'),
b('count',2,'ĐẾM NHÓM Y', ['Y = {Tàu 1, Tàu 2, Tàu 3}.', 'Nhóm Y có đúng 3 phần tử.', 'Không có tuyến nào xuất hiện ở X.'], 'Số cách của phương án Y là 3.',
  'Tương tự, tập Y chứa ba thẻ tàu. Ta có ba cách chọn tàu. Bây giờ hãy quan sát đồng thời cả hai tập. Không có thẻ nào vừa nằm ở nhóm xe buýt vừa nằm ở nhóm tàu. Nói bằng ngôn ngữ tập hợp, hai nhóm không có phần tử chung. Chính đặc điểm này bảo đảm phép cộng sẽ không tính cùng một kết quả hai lần.'),
b('count',3,'HỢP HAI NHÓM', ['Kết quả của bài toán là X ∪ Y.', 'Mỗi thẻ thuộc đúng một nhóm.', 'Lần lượt đếm 2 thẻ và 3 thẻ.'], 'Tổng: 2 + 3.',
  'Vì đề bài cho phép đi bằng xe buýt hoặc tàu nên tập tất cả kết quả hợp lệ chính là hợp của X và Y. Chúng ta đếm hai phần tử nhóm X, rồi tiếp tục đếm ba phần tử nhóm Y. Hai lượt đếm không đụng tới cùng một kết quả. Số phần tử của tập hợp bằng tổng số phần tử của hai nhóm.'),
b('count',4,'KẾT LUẬN BÀI MỞ ĐẦU', ['Nhóm xe buýt: 2 cách.', 'Nhóm tàu: 3 cách.', 'Hai nhóm không giao nhau.'], 'Kết luận: 5 cách.',
  'Kết luận của bài mở đầu là năm cách. Ta nhắc lại lý do, chứ không chỉ nhắc lại đáp số: hành khách chọn đúng một tuyến, mọi tuyến đã được liệt kê, và không có tuyến nào bị đếm hai lần. Nếu thay số tuyến của từng nhóm bằng những số khác, phương pháp cộng vẫn có thể sử dụng, miễn là hai nhóm lựa chọn không trùng nhau.', 'sum5'),
# 3. formulate
b('rule',0,'KHÁI QUÁT HAI PHƯƠNG ÁN', ['Một công việc có thể làm theo A', 'hoặc theo B.', 'A có m cách, B có n cách.'], 'Hỏi có bao nhiêu kết quả tất cả?',
  'Bây giờ ta rời khỏi ví dụ xe buýt và tàu để phát biểu quy tắc ở dạng tổng quát. Giả sử một công việc có thể thực hiện theo phương án A hoặc theo phương án B. Phương án A có m kết quả khác nhau, còn phương án B có n kết quả khác nhau. Câu hỏi quan trọng không chỉ là m và n bằng bao nhiêu, mà là hai nhóm có giao nhau hay không.'),
b('rule',1,'ĐIỀU KIỆN QUAN TRỌNG', ['Không kết quả nào của A', 'đồng thời thuộc B.', 'Tức A ∩ B = ∅.'], 'Không giao nhau → không đếm trùng.',
  'Nếu một kết quả không thể đồng thời được tính trong cả nhóm A và nhóm B, hai tập hợp kết quả là rời nhau. Khi đó, việc đếm hết A rồi đếm hết B không làm trùng bất kỳ kết quả nào. Ta có thể dùng công thức đơn giản m cộng n. Điều kiện không trùng nhau quan trọng như bản thân phép tính.'),
b('rule',2,'QUY TẮC CỘNG', ['Có m cách làm theo A;', 'có n cách làm theo B;', 'hai cách phân nhóm không trùng.'], 'Tổng số cách là m + n.',
  'Ta có quy tắc cộng: nếu một công việc có thể thực hiện theo một trong hai phương án không trùng nhau, phương án thứ nhất có m cách và phương án thứ hai có n cách, thì có m cộng n cách thực hiện công việc. Trước khi áp dụng, phải xác định rõ một kết quả cụ thể là gì. Khi kết quả đã được xác định, việc kiểm tra trùng lặp sẽ chính xác.', 'sum_general'),
b('rule',3,'MỞ RỘNG NHIỀU NHÓM', ['Có thể có 3, 4 hoặc nhiều nhóm.', 'Mỗi kết quả thuộc đúng một nhóm.', 'Khi đó cộng số cách từng nhóm.'], 'm₁ + m₂ + … + mᵣ.',
  'Quy tắc cộng không chỉ dành cho đúng hai phương án. Nếu có ba phương án không trùng nhau, ta cộng số cách của cả ba. Nếu có nhiều nhóm hơn cũng làm như vậy. Tuy nhiên, không được tự động cộng mọi con số chỉ vì bài toán có nhiều trường hợp. Các trường hợp cần được phân chia đầy đủ và không chồng lấn nhau.'),
b('rule',4,'KIỂM TRA TRƯỚC KHI CỘNG', ['1. Đã kể hết mọi trường hợp?', '2. Các trường hợp có trùng?', '3. Mỗi kết quả được tính một lần?'], 'Hai câu hỏi: đủ và không trùng.',
  'Tôi gợi ý ba câu hỏi để kiểm tra mọi bài đếm bằng quy tắc cộng. Thứ nhất, các nhóm đã bao phủ tất cả kết quả hợp lệ chưa? Thứ hai, có kết quả nào nằm ở hai nhóm hay không? Thứ ba, một kết quả đã được tính đúng một lần chưa? Chỉ cần trả lời rõ ba câu hỏi này, học sinh sẽ tránh được rất nhiều sai lầm trong đại số tổ hợp.'),
# 4. books
b('books',0,'VÍ DỤ 2 · CHỌN SÁCH', ['Có 4 cuốn Toán khác nhau.', 'Có 3 cuốn Vật lí khác nhau.', 'Chọn đúng 1 cuốn để đọc.'], 'Dự đoán số cách chọn sách.',
  'Ta chuyển sang một ví dụ gần gũi hơn. Trên giá có bốn cuốn sách Toán khác nhau và ba cuốn sách Vật lí khác nhau. Một học sinh chỉ lấy đúng một cuốn để đọc. Em hãy nhìn bảy cuốn sách trên màn hình và dự đoán số cách chọn. Điểm mấu chốt là mỗi cuốn sách được xem là một đối tượng riêng biệt.'),
b('books',1,'PHƯƠNG ÁN THỨ NHẤT', ['Chọn sách Toán.', 'Có T1, T2, T3, T4.', 'Tất cả 4 lựa chọn khác nhau.'], 'Nhóm Toán: 4 cách.',
  'Trước tiên, ta xét phương án chọn sách Toán. Bốn cuốn lần lượt được ký hiệu T một, T hai, T ba và T bốn. Vì chúng là bốn cuốn khác nhau, mỗi cuốn tạo ra một cách chọn. Vậy phương án lấy sách Toán có bốn cách. Hãy lưu ý chữ Toán ở đây chỉ nói về loại sách, không làm bốn cuốn trở thành cùng một kết quả.'),
b('books',2,'PHƯƠNG ÁN THỨ HAI', ['Chọn sách Vật lí.', 'Có L1, L2, L3.', 'Tất cả 3 lựa chọn khác nhau.'], 'Nhóm Vật lí: 3 cách.',
  'Tiếp theo, học sinh cũng có thể chọn một cuốn Vật lí. Có ba cuốn L một, L hai và L ba, tương ứng ba cách. Không một cuốn nào đồng thời được xếp vào loại Toán và loại Vật lí trong bài toán này. Vì thế, hai nhóm sách là hai nhóm lựa chọn rời nhau. Ta đã đủ dữ kiện để áp dụng quy tắc cộng.'),
b('books',3,'TỔNG HỢP HAI NHÓM', ['Chỉ lấy 1 cuốn Toán hoặc Vật lí.', 'Nhóm Toán có 4 cách;', 'nhóm Vật lí có 3 cách.'], '4 + 3 = 7 cách.',
  'Vì chỉ lấy đúng một cuốn, ta không ghép một cuốn Toán với một cuốn Vật lí thành một cặp. Nếu làm như vậy, ta đang giải một bài toán khác. Ở đây, tập kết quả là tất cả bảy cuốn sách được trưng bày. Cộng số cách của hai nhóm ta được bốn cộng ba bằng bảy cách.', 'sum7'),
b('books',4,'THAY ĐỔI YÊU CẦU', ['Nếu chọn 1 Toán và 1 Vật lí?', 'Đó là chọn hai cuốn cùng lúc.', 'Không còn là bài toán vừa giải.'], 'Nhận ra sự khác biệt “hoặc” và “và”.',
  'Hãy kiểm tra sự hiểu bài bằng một thay đổi rất nhỏ trong đề: bây giờ chọn một cuốn Toán và một cuốn Vật lí. Kết quả không còn là một cuốn sách nữa mà là một cặp gồm hai cuốn. Ta không được dùng đáp số bảy của bài vừa rồi. Sự khác biệt giữa từ hoặc và từ và chính là cầu nối sang quy tắc nhân ở video tiếp theo.'),
# 5. overlap
b('overlap',0,'THỬ THÁCH · CÓ TRÙNG KHÔNG?', ['Xét các số nguyên từ 1 đến 12.', 'Đếm số chia hết cho 2 hoặc 3.', 'Có thể cộng ngay 6 và 4?'], 'Cần kiểm tra xem hai nhóm có giao nhau.',
  'Bây giờ là thử thách quan trọng nhất của tập này. Xét các số nguyên từ một đến mười hai. Ta cần đếm những số chia hết cho hai hoặc chia hết cho ba. Từ hoặc khiến ta nghĩ tới quy tắc cộng, nhưng liệu hai nhóm có rời nhau không? Hãy tạm dừng vài giây và thử liệt kê các số thỏa mãn từng điều kiện.'),
b('overlap',1,'CÁC SỐ CHIA HẾT CHO 2', ['A = {2, 4, 6, 8, 10, 12}.', 'Có 6 số chẵn.', 'Tạm đánh dấu màu cyan.'], 'Nhóm A có 6 phần tử.',
  'Các số chia hết cho hai trong phạm vi một đến mười hai là hai, bốn, sáu, tám, mười và mười hai. Tổng cộng có sáu số. Ta tô chúng bằng màu xanh. Số sáu ở đây hoàn toàn chính xác, nhưng chỉ là số phần tử của nhóm A. Chúng ta chưa thể cộng với nhóm kia cho đến khi kiểm tra những phần tử chung.'),
b('overlap',2,'CÁC SỐ CHIA HẾT CHO 3', ['B = {3, 6, 9, 12}.', 'Có 4 số là bội của 3.', 'Một số đã xuất hiện ở A!'], 'Chú ý các số 6 và 12.',
  'Nhóm thứ hai gồm các số chia hết cho ba, đó là ba, sáu, chín và mười hai. Như vậy nhóm B có bốn số. Khi đặt cạnh danh sách số chẵn, ta dễ dàng nhận thấy số sáu và số mười hai xuất hiện trong cả hai danh sách. Nếu cộng sáu với bốn mà không điều chỉnh, hai số này sẽ được tính hai lần.'),
b('overlap',3,'PHÁT HIỆN PHẦN GIAO', ['A ∩ B = {6, 12}.', 'Có 2 số thuộc cả hai nhóm.', 'Phải loại phần bị đếm thêm.'], '6 + 4 đã đếm trùng 2 lần.',
  'Hãy quan sát hai ô số sáu và mười hai chuyển sang màu đỏ. Màu đỏ không có nghĩa chúng không được chọn; chúng vẫn là kết quả hợp lệ. Màu đỏ báo rằng mỗi số đã bị tính thêm một lần khi cộng hai lượng sáu và bốn. Muốn mỗi kết quả chỉ được tính đúng một lần, ta phải trừ đi đúng số phần tử chung là hai.'),
b('overlap',4,'SỬA PHÉP ĐẾM', ['Lấy tổng hai nhóm: 6 + 4.', 'Trừ 2 số chung: 6 và 12.', 'Kết quả: 6 + 4 − 2 = 8.'], 'Có 8 số thỏa mãn.',
  'Phép đếm đúng là sáu cộng bốn trừ hai, bằng tám. Nếu liệt kê trực tiếp, ta nhận được hai, ba, bốn, sáu, tám, chín, mười và mười hai, đúng tám số. Việc trừ phần giao không phải mẹo ghi nhớ tùy ý mà là cách sửa lại số lần mỗi kết quả được tính.', 'overlap8'),
b('overlap',5,'CÔNG THỨC HAI TẬP HỢP', ['Khi hai nhóm có giao nhau,', 'cộng số phần tử từng nhóm,', 'rồi trừ số phần tử chung.'], '|A ∪ B| = |A| + |B| − |A ∩ B|.',
  'Qua hình ảnh hai nhóm có phần chung, ta đi tới công thức đếm phần tử của hợp hai tập hợp. Số phần tử của hợp bằng số phần tử của tập thứ nhất cộng số phần tử tập thứ hai rồi trừ số phần tử giao. Quy tắc cộng cơ bản chính là trường hợp đặc biệt khi phần giao rỗng, nghĩa là số phần tử chung bằng không.', 'set_union'),
b('overlap',6,'ĐIỀU CẦN NHỚ', ['Dấu “hoặc” chưa đủ để cộng.', 'Luôn kiểm tra hai nhóm có trùng.', 'Nếu trùng, phải điều chỉnh.'], 'Đủ trường hợp — không đếm trùng.',
  'Đây là một cảnh báo quan trọng: không phải gặp chữ hoặc là lấy ngay hai con số cộng lại. Trước khi làm phép tính, ta phải xác định tập các kết quả, kiểm tra phần giao và quyết định công thức thích hợp. Những bài đếm khó ở các tập sau thường bắt đầu từ chính thói quen phân tích điều kiện này. Hãy xem thêm một trường hợp mà hai nhóm thực sự rời nhau.'),
# 6. disjoint numeric example
b('distinct',0,'VÍ DỤ 3 · CÁC NHÓM RỜI NHAU', ['Chọn số nguyên từ 1 đến 20.', 'Yêu cầu: số lẻ hoặc', 'số chia hết cho 4.'], 'Lần này có phần giao không?',
  'Xét các số nguyên từ một đến hai mươi. Hỏi có bao nhiêu số lẻ hoặc chia hết cho bốn? Hãy phân tích hai điều kiện: một số lẻ không chia hết cho hai, trong khi số chia hết cho bốn chắc chắn là số chẵn. Do đó không thể có số nào cùng lúc thỏa cả hai điều kiện. Đây là ví dụ lý tưởng để dùng quy tắc cộng.'),
b('distinct',1,'ĐẾM CÁC SỐ LẺ', ['Các số lẻ: 1, 3, 5, …, 19.', 'Có 10 số lẻ.', 'Đánh dấu chúng bằng màu cyan.'], 'Nhóm thứ nhất: 10 cách.',
  'Trong dãy từ một đến hai mươi có mười số lẻ, bắt đầu từ một và kết thúc ở mười chín. Trên lưới số, các ô lẻ được tô sáng. Dù nằm xen kẽ các số chẵn, chúng vẫn tạo thành một nhóm hợp lệ vì cùng thỏa điều kiện đầu tiên. Tổng số phần tử của nhóm này là mười.'),
b('distinct',2,'ĐẾM CÁC BỘI CỦA 4', ['Các số: 4, 8, 12, 16, 20.', 'Có đúng 5 số.', 'Không số nào trong nhóm số lẻ.'], 'Nhóm thứ hai: 5 cách.',
  'Các số chia hết cho bốn là bốn, tám, mười hai, mười sáu và hai mươi. Có tất cả năm số. Vì mọi số này đều chẵn, chúng không thể thuộc danh sách mười số lẻ vừa rồi. Như vậy, hai nhóm đã được kiểm tra là không trùng. Ta có thể đếm hết nhóm đầu rồi đếm tiếp nhóm thứ hai.'),
b('distinct',3,'ÁP DỤNG QUY TẮC CỘNG', ['Nhóm số lẻ: 10 số.', 'Nhóm bội của 4: 5 số.', 'Hai nhóm không giao nhau.'], '10 + 5 = 15 số.',
  'Kết quả là mười cộng năm bằng mười lăm số. Hãy so sánh với bài chia hết cho hai hoặc ba lúc trước. Ở ví dụ này, phép cộng trực tiếp hoàn toàn đúng vì phần giao là rỗng. Trong bài trước, phải trừ đi hai phần tử chung. Cách tính khác nhau bắt nguồn từ quan hệ giữa các nhóm, chứ không phải từ cách dùng từ trong câu hỏi.', 'sum15'),
b('distinct',4,'BÀI HỌC TỪ HAI VÍ DỤ', ['Hai nhóm rời nhau: cộng ngay.', 'Hai nhóm giao nhau: trừ phần chung.', 'Kiểm tra điều kiện trước công thức.'], 'Không học công thức tách khỏi mô hình.',
  'Qua hai bài toán số học, ta đã thấy cùng một yêu cầu kiểu hoặc có thể dẫn tới hai phép đếm khác nhau. Thay vì học thuộc một mẹo, em hãy vẽ hoặc tưởng tượng hai nhóm kết quả. Nếu hai nhóm không có phần giao, cộng trực tiếp. Nếu có phần giao, phải tránh đếm lặp. Đây là nền tảng tư duy tổ hợp rất quan trọng.'),
# 7. and/or
b('compare',0,'“HOẶC” VÀ “VÀ” KHÁC NHAU', ['Có 3 áo và 2 chiếc mũ.', 'Câu hỏi A: chọn 1 áo hoặc 1 mũ.', 'Câu hỏi B: chọn 1 áo và 1 mũ.'], 'Hai bài toán — hai loại kết quả.',
  'Để tránh nhầm lẫn giữa hai quy tắc đếm đầu tiên, ta xét ba chiếc áo khác nhau và hai chiếc mũ khác nhau. Nếu chỉ chọn một món đồ, có thể chọn áo hoặc mũ. Nhưng nếu yêu cầu một bộ gồm một áo và một mũ, ta phải tạo ra các cặp. Hai bài toán dùng cùng dữ kiện nhưng có kết quả hoàn toàn khác nhau.'),
b('compare',1,'TRƯỜNG HỢP “HOẶC”', ['Chọn đúng 1 món đồ.', 'Ba áo hoặc hai mũ.', 'Các món đồ là riêng biệt.'], '3 + 2 = 5 lựa chọn.',
  'Khi đề yêu cầu một áo hoặc một mũ, một kết quả chỉ là một món đồ. Các kết quả là áo một, áo hai, áo ba, mũ một và mũ hai. Tất cả có năm món riêng biệt. Vì các nhóm không trùng nhau nên số cách chọn là ba cộng hai bằng năm. Đây là bài toán dùng quy tắc cộng mà ta vừa học.', 'sum5compare'),
b('compare',2,'TRƯỜNG HỢP “VÀ”', ['Chọn 1 áo đồng thời với 1 mũ.', 'Mỗi áo ghép được với 2 mũ.', 'Có 6 cặp trang phục.'], '3 × 2 = 6 lựa chọn.',
  'Ngược lại, khi đề yêu cầu một áo và một mũ, mỗi kết quả gồm hai món đồ. Áo thứ nhất ghép với hai mũ tạo hai cặp; áo thứ hai cũng vậy, và áo thứ ba cũng vậy. Tổng cộng có sáu cặp. Đó là cấu trúc của quy tắc nhân mà chúng ta sẽ khám phá kỹ ở tập kế tiếp. Ở đây mục tiêu là phân biệt đúng đối tượng được đếm.', 'product6'),
b('compare',3,'KHÔNG ĐOÁN THEO TỪ KHÓA', ['Đầu tiên hỏi: một kết quả là gì?', 'Một món đồ hay một cặp đồ?', 'Sau đó mới chọn phép đếm.'], 'Xác định kết quả trước phép tính.',
  'Tuy chữ hoặc và chữ và gợi ý khá nhiều, ta không nên chỉ học thuộc dấu hiệu ngôn ngữ. Câu hỏi sâu hơn là: một kết quả hợp lệ cụ thể trông như thế nào? Nếu là một món đồ, ta đếm từng món. Nếu là một bộ hai món, ta đếm từng cặp. Khi làm đúng bước này, việc chọn quy tắc cộng hay nhân sẽ trở nên tự nhiên hơn.'),
b('compare',4,'TỔNG KẾT PHÂN BIỆT', ['Lựa chọn thay thế, không trùng: cộng.', 'Các bước ghép lựa chọn: nhân.', 'Tập 02 sẽ giải thích quy tắc nhân.'], 'Học bản chất, không học máy móc.',
  'Chúng ta đã hoàn thành sự phân biệt cơ bản giữa lựa chọn thay thế và lựa chọn phối hợp. Quy tắc cộng dùng để gộp các nhóm kết quả không trùng nhau. Quy tắc nhân sẽ xuất hiện khi kết quả được tạo qua nhiều bước kết hợp. Video kế tiếp sẽ bắt đầu từ những bộ trang phục, sơ đồ cây và quá trình ghép lựa chọn theo từng bước.'),
# 8. assess
b('quiz',0,'TỰ KIỂM TRA · CÂU 1', ['Có 5 phần quà loại A khác nhau.', 'Có 2 phần quà loại B khác nhau.', 'Chỉ chọn đúng 1 phần quà.'], 'Hãy tạm dừng để tính số cách.',
  'Trước khi kết thúc, em hãy làm hai câu tự kiểm tra. Câu thứ nhất, có năm phần quà loại A khác nhau và hai phần quà loại B khác nhau. Chọn đúng một phần quà. Em hãy tạm dừng video, viết tập kết quả nếu cần, rồi quyết định nên dùng quy tắc nào. Đừng chỉ ghi đáp số: hãy tự giải thích vì sao không đếm trùng.'),
b('quiz',1,'GIẢI CÂU 1', ['Hai nhóm quà khác loại,', 'không có phần tử chung.', 'Áp dụng quy tắc cộng.'], '5 + 2 = 7 cách.',
  'Lời giải câu một: có năm cách chọn một phần quà A và hai cách chọn một phần quà B. Vì một phần quà không thể vừa là phần quà A vừa là phần quà B trong đề này, các nhóm rời nhau. Chọn đúng một phần quà nghĩa là gộp hai nhóm kết quả. Ta được năm cộng hai bằng bảy cách.', 'quiz7'),
b('quiz',2,'TỰ KIỂM TRA · CÂU 2', ['Từ 1 đến 15, đếm các số', 'chia hết cho 3 hoặc chia hết cho 5.', 'Có được cộng 5 với 3 không?'], 'Tìm xem có số nào thỏa cả hai.',
  'Câu thứ hai khó hơn một chút. Từ một đến mười lăm, có bao nhiêu số chia hết cho ba hoặc chia hết cho năm? Các số chia hết cho ba có năm số, còn chia hết cho năm có ba số. Nếu cộng ngay ta được tám. Nhưng em hãy thử kiểm tra xem có số nào thỏa mãn đồng thời cả hai điều kiện hay không.'),
b('quiz',3,'GIẢI CÂU 2', ['Bội của 3: 5 số; bội của 5: 3.', 'Số 15 thuộc cả hai nhóm.', 'Phải trừ đúng 1 lần bị trùng.'], '5 + 3 − 1 = 7 số.',
  'Trong các số từ một tới mười lăm, số mười lăm vừa chia hết cho ba vừa chia hết cho năm. Đó là phần giao duy nhất. Khi cộng năm với ba, số mười lăm đã bị tính hai lần. Trừ bớt một lần, chúng ta được năm cộng ba trừ một bằng bảy số. Đây là lý do luôn cần kiểm tra giao nhau trước khi áp dụng phép cộng.', 'quiz7overlap'),
b('quiz',4,'KẾT THÚC · COMB01', ['Quy tắc cộng: gộp các phương án.', 'Đếm đủ, không đếm trùng.', 'COMB02: khám phá quy tắc nhân.'], 'Hiểu đối tượng được đếm trước.',
  'Hãy giữ lại ba câu hỏi cốt lõi sau bài học này. Một kết quả hợp lệ là gì? Ta đã kể hết các khả năng chưa? Và có khả năng nào bị tính hai lần không? Quy tắc cộng sẽ trở nên đơn giản khi ta trả lời được ba câu hỏi đó. Ở video tiếp theo, chúng ta sẽ học cách đếm các kết quả được tạo thành qua nhiều bước liên tiếp. Hẹn gặp lại em trong bài quy tắc nhân.', seconds=21.0),
]

CHAPTER_LABELS = {
    'roads': '01  ĐẶT VẤN ĐỀ', 'count': '02  PHÂN NHÓM',
    'rule': '03  KHÁI QUÁT', 'books': '04  VẬN DỤNG 1',
    'overlap': '05  ĐẾM TRÙNG', 'distinct': '06  VẬN DỤNG 2',
    'compare': '07  PHÂN BIỆT', 'quiz': '08  CỦNG CỐ',
}

FORMULAS = {
    'sum5': '2 + 3 = 5', 'sum_general': 'm + n',
    'sum7': '4 + 3 = 7', 'overlap8': '6 + 4 - 2 = 8',
    'set_union': '"|A ∪ B| = |A| + |B| − |A ∩ B|"',
    'sum15': '10 + 5 = 15', 'sum5compare': '3 + 2 = 5',
    'product6': '3 times 2 = 6', 'quiz7': '5 + 2 = 7',
    'quiz7overlap': '5 + 3 - 1 = 7',
}


def spoken_text(beat, limit_words=58):
    """Concise, sentence-complete voiceover, without cutting a thought mid-sentence.

    The unabridged narration is retained for teacher adaptation in the beat data.
    """
    import re
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-ZÀ-Ỹ])', beat.narration)
    selected = []
    count = 0
    for sentence in sentences:
        length = len(sentence.split())
        if selected and count + length > limit_words:
            break
        selected.append(sentence)
        count += length
    return ' '.join(selected)
