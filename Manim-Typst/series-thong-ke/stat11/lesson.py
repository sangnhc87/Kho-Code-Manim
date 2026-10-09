"""STAT11: Range and interquartile range for grouped data (descriptive school convention)."""
from __future__ import annotations
from dataclasses import dataclass
from math import isclose
from stat01.lesson import SCORES
from stat07.lesson import CLASSES,FREQ,Interval
from stat10.lesson import three_quartiles,school_raw_quartiles

@dataclass(frozen=True)
class Spread:
    span:float
    q1:float
    q2:float
    q3:float
    iqr:float
    lo:float
    hi:float

def grouped_range(classes, freq):
    if not classes or len(classes)!=len(freq) or not any(f>0 for f in freq):
        raise ValueError('Need populated grouped classes')
    if any(f<0 or isinstance(f,bool) or int(f)!=f for f in freq):
        raise ValueError('Invalid frequencies')
    for x in classes:
        if x.right<=x.left:raise ValueError('Class width must be positive')
    for a,b in zip(classes,classes[1:]):
        if a.right!=b.left:raise ValueError('Classes must be consecutive')
    indexes=[i for i,f in enumerate(freq) if f>0]
    a,b=classes[indexes[0]],classes[indexes[-1]]
    return b.right-a.left

def grouped_spread(classes,freq):
    q1,q2,q3=three_quartiles(classes,freq)
    return Spread(grouped_range(classes,freq),q1.value,q2.value,q3.value,
                  q3.value-q1.value,classes[0].left,classes[-1].right)

MAIN=grouped_spread(CLASSES,FREQ)
RAW_R=max(SCORES)-min(SCORES)
RAW_Q=school_raw_quartiles(SCORES)
RAW_IQR=RAW_Q[2]-RAW_Q[0]
UNIFORM=(10,10,10,10)
COMPARE=grouped_spread(CLASSES,UNIFORM)
SHIFTED=tuple(Interval(c.left+3,c.right+3) for c in CLASSES)
SHIFTED_MAIN=grouped_spread(SHIFTED,FREQ)
SCALED=tuple(Interval(2*c.left,2*c.right) for c in CLASSES)
SCALED_MAIN=grouped_spread(SCALED,FREQ)
EDGE_FREQ=(0,6,18,16)
EDGE_SPAN=grouped_range(CLASSES,EDGE_FREQ)

CHAPTERS=(
 'KHOẢNG BIẾN THIÊN: CỰC TRỊ GỐC VÀ RANH GIỚI LỚP',
 'KHOẢNG TỨ PHÂN VỊ: NỬA GIỮA CỦA DỮ LIỆU',
 'MÔ PHỎNG HAI THƯỚC ĐO ĐỘ PHÂN TÁN',
 'SO SÁNH HAI MẪU CÓ CÙNG KHOẢNG BIẾN THIÊN',
 'BIẾN ĐỔI DỮ LIỆU VÀ CÁC TÍNH CHẤT',
 'DỮ LIỆU GHÉP NHÓM CÓ THỂ LÀM MẤT GÌ?',
 'NHỮNG SAI LẦM PHỔ BIẾN VÀ CÂU HỎI ĐẢO',
 'BÀI TOÁN VẬN DỤNG VÀ TỔNG KẾT'
)
@dataclass(frozen=True)
class Beat:
    chapter:int
    step:int
    title:str
    thesis:str
    voice:str
    duration:float=32.0
