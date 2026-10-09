"""STAT13 - Comparing two datasets (upper-secondary descriptive statistics).

Single source of truth for scores, population-style variance, school quartile convention.
All examples are synthetic; do not infer causality or population conclusions.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections import Counter
from math import fsum, sqrt, isclose
from stat01.lesson import SCORES
from stat07.lesson import CLASSES, FREQ
from stat12.lesson import grouped_stats


def _median(sorted_values):
    n=len(sorted_values)
    if n==0: raise ValueError('Cannot take the median of no values')
    return (sorted_values[(n-1)//2]+sorted_values[n//2])/2

@dataclass(frozen=True)
class Profile:
    n:int
    mean:float
    median:float
    mode:tuple
    q1:float
    q3:float
    value_range:float
    iqr:float
    variance:float
    sd:float
    minimum:float
    maximum:float


def profile(values):
    if not values or any(isinstance(x,bool) or not isinstance(x,(float,int)) for x in values):
        raise ValueError('Expected a non-empty sequence of numeric observations')
    vals=sorted(float(x) for x in values)
    n=len(vals)
    mean=fsum(vals)/n
    md=_median(vals)
    if n%2: lower,upper=vals[:n//2],vals[n//2+1:]
    else: lower,upper=vals[:n//2],vals[n//2:]
    # n=1 does not have nonempty halves under this quartile convention.
    if not lower:raise ValueError('Quartiles require at least two observations')
    q1,q3=_median(lower),_median(upper)
    counts=Counter(vals);highest=max(counts.values())
    modes=tuple(v for v,f in sorted(counts.items()) if f==highest)
    variance=fsum((x-mean)**2 for x in vals)/n
    return Profile(n,mean,md,modes,q1,q3,vals[-1]-vals[0],q3-q1,
                   variance,sqrt(variance),vals[0],vals[-1])

# Ten-point groups chosen to have the SAME mean, median, and mode,
# and DIFFERENT dispersion, box plots and goal-attainment frequencies.
A=(5,6,6,7,7,7,7,8,8,9)
B=(4,4,4,7,7,7,7,10,10,10)
PA=profile(A)
PB=profile(B)
GROUPED_A=grouped_stats(CLASSES,FREQ)
GROUPED_B=grouped_stats(CLASSES,(9,19,3,9))
ORIGINAL=profile(SCORES)
EXERCISE_A=(5,6,6,7,7,8,8,9)
EXERCISE_B=(4,4,5,7,7,9,10,10)
EA=profile(EXERCISE_A)
EB=profile(EXERCISE_B)


def count_at_least(values,threshold):
    return sum(x>=threshold for x in values)


def compare(values_a,values_b):
    """Numerically compare two descriptive profiles without a value judgment."""
    a,b=profile(values_a),profile(values_b)
    return {'a':a,'b':b,'mean_delta':a.mean-b.mean,'sd_delta':a.sd-b.sd,
            'iqr_delta':a.iqr-b.iqr,'same_n':a.n==b.n}

@dataclass(frozen=True)
class Beat:
    chapter:int
    step:int
    title:str
    thesis:str
    voice:str
    duration:float=33.0

CHAPTERS=(
 'VÌ SAO PHẢI SO SÁNH NHIỀU TIÊU CHÍ?',
 'SO SÁNH VỊ TRÍ TRUNG TÂM',
 'TỨ PHÂN VỊ VÀ BIỂU ĐỒ HỘP',
 'PHƯƠNG SAI VÀ ĐỘ LỆCH CHUẨN',
 'SO SÁNH HAI BẢNG SỐ LIỆU GHÉP NHÓM',
 'LỰA CHỌN CHỈ SỐ THEO MỤC TIÊU',
 'GIỚI HẠN CỦA SỐ LIỆU VÀ KẾT LUẬN',
 'BÀI TẬP TỔNG HỢP VÀ PHƯƠNG PHÁP',
)

# 32 distinct spoken passages: statement => method => interpretation => caveat.
ROWS=[
 [
 ('Hai nhóm có cùng điểm trung bình','Cùng trung bình 7 chưa chắc phân bố giống nhau.',
  'Hãy quan sát hai nhóm học sinh, mỗi nhóm gồm mười điểm kiểm tra. Nhóm A phần lớn tập trung quanh bảy, còn nhóm B có nhiều điểm bốn và mười. Điều thú vị là trung bình của cả hai nhóm đều bằng bảy. Vậy ta có thể kết luận hai nhóm có kết quả giống nhau hay không?'),
 ('Quan sát các điểm trên trục số','Đám điểm A tụ lại; B trải rộng hơn.',
  'Từng chấm trên trục số biểu diễn đúng một học sinh. Ở nhóm A, điểm thấp nhất là năm và cao nhất là chín. Ở nhóm B, biên độ mở rộng từ bốn đến mười. Khi xem hình, em có thể dự đoán nhóm B phân tán hơn, nhưng chúng ta cần đo điều đó bằng đại lượng phù hợp.'),
 ('Cùng một tâm, nhiều hình dạng','Trung bình không mô tả toàn bộ mẫu.',
  'Giữ nguyên vạch trung bình ở vị trí bảy, hãy nhìn các chấm hai bên dịch chuyển. Mẫu A và mẫu B có cùng trung bình, song số điểm tập trung gần trung bình hoàn toàn khác nhau. Một thước đo trung tâm là chưa đủ để đánh giá sự đồng đều hay mức độ chênh lệch của các kết quả.'),
 ('Đặt câu hỏi so sánh đúng','So sánh điều gì phụ thuộc mục tiêu.',
  'Nếu muốn chọn lớp học ổn định, chúng ta quan tâm đến mức độ phân tán. Nếu muốn tìm học sinh xuất sắc, phải xem phần điểm cao. Nếu muốn đánh giá mức điểm điển hình, cần xét trung vị. Bài học sẽ lần lượt ghép các chỉ số lại, để đưa ra một kết luận có căn cứ thay vì chỉ nhìn một con số.'),
 ],
 [
 ('Tính trung bình có kiểm chứng','A và B đều có tổng điểm 70, trung bình 7.',
  'Bắt đầu với số trung bình cộng. Tổng mười điểm nhóm A là bảy mươi và nhóm B cũng bằng bảy mươi. Chia cho mười, cả hai cùng có trung bình bằng bảy. Việc kiểm tra tổng và cỡ mẫu là bước quan trọng, vì không thể so sánh trung bình một cách cẩn thận nếu nhập nhầm dữ liệu.'),
 ('Trung vị cũng bằng nhau','Hai giá trị giữa đều là 7 ở cả hai nhóm.',
  'Với mười quan sát đã sắp xếp, trung vị là trung bình cộng của vị trí thứ năm và thứ sáu. Trong cả hai mẫu, hai vị trí đó cùng bằng bảy. Vì vậy trung vị đều là bảy, giống như trung bình. Tuy nhiên, hãy nhớ trung vị chỉ cho biết vị trí trung tâm, chưa đo độ rộng của dãy điểm.'),
 ('Kiểm tra mốt','Giá trị 7 xuất hiện bốn lần ở mỗi nhóm.',
  'Đếm số lần xuất hiện của từng điểm, ta thấy điểm bảy có tần số lớn nhất, đều là bốn ở hai nhóm. Như vậy cả mốt, trung vị lẫn trung bình đều trùng nhau. Đây là minh họa quan trọng: có thể ba số đo trung tâm bằng nhau nhưng mức phân tán giữa các nhóm vẫn rất khác biệt.'),
 ('Ba chỉ số trung tâm chưa đủ','Cần thêm khoảng biến thiên, IQR và độ lệch chuẩn.',
  'Trung bình, trung vị và mốt là ba câu trả lời khác nhau về vị trí điển hình. Nhưng khi cả ba đều bằng bảy, ta vẫn chưa biết nhóm nào có nhiều điểm chênh lệch lớn. Bởi vậy bước tiếp theo là xác định tứ phân vị và khoảng biến thiên. Từ những kết quả ấy, hình dạng của hai phân bố sẽ lộ rõ hơn.'),
 ],
 [
 ('Nhóm A: xác định ba tứ phân vị','A: Q1=6, Q2=7, Q3=8.',
  'Dữ liệu nhóm A đã sắp xếp tăng dần. Chia mười số thành hai nửa, mỗi nửa năm số. Trung vị nửa dưới là sáu, trung vị toàn mẫu là bảy và trung vị nửa trên là tám. Ta được bộ ba tứ phân vị sáu, bảy và tám. Ba mốc này chia mẫu theo những vị trí có ý nghĩa.'),
 ('Nhóm B: phần giữa rộng hơn','B: Q1=4, Q2=7, Q3=10.',
  'Với nhóm B, năm điểm thấp có trung vị bốn, toàn bộ mẫu vẫn có trung vị bảy, còn năm điểm cao có trung vị mười. Vì vậy nhóm B có tứ phân vị thứ nhất bằng bốn và tứ phân vị thứ ba bằng mười. Mặc dù trung vị trùng với A, một nửa dữ liệu trung tâm của B trải rộng hơn nhiều.'),
 ('Dựng hai biểu đồ hộp','Độ dài hộp A bằng 2; hộp B bằng 6.',
  'Biểu đồ hộp đặt năm mốc nhỏ nhất, tứ phân vị thứ nhất, trung vị, tứ phân vị thứ ba và lớn nhất trên một trục. Với A, hộp từ sáu đến tám nên dài hai đơn vị. Với B, hộp từ bốn đến mười nên dài sáu. Cùng một tỉ lệ trục, hộp B dài hơn rõ rệt.'),
 ('So sánh IQR và khoảng biến thiên','A: R=4, IQR=2; B: R=6, IQR=6.',
  'Khoảng biến thiên nhóm A bằng chín trừ năm, tức bốn; nhóm B bằng mười trừ bốn, tức sáu. Khoảng tứ phân vị lần lượt bằng hai và sáu. Cả hai tiêu chí đều cho thấy B phân tán hơn. Với cách dựng biểu đồ hộp không có ngoại lệ trong ví dụ này, các râu đến đúng hai cực trị.'),
 ],
 [
 ('Vì sao cần độ lệch chuẩn','Một chỉ số dùng mọi quan sát.',
  'Khoảng biến thiên chỉ dựa vào hai cực trị, còn IQR dựa vào các tứ phân vị. Độ lệch chuẩn dùng toàn bộ quan sát, qua bình phương độ lệch so với trung bình. Nếu các giá trị thường nằm xa trung bình, độ lệch chuẩn sẽ tăng. Hãy dùng lại hai dãy mười điểm để lượng hóa quan sát trực quan ban đầu.'),
 ('Phương sai của nhóm A','A: tổng bình phương độ lệch = 12.',
  'Với nhóm A có trung bình bảy, ta lấy từng điểm trừ bảy rồi bình phương. Cộng tất cả mười bình phương độ lệch thu được mười hai. Chia cho cỡ mẫu mười, phương sai bằng một phẩy hai. Đây là công thức phương sai chia cho n trong thống kê mô tả phổ thông.'),
 ('Phương sai của nhóm B','B: tổng bình phương độ lệch = 54.',
  'Thực hiện đúng quy trình cho nhóm B, tổng bình phương độ lệch bằng năm mươi bốn. Chia cho mười, phương sai bằng năm phẩy bốn. Cả hai nhóm có cùng trung bình bảy nhưng phương sai của B lớn hơn nhiều, vì số điểm nằm xa trung bình xuất hiện thường xuyên hơn.'),
 ('Kết luận bằng độ lệch chuẩn','A: s≈1,095; B: s≈2,324.',
  'Lấy căn bậc hai của mỗi phương sai, nhóm A có độ lệch chuẩn khoảng một phẩy không chín năm, nhóm B khoảng hai phẩy ba hai bốn. Theo tiêu chí độ đồng đều, A ổn định hơn B trong bộ số liệu này. Chúng ta chỉ đang mô tả mười quan sát của từng nhóm, không khẳng định mọi lớp học tương lai đều như thế.'),
 ],
 [
 ('Từ dữ liệu thô sang bảng ghép nhóm','Dùng cùng các lớp để so sánh công bằng.',
  'Ở các tập trước, chúng ta học bảng tần số ghép nhóm với bốn lớp, trung điểm năm, bảy, chín và mười một. Khi so sánh hai bảng, các khoảng lớp và đơn vị phải tương thích. Bảng A có tần số sáu, mười tám, mười bốn, hai; bảng B có tần số chín, mười chín, ba, chín.'),
 ('Hai bảng cùng trung bình ghép nhóm','Trung bình ước lượng đều là 7,6.',
  'Thay từng giá trị trong lớp bằng trung điểm và tính trung bình có trọng số. Cả bảng A và bảng B đều có bốn mươi quan sát; cả hai cho trung bình ghép nhóm bảy phẩy sáu. Nhưng hãy quan sát hình dạng histogram: bảng B có nhiều quan sát hơn ở lớp hai đầu, khác rõ với sự tập trung ở các lớp giữa của A.'),
 ('Khác biệt ở phương sai ghép nhóm','A: s²≈2,44; B: s²≈4,44.',
  'Tiếp tục tính phương sai từ trung điểm lớp. Với A, kết quả xấp xỉ hai phẩy bốn bốn, còn B xấp xỉ bốn phẩy bốn bốn. Như vậy, theo mô hình đại diện bởi trung điểm, bảng B phân tán hơn A. Đây là phép so sánh dựa trên dữ liệu ghép nhóm, không được trình bày như thể biết chính xác từng điểm gốc.'),
 ('Nói rõ giới hạn của ước lượng','Không suy ra chính xác các chỉ số gốc.',
  'Tần số của từng lớp không cho ta biết vị trí thật của mỗi quan sát bên trong lớp. Bởi vậy các trung bình và phương sai vừa tính chỉ là những số đo từ trung điểm lớp. Ta có thể dùng chúng để mô tả, so sánh gần đúng, nhưng không thể khôi phục chắc chắn các tứ phân vị hay độ lệch chuẩn chính xác của dữ liệu thô.'),
 ],
 [
 ('Mục tiêu: nhiều học sinh đạt từ 6','A: 9/10; B: 7/10 đạt ít nhất 6.',
  'Bây giờ đặt một câu hỏi thực tế hơn: mục tiêu của giáo viên là bao nhiêu học sinh đạt ít nhất sáu điểm? Ở nhóm A, chín trên mười em đạt yêu cầu, tức chín mươi phần trăm. Ở nhóm B, bảy trên mười em đạt, tức bảy mươi phần trăm. Khi mục tiêu là mức đạt, chúng ta cần đếm theo ngưỡng.'),
 ('Mục tiêu: số điểm từ 9 trở lên','A: 1/10; B: 3/10 đạt ít nhất 9.',
  'Nếu mục tiêu chuyển sang tìm học sinh có điểm rất cao, kết luận lại đổi chiều. Nhóm A chỉ có một điểm từ chín trở lên, còn nhóm B có ba điểm. Các tỉ lệ tương ứng là mười và ba mươi phần trăm. Vì vậy một nhóm có độ phân tán lớn hơn không tự động là tốt hay xấu; còn tùy mục đích đánh giá.'),
 ('Không chỉ chọn theo một số đo','Trung bình bằng nhau không quyết định lựa chọn.',
  'Có lúc chúng ta quan tâm điểm trung bình, lúc khác quan tâm tỉ lệ đạt chuẩn, mức xuất sắc hoặc tính ổn định. Những mục tiêu khác nhau có thể ưu tiên các nhóm khác nhau. Trước khi so sánh, hãy nói rõ tiêu chí, tính toán đúng rồi mới đưa ra nhận xét có giới hạn, thay vì tuyên bố nhóm A hay B luôn tốt hơn.'),
 ('Quy trình ra quyết định','Mục tiêu → chỉ số → kết luận có điều kiện.',
  'Một bản phân tích thống kê đáng tin cậy thường có ba phần: mục tiêu đánh giá được phát biểu rõ; chỉ số được lựa chọn và tính đúng; kết luận gắn với số liệu cụ thể. Với mười điểm giả lập này, A có độ lệch chuẩn nhỏ hơn và tỉ lệ đạt sáu cao hơn, còn B có nhiều điểm chín và mười hơn.'),
 ],
 [
 ('So sánh cần cùng thang đo','Không đánh đồng điểm với thời gian.',
  'Nếu một mẫu ghi điểm kiểm tra trên thang mười còn mẫu kia đo thời gian làm bài bằng phút, các độ lệch chuẩn không cùng đơn vị nên không thể đem so trực tiếp. Ngay cả khi đều là điểm, việc thang điểm hoặc độ khó bài kiểm tra khác nhau cũng có thể khiến so sánh đơn thuần trở nên thiếu công bằng.'),
 ('Một giá trị cực đoan thay đổi điều gì','Trung bình và phương sai có thể nhạy với ngoại lệ.',
  'Hãy nghĩ đến một bộ dữ liệu thời gian học, trong đó một quan sát lớn bất thường. Trung bình và đặc biệt phương sai sẽ phản ứng mạnh vì các khoảng cách được bình phương. Trung vị và khoảng tứ phân vị thường bền vững hơn. Chọn chỉ số thích hợp đòi hỏi chúng ta nhận biết hình dạng phân bố và giá trị ngoại lệ.'),
 ('Quy mô mẫu và bối cảnh','Mười điểm không thay thế nghiên cứu lớn.',
  'Ví dụ đang xét chỉ có mười quan sát mỗi nhóm. Số liệu này cho phép mô tả đúng các nhóm đã quan sát, nhưng chưa đủ để kết luận về toàn bộ học sinh trong trường. Muốn suy rộng, chúng ta cần quan tâm cách chọn mẫu, tính đại diện, bối cảnh lớp học và những nguyên nhân khác có thể ảnh hưởng đến kết quả.'),
 ('Phát biểu kết luận có căn cứ','Dùng “trong mẫu này”, không suy diễn nhân quả.',
  'Một câu trả lời tốt có thể viết: trong mẫu mười điểm đã cho, hai nhóm cùng trung bình và trung vị bằng bảy, nhưng A có khoảng tứ phân vị và độ lệch chuẩn nhỏ hơn B. Do đó A đồng đều hơn theo hai tiêu chí ấy. Tránh suy ra rằng một phương pháp dạy học gây ra khác biệt khi chưa có thiết kế nghiên cứu phù hợp.'),
 ],
 [
 ('Đọc đề và kiểm tra dữ liệu','Hai mẫu tám điểm, cùng tổng 56.',
  'Bài tập tổng hợp cuối video cho hai dãy tám điểm. Hãy sắp xếp chúng, kiểm tra mỗi dãy có đúng tám số và cùng tổng năm mươi sáu. Nhiệm vụ là so sánh trung bình, trung vị, khoảng biến thiên, khoảng tứ phân vị và độ lệch chuẩn, rồi viết một kết luận phù hợp với các kết quả.'),
 ('Tính những số đo trung tâm','Cả hai: trung bình 7, trung vị 7.',
  'Vì tổng đều là năm mươi sáu và mỗi mẫu có tám quan sát, trung bình hai nhóm cùng bằng bảy. Trung vị là trung bình cộng vị trí thứ tư và thứ năm, cũng bằng bảy cho cả hai. Như vậy, các số đo trung tâm một lần nữa trùng nhau, nên ta phải chuyển sang độ phân tán để phân biệt.'),
 ('So sánh tứ phân vị và phương sai','IQR: 2 với 5; phương sai: 1,5 với 5,5.',
  'Với mẫu A, tứ phân vị thứ nhất bằng sáu, thứ ba bằng tám nên khoảng tứ phân vị bằng hai. Với mẫu B, hai tứ phân vị là bốn phẩy năm và chín phẩy năm, khoảng tứ phân vị bằng năm. Tính tiếp phương sai bằng cách chia tổng bình phương độ lệch cho tám, ta được một phẩy năm và năm phẩy năm.'),
 ('Viết kết luận và chọn mục tiêu','Hai mẫu cùng tâm; A đồng đều hơn theo IQR và s.',
  'Lấy căn bậc hai, độ lệch chuẩn A khoảng một phẩy hai hai năm, B khoảng hai phẩy ba bốn năm. Vì hai mẫu có cùng trung bình, cùng trung vị mà A có IQR và độ lệch chuẩn nhỏ hơn, ta kết luận trong mẫu đã cho, A đồng đều hơn. Bài học kết thúc bằng nguyên tắc: chọn chỉ số theo mục tiêu và nêu rõ dữ liệu chứng minh.'),
 ],
]
BEATS=tuple(Beat(i+1,j+1,*row) for i,chapter in enumerate(ROWS) for j,row in enumerate(chapter))

def validate():
    assert len(CHAPTERS)==8 and len(BEATS)==32
    assert all(len(ch)==4 for ch in ROWS)
    assert len(set(b.title for b in BEATS))==32
    assert all(len(b.voice.split())>=39 for b in BEATS)
    assert (PA.n,PB.n)==(10,10)
    assert all(isclose(p.mean,7) and isclose(p.median,7) and p.mode==(7,) for p in (PA,PB))
    assert (PA.q1,PA.q3,PB.q1,PB.q3)==(6,8,4,10)
    assert (PA.iqr,PB.iqr,PA.value_range,PB.value_range)==(2,6,4,6)
    assert isclose(PA.variance,1.2) and isclose(PB.variance,5.4)
    assert (count_at_least(A,6),count_at_least(B,6))==(9,7)
    assert (count_at_least(A,9),count_at_least(B,9))==(1,3)
    assert isclose(GROUPED_A.mean,7.6) and isclose(GROUPED_B.mean,7.6)
    assert isclose(GROUPED_A.variance,2.44) and isclose(GROUPED_B.variance,4.44)
    assert (EA.iqr,EB.iqr)==(2,5)
    assert isclose(EA.variance,1.5) and isclose(EB.variance,5.5)
    return True

if __name__=='__main__':
    print('STAT13_LESSON_OK',validate(),len(BEATS),sum(len(b.voice.split()) for b in BEATS))
