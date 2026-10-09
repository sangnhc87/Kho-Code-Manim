"""Pure Python, reproducible STAT05 data and Tukey box plot summaries."""
from __future__ import annotations
from dataclasses import dataclass
from stat01.lesson import SCORES
from stat04.lesson import quartiles, GROUP_A, GROUP_B


def box_summary(values):
    a=tuple(sorted(values))
    if not a: raise ValueError('Sample cannot be empty')
    q1,q2,q3=quartiles(a)
    iqr=q3-q1
    lo,hi=q1-1.5*iqr,q3+1.5*iqr
    included=tuple(x for x in a if lo<=x<=hi)
    if not included:raise ValueError('No values within Tukey fences')
    return dict(n=len(a), minimum=a[0], maximum=a[-1], q1=q1, median=q2, q3=q3,
        range=a[-1]-a[0], iqr=iqr, lower_fence=lo, upper_fence=hi,
        lower_whisker=included[0], upper_whisker=included[-1],
        outliers=tuple(x for x in a if x<lo or x>hi))

BASE=box_summary(SCORES)
EXTREME_DATA=tuple(sorted(SCORES)[:-1])+(30,)
EXTREME=box_summary(EXTREME_DATA)
GROUPS=(tuple(GROUP_A),tuple(GROUP_B))
COMPARE=tuple(box_summary(a) for a in GROUPS)
SAME_RANGE=((1,1,1,1,9,9,9,9),(1,4,4,5,5,6,6,9))
SPREAD=tuple(box_summary(a) for a in SAME_RANGE)
CONSTANT=box_summary((5,)*8)
EXERCISE_DATA=(2,4,4,5,5,6,7,8,8,9,20)
EXERCISE=box_summary(EXERCISE_DATA)

CHAPTERS=(
 'KHOẢNG BIẾN THIÊN VÀ HAI CỰC TRỊ',
 'NĂM MỐC ĐẶC TRƯNG VÀ KHOẢNG TỨ PHÂN VỊ',
 'DỰNG BIỂU ĐỒ HỘP TỪ 40 ĐIỂM',
 'NGƯỠNG NGOẠI LỆ VÀ BIỂU ĐỒ TUKEY',
 'SO SÁNH HAI MẪU CÓ CÙNG TRUNG VỊ',
 'CÙNG KHOẢNG BIẾN THIÊN, KHÁC PHÂN TÁN',
 'QUY ƯỚC VẼ HỘP VÀ CÁC TRƯỜNG HỢP ĐẶC BIỆT',
 'LUYỆN TẬP: ĐỌC HỘP VÀ PHÁT HIỆN NGOẠI LỆ',
)

@dataclass(frozen=True)
class Beat:
    chapter:int
    step:int
    title:str
    thesis:str
    voice:str
    duration:float=27.0

