"""Single source of truth: STAT02 charts and 32 independently narrated beats.
All datasets are synthetic and for education, never actual student records.
This module imports no Manim or Typst and can be tested anywhere.
"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from math import isclose
from stat01.lesson import SCORES, FREQUENCY, N, RELATIVE

# Same forty synthetic examination scores used in STAT01.
SCORE_VALUES = tuple(sorted(FREQUENCY))
PERCENT = {x: 100*FREQUENCY[x]/N for x in SCORE_VALUES}
PIE_ANGLES = {x: 360*FREQUENCY[x]/N for x in SCORE_VALUES}
GROUP_EDGES = (4, 6, 8, 10, 12)  # half-open integer-score intervals
GROUP_COUNT = tuple(sum(a <= x < b for x in SCORES)
                    for a,b in zip(GROUP_EDGES,GROUP_EDGES[1:]))
GROUP_DENSITY = tuple(f/(b-a) for f,a,b in zip(GROUP_COUNT,GROUP_EDGES,GROUP_EDGES[1:]))
# Separate synthetic comparison class of 50 students.
CLASS_B = {4:2, 5:6, 6:7, 7:10, 8:12, 9:9, 10:4}
CLASS_B_N = sum(CLASS_B.values())
CLASS_B_PCT = {x:100*f/CLASS_B_N for x,f in CLASS_B.items()}
# Separate monthly class-average dataset; meaningful ordering, unlike score categories.
MONTHS = ('T1','T2','T3','T4','T5','T6')
MONTHLY_MEAN = (6.1, 6.5, 6.4, 7.2, 7.0, 7.6)
# Separate synthetic continuous travel times, differing class widths.
TIME_CLASSES = ((0,10,12), (10,20,8), (20,40,20))
TIME_DENSITY = tuple(f/(b-a) for a,b,f in TIME_CLASSES)

CHAPTERS = (
    'MỘT DỮ LIỆU – NHIỀU CÂU CHUYỆN',
    'BIỂU ĐỒ CỘT VÀ ĐIỂM',
    'BIỂU ĐỒ TRÒN – GÓC Ở TÂM',
    'TẦN SỐ VÀ TẦN SỐ TƯƠNG ĐỐI',
    'HISTOGRAM VÀ PHÂN LỚP',
    'BIỂU ĐỒ ĐƯỜNG THEO THỜI GIAN',
    'ĐỌC BIỂU ĐỒ KHÔNG BỊ ĐÁNH LỪA',
    'CHỌN BIỂU ĐỒ VÀ LUYỆN TẬP',
)

@dataclass(frozen=True)
class Beat:
    chapter: int
    step: int
    title: str
    thesis: str
    voice: str
    duration: float = 23.0
    formula: str = ''

# Every narrated beat communicates an argument, not decorative filler.
ROWS = [
 [
  ('Vẫn là 40 điểm kiểm tra', 'Một bảng số có nhiều cách kể chuyện.',
   'Chúng ta trở lại bốn mươi điểm kiểm tra giả lập đã sử dụng trong tập một. Cùng một bộ số có thể được vẽ bằng nhiều hình khác nhau. Nhưng mỗi loại biểu đồ chỉ trả lời tốt một số câu hỏi. Hãy bắt đầu bằng điều em muốn biết, chứ không phải bằng một kiểu vẽ thật đẹp.'),
  ('Hai câu hỏi khác nhau', 'So sánh số lượng khác so sánh tỉ trọng.',
   'Câu hỏi thứ nhất là điểm nào có nhiều học sinh nhất. Câu hỏi thứ hai là mỗi mức điểm chiếm bao nhiêu phần trăm lớp. Hai câu hỏi dùng cùng dữ liệu, nhưng cách thể hiện trực quan phù hợp có thể khác. Chúng ta sẽ lần lượt giải quyết, rồi tự kiểm tra tính chính xác của mỗi biểu đồ.'),
  ('Giữ một nguồn dữ liệu', 'Tổng tần số luôn bằng bốn mươi.',
   'Mỗi cột trong bảng có giá trị điểm từ bốn đến mười và một tần số tương ứng. Khi chuyển bảng sang biểu đồ, chúng ta không được sửa số lượng quan sát. Tổng các tần số là bốn mươi, và tổng tần số tương đối phải là một trăm phần trăm. Hai tổng này là điều kiện kiểm tra bắt buộc.'),
  ('Thống kê phải trung thực', 'Chọn biểu đồ theo bản chất của biến.',
   'Điểm kiểm tra ở đây là biến số nhận giá trị nguyên. Một bộ dữ liệu khác có thể là môn học yêu thích, thời gian đi học hoặc điểm trung bình qua từng tháng. Khi bản chất biến khác nhau, phương pháp vẽ có thể khác nhau. Mọi bộ số trong tập hôm nay đều là dữ liệu minh họa, không phải dữ liệu thật của học sinh.'),
 ],
 [
  ('Từ bảng sang biểu đồ cột', 'Chiều cao cột bằng tần số.',
   'Bây giờ mỗi giá trị điểm trở thành một cột. Trục ngang ghi điểm, trục đứng ghi số học sinh. Chẳng hạn cột điểm sáu cao tám đơn vị, trong khi cột điểm bảy cao mười đơn vị. Hãy nhìn xem những cột có cùng số lượng có chiều cao bằng nhau. Đây là nguyên lý xây dựng biểu đồ cột.'),
  ('Nhóm nào nhiều nhất?', 'Điểm bảy có mười học sinh.',
   'Chúng ta đánh dấu cột cao nhất. Có đúng mười học sinh đạt điểm bảy, nhiều hơn sáu học sinh đạt điểm chín. Biểu đồ giúp so sánh rất nhanh, nhưng muốn đọc đúng con số vẫn phải nhìn các vạch chia hoặc nhãn dữ liệu. Không nên chỉ ước lượng bằng mắt khi đề bài yêu cầu kết quả chính xác.'),
  ('Vì sao các cột có khoảng cách?', 'Mỗi cột đại diện một giá trị riêng.',
   'Trong hình này, điểm bốn, điểm năm và các điểm tiếp theo là các giá trị tách biệt. Các cột được đặt cách nhau để người xem nhận ra từng nhóm. Điều đó khác với biểu đồ phân bố của một biến liên tục, nơi các khoảng dữ liệu liền nhau có ý nghĩa. Ta sẽ nghiên cứu trường hợp ấy ở chương histogram.'),
  ('Đổi cột thành các chấm', 'Một dấu chấm ứng với một quan sát.',
   'Tôi thay từng cột bằng những chấm xếp dọc. Mỗi chấm ứng với một điểm kiểm tra của một học sinh trong dữ liệu minh họa. Tại điểm bảy, em có thể đếm đủ mười chấm. Biểu đồ điểm hợp với bộ dữ liệu nhỏ và giúp không làm mất cảm giác về các quan sát riêng lẻ.'),
 ],
 [
  ('Chia hình tròn thành các phần', 'Toàn bộ hình tròn là một trăm phần trăm.',
   'Nếu mục tiêu là biểu diễn cơ cấu, chúng ta có thể sử dụng biểu đồ tròn. Cả hình tròn đại diện cho bốn mươi quan sát, mỗi phần biểu diễn tỉ lệ của một mức điểm. Các phần không giao nhau và phải phủ đúng cả vòng tròn. Lúc này, điều quan trọng là tỉ trọng chứ không phải chỉ riêng chiều cao.'),
  ('Mười trên bốn mươi', 'Điểm bảy chiếm 25 phần trăm.',
   'Điểm bảy có mười học sinh trên tổng bốn mươi. Tỉ lệ bằng mười chia bốn mươi, tức hai mươi lăm phần trăm. Một phần tư hình tròn ứng với một góc vuông chín mươi độ. Hình động sẽ làm nổi bật đúng miếng quạt của điểm bảy để em thấy phép tính gắn với diện tích và góc ở tâm.'),
  ('Đổi tần số thành góc', 'Một quan sát ứng với chín độ.',
   'Vì một vòng tròn có ba trăm sáu mươi độ và có bốn mươi quan sát, nên mỗi quan sát tương ứng chín độ. Chẳng hạn điểm chín có sáu quan sát, thành năm mươi bốn độ. Tổng các góc bằng ba trăm sáu mươi độ. Đây là phép kiểm tra tốt trước khi em vẽ một biểu đồ tròn bằng tay.'),
  ('Biểu đồ tròn có giới hạn', 'Quá nhiều lát nhỏ thì khó so sánh.',
   'Biểu đồ tròn tiện để thấy cơ cấu phần trăm, nhưng khó so sánh những phần gần bằng nhau, nhất là khi có nhiều nhóm nhỏ. Khi câu hỏi là điểm sáu hay điểm tám có nhiều hơn, biểu đồ cột dễ đọc hơn nhiều. Hình đẹp chưa chắc là hình tốt nhất; thông tin quan trọng phải là thứ được nhìn thấy dễ dàng.'),
 ],
 [
  ('Tần số hay tần số tương đối?', 'Số người và phần trăm không giống nhau.',
   'Ta có thêm lớp minh họa B gồm năm mươi học sinh. Nếu chỉ so số học sinh đạt cao, lớp đông hơn có thể luôn chiếm ưu thế vì cỡ lớp lớn. Muốn so tỉ trọng, chúng ta phải chia số học sinh thỏa điều kiện cho tổng số của từng lớp. Cần phân biệt rõ hai đại lượng này.'),
  ('Lớp A có 40 học sinh', 'Từ tám điểm: 16 trên 40, bằng 40 phần trăm.',
   'Trong lớp A, số học sinh đạt từ tám trở lên bằng tám cộng sáu cộng hai, tức mười sáu. Chia cho tổng bốn mươi, ta có bốn mươi phần trăm. Hình thanh ngang sẽ tô riêng nhóm đạt ngưỡng và nhóm chưa đạt, nhưng tổng chiều dài thanh vẫn giữ nguyên ở một trăm phần trăm.'),
  ('Lớp B có 50 học sinh', 'Từ tám điểm: 25 trên 50, bằng 50 phần trăm.',
   'Trong lớp minh họa B, số học sinh từ tám điểm trở lên bằng mười hai cộng chín cộng bốn, tức hai mươi lăm. Chia cho năm mươi ta được năm mươi phần trăm. Số lượng tuyệt đối là hai mươi lăm so với mười sáu, còn tỉ trọng là năm mươi phần trăm so với bốn mươi phần trăm.'),
  ('Thanh phần trăm cho hai lớp', 'Cùng thang 100% mới so sánh công bằng.',
   'Hãy quan sát hai thanh cùng chiều dài, đều biểu thị từ không đến một trăm phần trăm. Phần tô nổi của lớp B dài hơn lớp A, đúng bằng chênh lệch mười điểm phần trăm. Chúng ta không nói tăng mười phần trăm, bởi mười điểm phần trăm và tăng mười phần trăm theo tỉ lệ tương đối là hai khái niệm khác nhau.'),
 ],
 [
  ('Ghép các điểm thành khoảng', 'Các lớp [4;6), [6;8), [8;10), [10;12).',
   'Bây giờ thay vì giữ riêng từng điểm, ta gom thành bốn khoảng bằng nhau. Khoảng từ bốn đến dưới sáu chứa các điểm bốn và năm; khoảng từ sáu đến dưới tám chứa điểm sáu và bảy. Các khoảng theo quy ước trái đóng phải mở nên không có điểm nào nằm trong hai khoảng.'),
  ('Histogram khác biểu đồ cột', 'Các khoảng liên tiếp không có khe hở.',
   'Trên histogram, mỗi hình chữ nhật ứng với một khoảng giá trị, và các hình kề nhau không có khoảng trống. Với các khoảng đều rộng hai đơn vị, bốn nhóm của chúng ta có tần số sáu, mười tám, mười bốn và hai. Điều cần nhớ là diện tích hình chữ nhật biểu thị tần số khi vẽ theo mật độ tần số.'),
  ('Khi khoảng rộng không đều', 'Chiều cao phải là mật độ tần số.',
   'Tôi đưa ra một bộ dữ liệu khác về thời gian di chuyển. Ba khoảng từ không đến mười, mười đến hai mươi, và hai mươi đến bốn mươi phút có độ rộng khác nhau. Nếu lấy tần số làm chiều cao, diện tích sẽ đánh lừa mắt. Ta phải lấy tần số chia độ rộng lớp để tính mật độ.'),
  ('Diện tích mới là số lượng', 'Chiều rộng nhân chiều cao bằng tần số.',
   'Trong ví dụ thời gian di chuyển, lớp cuối chứa hai mươi người nhưng rộng hai mươi phút, nên mật độ của nó là một. Lớp đầu chứa mười hai người trong mười phút, mật độ một phẩy hai. Hình đầu cao hơn hình cuối, nhưng diện tích hình cuối lớn hơn. Đó là ý nghĩa thực sự của histogram khi độ rộng lớp không đều.'),
 ],
 [
  ('Dữ liệu có thứ tự thời gian', 'Biểu đồ đường thể hiện sự diễn tiến.',
   'Chúng ta tạm chuyển sang một bộ dữ liệu giả lập độc lập: điểm trung bình của một nhóm học sinh trong sáu tháng. Vì tháng một đến tháng sáu có thứ tự thời gian, nối các điểm lại tạo thành biểu đồ đường có ý nghĩa. Lúc này, độ dốc cho chúng ta thấy các giai đoạn tăng và giảm.'),
  ('Đi lên không phải luôn tăng', 'Từ tháng 2 sang tháng 3 có giảm nhẹ.',
   'Đường tăng từ tháng một đến tháng hai, sau đó giảm nhẹ ở tháng ba rồi tăng rõ ở tháng tư. Khi xem một đoạn đi lên, phải đọc trục tung để biết tăng bao nhiêu. Không nên kết luận xu hướng luôn tăng chỉ vì điểm cuối cao hơn điểm đầu; giữa các mốc vẫn có thể có những đoạn giảm.'),
  ('Không nối bừa các danh mục', 'Thứ tự tùy ý không tạo thành diễn tiến.',
   'Nếu trục ngang là các môn học yêu thích, thứ tự Toán, Văn, Anh có thể thay đổi mà bản chất dữ liệu không đổi. Nối các nhóm ấy thành đường gấp khúc dễ khiến người xem tưởng có một quá trình liên tục. Trong trường hợp đó, biểu đồ cột phù hợp hơn biểu đồ đường.'),
  ('Cùng một dữ liệu, một câu hỏi', 'Dùng đường khi trục ngang mang tính tiến trình.',
   'Khi kết quả được ghi theo tháng, ngày hoặc các thời điểm liên tiếp, biểu đồ đường thường giúp thấy biến động. Khi đối tượng là các nhóm rời nhau, biểu đồ cột thường thích hợp. Quy tắc này không hoàn toàn thay thế việc xem mục tiêu nghiên cứu, nhưng là một điểm kiểm tra rất hữu ích.'),
 ],
 [
  ('Đừng cắt trục tung tùy tiện', 'Cột tần số nên xuất phát từ mốc không.',
   'Tôi vẽ hai cột có giá trị tám và mười. Nếu cho trục bắt đầu từ không, độ cao chênh hai đơn vị được nhìn đúng tỷ lệ. Nhưng khi cắt mất phần lớn trục, chênh lệch nhỏ có thể bị phóng đại. Với biểu đồ cột, độ cao là thông tin nên việc cắt trục dễ gây hiểu nhầm.'),
  ('Kiểm tra diện tích histogram', 'Nếu lớp rộng khác nhau, cột cao chưa chắc nhiều.',
   'Nhìn lại histogram có độ rộng lớp mười và hai mươi phút. Hình rộng có thể thấp nhưng vẫn chứa nhiều quan sát. Khi đọc, đừng chỉ so chiều cao, hãy xét mật độ và diện tích. Không được nhầm histogram với biểu đồ cột tần số khi độ rộng lớp khác nhau.'),
  ('Biểu đồ thiếu đơn vị', 'Cần tên trục, đơn vị và cỡ mẫu.',
   'Một biểu đồ không có tiêu đề, không ghi đơn vị hoặc không nói rõ số quan sát thì rất khó kiểm chứng. Với dữ liệu của chúng ta, điểm số chạy từ bốn đến mười, đơn vị trục tung là học sinh, và cỡ dữ liệu là bốn mươi. Những thông tin này giúp người xem biết chính xác hình đang đo điều gì.'),
  ('Bộ tiêu chí bốn bước', 'Nguồn – thang đo – kiểu biểu đồ – kết luận.',
   'Trước khi tin một biểu đồ, hãy tự hỏi bốn câu. Nguồn dữ liệu có minh bạch không? Thang trục có trung thực không? Kiểu biểu đồ có phù hợp biến đang xét không? Và kết luận có vượt quá điều mà dữ liệu cho phép nói không? Một người giỏi thống kê biết đặt đúng câu hỏi.'),
 ],
 [
  ('Thử chọn biểu đồ cho tình huống', 'So sánh số học sinh theo điểm: cột.',
   'Tình huống một: muốn so sánh số học sinh ở từng điểm số trong lớp A. Em sẽ chọn biểu đồ nào? Cách hợp lý là biểu đồ cột, vì những nhóm điểm tách biệt và ta cần so sánh số lượng. Em hãy nghĩ trước khi màn hình làm nổi bật câu trả lời.'),
  ('Biểu diễn cơ cấu lớp học', 'Tỉ trọng từng mức điểm: tròn hoặc thanh 100%.',
   'Tình huống hai: muốn biết mỗi mức điểm chiếm bao nhiêu phần trăm cả lớp. Em có thể chọn biểu đồ tròn hoặc thanh một trăm phần trăm. Nếu có quá nhiều nhóm nhỏ, thanh phần trăm thường dễ đọc hơn. Chúng ta ưu tiên phương án đơn giản, rõ đơn vị và không che mất con số.'),
  ('Đọc phân bố theo thời gian', 'Theo sáu tháng: đường.',
   'Tình huống ba: cần quan sát kết quả học tập thay đổi qua sáu tháng. Biểu đồ đường sẽ giúp theo dõi sự tiến triển, bao gồm cả những thời điểm giảm nhẹ. Hãy nhớ bộ dữ liệu này là minh họa khác, không phải phép biến đổi trực tiếp từ bốn mươi điểm của lớp A.'),
  ('Tổng kết và câu hỏi cuối', 'Chọn đúng biểu đồ trước khi tính toán.',
   'Tóm lại, bảng cho số chính xác, biểu đồ cột so sánh nhóm, biểu đồ tròn và thanh phần trăm mô tả cơ cấu, histogram mô tả phân bố theo khoảng, còn biểu đồ đường cho thấy biến động theo thời gian. Hãy ghi rõ nguồn dữ liệu và đơn vị đo. Tập tiếp theo chúng ta sẽ tìm hiểu trung bình, trung vị và mốt.'),
 ]
]
BEATS = tuple(Beat(i+1,j+1,title,thesis,narration)
              for i,chapter in enumerate(ROWS)
              for j,(title,thesis,narration) in enumerate(chapter))

def validate():
    assert len(SCORES)==40 and sum(FREQUENCY.values())==N
    assert sum(PERCENT.values())==100 and sum(PIE_ANGLES.values())==360
    assert GROUP_COUNT==(6,18,14,2), GROUP_COUNT
    assert sum(GROUP_COUNT)==N
    assert all(isclose(d*(GROUP_EDGES[i+1]-GROUP_EDGES[i]), GROUP_COUNT[i])
               for i,d in enumerate(GROUP_DENSITY))
    assert CLASS_B_N==50 and sum(CLASS_B_PCT.values())==100
    assert sum(CLASS_B[s] for s in (8,9,10))==25
    assert len(BEATS)==32 and len(CHAPTERS)==8
    assert all(len(b.voice.split())>=44 for b in BEATS)
    assert all(b.duration>=20 for b in BEATS)
    assert sum(b.duration for b in BEATS)>=700
    return True

if __name__=='__main__':
    validate()
    print('STAT02 valid:',len(BEATS),'beats',sum(b.duration for b in BEATS),'seconds',GROUP_COUNT)
