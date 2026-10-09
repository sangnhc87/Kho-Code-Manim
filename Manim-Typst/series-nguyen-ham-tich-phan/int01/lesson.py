"""INT01 – Going backwards from differentiation: mathematically checked content.
This module must be importable without Manim, Typst or network access.
"""
from dataclasses import dataclass
from math import isclose
import sympy as sp

x,t=sp.symbols('x t', real=True)
F=x**2
f=2*x
C=sp.Symbol('C', real=True)
VELOCITY=2*t+1
POSITION=t**2+t+2
PRACTICE_DERIVATIVE=3*x**2
PRACTICE_PRIMITIVE=x**3+4

CHAPTERS=(
    'Câu hỏi đi ngược đạo hàm',
    'Tìm lại hàm số đã biết đạo hàm',
    'Vì sao có hằng số C?',
    'Các tiếp tuyến có cùng hệ số góc',
    'Hai nguyên hàm sai khác một hằng số',
    'Xác định nguyên hàm bằng một điều kiện',
    'Ứng dụng: tìm vị trí từ vận tốc',
    'Tự luyện và tổng kết',
)
@dataclass(frozen=True)
class Segment:
    chapter:int
    step:int
    title:str
    takeaway:str
    voice:str
    formula:str
    visual:str
    duration:float=27.0