ROWS=[
[
('Hai cực trị của dữ liệu thô','Điểm nhỏ nhất 4, lớn nhất 10.', 'Hãy quan sát bốn mươi điểm kiểm tra đã dùng xuyên suốt các bài trước. Điểm nhỏ nhất của lớp là bốn, điểm lớn nhất là mười. Hiệu của hai điểm cho biết toàn bộ dãy trải rộng đến đâu. Nhưng một giá trị cực đoan cũng có thể làm thay đổi thước đo ấy rất nhanh, vì thế ta cần học thêm khoảng tứ phân vị.'),
('Khoảng biến thiên của dữ liệu gốc','R gốc = 10 − 4 = 6.', 'Khoảng biến thiên của dữ liệu chưa ghép nhóm là số lớn nhất trừ số nhỏ nhất. Trong ví dụ này, mười trừ bốn bằng sáu. Giá trị sáu được xác định trực tiếp vì ta có cả danh sách. Hãy ghi nhớ điều kiện này: muốn tính khoảng biến thiên chính xác, phải biết chính xác hai giá trị cực trị.'),
('Nhưng bảng ghép nhóm chỉ cho khoảng','Lớp đầu [4;6), lớp cuối [10;12).', 'Khi nhìn bảng bốn lớp, em không thấy điểm nhỏ nhất hay lớn nhất nằm chính xác ở đâu bên trong lớp đầu và lớp cuối. Bảng chỉ cho ranh giới lớp. Do vậy ta dùng hiệu ranh giới trên của lớp cuối có quan sát và ranh giới dưới của lớp đầu có quan sát. Đó là cách tính từ mẫu ghép nhóm.'),
('Khoảng biến thiên từ bảng','R ghép nhóm = 12 − 4 = 8.', 'Lớp đầu có quan sát bắt đầu từ bốn và lớp cuối có quan sát kết thúc ở ranh giới mười hai. Bởi vậy khoảng biến thiên của bảng ghép nhóm là tám theo quy ước sử dụng ranh giới lớp. Nó không bằng khoảng biến thiên sáu của dữ liệu gốc, bởi trong lớp cuối thực tế chỉ có điểm mười, không có điểm mười hai.'),
],
[
('Tại sao chỉ nhìn hai đầu là chưa đủ?','Khoảng biến thiên nhạy với điểm ngoại lệ.', 'Khoảng biến thiên rất dễ hình dung, nhưng chỉ dựa vào hai điểm ở hai đầu. Nếu một học sinh có điểm số rất khác phần còn lại, hiệu hai cực trị có thể phình to trong khi phần lớn lớp học không thay đổi. Để hiểu mức tập trung của nửa giữa, ta dùng khoảng tứ phân vị.'),
('Nhắc lại ba tứ phân vị nội suy','Q1≈6,44; Q2≈7,56; Q3≈8,86.', 'Bảng của chúng ta có tần số sáu, mười tám, mười bốn và hai. Ở tập mười, ba mốc tích lũy mười, hai mươi, ba mươi cho ba tứ phân vị nội suy. Q một khoảng sáu phẩy bốn bốn, Q hai khoảng bảy phẩy năm sáu và Q ba khoảng tám phẩy tám sáu. Đây là các giá trị ước lượng, không phải tứ phân vị gốc.'),
('Ý nghĩa khoảng tứ phân vị','IQR = Q3 − Q1.', 'Q một chia khoảng một phần tư thấp nhất với phần còn lại; Q ba đánh dấu mốc ba phần tư. Khoảng từ Q một đến Q ba biểu diễn phần giữa của phân bố theo phương pháp nội suy đã chọn. Độ dài khoảng ấy gọi là khoảng tứ phân vị. Khác khoảng biến thiên, nó không chỉ được quyết định bởi hai cực trị.'),
('Tính IQR cho bảng 40 điểm','IQR ghép nhóm ≈ 2,41.', 'Lấy tứ phân vị thứ ba trừ tứ phân vị thứ nhất, ta được hai phẩy bốn mươi mốt khi làm tròn đến hai chữ số. Để tránh sai số tích lũy, trong code và phép tính nên giữ phân số hoặc số chưa làm tròn rồi mới kết luận. Từ dữ liệu gốc, IQR chỉ bằng hai, nên ta vẫn phải phân biệt giá trị chính xác với ước lượng.'),
],
[
('Đặt hai thước đo lên cùng trục','R = 8; IQR ≈ 2,41.', 'Trên trục từ bốn đến mười hai, đoạn lớn nối hai ranh giới xa nhất có độ dài tám. Một đoạn ngắn hơn nối Q một với Q ba có độ dài xấp xỉ hai phẩy bốn mươi mốt. Chúng cùng đo độ phân tán nhưng trả lời các câu hỏi khác nhau: toàn bộ phạm vi và độ rộng vùng giữa.'),
('Quan sát khoảng giữa','Tứ phân vị không phải phần trăm số điểm.', 'Trong hình, vạch Q một và Q ba được đặt ở giá trị nội suy trên trục điểm. Ta không đọc hai phẩy bốn mươi mốt thành hai phẩy bốn mươi mốt phần trăm. Đây là độ chênh lệch điểm số, có cùng đơn vị với dữ liệu. Nếu điểm được đo theo mét hay phút, khoảng tứ phân vị cũng mang đơn vị tương ứng.'),
('Đưa ngoại lệ vào dữ liệu gốc','Đổi 10 thành 30: R gốc tăng từ 6 lên 26.', 'Tưởng tượng thay một điểm mười trong bộ dữ liệu gốc bằng ba mươi, chỉ để khảo sát tác động toán học chứ không phải điểm kiểm tra hợp lệ trên thang mười. Khoảng biến thiên chính xác trở thành ba mươi trừ bốn, bằng hai mươi sáu. Các vị trí giữa gần như không thay đổi, nên độ phân tán trung tâm tương đối ổn định.'),
('Không suy ngoại lệ từ bảng tùy tiện','Cần bảng mới nếu giá trị vượt lớp cuối.', 'Một sai lầm thường gặp là kéo điểm ba mươi ra ngoài biểu đồ nhưng vẫn giữ nguyên bốn lớp cũ. Cách đó không hợp lệ vì bảng mới đã bỏ sót một quan sát. Muốn tính lại khoảng biến thiên ghép nhóm, phải thiết lập lớp cuối chứa giá trị ba mươi hoặc xây dựng một bảng phân lớp mới. Không dùng biểu đồ cũ cho dữ liệu đã thay đổi.'),
],
[
('Hai mẫu có cùng lớp đầu và cuối','Cả hai có R ghép nhóm bằng 8.', 'Xét bảng A quen thuộc với bốn tần số sáu, mười tám, mười bốn, hai. Bây giờ xét bảng B có mười quan sát ở mỗi lớp. Mỗi bảng đều có quan sát ở lớp đầu và lớp cuối; theo hiệu hai ranh giới, khoảng biến thiên ghép nhóm cùng bằng tám. Tuy nhiên mức tập trung của dữ liệu hoàn toàn khác nhau.'),
('Bảng A tập trung nhiều ở giữa','IQR A ≈ 2,41.', 'Hai lớp ở giữa của mẫu A chiếm phần lớn số liệu, nên Q một và Q ba không cách nhau quá xa. Khoảng tứ phân vị nội suy khoảng hai phẩy bốn mươi mốt. Nhìn vào bốn cột, ta thấy chiều cao của hai cột giữa rõ ràng lớn hơn hai cột biên, phù hợp với mô tả ấy.'),
('Bảng B trải đều bốn lớp','IQR B = 4.', 'Bảng B có tần số mỗi lớp đều bằng mười. Mốc một phần tư ở đúng ranh giới sáu, mốc ba phần tư ở đúng ranh giới mười, nên khoảng tứ phân vị bằng bốn. Lưu ý ranh giới trùng mức tích lũy được giải thích bằng hai lớp kề; hai cách nội suy cho cùng một ranh giới khi không có lớp trống.'),
('Chọn thước đo để so sánh','Cùng R chưa chắc cùng IQR.', 'Hai mẫu có thể bằng nhau về độ rộng từ lớp đầu đến lớp cuối nhưng khác nhau rõ về độ tập trung ở giữa. Khi so sánh mức độ phân tán, ta không nên kết luận chỉ từ khoảng biến thiên. Hãy nhìn mục tiêu thực tế, bảng tần số và thêm khoảng tứ phân vị; nhiều khi dùng đồng thời hai thước đo sẽ hợp lý hơn.'),
],
[
('Cộng cùng một hằng số','R và IQR đều không đổi.', 'Nếu cộng thêm ba vào mọi giá trị dữ liệu, các khoảng lớp phải dịch sang phải ba đơn vị. Khi đó hai ranh giới đầu và cuối đều tăng ba, nên hiệu của chúng giữ nguyên. Tương tự, Q một và Q ba đều tăng ba, nên khoảng tứ phân vị cũng không đổi. Đây là tính chất đơn giản mà rất hữu ích.'),
('Nhân dữ liệu với hệ số dương','R và IQR nhân với hệ số.', 'Nếu nhân tất cả các giá trị và ranh giới lớp với hai, chiều dài mỗi đoạn trên trục tăng gấp đôi. Khoảng biến thiên từ tám thành mười sáu; khoảng tứ phân vị từ khoảng hai phẩy bốn mươi mốt thành gần bốn phẩy tám ba. Đây không phải mẹo nhớ mà là tính chất của hiệu hai giá trị.'),
('Nhân dữ liệu với hệ số âm','Độ rộng nhân với trị tuyệt đối.', 'Nếu nhân với một hệ số âm, thứ tự các giá trị đảo ngược. Ta phải sắp lại lớp từ thấp đến cao; tứ phân vị đầu và cuối hoán đổi vai trò. Tuy nhiên độ dài khoảng vẫn không âm và được nhân với trị tuyệt đối của hệ số. Vì vậy R và IQR biến đổi theo độ lớn của phép co giãn.'),
('Không nhầm khi đổi đơn vị','Độ phân tán mang đơn vị dữ liệu.', 'Điểm số, phút và centimet là những đơn vị khác nhau. Nếu đổi phút sang giây, mọi khoảng thời gian và cả khoảng biến thiên, IQR sẽ tăng sáu mươi lần về giá trị số. Không thể so sánh trực tiếp số đo độ phân tán của hai biến có đơn vị khác nhau mà không nói rõ đơn vị hoặc chuẩn hóa thích hợp.'),
],
[
('Một bảng có thể che giấu cực trị','Lớp [10;12) không chứa điểm 12.', 'Trong ví dụ 40 điểm, lớp cuối là từ mười đến dưới mười hai nhưng cả hai quan sát đều có điểm mười. Chỉ nhìn bảng, ta không biết chi tiết ấy. Nếu tưởng rằng có học sinh đạt điểm mười hai, đó là suy diễn sai. Khoảng biến thiên ghép nhóm dùng ranh giới như một phép mô tả theo bảng, không phải sự xác nhận đã quan sát thấy các đầu mút.'),
('Đọc đúng lớp không có quan sát','Chọn lớp đầu và cuối có tần số dương.', 'Giả sử một bảng có lớp đầu tiên mang tần số bằng không. Khi tính khoảng biến thiên từ bảng ghép nhóm, ta không lấy ranh giới của lớp trống làm cực trị mô tả. Hãy tìm lớp đầu có ít nhất một quan sát và lớp cuối có ít nhất một quan sát, rồi lấy ranh giới tương ứng. Chương trình cần kiểm tra điều này.'),
('Cùng bảng, nhiều dữ liệu gốc','Không phục hồi chính xác cực trị.', 'Trong cùng một lớp từ sáu đến dưới tám, các điểm có thể nằm gần sáu hoặc gần tám. Rất nhiều bộ dữ liệu thô khác nhau có thể tạo đúng một bảng tần số ghép nhóm. Vì thế hai bộ có cùng bảng sẽ có cùng chỉ số nội suy theo công thức, nhưng vẫn có thể khác nhau về khoảng biến thiên và tứ phân vị thật.'),
('Không gọi phép nội suy là chính xác','Độ chính xác phụ thuộc cách chia lớp.', 'Ghép nhóm là một sự đánh đổi: hình và bảng dễ đọc hơn nhưng mất thông tin chi tiết. Với lớp càng rộng, ta thường càng khó biết chính xác vị trí các giá trị bên trong. Khi báo cáo Q một, Q ba và khoảng tứ phân vị từ bảng, phải nhấn mạnh đây là các kết quả ước lượng theo phép nội suy đã chọn.'),
],
[
('Sai lầm 1: lấy trung điểm lớp','R ghép nhóm không bằng hiệu trung điểm.', 'Để ước lượng số trung bình, ta có thể dùng trung điểm lớp. Nhưng khi tính khoảng biến thiên ghép nhóm theo quy ước đang học, ta dùng ranh giới của lớp đầu và lớp cuối có quan sát, không dùng trung điểm của hai lớp ấy. Nếu lấy mười một trừ năm bằng sáu, ta đã dùng sai quy tắc cho bảng đang xét.'),
('Sai lầm 2: chọn hai lớp bất kỳ','IQR phải từ Q3 trừ Q1.', 'Một số em lấy hai ranh giới sáu và mười rồi kết luận IQR bằng bốn, vì chúng trông như hai vạch phân chia. Không đúng. Q một và Q ba phải được xác định từ mức tích lũy một phần tư và ba phần tư; sau khi nội suy, ta mới lấy hiệu hai giá trị. Với bảng A, hiệu đó xấp xỉ hai phẩy bốn mươi mốt.'),
('Sai lầm 3: đưa điểm ngoài lớp','Nếu dữ liệu đổi, phải ghép nhóm lại.', 'Khi có một giá trị lớn khác thường, ta không thể tự vẽ điểm ngoài trục rồi tuyên bố bảng ghép nhóm vẫn giữ nguyên tổng tần số và ranh giới cũ. Hãy lập lại bảng mới, kiểm tra tổng số quan sát và các khoảng có phủ hết dữ liệu không. Bảng phải nhất quán với các điểm đang được mô tả.'),
('Câu hỏi đảo: biết R thì biết IQR?','Không thể suy ra IQR chỉ từ R.', 'Hãy nhìn lại hai bảng A và B. Cùng khoảng biến thiên bằng tám, nhưng một bảng có IQR gần hai phẩy bốn mươi mốt, bảng kia có IQR bằng bốn. Như vậy chỉ biết khoảng biến thiên thì chưa đủ để suy ra độ phân tán trung tâm. Muốn trả lời, cần biết thêm phân bố tần số hoặc thông tin về các tứ phân vị.'),
],
[
('Bài tập: tìm R ghép nhóm','Bảng A có R bằng 8.', 'Bài thứ nhất hãy xác định lớp có quan sát đầu tiên và cuối cùng của bảng A, rồi tìm khoảng biến thiên từ ranh giới. Ta không lấy điểm mười đã quan sát làm đầu cuối nếu đề chỉ cho bảng ghép nhóm; ranh giới trên của lớp cuối là mười hai, ranh giới dưới lớp đầu là bốn. Hiệu bằng tám.'),
('Bài tập: tính IQR nội suy','IQR A ≈ 2,41.', 'Hãy dùng tần số tích lũy sáu, hai mươi bốn, ba mươi tám, bốn mươi. Mốc mười nằm ở lớp hai, mốc ba mươi ở lớp ba. Nội suy lần lượt Q một bằng sáu phẩy bốn bốn và Q ba bằng tám phẩy tám sáu. Giữ kết quả chính xác trong khi tính rồi mới làm tròn hiệu để được khoảng hai phẩy bốn mươi mốt.'),
('Bài tập: so sánh hai mẫu','R bằng nhau nhưng IQR A nhỏ hơn B.', 'Bài thứ ba dùng bảng B với bốn tần số mười, mười, mười, mười. Khoảng biến thiên vẫn bằng tám, nhưng tứ phân vị đầu ở sáu và tứ phân vị cuối ở mười, cho IQR bằng bốn. Như vậy bảng B phân tán hơn A trong vùng giữa, theo thước đo IQR. Hãy kết luận đúng phạm vi của nhận xét.'),
('Tổng kết và nối sang phương sai','Hai thước đo chưa mô tả hết phân bố.', 'Kết thúc tập này, em cần phân biệt khoảng biến thiên gốc và ghép nhóm, hiểu ý nghĩa của Q ba trừ Q một, và biết so sánh hai bảng không máy móc. Tập tiếp theo sẽ xét phương sai và độ lệch chuẩn của mẫu ghép nhóm. Khi đó chúng ta sử dụng thông tin từ tất cả các lớp, thay vì chỉ dựa vào cực trị hay các tứ phân vị.'),
]
]
BEATS=tuple(Beat(i+1,j+1,*r) for i,rows in enumerate(ROWS) for j,r in enumerate(rows))
def validate():
    assert len(CHAPTERS)==8 and len(BEATS)==32
    assert all(len(ch)==4 for ch in ROWS)
    assert sum(b.duration for b in BEATS)==1024
    assert all(len(b.voice.split())>=39 for b in BEATS)
    assert FREQ==(6,18,14,2)
    assert (RAW_R,RAW_Q,RAW_IQR)==(6,(6,7,8),2)
    assert isclose(MAIN.span,8) and isclose(MAIN.iqr,152/63)
    assert isclose(COMPARE.span,8) and isclose(COMPARE.iqr,4)
    assert isclose(SHIFTED_MAIN.iqr,MAIN.iqr) and isclose(SCALED_MAIN.iqr,2*MAIN.iqr)
    assert EDGE_SPAN==6
    return True
if __name__=='__main__':print('STAT11_LESSON_OK',validate(),len(BEATS),sum(len(x.voice.split()) for x in BEATS))