ROWS=[
 [
  ('Một câu hỏi mới','Vị trí trung tâm chưa nói hết độ phân tán.',
   'Ba tập trước đã hướng dẫn đọc dữ liệu và tìm số trung bình, trung vị, mốt, tứ phân vị. Nhưng hai lớp có thể cùng trung bình trong khi các điểm cách xa nhau rất khác. Hôm nay chúng ta sẽ đo độ trải rộng và biến bộ số liệu thành biểu đồ hộp. Mọi kết quả đều phải xuất phát từ dữ liệu thực tế được hiển thị, không phải con số chọn tùy ý.'),
  ('Tìm hai cực trị','40 điểm: nhỏ nhất 4, lớn nhất 10.',
   'Ta tiếp tục bộ bốn mươi điểm kiểm tra giả lập đã dùng ở các video đầu. Khi sắp xếp dữ liệu, điểm bốn ở đầu dãy, điểm mười ở cuối dãy. Hai giá trị này là giá trị nhỏ nhất và lớn nhất. Chúng quyết định khoảng biến thiên, nhưng chưa biểu diễn đầy đủ hình dạng các nhóm điểm nằm ở giữa.'),
  ('Độ rộng của toàn dãy','R = max − min = 10 − 4 = 6.',
   'Khoảng biến thiên được ký hiệu R, bằng giá trị lớn nhất trừ giá trị nhỏ nhất. Ta lấy mười trừ bốn, được sáu điểm. Đoạn màu nối hai cực trị trên trục số có độ dài đúng sáu. Cách tính rất nhanh, nhưng cũng có nhược điểm: toàn bộ kết quả phụ thuộc vào chỉ hai quan sát biên.'),
  ('Thay đổi một giá trị','Kéo cực trị 10 thành 30: R = 26.',
   'Hãy thử thay một điểm mười bằng ba mươi. Đây chỉ là thí nghiệm minh họa về toán học, không phải điểm số hợp lệ của thang mười. Khoảng biến thiên lập tức tăng từ sáu lên hai mươi sáu, dù ba mươi chín điểm còn lại không đổi. Vì vậy ta cần một số đo khác mô tả vùng trung tâm của dữ liệu.'),
 ],
 [
  ('Ba tứ phân vị đã học','Q1 = 6, Q2 = 7, Q3 = 8.',
   'Từ bài trước, các tứ phân vị của bốn mươi điểm lần lượt bằng sáu, bảy, tám. Ta đặt chúng lên cùng trục số với hai cực trị. Q hai chính là trung vị. Q một và Q ba là trung vị của hai nửa đã sắp xếp, theo quy ước sách giáo khoa đang dùng. Chúng không phải ba mốc chia đoạn từ bốn đến mười thành bốn đoạn bằng nhau.'),
  ('Khoảng tứ phân vị','IQR = Q3 − Q1 = 2.',
   'Khoảng tứ phân vị bằng Q ba trừ Q một. Với bộ dữ liệu này, tám trừ sáu bằng hai. Phần trục số từ sáu đến tám được tô sáng để học sinh nhìn ra vùng giữa của phân bố. IQR ít nhạy hơn khoảng biến thiên đối với một thay đổi ở cực trị, nhưng không phải hoàn toàn bất biến với mọi thay đổi dữ liệu.'),
  ('Năm số đặc trưng','4 – 6 – 7 – 8 – 10.',
   'Đặt năm mốc theo thứ tự: nhỏ nhất bốn, Q một bằng sáu, trung vị bảy, Q ba bằng tám, lớn nhất mười. Ta gọi đây là tóm tắt năm số. Nó cho phép dựng một biểu đồ hộp đơn giản. Tóm tắt năm số không biểu diễn từng tần số, vì vậy cần tránh suy diễn về hình dạng phân bố chỉ bằng năm mốc.'),
  ('So sánh R và IQR','R = 6; IQR = 2.',
   'Hai đoạn có độ dài khác nhau cùng xuất hiện trên trục số. Đoạn dài sáu cho biết dữ liệu trải rộng từ cực tiểu đến cực đại. Đoạn dài hai cho biết độ rộng phần trung tâm giữa Q một và Q ba. Khoảng biến thiên và khoảng tứ phân vị cùng đo mức độ phân tán nhưng không thể thay thế nhau. Khi giải bài, hãy ghi rõ đại lượng đang tính.'),
 ],
 [
  ('Dựng chiếc hộp','Hộp có hai mép tại Q1 = 6 và Q3 = 8.',
   'Giờ chúng ta bắt đầu xây dựng biểu đồ hộp từng bước. Đầu tiên, dựng một hình chữ nhật có cạnh trái ở Q một bằng sáu, cạnh phải ở Q ba bằng tám. Hộp biểu diễn độ trải rộng giữa hai tứ phân vị. Trên cùng thang đo, hộp rộng hơn nghĩa là IQR lớn hơn. Đây là cách nhìn rất nhanh khi so sánh nhiều mẫu.'),
  ('Vạch trung vị','Đặt đường đậm tại Q2 = 7.',
   'Vạch dọc bên trong hộp biểu thị trung vị. Với bộ số liệu này, trung vị bảy nằm giữa sáu và tám. Tuy nhiên ở dữ liệu bất đối xứng, trung vị có thể nằm gần mép trái hoặc mép phải của hộp. Không nên mặc định vạch trung vị luôn đi qua tâm hình chữ nhật. Đó là dấu hiệu cần đọc trực tiếp từ số liệu.'),
  ('Thêm hai râu','Trái dừng ở 4, phải dừng ở 10.',
   'Kế tiếp vẽ hai đoạn râu nối hộp đến các quan sát hai đầu. Với dữ liệu gốc, không có điểm nào vượt ngưỡng ngoại lệ theo quy tắc Tukey, nên râu trái đến bốn và râu phải đến mười. Hai vạch ngắn được đặt ở hai đầu râu. Tập này sẽ làm rõ sự khác nhau giữa râu chạm cực trị và râu dừng ở quan sát không ngoại lệ.'),
  ('Đọc biểu đồ hoàn chỉnh','Năm số lần lượt 4, 6, 7, 8, 10.',
   'Biểu đồ hộp đã hoàn chỉnh. Đọc từ trái sang phải, ta thu được nhỏ nhất bốn, Q một sáu, trung vị bảy, Q ba tám, lớn nhất mười. Hình hộp tóm tắt vị trí trung tâm và mức phân tán, nhưng không cho ta biết trực tiếp có bao nhiêu điểm bảy hay phân bố có mấy đỉnh. Hãy phối hợp biểu đồ hộp với biểu đồ điểm nếu cần.'),
 ],
 [
  ('Kéo một điểm ra xa','Điểm lớn nhất dịch từ 10 đến 30.',
   'Hãy quan sát một điểm số dịch từ mười sang ba mươi trên trục ngang. Trong lúc kéo, giá trị cực đại và khoảng biến thiên thay đổi liên tục, nhưng ba tứ phân vị vẫn là sáu, bảy, tám. Chuyển động này minh họa vì sao IQR ổn định trước thay đổi của một cực trị. Không được vì thế khẳng định mọi phép thay điểm đơn lẻ đều để IQR không đổi.'),
  ('Đặt hai hàng rào Tukey','Ngưỡng dưới 3 và ngưỡng trên 11.',
   'Một quy tắc nhận diện ngoại lệ phổ biến lấy Q một trừ một phẩy năm lần IQR và Q ba cộng một phẩy năm lần IQR. Với Q một sáu, Q ba tám và IQR hai, ta nhận được ngưỡng dưới bằng ba, ngưỡng trên bằng mười một. Những quan sát nằm ngoài hai ngưỡng này được đánh dấu để kiểm tra thêm.'),
  ('Râu không nằm ở hàng rào','Râu vẫn chạm 4 và 10; 30 vẽ riêng.',
   'Trong biểu đồ hộp Tukey, hai đầu râu là quan sát xa nhất vẫn còn nằm bên trong hai ngưỡng, không phải chính tọa độ ngưỡng. Với dữ liệu sau thay đổi, đầu râu trái tại bốn, đầu râu phải tại mười; điểm ba mươi được tách thành một dấu riêng. Đây là chỗ rất dễ vẽ nhầm nếu chỉ học thuộc công thức một phẩy năm IQR.'),
  ('Ngoại lệ không đồng nghĩa lỗi','30 được gắn cờ; cần bối cảnh để kết luận.',
   'Dấu chấm đỏ báo một quan sát ngoại lệ theo quy tắc IQR. Ngoại lệ không nhất thiết là lỗi nhập liệu và cũng không phải giá trị phải xóa bỏ. Khi thống kê dữ liệu thật, chúng ta cần kiểm tra đơn vị, cách ghi, nguồn số liệu và nguyên nhân. Quy tắc phát hiện giúp đặt câu hỏi, chứ không tự đưa ra kết luận về chất lượng dữ liệu.'),
 ],
]
ROWS += [
 [
  ('Hai mẫu có trung vị bằng nhau','Trung vị A và B đều là 5,5.',
   'Ta đưa vào hai bộ số liệu minh họa độc lập, không phải bốn mươi điểm của lớp. Mẫu A và mẫu B đều có trung vị năm phẩy năm. Nếu chỉ nhìn trung vị, ta sẽ bỏ qua một khác biệt quan trọng: các quan sát phân tán xa hay gần giá trị giữa. Hãy dùng hai biểu đồ hộp chung một thang số để quan sát.'),
  ('Hộp của mẫu A','Q1 = 3,5; Q3 = 7,5; IQR = 4.',
   'Mẫu A có các số từ hai đến chín. Tứ phân vị dưới bằng ba phẩy năm, tứ phân vị trên bằng bảy phẩy năm, nên IQR bằng bốn. Hộp màu xanh được dựng tương ứng trên trục. Vạch trung vị ở năm phẩy năm. Đọc ba mốc này giúp ta mô tả phần trung tâm của mẫu mà không cần xem từng điểm riêng lẻ.'),
  ('Hộp của mẫu B','Q1 = 2; Q3 = 10; IQR = 8.',
   'Mẫu B có nhiều giá trị hai và mười. Tứ phân vị dưới bằng hai và tứ phân vị trên bằng mười, nên IQR bằng tám. Hộp màu cam rộng hơn rõ rệt, trong khi trung vị của hai mẫu vẫn bằng nhau. Đây là ví dụ tốt cho thấy vì sao mô tả phân bố không thể chỉ dừng ở một số đo xu thế trung tâm.'),
  ('Kết luận đúng mức','IQR mẫu B gấp đôi mẫu A.',
   'Khi hai biểu đồ dùng cùng đơn vị, cùng tỷ lệ trục, có thể kết luận IQR của mẫu B gấp đôi mẫu A. Nhưng từ đó không thể suy ra phương sai của B cũng gấp đôi A, hay chất lượng dữ liệu của B thấp hơn. Mỗi đại lượng chỉ đo một khía cạnh. Ta sẽ học phương sai và độ lệch chuẩn kỹ hơn trong những video tiếp theo.'),
 ],
 [
  ('Hai mẫu cùng khoảng biến thiên','Nhỏ nhất 1, lớn nhất 9 cho cả hai.',
   'Bây giờ xét hai dãy tám số khác nhau về tần số nhưng cùng có cực tiểu một và cực đại chín. Do đó cả hai có khoảng biến thiên bằng tám. Các chấm được xếp thành hai hàng, cùng một hệ trục số. Từ hai đầu của dãy, ta chưa thể phân biệt được mức độ tập trung của phần giữa.'),
  ('Mẫu A phân cực','Q1 = 1; Q3 = 9; IQR = 8.',
   'Trong dãy đầu tiên, bốn giá trị bằng một và bốn giá trị bằng chín. Trung vị bằng năm, nhưng Q một bằng một, Q ba bằng chín. Chiều rộng hộp bằng tám, trải gần hết khoảng biến thiên. Đây là ví dụ phân bố gồm hai cụm xa nhau. Biểu đồ hộp cho thấy hộp rộng, nhưng bản thân nó chưa chứng minh số đỉnh của phân bố.'),
  ('Mẫu B tập trung ở giữa','Q1 = 4; Q3 = 6; IQR = 2.',
   'Ở dãy thứ hai, các giá trị giữa tập trung quanh bốn, năm và sáu; chỉ hai cực trị giữ tại một và chín. Trung vị vẫn là năm, khoảng biến thiên vẫn bằng tám, nhưng tứ phân vị dưới bằng bốn, tứ phân vị trên bằng sáu. IQR chỉ bằng hai. So hai hộp ta thấy ngay vùng giữa phân tán khác nhau.'),
  ('Biểu đồ hộp không kể hết câu chuyện','Kết hợp thêm biểu đồ điểm khi cần.',
   'Dù hai dãy có cùng cực trị và cùng trung vị, hình dạng tần số có thể khác nhau đáng kể. Khoảng biến thiên và IQR bổ sung thông tin nhưng không đủ để mô tả toàn bộ phân bố. Khi cần quan sát cụm dữ liệu, tính đối xứng hay các đỉnh, hãy dùng thêm biểu đồ điểm hoặc histogram. Đây là một thói quen tốt khi trình bày thống kê.'),
 ],
 [
  ('Hai cách dựng râu','Râu cực trị và râu theo quy tắc Tukey.',
   'Một số bài học dùng biểu đồ hộp với hai râu kéo thẳng đến giá trị nhỏ nhất và lớn nhất. Một quy ước khác, biểu đồ Tukey, đánh dấu các điểm ngoài khoảng một phẩy năm IQR và đặt râu ở quan sát hợp lệ xa nhất. Với dữ liệu có ngoại lệ, hai biểu đồ sẽ khác nhau. Đọc chú thích của đề để dùng đúng quy ước.'),
  ('Mọi giá trị đều bằng 5','R = 0; IQR = 0; hộp co thành vạch.',
   'Nếu tám quan sát đều bằng năm, giá trị nhỏ nhất, hai tứ phân vị, trung vị và giá trị lớn nhất trùng nhau. Cả khoảng biến thiên và khoảng tứ phân vị bằng không. Khi đó hình hộp không có chiều rộng; tất cả mốc nằm trên một vạch. Phần mềm vẽ tốt phải hiển thị đúng tình huống này, không tự tạo độ rộng giả.'),
  ('Nếu có nhiều số trùng','IQR bằng 0 vẫn cần xem dữ liệu gốc.',
   'Dữ liệu rời rạc có thể chứa nhiều giá trị lặp. Khi Q một bằng Q ba, IQR bằng không và hai ngưỡng một phẩy năm IQR trùng nhau. Quy tắc nhận diện ngoại lệ sẽ cần được diễn giải thận trọng theo bối cảnh. Không nên kết luận một quan sát sai chỉ vì nó nằm bên ngoài ngưỡng, nhất là khi mẫu nhỏ hoặc rất nhiều giá trị trùng.'),
  ('Điều biểu đồ không tiết lộ','Năm mốc không thay thế phân bố đầy đủ.',
   'Biểu đồ hộp giỏi tóm tắt vị trí giữa và độ phân tán, nhưng không cung cấp đầy đủ tần số hay nguyên nhân của biến thiên. Tới đây, chúng ta đã biết tính khoảng biến thiên, IQR, xác định ngoại lệ và chọn loại râu thích hợp. Trong bài thi, luôn viết rõ quy ước tứ phân vị và kiểm tra xem đề yêu cầu biểu đồ hộp năm số hay biểu đồ Tukey.'),
 ],
 [
  ('Bài thử sức với 11 giá trị','Tìm năm mốc, hai độ rộng và ngoại lệ.',
   'Hãy tự giải bài cuối với dãy đã xếp: hai, bốn, bốn, năm, năm, sáu, bảy, tám, tám, chín, hai mươi. Có mười một quan sát. Em hãy tìm ba tứ phân vị, khoảng biến thiên và IQR. Sau đó áp dụng ngưỡng một phẩy năm IQR, xác định hai đầu râu Tukey. Hãy tạm dừng hình để thực hành trước khi xem lời giải.'),
  ('Tính tứ phân vị trước','Q1 = 4; Q2 = 6; Q3 = 8.',
   'Vì số quan sát lẻ bằng mười một, trung vị là phần tử ở vị trí thứ sáu, bằng sáu. Bỏ phần tử giữa ra trước khi chia thành hai nửa. Nửa dưới có trung vị bốn, nửa trên có trung vị tám. Do đó Q một bằng bốn, Q hai bằng sáu, Q ba bằng tám. Ta kiểm tra bằng việc đánh dấu từng vị trí của dãy.'),
  ('Tính hai hàng rào','IQR = 4; ngưỡng dưới -2; ngưỡng trên 14.',
   'Khoảng tứ phân vị bằng tám trừ bốn, được bốn. Một phẩy năm lần IQR bằng sáu, nên ngưỡng dưới bằng âm hai và ngưỡng trên bằng mười bốn. Quan sát hai mươi vượt ngưỡng trên nên là một ngoại lệ theo quy tắc Tukey. Giá trị hợp lệ thấp nhất là hai, giá trị hợp lệ cao nhất là chín.'),
  ('Vẽ hộp đúng quy ước','R = 18, IQR = 4, râu 2 đến 9, điểm 20 riêng.',
   'Ta hoàn thiện hình: hộp từ bốn đến tám, trung vị tại sáu, râu trái tới hai, râu phải tới chín và điểm hai mươi đứng riêng. Khoảng biến thiên của dữ liệu gốc vẫn bằng hai mươi trừ hai, được mười tám; IQR bằng bốn. Từ đây chúng ta chuyển sang phương sai và độ lệch chuẩn để hiểu sâu hơn độ phân tán của cả dãy.'),
 ],
]
BEATS=tuple(Beat(i+1,j+1,*row) for i,rows in enumerate(ROWS) for j,row in enumerate(rows))