ROWS=[
[
('Nhìn từ điều đã biết','Đạo hàm cho biết mức thay đổi của hàm số.','Khi biết hàm số F, ta có thể tìm đạo hàm của nó. Nhưng bài học hôm nay đặt ra câu hỏi theo hướng ngược lại. Nếu chỉ biết tốc độ thay đổi, liệu ta có thể khôi phục hàm số ban đầu không?','definition','question'),
('Một câu hỏi rất cụ thể','Biết đạo hàm bằng 2x. Hãy tìm một hàm số.','Giả sử một hàm số có đạo hàm tại mọi điểm bằng hai lần hoành độ x. Thử bắt đầu bằng những hàm số quen thuộc, rồi lấy đạo hàm để kiểm tra. Chúng ta chưa cần đến một công thức mới.','f','question'),
('Quan sát đường thẳng','Đồ thị y = 2x biểu diễn giá trị đạo hàm.','Đường thẳng đang xuất hiện biểu diễn giá trị hai x. Với x dương thì đạo hàm dương; khi x âm thì đạo hàm âm; tại x bằng không thì đạo hàm bằng không. Đồ thị này là đồ thị của đạo hàm, chưa phải hàm cần tìm.','f','question'),
('Mục tiêu của bài','Tìm F sao cho F\'(x) = f(x).','Ta sẽ tìm một hàm F có đạo hàm bằng f, tìm hiểu vì sao không chỉ có một đáp án, và cách sử dụng một điều kiện ban đầu để chọn đúng một hàm. Hãy nhìn cả đồ thị lẫn công thức.','definition','question')],
[
('Thử một ứng viên','Đạo hàm của x² là 2x.','Ta biết đạo hàm của x bình phương bằng hai x. Vậy F của x bằng x bình phương đáp ứng đúng yêu cầu. Đây là một nguyên hàm của hàm f bằng hai x, trên toàn bộ trục số thực.','square','reverse'),
('Thấy rõ bằng tiếp tuyến','Tại x = 1, hệ số góc tiếp tuyến bằng 2.','Trên parabol, tại hoành độ một, hệ số góc tiếp tuyến bằng hai. Khi chuyển tới x bằng không, tiếp tuyến nằm ngang. Điều đó phù hợp hoàn toàn với biểu thức đạo hàm hai x.','derivative','tangent_move'),
('Nhớ đúng chiều suy luận','Lấy đạo hàm để kiểm tra nguyên hàm.','Ta đã đi từ yêu cầu đạo hàm bằng hai x, đoán ra hàm x bình phương, rồi lấy đạo hàm để kiểm tra. Chiều kiểm tra luôn là từ hàm tìm được quay về đạo hàm đã cho.','square','reverse'),
('Khái niệm nguyên hàm','F là nguyên hàm của f trên một khoảng I nếu F\' = f trên I.','Một cách chính xác, hàm F được gọi là nguyên hàm của f trên khoảng I khi đạo hàm của F tại mọi điểm thuộc I bằng f. Chúng ta cần nói rõ khoảng đang xét, vì một số hàm không xác định trên toàn trục số.','definition','reverse')],
[
('Có phải chỉ có x²?','x² + 2 cũng có đạo hàm là 2x.','Hãy thử cộng thêm hai vào hàm x bình phương. Đồ thị đi lên hai đơn vị, nhưng đạo hàm vẫn bằng hai x. Như vậy, chúng ta đã tìm được đáp án thứ hai.','shiftplus','family'),
('Thử thêm những giá trị khác','x² − 2, x², x² + 2 đều phù hợp.','Nếu cộng thêm âm hai, đồ thị đi xuống hai đơn vị. Cả ba đường parabol có cùng hình dạng, chỉ khác vị trí theo chiều thẳng đứng. Đạo hàm của chúng đều bằng hai x tại cùng một hoành độ.','family','family'),
('Hằng số tự do','Với mọi hằng số C, F(x) = x² + C.','Thay hai, âm hai, hay bất kỳ số thực nào bởi ký hiệu C, ta được cả một họ nguyên hàm. Phép lấy đạo hàm làm mất hằng số cộng thêm, vì đạo hàm của một hằng số bằng không.','general','family'),
('Một họ, không phải một đường','Mỗi C cho một đồ thị khác nhau.','Quan sát các đường cong xê dịch lên hoặc xuống. Ta có vô số hàm số khác nhau nhưng cùng một đạo hàm. Đó là ý nghĩa hình học của hằng số C trong phép tính nguyên hàm.','general','family_shift')],
[
('Phóng to một điểm','Xét các đồ thị tại cùng hoành độ x = 1.','Lấy một điểm có hoành độ bằng một trên từng parabol. Dù tung độ khác nhau, các tiếp tuyến tại những điểm này đều có cùng hệ số góc bằng hai. Chúng ta đang so sánh các tiếp tuyến tại cùng một hoành độ.','sameslope','tangent'),
('Ba đường tiếp tuyến song song','Đổi C không làm đổi độ dốc.','Ba đường tiếp tuyến màu vàng trên màn hình song song với nhau. Vì cộng hằng số chỉ tịnh tiến đồ thị lên xuống, nó không làm thay đổi độ dốc của đường cong. Đây là lý do trực quan cho việc đạo hàm không đổi.','sameslope','tangent'),
('Đạo hàm phụ thuộc x','Tại x khác, hệ số góc có thể thay đổi.','Khi dịch điểm xét sang một hoành độ khác, chẳng hạn x bằng âm một, hệ số góc trở thành âm hai. Cần phân biệt hai điều: hệ số góc đổi theo x, nhưng không đổi theo hằng số C tại cùng x.','derivative','tangent_move'),
('Kết luận từ hình học','Tất cả F(x) = x² + C có cùng đạo hàm 2x.','Từ ba đường parabol và các tiếp tuyến, ta đã nhìn thấy lý do cùng một đạo hàm lại ứng với nhiều hàm số. Điều này không riêng x bình phương, mà là tính chất chung của nguyên hàm trên một khoảng.','general','tangent')],
[
('So sánh hai nguyên hàm','Lấy F₁(x) = x² − 1 và F₂(x) = x² + 2.','Giờ hãy xét hai nguyên hàm khác nhau của cùng hàm hai x. Một hàm là x bình phương trừ một, hàm còn lại là x bình phương cộng hai. Ta muốn biết chúng khác nhau theo quy luật nào.','difference','difference'),
('Hiệu có thay đổi không?','F₂(x) − F₁(x) luôn bằng 3.','Tại x bằng âm một, bằng không, bằng một hay bất kỳ giá trị nào, khoảng cách theo phương thẳng đứng giữa hai đường đều bằng ba. Về đại số, hiệu của chúng rút gọn thành hằng số ba.','constantdifference','difference'),
('Tại sao luôn như vậy?','Đạo hàm của hiệu bằng 0.','Nếu F một và F hai có cùng đạo hàm trên một khoảng, đạo hàm của F hai trừ F một bằng không. Theo tính chất hàm có đạo hàm bằng không trên một khoảng, hiệu đó là hằng số trên khoảng ấy.','zeroderivative','difference'),
('Chú ý miền xác định','Kết luận về hằng số được xét trên từng khoảng.','Trong các bài toán có miền xác định bị tách rời, ta phải xét từng khoảng riêng biệt. Không được khẳng định cùng một hằng số C cho hai khoảng rời nhau nếu không có thêm điều kiện.','interval','difference')],
[
('Chọn một thành viên của họ','Biết thêm F(1) = 3.','Chúng ta vẫn có vô số hàm x bình phương cộng C. Nhưng bài toán cho biết đồ thị cần đi qua điểm có hoành độ một và tung độ ba. Điều kiện này sẽ giúp xác định hằng số chưa biết.','condition','condition'),
('Thay tọa độ điểm','1 + C = 3.','Thay x bằng một vào F của x bằng x bình phương cộng C. Ta được một cộng C bằng ba. Đây là phương trình đơn giản để tìm hằng số.','solveC','condition'),
('Xác định C','C = 2, nên F(x) = x² + 2.','Giải phương trình ta được C bằng hai. Khi ấy đồ thị tương ứng chính là parabol đi qua điểm một phẩy ba. Hình động đang đưa đường cong đến đúng vị trí của điểm điều kiện.','answerC','condition_shift'),
('Kiểm tra hai điều kiện','F\'(x) = 2x và F(1) = 3.','Đừng dừng ở kết quả C bằng hai. Hãy kiểm tra cả hai yêu cầu: đạo hàm phải bằng hai x, đồng thời giá trị hàm tại x bằng một phải bằng ba. Khi cả hai đều đúng, lời giải mới hoàn chỉnh.','answerC','condition')],
[
('Vận tốc chưa cho vị trí','Giả sử v(t) = 2t + 1 mét mỗi giây.','Trong chuyển động thẳng theo một trục tọa độ, vận tốc là đạo hàm của tọa độ theo thời gian. Nếu biết vận tốc bằng hai t cộng một, liệu ta có biết vật đang ở vị trí nào tại mỗi thời điểm không?','velocity','motion_v'),
('Khôi phục hàm tọa độ','s(t) = t² + t + C.','Do đạo hàm của t bình phương cộng t là hai t cộng một, nên một nguyên hàm của vận tốc là t bình phương cộng t. Ta vẫn phải cộng hằng số C, vì riêng vận tốc không cho biết tọa độ ban đầu.','position','motion_s'),
('Tọa độ ban đầu','Nếu s(0) = 2 mét thì C = 2.','Giả sử tại thời điểm không giây, vật ở vị trí hai mét so với gốc tọa độ. Thay t bằng không vào biểu thức s, ta tìm được C bằng hai. Đây chính là ý nghĩa thực tế của hằng số nguyên hàm.','position_final','motion_s'),
('Đọc đúng các đại lượng','Vận tốc là mét/giây; tọa độ là mét.','Hàm tọa độ của vật trở thành t bình phương cộng t cộng hai. Đơn vị của tọa độ là mét; vận tốc là mét trên giây. Trong bài toán thực tế, phải phân biệt tọa độ, độ dời và tổng quãng đường đi được.','position_final','motion_s')],
[
('Bài tập tự luyện','Biết G\'(x) = 3x² và G(1) = 5.','Trước khi xem lời giải, em hãy thử tìm một hàm G có đạo hàm bằng ba x bình phương và đi qua điểm một phẩy năm. Hãy làm theo ba bước: tìm một nguyên hàm, thêm hằng số C, rồi dùng điều kiện để xác định C.','practice','practice'),
('Bước một: tìm họ nguyên hàm','G(x) = x³ + C.','Vì đạo hàm của x lập phương bằng ba x bình phương, họ nguyên hàm là x lập phương cộng C. Đó mới là đáp án tổng quát, chưa thỏa mãn đủ điều kiện ban đầu.','practice_primitive','practice'),
('Bước hai: dùng điều kiện','G(1) = 5 suy ra C = 4.','Thay x bằng một, ta có một cộng C bằng năm, nên C bằng bốn. Đồ thị đang được tịnh tiến để đi qua điểm có tọa độ một và năm.','practice_condition','practice_shift'),
('Bước ba: kiểm tra và ghi nhớ','G(x) = x³ + 4.','Kết quả là G bằng x lập phương cộng bốn. Đạo hàm đúng bằng ba x bình phương và giá trị tại một là năm. Từ bài này, em hãy nhớ: nguyên hàm là đi ngược đạo hàm; trên một khoảng, các nguyên hàm chỉ khác nhau một hằng số; điều kiện ban đầu giúp xác định hằng số đó.','practice_final','practice')],
]
FORMULAS={
 'definition':"F'(x) = f(x)",
 'f':"f(x) = 2x",
 'square':"F(x) = x^2",
 'derivative':"F'(x) = 2x",
 'shiftplus':"F(x) = x^2+2",
 'family':"x^2-2 quad x^2 quad x^2+2",
 'general':"F(x) = x^2+C",
 'sameslope':"F_1'(x) = F_2'(x) = 2x",
 'difference':"F_1(x) = x^2-1 quad F_2(x) = x^2+2",
 'constantdifference':"F_2(x)-F_1(x)=3",
 'zeroderivative':"(F_2-F_1)'=0",
 'interval':"F_2(x)-F_1(x)=C",
 'condition':"F(1)=3",
 'solveC':"1+C=3",
 'answerC':"F(x)=x^2+2",
 'velocity':"v(t)=2t+1",
 'position':"s(t)=t^2+t+C",
 'position_final':"s(t)=t^2+t+2",
 'practice':"G'(x)=3x^2",
 'practice_primitive':"G(x)=x^3+C",
 'practice_condition':"1+C=5",
 'practice_final':"G(x)=x^3+4",
}
SEGMENTS=tuple(Segment(i+1,j+1,*r) for i,rows in enumerate(ROWS) for j,r in enumerate(rows))

def validate():
    assert len(CHAPTERS)==8 and len(SEGMENTS)==32 and len(FORMULAS)>=20
    assert all(1<=s.chapter<=8 and 1<=s.step<=4 and s.formula in FORMULAS for s in SEGMENTS)
    assert all(s.voice and s.takeaway and s.title and s.visual and s.duration>=20 for s in SEGMENTS)
    assert sp.simplify(sp.diff(F,x)-f)==0
    for value in [-4,-2,0,2,5]:
        assert sp.simplify(sp.diff(F+value,x)-f)==0
    assert sp.simplify((F+2)-(F-1))==3
    assert sp.simplify((F+2).subs(x,1))==3
    assert sp.simplify(sp.diff(POSITION,t)-VELOCITY)==0
    assert POSITION.subs(t,0)==2
    assert sp.simplify(sp.diff(PRACTICE_PRIMITIVE,x)-PRACTICE_DERIVATIVE)==0
    assert PRACTICE_PRIMITIVE.subs(x,1)==5
    return True
validate()
