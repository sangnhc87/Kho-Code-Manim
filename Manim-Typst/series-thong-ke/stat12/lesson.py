"""STAT12: grouped-data population-style variance and standard deviation (THPT)."""
from __future__ import annotations
from dataclasses import dataclass
from math import sqrt, isclose, fsum
from stat01.lesson import SCORES
from stat07.lesson import CLASSES, FREQ, Interval

@dataclass(frozen=True)
class Stats:
    n: int
    mean: float
    second: float
    variance: float
    sd: float

def grouped_stats(classes, frequencies):
    if not classes or len(classes) != len(frequencies):
        raise ValueError('Classes and frequencies must be nonempty and match')
    if any(isinstance(f,bool) or not isinstance(f,int) or f<0 for f in frequencies):
        raise ValueError('Frequencies must be nonnegative integers')
    if not any(frequencies):
        raise ValueError('At least one observation is required')
    for c in classes:
        if c.right<=c.left:raise ValueError('Invalid class width')
    for c,d in zip(classes,classes[1:]):
        if c.right != d.left:raise ValueError('Classes must be consecutive')
    n=sum(frequencies)
    mean=fsum(f*c.midpoint for f,c in zip(frequencies,classes))/n
    second=fsum(f*c.midpoint**2 for f,c in zip(frequencies,classes))/n
    variance=fsum(f*(c.midpoint-mean)**2 for f,c in zip(frequencies,classes))/n
    if not isclose(variance,second-mean*mean,rel_tol=1e-10,abs_tol=1e-10):
        raise AssertionError('Equivalent variance formulas disagree')
    return Stats(n,mean,second,variance,sqrt(variance))

def raw_stats(values):
    if not values:raise ValueError('No observations')
    mu=fsum(values)/len(values)
    v=fsum((x-mu)**2 for x in values)/len(values)
    return Stats(len(values),mu,fsum(x*x for x in values)/len(values),v,sqrt(v))

MAIN=grouped_stats(CLASSES,FREQ)
RAW=raw_stats(SCORES)
OTHER_FREQ=(9,19,3,9)
OTHER=grouped_stats(CLASSES,OTHER_FREQ)
_changed=list(SCORES)
_changed[_changed.index(10)]=30
OUTLIER_RAW=raw_stats(_changed)
PRACTICE_CLASSES=tuple(Interval(i,i+2) for i in (0,2,4,6))
PRACTICE_FREQ=(2,8,6,4)
PRACTICE=grouped_stats(PRACTICE_CLASSES,PRACTICE_FREQ)

def inverse_counts(x):
    if isinstance(x,bool) or not isinstance(x,int) or not 0<=x<=6:raise ValueError('x must be an integer 0..6')
    return (x,8,6,6-x)

@dataclass(frozen=True)
class Beat:
    chapter:int
    step:int
    title:str
    thesis:str
    voice:str
    duration:float=36.0

