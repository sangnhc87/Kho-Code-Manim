"""Single source of truth for COMB02 V2 pedagogy, math, pacing and Typst.

Keep each spoken beat complete: TTS, teacher script, frame and QA are generated
from the SAME list. No arbitrary trimming of sentences at render time.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Beat:
    section: str
    state: int
    heading: str
    lines: tuple[str, ...]
    takeaway: str
    narration: str
    formula: str = ""
    min_seconds: float = 17.5
    focus: str = ""


def b(section, state, heading, lines, takeaway, narration, formula="", seconds=17.5, focus=""):
    assert 2 <= len(lines) <= 4
    return Beat(section, state, heading, tuple(lines), takeaway, narration, formula, seconds, focus)

CHAPTER_LABELS = {
    'outfit':'01  TÌNH HUỐNG',
    'grid':'02  LIỆT KÊ CÓ HỆ THỐNG',
    'tree':'03  SƠ ĐỒ CÂY',
    'general':'04  QUY TẮC NHÂN',
    'hat':'05  BA CÔNG ĐOẠN',
    'forbidden':'06  ĐIỀU KIỆN CẤM',
    'uneven':'07  SỐ NHÁNH THAY ĐỔI',
    'quiz':'08  LUYỆN TẬP VÀ TỔNG KẾT',
}

BEATS = [
# A. Why multiplication is needed, rather than merely spotting 'and'.
b('outfit',0,'MỘT BỘ TRANG PHỤC',['Có 3 chiếc áo phân biệt.','Có 2 chiếc quần phân biệt.','Chọn 1 áo VÀ 1 quần.'],'Một kết quả là một bộ áo–quần.',
  'Trước hết hãy quan sát ba chiếc áo và hai chiếc quần trên hình. Mỗi chiếc đều được phân biệt bằng một nhãn riêng. Công việc chúng ta phải thực hiện không phải chỉ chọn một món đồ. Ta cần chọn một áo và đồng thời chọn một quần để tạo thành một bộ trang phục.'),
b('outfit',1,'ĐẾM ĐÚNG ĐỐI TƯỢNG',['A1, A2, A3 là ba chiếc áo.','Q1, Q2 là hai chiếc quần.','Một bộ được ký hiệu (Ai, Qj).'],'Chỉ khi đủ hai món mới có một bộ.',
  'Một bộ trang phục được xác định bởi cặp gồm nhãn áo và nhãn quần. Chẳng hạn, áo một đi cùng quần một tạo thành một kết quả. Áo một đi cùng quần hai tạo thành một kết quả khác. Ta cần xác định đúng đối tượng đang được đếm trước khi nghĩ đến công thức.'),
b('outfit',2,'CỐ ĐỊNH ÁO THỨ NHẤT',['Giữ áo A1.','Ghép với Q1 hoặc Q2.','Thu được 2 bộ khác nhau.'],'A1 tạo 2 kết quả.',
  'Hãy tạm cố định chiếc áo thứ nhất. Ta có thể chọn quần một, hoặc quần hai. Vì hai chiếc quần khác nhau, hai bộ nhận được cũng khác nhau. Như vậy, chỉ riêng lựa chọn áo một đã sinh ra hai kết quả. Các bộ sẽ xuất hiện lần lượt ở phần hình.'),
b('outfit',3,'CHUYỂN SANG ÁO THỨ HAI',['Giữ áo A2.','Vẫn có Q1 và Q2.','Thêm đúng 2 bộ mới.'],'A2 cũng tạo 2 kết quả.',
  'Đổi sang áo thứ hai, ta vẫn có cả hai chiếc quần để ghép. Do đó áo hai sinh ra thêm hai bộ trang phục. Không bộ nào trùng với các bộ của áo một, bởi nhãn áo đã khác. Đây là lý do phép đếm theo từng áo có thể thực hiện một cách chắc chắn.'),
b('outfit',4,'ÁO THỨ BA VÀ DỰ ĐOÁN',['Giữ áo A3.','Vẫn ghép được với 2 quần.','Tổng cộng có 3 nhóm, mỗi nhóm 2.'],'Dự đoán tổng số bộ.',
  'Tương tự, áo thứ ba tạo ra hai bộ nữa. Em hãy nhìn ba nhóm kết quả, mỗi nhóm có đúng hai bộ và các nhóm không trùng nhau. Nếu cộng hai cộng hai cộng hai, ta được sáu. Có cách nào diễn đạt gọn hơn phép cộng lặp lại này không?'),
b('outfit',5,'KẾT QUẢ ĐẦU TIÊN',['3 lựa chọn áo.','Mỗi áo ứng với 2 lựa chọn quần.','Vậy có 3 × 2 = 6 bộ.'],'Không phải 3 + 2 = 5.',
  'Ta có ba cách chọn áo; với mỗi cách chọn áo, lại có hai cách chọn quần. Vì vậy số bộ bằng ba nhân hai, bằng sáu. Nếu lấy ba cộng hai, ta chỉ đang đếm số món đồ, không phải số bộ áo quần. Sự khác biệt này rất quan trọng.', 'p6'),
# B. Rectangular product set and one-to-one count.
b('grid',0,'LẬP BẢNG TẤT CẢ CÁC BỘ',['Mỗi hàng ứng với một áo.','Mỗi cột ứng với một quần.','Một ô biểu diễn đúng một bộ.'],'Bảng 3 hàng × 2 cột.',
  'Để không bỏ sót hoặc đếm trùng, chúng ta chuyển các bộ áo quần thành một bảng hình chữ nhật. Ba hàng tương ứng ba chiếc áo, hai cột tương ứng hai chiếc quần. Mỗi ô được xác định duy nhất bởi một hàng và một cột, tức là duy nhất một bộ.'),
b('grid',1,'ĐẾM HÀNG A1',['Hàng đầu gồm (A1,Q1).','Và bộ (A1,Q2).','Hàng thứ nhất có 2 ô.'],'Mỗi áo tương ứng 2 bộ.',
  'Hàng đầu tiên có hai ô: áo một với quần một và áo một với quần hai. Không có lựa chọn quần thứ ba trong bài toán. Cách xếp theo hàng giúp ta nhìn thấy rõ số lựa chọn tiếp theo khi đã xác định lựa chọn ban đầu.'),
b('grid',2,'ĐẾM HÀNG A2',['Hàng thứ hai có 2 ô.','Hai ô khác hàng A1.','Tổng sau hai hàng là 4.'],'2 + 2 = 4.',
  'Hàng thứ hai cũng có hai ô, nhưng chúng là những bộ có áo hai, nên không trùng với hàng trước. Đến lúc này đã có bốn bộ khác nhau. Từng ô trong bảng đều đại diện cho một kết quả hợp lệ của bài toán.'),
b('grid',3,'ĐẾM HÀNG A3',['Hàng thứ ba thêm 2 ô.','Bảng đã lấp đủ 6 ô.','Không thiếu, không trùng.'],'2 + 2 + 2 = 6.',
  'Khi điền hàng thứ ba, cả sáu ô đã xuất hiện. Mọi bộ hợp lệ phải nằm trong đúng một ô, vì mỗi bộ có một nhãn áo và một nhãn quần. Cách lập bảng đã chứng minh kết quả, chứ không chỉ minh họa đáp số. Ta thật sự biết rằng không thiếu và không đếm trùng.', 'sum222'),
b('grid',4,'CỘNG LẶP LẠI THÀNH NHÂN',['Có ba hàng bằng nhau.','Mỗi hàng có hai ô.','3 × 2 = 6 ô.'],'Quy tắc nhân rút gọn phép cộng.',
  'Cộng hai ba lần chính là lấy ba nhân hai. Mỗi hàng có cùng số ô, nên ta có thể thay một phép cộng dài bằng một phép nhân. Hình chữ nhật giúp ta ghi nhớ không phải vì áo và quần đứng cạnh nhau, mà vì từng lựa chọn đầu tạo ra số lựa chọn tiếp theo bằng nhau.', 'p6'),
# C. branching tree
b('tree',0,'CÂY LỰA CHỌN HAI TẦNG',['Tầng 1: chọn áo.','Tầng 2: chọn quần.','Mỗi đường từ gốc đến lá là 1 bộ.'],'Sơ đồ cây biểu diễn quá trình chọn.',
  'Bây giờ ta biểu diễn cùng bài toán bằng sơ đồ cây. Từ gốc, ba nhánh đầu tiên tương ứng ba cách chọn áo. Ở bước tiếp theo, từ mỗi nhánh áo lại có những lựa chọn quần. Một đường đi hoàn chỉnh từ gốc tới lá tương ứng với một bộ trang phục.'),
b('tree',1,'BA NHÁNH ÁO',['Từ gốc có A1, A2, A3.','Mỗi nhánh là một lựa chọn đầu.','Chưa tạo bộ vì thiếu quần.'],'Đếm một công việc theo hai bước.',
  'Ta chỉ vẽ tầng thứ nhất. Có ba nhánh, nhưng hiện tại ta mới chọn được áo, chưa hoàn thành công việc. Đây là điểm khác với quy tắc cộng. Trong quy tắc cộng ở video trước, ta chọn một phương án là hoàn thành. Còn ở đây phải đi tiếp sang bước chọn quần.'),
b('tree',2,'MỞ HAI NHÁNH TỪ A1',['A1 → Q1.','A1 → Q2.','A1 sinh ra 2 lá.'],'Mỗi lá là một kết quả hoàn chỉnh.',
  'Từ áo một, cây tách ra hai nhánh quần. Hai lá ở cuối lần lượt biểu diễn cặp áo một quần một và áo một quần hai. Chỉ những điểm cuối của đường đi đầy đủ mới được đếm là kết quả. Các nhánh áo đứng riêng không được đếm thêm lần nữa.'),
b('tree',3,'MỞ NHÁNH TỪ A2',['A2 → Q1 và Q2.','Số lá tăng từ 2 lên 4.','Không có lá nào trùng nhau.'],'Mỗi nhánh áo thêm 2 lá.',
  'Từ áo hai lại mở đúng hai nhánh quần. Lúc này sơ đồ có bốn lá. Dù nhãn quần lặp lại, kết quả vẫn khác, bởi đường đi có nhãn áo khác. Việc theo dõi cả đường đi giúp học sinh tránh nhầm hai bộ chỉ vì chúng cùng sử dụng một chiếc quần.'),
b('tree',4,'MỞ NHÁNH TỪ A3',['A3 → Q1 và Q2.','Toàn bộ cây có 6 lá.','Mỗi nhánh áo có đúng 2 lá.'],'3 nhánh × 2 lá = 6.',
  'Khi mở nốt hai nhánh xuất phát từ áo ba, cây có tổng cộng sáu lá. Quan sát cấu trúc cây, ta thấy mỗi nhánh áo đều tạo ra đúng hai lá. Bởi vậy số lá của cây bằng số nhánh ở tầng thứ nhất nhân với số nhánh tiếp theo.', 'p6'),
b('tree',5,'Ý NGHĨA CỦA PHÉP NHÂN',['Mỗi kết quả là một đường đi.','Không hai đường đi cùng kết quả.','Tất cả kết quả đều được liệt kê.'],'3 × 2 chính là số đường đi.',
  'Sơ đồ cây còn giúp ta kiểm tra tính đầy đủ và không trùng lặp. Mỗi cách chọn áo quần cho một đường đi duy nhất; ngược lại mỗi đường đi trọn vẹn cho một bộ hợp lệ. Vì thế đếm số đường đi hay đếm số bộ trang phục là cùng một bài toán. Đó là bản chất toán học của quy tắc nhân.'),
# D. general statement and conditions
b('general',0,'TỔNG QUÁT HAI CÔNG ĐOẠN',['Công đoạn 1 có m cách.','Sau MỖI cách đó, công đoạn 2','đều có đúng n cách.'],'Giả thiết: mọi nhánh có cùng n cách.',
  'Ta trừu tượng bài toán vừa giải. Giả sử một công việc được thực hiện qua hai công đoạn. Công đoạn thứ nhất có m cách. Sau mỗi cách chọn ở công đoạn thứ nhất, công đoạn thứ hai đều có đúng n cách. Cụm từ sau mỗi cách chọn là điều kiện quan trọng nhất của quy tắc nhân.'),
b('general',1,'ĐẾM THEO NHÁNH',['Nhánh đầu tiên có n kết quả.','Nhánh thứ hai cũng có n kết quả.','Tổng cộng có m nhánh như vậy.'],'n + n + … + n (m số hạng).',
  'Ta hãy tưởng tượng một cây với m nhánh ở bước thứ nhất. Mỗi nhánh lại sinh ra đúng n kết quả hoàn chỉnh. Vì kết quả thuộc những nhánh khác nhau không trùng nhau, ta có thể cộng số kết quả của từng nhánh. Kết quả là n cộng n, lặp lại m lần.', 'repeatn'),
b('general',2,'PHÁT BIỂU QUY TẮC NHÂN',['Số cách hoàn thành công việc:', 'm × n.', 'Áp dụng khi hai bước đều cần làm.'],'N = m × n.',
  'Theo định nghĩa của phép nhân, n được cộng m lần bằng m nhân n. Ta rút ra quy tắc nhân: nếu bước một có m cách, và sau mỗi lựa chọn của bước một, bước hai có n cách, thì số cách hoàn thành công việc bằng m nhân n. Đây là định lý đếm, không phải mẹo đoán phép tính.', 'mn'),
b('general',3,'NHỮNG ĐIỀU KIỆN CẦN NHỚ',['Một kết quả phải qua đủ các bước.','Không bỏ sót, không đếm trùng.','Số lựa chọn tiếp theo bằng nhau.'],'Không phải cứ có chữ “và” là nhân.',
  'Chúng ta không nên chỉ nhìn thấy chữ và rồi vội nhân. Phải kiểm tra ba điều: mỗi kết quả có được tạo qua đủ các bước không; liệu một kết quả có bị đếm theo nhiều đường đi không; và số cách ở bước tiếp theo có bằng nhau sau mọi lựa chọn đầu tiên hay không. Nếu điều kiện cuối bị thay đổi, cần đếm theo từng nhánh.'),
b('general',4,'SO SÁNH QUY TẮC CỘNG',['Chọn một áo HOẶC một quần: 5.','Chọn một áo VÀ một quần: 6.','Hai công việc khác nhau hoàn toàn.'],'“Hoặc” thay thế; “và” ghép bước.',
  'Đặt hai câu hỏi cạnh nhau. Nếu chỉ chọn một món đồ là áo hoặc quần, có năm lựa chọn riêng biệt. Nếu phải tạo một bộ có cả áo và quần, có sáu bộ. Cùng những đồ vật ban đầu nhưng đối tượng cần đếm thay đổi, nên phép tính thay đổi. Đây là cách phân biệt quy tắc cộng với quy tắc nhân.', 'compare'),
# E. three stages
b('hat',0,'THÊM CÔNG ĐOẠN THỨ BA',['3 chiếc áo, 2 chiếc quần.','Thêm 2 chiếc mũ khác nhau.','Chọn đủ áo, quần và mũ.'],'Mỗi bộ có thêm hai khả năng.',
  'Ta mở rộng bài toán. Ngoài ba áo và hai quần, bây giờ còn có hai chiếc mũ khác nhau. Một bộ trang phục đầy đủ phải gồm một áo, một quần và một mũ. Hãy dự đoán số kết quả mới. Ta sẽ giữ nguyên sáu bộ áo quần cũ rồi thêm bước chọn mũ.'),
b('hat',1,'GIỮ MỘT BỘ ÁO–QUẦN',['Cố định (A1,Q1).','Chọn mũ M1 hoặc M2.','Bộ cũ tạo 2 bộ mới.'],'Từ 1 bộ thành 2 bộ.',
  'Giữ cặp áo một quần một. Với cặp ấy, ta có thể đội mũ một hoặc mũ hai, tạo ra hai kết quả khác nhau. Chú ý rằng hai mũ khác nhau phải được xét riêng vì chúng dẫn đến hai bộ trang phục đầy đủ khác nhau.'),
b('hat',2,'XÉT CẢ SÁU BỘ CŨ',['Có 6 bộ áo–quần.','Mỗi bộ có 2 lựa chọn mũ.','Tổng cộng 6 × 2.'],'Số bộ mới = 12.',
  'Không chỉ bộ thứ nhất, cả sáu bộ áo quần đều có đúng hai cách chọn mũ. Mỗi bộ cũ tạo thành hai bộ mới. Vì vậy số bộ hoàn chỉnh là sáu nhân hai, bằng mười hai. Ở đây ta đã gộp hai bước đầu thành một công đoạn rồi nhân với công đoạn chọn mũ.', 'p12'),
b('hat',3,'NHÂN THEO TỪNG BƯỚC',['Bước 1: 3 cách chọn áo.','Bước 2: 2 cách chọn quần.','Bước 3: 2 cách chọn mũ.'],'3 × 2 × 2 = 12.',
  'Ta có thể tính trực tiếp bằng ba bước. Đầu tiên có ba cách chọn áo. Sau mỗi cách chọn áo, có hai cách chọn quần. Sau mỗi cặp áo quần, lại có hai cách chọn mũ. Nhân các số cách theo từng bước ta được ba nhân hai nhân hai, bằng mười hai.', 'p12'),
b('hat',4,'QUY TẮC NHÂN NHIỀU BƯỚC',['k công đoạn liên tiếp.','Mỗi bước có số cách không đổi','sau các lựa chọn trước.'],'N = n1 × n2 × … × nk.',
  'Với nhiều hơn hai công đoạn, ta lặp lại lập luận tương tự. Nếu ở mỗi bước, số lựa chọn là một số xác định như nhau đối với mọi lịch sử lựa chọn hợp lệ trước đó, số kết quả bằng tích số cách của các bước. Điều kiện này phải được kiểm tra, đặc biệt khi có những ràng buộc giữa các lựa chọn.', 'multistep'),
# F. forbid exactly one pair
b('forbidden',0,'XUẤT HIỆN ĐIỀU KIỆN CẤM',['Trở lại 3 áo và 2 quần.','Không được ghép A2 với Q2.','Có bao nhiêu bộ hợp lệ?'],'Một trong sáu ô bị loại.',
  'Trở lại bài toán chỉ có áo và quần, nhưng thêm điều kiện: áo hai không được ghép với quần hai. Nếu quên điều kiện, ta có sáu bộ. Vậy điều kiện cấm đã loại bỏ những bộ nào? Hãy quan sát bảng tất cả các bộ trước khi quyết định phép tính.'),
b('forbidden',1,'XÁC ĐỊNH CẶP VI PHẠM',['Bộ (A2,Q2) không hợp lệ.','Những bộ còn lại vẫn hợp lệ.','Chỉ có 1 ô bị gạch đỏ.'],'6 − 1 = 5.',
  'Ô ở hàng áo hai, cột quần hai được tô đỏ. Đó là đúng một bộ bị cấm, không phải cả hàng áo hai hay cả cột quần hai. Năm bộ khác vẫn được sử dụng. Vì vậy lấy sáu bộ ban đầu trừ một trường hợp không hợp lệ, ta còn năm.', 'minus1'),
b('forbidden',2,'CÁCH 1: ĐẾM PHẦN BÙ',['Không điều kiện: 3 × 2 = 6.','Số bộ bị cấm: 1.','Số bộ hợp lệ: 6 − 1.'],'Đếm tất cả rồi trừ trường hợp sai.',
  'Cách thứ nhất là đếm gián tiếp, còn gọi là đếm qua phần bù. Ta biết tổng số bộ khi không có điều kiện. Tìm riêng trường hợp bị cấm, rồi trừ khỏi tổng số. Ở bài này chỉ có một cặp không được phép, nên kết quả là năm. Phương pháp rất có ích khi phần bị loại dễ đếm.', 'minus1'),
b('forbidden',3,'CÁCH 2: ĐẾM THEO ÁO',['Áo A1: chọn 2 quần.','Áo A2: chỉ chọn Q1.','Áo A3: chọn 2 quần.'],'2 + 1 + 2 = 5.',
  'Cách thứ hai là chia theo lựa chọn áo. Nếu chọn áo một, ta có hai lựa chọn quần. Nếu chọn áo hai, chỉ còn quần một. Nếu chọn áo ba, lại có hai lựa chọn. Ba trường hợp không trùng nhau nên số cách bằng hai cộng một cộng hai, cũng bằng năm.', 'branch5'),
b('forbidden',4,'VÌ SAO KHÔNG LẤY 3 × 2?',['Số quần sau A2 chỉ còn 1.','Các nhánh có 2, 1, 2 lá.','Không có cùng hệ số n.'],'Không được nhân máy móc.',
  'Đây là một điểm rất dễ sai. Bước chọn quần không còn luôn có hai cách: riêng sau áo hai chỉ có một lựa chọn. Do vậy không thể áp dụng trực tiếp công thức ba nhân hai cho số bộ hợp lệ. Thay vào đó, phải cộng số kết quả của từng nhánh hoặc đếm phần bù.', 'branch5'),
b('forbidden',5,'KIỂM CHỨNG HAI CÁCH ĐẾM',['Đếm phần bù: 6 − 1 = 5.','Đếm theo nhánh: 2 + 1 + 2 = 5.','Hai cách cho cùng kết quả.'],'Đúng phương pháp, đúng điều kiện.',
  'Hãy đối chiếu hai phép tính. Cách đếm phần bù cho sáu trừ một bằng năm. Cách cộng các nhánh cho hai cộng một cộng hai cũng bằng năm. Khi hai lập luận độc lập dẫn tới cùng đáp số, chúng ta có thêm một cách kiểm tra. Quan trọng nhất vẫn là hiểu tại sao mỗi phép tính đúng.', 'both5'),
# G. heterogeneous branch factors 2,1,3 (different new scenario)
b('uneven',0,'KHI SỐ NHÁNH KHÁC NHAU',['Bài toán mới: 3 loại áo.','A1 hợp 2 quần; A2 hợp 1 quần.','A3 hợp 3 quần.'],'Không có cùng số cách bước hai.',
  'Ta xét một tình huống hoàn toàn mới. Với áo một, chỉ có hai loại quần phù hợp. Với áo hai, chỉ có một loại. Nhưng với áo ba, có tới ba loại quần phù hợp. Số cách chọn quần sau từng loại áo không còn bằng nhau. Bây giờ sẽ đếm như thế nào?'),
b('uneven',1,'NHÁNH THỨ NHẤT',['Sau A1 có 2 lựa chọn.','Vẽ được 2 đường đi đầy đủ.','Ghi số lá của nhánh A1.'],'Nhánh A1: 2 cách.',
  'Quan sát nhánh của áo một. Có đúng hai nhãn quần ở cuối hai đường đi. Vì một bộ được xác định bởi cả áo và quần, hai đường đi tạo hai bộ. Ta đặt một bộ đếm nhỏ ngay cạnh nhánh áo một để ghi nhận số cách của nhóm này.'),
b('uneven',2,'NHÁNH THỨ HAI',['Sau A2 chỉ có 1 lựa chọn.','Thêm đúng 1 bộ mới.','Tạm có 2 + 1 = 3 bộ.'],'Nhánh A2: 1 cách.',
  'Chuyển tới áo hai, ta chỉ vẽ một nhánh quần. Không được tự thêm một nhánh nữa cho đủ hai như ở bài toán đầu, vì nhánh đó không hợp lệ. Đến đây số bộ của hai nhóm là hai cộng một, bằng ba. Hình động cần phản ánh đúng ràng buộc đề bài.'),
b('uneven',3,'NHÁNH THỨ BA',['Sau A3 có 3 lựa chọn.','Có thêm 3 bộ mới.','Tổng: 2 + 1 + 3 = 6.'],'Cộng số lá thực tế.',
  'Nhánh áo ba có tới ba kết quả hoàn chỉnh. Cộng với hai và một kết quả trước đó, tổng số bộ là sáu. Ta không tìm một con số nhân chung cho cả ba nhánh, vì các nhánh không có cùng số lá. Quy tắc cộng theo trường hợp là lựa chọn phù hợp.', 'uneven6'),
b('uneven',4,'CÔNG THỨC ĐÚNG TỔNG QUÁT',['Nhánh i có r_i kết quả.','Các nhánh khác nhau không trùng.','Tổng N = r1 + … + rm.'],'Quy tắc nhân là trường hợp đều nhánh.',
  'Trong tình huống tổng quát, nếu lựa chọn thứ i ở công đoạn một tạo ra r i kết quả, số kết quả hoàn chỉnh là tổng tất cả các r i. Khi mọi r i đều bằng n, tổng ấy rút gọn thành m nhân n. Đây là mối liên hệ chính xác giữa quy tắc cộng và quy tắc nhân.', 'uneven_general'),
# H. Quiz / connecting concepts
b('quiz',0,'TỰ KIỂM TRA 1: LẬP SỐ',['Dùng các chữ số 1, 2, 3, 4.','Lập số có 2 chữ số khác nhau.','Có bao nhiêu số?'],'Hãy chọn từng vị trí.',
  'Bài kiểm tra thứ nhất: dùng các chữ số một, hai, ba, bốn để lập số tự nhiên có hai chữ số khác nhau. Trước khi nhìn lời giải, em hãy tự hỏi công việc có mấy bước, mỗi bước có bao nhiêu lựa chọn, và có chữ số nào bị cấm ở vị trí hàng chục không.'),
b('quiz',1,'GIẢI BÀI LẬP SỐ',['Hàng chục: 4 lựa chọn.','Hàng đơn vị: 3 lựa chọn còn lại.','Số kết quả = 4 × 3 = 12.'],'Không lặp chữ số.',
  'Vị trí hàng chục có bốn lựa chọn, vì cả bốn chữ số đều khác không. Sau khi chọn hàng chục, hàng đơn vị phải khác nên còn đúng ba lựa chọn. Theo quy tắc nhân có bốn nhân ba, bằng mười hai số. Số lựa chọn bước hai luôn bằng ba, dù đã chọn chữ số hàng chục nào.', 'quiz12'),
b('quiz',2,'TỰ KIỂM TRA 2: HOẶC',['Có 3 chiếc bút khác nhau.','Có 2 cuốn vở khác nhau.','Chỉ chọn đúng 1 món.'],'Cộng hay nhân?',
  'Bài tiếp theo nhìn rất giống tình huống áo quần, nhưng công việc đã thay đổi. Có ba chiếc bút và hai cuốn vở phân biệt. Một học sinh chỉ chọn đúng một món, hoặc bút hoặc vở. Theo em ta nên cộng hay nhân? Hãy xác định thế nào là một kết quả hoàn chỉnh.'),
b('quiz',3,'GIẢI BÀI CHỌN MỘT MÓN',['Chọn bút: 3 khả năng.','Hoặc chọn vở: 2 khả năng.','Tổng số cách = 3 + 2 = 5.'],'Dùng quy tắc cộng.',
  'Chỉ cần lấy một món là hoàn thành, nên các phương án bút và vở là thay thế cho nhau. Chọn một trong ba bút hoặc một trong hai vở tạo ra năm kết quả khác nhau. Vì vậy phải lấy ba cộng hai, không lấy ba nhân hai. Luôn đọc kỹ động từ của đề bài.', 'quiz5'),
b('quiz',4,'TỰ KIỂM TRA 3: HAI CẶP CẤM',['4 áo, 3 quần phân biệt.','A1 không được ghép Q2 và Q3.','Có bao nhiêu bộ hợp lệ?'],'Đếm phần bù hoặc đếm theo áo.',
  'Bài cuối nâng độ khó. Có bốn áo và ba quần phân biệt. Áo một không được đi cùng quần hai và cũng không được đi cùng quần ba. Hãy tránh sai lầm loại cả áo một. Ta chỉ cấm đúng hai cặp. Em hãy thử giải bằng hai cách trước khi nghe đáp số.'),
b('quiz',5,'LỜI GIẢI VÀ TỔNG KẾT',['Tất cả: 4 × 3 = 12.','Loại 2 cặp: còn 10 bộ.','Cũng có: 1 + 3 + 3 + 3 = 10.'],'Hiểu điều kiện trước khi tính.',
  'Tổng số bộ khi chưa xét điều kiện là mười hai. Có đúng hai cặp bị cấm, nên còn mười bộ hợp lệ. Nếu đếm theo từng áo, áo một có một lựa chọn quần; ba áo còn lại, mỗi áo có ba lựa chọn, cũng được mười. Kết thúc bài học, hãy nhớ đếm đủ, không trùng và kiểm tra số nhánh sau mỗi lựa chọn.', 'quiz10', 20.0),
]

FORMULAS = {
    'p6': '3 times 2 = 6',
    'sum222': '2 + 2 + 2 = 6',
    'repeatn': 'n + n + dots + n = m times n',
    'mn': 'N = m times n',
    'compare': '3 + 2 = 5 quad 3 times 2 = 6',
    'p12': '3 times 2 times 2 = 12',
    'multistep': 'N = n_1 times n_2 times dots times n_k',
    'minus1': '3 times 2 - 1 = 5',
    'branch5': '2 + 1 + 2 = 5',
    'both5': '6 - 1 = 2 + 1 + 2 = 5',
    'uneven6': '2 + 1 + 3 = 6',
    'uneven_general': 'N = r_1 + r_2 + dots + r_m',
    'quiz12': '4 times 3 = 12',
    'quiz5': '3 + 2 = 5',
    'quiz10': '4 times 3 - 2 = 10',
}


def validate():
    assert len(BEATS) == 44, f'Expected 44 beats, got {len(BEATS)}'
    assert list(dict.fromkeys(x.section for x in BEATS)) == list(CHAPTER_LABELS)
    assert len(set(CHAPTER_LABELS)) == 8
    assert all(x.formula == '' or x.formula in FORMULAS for x in BEATS)
    assert all(x.min_seconds >= 15 for x in BEATS)
    assert sum(x.min_seconds for x in BEATS) >= 700
    assert all(25 <= len(x.narration.split()) <= 110 for x in BEATS)
    return True

if __name__ == '__main__':
    validate()
    from collections import Counter
    print('beats',len(BEATS),'chapters',dict(Counter(x.section for x in BEATS)),
          'base_seconds',round(sum(x.min_seconds for x in BEATS),1),
          'narration_words',sum(len(x.narration.split()) for x in BEATS))
