"""STAT14: practical statistics decision lab; source of truth and Vietnamese narration.
All samples are synthetic. Descriptive variances use divisor n. Quartile method:
median of lower/upper halves (exclude whole median for odd n).
"""
from __future__ import annotations
from dataclasses import dataclass
from math import isclose, fsum, isfinite
from stat13.lesson import profile
from stat01.lesson import SCORES
from stat07.lesson import CLASSES, FREQ
from stat12.lesson import grouped_stats

# Waiting times in minutes: two different counters, 10 observed visitors each.
QUEUE_A=(6,7,7,8,8,8,8,9,9,10)
QUEUE_B=(2,3,5,7,8,8,9,10,13,15)
PA=profile(QUEUE_A)
PB=profile(QUEUE_B)
# Change one 10-minute observation to 30 minutes, no invented resampling.
QUEUE_OUTLIER=QUEUE_A[:-1]+(30,)
PO=profile(QUEUE_OUTLIER)
# Distinguish statistics calculated on 40 raw points versus grouped approximation.
RAW=profile(SCORES)
GROUPED=grouped_stats(CLASSES,FREQ)
# Two class sizes and means: correct combined mean 6.5, not (8+6)/2=7.
COHORTS=((10,8.0),(30,6.0))
# Independent practice, times in minutes, n=8 each.
EXERCISE_A=(6,7,7,8,8,8,9,11)
EXERCISE_B=(2,5,7,8,8,9,11,14)
EA=profile(EXERCISE_A)
EB=profile(EXERCISE_B)

def count_at_most(values, limit):
    if not isfinite(float(limit)): raise ValueError('Non-finite limit')
    return sum(v<=limit for v in values)

def weighted_mean(groups):
    if not groups:raise ValueError('Missing groups')
    if any(isinstance(n,bool) or not isinstance(n,int) or n<=0 or
           isinstance(m,bool) or not isinstance(m,(float,int)) or not isfinite(m)
           for n,m in groups):
        raise ValueError('Expected positive integer counts and finite means')
    return fsum(n*m for n,m in groups)/sum(n for n,m in groups)

def decision(a,b,objective,threshold=None):
    """A report about *observed* data only, not future probabilities."""
    if objective=='consistency':
        aa,bb=profile(a).sd,profile(b).sd
        return ('A' if aa<bb else 'B' if bb<aa else 'TIE',aa,bb)
    if objective=='at_most':
        if threshold is None:raise ValueError('Threshold required')
        aa,bb=count_at_most(a,threshold),count_at_most(b,threshold)
        return ('A' if aa>bb else 'B' if bb>aa else 'TIE',aa,bb)
    raise ValueError('Unknown objective')

@dataclass(frozen=True)
class Beat:
    chapter:int
    step:int
    title:str
    thesis:str
    voice:str
    duration:float=36.0

CHAPTERS=(
 'BÀI TOÁN THỰC TẾ: CHỌN QUẦY PHỤC VỤ',
 'PHÂN TÍCH ĐỘ PHÂN TÁN',
 'ĐỔI MỤC TIÊU, ĐỔI QUYẾT ĐỊNH',
 'ĐIỂM BẤT THƯỜNG VÀ CHỈ SỐ BỀN VỮNG',
 'DỮ LIỆU GỐC, GHÉP NHÓM VÀ SAI SỐ',
 'GỘP HAI NHÓM: TRỌNG SỐ VÀ QUY MÔ',
 'BÁO CÁO THỐNG KÊ CÓ TRÁCH NHIỆM',
 'THỬ THÁCH TỔNG HỢP CÓ LỜI GIẢI',
)

