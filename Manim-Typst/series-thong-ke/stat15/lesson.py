"""STAT15: detecting misleading graphs, synthetic data only.
All measurements, labels and narration originate from this module.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import isclose, isfinite, sqrt
from typing import Sequence

BAR_VALUES=(80,100)
BAR_CROP=75
YEARS=(2020,2021,2024,2025)
YEAR_VALUES=(40,44,52,56)
PICTOGRAM_VALUES=(20,40)
CLASSES=((0,2,8),(2,6,12),(6,7,6),(7,10,9))
CLASS_COUNTS=(18,24)
CLASS_TOTALS=(30,80)
TREND_YEARS=(2020,2021,2022,2023,2024,2025)
TREND_VALUES=(50,55,60,54,58,64)
CHALLENGE_VALUES=(62,68)
CHALLENGE_CROP=60


def ratio(a:float,b:float)->float:
    if not (isfinite(a) and isfinite(b)) or b<=0:raise ValueError('Expected finite positive denominator')
    return a/b

def exaggerated_height(values:Sequence[float],baseline:float)->float:
    a,b=values
    if not all(isfinite(x) for x in (a,b,baseline)) or not baseline<min(a,b):
        raise ValueError('Baseline must be below both values')
    return (b-baseline)/(a-baseline)

def percentages(counts=CLASS_COUNTS,totals=CLASS_TOTALS)->tuple[float,...]:
    if len(counts)!=len(totals) or not counts:raise ValueError('Mismatched observations')
    result=[]
    for c,n in zip(counts,totals):
        if type(n) is not int or n<=0 or type(c) is not int or not 0<=c<=n:
            raise ValueError('Invalid count or sample size')
        result.append(100*c/n)
    return tuple(result)

def histogram_densities(classes=CLASSES):
    if not classes:raise ValueError('Empty classes')
    last=None;dens=[]
    for left,right,count in classes:
        if (any(type(v) not in (int,float) or not isfinite(v) for v in (left,right))
            or type(count) is not int or count<0 or right<=left):
            raise ValueError('Invalid histogram class')
        if last is not None and left!=last:raise ValueError('Classes are not contiguous')
        dens.append(count/(right-left));last=right
    return tuple(dens)

def time_slopes(xs=YEARS,ys=YEAR_VALUES):
    if len(xs)!=len(ys) or len(xs)<2:raise ValueError('Bad series')
    if any(xs[i+1]<=xs[i] for i in range(len(xs)-1)):
        raise ValueError('Times must strictly increase')
    if any(not isfinite(y) for y in ys):raise ValueError('Nonfinite observations')
    return tuple((ys[i+1]-ys[i])/(xs[i+1]-xs[i]) for i in range(len(xs)-1))

def changes(values=TREND_VALUES):
    if not values or values[0]<=0 or values[2]<=0:raise ValueError('Invalid baseline')
    return ((values[-1]-values[0])/values[0]*100,
            (values[3]-values[2])/values[2]*100)

@dataclass(frozen=True)
class Beat:
    chapter:int
    step:int
    title:str
    thesis:str
    voice:str
    duration:float=36.0

CHAPTERS=(
 'CỘT BỊ CẮT TRỤC TUNG',
 'ĐỔI THANG ĐO ĐỂ THAY ĐỔI ẤN TƯỢNG',
 'TRỤC THỜI GIAN KHÔNG CÁCH ĐỀU',
 'HÌNH KHỐI VÀ BIỂU TƯỢNG PHÓNG ĐẠI',
 'SỐ LƯỢNG KHÔNG THỂ THAY CHO TỈ LỆ',
 'CHỌN LỌC KHOẢNG THỜI GIAN',
 'HISTOGRAM CÓ ĐỘ RỘNG LỚP KHÁC NHAU',
 'THÁM TỬ BIỂU ĐỒ: ĐỌC VÀ SỬA',
)

# Four teaching developments for each chapter; narration must not expose internal step labels.
ROWS=[
 [
 ('Cùng hai con số, hai cảm giác','Dữ liệu A = 80 và B = 100, chênh 20.',
  'Giả sử hai cửa hàng bán được tám mươi và một trăm sản phẩm trong cùng một ngày. Người xem cần biết đơn vị, thời điểm và tổng số thực tế. Chúng ta đưa hai con số lên hai biểu đồ đặt cạnh nhau. Chỉ thay đổi cách vẽ trục, ta sẽ thấy một biểu đồ làm chênh lệch có vẻ lớn hơn rất nhiều.'),
 ('Quan sát trục bị cắt tại 75','Cột chỉ cao 5 và 25 đơn vị hiển thị.',
  'Ở bản thứ nhất, trục tung bắt đầu từ bảy mươi lăm thay vì không. Cột tám mươi chỉ cao năm phần, trong khi cột một trăm cao hai mươi lăm phần. Phần chênh vẫn là hai mươi sản phẩm, nhưng mắt ta có thể lầm tưởng cột B lớn gấp năm cột A. Đây là bẫy cảm nhận thị giác.'),
 ('Trở lại mốc 0','Tỉ số số lượng thật là 100/80 = 1,25.',
  'Bây giờ chúng ta vẽ lại cột bắt đầu từ số không trên cùng một trục. Chiều cao hai cột lần lượt phản ánh tám mươi và một trăm. Tỉ số thật chỉ bằng một phẩy hai mươi lăm, nghĩa là B lớn hơn A hai mươi lăm phần trăm. Biểu đồ cột cần có gốc không để so sánh độ dài một cách trung thực.'),
 ('Quy tắc kiểm tra biểu đồ cột','Xem mốc gốc, nhãn trục, đơn vị và dữ liệu.',
  'Khi đọc một biểu đồ cột, điều đầu tiên cần kiểm tra không phải màu sắc mà là trục tung bắt đầu ở đâu. Đối chiếu chiều cao với giá trị được ghi, xem các cột có cùng thang đo không và liệu người vẽ đã thông báo rõ nếu cắt trục hay chưa. Ta không kết luận hành vi cố ý chỉ từ một đồ thị.'),
 ],
 [
 ('Giãn và nén trục tung','Cùng dữ liệu nhưng hai cửa sổ y khác nhau.',
  'Một đường biểu diễn có thể nhìn rất dốc khi khoảng giá trị của trục tung hẹp, rồi nhìn gần như phẳng khi trục tung rộng. Dữ liệu không đổi, chỉ thay khung quan sát. Ta đặt hai phiên bản cùng bốn số bốn mươi, bốn mươi bốn, năm mươi hai và năm mươi sáu để kiểm tra trực tiếp.'),
 ('Cửa sổ hẹp tạo dốc mạnh','Khoảng trục 38–58 làm biến thiên nổi bật.',
  'Khi trục tung chỉ đi từ ba mươi tám đến năm mươi tám, thay đổi mười sáu đơn vị chiếm phần lớn chiều cao hình vẽ. Người đọc dễ cảm nhận mức tăng rất mạnh. Tuy nhiên các con số vẫn như cũ, không hề có thêm số liệu mới. Cần chú ý cả nhãn trục trước khi đánh giá tốc độ biến đổi.'),
 ('Cửa sổ rộng tạo cảm giác phẳng','Khoảng trục 0–100 cho đường bớt dốc.',
  'Giữ nguyên bốn quan sát và cùng vị trí thời gian, nhưng mở thang tung từ không đến một trăm. Đường lúc này trông phẳng hơn. Hai hình đều mô tả đúng điểm dữ liệu nếu trục được ghi rõ; sự khác biệt nằm ở cách gây ấn tượng. Độ dốc trên màn hình chưa phải tốc độ thay đổi định lượng.'),
 ('Phân biệt cột và đường','Đường có thể phóng vùng y, nhưng phải ghi rõ.',
  'Với biểu đồ đường, việc phóng một khoảng trục tung không tự động là sai vì ta có thể muốn quan sát dao động nhỏ. Điều kiện là công bố rõ các mốc, không che đi bối cảnh và không dùng độ dốc bằng mắt làm bằng chứng duy nhất. Còn với biểu đồ cột so chiều cao, mốc không thường là nguyên tắc quan trọng.'),
 ],
 [
 ('Các mốc thời gian không cách đều','2020, 2021, 2024, 2025 cách nhau 1, 3, 1 năm.',
  'Xét bốn quan sát ghi tại hai nghìn không trăm hai mươi, hai nghìn không trăm hai mươi mốt, hai nghìn không trăm hai mươi bốn và hai nghìn không trăm hai mươi lăm. Giữa hai mốc ở giữa cách nhau ba năm, còn hai khoảng ngoài chỉ cách một năm. Trước khi nối các điểm, phải quyết định trục ngang đang biểu diễn năm thật hay chỉ thứ tự quan sát.'),
 ('Giãn đều bốn mốc gây nhầm','Đặt các năm cách đều sẽ bóp méo tốc độ theo năm.',
  'Nếu đặt bốn nhãn năm ở các vị trí cách đều mà không giải thích, mắt sẽ cho rằng khoảng từ hai nghìn không trăm hai mươi mốt đến hai nghìn không trăm hai mươi bốn cũng chỉ dài như các khoảng một năm. Độ dốc đoạn nối vì thế trở nên khó so sánh. Một đồ thị theo thời gian cần trục ngang phản ánh thời gian trôi thực tế.'),
 ('Đặt đúng khoảng cách năm','Tốc độ mỗi năm là 4; 8/3; 4.',
  'Đưa các điểm về tọa độ năm thật. Đoạn đầu tăng bốn đơn vị trong một năm; đoạn giữa tăng tám đơn vị trong ba năm, nên trung bình mỗi năm tăng tám phần ba; đoạn cuối tăng bốn đơn vị trong một năm. Mốc thời gian đúng cho phép ta đánh giá biến thiên theo cùng đơn vị năm.'),
 ('Đừng bỏ các mốc không có đo đạc','Khoảng trống dữ liệu không có nghĩa giá trị bằng 0.',
  'Việc không đo vào hai năm ở giữa không có nghĩa đại lượng rơi về số không. Khi nối các mốc, đoạn thẳng chỉ là quy ước trình bày xu hướng giữa các lần đo, không chứng minh những giá trị thực sự ở từng năm thiếu. Hãy nêu rõ thời điểm có dữ liệu và tránh tạo độ chính xác giả.'),
 ],
 [
 ('Hai biểu tượng có giá trị gấp đôi','Số 20 và 40 có tỉ số đúng bằng 2.',
  'Một biểu đồ hình người hoặc hình tròn có thể dùng biểu tượng để so sánh hai quy mô. Giả sử nhóm A có hai mươi người và nhóm B có bốn mươi người. Ta mong hình ảnh thể hiện B gấp đôi A. Nhưng nếu phóng to mọi chiều dài của biểu tượng hai lần, mắt sẽ thấy một chênh lệch lớn hơn giá trị thật.'),
 ('Bẫy bán kính và diện tích','Bán kính gấp 2 thì diện tích gấp 4.',
  'Hãy nhìn hai hình tròn: hình thứ hai có bán kính gấp đôi hình thứ nhất. Công thức diện tích hình tròn là pi nhân bình phương bán kính, nên diện tích bề mặt gấp bốn. Trong khi số người chỉ gấp hai. Nếu người xem đánh giá theo diện tích, hình vẽ đã phóng đại mạnh khoảng cách.'),
 ('Phóng theo diện tích đúng tỉ lệ','Muốn diện tích gấp 2, bán kính phải nhân √2.',
  'Để diện tích của hình tròn B bằng đúng hai lần diện tích A, bán kính của B chỉ cần nhân căn bậc hai của hai, xấp xỉ một phẩy bốn một bốn. Cách vẽ này có cơ sở hình học rõ ràng. Một lựa chọn khác còn dễ đọc hơn là dùng biểu đồ cột có gốc không.'),
 ('Cẩn trọng với biểu đồ 3D','Chiều sâu và phối cảnh có thể đánh lừa mắt.',
  'Biểu đồ ba chiều thường thêm chiều sâu, đổ bóng và phối cảnh. Những yếu tố ấy có thể khiến hình ở phía trước che hình phía sau hoặc khiến khối lớn trông quá nổi bật. Khi cần so sánh những đại lượng một chiều, biểu đồ hai chiều có nhãn và trục rõ ràng thường dễ kiểm tra chính xác hơn.'),
 ],
 [
 ('Hai nhóm có quy mô khác nhau','A: 18 trên 30; B: 24 trên 80.',
  'Một lớp A có ba mươi học sinh, mười tám em hoàn thành nhiệm vụ; lớp B có tám mươi học sinh, hai mươi bốn em hoàn thành. Nếu chỉ vẽ hai cột đếm số em hoàn thành, ta thấy hai mươi bốn lớn hơn mười tám. Nhưng số học sinh của hai lớp khác nhau rất nhiều, nên cột đếm tuyệt đối chưa trả lời câu hỏi về tỉ lệ thành công.'),
 ('Đếm số lượng không đồng nghĩa hiệu quả','B có 24 em, nhưng tỉ lệ chỉ 30 phần trăm.',
  'Đúng là B có nhiều hơn A sáu em hoàn thành nhiệm vụ. Tuy nhiên khi chia cho tổng sĩ số, tỉ lệ B là hai mươi bốn trên tám mươi, bằng ba mươi phần trăm. Nếu mục tiêu là số em tuyệt đối, B đứng trước. Nếu mục tiêu là tỉ lệ hoàn thành trong lớp, kết luận sẽ khác.'),
 ('Quy đổi cùng đơn vị phần trăm','A = 60%; B = 30%.',
  'Lớp A có mười tám chia ba mươi, bằng sáu mươi phần trăm. Lớp B có hai mươi bốn chia tám mươi, bằng ba mươi phần trăm. Sau khi chuẩn hóa theo quy mô, biểu đồ tỉ lệ cho thấy A có phần trăm hoàn thành gấp đôi B. Hãy luôn kiểm tra mẫu số của mỗi tỉ lệ trước khi so sánh.'),
 ('Đọc cả số lượng lẫn mẫu số','Báo cáo đúng: n/N và phần trăm, không chỉ một con số.',
  'Một báo cáo trung thực có thể ghi cả số đếm và tỉ lệ: A là mười tám trên ba mươi, tức sáu mươi phần trăm; B là hai mươi bốn trên tám mươi, tức ba mươi phần trăm. Không cần xóa bỏ cột số lượng, chỉ cần đặt chúng đúng với mục tiêu và tránh dùng số lượng thay cho tỉ lệ.'),
 ],
 [
 ('Chọn một năm để tạo câu chuyện','Năm 2022 là 60; năm 2023 là 54.',
  'Một biểu đồ chỉ chọn hai mốc năm hai nghìn không trăm hai mươi hai và hai nghìn không trăm hai mươi ba sẽ cho thấy chỉ số giảm từ sáu mươi xuống năm mươi bốn. Đó là mức giảm sáu đơn vị, hay mười phần trăm theo mốc đầu. Kết luận giảm trong giai đoạn này là đúng, nhưng chưa nói lên toàn bộ diễn biến nhiều năm.'),
 ('Mở rộng khung thời gian','Cả dãy 2020–2025: 50, 55, 60, 54, 58, 64.',
  'Khi hiện đủ sáu năm, ta thấy chỉ số biến động lên xuống, chứ không giảm liên tục. Sau giai đoạn giảm ngắn, các năm tiếp theo có tăng trở lại. Nếu người xem chỉ được nhìn một đoạn nhỏ, họ có thể hiểu nhầm xu hướng chung. Vì thế hãy kiểm tra điểm đầu, điểm cuối và tất cả các khoảng quan sát hợp lí.'),
 ('Hai kết luận không mâu thuẫn','2022→2023 giảm 10%; 2020→2025 tăng 28%.',
  'Mức giảm từ sáu mươi xuống năm mươi bốn là mười phần trăm. Trong khi đó từ năm mươi lên sáu mươi bốn trong toàn giai đoạn, tổng mức tăng là hai mươi tám phần trăm. Hai kết quả đều đúng vì nói về hai khoảng thời gian khác nhau. Sai lầm nằm ở việc lén chuyển từ kết luận ngắn hạn sang phát biểu tuyệt đối.'),
 ('Đặt câu hỏi về cách chọn cửa sổ','Có thiếu năm, thiếu đơn vị hoặc thiếu nguồn không?',
  'Khi gặp một hình khẳng định chỉ số tăng mạnh hoặc giảm mạnh, hãy hỏi có bao nhiêu mốc được giữ lại, khoảng thời gian dài bao nhiêu và liệu người vẽ đã bỏ những năm không thuận với thông điệp hay chưa. Không đủ dữ liệu để phán đoán ý định; điều quan trọng là kiểm tra sự đầy đủ và tính nhất quán của thông tin.'),
 ],
 [
 ('Khi lớp histogram rộng không đều','Các lớp có độ rộng 2, 4, 1, 3.',
  'Một histogram được chia thành bốn khoảng: từ không đến dưới hai, từ hai đến dưới sáu, từ sáu đến dưới bảy, và từ bảy đến dưới mười. Độ rộng các lớp khác nhau. Tần số lần lượt tám, mười hai, sáu, chín. Nếu lấy nguyên tần số làm chiều cao tất cả cột, diện tích mỗi cột sẽ không còn tỉ lệ đúng với số quan sát.'),
 ('Đừng lẫn tần số và chiều cao','Lớp đông nhất có 12, nhưng không cao nhất theo mật độ.',
  'Lớp từ hai đến dưới sáu có mười hai quan sát, đông nhất trong bốn lớp. Tuy nhiên bề rộng của nó là bốn đơn vị. Một lớp khác chỉ có sáu quan sát nhưng rộng một đơn vị. Vì vậy chiều cao histogram không được chỉ căn cứ vào tần số khi độ rộng lớp khác nhau.'),
 ('Lấy tần số chia độ rộng','Mật độ lần lượt là 4, 3, 6, 3.',
  'Chúng ta chia từng tần số cho độ rộng lớp để tìm mật độ tần số. Kết quả là bốn, ba, sáu và ba. Cột ứng với lớp từ sáu đến dưới bảy cao nhất về mật độ, nhưng diện tích của nó chỉ là sáu vì lớp rộng một. Công thức quan trọng là diện tích cột bằng chiều cao nhân độ rộng.'),
 ('Kiểm tra diện tích toàn histogram','Tổng diện tích 8+12+6+9 = 35.',
  'Tổng diện tích của bốn cột sẽ là tám cộng mười hai cộng sáu cộng chín, bằng ba mươi lăm, đúng tổng số quan sát. Nếu muốn histogram diện tích tổng bằng một, ta tiếp tục chia các mật độ cho ba mươi lăm. Đây là lý do không thể vẽ histogram lớp rộng không đều bằng chiều cao tần số thô.'),
 ],
 [
 ('Thử thách: đọc quảng cáo tăng trưởng','Hai giá trị 62 và 68; trục bắt đầu từ 60.',
  'Một áp phích trình bày hai tỉ lệ khảo sát là sáu mươi hai và sáu mươi tám phần trăm. Trục tung của biểu đồ cột lại bắt đầu từ sáu mươi, khiến cột thứ nhất chỉ cao hai, còn cột thứ hai cao tám trên vùng hiển thị. Em hãy tự quan sát và chỉ ra điều gì có thể khiến người xem hiểu nhầm.'),
 ('Tính mức tăng đúng trước khi nhận xét','Chênh lệch 6 điểm phần trăm; tăng tương đối khoảng 9,68%.',
  'Tỉ lệ tăng từ sáu mươi hai lên sáu mươi tám phần trăm, chênh sáu điểm phần trăm. Nếu tính mức tăng tương đối so với sáu mươi hai, ta lấy sáu chia sáu mươi hai, được khoảng chín phẩy sáu tám phần trăm. Không được nhầm sáu điểm phần trăm với sáu phần trăm tăng tương đối; hai đại lượng khác nhau.'),
 ('Sửa biểu đồ và kiểm tra tỉ số','Chiều cao thật 68/62 ≈ 1,097, không phải 4.',
  'Khi đặt lại mốc không cho trục tung, hai cột cao sáu mươi hai và sáu mươi tám. Tỉ số chiều cao thật chỉ xấp xỉ một phẩy không chín bảy, chứ không phải bốn lần như tỉ số phần vượt quá mốc sáu mươi. Hãy ghi rõ đơn vị phần trăm và số lượng người được khảo sát nếu nguồn có cung cấp.'),
 ('Bốn câu hỏi để phát hiện biểu đồ sai lệch','Gốc trục; thang đo; mẫu số; khoảng thời gian.',
  'Tổng kết bài học, khi gặp một biểu đồ trên mạng hoặc trong báo cáo, hãy kiểm tra bốn điều: trục và đơn vị có rõ không, thang đo có nhất quán không, số đếm đi với mẫu số nào, và khung thời gian có đủ bối cảnh không. Nhận xét khách quan dựa trên số liệu đã cho, không suy diễn động cơ người trình bày.'),
 ],
]
BEATS=tuple(Beat(i+1,j+1,*r) for i,chapter in enumerate(ROWS) for j,r in enumerate(chapter))

def validate():
    assert len(CHAPTERS)==8 and len(ROWS)==8 and len(BEATS)==32
    assert all(len(ch)==4 for ch in ROWS)
    assert len({b.title for b in BEATS})==32
    assert all(len(b.voice.split())>=45 for b in BEATS)
    assert isclose(ratio(100,80),1.25)
    assert isclose(exaggerated_height(BAR_VALUES,75),5)
    assert time_slopes()==(4,8/3,4)
    assert histogram_densities()==(4,3,6,3)
    assert sum(c for _,_,c in CLASSES)==35
    assert percentages()==(60,30)
    assert all(isclose(a,b) for a,b in zip(changes(),(28,-10)))
    assert isclose(exaggerated_height(CHALLENGE_VALUES,60),4)
    assert isclose(CHALLENGE_VALUES[1]/CHALLENGE_VALUES[0],68/62)
    return True

if __name__=='__main__':print('STAT15_LESSON_OK',validate(),len(BEATS),sum(len(b.voice.split()) for b in BEATS))
