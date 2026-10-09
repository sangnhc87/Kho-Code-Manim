"""STAT16: Simpson's paradox in stratified success rates. All data is synthetic.
Single mathematical source of truth for plots, scripts, formulas, and tests.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import isclose, isfinite

# Each tuple is (successes, total). Never store percentages independently.
MAIN = {
    'A': {'easy': (18, 20), 'hard': (28, 80)},
    'B': {'easy': (72, 90), 'hard': (3, 10)},
}
CHALLENGE = {
    'A': {'easy': (9, 10), 'hard': (8, 40)},
    'B': {'easy': (24, 30), 'hard': (1, 10)},
}
GROUPS=('easy','hard')
METHODS=('A','B')


def validate_table(table):
    if not isinstance(table, dict) or set(table) != set(METHODS):
        raise ValueError('Exactly two methods A and B expected')
    for method in METHODS:
        if not isinstance(table[method], dict) or set(table[method]) != set(GROUPS):
            raise ValueError('Exactly easy and hard strata expected')
        for key in GROUPS:
            pair=table[method][key]
            if not isinstance(pair,(tuple,list)) or len(pair)!=2:
                raise ValueError('Expected (successes,total)')
            hits,total=pair
            if type(hits) is not int or type(total) is not int or total<=0 or not 0<=hits<=total:
                raise ValueError('Nonnegative integer successes <= positive total required')
    return True


def rate(pair):
    hits,total=pair
    if type(hits) is not int or type(total) is not int or total<=0 or not 0<=hits<=total:
        raise ValueError('Invalid count')
    return hits/total


def aggregate(table=MAIN,method='A'):
    validate_table(table)
    if method not in METHODS:raise ValueError('Unknown method')
    hits=sum(table[method][key][0] for key in GROUPS)
    total=sum(table[method][key][1] for key in GROUPS)
    return (hits,total)


def weight_easy(table=MAIN,method='A'):
    validate_table(table)
    return table[method]['easy'][1]/aggregate(table,method)[1]


def mix(table=MAIN,method='A',easy_weight=.5):
    validate_table(table)
    if method not in METHODS or not isinstance(easy_weight,(int,float)) or isinstance(easy_weight,bool) or not isfinite(easy_weight) or not 0<=easy_weight<=1:
        raise ValueError('Mix weight must be between 0 and 1')
    return easy_weight*rate(table[method]['easy'])+(1-easy_weight)*rate(table[method]['hard'])


def pooled_easy_weight(table=MAIN):
    validate_table(table)
    easy=sum(table[m]['easy'][1] for m in METHODS)
    total=sum(aggregate(table,m)[1] for m in METHODS)
    return easy/total


def paradox(table=MAIN):
    validate_table(table)
    return (all(rate(table['A'][x]) > rate(table['B'][x]) for x in GROUPS)
            and rate(aggregate(table,'A')) < rate(aggregate(table,'B')))


def as_pct(x,digits=1):
    if not isfinite(x):raise ValueError('Nonfinite rate')
    formatted=f'{x*100:.{digits}f}'
    if '.' in formatted:formatted=formatted.rstrip('0').rstrip('.')
    return formatted.replace('.',',')+'%'


@dataclass(frozen=True)
class Beat:
    chapter:int
    step:int
    title:str
    thesis:str
    voice:str
    duration:float=38.0


CHAPTERS=(
 'MỘT KẾT LUẬN BỊ ĐẢO NGƯỢC',
 'ĐỌC ĐÚNG TỈ LỆ TỪNG NHÓM',
 'GỘP BẢNG VÀ XUẤT HIỆN NGHỊCH LÝ',
 'VÌ SAO TRỌNG SỐ LÀM ĐỔI KẾT QUẢ?',
 'CHUẨN HÓA CÙNG CƠ CẤU MẪU',
 'DIỄN GIẢI ĐÚNG VÀ KHÔNG SUY DIỄN NHÂN QUẢ',
 'BA BẪY THƯỜNG GẶP TRONG THỐNG KÊ',
 'TỰ GIẢI MỘT BÀI TOÁN ĐẢO CHIỀU',
)

# The voice text is classroom narration, not an operational log.
ROWS=[
 [
 ('Lựa chọn nào có kết quả cao hơn?',
  'Hai cách ôn tập A và B được so sánh qua tỉ lệ đạt yêu cầu.',
  'Giả sử hai cách ôn tập được quan sát trong một bài kiểm tra gồm câu dễ và câu khó. Chúng ta muốn biết nhóm nào có tỉ lệ đạt yêu cầu cao hơn. Đầu tiên, hãy nhìn kết quả ở từng mức độ, sau đó nhìn kết quả gộp chung. Các con số trong video là dữ liệu giả lập để học toán, không phải kết quả nghiên cứu về một phương pháp giảng dạy thực tế.'),
 ('Nhóm bài dễ: A đạt 90%',
  'Ở bài dễ, 18/20 > 72/90.',
  'Với nhóm bài dễ, A có mười tám lượt đạt trong hai mươi lượt, tức chín mươi phần trăm. B có bảy mươi hai lượt đạt trong chín mươi lượt, tức tám mươi phần trăm. Nếu chỉ xét nhóm dễ, A cao hơn B mười điểm phần trăm. Hãy chú ý cả số đạt và tổng số lượt, bởi hai mẫu có quy mô rất khác nhau.'),
 ('Nhóm bài khó: A vẫn cao hơn',
  'Ở bài khó, A: 28/80 = 35%; B: 3/10 = 30%.',
  'Chuyển sang nhóm bài khó, A đạt hai mươi tám trên tám mươi, bằng ba mươi lăm phần trăm. B đạt ba trên mười, bằng ba mươi phần trăm. A tiếp tục cao hơn B, lần này là năm điểm phần trăm. Như vậy, ở từng nhóm độ khó riêng rẽ, A đều có tỉ lệ đạt cao hơn. Em hãy thử dự đoán điều gì xảy ra khi chúng ta cộng tất cả lượt lại.'),
 ('Đặt câu hỏi trước khi gộp',
  'Biết A hơn ở cả hai nhóm, liệu A hơn khi gộp?',
  'Nhiều người sẽ trả lời ngay rằng A tất nhiên phải tốt hơn khi gộp, vì A đang dẫn trước ở cả hai nhóm. Tuy nhiên, dự đoán này bỏ qua một chi tiết: tỉ trọng bài dễ và bài khó của hai phương án không giống nhau. Để trả lời chính xác, chúng ta cần xem mỗi phương án đã được thử trên bao nhiêu lượt dễ và bao nhiêu lượt khó.'),
 ],
 [
 ('Bốn phân số cần kiểm tra',
  'Dễ: 18/20 và 72/90. Khó: 28/80 và 3/10.',
  'Ta viết toàn bộ dữ liệu dưới dạng bảng hai chiều. Mỗi ô ghi rõ số lượt đạt và tổng số lượt. Ở hàng dễ có A là mười tám trên hai mươi, B là bảy mươi hai trên chín mươi. Ở hàng khó có A là hai mươi tám trên tám mươi, B là ba trên mười. Việc giữ mẫu số là bước cực kì quan trọng.'),
 ('Đổi các phân số sang phần trăm',
  'Dễ: 90% > 80%; khó: 35% > 30%.',
  'Đổi sang phần trăm để so sánh trên cùng thang đo. Ở bài dễ, chín mươi phần trăm cao hơn tám mươi phần trăm. Ở bài khó, ba mươi lăm phần trăm cao hơn ba mươi phần trăm. Nhớ rằng phép so sánh này diễn ra trong cùng một nhóm độ khó. Chúng ta chưa hề khẳng định kết quả chung khi các nhóm được gộp.'),
 ('Không đổi điểm phần trăm thành phần trăm tăng',
  'Chênh 10 và 5 điểm phần trăm, không phải tăng 10% và 5%.',
  'Ở hàng dễ, khoảng cách giữa chín mươi và tám mươi là mười điểm phần trăm, không phải chỉ là tăng mười phần trăm so với B. Ở hàng khó, khoảng cách là năm điểm phần trăm. Trong báo cáo thống kê, phân biệt điểm phần trăm và phần trăm tương đối giúp tránh phóng đại hoặc hiểu nhầm. Đơn vị nói đúng cũng quan trọng như phép tính đúng.'),
 ('A dẫn trước ở mọi hàng của bảng',
  'Tỉ lệ của A cao hơn B trong từng nhóm được xét.',
  'Hãy nhìn lại hai hàng cùng lúc. A đứng trên B ở cả hàng dễ lẫn hàng khó. Điều đó không sai và cũng không bị thay đổi bởi những phép tính sắp tới. Khi nghe nói nghịch lý Simpson, ta không nên nghĩ phép chia trong bảng bị sai. Nghịch lý xuất hiện vì phép gộp tạo ra hai trung bình có trọng số khác nhau.'),
 ],
 [
 ('Gộp số lượt đạt của A',
  'A: (18+28)/(20+80) = 46/100 = 46%.',
  'Bây giờ cộng hai ô của A. Số lượt đạt là mười tám cộng hai mươi tám, bằng bốn mươi sáu. Tổng lượt là hai mươi cộng tám mươi, bằng một trăm. Tỉ lệ đạt chung của A bằng bốn mươi sáu phần trăm. Chúng ta phải cộng cả tử lẫn mẫu trước khi chia, chứ không được lấy trung bình đơn giản của chín mươi và ba mươi lăm.'),
 ('Gộp số lượt đạt của B',
  'B: (72+3)/(90+10) = 75/100 = 75%.',
  'Làm tương tự với B, số lượt đạt là bảy mươi hai cộng ba, bằng bảy mươi lăm. Tổng số lượt là chín mươi cộng mười, cũng bằng một trăm. Tỉ lệ chung của B bằng bảy mươi lăm phần trăm. Như vậy, kết quả gộp khác rất xa những so sánh riêng từng nhóm. Ta hãy đặt bốn tỉ lệ riêng và hai tỉ lệ chung cạnh nhau.'),
 ('Kết quả chung đảo chiều',
  'Trong từng nhóm A hơn B, nhưng gộp lại 46% < 75%.',
  'Đây là nghịch lý Simpson. Ở nhóm dễ A đạt chín mươi so với tám mươi phần trăm. Ở nhóm khó A đạt ba mươi lăm so với ba mươi phần trăm. Thế nhưng khi gộp, A chỉ đạt bốn mươi sáu, thấp hơn bảy mươi lăm phần trăm của B. Không có phép tính nào sai: chúng ta đang so sánh các tỉ lệ với những cơ cấu mẫu rất khác nhau.'),
 ('Tại sao không thể lấy trung bình hai tỉ lệ?',
  '(90%+35%)/2 không bằng 46% vì 20 và 80 lượt.',
  'Một bẫy thường gặp là lấy trung bình cộng của chín mươi và ba mươi lăm, được sáu mươi hai phẩy năm phần trăm, rồi cho rằng đây là tỉ lệ chung của A. Nhưng nhóm dễ chỉ có hai mươi lượt, nhóm khó có tám mươi lượt. Vì không cùng quy mô nên hai nhóm không thể có trọng số bằng nhau. Tỉ lệ chung phải phản ánh đúng số quan sát.'),
 ],
 [
 ('Cơ cấu của A nghiêng về bài khó',
  'A: 20% lượt dễ và 80% lượt khó.',
  'Hãy nhìn cột cơ cấu lượt của A, không nhìn tỉ lệ đạt trong từng nhóm. Trong một trăm lượt của A, có hai mươi lượt dễ và tám mươi lượt khó. Nghĩa là phần lớn dữ liệu của A nằm ở nhóm có tỉ lệ đạt thấp hơn. Chính số lượng quan sát của từng nhóm quyết định mức đóng góp của nó vào kết quả chung.'),
 ('Cơ cấu của B nghiêng về bài dễ',
  'B: 90% lượt dễ và 10% lượt khó.',
  'Trong một trăm lượt của B, có tới chín mươi lượt dễ và chỉ mười lượt khó. Đây là cơ cấu gần như ngược lại với A. B có kết quả thấp hơn A nếu so trong từng độ khó, nhưng B lại có rất nhiều lượt ở nhóm dễ, nơi tỉ lệ đạt vốn cao. Vì vậy tỉ lệ chung của B có thể tăng mạnh.'),
 ('Viết tỉ lệ chung như trung bình có trọng số',
  'A = 0,2×90% + 0,8×35% = 46%.',
  'Từ cơ cấu của A, ta viết tỉ lệ đạt chung bằng không phẩy hai nhân chín mươi phần trăm, cộng không phẩy tám nhân ba mươi lăm phần trăm. Kết quả là bốn mươi sáu phần trăm. Đây chính là công thức trung bình có trọng số đã học ở những tập trước. Trọng số không tùy chọn: chúng được suy ra từ số quan sát của từng nhóm.'),
 ('Thử công thức tương tự với B',
  'B = 0,9×80% + 0,1×30% = 75%.',
  'B có trọng số dễ là không phẩy chín, khó là không phẩy một. Ta được không phẩy chín nhân tám mươi phần trăm cộng không phẩy một nhân ba mươi phần trăm, bằng bảy mươi lăm phần trăm. Nhìn hai biểu thức đặt cạnh nhau, em sẽ thấy ngay: dù A dẫn trước trong từng nhóm, phần lớn trọng số của A lại đặt vào nhóm khó.'),
 ],
 [
 ('Câu hỏi công bằng: cùng cơ cấu thì sao?',
  'Cho A và B cùng trọng số 50% dễ, 50% khó.',
  'Giờ ta làm một thí nghiệm toán học: không thay các tỉ lệ đạt ở từng nhóm, nhưng yêu cầu cả A và B được so sánh dưới cùng một cơ cấu. Trước hết, lấy một nửa trọng số cho bài dễ và một nửa cho bài khó. Đây là một cách chuẩn hóa minh họa, không phải dữ liệu quan sát mới. Mục tiêu là cô lập ảnh hưởng của thành phần nhóm.'),
 ('Chuẩn hóa A về cơ cấu 50–50',
  'A chuẩn hóa = 0,5×90% + 0,5×35% = 62,5%.',
  'Với cùng trọng số một nửa cho mỗi độ khó, A có tỉ lệ chuẩn hóa là một nửa của chín mươi cộng một nửa của ba mươi lăm, bằng sáu mươi hai phẩy năm phần trăm. Hãy lưu ý đây không phải tỉ lệ gộp quan sát của A, vốn chỉ bằng bốn mươi sáu phần trăm. Đây là tỉ lệ tính theo một cơ cấu so sánh chung do ta nêu rõ.'),
 ('Chuẩn hóa B về cơ cấu 50–50',
  'B chuẩn hóa = 0,5×80% + 0,5×30% = 55%.',
  'Tính tương tự cho B, một nửa của tám mươi cộng một nửa của ba mươi, bằng năm mươi lăm phần trăm. Trên cùng cơ cấu năm mươi, năm mươi, A lại cao hơn B: sáu mươi hai phẩy năm so với năm mươi lăm phần trăm. Nghịch lý không còn vì hai phương án không bị so bằng hai hỗn hợp độ khó khác nhau nữa.'),
 ('Chuẩn hóa cần ghi rõ cơ cấu chung',
  'Mọi trọng số chung đều bảo toàn A > B ở hai nhóm này.',
  'Một lựa chọn khác là dùng cơ cấu gộp của cả hai phương án, với tổng một trăm mười lượt dễ trên hai trăm lượt, tức năm mươi lăm phần trăm dễ. Khi dùng cùng một trọng số ở hai phương án, A tiếp tục dẫn trước. Ta không nên gọi một cơ cấu là luôn đúng cho mọi bài toán; phải giải thích cơ cấu chung được chọn nhằm trả lời câu hỏi nào.'),
 ],
 [
 ('Nghịch lý Simpson không phải phép toán sai',
  'Khác đối tượng so sánh: tỉ lệ từng nhóm và tỉ lệ gộp.',
  'Tại sao gọi là nghịch lý nếu mọi phép tính đều đúng? Bởi vì kết luận dễ gây bất ngờ cho trực giác. Một bên là so sánh sau khi phân tầng theo độ khó, bên kia là so sánh hai tập hợp có cơ cấu phân tầng khác nhau. Những đại lượng này trả lời các câu hỏi khác nhau. Hiểu điều đó giúp ta tránh biến một tình huống hợp lệ về toán thành câu chuyện gây hoang mang.'),
 ('Độ khó là biến cần xem xét',
  'Độ khó liên quan cả cơ cấu lượt và tỉ lệ đạt.',
  'Ở ví dụ này, độ khó ảnh hưởng mạnh đến khả năng đạt và lại được phân bố không đều giữa A và B. Vì thế độ khó là biến quan trọng cần xem xét khi diễn giải phép so sánh. Trong thực tế, ta còn phải kiểm tra cách phân nhóm, cách chọn mẫu, mức độ đại diện và các khác biệt ban đầu. Dữ liệu gộp một mình không cho ta tất cả thông tin ấy.'),
 ('Không suy ngay A là nguyên nhân thành công',
  'Tương quan quan sát không tự chứng minh quan hệ nhân quả.',
  'Mặc dù A có tỉ lệ cao hơn trong cả hai nhóm độ khó, điều đó chưa đủ chứng minh bản thân cách ôn tập A gây ra kết quả tốt hơn. Ta chưa biết người tham gia được phân vào A và B ra sao, có khác về năng lực hay hoàn cảnh ban đầu hay không. Nghịch lý Simpson là bài học về cách phân tích dữ liệu, không phải một phép thử nhân quả hoàn chỉnh.'),
 ('Một báo cáo thống kê đầy đủ nên ghi gì?',
  'Cần tỉ lệ, tử số, mẫu số, cơ cấu và giả định.',
  'Khi báo cáo, hãy đưa ra cả tỉ lệ theo từng độ khó và tỉ lệ chung; ghi rõ số lượt đạt, tổng số lượt và tỉ trọng các nhóm. Nếu dùng chuẩn hóa, cần nêu cơ cấu chung đã chọn. Sau cùng, kết luận chỉ nên đi xa đến mức dữ liệu cho phép. Một bảng đủ mẫu số thường có giá trị giải thích hơn một con số phần trăm được đặt thật lớn.'),
 ],
 [
 ('Bẫy thứ nhất: trung bình đơn giản',
  'Không lấy trung bình không trọng số của 90% và 35% để gộp A.',
  'Sai lầm thứ nhất là nhìn hai hàng của bảng và cộng các phần trăm rồi chia hai, bỏ qua quy mô mỗi hàng. Cách tính đó chỉ tương ứng với một cơ cấu giả định có trọng số bằng nhau. Khi báo cáo tỉ lệ gộp thực tế, trọng số bắt buộc phải đến từ số lượt. Em hãy luôn thử viết lại công thức dưới dạng tổng số đạt chia tổng số lượt.'),
 ('Bẫy thứ hai: giấu mất mẫu số',
  'Nếu chỉ ghi 90%, 80%, 35%, 30% thì chưa đủ.',
  'Sai lầm thứ hai là trình bày một bảng chỉ có bốn tỉ lệ mà không có cỡ mẫu. Lúc đó ta có thể so sánh từng nhóm, nhưng chưa tính được tỉ lệ gộp vì không biết mỗi nhóm có bao nhiêu lượt. Nhiều bảng dữ liệu trông đầy đủ vì có phần trăm, nhưng để trả lời câu hỏi về tổng thể, ta vẫn cần cả tử số lẫn mẫu số.'),
 ('Bẫy thứ ba: nhầm lẫn kết luận mô tả và nhân quả',
  'Đảo chiều không tự chứng minh nguyên nhân do phương án A hay B.',
  'Sai lầm thứ ba là dùng kết quả thống kê mô tả để khẳng định ngay nguyên nhân. Nếu không kiểm soát cách phân nhóm và những yếu tố liên quan, ta chưa biết liệu sự khác biệt có do phương pháp, người tham gia hay cách lựa chọn dữ liệu. Thống kê có thể gợi câu hỏi và giúp phát hiện biến cần kiểm tra, nhưng không cho phép suy luận nhân quả chỉ bằng phép chia.'),
 ('Quy trình bốn câu hỏi',
  'Phân nhóm thế nào? Mẫu số đâu? Trọng số ra sao? Kết luận gì?',
  'Tóm tắt một cách kiểm tra đơn giản. Thứ nhất, dữ liệu được chia theo biến nào và vì sao? Thứ hai, tử số và mẫu số ở từng ô là bao nhiêu? Thứ ba, trọng số giữa các nhóm có giống nhau không? Thứ tư, kết luận đang nói về mẫu gộp, về từng nhóm hay về tác động nhân quả? Bốn câu hỏi này giúp em đọc nhiều thống kê ngoài lớp học một cách thận trọng.'),
 ],
 [
 ('Tự giải một bảng dữ liệu mới',
  'Dễ A 9/10, B 24/30; khó A 8/40, B 1/10.',
  'Đến lượt em giải một bài mới. Ở nhóm dễ, A đạt chín trên mười, B đạt hai mươi bốn trên ba mươi. Ở nhóm khó, A đạt tám trên bốn mươi, B đạt một trên mười. Trước khi xem lời giải, hãy tính bốn tỉ lệ theo nhóm, sau đó gộp mỗi phương án theo đúng tổng số lượt. Em dự đoán có xảy ra đảo chiều hay không?'),
 ('Kiểm tra từng nhóm trước',
  'Dễ A 90% > B 80%; khó A 20% > B 10%.',
  'Chúng ta giải hàng dễ trước: A đạt chín mươi phần trăm, B tám mươi phần trăm. Ở hàng khó, A đạt hai mươi phần trăm, B mười phần trăm. Như vậy A tiếp tục cao hơn ở cả hai nhóm, nhưng đó mới chỉ là nửa đầu bài toán. Hãy tạm dừng và tự cộng số đạt cũng như số lượt của mỗi phương án, rồi mới nhìn kết quả gộp.'),
 ('Lời giải kết quả gộp',
  'A: 17/50 = 34%; B: 25/40 = 62,5%.',
  'Với A, ta có chín cộng tám bằng mười bảy lượt đạt trên mười cộng bốn mươi bằng năm mươi lượt, tức ba mươi bốn phần trăm. Với B, ta có hai mươi bốn cộng một bằng hai mươi lăm lượt đạt trên ba mươi cộng mười bằng bốn mươi lượt, tức sáu mươi hai phẩy năm phần trăm. Vậy kết luận gộp lại đảo chiều một lần nữa.'),
 ('Kết luận đúng theo dữ liệu đã cho',
  'Luôn kiểm tra độ khó, cỡ mẫu và trọng số trước khi kết luận.',
  'Qua hai ví dụ, em đã thấy nghịch lý Simpson không khiến một phép tính đúng biến thành sai. Nó nhắc chúng ta phải phân biệt các tỉ lệ trong từng nhóm với tỉ lệ gộp, và quan sát trọng số tạo nên mỗi kết quả. Khi gặp một bảng thống kê gây bất ngờ, đừng vội tin hoặc bác bỏ kết luận. Hãy phân tầng dữ liệu, kiểm tra mẫu số và nêu rõ phạm vi của nhận xét.'),
 ],
]
BEATS=tuple(Beat(i+1,j+1,*r) for i,chapter in enumerate(ROWS) for j,r in enumerate(chapter))


def validate():
    assert validate_table(MAIN) and validate_table(CHALLENGE)
    assert len(CHAPTERS)==8 and len(ROWS)==8 and len(BEATS)==32
    assert all(len(ch)==4 for ch in ROWS)
    assert len({b.title for b in BEATS})==32
    assert all(len(b.voice.split())>=46 for b in BEATS)
    assert all(b.duration>=35 for b in BEATS)
    assert paradox(MAIN) and paradox(CHALLENGE)
    assert rate(aggregate(MAIN,'A'))==.46
    assert rate(aggregate(MAIN,'B'))==.75
    assert isclose(mix(MAIN,'A',.5),.625)
    assert isclose(mix(MAIN,'B',.5),.55)
    assert isclose(pooled_easy_weight(MAIN),.55)
    assert isclose(rate(aggregate(CHALLENGE,'A')),.34)
    assert isclose(rate(aggregate(CHALLENGE,'B')),.625)
    return True


if __name__=='__main__':
    print('STAT16_LESSON_OK',validate(),len(BEATS),sum(len(b.voice.split()) for b in BEATS))