# A single voice paragraph per *internal* beat. No beat number should appear on screen.
ROWS=[
 [
 ('Hai quầy phục vụ, một câu hỏi','Cùng trung bình chưa chắc cùng chất lượng phục vụ.',
  'Một thư viện khảo sát thời gian chờ của mười lượt khách tại mỗi quầy A và B. Bảng thời gian được đo bằng phút, đã sắp theo thứ tự tăng dần để tiện theo dõi. Nếu chỉ có một chỉ số để chọn quầy, em sẽ xem số trung bình hay thời gian lâu nhất? Trước hết hãy đọc dữ liệu và đặt tiêu chí rõ ràng.'),
 ('Đặt hai dãy thời gian cạnh nhau','Quầy A tập trung quanh tám phút; quầy B trải rộng.',
  'Ở quầy A, các quan sát từ sáu đến mười phút, nhiều lần bằng tám. Ở quầy B, khách nhanh nhất đợi hai phút, còn có khách phải đợi đến mười lăm phút. Chúng ta vẽ các điểm trên cùng trục phút, không tùy ý thay đổi tỉ lệ trục để làm sự khác biệt trông lớn hơn hoặc nhỏ đi.'),
 ('Tính trung bình và trung vị','Cả hai quầy cùng trung bình 8 phút, trung vị 8 phút.',
  'Tổng thời gian chờ tại mỗi quầy đều bằng tám mươi phút. Chia cho mười lượt khảo sát, cả hai quầy cùng trung bình tám phút. Giá trị giữa, tức trung vị, của mỗi dãy cũng bằng tám. Hai con số trung tâm đều giống nhau, nhưng điều đó chưa cho phép ta nói rằng trải nghiệm của mọi lượt khách là giống nhau.'),
 ('Nêu mục tiêu trước khi tính','Đồng đều, nhanh nhất hay đúng hạn là ba tiêu chí khác nhau.',
  'Nếu quản lý muốn thời gian phục vụ ổn định, cần xem độ phân tán. Nếu khách mong có cơ hội được phục vụ cực nhanh, hãy đếm những lượt chờ không quá năm phút. Nếu thư viện cam kết chờ không quá mười phút, ta phải đếm lượt đạt cam kết. Bài toán vận dụng bắt đầu bằng việc xác định rõ điều cần đánh giá.'),
 ],
 [
 ('So sánh khoảng biến thiên','A: R=4 phút; B: R=13 phút.',
  'Khoảng biến thiên bằng thời gian lớn nhất trừ thời gian nhỏ nhất. Quầy A có khoảng biến thiên mười trừ sáu, bằng bốn phút. Quầy B có khoảng biến thiên mười lăm trừ hai, bằng mười ba phút. Đây là một tín hiệu quầy B biến động mạnh hơn, nhưng khoảng biến thiên chỉ dựa vào hai giá trị ở hai đầu.'),
 ('Dùng biểu đồ hộp cùng một trục','A có Q1=7, Q3=9; B có Q1=5, Q3=10.',
  'Sử dụng quy ước tứ phân vị lấy trung vị mỗi nửa dữ liệu. Với quầy A, tứ phân vị thứ nhất bằng bảy và thứ ba bằng chín, nên hộp dài hai phút. Với B, hai mốc đó là năm và mười, hộp dài năm phút. Hãy quan sát hai hộp đặt trên cùng trục, tuyệt đối không kéo co giãn một hình để gây hiểu nhầm.'),
 ('Phương sai và độ lệch chuẩn','A: s²=1,2; B: s²=15, đơn vị bình phương phút.',
  'Cả hai quầy cùng trung bình tám phút. Lấy từng quan sát trừ tám, bình phương rồi lấy trung bình cộng, ta thu được phương sai của A bằng một phẩy hai, còn B bằng mười lăm. Công thức đang dùng mẫu số n trong thống kê mô tả. Đơn vị của phương sai là phút bình phương, không phải phút.'),
 ('Kết luận đúng tiêu chí đồng đều','s(A)≈1,095 phút; s(B)≈3,873 phút.',
  'Lấy căn bậc hai để đưa về đơn vị phút, độ lệch chuẩn của A xấp xỉ một phẩy không chín năm phút, của B xấp xỉ ba phẩy tám bảy ba phút. Trong mười lượt đã khảo sát, quầy A đồng đều hơn theo độ lệch chuẩn và khoảng tứ phân vị. Đây là kết luận mô tả mẫu quan sát, chưa phải bảo đảm cho những ngày tiếp theo.'),
 ],
 [
 ('Đặt mục tiêu không quá 10 phút','A: 10/10; B: 8/10 lượt đạt.',
  'Thư viện đưa ra cam kết thời gian chờ không quá mười phút. Đếm trực tiếp từ dãy số, cả mười lượt ở quầy A đều đạt, còn quầy B chỉ có tám trong mười lượt đạt. Như vậy theo tiêu chí duy trì cam kết trong mẫu quan sát, A tốt hơn B. Ta không cần dùng trung bình hay độ lệch chuẩn để thay cho phép đếm đúng ngưỡng.'),
 ('Đặt mục tiêu được phục vụ rất nhanh','Không quá 5 phút: A có 0 lượt, B có 3 lượt.',
  'Một vị khách lại quan tâm đến những lần chờ rất ngắn, chẳng hạn không quá năm phút. Quầy A không có lượt nào đạt, nhưng quầy B có ba lượt: hai, ba và năm phút. Với tiêu chí này, quầy B có nhiều lượt nhanh hơn trong mẫu. Kết luận thay đổi do mục tiêu thay đổi, không phải vì dữ liệu bị đổi.'),
 ('Hai mục tiêu, hai câu trả lời','Không tồn tại một quầy luôn tốt hơn ở mọi tiêu chí.',
  'Đặt hai ngưỡng năm phút và mười phút lên cùng biểu đồ. Ở ngưỡng năm, B có ba lượt đạt so với không lượt của A; ở ngưỡng mười, A có mười lượt so với tám lượt của B. Việc chọn chỉ số đúng quan trọng hơn tìm ra một câu trả lời nghe có vẻ tuyệt đối. Hãy luôn nói rõ mình đang tối ưu điều gì.'),
 ('Không biến tần suất mẫu thành lời hứa','Tỉ lệ quan sát không tự động là xác suất tương lai.',
  'Mười lượt được quan sát ở từng quầy chưa đủ để khẳng định trong tương lai khách sẽ luôn đợi không quá mười phút tại A. Các con số mười trên mười và tám trên mười là tần suất trong dữ liệu đang xét. Muốn ước lượng cho thời gian dài hơn, cần cách lấy mẫu phù hợp, thêm quan sát và xem thời điểm đông khách.'),
 ],
 [
 ('Khi một lượt chờ thành 30 phút','Thay đúng một giá trị 10 bằng 30.',
  'Giả sử trong dữ liệu quầy A, một lượt vốn chờ mười phút được thay bằng một lượt phải chờ ba mươi phút. Mọi lượt còn lại được giữ nguyên. Trên hình, chỉ một điểm dịch về bên phải. Ta không bỏ qua giá trị này hay chỉnh sửa dữ liệu để có kết luận đẹp, mà thử xem mỗi đại lượng thống kê phản ứng như thế nào.'),
 ('Số trung bình nhạy với ngoại lệ','Trung bình từ 8 lên 10 phút.',
  'Ban đầu tổng thời gian của A là tám mươi phút. Khi thay mười bằng ba mươi, tổng tăng thêm hai mươi thành một trăm phút; trung bình của mười lượt thành mười phút. Số trung bình tăng hai phút, dù chín lượt khác không hề thay đổi. Đây là lý do cần kiểm tra các giá trị rất lớn trước khi dùng trung bình để mô tả trải nghiệm điển hình.'),
 ('Trung vị và IQR vẫn ổn định','Trung vị 8 phút, IQR 2 phút không đổi.',
  'Sắp xếp dãy sau thay đổi, hai giá trị giữa vẫn là tám nên trung vị không đổi. Trung vị nửa dưới vẫn bằng bảy và nửa trên vẫn bằng chín, do đó khoảng tứ phân vị cũng giữ nguyên hai phút. Điều này không có nghĩa trung vị và IQR không bao giờ thay đổi, mà cho thấy chúng ít nhạy hơn trong phép thay một giá trị cụ thể này.'),
 ('Độ lệch chuẩn tăng rất mạnh','Phương sai tăng từ 1,2 lên 45,2.',
  'Tính lại bình phương độ lệch quanh trung bình mới là mười phút, phương sai của A sau thay đổi bằng bốn mươi lăm phẩy hai. Giá trị này lớn hơn rất nhiều so với một phẩy hai ban đầu, vì khoảng cách tới ba mươi được bình phương. Khi báo cáo, hãy ghi cả trung vị, IQR và các số đo nhạy với ngoại lệ để không che khuất đặc điểm dữ liệu.'),
 ],
 [
 ('Đọc lại 40 điểm gốc','Dữ liệu gốc có trung bình 7,1.',
  'Chuyển sang bộ bốn mươi điểm kiểm tra quen thuộc của Series. Nếu giữ đủ từng điểm gốc, chúng ta tính được trung bình chính xác bằng bảy phẩy một. Khi đã biết dữ liệu thô, phép tính này không cần giả sử mỗi quan sát nằm ở trung điểm lớp. Bây giờ thử thay bảng thô bằng bảng ghép nhóm để thấy thông tin nào bị mất.'),
 ('Ước lượng bằng trung điểm lớp','Trung bình ghép nhóm 7,6, không phải 7,1.',
  'Bốn lớp điểm có trung điểm năm, bảy, chín và mười một; tần số tương ứng sáu, mười tám, mười bốn và hai. Lấy tổng các tích trung điểm với tần số rồi chia bốn mươi, ta được bảy phẩy sáu. Kết quả này không sai: nó là giá trị ước lượng sau khi thay mọi điểm trong lớp bằng trung điểm.'),
 ('Phương sai cũng chỉ là ước lượng','Gốc: 2,29; từ trung điểm lớp: 2,44.',
  'Tính trên bốn mươi điểm gốc, phương sai là hai phẩy hai chín. Nếu chỉ dùng trung điểm của các lớp, phương sai ghép nhóm bằng hai phẩy bốn bốn. Chênh lệch không do đổi công thức chia n, mà do phép đại diện các giá trị trong lớp. Trong bài giải, phải ghi rõ đại lượng nào tính từ dữ liệu thô và đại lượng nào ước lượng từ bảng ghép.'),
 ('Không thể khôi phục chính xác','Bảng tần số không cho biết từng điểm bên trong lớp.',
  'Một bảng ghép nhóm có thể được tạo ra từ nhiều dãy số khác nhau. Khi chỉ biết sáu quan sát ở lớp từ bốn đến dưới sáu, ta không biết từng quan sát cụ thể. Do đó không được khẳng định chắc chắn trung bình gốc bằng trung bình trung điểm lớp. Quy tắc thực hành là nêu nguồn dữ liệu, đánh dấu rõ ước lượng và tránh suy luận quá mức.'),
 ],
 [
 ('Hai nhóm học sinh quy mô khác nhau','Nhóm A: 10 em, trung bình 8; B: 30 em, trung bình 6.',
  'Một trường cần tính trung bình điểm kiểm tra của hai nhóm học sinh. Nhóm A có mười em với trung bình tám, nhóm B có ba mươi em với trung bình sáu. Vì số học sinh khác nhau, ta không thể tùy tiện lấy tám cộng sáu rồi chia hai để coi đó là trung bình chung của bốn mươi em.'),
 ('Vì sao trung bình của hai số là sai','Lấy (8+6)/2=7 bỏ qua quy mô nhóm.',
  'Nếu lấy trung bình của hai mức trung bình, ta thu được bảy. Cách này ngầm coi hai nhóm có trọng số bằng nhau, trong khi nhóm B có số học sinh gấp ba A. Muốn tìm trung bình cho toàn bộ bốn mươi em, phải khôi phục tổng điểm từng nhóm bằng cỡ mẫu nhân trung bình rồi chia theo tổng số học sinh.'),
 ('Tính trung bình có trọng số','(10×8+30×6)/40 = 6,5.',
  'Tổng điểm nhóm A là tám mươi; nhóm B là một trăm tám mươi. Tổng cộng hai trăm sáu mươi điểm cho bốn mươi học sinh. Chia hai trăm sáu mươi cho bốn mươi, trung bình chung đúng là sáu phẩy năm. Trên biểu đồ, khối nhóm ba mươi học sinh phải dài gấp ba khối mười học sinh, để trực quan khớp số liệu.'),
 ('Quy tắc khi gộp nhiều nhóm','Trọng số chính là số quan sát của từng nhóm.',
  'Với nhiều nhóm, công thức trung bình chung là tổng cỡ mẫu nhân trung bình của từng nhóm, chia tổng cỡ mẫu. Mỗi học sinh chỉ được tính đúng một lần. Nếu bảng chỉ cho phần trăm, phải kiểm tra các phần trăm cùng cơ sở. Đây là kỹ năng đặc biệt quan trọng khi tổng hợp báo cáo giữa các lớp hoặc các đợt khảo sát không cùng quy mô.'),
 ],
 [
 ('Bước một: nêu dữ liệu và phạm vi','Dữ liệu được ghi theo phút, mẫu chỉ gồm 10 lượt/quầy.',
  'Một báo cáo đáng tin cậy cần nói đang đo đại lượng gì, đơn vị nào và khảo sát được bao nhiêu lượt. Trong tình huống này, chúng ta có mười thời gian chờ được ghi ở mỗi quầy, đơn vị là phút. Số liệu giả lập này chỉ dùng để học cách phân tích, không đại diện cho hoạt động của một thư viện thật.'),
 ('Bước hai: chọn thước đo theo mục tiêu','Ổn định dùng độ phân tán; đúng hạn dùng tỉ lệ đạt ngưỡng.',
  'Đừng lập báo cáo chỉ bằng một bảng toàn công thức. Nếu cần xét sự đồng đều, hãy so sánh độ lệch chuẩn và IQR trên cùng đơn vị. Nếu cần kiểm tra cam kết, hãy đếm số lượt không quá giới hạn. Nếu dữ liệu có ngoại lệ, cân nhắc trung vị và IQR bên cạnh trung bình. Thước đo phải phục vụ câu hỏi cần trả lời.'),
 ('Bước ba: kiểm tra giả định và cách đo','Không suy nhân quả từ vài quan sát mô tả.',
  'Hai quầy có thể được quan sát vào những khung giờ khác nhau, khi lượng khách khác nhau hoặc quy trình phục vụ khác nhau. Bản thống kê mô tả không chứng minh quầy nào vận hành tốt hơn trong mọi điều kiện. Muốn tìm nguyên nhân, cần một thiết kế thu thập dữ liệu phù hợp, kiểm soát các yếu tố khác và quan sát đủ rộng.'),
 ('Viết kết luận có điều kiện','Nói trong mẫu này, theo tiêu chí này.',
  'Một kết luận gọn và chặt chẽ là: trong mười lượt khảo sát tại mỗi quầy, hai trung bình cùng bằng tám phút; A có độ lệch chuẩn thấp hơn và mười trên mười lượt đạt ngưỡng mười phút, trong khi B có tám. Nhưng B có ba lượt chờ không quá năm phút còn A không có. Mọi nhận xét cần gắn rõ tiêu chí.'),
 ],
 [
 ('Bài tập: hai phương án giao hàng','Hai dãy 8 thời gian chờ; cần chọn phương án ổn định.',
  'Đến thử thách cuối, hãy xem hai phương án giao hàng giả lập C và D, mỗi phương án có tám thời gian thực hiện tính bằng phút. Nhiệm vụ đầu tiên là kiểm tra tổng và trung bình; sau đó tìm trung vị, khoảng biến thiên, tứ phân vị và phương sai. Trước khi hiện lời giải, em nên tự ghi dự đoán phương án nào ổn định hơn.'),
 ('Tính tâm và các cực trị','C và D cùng trung bình 8, trung vị 8.',
  'Tổng thời gian mỗi phương án đều bằng sáu mươi bốn phút, vì thế trung bình đều bằng tám. Trung vị của cả hai cũng bằng tám. Tuy nhiên C trải từ sáu đến mười một, còn D trải từ hai đến mười bốn. Khoảng biến thiên của C là năm và của D là mười hai. Chỉ riêng điều đó đã cho thấy sự khác biệt đáng quan sát.'),
 ('Giải thích IQR và phương sai','C: IQR=1,5, s²=2; D: IQR=4, s²=11,5.',
  'Theo cách lấy trung vị của mỗi nửa, phương án C có tứ phân vị thứ nhất là bảy và thứ ba là tám phẩy năm, khoảng tứ phân vị một phẩy năm. Với D, hai mốc lần lượt là sáu và mười, IQR bằng bốn. Tính bình phương độ lệch rồi chia tám, phương sai của C bằng hai, còn D bằng mười một phẩy năm.'),
 ('Lựa chọn và viết kết luận hoàn chỉnh','C ổn định hơn trong mẫu; nêu rõ tiêu chí.',
  'Theo tiêu chí ổn định trong tám lần ghi nhận, phương án C có cả IQR và phương sai nhỏ hơn nên là lựa chọn phù hợp hơn. Nhưng nếu mục tiêu là tìm một số lần giao cực nhanh dưới năm phút, D có những trường hợp mà C không có. Bài học kết thúc bằng quy trình: đọc đúng dữ liệu, chọn đúng chỉ số, tính đúng và phát biểu kết luận có giới hạn.'),
 ],
]
BEATS=tuple(Beat(i+1,j+1,*r) for i,group in enumerate(ROWS) for j,r in enumerate(group))

