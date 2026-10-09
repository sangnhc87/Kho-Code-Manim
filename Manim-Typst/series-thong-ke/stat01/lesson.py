"""Pure-Python single source of truth for STAT01.
All scores are SYNTHETIC, for teaching only. Manim is not needed for these tests.
"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from math import isclose
from typing import Tuple

SCORES: Tuple[int, ...] = (
    7,8,6,9,5,7,8,6,7,10,4,8,7,6,9,5,8,7,6,8,
    7,9,5,6,8,7,4,9,10,6,7,8,5,9,6,7,8,6,9,7,
)
SORTED_SCORES = tuple(sorted(SCORES))
FREQUENCY = dict(sorted(Counter(SCORES).items()))
N = len(SCORES)
RELATIVE = {score: count / N for score, count in FREQUENCY.items()}
CUMULATIVE = {s: sum(c for v, c in FREQUENCY.items() if v <= s) for s in FREQUENCY}
CHAPTERS = (
    'DỮ LIỆU BIẾT NÓI',
    'TỪ HỖN ĐỘN ĐẾN CÓ THỨ TỰ',
    'BẢNG TẦN SỐ',
    'BIỂU ĐỒ CỘT VÀ BIỂU ĐỒ ĐIỂM',
    'TẦN SỐ TƯƠNG ĐỐI',
    'ĐỌC VÀ HIỂU PHÂN BỐ',
    'DỮ LIỆU CÓ THỂ ĐÁNH LỪA',
    'THỰC HÀNH VÀ KẾT LUẬN',
)

@dataclass(frozen=True)
class Beat:
    chapter: int
    step: int
    title: str
    thought: str
    narration: str
    duration: float = 22.0
    formula: str = ''

# Four complete voice tracks / argument steps per chapter. Each beat includes
# a mathematically meaningful visual state; no filler animations or repeated scenes.
ROWS = [
    [
        ('Một lớp, 40 con số', '40 điểm số chưa kể hết câu chuyện.',
         'Trước mắt chúng ta là bốn mươi điểm kiểm tra minh họa của một lớp học. Nhìn vào danh sách, em có thể nói ngay lớp học đang học tốt hay chưa? Có lẽ chưa, vì mắt chúng ta khó quan sát cùng lúc nhiều số.'),
        ('Dữ liệu là gì?', 'Mỗi số ứng với một kết quả quan sát.',
         'Mỗi điểm trên màn hình là một giá trị dữ liệu. Ở đây, điểm kiểm tra là dữ liệu định lượng. Còn những thông tin như tổ học tập hay môn học yêu thích sẽ là dữ liệu phân loại. Ta không được đánh đồng hai kiểu dữ liệu.'),
        ('Đặt câu hỏi trước khi đếm', 'Cần trả lời: nhiều điểm nào, ít điểm nào?',
         'Trước khi tính bất cứ công thức nào, hãy đặt câu hỏi: điểm nào xuất hiện nhiều nhất, có bao nhiêu học sinh đạt từ tám trở lên, và kết quả có tập trung hay phân tán? Chính câu hỏi quyết định cách xử lý dữ liệu.'),
        ('Dữ liệu minh họa', 'Không gán số liệu giả lập cho lớp học thật.',
         'Bốn mươi điểm số này do chúng ta tạo ra để học toán, không phải dữ liệu cá nhân của học sinh thật. Khi gặp dữ liệu thực tế, cần ghi rõ nguồn, thời điểm và cách thu thập. Sự minh bạch là bước đầu của thống kê tốt.'),
    ],
    [
        ('Sắp xếp từ nhỏ đến lớn', 'Sắp xếp không làm thay đổi dữ liệu.',
         'Bây giờ các thẻ điểm tự chuyển về thứ tự tăng dần. Ta chỉ đổi vị trí các con số, hoàn toàn không thêm hoặc bớt giá trị nào. Kết quả được nhóm lại thành những dãy bốn, năm, sáu, bảy, tám, chín và mười.'),
        ('Thấp nhất và cao nhất', 'Giá trị nhỏ nhất: 4; lớn nhất: 10.',
         'Sau khi sắp xếp, điểm nhỏ nhất nằm bên trái và điểm lớn nhất nằm bên phải. Ta thấy hai đầu là bốn và mười. Nhưng khoảng giá trị này chỉ cho biết hai cực trị, chưa cho biết đa số học sinh đạt mức nào.'),
        ('Nhóm các điểm giống nhau', 'Mỗi nhóm sẽ trở thành một tần số.',
         'Nhìn vào các thẻ số bảy. Chúng xuất hiện nhiều lần hơn những thẻ số mười. Ta sẽ gộp các thẻ có cùng giá trị lại. Quy trình này biến danh sách dữ liệu thô thành một bức tranh dễ đọc.'),
        ('Kiểm tra tính toàn vẹn', 'Vẫn đúng 40 thẻ sau khi sắp xếp.',
         'Một lỗi thường gặp khi xử lý dữ liệu là sao chép thiếu hoặc trùng. Vì vậy, mỗi lần sắp xếp hay phân nhóm, hãy kiểm tra tổng số quan sát. Trước và sau khi chuyển đổi, số điểm phải luôn là bốn mươi.'),
    ],
    [
        ('Tần số là số lần xuất hiện', 'Điểm 4 xuất hiện 2 lần.',
         'Ta lập bảng gồm hai hàng: giá trị điểm và số lần xuất hiện. Số lần một giá trị xuất hiện được gọi là tần số. Chẳng hạn, điểm bốn xuất hiện hai lần nên có tần số bằng hai.'),
        ('Tìm nhóm đông nhất', 'Điểm 7 có tần số 10.',
         'Khi đi qua từng cột, em hãy chú ý nhóm điểm bảy. Có tới mười học sinh trong bộ dữ liệu nhận điểm bảy. Đây là giá trị xuất hiện nhiều nhất, nhưng ta chưa cần học công thức số đo xu thế trung tâm ở tập này.'),
        ('Tổng tần số bằng cỡ mẫu', '2 + 4 + 8 + 10 + 8 + 6 + 2 = 40.',
         'Cộng toàn bộ tần số: hai cộng bốn cộng tám cộng mười cộng tám cộng sáu cộng hai. Kết quả đúng bằng bốn mươi. Đẳng thức này là cách kiểm tra nhanh một bảng tần số có bỏ sót dữ liệu hay không.'),
        ('Tần số tích lũy', 'Tới điểm 7: đã có 24 quan sát.',
         'Nếu cộng dồn từ trái sang phải, ta nhận được tần số tích lũy. Chẳng hạn, số điểm không quá bảy bằng hai cộng bốn cộng tám cộng mười, tức hai mươi bốn. Đây là công cụ rất hữu ích cho những bài học thống kê sau.'),
    ],
    [
        ('Vẽ biểu đồ cột', 'Trục đứng bắt đầu từ 0.',
         'Mỗi giá trị điểm được biểu diễn bằng một cột. Chiều cao của cột chính là tần số. Trục ngang ghi điểm số, trục đứng ghi số học sinh. Trong biểu đồ cột để so sánh độ cao, trục đứng nên bắt đầu từ không.'),
        ('Đọc đỉnh biểu đồ', 'Cột điểm 7 cao nhất: 10 em.',
         'Quan sát đỉnh các cột. Cột điểm bảy cao mười đơn vị nên nổi bật nhất. Hai cột bốn và mười đều cao hai đơn vị. Chỉ cần nhìn biểu đồ, chúng ta đã có thể mô tả nhanh hình dạng phân bố.'),
        ('Mỗi chấm là một học sinh', 'Biểu đồ điểm giữ lại từng quan sát.',
         'Ta thay cột bằng những chấm tròn xếp thành hàng dọc. Một chấm tương ứng đúng một học sinh. Đây là biểu đồ điểm. Ưu điểm của nó là giúp người xem cảm nhận số lượng quan sát trong từng nhóm mà không chỉ nhìn chiều cao.'),
        ('Chọn biểu đồ theo mục đích', 'Bảng: đọc chính xác. Biểu đồ: nhìn xu hướng.',
         'Không có biểu đồ nào tốt nhất cho mọi câu hỏi. Bảng tần số giúp đọc con số chính xác. Biểu đồ cột giúp so sánh nhóm. Biểu đồ điểm giúp thấy từng quan sát. Người làm thống kê phải chọn hình thức phù hợp mục đích.'),
    ],
    [
        ('Tần số tương đối là tỉ phần', 'Tần số chia cho 40.',
         'Mười học sinh đạt điểm bảy trên tổng bốn mươi học sinh. Vậy tần số tương đối của điểm bảy là mười chia bốn mươi, bằng một phần tư. Khi biểu diễn theo phần trăm, ta được hai mươi lăm phần trăm.'),
        ('Từ đếm sang phần trăm', 'Điểm 7 chiếm 25%.',
         'Trên hình, các phần màu được kéo dài theo tỉ lệ của từng nhóm. Nhóm bảy chiếm một phần tư toàn bộ thanh. Nhóm bốn chỉ chiếm năm phần trăm. Phần trăm giúp ta so sánh các nhóm có quy mô khác nhau.'),
        ('Tổng các tỉ lệ', 'Tổng tần số tương đối phải bằng 100%.',
         'Nếu mỗi học sinh thuộc đúng một nhóm điểm, các phần này không trùng nhau và bao phủ toàn bộ dữ liệu. Tổng tỉ lệ vì thế phải bằng một, hay một trăm phần trăm. Nếu không đạt, hãy kiểm tra phép chia hoặc làm tròn.'),
        ('So sánh hai cách biểu diễn', 'Tần số 8 ↔ tần số tương đối 20%.',
         'Điểm tám có tám học sinh, tương ứng hai mươi phần trăm. Hai cách ghi không mâu thuẫn: một cách cho biết số lượng, cách kia cho biết tỉ phần. Ở bài toán thực tế, hãy luôn để ý người ta đang hỏi số người hay phần trăm.'),
    ],
    [
        ('Đếm từ tám điểm trở lên', '8 + 6 + 2 = 16 học sinh.',
         'Nếu đặt ngưỡng từ tám điểm trở lên, ta cần cộng ba nhóm tám, chín và mười. Có tám cộng sáu cộng hai, tức mười sáu học sinh đạt ngưỡng. Trên biểu đồ, ba cột tương ứng sẽ sáng lên cùng lúc.'),
        ('Đổi sang tỉ lệ', '16 trên 40 tương ứng 40%.',
         'Mười sáu học sinh trên tổng bốn mươi tương ứng bốn mươi phần trăm. Tỉ lệ giúp ta diễn đạt kết luận rõ ràng hơn: cứ một trăm quan sát có quy mô và phân bố giống mẫu này, dự kiến khoảng bốn mươi quan sát ở mức từ tám trở lên.'),
        ('Đọc mà không phán xét', 'Biểu đồ mô tả, không giải thích nguyên nhân.',
         'Ta thấy một nhóm điểm bảy khá đông, nhưng không thể chỉ dựa vào biểu đồ để kết luận nguyên nhân. Chưa thể nói đề dễ hay khó, giáo viên chấm nghiêm hay nhẹ. Thống kê mô tả cho biết điều gì xảy ra, chưa tự giải thích vì sao.'),
        ('Câu hỏi nào cần học tiếp?', 'Trung bình, trung vị và độ phân tán.',
         'Một câu hỏi mới nảy sinh: nếu muốn gói gọn kết quả lớp bằng một con số, nên dùng gì? Và nếu hai lớp có cùng giá trị trung bình, liệu chất lượng phân bố có giống nhau? Đó là nội dung dành cho các tập tiếp theo.'),
    ],
    [
        ('Cột bị cắt trục có thể gây hiểu nhầm', 'Chiều cao 8 so với 10 phải nhìn đúng.',
         'Hãy thử cắt trục tung để chỉ hiện từ bảy đến mười. Lập tức độ cao cột tám và mười trông khác nhau quá mức. Đây là ví dụ về biểu đồ gây hiểu nhầm. Khi so sánh chiều cao cột, cần xem kỹ gốc trục.'),
        ('Dữ liệu trùng lặp', 'Một học sinh bị nhập hai lần sẽ sai tổng.',
         'Một bảng dữ liệu tốt cần có quy tắc kiểm tra. Nếu cùng một học sinh được nhập hai lần, tần số và tỉ lệ đều bị sai. Với dữ liệu thực tế, nên kiểm tra mã định danh, ô trống, đơn vị và những giá trị ngoài khoảng cho phép.'),
        ('Chọn mẫu có thể thiên lệch', 'Chỉ hỏi một nhóm tự nguyện chưa đại diện.',
         'Giả sử chỉ những học sinh muốn khoe điểm tự nguyện gửi kết quả. Điểm trong nhóm trả lời có thể cao hơn cả lớp. Khi ấy, dù phép tính chính xác, kết luận về toàn bộ lớp vẫn có thể sai vì chọn mẫu thiên lệch.'),
        ('Mẫu và tổng thể', 'Phải nói rõ đang kết luận về ai.',
         'Nếu có dữ liệu của cả bốn mươi học sinh, ta đang mô tả chính lớp minh họa này. Nếu chỉ có một phần học sinh, đó là mẫu. Không thể suy rộng cho toàn trường nếu cách lấy mẫu không phù hợp. Thống kê luôn đi cùng bối cảnh.'),
    ],
    [
        ('Kiểm tra một', 'Có bao nhiêu học sinh đạt điểm 9?',
         'Câu hỏi thứ nhất: có bao nhiêu học sinh đạt đúng điểm chín? Hãy dừng hình để đọc bảng hoặc đếm các chấm. Đáp số là sáu. Chú ý cụm từ đúng điểm chín, không phải từ chín điểm trở lên.'),
        ('Kiểm tra hai', 'Bao nhiêu phần trăm đạt điểm 7?',
         'Câu thứ hai: điểm bảy chiếm bao nhiêu phần trăm? Ta lấy tần số mười chia cho tổng bốn mươi và nhân một trăm phần trăm. Kết quả là hai mươi lăm phần trăm. Em cần nêu được cả phép tính và đơn vị.'),
        ('Kiểm tra ba', 'Số học sinh đạt từ 8 trở lên?',
         'Câu thứ ba: từ tám trở lên có bao nhiêu học sinh, và chiếm tỉ lệ bao nhiêu? Ta cộng tần số của ba cột tám, chín, mười để được mười sáu học sinh, tương đương bốn mươi phần trăm.'),
        ('Tổng kết', 'Dữ liệu → bảng → biểu đồ → nhận xét.',
         'Kết thúc bài, ta đã biết cách biến một danh sách dài thành thông tin có thể kiểm tra được. Hãy nhớ bốn bước: xác định câu hỏi, kiểm tra dữ liệu, lập bảng và biểu đồ, rồi rút ra kết luận có giới hạn. Hẹn gặp trong tập tiếp theo.'),
    ],
]
BEATS = tuple(Beat(chapter=i+1, step=j+1, title=t, thought=th, narration=n)
              for i, chapter in enumerate(ROWS) for j, (t, th, n) in enumerate(chapter))

def validate():
    assert N == 40
    assert FREQUENCY == {4:2, 5:4, 6:8, 7:10, 8:8, 9:6, 10:2}
    assert sum(FREQUENCY.values()) == N
    assert sum(RELATIVE.values()) == 1
    assert sum(SCORES) == 284
    assert len(BEATS) == 32
    assert [b.chapter for b in BEATS] == [x for x in range(1,9) for _ in range(4)]
    assert all(len(b.narration) > 115 for b in BEATS)
    return True

if __name__ == '__main__':
    validate()
    print('STAT01 data valid, N=', N, 'mean=', sum(SCORES)/N,
          'base seconds=', sum(b.duration for b in BEATS))