CHAPTERS=(
    'VÌ SAO CẦN ĐỘ LỆCH CHUẨN CHO DỮ LIỆU GHÉP NHÓM?',
    'TRUNG ĐIỂM LỚP VÀ SỐ TRUNG BÌNH ƯỚC LƯỢNG',
    'XÂY DỰNG CÔNG THỨC PHƯƠNG SAI TỪ ĐỘ LỆCH',
    'CÔNG THỨC RÚT GỌN VÀ KIỂM CHỨNG',
    'CÙNG TRUNG BÌNH, KHÁC ĐỘ PHÂN TÁN',
    'ĐƠN VỊ ĐO, PHÉP BIẾN ĐỔI VÀ CÔNG THỨC THƯỜNG NHẦM',
    'NGOẠI LỆ VÀ GIỚI HẠN CỦA MẪU GHÉP NHÓM',
    'VẬN DỤNG: TÌM TẦN SỐ CHƯA BIẾT'
)
ROWS=[
[
('Nhìn lại bảng 40 điểm','Bốn nhóm: 6, 18, 14, 2.', 'Chúng ta vẫn dùng bốn mươi điểm kiểm tra đã học trong những tập trước. Bảng tần số gồm bốn lớp điểm, có sáu, mười tám, mười bốn và hai quan sát. Bảng cho ta hình dạng chung của phân bố, nhưng chỉ biết trung bình thì chưa thể xác định các điểm tập trung hay phân tán như thế nào.'),
('Hai lớp học có thể cùng trung bình','Cùng một tâm chưa nói hết phân bố.', 'Hãy tưởng tượng hai lớp có cùng điểm trung bình. Một lớp nhiều học sinh đạt điểm gần mức trung bình, lớp kia có cả điểm rất thấp và rất cao. Hai lớp có cùng tâm nhưng mức dao động khác nhau. Độ lệch chuẩn là thước đo giúp trả lời câu hỏi: các giá trị thường cách tâm bao xa?'),
('Dữ liệu đã được ghép nhóm','Không còn biết chính xác từng điểm.', 'Khi ghép nhóm, ta chỉ biết số quan sát trong mỗi khoảng. Trong lớp từ sáu đến dưới tám có mười tám điểm, nhưng không rõ từng giá trị chính xác. Bởi vậy ta thay các điểm trong mỗi lớp bằng trung điểm của khoảng. Cách thay thế ấy cho phép tính gần đúng phương sai và độ lệch chuẩn.'),
('Báo trước ý nghĩa xấp xỉ','Kết quả ghép nhóm chỉ là ước lượng.', 'Trong tập này, các dấu xấp xỉ rất quan trọng. Nếu chỉ có bảng ghép nhóm, phương sai tính từ trung điểm lớp không nhất thiết bằng phương sai của danh sách gốc. Chúng ta sẽ lần lượt dựng phép tính, kiểm tra bằng hai công thức và cuối cùng so sánh kết quả ước lượng với dữ liệu thật.'),
],
[
('Chọn bốn trung điểm','m = 5, 7, 9, 11.', 'Bốn khoảng có cùng độ rộng hai điểm. Trung điểm của từng khoảng lần lượt là năm, bảy, chín và mười một. Trong mô hình ghép nhóm, mỗi trung điểm được lặp theo tần số của lớp đó. Như vậy ta có một phân bố xấp xỉ gồm bốn mươi giá trị đại diện.'),
('Đặt trọng số theo tần số','Tổng tần số vẫn là 40.', 'Vì không phải lớp nào cũng đông như nhau, trung bình các trung điểm không thể chỉ là cộng bốn số rồi chia bốn. Ta phải nhân mỗi trung điểm với tần số của lớp tương ứng. Chỉ khi kết hợp đúng cả giá trị đại diện và trọng số, trung bình ghép nhóm mới có ý nghĩa.'),
('Tính số trung bình ghép nhóm','(6×5 + 18×7 + 14×9 + 2×11)/40.', 'Các tích lần lượt là ba mươi, một trăm hai mươi sáu, một trăm hai mươi sáu và hai mươi hai. Tổng bằng ba trăm linh bốn, chia cho bốn mươi được bảy phẩy sáu. Đây là trung bình ước lượng sẽ làm tâm tham chiếu cho toàn bộ phép tính phương sai ghép nhóm.'),
('So với số liệu ban đầu','Trung bình gốc 7,1; ghép nhóm 7,6.', 'Khi còn giữ toàn bộ bốn mươi điểm, ta tính chính xác được trung bình bảy phẩy một. Sau khi thay mỗi điểm bằng trung điểm lớp, trung bình xấp xỉ bảy phẩy sáu. Chênh lệch nửa điểm nhắc chúng ta rằng thao tác ghép nhóm làm mất thông tin, chứ không chỉ là đổi kiểu biểu đồ.'),
],
[
('Đo khoảng cách tới tâm','Độ lệch: mᵢ − 7,6.', 'Bây giờ hãy nhìn từng trung điểm nằm bên trái hay bên phải mốc bảy phẩy sáu. Trung điểm năm thấp hơn hai phẩy sáu; bảy thấp hơn không phẩy sáu; chín cao hơn một phẩy bốn; mười một cao hơn ba phẩy bốn. Các độ lệch mang dấu khác nhau nên không thể cộng trực tiếp để đo mức phân tán.'),
('Bình phương độ lệch','Bình phương làm mọi đóng góp không âm.', 'Nếu cộng độ lệch có dấu, những phần âm và dương sẽ triệt tiêu. Phương sai dùng bình phương để tránh sự triệt tiêu ấy; độ lệch càng lớn thì đóng góp sau bình phương càng đáng kể. Đây cũng là lý do một giá trị rất xa trung bình có thể làm phương sai tăng mạnh.'),
('Cân bằng mỗi lớp theo tần số','Nhân bình phương độ lệch với tần số.', 'Một lớp có mười tám học sinh phải góp mười tám lần, không thể chỉ đóng góp một lần như lớp có hai học sinh. Chúng ta nhân bình phương độ lệch của từng trung điểm với tần số, cộng bốn tích rồi chia cho tổng bốn mươi quan sát. Đó là công thức phương sai theo mẫu ghép nhóm.'),
('Kết quả phương sai và căn bậc hai','Phương sai ≈ 2,44; độ lệch chuẩn ≈ 1,562.', 'Bốn đóng góp lần lượt là bốn mươi phẩy năm sáu, sáu phẩy bốn tám, hai mươi bảy phẩy bốn bốn và hai mươi ba phẩy một hai. Tổng bằng chín mươi bảy phẩy sáu. Chia bốn mươi ta được phương sai hai phẩy bốn bốn; lấy căn bậc hai được độ lệch chuẩn khoảng một phẩy năm sáu hai.'),
],
[
('Một con đường tính khác','Dùng bình phương trung điểm lớp.', 'Công thức vừa xây dựng rất trực quan, nhưng với bảng có nhiều nhóm, phép trừ từng trung điểm có thể dài. Ta có thể biến đổi đại số thành cách tính khác: trung bình có trọng số của bình phương các trung điểm, trừ đi bình phương của trung bình có trọng số. Hai công thức phải cho cùng kết quả.'),
('Tính trung bình bình phương','Tổng có trọng số là 2408.', 'Bình phương các trung điểm cho hai mươi lăm, bốn mươi chín, tám mươi mốt và một trăm hai mươi mốt. Nhân tương ứng với sáu, mười tám, mười bốn, hai ta được tổng hai nghìn bốn trăm linh tám. Chia cho bốn mươi, trung bình bình phương của các giá trị đại diện bằng sáu mươi phẩy hai.'),
('Trừ bình phương trung bình','60,2 − 7,6² = 2,44.', 'Tiếp theo lấy sáu mươi phẩy hai trừ bình phương của bảy phẩy sáu. Kết quả bằng hai phẩy bốn bốn, khớp với cách đếm theo từng độ lệch. Việc có hai lối tính không chỉ để làm nhanh mà còn rất hữu ích khi kiểm tra xem chúng ta có gõ sai tần số hoặc trung điểm nào không.'),
('Nhớ căn bậc hai ở bước cuối','Độ lệch chuẩn dùng cùng đơn vị dữ liệu.', 'Phương sai đo theo đơn vị bình phương. Nếu điểm kiểm tra đo bằng điểm, đơn vị của phương sai là điểm bình phương, còn độ lệch chuẩn lại có đơn vị điểm. Lấy căn bậc hai giúp kết quả quay về cùng đơn vị với dữ liệu. Giá trị một phẩy năm sáu hai không phải một tỷ lệ phần trăm.'),
],
[
('Tạo bảng thứ hai cùng trung bình','Tần số mới: 9, 19, 3, 9.', 'Chúng ta so sánh bảng A quen thuộc với bảng B có chín, mười chín, ba và chín quan sát trong bốn lớp. Bảng B cũng có đúng bốn mươi quan sát. Điều đáng chú ý là cả hai bảng đều có trung bình ghép nhóm bảy phẩy sáu, mặc dù hình dạng các cột khác nhau rõ rệt.'),
('Giữ nguyên vạch trung bình','Hai vạch trung bình đều ở 7,6.', 'Khi thay bảng A bằng bảng B, đường thẳng chỉ vị trí trung bình không dịch chuyển. Nhưng bảng B có nhiều quan sát nằm ở những lớp xa trung bình hơn. Quan sát sự thay đổi của các cột là cách trực quan để thấy rằng trung bình bằng nhau không kéo theo độ phân tán bằng nhau.'),
('So sánh hai phương sai','A: 2,44; B: 4,44.', 'Tính theo cùng bốn trung điểm và công thức vừa học, phương sai của bảng A bằng hai phẩy bốn bốn, còn phương sai bảng B bằng bốn phẩy bốn bốn. Cả hai cùng được chia cho bốn mươi. Mẫu B phân tán hơn mẫu A theo tiêu chí phương sai, vì độ lệch bình phương trung bình lớn hơn.'),
('So sánh độ lệch chuẩn','A: 1,562; B: 2,107.', 'Lấy căn bậc hai, mẫu A có độ lệch chuẩn xấp xỉ một phẩy năm sáu hai, còn mẫu B khoảng hai phẩy một không bảy. Chúng ta có thể đưa kết quả về cùng đơn vị điểm để so sánh. Hãy nhớ kết luận chỉ nói về các giá trị đại diện của bảng ghép nhóm, không phải đo được chính xác từng điểm chưa biết.'),
],
[
('Cộng một hằng số vào toàn bộ điểm','Phương sai và độ lệch chuẩn không đổi.', 'Nếu cộng ba điểm cho mọi giá trị đại diện, trung bình tăng thêm ba, nhưng khoảng cách của từng giá trị đến trung bình mới không đổi. Do vậy phương sai và độ lệch chuẩn vẫn giữ nguyên. Trên hình, cả các cột lẫn vạch trung bình cùng dịch chuyển; độ rộng phân bố không thay đổi.'),
('Nhân mọi giá trị với hai','Phương sai nhân 4; độ lệch chuẩn nhân 2.', 'Khi nhân tất cả điểm số với hai, độ lệch so với trung bình cũng tăng gấp đôi. Bình phương các độ lệch khiến phương sai tăng gấp bốn; còn độ lệch chuẩn tăng gấp hai. Nếu nhân với hệ số âm, phương sai vẫn nhân bình phương hệ số, độ lệch chuẩn nhân giá trị tuyệt đối.'),
('Vì sao ở THPT chia cho n?','Dùng n, không tự đổi thành n − 1.', 'Trong các bài thống kê mô tả THPT đang học, ta lấy tổng bình phương độ lệch chia cho n, tức tổng tần số của bảng. Công thức chia n trừ một xuất hiện trong một số bài toán ước lượng phương sai tổng thể từ mẫu, thuộc bối cảnh thống kê suy luận khác. Không được tự hoán đổi hai mẫu số khi làm bài học này.'),
('Không nhầm phương sai với độ lệch chuẩn','s² và s có đơn vị khác nhau.', 'Một đáp án hai phẩy bốn bốn là phương sai; một phẩy năm sáu hai là độ lệch chuẩn. Nếu đề hỏi độ lệch chuẩn mà dừng ở phương sai, lời giải chưa hoàn chỉnh. Ngược lại, nếu đề hỏi phương sai mà ghi căn bậc hai, ta đã tính nhầm đại lượng. Hãy quan sát đơn vị để tự phát hiện lỗi.'),
],
[
('Ngoại lệ xuất hiện trên dữ liệu gốc','Thay một điểm 10 bằng 30.', 'Để khảo sát tác động của ngoại lệ, ta tạm thay một trong hai giá trị mười của dữ liệu gốc thành ba mươi. Đây là thí nghiệm toán học, không phải một điểm hợp lệ trên thang mười. Một quan sát biến đổi nhưng các quan sát khác giữ nguyên. Hãy dự đoán xem trung bình và phương sai sẽ tăng nhiều hay ít.'),
('Tính lại phương sai từ dữ liệu gốc','Phương sai gốc: 2,29 → 14,94.', 'Sau khi thay, trung bình của dữ liệu gốc tăng từ bảy phẩy một lên bảy phẩy sáu, trong khi phương sai tăng từ hai phẩy hai chín lên mười bốn phẩy chín bốn. Bình phương khiến giá trị rất xa trung bình tạo ra ảnh hưởng lớn. Đây là điểm mạnh trong nhận diện phân tán, nhưng cũng là điều cần thận trọng khi dữ liệu có ngoại lệ.'),
('Không được giữ bảng lớp cũ','Nếu có điểm 30 phải ghép nhóm lại.', 'Điểm ba mươi nằm ngoài lớp cuối từ mười đến dưới mười hai. Vì vậy không thể dùng bảng tần số bốn lớp cũ rồi chỉ sửa một cột trên hình. Muốn tính phương sai ghép nhóm mới, trước hết ta phải chia lại các khoảng để chứa toàn bộ dữ liệu. Bảng phải tương ứng đúng với dữ liệu hiện hành.'),
('Dữ liệu ghép nhóm luôn mất chi tiết','Hai bộ dữ liệu gốc có thể cùng bảng.', 'Các quan sát khác nhau trong một lớp có thể được thay bằng cùng một trung điểm. Vì vậy hai bộ dữ liệu thô có cùng bảng tần số ghép nhóm vẫn có thể có phương sai gốc khác nhau. Khi phân tích thực tế, ta phải nói rõ đây là số đo tính từ trung điểm lớp, chỉ xấp xỉ độ phân tán của dữ liệu thô.'),
],
[
('Đề bài ngược có bốn lớp','[0;2), [2;4), [4;6), [6;8).', 'Bài tổng hợp cuối video dùng một bộ số liệu mới, chia vào bốn lớp từ không đến tám, mỗi lớp rộng hai. Gọi tần số lần lượt là x, tám, sáu và sáu trừ x, với tổng hai mươi quan sát. Biết trung bình ghép nhóm bằng bốn phẩy hai, hãy tìm x và độ lệch chuẩn.'),
('Tìm ẩn từ số trung bình','(96 − 6x)/20 = 4,2.', 'Trung điểm của bốn lớp lần lượt là một, ba, năm và bảy. Tổng có trọng số là x cộng hai mươi bốn cộng ba mươi cộng bốn mươi hai trừ bảy x, bằng chín mươi sáu trừ sáu x. Chia hai mươi và cho bằng bốn phẩy hai, ta tìm được x bằng hai.'),
('Tính độ phân tán sau khi tìm x','Tần số: 2, 8, 6, 4.', 'Khi x bằng hai, bốn tần số lần lượt là hai, tám, sáu và bốn. Tổng trung điểm bình phương có trọng số bằng bốn trăm hai mươi. Chia hai mươi được hai mươi mốt, rồi trừ bình phương bốn phẩy hai. Phương sai xấp xỉ ba phẩy ba sáu; độ lệch chuẩn khoảng một phẩy tám ba ba.'),
('Tổng kết hai cách tính phương sai','Xác định lớp → trung điểm → trung bình → phương sai.', 'Khi gặp một bảng ghép nhóm, hãy kiểm tra tổng tần số, xác định trung điểm, tính trung bình có trọng số, sau đó chọn công thức phương sai phù hợp. Cuối cùng lấy căn nếu đề yêu cầu độ lệch chuẩn. Mọi kết quả cần có đơn vị và dấu xấp xỉ thích hợp. Tập tiếp theo chúng ta sẽ so sánh hai mẫu số liệu toàn diện hơn.'),
]
]
BEATS=tuple(Beat(i+1,j+1,*r) for i,rows in enumerate(ROWS) for j,r in enumerate(rows))

def validate():
    assert len(CHAPTERS)==8 and len(BEATS)==32 and all(len(r)==4 for r in ROWS)
    assert FREQ==(6,18,14,2)
    assert isclose(MAIN.mean,7.6) and isclose(MAIN.variance,2.44)
    assert isclose(MAIN.second,60.2) and isclose(RAW.mean,7.1)
    assert isclose(RAW.variance,2.29) and isclose(OTHER.mean,7.6)
    assert isclose(OTHER.variance,4.44)
    assert isclose(OUTLIER_RAW.mean,7.6) and isclose(OUTLIER_RAW.variance,14.94)
    assert isclose(PRACTICE.mean,4.2) and isclose(PRACTICE.variance,3.36)
    assert inverse_counts(2)==PRACTICE_FREQ
    assert all(len(b.voice.split())>=38 for b in BEATS)
    assert len({b.title for b in BEATS})==32
    return True
if __name__=='__main__':print('STAT12_LESSON_OK',validate(),len(BEATS),sum(len(b.voice.split()) for b in BEATS))