def validate():
    assert len(CHAPTERS)==8 and len(ROWS)==8 and len(BEATS)==32
    assert len({b.title for b in BEATS})==32 and all(len(row)==4 for row in ROWS)
    assert all(len(b.voice.split())>=45 for b in BEATS)
    assert isclose(PA.mean,8) and isclose(PB.mean,8)
    assert isclose(PA.median,8) and isclose(PB.median,8)
    assert isclose(PA.variance,1.2) and isclose(PB.variance,15)
    assert (PA.q1,PA.q3,PB.q1,PB.q3)==(7,9,5,10)
    assert (PA.iqr,PB.iqr,PA.value_range,PB.value_range)==(2,5,4,13)
    assert (count_at_most(QUEUE_A,10),count_at_most(QUEUE_B,10))==(10,8)
    assert (count_at_most(QUEUE_A,5),count_at_most(QUEUE_B,5))==(0,3)
    assert (PO.mean,PO.median,PO.iqr)==(10,8,2) and isclose(PO.variance,45.2)
    assert isclose(RAW.mean,7.1) and isclose(RAW.variance,2.29)
    assert isclose(GROUPED.mean,7.6) and isclose(GROUPED.variance,2.44)
    assert isclose(weighted_mean(COHORTS),6.5)
    assert isclose(EA.mean,8) and isclose(EB.mean,8)
    assert (EA.median,EB.median,EA.iqr,EB.iqr)==(8,8,1.5,4)
    assert isclose(EA.variance,2) and isclose(EB.variance,11.5)
    return True

if __name__=='__main__':
    print('STAT14_LESSON_OK',validate(),'beats',len(BEATS),'words',sum(len(b.voice.split()) for b in BEATS))