def validate():
    assert len(SCORES)==40 and len(BEATS)==32 and len(CHAPTERS)==8
    assert (BASE['minimum'],BASE['q1'],BASE['median'],BASE['q3'],BASE['maximum'])==(4,6,7,8,10)
    assert (BASE['range'],BASE['iqr'],BASE['lower_fence'],BASE['upper_fence'])==(6,2,3,11)
    assert BASE['outliers']==()
    assert (EXTREME['range'],EXTREME['iqr'],EXTREME['outliers'])==(26,2,(30,))
    assert (EXTREME['lower_whisker'],EXTREME['upper_whisker'])==(4,10)
    assert (COMPARE[0]['median'],COMPARE[1]['median'])==(5.5,5.5)
    assert (COMPARE[0]['iqr'],COMPARE[1]['iqr'])==(4,8)
    assert tuple(x['range'] for x in SPREAD)==(8,8)
    assert tuple(x['iqr'] for x in SPREAD)==(8,2)
    assert (CONSTANT['range'],CONSTANT['iqr'])==(0,0)
    assert (EXERCISE['q1'],EXERCISE['median'],EXERCISE['q3'])==(4,6,8)
    assert (EXERCISE['range'],EXERCISE['iqr'],EXERCISE['outliers'])==(18,4,(20,))
    assert (EXERCISE['lower_whisker'],EXERCISE['upper_whisker'])==(2,9)
    assert [b.chapter for b in BEATS]==[k for k in range(1,9) for _ in range(4)]
    assert [b.step for b in BEATS]==list(range(1,5))*8
    assert all(len(b.voice.split())>=42 for b in BEATS)
    assert sum(b.duration for b in BEATS)==864
    return True
if __name__=='__main__':print('STAT05',validate(),'beats:',len(BEATS),'planned seconds:',sum(b.duration for b in BEATS))
