"""STAT10: grouped quartiles, consistent with the previous grouped-data episodes.
All quartiles are INTERPOLATED estimates, not exact raw-data quartiles.
School convention: median of lower and upper halves for raw n=40 dataset.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import isclose, isfinite
from statistics import median
from stat01.lesson import SCORES
from stat07.lesson import CLASSES, FREQ, CUM, ASYM, ASYM_FREQ, Interval

@dataclass(frozen=True)
class Quartile:
    part: int
    n: int
    rank: float
    index: int
    before: int
    frequency: int
    left: float
    width: float
    value: float

def grouped_quantile(classes, counts, part):
    """Continuous grouped quartile interpolation at p*n/4 (p=1,2,3).
    Classes must be consecutive, positive-width, counts nonnegative integers.
    A rank exactly on an interior boundary may select the following nonempty
    class; both estimates give the same boundary value.
    """
    if part not in (1,2,3) or isinstance(part,bool):
        raise ValueError('Quartile part must be 1, 2 or 3')
    if not classes or len(classes)!=len(counts):
        raise ValueError('Nonempty intervals and counts must have equal lengths')
    if any(not isfinite(float(x)) or isinstance(x,bool) or x<0 or int(x)!=x for x in counts):
        raise ValueError('Counts must be nonnegative finite integers')
    for c in classes:
        if not isfinite(float(c.left)) or not isfinite(float(c.right)) or c.width<=0:
            raise ValueError('Invalid interval endpoints')
    for a,b in zip(classes,classes[1:]):
        if not isclose(a.right,b.left,abs_tol=1e-12,rel_tol=0):
            raise ValueError('Classes must be consecutive and not overlap')
    n=sum(counts)
    if n<=0:raise ValueError('Empty dataset')
    target=part*n/4
    before=0
    for idx,(c,f) in enumerate(zip(classes,counts)):
        if before+f>target:
            return Quartile(part,n,target,idx,before,f,c.left,c.width,
                            c.left+(target-before)*c.width/f)
        before+=f
    raise ValueError('No interval contains rank')

def three_quartiles(classes, counts):
    return tuple(grouped_quantile(classes,counts,k) for k in (1,2,3))

def school_raw_quartiles(values):
    a=sorted(values)
    if not a:raise ValueError('Empty raw dataset')
    n=len(a)
    lo=a[:n//2]
    hi=a[(n+1)//2:]
    if not lo or not hi:raise ValueError('At least two observations needed')
    return (median(lo), median(a), median(hi))

RAW=school_raw_quartiles(SCORES)
MAIN=three_quartiles(CLASSES,FREQ)
ALT=three_quartiles(ASYM,ASYM_FREQ)
IQR=MAIN[2].value-MAIN[0].value
BOUND_FREQ=(10,10,10,10)
BOUND=three_quartiles(CLASSES,BOUND_FREQ)
REVERSE_FREQ=(6,16,16,2)
REVERSE=three_quartiles(CLASSES,REVERSE_FREQ)

CHAPTERS=(
 'KHÁM PHÁ TỨ PHÂN VỊ TỪ BẢNG GHÉP NHÓM',
 'BA MỨC TÍCH LŨY 25%, 50%, 75%',
 'NỘI SUY Q1: MỘT PHẦN TƯ TRONG BẢNG',
 'NỘI SUY Q2: CÙNG LỚP, KHÁC VỊ TRÍ',
 'NỘI SUY Q3 VÀ KHOẢNG TỨ PHÂN VỊ',
 'OGIVE: ĐỌC BA PHÂN VỊ TRÊN ĐỒ THỊ',
 'RANH GIỚI LỚP VÀ THAY ĐỔI CÁCH GHÉP',
 'BÀI TOÁN NGƯỢC CÓ TẦN SỐ CHƯA BIẾT',
)

@dataclass(frozen=True)
class Beat:
    chapter:int
    step:int
    title:str
    thesis:str
    voice:str
    duration:float=34.0

ROWS=[
 [
 ('Từ bốn mươi điểm sang bốn nhóm','Mẫu gốc có Q1=6, Q2=7, Q3=8.',
 'Ở tập mười, chúng ta giữ lại bốn mươi điểm kiểm tra giả lập đã xuất hiện nhiều lần trong cả series. Khi có dữ liệu gốc, ta sắp xếp các điểm, chia thành hai nửa và tìm trung vị của từng nửa. Kết quả là Q một bằng sáu, Q hai bằng bảy và Q ba bằng tám. Đây là các tứ phân vị xác định trực tiếp, không cần nội suy. Nhưng nếu chỉ được xem bảng tần số ghép nhóm thì sao?'),
 ('Tần số sau khi ghép nhóm','Bốn lớp có tần số 6, 18, 14, 2.',
 'Bảng tần số có bốn khoảng: từ bốn đến dưới sáu, từ sáu đến dưới tám, từ tám đến dưới mười và từ mười đến dưới mười hai. Các số học sinh tương ứng là sáu, mười tám, mười bốn và hai. Tổng vẫn bằng bốn mươi, nhưng một lớp gộp nhiều giá trị. Do đó chúng ta không thể khôi phục chính xác mọi vị trí và phải nêu rõ đây là phép ước lượng.'),
 ('Tứ phân vị chia dữ liệu thế nào?','Các mức tương ứng 25%, 50% và 75%.',
 'Ba tứ phân vị đánh dấu những vị trí mà tần số tích lũy lần lượt đạt một phần tư, một nửa và ba phần tư tổng số quan sát. Khái niệm không thay đổi khi ghép nhóm. Điều thay đổi là khả năng biết chính xác vị trí nằm ở giá trị nào bên trong một khoảng. Ta sẽ tạo một phép nội suy tuyến tính, và nhìn trên hình để hiểu vì sao có độ rộng lớp trong công thức.'),
 ('Một câu hỏi kiểm chứng','Tứ phân vị ghép nhóm không nhất thiết bằng tứ phân vị gốc.',
 'Hãy thử dự đoán xem ba tứ phân vị ước lượng có bằng đúng sáu, bảy và tám hay không. Bảng chỉ biết có bao nhiêu học sinh nằm trong một khoảng, không cho biết từng điểm nằm ở đầu trái hay cuối phải của khoảng ấy. Vì thế các số tính được từ bảng có thể khác dữ liệu gốc. Điều quan trọng là phải nói đúng chúng ta đang đo dữ liệu gốc hay đang ước lượng bằng mô hình.'),
 ],
 [
 ('Đọc dãy tích lũy','6 → 24 → 38 → 40.',
 'Ta bắt đầu bằng cách cộng dồn tần số. Hết lớp thứ nhất có sáu quan sát. Hết lớp thứ hai tăng lên hai mươi bốn. Hết lớp thứ ba có ba mươi tám, và hết lớp cuối là bốn mươi. Dãy tích lũy không giảm. Mỗi mốc sẽ giúp chúng ta xác định lớp chứa một tứ phân vị, thay vì chọn lớp có tần số lớn nhất hay đoán theo chiều cao cột.'),
 ('Đặt ba mốc vị trí','n/4=10, n/2=20, 3n/4=30.',
 'Vì cỡ mẫu là bốn mươi, một phần tư tổng số là mười, một nửa là hai mươi, còn ba phần tư là ba mươi. Lưu ý đây là số quan sát tích lũy mục tiêu, không phải điểm kiểm tra. Cũng không nên nhầm với vị trí tính tứ phân vị của dữ liệu thô trong từng quy ước sách giáo khoa. Trong công thức nội suy ghép nhóm, chúng ta dùng chính ba mức này.'),
 ('Tìm lớp Q1 và Q2','Cả hai đều thuộc lớp [6;8).',
 'Mức mười và hai mươi đều lớn hơn sáu, nhưng chưa vượt hai mươi bốn. Vậy Q một và Q hai cùng nằm trong lớp thứ hai, từ sáu đến dưới tám. Đây là điểm dễ gây ngạc nhiên: dù hai tứ phân vị ở mức tích lũy khác nhau, chúng vẫn có thể thuộc cùng một lớp khi lớp ấy chứa nhiều quan sát. Vì thế phải tính riêng tỷ phần nội suy cho từng vị trí.'),
 ('Tìm lớp Q3','Mốc 30 thuộc lớp [8;10).',
 'Sau lớp thứ hai chúng ta có hai mươi bốn quan sát, chưa tới ba mươi. Sau lớp thứ ba thì có ba mươi tám, nên mức ba mươi thuộc khoảng tám đến dưới mười. Tóm lại, hai tứ phân vị đầu nằm trong lớp thứ hai, còn tứ phân vị ba ở lớp thứ ba. Việc chọn đúng lớp là điều kiện trước tiên để mọi phép thế số tiếp theo có ý nghĩa.'),
 ],
 [
 ('Định vị lớp thứ hai','Cận trái 6; độ rộng 2; tần số 18.',
 'Muốn ước lượng Q một, ta bắt đầu bằng lớp từ sáu đến dưới tám. Cận dưới lớp là sáu và độ rộng lớp là hai điểm. Lớp này chứa mười tám học sinh. Trước khi đến lớp ấy, tổng tích lũy bằng sáu. Bốn con số phải được chỉ đúng trên hình: sáu của cận trái, hai của độ rộng, mười tám của tần số và sáu của tích lũy trước lớp.'),
 ('Từ mốc 6 đến mốc 10','Cần đi 4 trong 18 quan sát của lớp.',
 'Mức mục tiêu của Q một là mười, trong khi trước lớp chỉ có sáu quan sát. Vậy ta cần đi thêm bốn quan sát bên trong lớp thứ hai. Lớp có mười tám quan sát nên tỷ phần cần đi là bốn phần mười tám. Mô hình nội suy giả định tích lũy tăng đều khi di chuyển theo chiều ngang của lớp. Tỷ phần số quan sát được đổi thành tỷ phần độ dài.'),
 ('Công thức và kết quả Q1','Q1 ≈ 6 + (10−6)/18 × 2 = 6,44.',
 'Lấy cận trái sáu cộng với bốn chia mười tám rồi nhân độ rộng hai, ta được sáu phẩy bốn bốn khi làm tròn hai chữ số thập phân. Vạch Q một nằm ở gần đầu trái của lớp sáu đến tám, như hình đang hiển thị. Ta cũng kiểm tra sáu phẩy bốn bốn lớn hơn sáu và nhỏ hơn tám; nếu nằm ngoài lớp đã chọn thì chắc chắn có sai sót khi thế số.'),
 ('Vì sao không lấy Q1 bằng 6?','Giá trị 6 thuộc dữ liệu gốc, không phải giá trị nội suy.',
 'Với bốn mươi điểm gốc, tứ phân vị thứ nhất chính xác là sáu. Nhưng từ bảng ghép nhóm, phương pháp nội suy cho khoảng sáu phẩy bốn bốn. Hai con số không phải là hai đáp án cho cùng một nguồn thông tin: một con số dựa trên các giá trị quan sát cụ thể, con số còn lại dựa trên giả định phân bố trong lớp. Em cần ghi ký hiệu xấp xỉ khi làm việc với bảng ghép nhóm.'),
 ],
 [
 ('Q2 cũng thuộc lớp [6;8)','Độ rộng 2, tần số 18, tích lũy trước 6.',
 'Bây giờ chuyển sang Q hai, tức trung vị của bảng ghép nhóm. Ta vẫn sử dụng lớp sáu đến dưới tám, vẫn có mười tám quan sát, và số tích lũy trước lớp vẫn bằng sáu. Điều khác biệt là mức mục tiêu không còn là mười mà là hai mươi. Hãy giữ nguyên hình lớp và chỉ thay vị trí của vạch ngang tích lũy; nhờ vậy ta thấy công thức thay đổi ở đúng tử số.'),
 ('Q2 đi xa hơn Q1','Cần đi 14 trong 18 quan sát.',
 'Từ số tích lũy sáu để đạt hai mươi, ta cần thêm mười bốn quan sát bên trong lớp. Tỷ lệ mười bốn trên mười tám lớn hơn tỷ lệ bốn trên mười tám của Q một. Vì vậy vạch Q hai tiến xa về bên phải trong cùng đoạn từ sáu đến tám. Đây là chuyển động mang ý nghĩa toán học: vị trí thay đổi theo số quan sát tích lũy, chứ không phải theo một hiệu ứng trang trí.'),
 ('Kết quả nội suy Q2','Q2 ≈ 6 + (20−6)/18 × 2 = 7,56.',
 'Lấy sáu cộng mười bốn phần mười tám nhân hai, ta được bảy phẩy năm sáu. Kết quả trùng với phép nội suy trung vị mà ta đã học ở Video chín. Vì ba tứ phân vị được tính từ cùng mô hình tích lũy nên Q hai chính là trung vị ghép nhóm, không có một công thức hoàn toàn mới. Giá trị này vẫn là ước lượng, khác trung vị chính xác bằng bảy.'),
 ('So sánh Q1 với Q2','6,44 < 7,56; cùng lớp nhưng khác tỷ phần.',
 'Trên hình, Q một và Q hai đều nằm giữa sáu và tám, nhưng Q hai ở bên phải Q một. Đây là điều bắt buộc vì mức tích lũy năm mươi phần trăm cao hơn mức hai mươi lăm phần trăm. Nếu phép tính làm Q một lớn hơn Q hai, ta đã có một dấu hiệu để kiểm tra lại dữ liệu hoặc việc chọn lớp. Một quy tắc kiểm soát rất quan trọng là Q một không vượt Q hai.'),
 ],
 [
 ('Q3 chuyển sang lớp thứ ba','Cận trái 8, trước lớp 24, tần số 14.',
 'Khi tìm Q ba, mức mục tiêu là ba mươi. Sau lớp thứ hai mới tích lũy được hai mươi bốn, vì thế phải sang lớp thứ ba, từ tám đến dưới mười. Cận trái của lớp thứ ba là tám, độ rộng bằng hai, tần số bằng mười bốn và tích lũy trước lớp bằng hai mươi bốn. Chúng ta tuyệt đối không dùng tần số mười tám của lớp Q hai.'),
 ('Mốc 30 nằm ở đâu trong lớp?','Cần đi 6 trong 14 quan sát.',
 'Để tăng từ hai mươi bốn lên ba mươi, ta cần đi sáu trong tổng mười bốn quan sát của lớp thứ ba. Như vậy tỷ phần chiều dài theo nội suy là sáu trên mười bốn, tương đương ba trên bảy. Trên trục từ tám tới mười, vạch Q ba nằm chưa đến giữa lớp. Việc nhìn độ dài giúp học sinh phát hiện nhanh nếu một phép tính nhầm cho kết quả lớn hơn cận phải.'),
 ('Hoàn tất ba tứ phân vị','Q3 ≈ 8,86; bộ ba ≈ 6,44; 7,56; 8,86.',
 'Lấy tám cộng sáu phần mười bốn nhân hai, ta được tám phẩy tám sáu khi làm tròn. Bộ ba giá trị ước lượng là sáu phẩy bốn bốn, bảy phẩy năm sáu và tám phẩy tám sáu. Chúng theo đúng thứ tự tăng dần và thuộc các lớp đã xác định. Ta đã hoàn thành mục tiêu đầu tiên: từ một bảng tần số, xác định ba vị trí và nội suy ba giá trị.'),
 ('Khoảng tứ phân vị ước lượng','IQR ≈ 8,86 − 6,44 = 2,41.',
 'Khoảng tứ phân vị bằng Q ba trừ Q một. Nếu giữ giá trị chính xác trước khi làm tròn, phép trừ cho kết quả khoảng hai phẩy bốn một. Em lưu ý không trừ hai số đã làm tròn rồi khẳng định được một kết quả tuyệt đối chính xác; đây vẫn là giá trị ước lượng. Với dữ liệu gốc, IQR bằng tám trừ sáu, tức hai, nên ghép nhóm đã tạo ra chênh lệch.'),
 ],
 [
 ('Từ bảng sang đường tích lũy','Các đỉnh đường gấp khúc là (4,0),(6,6),(8,24),(10,38),(12,40).',
 'Đường tần số tích lũy đặt ranh giới lớp lên trục ngang và số quan sát tích lũy lên trục dọc. Bắt đầu tại bốn với mức không; tới sáu có sáu; tới tám có hai mươi bốn; tới mười có ba mươi tám; và tới mười hai có đủ bốn mươi. Nối các điểm bằng đoạn thẳng tức là dùng đúng mô hình nội suy tuyến tính trong từng lớp.'),
 ('Đường ngang 25 phần trăm','Mức 10 cắt đường tại Q1 ≈ 6,44.',
 'Ta kẻ đường ngang qua mức tích lũy mười, tương ứng một phần tư cỡ mẫu. Đường ấy cắt đoạn từ mức sáu lên hai mươi bốn. Hạ vuông góc xuống trục hoành sẽ tìm được khoảng sáu phẩy bốn bốn. Cảnh này kiểm chứng trực quan công thức Q một, bởi hệ số góc của đoạn đường tích lũy chính là tần số lớp chia cho độ rộng lớp.'),
 ('Đường ngang 50 và 75 phần trăm','Mức 20 cho Q2; mức 30 cho Q3.',
 'Ta tiếp tục kẻ hai đường ngang qua mức hai mươi và ba mươi. Mức hai mươi cắt cùng đoạn với Q một nhưng xa hơn về bên phải. Mức ba mươi cắt đoạn kế tiếp, ứng với lớp từ tám đến mười. Ba giao điểm được hạ xuống trục ngang tạo thành ba vạch tứ phân vị. Nhờ hình động, học sinh có thể tự ước lượng trước khi kết quả số được ghi chính xác.'),
 ('Tự đọc biểu đồ và kiểm tra','Q1 ≤ Q2 ≤ Q3; lớp và tích lũy phải khớp.',
 'Khi đọc ogive, không chọn điểm cao nhất của cột như khi tìm lớp mốt. Ta tìm độ cao tích lũy thích hợp, đọc hoành độ giao điểm rồi kiểm tra thuộc lớp nào. Nếu bảng cho phân lớp rộng khác nhau, đoạn trên đồ thị có hệ số góc khác nhau; không nên dùng một tỷ lệ chiều dài chung cho mọi lớp. Cách đọc đồ thị và cách nội suy đại số phải cho cùng kết quả.'),
 ],
 [
 ('Khi phần tư trùng đúng biên','Với tần số 10,10,10,10: Q1=6, Q2=8, Q3=10.',
 'Ta chuyển sang một ví dụ đặc biệt có bốn lớp cùng độ rộng hai, mỗi lớp chứa mười quan sát. Khi đó các mức mười, hai mươi và ba mươi trùng đúng tần số tích lũy ở cuối ba lớp đầu. Giá trị nội suy tương ứng là chính ba ranh giới sáu, tám và mười. Đây không phải là trường hợp công thức hỏng; ta chỉ cần hiểu rằng biên phải lớp trước cũng là biên trái lớp kế tiếp.'),
 ('Hai cách chọn lớp ở ranh giới','Cùng một ranh giới cho cùng giá trị.',
 'Khi một mức mục tiêu trùng đúng điểm tích lũy giữa hai lớp có số quan sát dương, ta có thể nội suy đến hết lớp bên trái hoặc bắt đầu từ lớp bên phải. Cả hai đều dẫn tới cùng hoành độ ranh giới. Trong code, tôi sẽ chọn lớp không rỗng tiếp theo để tránh chia cho tần số không. Nếu có một lớp trống ở giữa, kết quả nội suy phải được hiểu thận trọng hơn: bảng không xác định một vị trí duy nhất trong đoạn phẳng của đường tích lũy.'),
 ('Đổi ranh giới, đổi ước lượng','Bảng khác cho Q1=6,5; Q2≈7,67; Q3≈8,78.',
 'Với cùng bốn mươi điểm gốc, ta thử đổi thành các lớp từ bốn đến dưới sáu, sáu đến dưới bảy, bảy đến dưới chín, và chín đến dưới mười một. Tần số trở thành sáu, tám, mười tám và tám. Phép nội suy mới cho Q một bằng sáu phẩy năm, Q hai khoảng bảy phẩy sáu bảy và Q ba khoảng tám phẩy bảy tám. Thay bảng ghép nhóm đã làm thay đổi các ước lượng, dù dữ liệu thật vẫn giữ nguyên.'),
 ('Kiểm tra lại tính nhất quán','Các tứ phân vị luôn không giảm.',
 'Trước khi kết thúc phần lý thuyết, hãy kiểm tra cỡ mẫu, tổng tần số, tần số tích lũy và ba lớp đã chọn. Các giá trị ước lượng phải theo thứ tự không giảm và nằm trong phạm vi các khoảng quan sát. Không được nhầm tứ phân vị của dữ liệu gốc với tứ phân vị ước lượng từ bảng. Nếu bảng có lớp tần số bằng không, một số vị trí biên có thể không xác định duy nhất khi chỉ dựa trên đường tích lũy.'),
 ],
 [
 ('Bài ngược: tìm tần số x','Tần số là 6, x, 32−x, 2; n=40.',
 'Bài toán cuối có bốn lớp quen thuộc, nhưng tần số lớp thứ hai chưa biết, gọi là x. Bốn tần số lần lượt là sáu, x, ba mươi hai trừ x và hai, nên tổng bằng bốn mươi. Biết Q một nội suy bằng sáu phẩy năm, hãy tìm x, sau đó xác định Q hai, Q ba và khoảng tứ phân vị. Đây là một bài toán ngược, buộc ta hiểu vì sao các đại lượng được đưa vào công thức.'),
 ('Tạo phương trình từ Q1','6 + (10−6)×2/x = 6,5.',
 'Vì Q một bằng sáu phẩy năm thuộc lớp từ sáu đến dưới tám, đó phải là lớp thứ hai và có tần số x. Trước lớp ấy có sáu quan sát; mức mục tiêu là mười. Phương trình nội suy sáu cộng bốn trên x nhân hai bằng sáu phẩy năm. Chuyển vế cho tám trên x bằng không phẩy năm, ta tìm được x bằng mười sáu. Tần số lớp thứ ba cũng bằng mười sáu.'),
 ('Tìm Q2 và Q3 theo bảng mới','Q2 = 7,75; Q3 = 9.',
 'Bảng mới có tần số sáu, mười sáu, mười sáu và hai; tích lũy lần lượt sáu, hai mươi hai, ba mươi tám và bốn mươi. Mức hai mươi của Q hai vẫn thuộc lớp thứ hai: nội suy sáu cộng mười bốn chia mười sáu nhân hai bằng bảy phẩy bảy lăm. Mức ba mươi của Q ba thuộc lớp thứ ba, nội suy tám cộng tám chia mười sáu nhân hai bằng chín.'),
 ('Kết luận và tự kiểm tra','Q1=6,5; Q2=7,75; Q3=9; IQR=2,5.',
 'Kết quả bài ngược là x bằng mười sáu, bộ ba tứ phân vị lần lượt sáu phẩy năm, bảy phẩy bảy lăm và chín, còn khoảng tứ phân vị bằng hai phẩy năm. Hãy kiểm tra lại bằng bảng tích lũy vừa thu được. Qua video này, em cần nhớ đúng quy trình: xác định mức một phần tư, một nửa và ba phần tư; xác định lớp; đọc số tích lũy trước lớp; cuối cùng mới nội suy. Hiểu được hình sẽ tránh nhiều lỗi hơn học thuộc công thức.'),
 ],
]
BEATS=tuple(Beat(i+1,j+1,*r) for i,ch in enumerate(ROWS) for j,r in enumerate(ch))

def validate():
    assert len(BEATS)==32 and len(CHAPTERS)==8
    assert len(set(b.title for b in BEATS))==32
    assert all(len(b.voice.split())>48 for b in BEATS)
    assert sum(b.duration for b in BEATS)==1088
    assert RAW==(6,7,8)
    assert tuple(CUM)==(6,24,38,40)
    assert isclose(MAIN[0].value,58/9) and isclose(MAIN[1].value,68/9)
    assert isclose(MAIN[2].value,62/7) and isclose(IQR,152/63)
    assert tuple(x.index for x in MAIN)==(1,1,2)
    assert tuple(x.index for x in BOUND)==(1,2,3)
    assert tuple(x.value for x in BOUND)==(6,8,10)
    assert REVERSE_FREQ==(6,16,16,2)
    assert all(isclose(x.value,v) for x,v in zip(REVERSE,(6.5,7.75,9)))
    return True

if __name__=='__main__':
    print('STAT10_LESSON_OK',validate(),'beats',len(BEATS),'words',sum(len(b.voice.split()) for b in BEATS))
