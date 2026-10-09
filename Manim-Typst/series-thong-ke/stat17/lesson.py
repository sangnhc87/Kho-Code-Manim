"""STAT17: Pearson correlation and ordinary least squares (OLS).
The classroom observations are invented; this is descriptive, not causal inference.
Keep all displayed statistics derived from this module, never from hard-coded chart numbers.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import sqrt, isfinite
from fractions import Fraction

X = (1, 2, 3, 4, 5, 6, 7, 8)
Y = (2, 4, 3, 5, 4, 6, 7, 9)
NEGATIVE_Y = tuple(10 - y for y in Y)
CURVED_X = tuple(float(x)-4.5 for x in X)
CURVED_Y = tuple((x-4.5)**2 for x in X)
OUTLIER_Y = Y[:-1]+(18,)
PRACTICE_X = (1, 2, 3, 4, 5)
PRACTICE_Y = (3, 5, 7, 9, 11)


def pairs(x, y, minimum=2):
    if len(x)!=len(y) or len(x)<minimum:
        raise ValueError('Paired samples must have equal length >= minimum')
    if any(not isinstance(v,(float,int,Fraction)) or isinstance(v,bool) or not isfinite(float(v)) for v in (*x,*y)):
        raise ValueError('Data must be finite real numbers, no booleans')
    return tuple((float(a),float(b)) for a,b in zip(x,y))


def statistics(x=X,y=Y):
    p=pairs(x,y)
    n=len(p)
    mx=sum(a for a,b in p)/n
    my=sum(b for a,b in p)/n
    sxx=sum((a-mx)**2 for a,b in p)
    syy=sum((b-my)**2 for a,b in p)
    sxy=sum((a-mx)*(b-my) for a,b in p)
    if sxx<=0 or syy<=0:
        raise ValueError('Both variables must vary to define Pearson r and y-on-x regression')
    slope=sxy/sxx
    intercept=my-slope*mx
    corr=sxy/sqrt(sxx*syy)
    result=dict(n=n,mx=mx,my=my,sxx=sxx,syy=syy,sxy=sxy,
                slope=slope,intercept=intercept,r=corr,r2=corr**2)
    assert -1-1e-12 <= corr <= 1+1e-12
    return result


def fitted(x,stats=None):
    s=stats if stats is not None else statistics()
    return s['intercept']+s['slope']*x


def residuals(x=X,y=Y):
    s=statistics(x,y)
    return tuple(b-fitted(a,s) for a,b in pairs(x,y))


def losses(x=X,y=Y):
    e=residuals(x,y)
    return sum(v*v for v in e)


def decimal(value,ndigits=2):
    if not isfinite(float(value)):
        raise ValueError('Nonfinite number')
    s=f'{value:.{ndigits}f}'.replace('.',',')
    return s


@dataclass(frozen=True)
class Beat:
    chapter:int
    step:int
    title:str
    thesis:str
    voice:str
    duration:float=38.0

CHAPTERS=(
 'TỪ HAI ĐẠI LƯỢNG ĐẾN ĐÁM MÂY ĐIỂM',
 'CHIỀU HƯỚNG VÀ ĐỘ MẠNH CỦA TƯƠNG QUAN',
 'HỆ SỐ TƯƠNG QUAN PEARSON',
 'VÌ SAO CẦN ĐƯỜNG HỒI QUY?',
 'PHƯƠNG PHÁP BÌNH PHƯƠNG TỐI THIỂU',
 'DỰ ĐOÁN VÀ ĐÁNH GIÁ MÔ HÌNH',
 'NGOẠI LỆ, PHI TUYẾN VÀ NHÂN QUẢ',
 'BÀI TẬP TỔNG HỢP VÀ KẾT LUẬN',
)
ROWS=[
 [
 ('Từ bảng dữ liệu đến câu hỏi', 'Tám cặp số liệu: thời gian ôn tập và điểm giả lập.',
  'Giả sử tám bạn học sinh có số giờ ôn tập lần lượt từ một đến tám. Điểm kiểm tra mô phỏng của các bạn là hai, bốn, ba, năm, bốn, sáu, bảy, chín. Ta cần khám phá giữa hai đại lượng có xu hướng gì. Đây chỉ là bộ dữ liệu học tập, không phải bằng chứng rằng ôn thêm một giờ sẽ gây ra mức tăng điểm nhất định.'),
 ('Mỗi học sinh là một điểm', 'Hoành độ x là giờ ôn; tung độ y là điểm.',
  'Mỗi cặp số phải được biểu diễn bằng đúng một chấm trên mặt phẳng tọa độ. Chẳng hạn bạn đầu tiên tương ứng với điểm có hoành độ một, tung độ hai. Khi đọc biểu đồ phân tán, đừng tách các cặp số rồi sắp xếp riêng từng cột, vì làm như vậy sẽ phá vỡ quan hệ giữa hai đại lượng.'),
 ('Nhận ra xu hướng đi lên', 'Khi x tăng, y nhìn chung có xu hướng tăng.',
  'Quan sát đám mây tám điểm. Các điểm không nằm trên cùng một đường thẳng, nhưng từ trái sang phải, chúng có xu hướng đi lên. Ta gọi đây là xu hướng tương quan dương. Hãy chú ý cụm từ nhìn chung, vì tại một vài vị trí, người học ôn nhiều hơn vẫn có thể nhận điểm thấp hơn một người ôn ít hơn.'),
 ('Đọc biểu đồ có giới hạn', 'Tương quan mô tả xu hướng, không tự khẳng định nguyên nhân.',
  'Một biểu đồ có xu hướng đi lên là dấu hiệu để ta nghiên cứu mối liên hệ, chứ chưa chứng minh quan hệ nhân quả. Còn có các yếu tố như năng lực ban đầu, độ khó bài kiểm tra và cách chọn học sinh. Trong bài học này, chúng ta sẽ đo mức độ liên hệ tuyến tính, sau đó dựng một đường thẳng mô tả dữ liệu.'),
 ],
 [
 ('Ba dáng đám mây thường gặp', 'Tương quan dương, âm và không rõ xu hướng tuyến tính.',
  'Một đám mây đi lên từ trái sang phải gợi xu hướng dương. Nếu đi xuống thì gợi xu hướng âm. Nếu các điểm tỏa ra mà không có hướng tuyến tính rõ ràng, hệ số tương quan có thể gần không. Tuy vậy, gần không chưa chắc là hai đại lượng hoàn toàn không liên hệ với nhau, như chúng ta sẽ thấy ở phần sau.'),
 ('Tương quan dương ở mẫu chính', 'r dương khi x và y có xu hướng cùng chiều.',
  'Quay lại tám học sinh trong ví dụ. Điểm số tăng nhìn chung theo thời gian ôn, nên dấu của hệ số tương quan là dương. Đám mây khá gần một đường thẳng, vì vậy ta kỳ vọng độ lớn của hệ số tương quan khá cao. Ta chưa vội đoán một con số chính xác bằng mắt; công thức sẽ giúp kiểm chứng.'),
 ('Đổi hướng điểm để có tương quan âm', 'Phản chiếu theo trục ngang đổi dấu của r.',
  'Nếu thay mỗi giá trị điểm y bằng mười trừ y, các điểm được phản chiếu theo phương thẳng đứng. Xu hướng đi lên chuyển thành đi xuống. Độ chặt tuyến tính của đám mây vẫn như cũ, nhưng dấu của hệ số tương quan đổi từ dương sang âm. Như vậy dấu diễn đạt chiều hướng, còn giá trị tuyệt đối gợi mức độ chặt chẽ tuyến tính.'),
 ('Một đám mây có r bằng không', 'Không tương quan tuyến tính vẫn có thể có cấu trúc cong.',
  'Xét các giá trị nằm trên một đường cong hình chữ U đối xứng quanh hoành độ trung tâm. Bên trái đi xuống, bên phải đi lên, nên đóng góp vào tương quan tuyến tính triệt tiêu nhau. Khi đó r bằng không dù y được tính trực tiếp từ x. Đừng bao giờ diễn giải r bằng không thành khẳng định hai biến hoàn toàn độc lập.'),
 ],
 [
 ('Tìm tâm của đám mây', 'Trung bình x = 4,5; trung bình y = 5.',
  'Trước khi tính hệ số Pearson, chúng ta xác định hai trung bình. Tổng giờ ôn là ba mươi sáu nên trung bình x bằng bốn phẩy năm. Tổng điểm là bốn mươi nên trung bình y bằng năm. Giao điểm của hai đường trung bình chính là tâm của đám mây, là vị trí quan trọng trong phép tính tương quan và đường hồi quy.'),
 ('Độ lệch cùng chiều, trái chiều', 'Tích (x−x̄)(y−ȳ) cho biết hướng đóng góp.',
  'Một điểm ở góc trên bên phải so với tâm có hai độ lệch dương, nên tích của chúng dương. Điểm ở dưới bên trái có hai độ lệch âm nên tích vẫn dương. Trái lại, hai góc còn lại tạo tích âm. Tổng các tích độ lệch đo xu hướng biến thiên cùng chiều hay ngược chiều, nhưng còn phụ thuộc đơn vị đo.'),
 ('Chuẩn hóa để được hệ số r', 'r = Sxy / căn(Sxx × Syy).',
  'Ta chia tổng tích độ lệch cho căn bậc hai của tích hai tổng bình phương độ lệch. Đó là hệ số tương quan Pearson. Mẫu chính có Sxx bằng bốn mươi hai, Syy bằng ba mươi sáu và Sxy bằng ba mươi sáu. Do đó r bằng ba mươi sáu chia căn của một nghìn năm trăm mười hai, xấp xỉ không phẩy chín hai sáu.'),
 ('Đọc r đúng mức độ', 'r ≈ 0,926 là tương quan tuyến tính dương khá mạnh.',
  'Giá trị r luôn nằm từ âm một đến một nếu cả hai biến đều có độ phân tán khác không. Trong ví dụ này, r xấp xỉ không phẩy chín hai sáu cho thấy mối liên hệ tuyến tính dương khá mạnh trong tám quan sát. Nhưng tám điểm là một mẫu rất nhỏ, và giá trị r không phải là phần trăm xác suất hay mức tăng điểm khi ôn thêm.'),
 ],
 [
 ('Tìm một đường thẳng mô tả', 'Đường dự đoán có dạng ŷ = a + bx.',
  'Bây giờ chúng ta muốn vẽ một đường thẳng đi qua vùng trung tâm của đám mây để dự đoán y từ x. Ta chọn mô hình có dạng y mũ bằng a cộng b nhân x. Kí hiệu y mũ chỉ giá trị dự đoán, không phải điểm số thực tế của từng bạn. Hai tham số a và b sẽ được xác định từ số liệu.'),
 ('Hiểu hệ số góc b', 'b = Sxy / Sxx = 6/7.',
  'Hệ số góc dương khiến đường dự đoán đi lên. Với số liệu đang xét, tổng tích độ lệch bằng ba mươi sáu và tổng bình phương độ lệch x bằng bốn mươi hai. Do đó hệ số góc bằng ba mươi sáu phần bốn mươi hai, rút gọn thành sáu phần bảy. Đây là mức thay đổi của giá trị dự đoán khi x tăng một đơn vị trong mô hình tuyến tính.'),
 ('Hiểu hệ số tự do a', 'a = ȳ − b x̄ = 8/7.',
  'Một tính chất quan trọng là đường hồi quy tuyến tính có hệ số tự do đi qua tâm của đám mây. Từ trung bình y bằng năm, trung bình x bằng bốn phẩy năm và hệ số góc sáu phần bảy, ta suy ra a bằng tám phần bảy. Vậy phương trình dự đoán hoàn chỉnh là y mũ bằng tám phần bảy cộng sáu phần bảy nhân x.'),
 ('Đặt đường dự đoán lên dữ liệu', 'Một đường thẳng mô tả xu hướng, không đi qua mọi điểm.',
  'Khi đường dự đoán xuất hiện trên biểu đồ, ta thấy có điểm nằm phía trên, có điểm nằm phía dưới. Không cần buộc đường đi qua mọi quan sát, vì dữ liệu thực tế có dao động. Một mô hình tốt theo bình phương tối thiểu là mô hình cân bằng các độ lệch theo một tiêu chí được xác định rõ, chứ không phải đường được vẽ tùy ý bằng mắt.'),
 ],
 [
 ('Thế nào là phần dư?', 'Phần dư = y thực tế − ŷ dự đoán.',
  'Khoảng cách thẳng đứng từ một điểm đến đường dự đoán được gọi là phần dư có dấu. Nếu điểm nằm phía trên, phần dư dương; nếu ở phía dưới, phần dư âm. Cần đo khoảng cách theo phương thẳng đứng vì mô hình đang dự đoán y theo x. Ta không dùng khoảng cách vuông góc đến đường thẳng trong phương pháp bình phương tối thiểu thông thường này.'),
 ('Vì sao bình phương phần dư?', 'Bình phương giúp các sai lệch không triệt tiêu dấu.',
  'Nếu cộng trực tiếp phần dư dương và âm, chúng có thể bù trừ nhau và che khuất mức độ sai lệch. Bình phương từng phần dư giúp mọi đóng góp không âm, đồng thời phạt mạnh hơn các dự đoán lệch xa. Vì vậy ta chọn đường thẳng làm nhỏ nhất tổng bình phương phần dư. Đây là nguyên tắc bình phương tối thiểu thường dùng.'),
 ('Tìm b bằng cực tiểu tổng bình phương', 'b = Sxy / Sxx khi Sxx > 0.',
  'Đặt tổng bình phương phần dư là một hàm của hai tham số a và b, rồi tìm giá trị nhỏ nhất. Kết quả cho công thức hệ số góc bằng Sxy chia Sxx, còn hệ số tự do bằng trung bình y trừ b nhân trung bình x. Công thức này chỉ phù hợp khi x có biến thiên; nếu mọi x đều như nhau, ta không thể xác định hệ số góc từ mẫu.'),
 ('Đường hồi quy không phải đường nối điểm', 'Đường thẳng tối ưu cho toàn bộ dữ liệu theo tiêu chí SSE.',
  'Khi nhìn đường hồi quy, em đừng nối các chấm thành đường gấp khúc, cũng không chọn hai điểm bất kỳ rồi coi đó là mô hình duy nhất. Đường hồi quy dùng thông tin của cả tám cặp quan sát. Tổng bình phương phần dư, viết tắt là SSE, cho phép kiểm chứng tính tối ưu bằng cách so sánh các đường thẳng ứng viên.'),
 ],
 [
 ('Dự đoán tại x = 5', 'ŷ(5) = 38/7 ≈ 5,43.',
  'Ta thử dùng đường hồi quy để dự đoán điểm số khi một học sinh ôn năm giờ. Thay x bằng năm vào phương trình, ta được y mũ bằng ba mươi tám phần bảy, khoảng năm phẩy bốn ba. Giá trị dự đoán có thể không trùng điểm số quan sát, vì dự đoán là giá trị trên đường mô hình, không phải quy tắc gán điểm chính xác cho từng người.'),
 ('Nội suy và ngoại suy', 'Dự đoán trong miền x quan sát đáng tin cậy hơn ngoài miền.',
  'Trong bộ dữ liệu, x chỉ nằm từ một đến tám. Dự đoán tại x bằng năm là nội suy trong vùng đã quan sát. Nếu cố dự đoán tại hai mươi giờ, ta đã ngoại suy rất xa khỏi dữ liệu. Quan hệ thật có thể đổi dạng hoặc bị giới hạn điểm tối đa, nên không nên dùng đường thẳng một cách máy móc ở ngoài phạm vi ấy.'),
 ('R bình phương diễn đạt điều gì?', 'R² ≈ 0,857 là mức giải thích biến thiên trong mẫu.',
  'Với hồi quy tuyến tính đơn có hệ số tự do, R bình phương bằng bình phương của hệ số tương quan Pearson. Trong mẫu này, R bình phương bằng sáu phần bảy, khoảng không phẩy tám năm bảy. Theo định nghĩa đại số, phần biến thiên y được mô hình tuyến tính giải thích trong mẫu tương ứng khoảng tám mươi lăm phẩy bảy phần trăm. Đây không phải phần trăm quan hệ nhân quả.'),
 ('Độ phù hợp không đủ để suy nhân quả', 'Mô hình mô tả liên hệ trong mẫu, chưa chứng minh tác động.',
  'Ngay cả khi đường hồi quy bám khá sát dữ liệu, ta vẫn chưa thể kết luận tăng một giờ ôn chắc chắn làm tăng đúng sáu phần bảy điểm. Có thể những người chuẩn bị tốt vốn cũng ôn nhiều hơn. Một báo cáo có trách nhiệm phải nêu độ lớn mẫu, phạm vi x, phần dư và những biến có thể ảnh hưởng đến cả hai đại lượng.'),
 ],
 [
 ('Một điểm ngoại lệ thay đổi kết quả', 'Giá trị y = 18 tại x = 8 làm đường ước lượng đổi.',
  'Giả sử quan sát cuối cùng không còn là chín điểm mà là mười tám. Đây là một giá trị rất khác những quan sát còn lại. Khi tính lại hồi quy, hệ số góc và độ tương quan đều thay đổi, dù bảy cặp dữ liệu đầu vẫn giữ nguyên. Bài học là một vài điểm có thể ảnh hưởng mạnh đến đường hồi quy, nhất là khi chúng nằm xa trung tâm theo x.'),
 ('r bằng 0 không có nghĩa không có quan hệ', 'Dữ liệu hình chữ U có r = 0.',
  'Chúng ta trở lại một đám mây hình chữ U. Tất cả tung độ được xác định chính xác bằng bình phương độ lệch của x so với trung tâm. Tuy nhiên, các cặp nằm đối xứng làm tổng tích độ lệch bằng không, nên Pearson r bằng không. Rõ ràng quan hệ phi tuyến vẫn tồn tại. Vì vậy hãy nhìn hình dạng điểm trước khi quyết định chọn mô hình tuyến tính.'),
 ('Cách chọn mẫu và biến bị bỏ sót', 'Một biến thứ ba có thể cùng ảnh hưởng đến x và y.',
  'Ở bài toán giờ ôn và điểm, năng lực ban đầu hay môi trường học có thể liên hệ với cả thời gian ôn và kết quả. Nếu không quan sát hoặc kiểm soát những yếu tố này, hệ số tương quan và đường hồi quy không tách riêng được tác động nhân quả của số giờ ôn. Dữ liệu mô tả giúp đưa ra giả thuyết, không thay thế thiết kế nghiên cứu phù hợp.'),
 ('Bốn điều cần kiểm tra trước khi báo cáo', 'Dạng đám mây, ngoại lệ, phạm vi dự đoán, nhân quả.',
  'Trước khi chấp nhận một mô hình, em hãy quan sát đám mây có gần tuyến tính không, các điểm ngoại lệ nằm ở đâu, mô hình được dùng trong phạm vi nào và kết luận có vượt quá tính mô tả hay không. Đồng thời, chú ý đơn vị đo cho hệ số góc và không lẫn r với R bình phương. Một đồ thị đẹp không thay thế được suy luận có căn cứ.'),
 ],
 [
 ('Bài tập: năm cặp dữ liệu', 'x = 1,2,3,4,5; y = 3,5,7,9,11.',
  'Đến lượt em tự giải. Một bộ dữ liệu khác gồm năm cặp: x lần lượt từ một đến năm, còn y là ba, năm, bảy, chín, mười một. Hãy tính trung bình của mỗi biến, dự đoán dấu của hệ số tương quan rồi tìm phương trình đường thẳng hồi quy. Hãy thử làm trước khi theo dõi lời giải từng phần.'),
 ('Tìm các trung bình và tổng độ lệch', 'x̄ = 3, ȳ = 7; Sxx = 10, Sxy = 20.',
  'Trung bình x của năm quan sát bằng ba, còn trung bình y bằng bảy. Tổng bình phương độ lệch x bằng mười; tổng tích độ lệch bằng hai mươi. Các điểm nằm thẳng hàng nên phép tính này tương đối gọn. Bây giờ lấy Sxy chia Sxx để tìm hệ số góc, rồi thay vào công thức tìm hệ số tự do.'),
 ('Tìm đường hồi quy và hệ số tương quan', 'ŷ = 1 + 2x; r = 1.',
  'Từ hai mươi chia mười, ta được hệ số góc bằng hai. Hệ số tự do bằng bảy trừ hai nhân ba, bằng một. Vậy phương trình đường hồi quy là y mũ bằng một cộng hai x. Toàn bộ năm điểm nằm đúng trên đường này nên các phần dư đều bằng không và hệ số tương quan Pearson bằng một.'),
 ('Kết luận bài học', 'Tương quan mô tả liên hệ; hồi quy mô tả và dự đoán có điều kiện.',
  'Qua bài học, em đã biết quan sát đám mây điểm, nhận diện tương quan dương âm và phi tuyến, tính hệ số Pearson và lập đường hồi quy tuyến tính đơn bằng bình phương tối thiểu. Khi diễn giải, cần phân biệt dữ liệu thực với giá trị dự đoán, đọc đúng R bình phương, chú ý ngoại lệ và không khẳng định nhân quả nếu chưa có chứng cứ thích hợp.'),
 ],
]
BEATS=tuple(Beat(i+1,j+1,*row) for i,chapter in enumerate(ROWS) for j,row in enumerate(chapter))

def validate():
    assert len(CHAPTERS)==8 and len(ROWS)==8 and all(len(c)==4 for c in ROWS)
    assert len(BEATS)==32 and len({b.title for b in BEATS})==32
    assert all(len(b.voice.split())>=48 for b in BEATS)
    assert all(b.duration==38 for b in BEATS)
    s=statistics()
    assert s['n']==8 and s['mx']==4.5 and s['my']==5
    assert s['sxx']==42 and s['syy']==36 and s['sxy']==36
    assert abs(s['slope']-6/7)<1e-12 and abs(s['intercept']-8/7)<1e-12
    assert abs(s['r2']-6/7)<1e-12
    assert abs(statistics(X,NEGATIVE_Y)['r']+s['r'])<1e-12
    assert abs(statistics(X,CURVED_Y)['r'])<1e-12
    assert abs(statistics(PRACTICE_X,PRACTICE_Y)['r']-1)<1e-12
    return True

if __name__=='__main__':
    print('STAT17_LESSON_OK',validate(),'beats',len(BEATS),'words',sum(len(b.voice.split()) for b in BEATS),statistics())
